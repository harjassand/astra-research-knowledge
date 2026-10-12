# CRAY analytic-anchor research packet

Start with `RESEARCH_NOTE.md`. Proof status and limitations are explicit there and in `RESTART.md` and `CLAIMS.json`.

## Reproduce

Python 3.13; recorded environment in `environment.json`. Requires NumPy, SciPy, and Numba.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python audit.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiment.py --h 0.02 --duration 600
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiment.py --h 0.01 --duration 2400
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiment.py --h 0.005 --duration 2400
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python connected_test.py
```

The audit uses exact fractions for coefficient tests and sampled algebra inequalities. The stochastic solver and independent quadrature are floating-point diagnostics. Neither the specialised baseline nor the stochastic implementation is an interval-certified quadrature or arbitrary-precision production implementation. Re-execution changes timings and may show small platform numerical differences.

`MANIFEST.json` hashes payload files; it establishes file integrity, not mathematical or experimental validation. No third-party manuscripts, fonts, or earlier research packets are included. No GitHub changes were made.
