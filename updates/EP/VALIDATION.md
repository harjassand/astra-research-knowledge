# EP validation receipt

Base: `ac6ce52c80d55173ca38f9cb99cd3ba7f50fb132`. Exact commands, exit codes, test counts and failure messages are in [VALIDATION.json](VALIDATION.json).

| Check | Actual result |
| --- | --- |
| `python3 updates/EP/validate.py` | PASS: 40 original files / 1,506,550 bytes; three pastes and ZIPs; 34 exact members; 31 producer digests; safe paths and CRC; eight scripts syntax parsed, zero executed. Three NPZ inputs are byte-preserved and not loaded. |
| `python3 -m unittest discover -s updates/EP -p 'test_*.py'` | 23 tests PASS. Negative checks reject changed source/binary hashes, omitted members, erased provenance/obligations, scientific promotion, invented telemetry, altered old mathematics, scalar-to-G1 promotion, necessary interpretation of an unexecuted upper budget, lost rounding-family history, existence-to-algorithm promotion and local-to-global resonance overclaim. |
| Existing regression suites | 179 tests PASS: checkpoint self-test 7; frontier 7; evaluation 25; technology 24; EC 4; ED 4; EE 5; EF 4; EG 6; EH 6; EI 5; EJ 10; EK 10; EL 13; EM 12; EN 17; EO 20. Total with EP: **202**. |
| `python3 frontier/build_access.py check` | PASS: 820 cards, 271 gates, 1,185 proof ranges and zero source-access issues. Public deterministic builder used; unavailable private SQLite builders were not run. |
| `python3 technology/validate.py validate --include-fixtures --immutable-base ac6ce52c80d55173ca38f9cb99cd3ba7f50fb132` | PASS; historical technology records immutable, no experiments executed. |
| `python3 evaluation/workflow_trace.py validate --include-fixtures --immutable-base ac6ce52c80d55173ca38f9cb99cd3ba7f50fb132` | PASS; historical traces immutable. Actual source model configuration, worker use and expenditure remain UNKNOWN. |
| `python3 evaluation/research_eval.py validate` | PASS; matched-evaluation historical rows retained, no model calls or effectiveness claim. |
| Selective retrieval | N748, N749, N750 and reciprocal N747, N689, N692, N746 dossiers retrieve successfully with bounded proof sources and current scoped status. |
| Checkpoint record audit | 114 supported records PASS, including all three new intake records. Three unsupported legacy records are byte-identical to base. |
| `python3 state/publish_checkpoint.py validate` | Exit 1: `ERROR: unsupported checkpoint schema`. Legacy failure retained; no schema/ancestry guessed and no global-validation success claimed. |
| Historical standalone intake validators | DV PASS. DX/DY/EC and EN/EO now stop on frozen earlier-route/notice guards. ED–EK retain eight earlier snapshot failures; EL/EM retain earlier notice-set failures. Full exact messages are preserved in the JSON receipt. Unit tests pass; standalone guards are not relabelled as passing. |
| `git diff --cached --check` | Exit 2: 934 preserved original-source whitespace instances. |
| `git diff --cached --check -- . ':(exclude)updates/EP/package/**'` | Exit 2: two literal source-projection instances remain. |
| Authored staged whitespace check | PASS after excluding only the source package and the two exact projections listed below. |

Authored check: `git diff --cached --check -- . ':(exclude)updates/EP/package/**' ':(exclude)frontier/proof_ranges/9da81e282a150247167d5c95.txt' ':(exclude)web/pages/src-EP-frontier-restart-reconstruction.html'`. The excluded proof range and HTML retain original text; source mirrors and ranges are checked by the intake validator and deterministic access builder. Original whitespace and control characters are preserved.

The validator pins all original sources and source ranges, checks card/status/catalog/web consistency and append-only historical ledgers, validates each new checkpoint and observational trace, and confirms 2,777 earlier scientific navigation outputs remain byte-identical. Only the generated dossiers and connections for N747, N689, N692 and N746 change. Removing each exact new continuation notice and claim node/edge, then restoring the earlier generated snapshot metadata, recovers the old content. The current snapshot is checked against the public access manifest. Earlier mathematical cards, statuses, source archives, branch checkpoints, evaluation records and technology objects remain unchanged. Historical validators and receipts have not been relaxed or edited.

N748 returns a proposed finite-ring randomized scalar approximation; it does not construct literal N747 G1 rational witnesses or a quantitative thermodynamic limit. N749 refines an existing qualitative rounding family; existential support does not supply polynomial-time acquisition. N750 removes a local variance singularity; global phase control and affordable acquired blocks remain open. No copied scientific program was imported or run. Archive hashes, Python syntax parsing and repository tests do not establish mathematical correctness, numerical reproduction, physical validation, priority, practical advantage or research effectiveness.
