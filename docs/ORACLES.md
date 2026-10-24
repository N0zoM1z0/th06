# Exact acceptance

Oracle A is the original Japanese TH06 1.02h file, pinned by SHA-256, MD5,
size and PE mapping in `config/target.toml`. Ghidra is a view of that file.
Every headless query repeats the identity and mapped-code attestation.

Oracle B is VC7.0 13.00.9466, pinned in `config/tools.lock.toml`. Preserve
per-owner optimization/PCH flags and record source, tool and object digests.
The upstream baseline uses its documented `var_order` frontend wrapper,
compiled locally from the pinned CC0 source; the stock frontend is preserved.
The wrapper and upstream inline assembly are baseline dependencies, not new
permission to introduce matching tricks into maintained source.

Strict exact requires equal complete extents and all bytes after replaying
all DIR32/REL32 relocations. Destinations must come from independent named
function/global mappings, PE imports, section anchors, or a unique complete
read-only constant section. Never use target instruction operands to solve
relocations. Missing, conflicting or unsupported relocations fail closed.
A relocation-masked structural match earns no strict exact credit.

A second strict route compares the final linked image at the original symbol
address. It requires the entire COFF extent, the complete relocation inventory,
a unique matching linker-map anchor and equality of every linked byte. The
image is produced entirely from source and libraries; it contains no injected
original code. The comparator checks maintained source hashes, compiler and
frontend identity, object hashes, all linked inputs, linker identity, image
hash and map hash. Thus relocation bytes are independently generated, not
masked or solved from the original instruction.

When two original symbols share a name, the independently generated linked
image may select one existing named target address. This is used for the two
DebugPrint copies. The generated destination must already be in the independent
name mapping; the original operand never selects it. Accepted fixed relocation
values and their evidence are preserved in `config/relocation-evidence.csv`.

The reference baseline is kept separate from maintained authored progress.
Function names, extents and ownership imported from upstream remain
provisional until reconciled with target control flow and Ghidra inventory.
The initial conservative named scope includes PBG3, WinMain and the upstream
GameErrorContext destructor label; the latter is now reviewed as compiler
exit callback `Global.obj::_$E10`. SDK inline helpers and compiler startup are
separate. Unknown inventory entries and uncovered code remain review debt.
A 98% named-scope result alone cannot close the project's 98% goal.

`compare-coff-function.py --unit NAME` follows th095's canonical manifest
replay. Raw positional mode reports structural diagnostics only.
