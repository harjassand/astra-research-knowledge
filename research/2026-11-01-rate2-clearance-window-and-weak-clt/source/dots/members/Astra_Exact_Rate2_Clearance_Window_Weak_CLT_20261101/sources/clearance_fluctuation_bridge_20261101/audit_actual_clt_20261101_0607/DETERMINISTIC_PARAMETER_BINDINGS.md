# Separate deterministic parameter receipts: identification, not new numerical replay

The main weak-CLT proof does not depend on a numerical solver. The following
previously accepted deterministic numerical results may now be attached to its
parameters because the functions and normalization are mathematically identical.
Their older receipts remain unchanged and retain their original deterministic
scope. It is the new actual-chain proof, not a rewriting of those receipts,
that supplies the weak-limit identification.

## Scalar center

- `inverse_clearance_clock_20261101/SCALAR_FREEZE.json`:
  `11c22f296fadc36a5374c5bfab2c7b214a3c2a77ea27f3a5910055f93027b4a5`.
- `audit_inverse_clock_certificate_20261101/RECEIPT.md`:
  `cd479dd41961133eecf6477916bf3fefe84f0d8a59f2a66ec46f315a148af723`.
- That audit's `RECEIPT_BINDINGS.json`:
  `e6d5fbaf44968a7096eac0abacfb27278247c2853ec8eec9ca327d6694fa5cab`.
- Fine certificate:
  `ad0e3e581ed0a6d516c1cd56498fea073ff15f6d5411bd7ca009e9769c98fe21`.

The exact same origin orbit satisfies l=s+3e²/4, so its maximal time is the
accepted scalar s_*. The prior outward enclosure is

    1.106580521912579472 <= s_* <= 1.106580521912579663.

The CLT centers at the mathematical s_*, not at an arbitrarily chosen fixed
endpoint or rounded midpoint of this interval. A fixed nonzero centering error
multiplied by T/sqrt(T) would eventually diverge. Numerical precision required
for a finite-N standardized calculation is a separate consumer question.

## Weak-fluctuation parameter

- `inverse_clock_variance_20261101/VARIANCE_FREEZE.json`:
  `60636c65f720823168088f2b97760d5473f3fe5b51c6388369fedd1ada456129`.
- `audit_inverse_clock_variance_20261101/RECEIPT.md`:
  `ecab49dfe2546f8d59f1294d7d7cc5b99cf691294791bc0f0b44da35e44c9f3c`.
- That audit's `RECEIPT_BINDINGS.json`:
  `daaa7535453b6b4934143d4f186a200c5a3f2b3f32cc03a958371e5a57115076`.
- Variance-functional certificate:
  `2d4e2c09d7213b8998b630d05624b8f6528ddd568e3d640dd0602d581b0ca806`.

The deterministic receipt evaluates int(1-J_inf)² dl on the origin orbit.
Since b_l=J_inf-1 and the new bridge independently derives the actual leading
rate 1+3l²e=dl/ds, this is exactly the Sigma² in the limiting normal law.
Its previously accepted outward enclosure is

    0.5677211094 <= Sigma² <= 0.5687113183.

It remains impermissible to read this as an enclosure of Var(tau)/T at finite N,
or as proof that Var(tau)/T converges. The new weak limit alone does not provide
uniform integrability, means, variances, rates of CDF convergence, or a normal
approximation at any specified finite N.

`check_parameter_bindings.py` independently read back all 63 payload pins
across these four earlier manifests. Selected controlling proof/certificate/
receipt bytes are snapshotted in this audit; the full old numerical runtime is
not duplicated here. The saved earlier numerical replay evidence is received,
not claimed rerun by the present audit. This separation avoids both circular
acceptance and silent promotion of numerical code to a stochastic theorem.
