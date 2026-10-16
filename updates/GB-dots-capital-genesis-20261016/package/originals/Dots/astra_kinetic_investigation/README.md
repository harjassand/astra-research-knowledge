# Reproducibility package

Start with **REPORT.md** for scientific scope and results, **PROOFS.md** for complete analytic arguments. No foundational or historical-novelty claim is made.

## Replay

Use a Python environment with numpy, scipy, sympy and numba. Executed versions and CPU details are in `environment.json`. All commands are run from this directory. No network access is needed.

```sh
OPENBLAS_NUM_THREADS=1 python verify_algebra.py
OPENBLAS_NUM_THREADS=1 python run_replicates.py 0 12
OPENBLAS_NUM_THREADS=1 python fsp_reference.py 100 .2
OPENBLAS_NUM_THREADS=1 python fsp_reference.py 120 .2
OPENBLAS_NUM_THREADS=1 python validate_sampler.py
OPENBLAS_NUM_THREADS=1 python summarize.py
```

Replays overwrite their corresponding JSON files. Floating stochastic replay may depend on library/CPU versions; exact rational checks do not depend on stochastic replay. Wall times are not expected to match. The 12 main runs take roughly three minutes in the measured environment; source acquisition, failed attempts and process startup are outside that figure. This is not a promise about another machine.

## Contents

- `kinetics.py`: independent direct SSA and standard fixed-level splitting.
- `run_replicates.py`: preselected seeds and main 2x4 experiment.
- `split_rep_*.json`: all 12 independent main run records, including each interface.
- `split_pilot.json`: excluded coarse-interface tuning pilot.
- `fsp_reference.py`: independent two-site absorbing-overflow sparse master equation.
- `fsp_*.json`: floating matrix-exponential reference and overflow masses.
- `validate_sampler.py`, `sampler_validation.json`: SSA/splitting diagnostic against the two-site master equation.
- `verify_algebra.py`, `algebra_checks.json`: exact identities and positive rational divergence witness.
- `algebra_explore.py`: retained exploratory symbolic calculation.
- `summarize.py`, `experiment_summary.json`: reported descriptive statistics.
- `input_contract.json`: explicit scientific model/observable contract and source identity.
- `environment.json`: versions, timing scope, processor details, and known failed attempts.
- `MANIFEST.json`: SHA-256 hashes of packaged files, excluding itself.

The exact counterexamples use eventual hitting, while the spatial benchmark uses finite-horizon first entry. They must not be conflated. The two-site calculation is an implementation diagnostic, not a substitute for the full eight-site scientific experiment. No original NNCME training run or tensor/control incumbent is claimed.
