# Validation and one failed finite-size check

30 October 2026. Run:

```
python new_science/continuation9_20261030/physical_mechanism/check_wave_counter.py
```

The executed script independently builds the normalized four-mode drift and both noise matrices. It checks the characteristic polynomial, exact canonical covariance identity, momentum-reversal identity, real slow-mode projection and the native velocity spectrum including conservative auxiliary noise. It also evaluates the grounded-loss pole against its distinct k^4 asymptotic. These are population-model checks, not physical measurements or acquired precision certificates.

Executed maxima:

* Characteristic polynomial coefficient error: `2.89e-15`.
* Stationarity and momentum-reversal identity errors: zero at the arithmetic precision displayed.
* Slow projection identity error: `9.00e-16`.
* Direct versus passive-impedance spectrum error: `1.34e-15`.
* Sampled covariance error divided by `(kappa+ell)`: at most `0.628` in the checked cases. This sampled number is not the proof's universal constant.

The initial check included `kappa=1/log(33)` at N=32. For one chosen set of coefficients this lies outside the small-parameter real-slow-pole neighborhood: two poles form a complex pair, and the real-pole momentum-reversal projection has zero signature. That assertion failed even though the polynomial and spectrum identities already agreed. The governing proof explicitly asserts the projection only for sufficiently small ell and kappa. The executed projection cases were therefore restricted to `.1/log(N+1)` and `N^(-1.5)`, with N in `{32,128,512}`, and now assert that the chosen pole is real. This is an application-boundary failure, not a correction of the polynomial or a numerical proof that the asymptotic sequence works at every small N.

The all-time covariance, complete path convergence, Gaussian exponential tightness, rare-current scale and actual physical supplier scope are proved in `RECIPROCAL_WAVE_COUNTER.md`; finite matrix checks do not replace them. `WAVE_COUNTER_CHECKS.json` preserves the parameters and executed outputs. No further fixtures are required for this unit.
