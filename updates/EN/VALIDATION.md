# EN validation receipt

Base: `5ab60ff49af6da752fe8452031996410a50f00b4`. [VALIDATION.json](VALIDATION.json) records actual commands, exits, test counts, relevant outputs and inherited failures. These are preservation and repository checks; they establish no scientific correctness, novelty, experiment or prompting advantage.

| Check | Actual result |
| --- | --- |
| `python3 frontier/build_access.py build` then `check` | PASS: 814 cards, 259 gates, 1,122 proof ranges, zero source-access issues. |
| `python3 updates/EN/validate.py` | PASS: 42 originals, 1,646,260 bytes; three pastes, three ZIPs, 36 exact extracted members, 33 producer digests and 33 new claim proof ranges. Ten scripts syntax parsed, zero executed. |
| Unit suites | PASS: frontier 7, evaluation 25, technology 24; EC 4, ED 4, EE 5, EF 4, EG 6, EH 6, EI 5, EJ 10, EK 10, EL 13, EM 12, EN 17. |
| `python3 state/publish_checkpoint.py self-test` | PASS: 7. Together with the suites above, **159 tests pass**. |
| Technology and workflow validators with `--include-fixtures --immutable-base 5ab60ff49af6da752fe8452031996410a50f00b4` | PASS. Earlier records immutable; three observational traces added, 36 live latest traces total. All usage incomplete; no comparative advantage inferred. |
| `python3 evaluation/research_eval.py validate` | PASS; matched-evaluation records unchanged. |
| `python3 frontier/retrieve.py dossier <id>` for N742, N743, N744 and N735 | PASS, all four. |
| Standalone compatible intake validators DV, DX, DY and EC | PASS, all four. |
| Individual checkpoint validation using the unchanged record validator | PASS for 108 supported records, including the three new intake handoffs. |
| `python3 state/publish_checkpoint.py validate` | FAIL: `unsupported checkpoint schema`; three inherited files remain byte-identical. |
| Historical standalone validators ED–EK | FAIL on their inherited frozen-snapshot guards; original validators and receipts retained. |
| Historical standalone validator EL | FAIL: `earlier scientific navigation changed outside exact notices`; its older allowed set predates EM's N728 notice. |
| Historical standalone validator EM | FAIL: `earlier scientific navigation changed beyond exact scoped notices`; EN's N735 notice is outside EM's frozen allowed set. |

The unsupported historical checkpoint files are:

- `state/checkpoints/worker-conditional-copy-hierarchy/2026-10-11-conditional-copy-hierarchy.json`
- `state/checkpoints/worker-mixed-state-classicalization/2026-10-11-mixed-state-classicalization.json`
- `state/checkpoints/worker-weighted-union-uniformization/2026-10-11-weighted-union-uniformization.json`

No legacy schema fields or ancestry were guessed. New records are independently validated and only their new branch views/registry rows are added. Existing active objectives, checkpoints, source files, claims, status records, evaluation history and technology records remain intact.

The current EN guard checks older ledger prefixes, graph/catalog prefixes, aliases and scientific object immutability. Of 2,711 older scientific navigation outputs, **2,709 are byte-unchanged**. The only changes are N735's dossier and connection view, carrying the explicit generator-interface reuse notice. Removing exactly that notice, its new claim node/edge and changed snapshot fingerprint recovers the earlier views. This does not rewrite or relax older validation receipts.

The 17 new tests reject source/member omission, lost producer digest coverage, integrity promoted to reproduction, invented model/worker/usage telemetry, scientific status promotion, erased imported premises, topical dependencies, missing reciprocal notices, false capability completion, cover falsifiers without offsets/coverage/private witnesses, erased actuator/reference acquisition obligations, concealed vacuous mixed-probe certificates, compiler-cost transfer through a generator interface and older mathematics changed under a notice.

Raw staged `git diff --check` exits 2 on **506 retained source whitespace findings**. Excluding only `updates/EN/package/**` still exits 2 on six literal mirrored tab-indent findings. Authored checking passes when additionally excluding exactly `web/pages/src-EN-genesis-clock-lift.html` and `frontier/proof_ranges/68ad94ae7eca5cdef0a42d62.txt`, both literal source projections checked by the public builder. No original or literal source projection is whitespace-repaired.
