# Authored denominator review

The original target is pinned in `config/target.toml`. The unmodified reference
was measured before changing its ownership labels: 508 / 509 named functions,
241,025 / 241,030 exact bytes (99.9979256%).

The maintained denominator is 493 authored functions / 238,624 bytes. Sixteen
entries (2,406 bytes) were independently classified as compiler emission:

- Eleven default constructors: AsciiManager, StageMenu, Stage, Enemy,
  BulletTypeSprites, GuiImpl, GuiMsgVm, ItemManager, Player, PlayerBombInfo and
  MainMenu. Their owner declarations contain no written constructor body;
  VC7 emits their complete COMDAT sections when composing member lifetimes.
- Four scalar deleting destructor wrappers: CSound, CStreamingSound,
  IPbg3Reader and Pbg3Reader. Their compiler-decorated `??_G` symbols and
  deletion-flag ABI identify generated wrappers, distinct from written
  destructor bodies, which remain authored.
- `0x00469A30`, labeled GameErrorContext::~GameErrorContext upstream, is
  `Global.obj::_$E10` in the compiler/linker map, inside `.text$yd`. It is a
  five-byte generated exit callback, not a written destructor definition.

This classification does not depend on whether those functions match. All
fifteen mapped constructor/deleting wrappers also passed strict comparison.
The conservative original score is preserved in `config/reference-baseline.csv`
and `config/boundary-review.json` so the ownership adjustment is visible.

The game/PBG code region is `[0x00401000, 0x0043D158)`. Every Ghidra function
entry there has an upstream mapping. Complete source-object extents account
for embedded switch tables. The remaining gaps contain only NOP/INT3
alignment, except one eight-byte compiler-generated this-adjustor at
`0x0043C6D0`. Its linker symbol is
`?ReadByte@Pbg3Reader@th06@@WBI@AEHXZ`; its entire generated linked body matches
the target. Embedded D3DXMatrixIdentity and D3DXVec3Length are SDK inlines and
are classified separately. Neither alignment nor table bytes inflate the
function-code denominator.

Code after the game/PBG region belongs to linked SDK/CRT, compiler EH helpers
and compiler startup/exit sections. Those bytes remain separate from authored
coverage. The 1,395-entry initial Ghidra inventory is retained verbatim in
`config/ghidra-functions.csv`; it establishes analysis candidates, not origin
or final function size. The maintained ledger includes 1,509 reference entries
plus the independently identified adjustor.

`import-exact-reference.py` verifies the region gaps, Ghidra-entry coverage,
source provenance and strict comparisons before generating the canonical
493-unit ledger. It retains all compiler/library classifications. Canonical
replay independently rechecks the admitted functions against the target.

The result is function-level byte identity. It does not accept all supporting
unlinked routines, a whole-program semantic reconstruction, SDK/CRT identity,
resource reconstruction or runtime behavior. The maintained reconstruction
retains upstream's documented var_order extension and x87 source assembly;
removing them would require a separate compiler-oracle project.
