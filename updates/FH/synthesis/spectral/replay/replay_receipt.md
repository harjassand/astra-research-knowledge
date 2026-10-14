# Safe-copy replay receipt

**Source:** `../FH-sources/spectral/` (read-only throughout).  
**Replay date:** 2026-10-14.  
**Scope:** producer validator and its own optical/reference outputs only.

The source tree was copied into `producer_copy/`, then duplicated into `producer_replay/`. The copied producer inputs (`README.md`, `optical_model.py`, `validate_operation.py`, `requirements.txt`, `environment.json`, `sha256sums.txt`) are byte-identical between those two directories and their hashes agree with the source's `sha256sums.txt`; the original source tree was not run in place or edited. `../evidence/source_hashes_local.sha256` records the direct source-to-copy checksums.

Command run from the workspace root:

```sh
work/FH-spectral/replay/producer_env/bin/python work/FH-spectral/replay/producer_replay/validate_operation.py
```

The replay passed all 73 producer assertions. The producer-declared environment is Python 3.13.5, NumPy 2.3.5 and SciPy 1.17.0. The replay used Python 3.13.2, NumPy 2.3.5 and SciPy 1.17.0, so the Python patch/minor build differs while the numerical libraries match. Standard error was empty. The 73-line validation log is byte-identical to the copied producer log.

The relevant producer thresholds were: laminate-moment comparisons `rtol=1e-12, atol=1e-12`; ideal static-reflection residual `<1e-12` on 801 `q` values from `1.2e6` to `4e8 m^-1`; sampled evanescent `Im(rp)>-1e-10` on a 121-by-101 frequency/`q` grid; homogeneous-layer subdivision `rtol=atol=1e-9`; witness-integral change `<1e-6` when increasing `n_q` from 10,000 to 20,000 over `1.2e6` to `1e9 m^-1`; harmonic covariance eigenvalue bounds with `1e-8` slack; covariance-integral comparison `rtol=1e-9, atol=1e-10`; and uniform-mass-scaling equality `rtol=1e-10`. These are finite numerical checks, not global continuum certificates. The imaginary-frequency maximum is sampled on a 160-by-200 grid, not a rigorous continuum bound.

The replay rewrote the copied output files. `results.json` is not byte-identical to the frozen producer result: 25 of 96 numeric JSON scalars differ in final floating-point digits; excluding the near-zero quadrature-error estimate, the largest relative difference is about (1.02\times10^{-14}), and the largest absolute difference among dimensionless response/error ratios is (3.96\times10^{-16}). The quadrature-error estimate itself differs by (2.22\times10^{-16}) absolute on a value near (3.9\times10^{-14}). The 121-row reflection CSV has identical frequency coordinates and maximum relative differences no larger than (5.88\times10^{-14}) in any reported reflection column. Hashes and per-column differences are recorded in `replay_diff.json`.

The independent global transfer matrix was also compared against the unchanged producer recursion over the full 121-row real-frequency CSV at `q=2e7 m^-1` and an 801-point static `q` sweep. The largest relative complex-reflection differences were `3.0e-14` for sequence A and `1.8e-14` for B on the frequency grid, and below `3.9e-15` on the static sweep; see `../analysis/cross_implementation_results.json`.

This receipt establishes safe-copy integrity, successful execution of the producer validator, and numerical agreement at floating-point precision in the rerun environment. It does not establish external mathematical correctness, fabrication, a measured dielectric tensor, κ-ET response, causality over untested bands, scientific advantage or novelty.

