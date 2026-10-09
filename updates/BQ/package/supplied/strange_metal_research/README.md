# Conditional thermality tests: reproducibility package

This package contains analytical derivations, counterexamples, and synthetic numerical checks from an investigation of anomalous electronic noise. **It does not contain experimental data, an empirically established mechanism, or a claimed foundational scientific discovery.**

Read `RESEARCH_NOTE.md` for assumptions, complete derivations, empirical limitations, and attribution. `CLAIM_STATUS.json` records the distinction between conditional mathematics, numerical checks, and scientific discovery.

## Reproduce

Use Python 3.10 or newer. Install NumPy, SciPy and SymPy in a virtual environment:

```sh
python -m pip install -r requirements.txt
python check_theorems.py
python check_heat_potential.py
```

The scripts write JSON results into `results/`. They use no network access and require no experimental input. The seeded graph tests are reproducible up to library/platform floating-point differences. No claim of bit-for-bit cross-platform reproducibility is made.

`check_theorems.py` tests 1,500 frozen-temperature networks, explicit hypothesis-breaking counterexamples, and 60 weak-bias electrothermal network/frequency cases. `check_heat_potential.py` tests 24 nonlinear one-dimensional spatial boundary-value problems and symbolic coefficient relations.

The scripts are finite numerical diagnostics, not formal verification. The extended tensor geometry in the analytical heat-potential proof is not simulated by the one-dimensional BVP test.

`sources.json` preserves repository revisions, accessed paths, primary literature identifiers, and raw-data acquisition failures. `MANIFEST_SHA256.json` records package file hashes (excluding itself). No files were written to the upstream repositories.
