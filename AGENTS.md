# TH06 reconstruction rules

## Highest priority: lightweight exact reconstruction and useful knowledge

These are the user's current workflow requirements. They override older
instructions that mandate broad CI, repeated preflights, document/source-pin
refreshes, per-checkpoint audits or extra workflow machinery. Preserve the
actual exactness, target identity, natural-source and state-isolation rules.

- Prioritize exact reconstruction and reusable knowledge. Use the shortest
  useful loop: inspect relevant state, analyze/edit, compile and compare the
  affected scope, retain useful learning, and create a coherent checkpoint.
- Use existing repository scripts and composable Bash. Add only the smallest
  change needed for an observed problem. Do not introduce a framework, schema,
  registry, state machine, generalized validator, test family or reporting
  process merely to make a local reconstruction task look more engineered.
- Documentation, knowledge and handoff edits require no compiler, analyzer,
  full CI, cold replay or receipt refresh. Inspect the diff. Check syntax only
  for machine-readable inputs actually changed.
- Source changes need the complete affected exact comparison, including its
  owned extents and relocations. Recheck known consumers of changed shared
  inputs. Tool changes need relevant positive/negative cases and a bounded
  real smoke. Run a broad suite only for an explicit request or a demonstrated
  impact that cannot be narrowed; state that reason first.
- Do not add tests or live freshness gates for prose hashes, prompt wording,
  progress totals, handoff source-SHA tables or ordinary source spelling.
  Bind exact evidence to executable inputs and relevant verification settings.
  Keep Git metadata as provenance. A document genuinely consumed by a build
  remains a build input. Never edit historical receipts to manufacture a pass.
- Plain Markdown is sufficient for knowledge: record the finding, applicable
  target/compiler/scope, evidence links, useful failed attempts and open
  questions. No mandatory JSON conversion, promotion workflow or test per note.
  Search relevant sections; do not read an entire large knowledge journal.
- Write documentation and knowledge in natural, fluent English. Lead with the
  concrete finding and connect the evidence and next action clearly. Remove
  filler, circular restatements, repeated conclusions and unnecessary jargon.
  Do not add defensive-claim boilerplate. State a real uncertainty or scope
  limit once when it changes a decision; do not repeat disclaimers about what
  a note does not prove, certify or authorize. Prefer a small useful note over
  an exhaustive report that is difficult to read.
- Keep handoff focused on current work, evidence references, blockers and the
  next useful action. Generate progress from canonical ledgers; avoid manual
  duplicate counts, recurring full reports and unrelated documentation chores.
- Preserve dirty/untracked work, targets, useful evidence, game-specific Wine
  prefixes and analyzer projects. Exactness still requires a complete strict
  comparison; knowledge and successful commands alone confer no exact credit.


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
  visible; never change ownership or shrink a denominator to inflate coverage.
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

## Shared Factory runtime

Follow [the shared tools instructions](docs/SHARED_TOOLS.md). Ghidra/JDK and
Wine executables are shared through Factory; repository scripts also work
without MCP. Use `scripts/shared_runtime.py` and the existing compiler/analysis
frontends. Keep this game's prefix, analyzer project, Java home/cache, target
and compiler profile isolated. Do not install duplicate tools or inherit
another game's `WINEPREFIX`. This shared-runtime procedure supersedes older
per-repository installation instructions; pinned versions/hashes still apply.
