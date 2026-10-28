# Actual computations and replay

Use the read-only provisioned Python runtime from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ../solver_runtime/.venv/bin/python verify_exact.py
```

This command was executed successfully. The final receipt is
`data/EXACT_REPLAY.json`; its scope and source hashes are included.
`aspect_family.py` also executed successfully, acquiring the continuum
polynomials and both exact Sturm sequences in about1.18 seconds.
The independent replay took about2.6 seconds on this host. Exact profile
moment acquisition took about.49 seconds. These are observed local
timings, not a complexity or performance advantage claim.

Numerical searches before exact acquisition are preserved separately:

| Restriction/objective | Actual retained record | Best positive value |
|---|---|---:|
| Fourier cutoff1, Δ/M4 in F/α units | fourier_cutoff1.json,16starts | .92524580 |
| Fourier cutoff2 | fourier_cutoff2.json,12starts | .73307806 |
| Fourier cutoff3 | fourier_cutoff3.json,12starts | .59152128 |
| Residual-directed Fourier mode growth,24→56modes | mode_growth.json,8generations | .391320 |
| P1 mesh8 uniform diagonal | fem_n8_alt0.json,12starts | .44384563 |
| P1 mesh16 alternating diagonal | fem_n16_alt1.json,8starts | .40030468 |
| Covariance-diversity-constrained then released searches | diverse_fourier3.json, diverse_fem16.json,30pipelines | no negative value |
| Δ/c search, Fourier cutoff3 and P1 mesh16 | schur_ratio_search.json,16starts | .13320357 on P1 |
| P1 prolongation/refinement16→32→64→128 | schur_refinement.json,8new starts | .1057691743 for Δ/c |

All paths in the table are under `data/`. These are restricted numerical
candidate generators; a positive local minimum is not a QC certificate.
The searches record122 start/pipeline/generation records in total and
about64.21 seconds of timed numerical optimization bodies, including
rejected candidates. Imports, symbolic setup, human/agent reasoning,
source acquisition and all tool overhead are outside those numerical
timers. No physical acquisition, experiment, purchase or paid compute
was performed. The directory data occupies about8.5MiB on this host.

Finite Fourier quadrature uses at least4K+1 points per coordinate for
fourth-degree moments of cutoffK fields. The residual-directed growth
uses a grid large enough for the cubic Euler residual frequencies.
P1 moments use exact equal triangle weights; no sample quadrature is
needed. The exact proof rounds the selected nodal values to denominator
10⁸ and reacquires every moment; the rounded field is the authoritative
profile, not the floating candidate.

The Schur-ratio envelope derivative was also checked in8 random directions
on each of Fourier cutoff3 and P1 mesh16. Maximum central-difference
errors were5.47×10⁻¹² and1.11×10⁻¹¹; `data/NUMERICAL_CONTROLS.json` stores
the actual result. `search_schur_ratio.derivative_check()` replays this
bounded numerical control. The exact conclusions do not require an
optimizer stationarity or global-optimality assertion.

Recorded `gradient_norm` fields in the Schur-ratio search/refinement are
the base Δ/M4 gradient norm, not the Δ/c gradient norm. They are not
evidence of stationarity for Δ/c. The exact conclusions use only the
acquired rational profile, not any stationarity or globality claim.

Core files actually used are `compatible_core.py`, `search_fem.py`,
`search_schur_ratio.py`, `refine_schur.py`, `exact_profile.py`,
`aspect_family.py`, and `verify_exact.py`. Earlier candidate-generation
scripts and all their actual records remain in the directory.
