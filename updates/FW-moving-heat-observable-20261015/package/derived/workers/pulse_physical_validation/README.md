# Pulse physical-interface worker

Read [REPORT.md](REPORT.md). The original Zenodo MAT data are acquired and checksummed. Actual current, absolute capacity calibration, and initial-state control remain unavailable. The saved result is a conditional continuum gate and an executed original joint-domain incumbent, not physical validation.

From this directory, the core replay is:

```sh
uv run --python 3.11 --with numpy --with scipy python code/acquire.py
uv run --python 3.11 --with numpy --with scipy python code/audit_data.py
uv run --python 3.11 --with numpy --with scipy python code/paired_gate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --python 3.11 --with numpy --with scipy python code/joint_lp.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --python 3.11 --with numpy --with scipy python code/joint_target_queries.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --python 3.11 --with ./sources/hybrid-drt-e01dba1bf5f02fa6b63c82169c0652a5a695344d --with ./sources/mittag-leffler-6e875fa3e124d25420fd791e4e742d67599d94a7 python code/benchmark_hybrid.py
uv run --python 3.11 --with numpy --with scipy python code/check_results.py
uv run --python 3.11 --with numpy --with scipy --with matplotlib python code/make_figure.py
```

`MANIFEST.json` records local hashes; `RECEIPT.json` is the compact handoff. `results/paired_gate.json` is the analytic gate receipt; `results/hybrid_baseline.json` and NPZ arrays are actual upstream fit outputs. Finite-grid optima are marked exploratory. The exact rational endpoint discrepancy is not a voltage-noise confidence bound.
