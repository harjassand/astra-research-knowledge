# Read ledger

All repository reads below were from the read-only `work/astra-capital` checkout. I wrote only inside `work/FJ-ultra-power`. No other FJ worker directory or any of the three incoming FJ source packets was read.

## Pinned lineage and current notices

| Source | Read scope | Purpose / status |
|---|---:|---|
| `work/FJ_PIN.json` | full | Main/checkout pins and retained Ultra revision; establishes task routing only. |
| `work/astra-capital/00_START_HERE.txt`, `AGENTS.md` | full | Retrieval and read-only research contract. |
| `state/branches/ultra.txt` at retained revision `00d1c9769bc26829fef2653dbcc10ed1dc8a927c` | full | Exact old current checkpoint: `2026-10-10-ct-ultra`. |
| `state/checkpoints/ultra/2026-10-10-ct-ultra.json` at retained revision | full | Exact old checkpoint contract; the seven CT results were source-derived/unreviewed and did not select a transformative route. |
| `state/branches/ultra.txt` at checked-out `cb62d881a071c617b11d7dbc82a98921969389a7` | full | Current Ultra checkpoint: `2026-10-11-sampler-encoder-gates`. |
| `state/checkpoints/ultra/2026-10-11-sampler-encoder-gates.json` | full | Exact assumptions, query/cost contract, failures, source pins, and open sampler/encoder gates. SHA-256 `d2247dc78c004eac31d033ff4be55d07503af32ed1e64534d063a26311091f12`. |
| `state/checkpoints/ultra/*.json` | summary fields for all 11 records | Compared all Ultra intake objectives/results/obstacles; no later sampler/encoder checkpoint supersedes the 11 October record. |
| `frontier/dossiers/N687.txt` | full | Current sampler scope and exact proof pointers. SHA-256 `df97376c5f666c651606788d6c07284164b3705a3c3ea12c72b1dcd2728e213c`. |
| `frontier/dossiers/N688.txt` | full | Current quantum encoder scope; not pursued as the primary target. SHA-256 `e1656376474db4f005217fafbb6354891d9495a6494bad97b05bd8e55e60399f`. |
| `agent/COMPOSITION.txt`, `state/CONTINUITY.md` | full | Applied transfer/status distinctions and read-only handoff constraints; no cross-result bridge was asserted. |
| `agent/CURRENT.txt`, `agent/RECENT.tsv` | targeted search | Checked current-route freshness and recent intake navigation. |

The ancestry check `git merge-base --is-ancestor 00d1c9769bc26829fef2653dbcc10ed1dc8a927c HEAD` succeeded. No file in `work/astra-capital` was modified.

## Sampler proof material

| Source | Read scope | SHA-256 | Use |
|---|---:|---|---|
| `updates/DP/package/foundational_campaign/FINAL_ROUND/r16_integrable_mean_mechanism.txt` | full (492 lines) | `28c024bc4a9f2c410b853c4db479fd8bf95709a3324b2fe6e9b18e337aa70615` | Exact fixed-a quantifiers and model at lines 25–41; noise-absorption and average-query cost at lines 392–416; candidate remains unaudited. |
| `updates/DP/package/foundational_campaign/FINAL_ROUND/r21_polylog_mean_compiler.txt` | lines 1–120, 540–568, 620–669 | `8c738542aa28fbf5fa603baf93ab47a1c3893111a48aa1a9f28e902d5b392bb5` | Stronger polylog target is open; exact Gaussian Stein identities and residual/acquisition gap. |
| `updates/DP/package/foundational_campaign/FINAL_ROUND/r22_polylog_mean_factory.txt` | lines 1–125, 300–430, 500–557 | `11a39e2ddeeaacc7daecdcfb837a1425dc7b2840a17a92ef7f15c6f2f83b2ba1` | Whole-vector query target, two-query action, and full-law acquisition gap. |
| `updates/DP/package/foundational_campaign/FINAL_ROUND/r28_multiscale_gaussian_mean.txt` | lines 1–20, 130–220 | `696bae5a65adb63e840200927abfcaca89b4b0c9960e66e254471af6831f4806` | Reconstructed scope of the frozen-source central-secant counterexample; it rejects that flow only. |
| `updates/DP/package/foundational_campaign/FINAL_ROUND/ROUND_FINDINGS.txt` | lines 43–126, 159–196, 269–312 | `3a99d8c382cc83241c5c051836d48d67d1395edf069f0e9c35ed148a627f9cc4` | Fixed-exponent candidate, Stein action, Newton inverse, and scoped sampler counterexamples/open gates. |

No external paper or web source was used for this scoped derivation. No preserved code or diagnostic was run.
