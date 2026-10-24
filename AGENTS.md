# TH06 reconstruction rules

Target only the original Japanese 1.02h PE32 executable pinned in
`config/target.toml`. Read `docs/RE_HANDOFF.md`, `docs/ORACLES.md` and
`docs/RE_WORKFLOW.md` before changing reconstruction state.

- Do not use REA. Every tool must run headless. Ghidra uses only
  `scripts/ghidra.py`; inventory exports are kept in separate
  `config/ghidra-*.csv` snapshots, never the maintained acceptance ledgers. Wine clears DISPLAY/WAYLAND_DISPLAY and disables
  winemenubuilder. Do not launch the game or GUI tools.
- One writable reconstruction session and one compiler process at a time.
  Do not delegate matching. Use low process priority and at most one CPU for
  expensive analysis; keep Ghidra heap at or below 2 GiB. Delete disposable
  PCH/PDB files after each owner. Never touch other projects' processes.
- Verify target identity before every comparison. Ghidra queries must pass
  file identity, PE mapping and six mapped-code samples. Do not patch target
  bytes. Ghidra extents and reference names remain provisional evidence.
- Exact means complete function bytes, complete extent and complete COFF
  relocation inventory, with each relocation independently resolved. Never
  mask relocation fields or infer their destinations from the operand being
  compared. Structural equality is diagnostic only.
- Mapping, ownership, source presence, compilation, strict exact and runtime
  behavior are separate claims. Unknown origin/boundary debt must remain
  visible; never shrink a denominator to make a percentage meet the goal.
- Before accepting changes, run `scripts/verify-target.py`,
  `scripts/validate-tracking.py --require-target`, affected exact replay and CI.
- Accepted units require reproducible build receipts, pinned source/toolchain,
  relocation manifest and canonical replay. Deduplicate overlapping ranges.
- No copied target code, incbin, byte arrays, fake locals/returns, arbitrary
  padding or new inline assembly to force a match. Upstream assembly and
  compiler extensions are reference evidence; retain their provenance and
  explicitly track their acceptance separately.
- Keep original executables/data, archives, toolchains, analysis databases,
  decompiler output, build products and credentials out of Git. Use
  `.private/`, `.tools/`, `.analysis/`, `build/`, `ghidra-project/` and
  `_reference/` for private state. Do not edit the pinned upstream checkout.
- Cite GensokyoClub/th06 and retain the CC0 license for reused material.
- Commit messages: `gpt-6.1-sol: ...`.
