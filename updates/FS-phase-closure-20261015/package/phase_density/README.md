# Astra direction-preserving density research

Read `PHASE_DENSITY_COMPATIBILITY.md` for the analytic arguments and `CHECKPOINT.md` for the exact unfinished state.

The full quasiconvexity question is not solved. The package supplies a general convex amplitude replacement and Picone identity for rank-one-convex vectorial energies, a continuum certificate for one coupled phase, an exact obstruction to joint convexity, and unsuccessful compatible counterexample searches.

## Verify

```
python verify_directional_density.py
python certify_adaptive_dual.py
python certify_phase_density.py 512
```

The symbolic checker needs SymPy. The interval checkers need SymPy and NumPy and rely on outward-rounded IEEE basic arithmetic, with rational bounds for trigonometric evaluations. They do not trust the stored numerical search outputs. Their rational input is `phase_density_certificate.json`.

The exploration scripts additionally require SciPy and PyTorch. Their collocation/Gauss values are not theorem certificates. `adaptive_continuum_certificate.json` and `directional_density_verification.json` contain the actually completed checks. Prior checks and their scope are under `audit/`.

No private repository data, third-party manuscripts or fonts are included. A file-integrity manifest is supplied; hashes do not establish mathematical correctness.
