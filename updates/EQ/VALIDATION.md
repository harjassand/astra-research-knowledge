# EQ validation receipt

Base: `32392b30ecb2fbe3e94ce4fc04ebc3acb4dd5b2f`. Exact commands, exit codes, counts and failure messages are in [VALIDATION.json](VALIDATION.json).

| Check | Actual result |
| --- | --- |
| `python3 updates/EQ/validate.py` | PASS: 18 original files / 634,096 bytes; one paste and ZIP; 16 exact members; 15 producer SHA256SUMS digests; safe paths, unique names and CRC. Six scientific scripts syntax parsed, zero executed. |
| `python3 -m unittest discover -s updates/EQ -p 'test_*.py'` | 20 tests PASS. Includes source/witness preservation, erased import/obligation rejection, scientific-promotion rejection, unknown telemetry, distinct family contracts and cached-output compatibility guards. |
| Existing regression suites | 202 tests PASS: checkpoint self-test 7; frontier 7; evaluation 25; technology 24; EC 4; ED 4; EE 5; EF 4; EG 6; EH 6; EI 5; EJ 10; EK 10; EL 13; EM 12; EN 17; EO 20; EP 23. Total with EQ: **222**. |
| `python3 frontier/build_access.py check` | PASS: 821 cards, 273 gates, 1,197 proof ranges and zero source-access issues. Public deterministic builder used; private SQLite builders were not run. |
| `python3 technology/validate.py validate --include-fixtures --immutable-base 32392b30ecb2fbe3e94ce4fc04ebc3acb4dd5b2f` | PASS; historical technology records immutable, no scientific or physical experiment executed. |
| `python3 evaluation/workflow_trace.py validate --include-fixtures --immutable-base 32392b30ecb2fbe3e94ce4fc04ebc3acb4dd5b2f` | PASS; historical traces immutable. Displayed inference duration and producer program timings remain distinct; actual research expenditure UNKNOWN. |
| `python3 evaluation/research_eval.py validate` | PASS; matched-evaluation historical rows retained, no model calls or effectiveness claim. |
| Selective retrieval | N751 and comparison N747, N748, N721 dossiers retrieve successfully. Comparisons are navigation, not imported hypotheses. |
| Checkpoint record audit | 115 supported records PASS, including the new intake record. Three unsupported legacy records are byte-identical to base. |
| `python3 state/publish_checkpoint.py validate` | Exit 1: `ERROR: unsupported checkpoint schema`. Historical failure retained; no guessed schema/ancestry or global-validation success. |
| Historical standalone validators | DV and EP PASS. DX/DY/EC, ED–EK and EL/EM/EN/EO retain earlier frozen historical-route/snapshot guards. Exact messages are recorded; their unit suites pass. |
| EP cached-output compatibility | One EP test and its standalone validator initially failed on unchanged cached snapshot metadata. The exact guard fix checks the published connection hash instead of requiring the newest global snapshot. Both reruns PASS. Original failure messages and resolution are retained in the JSON receipt. |
| `git diff --cached --check` | Exit 2: one trailing-space instance in the byte-exact original paste. |
| `git diff --cached --check -- . ':(exclude)updates/EQ/package/**'` | PASS; only the original-source package excluded. |

All 2,825 earlier scientific navigation outputs remain byte-identical. Earlier mathematical cards, statuses, proof/source archives, branch checkpoints, evaluation/technology records and validation receipts are unchanged. The only earlier validator-code change is the exact EP cached-output guard described in [VALIDATOR_COMPATIBILITY.md](VALIDATOR_COMPATIBILITY.md). EQ rejects any further change to that file; regression tests accept a legitimate cached output and reject a stale hash. Historical notice removal and proof-content equality checks remain effective.

N751 preserves source-reported complete local admissibility, exact witness files, symbolic deductions and the scoped box-closure obstruction. The supplied verifier is separate from the optimizer but belongs to the same producer. No archived scientific program was imported or executed and literature/priority was not audited. These tests establish repository integrity and interface preservation, not theorem correctness, numerical reproduction, physical validation, computational advantage or scientific discovery effectiveness.
