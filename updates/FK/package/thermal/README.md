# Reproduce the finite-anchor thermal-response obstruction checks

This package records a **rejected mechanism**, not a new many-body solver.

Read `REPORT.md` for the exact models, proofs, source attribution, scope and failures.

Run from this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python checks.py --out results
```

Requires Python 3.10 or later, NumPy and SciPy. No external datasets, training,
network calls, quantum hardware, or authors' code are used. The retained run
used NumPy 2.3.5 and SciPy 1.17.0. The version numbers document the environment;
they are not assertions that those are the latest releases.

`results/results.json` contains all checks, environment versions and timing.
CSV files contain the response and convergence values. Assertions fail on a
violated check. Floating-point convergence is not a certified truncation bound.

The 64^3 lattice test evaluates a first perturbative coefficient exactly as a
finite momentum sum. It does not simulate the full interacting system at finite
quartic coupling. The oscillator tables are spectral reference computations,
not measured finite-anchor sampler outputs. Diagnostic timing is not a speedup.

No claim of independent validation or historical novelty is made. Source papers
are not bundled; their identifiers and their roles appear in REPORT.md.
