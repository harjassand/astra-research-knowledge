# Restart-and-reconstruct transport: research package

Read `research_note.md` for the full mathematical construction, scope, costs, and remaining thermodynamic theorem.

The theorem addresses a **classical randomized additive estimate of the full finite-ring current response**, at fixed positive physical dephasing and bounded finite-range interactions. It does not require dominant dephasing or a supplied many-body gap. Its conservative worst-case overhead is impractical. It is not a high-precision theorem for the infinite chain.

## Reproduction

With Python, NumPy, SciPy, and SymPy installed:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python checks.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python schur_check.py
```

`checks.py` writes `checks.json`, including exact small block identities, floating physical quotient checks, finite-ring reconstruction diagnostics, a synthetic monitored-trajectory test, and a conservative resource budget. `schur_check.py` writes `schur_exact.json` with a rational counterexample to interpreting the full population Schur complement as a Markov generator.

These scripts use full small-system representations. **They do not implement the asymptotic locality-based block/MPS compiler proved to exist in the note.** They are debugging and falsification tests, not a scalable production solver, independently reviewed proof, formally verified code, or laboratory evidence.

`checkpoint.md` records the theorem and exact remaining obligations. `manifest.json` records package hashes. No repository was modified.
