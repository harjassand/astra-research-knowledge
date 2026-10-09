# Applied inverse-problem candidate

Start with `FINITE_TIME_FRAGMENTATION_INVERSE.md` for the exact model, proof,
reconstruction algorithm, limitations, primary-source comparison, and status.

## Current status

Promising direct finite-time fragmentation inverse. The continuous theorem and
algorithm passed one focused AI-assisted mathematical check, included here.
This is not external expert review or formal certification. Priority remains
provisional. No real experimental validation.
The proposal requires calibrated mass-weighted data, known positive rate
exponent, and controlled near-parent fragmentation/measurement behavior.

## Reproduce

Dependencies already present in the included environment: Python, NumPy, SciPy,
mpmath. No installs, external jobs, or repository publication are required.

From this directory:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python test_fragment_inverse.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python continuum_test.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python fast_baseline_test.py

The JSON result files preserve all outcomes, including numerical failures in
adverse near-constant-rate tests. High-precision repair is recorded separately.
`continuum_test.py` is an event-driven continuous-size simulation independent
of the geometric-grid forward model; it uses a fixed seed and 4 million mass
tags. Its sampling model is explicitly idealized, not a laboratory dataset.

The likelihood baselines use the full finite-time forward model, a
nonnegativity constraint, and an analytic adjoint. The matrix-free version uses
classical uniformization and is independent of the proposed conjugacy. Timings
against converged likelihood fitting should not be read as an accuracy-matched
lower bound on every early-stopped or regularized optimizer.

See `FOCUSED_PROOF_PRIOR_AUDIT.md` for the AI-assisted check, attribution of
the established spectral-conjugacy mechanism, and all important limitations.
`requirements.txt` records the exact dependency versions used. No dependency
installation is needed in the environment in which these results were made.

No Astra or OpenAI/math repository was used. Primary paper URLs and exact arXiv
version where available are recorded in the research note.
