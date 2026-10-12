# EU validation receipt

Base: `da0a23e56c83271667b701a400595270bcbac785`. [VALIDATION.json](VALIDATION.json) retains exact commands, outcomes, test counts and failures.

| Check | Actual result |
| --- | --- |
| `python3 updates/EU/validate.py` | PASS:7 original objects,85,754 bytes,5 ZIP members,4 producer hashes,12 proof ranges,1 checkpoint,2,917 unchanged earlier scientific views |
| EU unit suite | **24 PASS**: preservation, member/hash coverage, evidence/status/import/family/gate limits, unknown telemetry, exact prompt/duration ranges and invalid promotion rejection |
| Existing regression suites | **309 PASS**: checkpoint7,frontier7,evaluation25,technology24; EC4,ED4,EE5,EF4,EG6,EH6,EI5,EJ10,EK10,EL13,EM12,EN17,EO20,EP23,EQ20,ER30,ES32,ET25. **333 total PASS** |
| `python3 frontier/build_access.py check` | PASS:831 cards,284 gates,1,269 proof ranges,zero source-access issues |
| Workflow and technology validation with fixtures and immutable base | PASS; existing records preserved; no scientific experiments or truth checking |
| `python3 evaluation/research_eval.py validate` | PASS; historical matched protocol retained, no prompting comparison inferred |
| Selective retrieval | N761,N26,N632 dossiers PASS |
| Individual unchanged checkpoint validator | **125 supported records PASS**; three unsupported inherited records byte-identical to base |
| `python3 state/publish_checkpoint.py validate` | Exit1: `ERROR: unsupported checkpoint schema` |
| Historical standalone validators | DV,ET PASS. DX/DY/EC and ED–ES retain earlier frozen-history guard failures; exact stderr retained |
| Raw staged whitespace check | Exit2: original paste line211 trailing whitespace |
| Authored whitespace check | PASS, excluding only that exact preserved original |

The original paste and ZIP equal their supplied/recovered local bytes. Every extracted member equals its ZIP bytes; safe unique member paths, CRC and all four producer hashes pass. The verifier is AST syntax parsed only, never executed or imported. Producer90-code/32,906-family checks, exact examples and floating quantum diagnostics remain internal source evidence. No independent mathematical reconstruction, literature audit, certified floating PSD or physical experiment occurred.

All **2,917 earlier scientific navigation outputs** are byte-identical to the pinned base. Earlier cards, statuses, source packages, checkpoints, branch views, evaluation/technology records, validators, tests and receipts are unchanged. Append-only ledgers and graph/catalog prefixes pass. Family comparisons are navigation only; no prior scientific status or gate is changed. Imported analytic premises are explicitly recorded as source-reported external dependencies.

The three inherited checkpoint schemas remain unsupported rather than being guessed. Older standalone validators freeze historical navigation/objects from before documented later updates; those failures remain explicit. This intake changes none of those older scientific objects or views and does not weaken their validators. Both previous ET validation and its25 tests pass.

The initial new boundary guard used three phrases that differed from the authored card wording; it was corrected to the actual scope, with sources/card unchanged. The final24 intake tests pass. Browser event waiting timed out after20s, but the complete matching ZIP appeared locally and passed full integrity checks; no successful event-wait receipt is claimed. The original trailing space is preserved deliberately.

These are repository checks. They do not establish arbitrary-dimensional theorem correctness, novelty, general sampling hardness, entangled marginal compatibility, useful implementation advantage, technology readiness or research-workflow effectiveness. The linear-versus-square-root approximate-degree obligation and acquisition/priority review remain open.
