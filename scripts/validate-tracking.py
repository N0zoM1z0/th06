#!/usr/bin/env python3
"""Validate source/ownership/manifest links without needing copyrighted files."""
import argparse,csv,json,tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--require-target',action='store_true');a=p.parse_args()
    functions=list(csv.DictReader((ROOT/'config/functions.csv').open()));origins=list(csv.DictReader((ROOT/'config/function-origins.csv').open()));matches=list(csv.DictReader((ROOT/'config/matches.csv').open()))
    units=tomllib.loads((ROOT/'config/match-units.toml').read_text())['units']
    addresses=[f['address'] for f in functions]
    if len(set(addresses))!=len(addresses):raise ValueError('duplicate function address')
    if {r['address'] for r in origins}!=set(addresses):raise ValueError('origin/function ledgers diverge')
    if len(set(r['unit'] for r in matches))!=len(matches):raise ValueError('duplicate match unit')
    if set(units)!=set(r['unit'] for r in matches):raise ValueError('unit/match ledgers diverge')
    authored={r['address'] for r in origins if r['origin']=='authored'}
    if authored!=set(r['address'] for r in matches):raise ValueError('authored denominator/accepted scope differ')
    previous_end=-1
    for r in sorted(matches,key=lambda r:int(r['address'],0)):
        u=units[r['unit']];address=int(r['address'],0);size=int(r['size'])
        if r['result']!='exact' or size!=u['size'] or address!=u['target_address']:raise ValueError('match/manifest identity differs')
        if size<=0 or u['compare_size']<size or address<previous_end:raise ValueError('invalid or overlapping authored coverage')
        previous_end=address+size
        if not (ROOT/r['source_file']).is_file():raise ValueError('missing maintained source')
        if u.get('build_receipt')!='build/authored/build-receipt.json':raise ValueError('accepted unit lacks maintained build evidence')
        if u.get('kind') not in ['linked','coff']:raise ValueError('unknown acceptance method')
        if u['kind']=='linked' and u.get('link_receipt')!='build/authored/link-receipt.json':raise ValueError('linked acceptance lacks receipt')
    review=json.loads((ROOT/'config/boundary-review.json').read_text())
    if review['unreviewed_game_gap_bytes'] or review['unmapped_ghidra_game_entries']:raise ValueError('unresolved authored boundary debt')
    if a.require_target:
        import subprocess,sys
        subprocess.run([sys.executable,str(ROOT/'scripts/verify-target.py')],check=True)
    print(f'Tracking OK: {len(matches)} authored exact units; ownership and complete extents consistent.')
if __name__=='__main__':main()
