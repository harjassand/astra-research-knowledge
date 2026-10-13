# Conditional lattice-loop transport research packet

Read **DERIVATION_AND_EXPERIMENT.md** first. This packet records a proposed
experiment, model identities, limitations and reproducible arithmetic. It does
not establish a novel physical effect or a useful technology.

## Contents

- `DERIVATION_AND_EXPERIMENT.md`: derivation, coupled material constraints,
  symmetry and timescale restrictions, experiment and rejection criteria.
- `check_transport.py`: dimensionless model and algebra checks; not a material simulation.
- `checks.json`: output from the included script.
- `SOURCES.json`: primary-source metadata and the scope of use.
- `MANIFEST.json`: file hashes and the environment used for the checks.

## Reproduce

Use Python 3.10 or newer with NumPy and SciPy installed, then run:

```sh
python check_transport.py --output checks.json
```

No data download, paid API, DFT installation or external service is used by the
script. Floating-point checks are not interval-certified proofs. Re-running the
same equations does not independently validate an experiment or historical
novelty. The arbitrary dimensionless amplitudes and synthetic stiffness matrices
are test fixtures, not favorable properties attributed to an actual material.
