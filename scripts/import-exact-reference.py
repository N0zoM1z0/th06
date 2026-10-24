#!/usr/bin/env python3
"""Admit only reproduced strict units; preserve the original conservative baseline."""
import csv,hashlib,importlib.util,json,shutil,struct,sys
from pathlib import Path
from coff import Object
ROOT=Path(__file__).resolve().parents[1]
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
b=module('baseline','reference-baseline.py');c=module('comparison','compare-coff-function.py')
def write_csv(path,fields,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
def main():
    out=ROOT/'build/authored';report=b.measure(out)
    receipt=json.loads((out/'build-receipt.json').read_text());sources={r['object']:r['source'] for r in receipt['commands']}
    # Identity review is independent of matching: these are compiler-emitted
    # default constructors, deleting wrappers and an exit callback, not written
    # authored bodies. The conservative 509-entry score already exceeds 98%.
    implicit=['AsciiManager','StageMenu','Stage','Enemy','BulletTypeSprites','GuiImpl','GuiMsgVm','ItemManager','Player','PlayerBombInfo','MainMenu']
    default_names={f'th06::{n}::{n}' for n in implicit}
    def generated(f):return f['name'] in default_names or 'scalar_deleting_destructor' in f['name'] or f['address']==0x469a30
    authored=[f for f in report['functions'] if not generated(f)]
    failed=[f for f in authored if f['status']!='exact']
    if failed:raise ValueError('cannot admit unproven authored functions: '+repr(failed))
    provenance=json.loads((ROOT/'config/source-provenance.json').read_text())
    if {r['path']:r['sha256'] for r in provenance['files']}!={r['path']:r['sha256'] for r in receipt['source_tree']}:raise ValueError('maintained sources differ from pinned upstream provenance')
    target=c.verified_target();linked=(out/'th06.exe').read_bytes()
    raw_mapping=list(csv.reader((ROOT/'_reference/gensokyoclub-th06/config/mapping.csv').open()))
    ranges=[(f['address'],f['address']+f.get('compare_size',f['size'])) for f in report['functions'] if 0x401000<=f['address']<0x43d158]
    for r in raw_mapping:
        if r[0] in ['D3DXMatrixIdentity','D3DXVec3Length']:ranges.append((int(r[1],0),int(r[1],0)+int(r[2],0)))
    cursor=0x401000;padding=[]
    for start,end in sorted(ranges):
        if start>cursor:
            data=c.pe_bytes_at(target,cursor,start-cursor)
            if cursor==0x43c6d0 and start==0x43c6e0:
                # Linker identifies the 8-byte this-adjusting ReadByte wrapper.
                if c.pe_bytes_at(target,cursor,8)!=c.pe_bytes_at(linked,cursor,8):raise ValueError('compiler adjustor thunk differs')
                data=data[8:];cursor+=8
            if any(x not in (0x90,0xcc) for x in data):raise ValueError(f'unreviewed game code gap at {cursor:#x}')
            if data:padding.append({'address':cursor,'size':len(data),'origin':'alignment'})
        cursor=max(cursor,end)
    if cursor!=0x43d158:raise ValueError('game-region end differs from reviewed extent')
    ghidra=list(csv.DictReader((ROOT/'config/ghidra-functions.csv').open()))
    mapped={int(r[1],0) for r in raw_mapping}
    extra=[r for r in ghidra if 0x401000<=int(r['address'],0)<0x43d158 and int(r['address'],0) not in mapped]
    if extra:raise ValueError('unreviewed Ghidra game-region function entries')
    matches=[];manifest=['# Reproduced strict units; complete COFF extents and relocation inventories.','']
    objs={}
    for f in authored:
        unit=f'f_{f["address"]:08x}';obj=objs.setdefault(f['object'],Object(ROOT/f['object']));fn=next(x for x in obj.functions() if x['name']==f['symbol']);code,relocs=obj.body(fn)
        kind='linked' if f['method']=='linked-raw-full-extent' else 'coff'
        manifest += [f'[units.{unit}]',f'kind = "{kind}"',f'object = "{f["object"]}"',f'symbol = {json.dumps(f["symbol"])}',f'target_address = 0x{f["address"]:08X}',f'size = {f["size"]}',f'compare_size = {len(code)}','build_receipt = "build/authored/build-receipt.json"']
        if kind=='linked':
            manifest += ['image = "build/authored/th06.exe"','map = "build/authored/th06.map"','link_receipt = "build/authored/link-receipt.json"']
            inventory=[{'offset':r['offset'],'type':'DIR32' if r['type_id']==6 else 'REL32','symbol':r['symbol']['name']} for r in relocs]
        else:inventory=[{k:r[k] for k in ['offset','type','symbol','target']} for r in f['relocations']]
        manifest.append('relocations = [')
        for r in inventory:
            fields=[f'offset = {r["offset"]}',f'type = "{r["type"]}"',f'symbol = {json.dumps(r["symbol"])}']
            if 'target' in r:fields.append(f'target = 0x{r["target"]:08X}')
            manifest.append('  { '+', '.join(fields)+' },')
        manifest += [']','']
        matches.append({'unit':unit,'address':f'0x{f["address"]:08X}','size':f['size'],'name':f['name'],'source_file':sources[f['object']],'method':f['method'],'result':'exact'})
    (ROOT/'config/match-units.toml').write_text('\n'.join(manifest))
    relocation_rows=[]
    for f in authored:
        if f.get('method')=='coff-relocation-replay':
            for r in f['relocations']:relocation_rows.append({'address':hex(f['address']),'offset':r['offset'],'symbol':r['symbol'],'target':hex(r['target']),'evidence':r['evidence']})
    write_csv(ROOT/'config/relocation-evidence.csv',['address','offset','symbol','target','evidence'],relocation_rows)
    write_csv(ROOT/'config/matches.csv',['unit','address','size','name','source_file','method','result'],matches)
    write_csv(ROOT/'config/implemented.csv',['address','name','source_file'],[{k:r[k] for k in ['address','name','source_file']} for r in matches])
    by_address={f['address']:f for f in report['functions']};match_by_address={int(r['address'],0):r for r in matches}
    functions=[];origins=[]
    for r in raw_mapping:
        a=int(r[1],0);f=by_address.get(a);match=match_by_address.get(a)
        origin='authored' if match else 'compiler' if f and generated(f) or a>=0x469110 else 'library'
        note='source and complete compiler/linker extent verified' if match else ('synthesized default constructor' if r[0] in default_names else 'scalar deleting wrapper' if 'scalar_deleting_destructor' in r[0] else 'compiler exit callback _$E10; upstream destructor label corrected' if a==0x469a30 else 'compiler EH/startup section' if origin=='compiler' else 'linked SDK/CRT region; embedded SDK inlines excluded')
        functions.append({'address':f'0x{a:08X}','size':int(r[2],0),'compare_size':f.get('compare_size',int(r[2],0)) if f else int(r[2],0),'name':r[0],'source_file':match['source_file'] if match else '', 'status':'exact' if match else 'classified'})
        origins.append({'address':f'0x{a:08X}','origin':origin,'evidence':'source/provenance + COFF/linker + target + Ghidra-region-audit','notes':note})
    functions.append({'address':'0x0043C6D0','size':8,'compare_size':8,'name':'Pbg3Reader::ReadByte this-adjustor','source_file':'','status':'classified'})
    origins.append({'address':'0x0043C6D0','origin':'compiler','evidence':'linker ?ReadByte@Pbg3Reader@th06@@WBI@AEHXZ + target raw match','notes':'compiler-generated this-adjustor; excluded from authored progress'})
    write_csv(ROOT/'config/functions.csv',['address','size','compare_size','name','source_file','status'],sorted(functions,key=lambda r:r['address']))
    write_csv(ROOT/'config/function-origins.csv',['address','origin','evidence','notes'],sorted(origins,key=lambda r:r['address']))
    fields=['address','size','name','status','method','ownership']
    write_csv(ROOT/'config/reference-baseline.csv',fields,[{'address':f'0x{f["address"]:08X}','size':f['size'],'name':f['name'],'status':f['status'],'method':f.get('method',''),'ownership':'compiler' if generated(f) else 'authored'} for f in report['functions']])
    review={'target_sha256':report['target_sha256'],'conservative_reference_functions':report['authored_functions'],'conservative_reference_bytes':report['authored_bytes'],'conservative_reference_exact_bytes':report['exact_bytes'],'reviewed_authored_functions':len(authored),'reviewed_authored_bytes':b.union_size((f['address'],f['address']+f['size']) for f in authored),'compiler_entries_within_reference_scope':sum(generated(f) for f in report['functions']),'compiler_bytes_within_reference_scope':sum(f['size'] for f in report['functions'] if generated(f)),'game_region_start':0x401000,'game_region_end_exclusive':0x43d158,'unmapped_ghidra_game_entries':len(extra),'unreviewed_game_gap_bytes':0,'padding_ranges':padding,'compiler_adjustor_bytes':8}
    (ROOT/'config/boundary-review.json').write_text(json.dumps(review,indent=2)+'\n')
    print(json.dumps({k:v for k,v in review.items() if k!='padding_ranges'},indent=2))
if __name__=='__main__':main()
