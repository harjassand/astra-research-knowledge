# Reproducible research package

Read `RESEARCH_NOTE.md` for the theorem, proof, assumptions, empirical analysis, prior-art limits, and scientific status. No physical validation of a new operation or novelty claim is established.

Requirements: Python 3.10 or later; NumPy and SciPy.

Run:

```sh
python -m pip install numpy scipy
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python closure_experiment.py
python empirical_analysis.py
```

Outputs:
- `synthetic_results.json`: exact synthetic checks, assumed-noise tests, hidden-support failures, and two analytic counterexamples.
- `empirical_results.json`: arithmetic on three published experimental objective traces, with source URLs.

The synthetic plant simulator knows its matrix; the acquisition estimator receives only the simulated measured sensor responses. The empirical objective values were manually transcribed from the public CSV text, not generated synthetically. They validate only the published reciprocal baseline, not the proposed extension. Numerical roundoff may vary across linear-algebra libraries.
