# Independent Astra research handoff: stationary generator tomography

**Status: independent derivation and self-tests, unreviewed; no historic breakthrough or verified novelty.**

The main research record is `RESEARCH_HANDOFF.md`, containing the mathematical proof,
explicit information and cost contract, current prior art, falsifiers, and Astra bridge.

Run (Python 3.13; NumPy, SciPy and scikit-learn needed):

```bash
python proof_checks.py
OPENBLAS_NUM_THREADS=1 python stationary_tilt_experiment.py --sizes 500 2000 8000 32000 --reps 25 --output results.json
OPENBLAS_NUM_THREADS=1 python general_identity_torus.py --sizes 24 40 64 96 128 192 --output torus_results.json
OPENBLAS_NUM_THREADS=1 python entropy_production_experiment.py --n 2000 8000 32000 --reps 12 --output entropy_production_results.json
```

This packet contains results `results.json`, `torus_results.json`,
`entropy_production_results.json`, and `proof_checks_results.json`, together with their
reproduction scripts and a provenance manifest. No online API or GitHub writes required.

Additional restricted-model experiment:

```bash
OPENBLAS_NUM_THREADS=1 python weak_stein_torus.py --grid 128 --sizes 1000 5000 20000 80000 --reps 12 --output stein_results.json
```

It estimates 11 coefficients directly from weak generator moments, **but the eight drift basis functions are supplied**; related weak-form Stein methods are established prior art.

Matched-information **adversarial comparator** (25 paired repetitions per size; complete data in `matched_comparator_results.json`):

```bash
OPENBLAS_NUM_THREADS=1 python matched_stein_comparator.py --sizes 500 2000 8000 32000 --reps 25 --output matched_comparator_results.json
```

The fitted baseline-potential score-moment estimator competes with and sometimes outperforms logistic density-ratio estimation on the exact same samples, so there is **no new algorithmic dominance claim**.
