# Rigorous scalar clock ingredient — author construction

**Certified:** `1.106580521912579472 <= s_* <= 1.106580521912579663` for
`e'=2(s+3e²/4)²`, `e(0)=0`.

**Not certified by this package:** finite-N actual clearance time, a stochastic
boundary/interface theorem, or novelty relative to ordinary validated ODE solvers.

- `PROOF.md`: ordinary proof, complete error ledger and conditional interfaces.
- `validated_clock.py`: standalone Python exact-rational/directed-dyadic solver.
- `CERTIFICATE.json`: coarser 507-step certificate.
- `CERTIFICATE_FINE.json`: 1,142-step, width `<1.896e-16` certificate.
- `verify_saved.py`: exact checks plus full deterministic replay of both runs.
- `SOURCE_BINDINGS.json`: hashes and qualified roles of inputs.
- `VERIFY_RESULTS.json`: replay results, created by the verifier.

From the parent directory:

```sh
python inverse_clearance_clock_20261101/validated_clock.py \
  --order 12 --grid-power 7 --end 256 \
  --output producer-workspace/scalar_clock_fine.json
python inverse_clearance_clock_20261101/verify_saved.py
```

No installs, external sources, floating confidence intervals, `flint`, `arb`,
NumPy, or SciPy are needed. This is an author self-check, not independent review.
