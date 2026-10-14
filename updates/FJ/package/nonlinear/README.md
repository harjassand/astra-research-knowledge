# Reproduce the nonlinear-query investigation

Python 3.10 or newer is required.

```bash
python -m pip install numpy numba
python verify_certificates.py
python nonlinear_query.py --samples 200000 --output results.json
```

`research_note.md` contains the theorem, construction, proof, costs, limits and prior-art assessment. `exact_certificate_checks.json` records exact rational verification of the global inequalities. `results.json` records the original numerical run, including seeds, confidence radii, node counts, timings, the full-field FFT baseline and rejected certificates.

The reference is a converged floating-point FFT calculation, not an interval-verified continuum solution. The Monte Carlo confidence theorem assumes ideal random draws and exact arithmetic. The executable is an ordinary floating-point prototype. The one-dimensional FFT baseline is faster than the new implementation. Historical novelty and superiority over the strongest existing algorithms are not established.

The predictors are explicitly constructed from the input equation. No nonlinear solution is used to construct them. There is no generation-depth cap, rejection of costly paths, or post-selection of successful samples; zero products are short-circuited exactly. Numba compilation time is reported separately from query time. Repeated timings will vary with hardware and software versions.
