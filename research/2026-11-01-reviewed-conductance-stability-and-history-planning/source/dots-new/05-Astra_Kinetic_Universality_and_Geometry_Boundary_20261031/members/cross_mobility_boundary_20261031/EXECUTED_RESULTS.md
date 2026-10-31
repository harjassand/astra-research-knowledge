# Executed result

Final independent audit: PASS.

- Author: 305 exact algebra/grid checks, 21 malformed parsed-object rejections,
  2 raw duplicate-key rejections, 1 pre-allocation budget rejection, 4 exact
  rational certificates.
- Independent: exact symbolic identities, exact full-fiber boundary/patch
  diagnostics, all 4 certificates replayed, 73 additional valid models,
  17 additional malformed objects, 3 raw duplicate-key cases, 8 budget cases,
  and 2 exact budget boundaries.
- Higher-dimensional extension: reviewed analytic Gaussian-tail/shoulder proof,
  symbolic dimension-dependent Lyapunov, and exact H3 arithmetic/asymptotic checks.
- Valid/invalid CLI paths and compilation all PASS.

The standalone rational example k=128, epsilon=1/100000000 certifies

    capacity < 3.601 x 10^-7,
    capacity / mu(A) < 1.441 x 10^-6.

These displayed decimal inequalities round OUTWARD. Exact certificates retain
the positive tail term that ordinary float output rounds away. The matrix
condition number is at least approximately 1.6384 x 10^12; this severe geometric
cost is part of the example, not suppressed.

The main analytic result is exact: within the stated fixed 2D potential and
full-fiber basin geometry, cap(D_n)->0 iff the conditional longitudinal mobility
vanishes AND the cross coefficient diverges. No all-cross-terms failure claim
is made. The high-dimensional corollary transfers the same paid obstruction to
the relative freely-equilibrated benchmark.

No actual-capacity PDE was solved; the rigorous inequalities prove the result.
Quadrature/sample outputs are optional diagnostics, never the guarantee.
