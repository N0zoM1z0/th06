# 東方紅魔郷 ～ the Embodiment of Scarlet Devil

<p align="center">
  <img src="resources/progress.svg" alt="TH06 strict authored reconstruction progress">
</p>

Source reconstruction of the original Japanese TH06 1.02h executable.
The maintained source reproduces **493 / 493 reviewed authored functions,
238,624 / 238,624 bytes (100%)** through complete comparisons with full
relocation inventories.

The unmodified [GensokyoClub reference](https://github.com/GensokyoClub/th06)
at `7411374` reaches **99.9979%** in the initial conservative named scope:
508 / 509 functions, 241,025 / 241,030 bytes. The remaining five bytes are a
compiler-generated exit callback mislabeled as a destructor. See
[progress](docs/PROGRESS.md) and the [boundary review](docs/BOUNDARY_AUDIT.md).

| Target property | Required value |
| --- | --- |
| Version | Original Japanese 1.02h |
| Size | 512,000 bytes |
| SHA-256 | `9f76483c46256804792399296619c1274363c31cd8f1775fafb55106fb852245` |
| MD5 | `fa3d64768b1bfc50703dedc2db92f7fa` |
| Image base | `0x00400000` |
| Entry point | `0x0045D746` |

Provide your own original executable at `resources/th06.exe`, then run
`python3 scripts/verify-target.py`. Executables, assets, toolchains, generated
code and analysis databases are private and excluded from this repository.

The project follows [th095](https://github.com/N0zoM1z0/th095)'s hash-attested
Ghidra, two-oracle acceptance, manifest replay and progress workflow. TH06
uses pinned **VC7.0 13.00.9466**. Every tool runs headless, with serialized
compiler work and bounded analysis resources.

## Reproduce

Python 3.11+, Git, Wine and a Linux headless environment are required. Bootstrap
pinned tools, or pass existing installations to avoid duplicate downloads:

```bash
python3 scripts/bootstrap-tools.py
scripts/import-target.sh /path/to/original/th06.exe
python3 scripts/build.py
python3 scripts/replay-exact-units.py
python3 scripts/validate-tracking.py --require-target
python3 scripts/ci.py
```

`bootstrap-tools.py --help` lists `--ghidra-home`, `--jdk-home` and `--dx8sdk`
reuse options. The original target is never downloaded. Ghidra setup is
optional for replay; use `python3 scripts/ghidra.py initialize` for analysis.

Reference-only measurement:

```bash
python3 scripts/build-reference.py
python3 scripts/link-reference.py
python3 scripts/reference-baseline.py
```

The reference uses its existing `var_order` frontend wrapper and inline x87
assembly. Their provenance is retained; stock compiler matching is a separate
question. The maintained build retains supporting unlinked routines as build
dependencies; they receive no exact credit. This result establishes authored
function bytes, not semantic completion, runtime playability or identity of the
whole executable (SDK/CRT/resource bytes are separate).

Current setup and evidence: [handoff](docs/RE_HANDOFF.md),
[oracle policy](docs/ORACLES.md), [workflow](docs/RE_WORKFLOW.md),
[Ghidra](docs/GHIDRA.md). Reference exactness and maintained authored progress
are separate; a build or structural match does not earn exact credit.

## Credits

[GensokyoClub/th06](https://github.com/GensokyoClub/th06) provides the source
reference, names, mapping and VC7.0 build profile. The reference is pinned in
`config/reference.toml`; reused helpers retain their
[CC0 license](docs/LICENSE-GensokyoClub.txt). Their work is measured against
this project's original target and strict oracle before acceptance.

Touhou and its original game code/assets are by ZUN / Team Shanghai Alice.
This repository distributes reconstruction work and tooling only.
