# Current handoff

The 98% authored exact-byte goal is achieved and reproducible: 493 / 493
reviewed authored functions, 238,624 / 238,624 exact bytes. Canonical replay
passed all 493 units after a cold maintained-source compile/link.

The original conservative reference measurement remains 99.9979256%:
508 / 509 named entries, 241,025 / 241,030 bytes. The residual five-byte
upstream destructor label is compiler exit callback Global.obj::_$E10.
Ownership review separately classifies sixteen compiler-generated entries;
see `docs/BOUNDARY_AUDIT.md`. This adjustment was unnecessary to exceed 98%.

Pinned reference: GensokyoClub/th06 at
7411374cef282756ef5a8984ce896fb8db797e9e, CC0. Maintained source was copied
without body/header changes and independently rebuilt. `source-provenance.json`
records every source hash. Upstream supporting unlinked routines receive no
credit; retained var_order and x87 assembly dependencies are explicit.

All tools run headless. REA is prohibited; only its empty session state was
queried before the user disabled it, and no target was opened through REA.
Ghidra 12.1.3 initialization, six mapped-code samples and inventory passed.
The original Ghidra ledger is separate from maintained function/origin ledgers.

Reproduce with `scripts/build.py`, `scripts/replay-exact-units.py`,
`scripts/validate-tracking.py --require-target` and `scripts/ci.py`.
No original executables/data, generated products or toolchains are committed.
Whole-executable identity, semantic acceptance and runtime playability are not
claimed. This session did not launch the game.

Keep one headless compiler process active, pin expensive processes to one CPU,
use low priority and delete PCH/PDB files after each owner. Preserve compact
receipts and canonical maintained objects; remove superseded reference builds.
Commit messages use `gpt-6.1-sol: ...`.
