#!/usr/bin/env python3
"""Measure complete functions, resolving relocations from independent symbol/content evidence."""
import argparse,csv,hashlib,importlib.util,json,struct,re
from collections import defaultdict,Counter
from pathlib import Path
from coff import Object
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('comparison',ROOT/'scripts/compare-coff-function.py');compare=importlib.util.module_from_spec(spec);spec.loader.exec_module(compare)

def aliases(name):
    yield name
    if name.startswith('_'):yield name.lstrip('_')
    if name=='@__security_check_cookie@4':yield '___security_check_cookie'
    if name.startswith('th06::'):
        yield name.replace('::','_',1)

def union_size(ranges):
    end=-1;total=0
    for a,b in sorted(ranges):
        total+=max(0,b-max(a,end));end=max(end,b)
    return total

def measure(build_dir):
    ref=ROOT/'_reference/gensokyoclub-th06';target=compare.verified_target()
    mapping=[{'name':r[0],'address':int(r[1],0),'size':int(r[2],0)} for r in csv.reader((ref/'config/mapping.csv').open())]
    # Fixed provisional ownership: game/PBG code before the linked DirectX library.
    # Embedded SDK inline helpers are excluded. Startup and unreviewed candidates stay separate.
    authored=[r for r in mapping if (r['name'].startswith('th06::') or r['name']=='WinMain')]
    names=defaultdict(set)
    def put(n,a):
        for alias in aliases(n):names[alias].add(a)
    for r in mapping:put(r['name'],r['address'])
    for r in csv.DictReader((ref/'config/reccmp-functions.csv').open()):put(r['name'],int(r['address'],16))
    for r in csv.DictReader((ref/'config/reccmp-globals.csv').open()):put(r['name'],int(r['address'],16))
    for r in csv.reader((ref/'config/globals.csv').open()):put(r[0].strip(),int(r[1],0))
    # IAT identities come directly from the attested PE import descriptors.
    pe=struct.unpack_from('<I',target,60)[0];opt=pe+24;base=struct.unpack_from('<I',target,opt+28)[0]
    def at(rva,n):return compare.pe_bytes_at(target,base+rva,n)
    def cstr(rva):
        b=bytearray()
        while at(rva+len(b),1)!=b'\0':b.extend(at(rva+len(b),1))
        return b.decode('ascii')
    imports=struct.unpack_from('<I',target,opt+104)[0];i=0
    while True:
        orig,_,_,dll,iat=struct.unpack('<IIIII',at(imports+i*20,20));i+=1
        if not any([orig,dll,iat]):break
        j=0
        while True:
            ptr=struct.unpack('<I',at((orig or iat)+j*4,4))[0]
            if not ptr:break
            if not ptr&0x80000000:put('IAT:'+cstr(ptr+2),base+iat+j*4)
            j+=1
    float_rows=list(csv.DictReader((ref/'config/reccmp-floats.csv').open()))
    string_rows=list(csv.reader((ref/'config/reccmp-strings.csv').open()))
    objects=[Object(p) for p in sorted(build_dir.glob('*.obj')) if p.stem!='pragma']
    funcs=defaultdict(list)
    for obj in objects:
        for f in obj.functions():
            for alias in aliases(f['demangled']):funcs[alias].append((obj,f))
    # Resolve a section only from an independently named symbol, or its complete
    # relocation-free constant contents. Never solve from an instruction operand.
    def resolve(obj,sym):
        choices=set()
        if sym['name']=='__except_list':return 0,'VC7-x86-SEH-fs-zero'
        if sym['name'].startswith('?') and '@?' in sym['name']:
            local=sym['name'][1:].split('@',1)[0]
            if len(names.get(local,()))==1:return next(iter(names[local])),'mapped-local-static'
        if sym['type']==0x20 and len(names.get(sym['name'],()))==1:return next(iter(names[sym['name']])),'decorated-function-map'
        if sym['section']==-1:return sym['value'],'coff-absolute-symbol'
        if sym['name'].startswith('__imp_'):
            api=sym['name'][6:].lstrip('_').split('@')[0]
            choices.update(names.get('IAT:'+api,()))
        for n in [sym['name'],sym['demangled']]:
            for alias in aliases(n):choices.update(names.get(alias,()))
        if len(choices)==1:return next(iter(choices)),'symbol-map'
        if sym['section']>0:
            sec=obj.sections[sym['section']-1]
            anchors=set()
            for anchor in obj.symbols.values():
                if anchor['section']!=sym['section']:continue
                v=set()
                for n in [anchor['name'],anchor['demangled']]:
                    for a in aliases(n):v.update(names.get(a,()))
                if len(v)==1:anchors.add(next(iter(v))-anchor['value']+sym['value'])
            if len(anchors)==1:return next(iter(anchors)),'section-anchor'
            blob=sec['data']
            if blob and len(blob)>=1 and not sec['relocations'] and not sec['flags']&0x20 and sec['name'].startswith('.rdata'):
                # Read-only constant pooling: every candidate contains the whole object section.
                hits=[]
                if sym['name'].startswith('__real@'):
                    for r in float_rows:
                        a=int(r['address'],16)
                        if int(r['size'])==len(blob) and compare.pe_bytes_at(target,a,len(blob))==blob:hits.append(a+sym['value'])
                    if len(set(hits))==1:return hits[0],'mapped-float-content'
                elif sym['name'].startswith('??_C'):
                    for r in string_rows:
                        if not r or not r[0].startswith('0x'):continue
                        a=int(r[0],16)
                        if compare.pe_bytes_at(target,a,len(blob))==blob:hits.append(a+sym['value'])
                    if len(set(hits))==1:return hits[0],'mapped-string-content'
                hits=[];off=0
                while True:
                    off=target.find(blob,off)
                    if off<0:break
                    if 0x6a000<=off and off+len(blob)<=0x75b7c:hits.append(0x400000+off+sym['value'])
                    off+=1
                if len(hits)==1:return hits[0],'unique-readonly-section'
        return None,'unresolved'
    linked_path=build_dir/'th06.exe'
    linked=linked_path.read_bytes() if linked_path.is_file() else None
    linked_symbols=defaultdict(set)
    if linked is not None:
        receipt=json.loads((build_dir/'link-receipt.json').read_text())
        if hashlib.sha256(linked).hexdigest()!=receipt['output_sha256']:raise ValueError('linked output digest mismatch')
        for item in receipt['objects']:
            if hashlib.sha256((ROOT/item['object']).read_bytes()).hexdigest()!=item['object_sha256']:raise ValueError('linked input object changed')
        for line in (build_dir/'th06.map').read_text(errors='replace').splitlines():
            m=re.match(r'\s+[0-9a-fA-F]{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]{8})\s',line)
            if m:linked_symbols[m[1]].add(int(m[2],16))
    rows=[]
    for r in authored:
        candidates=funcs.get(r['name'],[])
        # Deduplicate the same symbol reachable through aliases.
        candidates=list({(str(o.path),f['index']):(o,f) for o,f in candidates}.values())
        best=None
        for obj,f in candidates:
            code,rel=obj.body(f)
            row={**r,'object':str(obj.path.relative_to(ROOT)),'symbol':f['name'],'object_size':len(code),'status':'size-mismatch','unresolved':[],'relocations':[]}
            next_address=min((x['address'] for x in mapping if x['address']>r['address']),default=0x469a5f)
            # VC7 counts trailing switch tables in COFF TotalSize. The target
            # function ledger excludes them. Compare every table byte too, and
            # accept extension only at a named local-label boundary without
            # crossing the next mapped function.
            trailing_labels=[s for s in obj.symbols.values() if s['section']==f['section'] and s['value']==f['value']+r['size'] and s['name'].startswith('$L')]
            extent_ok=len(code)==r['size'] or (len(code)>r['size'] and trailing_labels and r['address']+len(code)<=next_address)
            row['compare_size']=len(code)
            if not extent_ok:
                row['rank']=(0,-abs(len(code)-r['size']))
            else:
                expected=compare.pe_bytes_at(target,r['address'],len(code));ignored=set()
                valid=True
                for reloc in rel:
                    off=reloc['offset'];t=reloc['type_id'];s=reloc['symbol']
                    if off+4>len(code) or t not in (6,20):valid=False;continue
                    ignored.update(range(off,off+4));dest,evidence=resolve(obj,s)
                    if dest is None and linked is not None and linked_symbols.get(f['name'])=={r['address']}:
                        # Independent linker output can select an ambiguous mapped
                        # symbol. Decode only the generated image, never the target.
                        field=struct.unpack('<I',compare.pe_bytes_at(linked,r['address']+off,4))[0]
                        addend=struct.unpack_from('<I',code,off)[0]
                        generated=(field-addend+(r['address']+off+4 if t==20 else 0))&0xffffffff
                        mapped=set()
                        for n in [s['name'],s['demangled']]:
                            for alias in aliases(n):mapped.update(names.get(alias,()))
                        if generated in mapped:dest,evidence=generated,'independent-linker-selects-mapped-symbol'
                    if dest is None:row['unresolved'].append(s['name']);continue
                    addend=struct.unpack_from('<I',code,off)[0]
                    value=dest+addend-(r['address']+off+4 if t==20 else 0)
                    struct.pack_into('<I',code,off,value&0xffffffff)
                    row['relocations'].append({'offset':off,'type':'DIR32' if t==6 else 'REL32','symbol':s['name'],'target':dest,'evidence':evidence})
                row['structural_differences']=sum(a!=b for i,(a,b) in enumerate(zip(code,expected)) if i not in ignored)
                row['byte_differences']=sum(a!=b for a,b in zip(code,expected))
                row['status']='exact' if valid and not row['unresolved'] and code==expected else ('unresolved' if not row['structural_differences'] else 'mismatch')
                row['method']='coff-relocation-replay'
                row['rank']=(3 if row['status']=='exact' else 2 if not row['structural_differences'] else 1,-row['byte_differences'])
            # Whole linked bytes are a second strict route: the entire actual
            # COFF extent, including switch tables/padding, must match at the
            # independently mapped symbol address. No masked fields or truncation.
            if linked is not None and linked_symbols.get(f['name'])=={r['address']} and len(code)>=r['size']:
                expected=compare.pe_bytes_at(target,r['address'],len(code))
                generated=compare.pe_bytes_at(linked,r['address'],len(code))
                if expected==generated:
                    row['status']='exact';row['method']='linked-raw-full-extent';row['rank']=(4,0)
            if best is None or row['rank']>best['rank']:best=row
        if best is None:best={**r,'status':'missing-symbol','rank':(-1,0)}
        best.pop('rank');rows.append(best)
    denominator=union_size((r['address'],r['address']+r['size']) for r in authored)
    exact=union_size((r['address'],r['address']+r['size']) for r in rows if r['status']=='exact')
    structural=union_size((r['address'],r['address']+r['size']) for r in rows if r.get('structural_differences')==0)
    return {'target_sha256':hashlib.sha256(target).hexdigest(),'upstream_commit':'7411374cef282756ef5a8984ce896fb8db797e9e','scope':'provisional named th06 functions plus WinMain; compiler startup and unresolved origin/boundary debt tracked separately','authored_functions':len(authored),'authored_bytes':denominator,'exact_bytes':exact,'exact_percent':100*exact/denominator,'structural_bytes':structural,'structural_percent':100*structural/denominator,'statuses':dict(Counter(r['status'] for r in rows)),'functions':rows}

def main():
    p=argparse.ArgumentParser();p.add_argument('--build-dir',type=Path,default=ROOT/'build/upstream');p.add_argument('--output',type=Path,default=ROOT/'build/reference-baseline.json');a=p.parse_args()
    result=measure(a.build_dir.resolve());a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='functions'},indent=2))
if __name__=='__main__':main()
