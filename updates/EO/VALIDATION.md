# EO validation receipt

Base: `a33fc7e1db8f42873025fa29882f85f2d4503695`. Exact commands, exit codes, test counts and failure messages are in [VALIDATION.json](VALIDATION.json).

| Check | Actual result |
| --- | --- |
| `python3 updates/EO/validate.py` | PASS: 49 original files / 399,569 bytes; three pastes and ZIPs; 43 exact members; 40 producer digests; safe paths and CRC; ten scripts syntax parsed, zero executed. |
| `python3 -m unittest discover -s updates/EO -p 'test_*.py'` | 20 tests PASS. Negative checks reject erased provenance/imports/obligations, scientific promotion, invented telemetry, strengthened robust-rank exponent, an executed/necessary interpretation of the upper budget, removed finite-size gate and synthetic-to-physical promotion. |
| Existing regression suites | 159 tests PASS: checkpoint self-test 7; frontier 7; evaluation 25; technology 24; EC 4; ED 4; EE 5; EF 4; EG 6; EH 6; EI 5; EJ 10; EK 10; EL 13; EM 12; EN 17. Total with EO: **179**. |
| `python3 frontier/build_access.py check` | PASS: 817 cards, 265 gates, 1,151 proof ranges and zero source-access issues. Public deterministic builder used; unavailable private SQLite builders were not run. |
| `python3 technology/validate.py validate --include-fixtures --immutable-base a33fc7e1db8f42873025fa29882f85f2d4503695` | PASS; historical technology records immutable, no experiments executed. |
| `python3 evaluation/workflow_trace.py validate --include-fixtures --immutable-base a33fc7e1db8f42873025fa29882f85f2d4503695` | PASS; historical traces immutable. New records retain actual configuration, worker use and expenditure as UNKNOWN. |
| `python3 evaluation/research_eval.py validate` | PASS; matched-evaluation historical rows retained, no model calls or effectiveness claim. |
| Selective retrieval | N745, N746, N747 and reciprocal N742 dossiers retrieve successfully with exact bounded proof sources and current scoped status. |
| Checkpoint record audit | 111 supported records PASS, including all three new intake records. Three unsupported legacy records are byte-identical to base. |
| `python3 state/publish_checkpoint.py validate` | Exit 1: `ERROR: unsupported checkpoint schema`. Legacy failure retained; no schema/ancestry guessed and no global-validation success claimed. |
| Historical standalone intake validators | DV, DX, DY, EC and EN PASS. ED–EK retain eight earlier snapshot guards; EL/EM retain prior notice-set guard failures. Full exact messages are preserved in the JSON receipt. Their unit tests pass; standalone guards are not relabelled as passing. |
| `git diff --cached --check` | Exit 2: eleven preserved original-source whitespace instances. |
| `git diff --cached --check -- . ':(exclude)updates/EO/package/**'` | PASS. Only raw original source package excluded; authored/generated files pass. |

The validator pins all original sources and source ranges, checks card/status/catalog/web consistency and append-only historical ledgers, validates each new checkpoint and observational trace, and confirms 2,748 earlier scientific navigation outputs remain byte-identical. Only N742's generated dossier and connection change. Removing the exact new continuation notice, node/edge and snapshot fingerprint recovers their base content. Earlier mathematical cards, statuses, sources, branch checkpoints, evaluation records and technology objects remain unchanged.

N742's passive thermal-copy lower bound is not invalidated. N747 uses a different state, physical model, preparation access and scalar output. A navigation comparison is not a theorem premise. No copied scientific program was imported or run; parsing Python syntax, archive hashes and repository tests do not validate the underlying proofs, numerical claims, experiment, priority, practical advantage or research effectiveness.
