# Exact progress

Generated from canonical ledgers by `python3 scripts/progress.py`.

| Measure | Result |
| --- | --- |
| Reviewed authored functions | 493 / 493 exact |
| Authored exact bytes | 238,624 / 238,624 (100.00%) |
| Unreviewed main-game code gaps | 0 bytes |
| Unmapped Ghidra entries in main-game code | 0 |
| Conservative original reference scope | 99.9979% |

The conservative reference measurement is 508 / 509 named functions and
241,025 / 241,030 bytes. Its five-byte residual is compiler-generated exit
callback `Global.obj::_$E10`, previously mislabeled as a destructor. The original
measurement is retained separately from the reviewed authored coverage.

The reviewed denominator separately removes eleven implicit constructors,
four deleting wrappers and that exit callback (16 entries / 2,406 bytes).
Their classification is independent of matching. The reviewed authored
functions cover the complete game/PBG source region, with SDK inline helpers,
compiler startup/EH/adjustors, alignment and tables separately accounted for.

Canonical replay: `python3 scripts/replay-exact-units.py`. It checks maintained
source/tree/compiler/object/link receipts before comparing every complete
function extent. Structural scores, unlinked support code, semantics,
playability and whole-executable identity earn no additional credit.
