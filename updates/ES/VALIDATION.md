# ES validation receipt

Base: `76f1e365648e225f89bff437693e7bd148cc88d9`. [VALIDATION.json](VALIDATION.json) records the exact commands, exit codes, test counts and errors.

| Check | Actual outcome |
| --- | --- |
| `python3 updates/ES/validate.py` | PASS:46 originals,345,518 bytes,17 proof ranges,3 unique checkpoints/traces for one campaign,9 scripts syntax parsed only |
| ES unit suite | **32 PASS**: source coverage, status/import boundaries, unresolved gates, family fit, unknown telemetry and campaign-subaccount accounting |
| Existing regression suites | **252 PASS**: checkpoint7, frontier7, evaluation25, technology24; EC4, ED4, EE5, EF4, EG6, EH6, EI5, EJ10, EK10, EL13, EM12, EN17, EO20, EP23, EQ20, ER30. **284 total PASS** with ES |
| `python3 frontier/build_access.py check` | PASS:829 cards,281 gates,1,244 proof ranges, zero source-access issues |
| Workflow and technology validation with fixtures and immutable base | PASS; prior records immutable; zero model calls/experiments or scientific truth checking |
| `python3 evaluation/research_eval.py validate` | PASS; matched protocol/history retained; no effectiveness comparison inferred |
| Selective dossier retrieval | N757,N758,N759 and comparison cards N58,N393,N594,N88 all retrieve successfully |
| Checkpoint record audit | **123 supported records PASS**; three inherited unsupported records byte-identical to base |
| `python3 state/publish_checkpoint.py validate` | Exit1: `ERROR: unsupported checkpoint schema`; inherited limitation |
| Historical standalone validators | DV and ER PASS. DX/DY/EC and ED–EQ fail inherited frozen historical guards; exact errors retained |
| `git diff --cached --check` | Exit2: extra blank EOF line in the byte-exact original `updates/ES/package/adaptive_invention/sources/astra_N733_overlap_proof.txt` |
| Authored diff check excluding only that exact original | PASS |

All 46 archived files were compared byte-for-byte with the supplied local campaign directory, in addition to pinned hash/extent checks. Ten omitted local files have exclusion receipts: eight downloaded third-party fulltexts and two regenerable bytecode caches. No producer-wide manifest or ZIP existed for this directory; no such receipt is invented. Producer output JSON is preserved as source evidence, not independently reproduced diagnostics.

All **2,879 earlier scientific navigation outputs** are byte-identical. Earlier cards, status objects, originals, checkpoints, evaluation/technology records, validators, tests and receipts are unchanged. Ledgers and graph/catalog prefixes remain append-only; no scoped historical notice or theorem dependency was added.

The first ES validator run encountered an older metadata row without `source_id`. The new selector now ignores such nonmatching historical rows without rewriting them. The final full validator and all32 ES tests pass. Its initial failure and repair are recorded in JSON. No earlier test or validator needed modification.

The global checkpoint/schema limitation and historical frozen-guard failures are recorded rather than hidden or repaired by guessing research ancestry. Each supported record passes the unchanged record validator. Three new views/registry rows are generated only for the new intake routes.

These are repository checks. No campaign scientific script was executed or imported, and no independent analytic reconstruction, formal verification, literature/priority audit, physical validation or discovery-effectiveness experiment was performed at intake. Internal producer review remains internal. The particle kinetic limit, general LP acquisition/progress and interacting quantum cancellation targets stay open.
