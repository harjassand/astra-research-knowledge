# ASTRA collision-dual research package

Read **RESEARCH_NOTE.md** for the model, proofs, input/output contract, cost accounting, prior art and limitations.

The main result is an ideal-arithmetic exact one-particle sampler with finite expected work uniform in collision time, for a restricted homogeneous isotropic Maxwell/Gaussian-scale-mixture family with 0<a<b<3a/2. The executable is a floating-point research prototype, not a bit-exact implementation. Historical novelty and independent proof verification remain unresolved.

## Files

- `collision_dual.py`: finite marked genealogy, unbiased observable estimators, and a full-law bounded-error sampler for any 0<a<b.
- `exact_extension.py`: bounded signed Laguerre estimator and rejection extension. Its linear Bernoulli factory implements Mark Huber's published method, explicitly credited in the source and note.
- `validate.py`, `results.json`: independent moment/finite-state references and broad-family diagnostics.
- `validate_exact.py`, `exact_results.json`: factory and exact-extension floating-point diagnostics.
- `environment.json`: versions in the environment where the saved tests were run.
- `MANIFEST.json`: SHA-256 hashes of the other bundled files.

## Run

Use Python 3 with NumPy and SciPy. The precise versions used are in `environment.json`.

```bash
python -m pip install -r requirements.txt
python validate.py --output results.json
python validate_exact.py
```

The scripts use fixed seeds. Numerical timing varies by machine. Random samples can vary across library versions. Test scripts overwrite their result JSON files; retain the supplied files separately when comparing reruns. No external service, API key, GPU or quantum device is required.

## Minimal example

```python
import numpy as np
from collision_dual import DiscreteVariance
from exact_extension import exact_velocity_ideal_prototype

rng = np.random.default_rng(123)
initial = DiscreteVariance((1.0, 1.1), (0.5, 0.5))
velocity, work = exact_velocity_ideal_prototype(
    t=1_000_000.0, a=1.0, b=1.1, rho=0.2,
    initial=initial, rng=rng,
)
print(velocity)
print(work)
```

The theorem refers to ideal primitives. This example uses floating-point approximations and does not have certified total-variation error relative to the continuous target law. There is no iteration cap: adding one without reporting failure would change the law.
