# Decision-matched quantum transport calibration

This package contains the derivation, explicit rational quantum-response witnesses, full error polynomials, sensing/control certificate and reproduction code. The physics, scope and evidence limitations are in `research_note.md`.

The main computed output is a uniformly near-optimal interaction setting from one local measurement contrast, with unknown U and d. It is not an experimentally acquired transport value. Synthetic counts are labelled as such.

## Verify existing artifacts

Use Python with NumPy, SciPy, Numba and SymPy. The recorded environment is in `results/resource_ledger.json`; those versions are observations, not minimum-version guarantees. Run from this directory:

```sh
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
python code/verify_multi.py
python code/certify_policy.py
python code/structural_checks.py
python code/physical_polynomial_checks.py
python code/acquisition_protocol.py
```

`verify_multi.py` regenerates the complete exact Gram matrices and output polynomials of every packet from its rational operator coefficients, without running the optimizer. `certify_policy.py` checks all parameter intervals, globality, sensing errors, regret, fixed-control lower bound and the exactly indistinguishable pair. Timing fields change on rerun; exact substantive fields should not.

`acquisition_protocol.py` simulates labelled binomial observations for tests. It does not connect to hardware. Its `select_control(plus_count, shots)` function accepts an integer number of +1 outcomes and either specified shot count, and returns the rational command. The probability/physical assumptions and extra actuator budget must actually hold before using that command.

Example import (replace counts with actual validated observations, not simulated ones):

```python
import sys
sys.path.insert(0, "code")
from acquisition_protocol import select_control
# V = select_control(actual_plus_count, 262144)
```

## Regenerate all response coefficients from scratch

The following constructs a dictionary from span-eight words. It does not use a previously solved response as input:

```sh
python code/fresh_benchmark.py results/fresh_acquisition
python code/multi_solver.py --basis-file results/fresh_acquisition/witness.npz \
  --order 3 --out results/main_multi
python code/multi_certificate.py results/main_multi.npz results/main_multi_exact
python code/build_multi_anchors.py results/anchors
python code/certify_policy.py
```

Numerical acquisition is a heuristic proposal with fixed caps; acceptance requires the exact residual certificate. The narrow known parameter family is a successful instance, not a guarantee that these caps suffice elsewhere. Reproduction time and intermediate disk usage exceed verification alone. Main matrices can use about two GiB RAM in the recorded run; this is not a uniform memory guarantee.

## Files and provenance

- `results/main_multi_exact.npz` stores exact derivative coefficients and their denominator. Its matching JSON stores exact full residual Grams and output polynomials.
- `results/anchors/*_exact.*` are six newly computed anchor families; four are used, two unsuccessful-for-this-purpose attempts remain charged and preserved.
- `results/policy_certificate.json` is the compact global sensing/control certificate.
- `results/acquisition_checks.json` contains the optional coarse-calibration budget and labelled synthetic tests.
- `results/resource_ledger.json` records fresh construction costs and their exclusions.
- `results/standalone_verification.json`, `structural_checks.json` and `physical_polynomial_checks.json` document finite checks, not external review.
- `code/fast_algebra.py`, `local_solver.py`, `prior_exact.py`, `jet_solver.py`, `jet_certificate.py`, `adaptive_jets.py`, `fresh_benchmark.py` and associated single-parameter support modules are reused/adapted from the preceding conversation's compiler. New multivariate and sensing modules have explicit docstrings.

The archive intentionally omits large floating discovery checkpoints and caches. The final rational witnesses and data needed to verify all reported bounds are included. No font files, third-party package binaries or laboratory data are included.

No repository was modified. No formal proof, independent scientific validation, universal inversion theorem, high-dimensional global-optimization result or experimental implementation is claimed.
