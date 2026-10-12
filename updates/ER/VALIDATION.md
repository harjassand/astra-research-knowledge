# ER validation receipt

Base: `b07610a28f61ce9020b485033d5628baf7a47dc5`. [VALIDATION.json](VALIDATION.json) records exact commands, exit codes, unit counts, historical errors and resolved failures.

| Check | Actual outcome |
| --- | --- |
| `python3 updates/ER/validate.py` | PASS:53 originals /418,570 bytes; paste, ZIP/11 members and directory/40 files;49 producer digests;15 scientific scripts syntax parsed, zero executed;30 proof ranges;5 checkpoints;10 exact scoped historical view changes |
| `python3 -m unittest discover -s updates/ER -p test_*.py` | **30 PASS**: preservation, missing manifest coverage, integrity/status distinction, known imports, exact historical projections, telemetry/prompt/bundle-run boundaries and narrowly pinned EP test adaptation |
| Existing regression suites | **222 PASS**: checkpoint7, frontier7, evaluation25, technology24; EC4, ED4, EE5, EF4, EG6, EH6, EI5, EJ10, EK10, EL13, EM12, EN17, EO20, EP23, EQ20. Total with ER: **252 PASS** |
| `python3 frontier/build_access.py check` | PASS:826 cards,278 gates,1,227 proof ranges, zero source-access issues; public deterministic builder only |
| Workflow/technology validation with `--include-fixtures --immutable-base b07610a28f61ce9020b485033d5628baf7a47dc5` | PASS: historical records immutable; no models, physical experiments or scientific truth checking |
| `python3 evaluation/research_eval.py validate` | PASS: matched protocol/history retained; zero model calls or effectiveness inference |
| Selective dossier retrieval | All five new cards and N749, P-round, N738, N747, N748 retrieve successfully |
| Record-level checkpoint audit | **120 supported records PASS**; three unsupported legacy records byte-identical to base; no schema/ancestry guessed |
| `python3 state/publish_checkpoint.py validate` | Exit1: `ERROR: unsupported checkpoint schema`; inherited global limitation retained |
| Historical standalone validators | DV PASS. DX/DY/EC and ED–EQ fail frozen historical object/navigation guards; exact errors retained. EP/EQ now encounter the five scoped later notices and test fixture. No blanket historical-validation success claimed |
| `git diff --cached --check` | PASS without exclusions |

Earlier cards, scoped status objects, source archives, checkpoints, evaluation and technology records are unchanged. Ledgers and graph/catalog prefixes are append-only. **2,829** earlier scientific navigation outputs remain byte-identical. Only five earlier dossiers/connections change: N749, P-round, N738, N747 and N748. ER removes the exact new notice blocks and their single incident edge/node, restores snapshot metadata and requires equality with the base content. Tests reject changed mathematics or graph interfaces.

One existing EP unit test originally assumed its old notice was the only notice on N747. It now removes only the exact later N747→N754 projection before testing EP's historical equality and mutation rejection. ER pins the exact code insertion and rejects any broader edit. The EP validator, EQ cached-output fix and all prior receipts remain untouched. EP23, EQ20 and ER30 tests pass. An initially incorrect frontier test-discovery directory was corrected to `frontier`; all seven tests pass. Initial failures and resolutions remain in the JSON receipt.

The initial source-bootstrap workflow-ID collision and an overly literal ER context assertion were fixed before final validation. Four bundle subaccounts now have unique locators and matching checkpoint hashes, while their records explicitly prohibit counting them as four independent inference runs. The final rounding source ZIP was already present locally and matches the inspected source response; a timed-out browser wait is not represented as successful fresh recovery.

These are repository and interface checks. Producer diagnostics, proof narratives, exact finite arithmetic, compilation, library searches and conservative resource prescriptions do not establish independent mathematical correctness, novelty, a full implemented compiler/rounder, physical validation, useful technological performance or research-workflow effectiveness. No archived scientific code was imported or run.
