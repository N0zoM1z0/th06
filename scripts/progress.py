#!/usr/bin/env python3
"""Generate the public progress artifact from reviewed canonical ledgers."""
import importlib.util
import argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
def write(path,content):
    if args.check:
        if not path.is_file() or path.read_text()!=content:raise SystemExit('generated progress is stale: '+str(path))
    else:path.write_text(content)

spec=importlib.util.spec_from_file_location('status',ROOT/'scripts/report-reconstruction-status.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);s=m.status()
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="138" role="img" aria-label="TH06 authored exact {s['authored_exact_percent']:.2f} percent">
<rect width="760" height="138" rx="12" fill="#171923"/>
<text x="24" y="32" fill="#f6e9ef" font-family="sans-serif" font-size="20">TH06 · strict authored exact bytes</text>
<text x="24" y="59" fill="#f6b8c7" font-family="sans-serif" font-size="18">{s['exact_bytes']:,} / {s['authored_bytes']:,} bytes · {s['authored_exact_percent']:.2f}%</text>
<rect x="24" y="75" width="712" height="12" rx="6" fill="#343646"/><rect x="24" y="75" width="{712*s['authored_exact_percent']/100:.2f}" height="12" rx="6" fill="#d76683"/>
<text x="24" y="112" fill="#c9c9d3" font-family="sans-serif" font-size="13">{s['exact_functions']} / {s['authored_functions']} reviewed authored functions · goal ≥ 98%</text>
<text x="736" y="131" text-anchor="end" fill="#999baa" font-family="sans-serif" font-size="10">Complete function bytes · full relocation inventory · compiler/library bytes separate</text></svg>
'''
write(ROOT/'resources/progress.svg',svg)
write(ROOT/'docs/PROGRESS.md',f'''# Exact progress

Generated from canonical ledgers by `python3 scripts/progress.py`.

| Measure | Result |
| --- | --- |
| Reviewed authored functions | {s['exact_functions']} / {s['authored_functions']} exact |
| Authored exact bytes | {s['exact_bytes']:,} / {s['authored_bytes']:,} ({s['authored_exact_percent']:.2f}%) |
| Goal | At least 98% |
| Unreviewed main-game code gaps | {s['unreviewed_game_gap_bytes']} bytes |
| Unmapped Ghidra entries in main-game code | {s['unmapped_ghidra_game_entries']} |
| Conservative original reference scope | {s['conservative_reference_exact_percent']:.4f}% |

The conservative reference measurement is 508 / 509 named functions and
241,025 / 241,030 bytes. Its five-byte residual is compiler-generated exit
callback `Global.obj::_$E10`, previously mislabeled as a destructor. This score
already exceeds 98% before any ownership adjustment.

The reviewed denominator separately removes eleven implicit constructors,
four deleting wrappers and that exit callback (16 entries / 2,406 bytes).
Their classification is independent of matching. The reviewed authored
functions cover the complete game/PBG source region, with SDK inline helpers,
compiler startup/EH/adjustors, alignment and tables separately accounted for.

Canonical replay: `python3 scripts/replay-exact-units.py`. It checks maintained
source/tree/compiler/object/link receipts before comparing every complete
function extent. Structural scores, unlinked support code, semantics,
playability and whole-executable identity earn no additional credit.
''')
