# Headless Ghidra

The wrapper is adapted from th095 and uses pinned Ghidra 12.1.3/JDK 21.
It clears display variables, lowers priority and pins headless analysis to one
CPU. The Java heap defaults to 2 GiB. Local installations may be reused via
ignored `.tools/ghidra` and `.tools/jdk` symlinks.

```
python3 scripts/ghidra.py initialize
python3 scripts/ghidra.py check
python3 scripts/ghidra.py inventory
python3 scripts/ghidra.py decompile .analysis/function.c 0x00401000
python3 scripts/ghidra.py query .analysis/function.txt function 0x00401000
```

Initialization verifies SHA-256, MD5, module name, file-side PE32 machine,
base, entry point, image size, headers and text mapping, plus six mapped text
samples. Every query repeats these checks and requires a hash-bearing success
marker, because analyzeHeadless can return zero after a script exception.
Private databases stay below `ghidra-project/`; decompiler hypotheses stay
below `.analysis/`. Never patch program bytes or launch the GUI.

The initial inventory contains 1,395 Ghidra candidates. This is neither an
accepted function count nor an authored denominator. Reference mapping has
1,509 entries; control flow, data/table extents and ownership require review.
