# Read ledger

Observation date: 2026-10-14. This worker wrote only `work/FJ-nonlinear-benchmark/`; the capital repository and incoming archives remained read-only. No sibling FJ worker results were read.

## Governing pin and contract

| Path | Read depth | SHA-256 | Use |
|---|---:|---|---|
| `work/FJ_WORKER_CONTRACT.txt` | Full, 8 lines | `4516f9b3dd25310868cd2e449765e244c1a72cef8137339edcb8c63c266eb19c` | Scope, isolation, read-only, reproduction, and frozen-artifact requirements. |
| `work/FJ_PIN.json` | Full, 12 lines | `b152a3f7ca70e8c582b69a47f46876ed44745c8a152f53800fe2de449eb7440c` | Incoming pin: main `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871`; checkout/cumulative PR83 `cb62d881a071c617b11d7dbc82a98921969389a7`; ultra ref `00d1c9769bc26829fef2653dbcc10ed1dc8a927c`; observation `2026-10-14T08:47:41.682451+00:00`. |

## Incoming nonlinear source archive

These files were read in full. No source file was executed or modified; the benchmark was independently implemented in the owned folder. The source's exact certificates are not transplanted: the new 8D model has its own rational derivation in `analyze.py`.

| Path | Size / lines | SHA-256 | Read and use |
|---|---:|---|---|
| `work/FJ-sources/nonlinear/README.md` | 1,388 B / 15 | `ddfbc790791bc96ba877c670808a054579d53bdfde443df84b463f3bcd91db4d` | Full package scope and reproducibility notes. |
| `work/FJ-sources/nonlinear/research_note.md` | 17,810 B / 272 | `a843a6cdfc1f0b55b25dbe1dd1b24ba2b157f7f4c67e51e5fcbc28f080c721f0` | Full assumptions, theorem, cost contract, original 1D experiment, obstruction, and prior-art scope. The sampled correction theorem is used only under its explicit global residual/tangent/Taylor bounds. |
| `work/FJ-sources/nonlinear/nonlinear_query.py` | 9,133 B / 214 | `829f370818ca2cf0de04b9930f09de5bd2cd1d3f35987a7a24dd55c894e861e4` | Full code read to understand branch categories, endpoint generation, coefficient/evaluator assumptions, exact-vs-floating caveat, and 1D baseline. Not executed. |
| `work/FJ-sources/nonlinear/verify_certificates.py` | 2,377 B / 55 | `dfdbcad1f43ac71283e269c2e8f21ecc69a0346554ccc94edf6fadc5d17c706e` | Full exact-rational verifier read. Not run because it writes beside the source; the new analyzer derives and asserts the new model's exact rational checks in the owned folder. |
| `work/FJ-sources/nonlinear/exact_certificate_checks.json` | 4,706 B / 176 | `b30d837a480ecd64c5c1b0aefa43770ed0c7020f98ac915b1c2b1c0ff20745d3` | Full result read; recorded as producer output, not independent evidence for this 8D model. |

## Existing capital and lexical routing

