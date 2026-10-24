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

The reference baseline is kept separate from maintained authored progress.
Function names, extents and ownership imported from upstream remain
provisional until reconciled with target control flow and Ghidra inventory.
The provisional named authored scope includes PBG3, WinMain and the named
GameErrorContext destructor. SDK inline helpers and compiler startup are
separate. Unknown inventory entries and uncovered code remain review debt.
A 98% named-scope result alone cannot close the project's 98% goal.

`compare-coff-function.py --unit NAME` follows th095's canonical manifest
replay. Raw positional mode reports structural diagnostics only.
