#!/usr/bin/env python3
"""Report reviewed authored exact coverage; compiler/library bytes are separate."""
import argparse,csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def union(ranges):
    end=-1;total=0
    for a,b in sorted(ranges):total+=max(0,b-max(a,end));end=max(end,b)
    return total
def status():
    functions={r['address']:r for r in csv.DictReader((ROOT/'config/functions.csv').open())}
    origins=list(csv.DictReader((ROOT/'config/function-origins.csv').open()))
    authored=[functions[r['address']] for r in origins if r['origin']=='authored']
    matches=list(csv.DictReader((ROOT/'config/matches.csv').open()))
    accepted=[r for r in matches if r['result']=='exact' and r['address'] in {f['address'] for f in authored}]
    total=union((int(r['address'],0),int(r['address'],0)+int(r['size'])) for r in authored)
    exact=union((int(r['address'],0),int(r['address'],0)+int(r['size'])) for r in accepted)
    review=json.loads((ROOT/'config/boundary-review.json').read_text())
    return {'authored_functions':len(authored),'exact_functions':len(accepted),'authored_bytes':total,'exact_bytes':exact,'authored_exact_percent':100*exact/total,'goal_percent':98,'unreviewed_game_gap_bytes':review['unreviewed_game_gap_bytes'],'unmapped_ghidra_game_entries':review['unmapped_ghidra_game_entries'],'compiler_functions':sum(r['origin']=='compiler' for r in origins),'library_functions':sum(r['origin']=='library' for r in origins),'conservative_reference_exact_percent':100*review['conservative_reference_exact_bytes']/review['conservative_reference_bytes']}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--summary',action='store_true');p.parse_args();print(json.dumps(status(),indent=2))
