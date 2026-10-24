#!/usr/bin/env python3
"""Replay the canonical accepted ledger with strict, complete byte comparisons."""
import argparse,importlib.util,json,sys,tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('comparison',ROOT/'scripts/compare-coff-function.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def main():
    p=argparse.ArgumentParser();p.add_argument('--unit');p.add_argument('--output',type=Path,default=ROOT/'build/exact-replay.json');a=p.parse_args()
    units=tomllib.loads((ROOT/'config/match-units.toml').read_text())['units'];rows=[]
    for name in ([a.unit] if a.unit else units):
        try:rows.append(m.compare_unit(name))
        except (OSError,KeyError,ValueError) as e:rows.append({'unit':name,'result':'error','error':str(e)})
    accepted=[r for r in rows if r['result']=='exact'];report={'units':len(rows),'exact':len(accepted),'failed':len(rows)-len(accepted),'exact_bytes':sum(r['size'] for r in accepted),'results':rows}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
    for r in rows:
        if r['result']!='exact':print(r['unit'],r.get('error',r['result']),file=sys.stderr)
    return int(report['failed']>0)
if __name__=='__main__':raise SystemExit(main())
