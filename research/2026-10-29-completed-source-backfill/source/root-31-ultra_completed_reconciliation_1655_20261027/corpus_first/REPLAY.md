# Offline reproduction

Use the shared read-only Python runtime. It pins NumPy2.5.4, SciPy1.18.1 and SymPy1.14 in the adjacent solver_runtime/requirements.lock. No external service is used by the computation replay.

From the original task workspace:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
producer-workspace/python -B \
producer-workspace/replay_all.py
```

The13 scripts run sequentially in dependency order, writing owned results and logs. The final fresh replay passed in24.3seconds with one BLAS thread. Runtime metadata changes between runs; hashes pin a saved snapshot, not runtime-field byte determinism. The source manifest records downloaded primary PDFs. fetch_sources.py is optional network retrieval and is not invoked by the computation replay.

Important checks:

- compile_classical: all16 exact rational Holevo identities;385-state controlled model;1540 exact matrix columns; stochasticity and nonnegativity.
- direct_polytope / instrument_rank_check:15-state controlled model;60 exact columns; exact rank-nine reachable and observable minors; nonzero temporal correlation.
- exact_product_counterexample: all225 exact witness inequalities, rational gate unitarity, rational negative output expectation.
- repair_frame: floating LP/dual search proposes two extra rational projectors. This step alone is not certification.
- exact_repair_kernel: every one of289 columns has exact nonnegative rational weights, exact unit mass and exact nine-by-nine matrix intertwining. It uses integer arithmetic and a fixed spanning-basis residual correction.
- kernel_robustness: exact minimum positive weight and the rational1/12000 channel-neighbourhood inequality.
- circuit_replay: six overlapping/reversed placements on three qutrits versus full density evolution. This tests implementation; local exact identities establish the arbitrary-size statement.
- werner_unraveling / verify_unraveling_full: phase moments, nonnegative Schmidt factors,1800 spectrum fixtures and96 full-state comparisons against an independent Kraus calculation. The all-dimensional argument is in MATHEMATICS.md and is an independent specialization of known Lami-Huber2016 science.

The positive product-cone diagnostics at c=2 are finite diagnostics only. The exact counterexample is at c=9/5, where single-site closure is also proved; it does not reject c=2 product-cone closure. Threshold-search failures are retained in their own JSONs. Source-search failure is also retained: the old Vidyasagar author URL returned an HTML response rather than a PDF; that file is named accordingly and excluded from valid PDF provenance.

Expected evidence files include REPLAY_ALL.json, EXACT_REPAIR_RESULT.json, KERNEL_ROBUSTNESS.json, INSTRUMENT_RANK.json and FULL_UNRAVELING_VERIFICATION.json. The full exact transition artifact is EXACT_REPAIRED_KERNEL.json. All outputs live in this owned folder. Earlier completed research folders and the shared runtime remain untouched.
