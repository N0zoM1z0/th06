# Reconstruction workflow

1. Inspect Git status and read the handoff, target manifest and oracle policy.
2. Run `python3 scripts/verify-target.py` and `python3 scripts/ghidra.py check`.
3. Consult the provisional function/origin ledgers. Confirm complete control
   flow, padding and ownership for the bounded address under investigation.
4. Build one owner under pinned VC7.0 flags. Preserve compact receipts and
   remove disposable PCH/PDB output. All tools run headless and serially.
5. Compare full function bytes and independently resolve every relocation.
   Store diagnostic experiments under `.analysis/`, not maintained source.
6. Admit proven source with attribution, canonical match units and replay.
   Keep unresolved source, layout and compiler-extension debt explicit.
7. Update progress SVG, evidence/handoff and tests; commit a stable checkpoint.

Reference reproduction:

```
python3 scripts/build-reference.py
python3 scripts/reference-baseline.py
```

The build uses `_reference/gensokyoclub-th06` at the pinned commit, preserves
its per-file flags, compiles one object at a time and removes PCH/PDB output.
The reference script does not overwrite the maintained match ledger.

Never add original code/data to the repository, call REA, run GUI tools or
report structural comparisons as strict exact. The target goal is at least
98% authored exact bytes with a reviewed denominator.
