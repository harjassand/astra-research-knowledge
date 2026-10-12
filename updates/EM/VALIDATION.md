# EM validation receipt

Base: `0ec7c861e1d687a84a6509c6520f0ad44135f724`. Exact command exits, test counts and relevant outputs are in [VALIDATION.json](VALIDATION.json). These are architecture and preservation checks; they establish no scientific discovery, proof correctness, priority, experimental result or prompting advantage.

| Command or check | Actual result |
| --- | --- |
| `python3 frontier/build_access.py build` then `check` | PASS: 811 cards, 253 gates, 1,089 proof ranges; zero source-access issues. |
| `python3 updates/EM/validate.py` | PASS: 38 originals, 342,304 bytes; three pastes, three ZIPs, 32 exact members, 29 producer hashes, 49 new claim proof ranges. Eight scripts syntax parsed, zero executed. |
| `python3 -m unittest discover -s <suite> -p 'test_*.py'` | PASS: frontier 7, evaluation 25, technology 24, EC 4, ED 4, EE 5, EF 4, EG 6, EH 6, EI 5, EJ 10, EK 10, EL 13, EM 12. |
| `python3 state/publish_checkpoint.py self-test` | PASS: 7 tests. Together with the suites above, **142 tests pass**. |
| `python3 technology/validate.py validate --include-fixtures --immutable-base 0ec7c861e1d687a84a6509c6520f0ad44135f724` | PASS; all prior technology records unchanged. |
| `python3 evaluation/workflow_trace.py validate --include-fixtures --immutable-base 0ec7c861e1d687a84a6509c6520f0ad44135f724` | PASS; three observational traces added, 33 live latest traces total; all usage incomplete, no comparative advantage inferred. |
| `python3 evaluation/research_eval.py validate` | PASS; frozen matched-evaluation records unchanged. |
| `python3 frontier/retrieve.py dossier <id>` for N739, N740, N741 and N728 | PASS, all four. |
| Standalone compatible intake validators DV, DX, DY and EC | PASS, all four; historical source and checkpoint guards remain effective. |
| Individual checkpoint record validation | PASS for 105 supported records, including the three new independent intake handoffs. |
| `python3 state/publish_checkpoint.py validate` | FAIL: `unsupported checkpoint schema`. Three legacy files remain byte-identical to the base; see below. |
| Standalone historical validators ED–EK | FAIL with their original frozen-snapshot guards; these eight failures were already recorded at the EL publication. Their original files and receipts are unchanged. |
| `python3 updates/EL/validate.py` | FAIL: `earlier scientific navigation changed outside exact notices`. EM adds a new N728 notice outside EL's older permitted set. |

The global checkpoint failures are:

- `state/checkpoints/worker-conditional-copy-hierarchy/2026-10-11-conditional-copy-hierarchy.json`
- `state/checkpoints/worker-mixed-state-classicalization/2026-10-11-mixed-state-classicalization.json`
- `state/checkpoints/worker-weighted-union-uniformization/2026-10-11-weighted-union-uniformization.json`

No missing legacy schema fields or research ancestry were guessed. New checkpoints are validated individually and their new views/registry rows added without changing existing branches or active research objectives.

The current EM validator verifies append-only older ledgers, graph/catalog prefixes, aliases, and immutable earlier source, card, status, checkpoint, evaluation and technology objects. Of 2,656 older scientific navigation outputs, 2,654 are byte-unchanged. The only two changes are N728's dossier and connection view. Removing the exact new reciprocal notice, its new claim node/edge and the changed snapshot fingerprint recovers those prior views exactly. This does not relax or overwrite historical validation receipts.

The new tests reject source/member omission, lost producer hash coverage, integrity promoted to reproduction, invented model/worker/usage telemetry, scientific status promotion, erased imported premises, topical dependencies, a missing reciprocal notice, false Q4 completion and older mathematical content changes disguised as a notice. Raw staged `git diff --check` exits 2 on one original Markdown hard-break line in the Genesis note. Its two trailing spaces are preserved intentionally. Authored/generated publication checking excludes only `updates/EM/package/**` and passes; no original source is whitespace-repaired.
