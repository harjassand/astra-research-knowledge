# Self-audit and precise failure boundaries

This is the author's self-audit, not independent mathematical review.

The high-gap estimate was checked at its delicate point: the off-diagonal entry is normalized by the geometric mean of the two commuting endpoint densities. This gives the exponent \(aQ\). Diagonal corrections are even in \(b\), including the \(-bv p_2\) term, and are bounded by \(b^2[(3/2)\sup|p_{22}|+a\sup|p_{122}|]\). A bound using the smaller endpoint for the off-diagonal entry would lose the sharp exponential radius.

The radial construction uses two distinct index controls. The point's radius controls the low-gap cutoff \(A_{k+2}\); the shift length controls \(A_{\ell+2}\). The thresholds enforce both. The inequality \(k(s+c_0)\le k(s)+1\) then handles every intermediate point in the distribution's support. This avoids treating compactness at a fixed radius as uniform control of unbounded shifts.

For the low-gap estimate, convexity makes the Taylor factor \(e^{-F}\le1\) globally. The bound does not require \(F\) to be small before the final Hessian estimate. The exact order-one sphere formula supplies the distribution constant explicitly.

The finite-radius endpoint is open. A potential with slope tending to \(R\) has \(V(z)/|z|\to R\), so interior moments exist; the separate inequality \(V(z)\le R|z|\) forces divergence on every boundary ray tube. This is stronger than just showing that the domain contains the target ball.

For \(b_n=e^{-Rn+\sqrt n}\), the tilted variance must diverge as the tilt approaches \(R\). No uniform boundary variance or product-coordinate noise is smuggled into the construction.

Each block normalizes to identity. The whole POVM is a direct sum of normalized measures, with strong countable additivity. Its Fourier identity is a strong operator identity, and its characteristic need not be norm-continuous at zero. Scalar shifts \(c_n\) cancel the normalized tilted inequalities and translate the positive block densities; they do not give uniform global energy tails.

The existence proof constructs one density directly. It does not deduce a common regularizer by intersecting finite truncation existence statements, mixing laws with incompatible domains, or applying the FU norm-interior theorem outside its hypotheses.

The comparison is sharp within the stated separated two-dimensional block architecture. It does not prove that norm-entire interactions suffice for arbitrary unbounded observable pairs, nor that every open convex domain inside the necessary vertical strip is attainable. The ellipse addendum gives every finite requested set of interior tilts; a covering family of ellipses does not establish one-law strip attainment.

Replayed checks passed: exact symbolic Schur identities at axial and arbitrary tilts; 120 rational kernel moments through total degree 14; explicit cutoff and low-/high-gap bound evaluations for the all-exponential and critical-radius examples. Their finite scope is retained in CHECKS.json. Historical priority, external review and formal verification remain open.
