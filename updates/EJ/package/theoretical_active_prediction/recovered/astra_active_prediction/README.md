# Active imaginary-time predictive certification

Read `research_note.md` for the exact access model, complete proofs, limits, primary-source comparisons, and the separate Genesis interface bridge.

Run the diagnostics:

```sh
python verify.py
python verify_genesis_bridge.py
```

Requirements: Python 3.10 or later, NumPy, SciPy. Setting `OPENBLAS_NUM_THREADS=1` can avoid unnecessary threading overhead on the small test matrices.

`diagnostics.json` and `genesis_bridge_diagnostics.json` are the actual output of those scripts in this research session. Tests are finite mathematical diagnostics, not a proof checker or quantum hardware experiment. `MANIFEST.json` hashes each other supplied file.

No original source repository was modified. Historical novelty and independent proof validation are unresolved.