| Path | Read depth | SHA-256 | Relevance / non-transfer conclusion |
|---|---:|---|---|
| `work/astra-capital/00_START_HERE.txt` | Full, 8 lines | `4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360` | Followed task-first pin/status/dossier navigation; authority and scope rules. |
| `work/astra-capital/agent/CURRENT.txt` | Full, 6 lines | `8b7ddf96051daad68917f8c37d936984f99c4ff78891d8ce7929376dc70fa1aa` | Current inventory metadata says generated access/status aids do not certify mathematics. |
| `work/astra-capital/agent/RECENT.tsv` | Last 20 of 42 lines | `46612d0d09cc3bbb0a417e7bef6a139980e1881abdc0b7dbb5e0f6099bf85faa` | Recent intake through N805; no direct FJ nonlinear point-query route was identified. |
| `work/astra-capital/agent/concepts/p.tsv` | Targeted row searches; `pde` line 53 and `picard` line 105 (320 lines total) | `25f2d650bca9ab85fd4654d3423ba4b0b3c95a89f9959a7d88988c2de88731f2` | `pde` routes to N415 and `picard` to N731. |
| `work/astra-capital/agent/concepts/b.tsv` | Targeted row search; `branching` line 130 (171 lines total) | `6dfe2c272b3b40e1b5751d9b99108ad109179f6d28f6291ea312568a80570dc6` | `branching` routes to N783. |
| `work/astra-capital/frontier/dossiers/N731.txt` | Full, 50 lines | `7adee85b40ccd124a7da2adce7fd34fb07a07e59177987895b81431f171361f5` | Navier–Stokes snapshot-to-path minimax claim with a different input/output contract and open independent-review/acquisition gate. No proof range reused. |
| `work/astra-capital/frontier/dossiers/N415.txt` | Full, 44 lines | `642854c98256ac7481bebbd7770ddb8e786fdfb287d334c1bc32e17f153f8542` | Full-space fractional-PDE representation for a restricted distributional class; unrelated operator/domain and open review gate. No proof range reused. |
| `work/astra-capital/frontier/dossiers/N783.txt` | Full, 90 lines | `f9e0c41cd87d57ba7dae4b636a85f8664dc2e32ec61c6b6d550717054037e4f8` | Retained-repair/carrier reward model; physical state/kernel/acquisition gates remain open. Not an elliptic branching solver result. |

The three dossiers are `source_derived_unreviewed` in their own stated scopes. None establishes, refutes, or supplies assumptions for the incoming periodic quartic point-query theorem. Their original proofs were not opened because the task has no transfer to those PDE or physical-state statements.

## External primary literature

1. Beck, Gonon, Jentzen, “Overcoming the curse of dimensionality in the numerical approximation of high-dimensional semilinear elliptic partial differential equations,” *Partial Differential Equations and Applications* 5, article 31 (2024), [publisher page](https://link.springer.com/article/10.1007/s42985-024-00272-4), [official arXiv record/source](https://arxiv.org/abs/2003.00596), arXiv:2003.00596. Read the publisher abstract/introduction and Theorem 1.1/MLP recursion (HTML lines 41–165), Corollary 3.11 (lines 1147–1161), and Theorem 3.16 plus the full-history cost recurrence (lines 1351–1368). The publisher renders the Corollary 3.11 displayed bound as an image; the official arXiv TeX source was also inspected for the explicit RMS factor \(M^{-n/2}[1+(1+\sqrt M)\sqrt{L/\lambda}]^n\). Used to map and cost one published MLP certificate, not to claim a lower bound on MLP.
2. Fan, Sun, Yang, Lu, “Physics-Informed Inference Time Scaling for Solving High-Dimensional Partial Differential Equations,” ICLR 2026, [official proceedings abstract](https://proceedings.iclr.cc/paper_files/paper/2026/hash/cf8353a0efc3644454a5591a7cb55c17-Abstract-Conference.html), read lines 0–10 only. It describes SCaSML's defect PDE and stochastic correction of pretrained PDE surrogates, with reported examples up to 160 dimensions. Used only to delimit prior-art scope; no quantitative benchmark claim was taken from the abstract.

## Execution environment and validation depth

- Host: macOS 25.4, arm64; Apple clang 17 (`clang-1700.6.3.2`); Python 3.14.3.
- The two owned C++ programs were rebuilt with `clang++ -O3 -std=c++17 -Wall -Wextra -pedantic` and both exited successfully. `benchmark.cpp` ran a fixed 47-sample result, a 100,000-sample diagnostic, and 1,000 repeated 47-sample timings. `sparse_deterministic.cpp` ran its build/query and cached-query timings. Results are preserved as JSON; timings are single-run measurements.
- `analyze.py` uses Python `Fraction` for all tube inequalities and MLP/tree count recurrences, asserts the relevant inequalities, and emits the JSON diagnostic. Its Fourier support/evaluation cross-check uses ordinary complex doubles.
- `deterministic_interval.py` ran using the existing read-only `work/FE-hidden-gate/venv` (mpmath 1.3.0), 40 decimal digits, and emitted the exact-expression interval plus the contraction-radius solution enclosure. It does not validate FJ's floating-point random sampler.
- No grid solution, physical parameters, data acquisition, external experiment, or exact nonlinear reference was used. Timing variation, random-generator bias, and source-model evaluation bias for FJ remain unmeasured.
