# Independent audit: anchored reference-filter high-noise payment

**Analytic PASS — 26 October 2026.** Governing note: `anchored_reference_filter_high_noise_payment.md`.

At the reference-only baseline B=I3 tensor A0, the BKM metric makes the physical-identity and physical-traceless components orthogonal. Reference partial trace contributes exactly the former component's metric; WH fixes that component and acts as minus physical transpose divided by two on the latter. Partial physical transpose is an isometry for this product-baseline BKM quadratic form, so its squared factor is 1/4. In the deficit Hessian the identity component cancels, leaving half the traceless metric. The entropy Taylor prefactor 1/(2s) consequently gives exactly `g_B(H)/(4s)`, with `H=3d(Phi-I9/9)`. This checks the load-bearing factor.

The same decomposition applies after the reference filter, which commutes with the physical conditional expectation. A0 is faithful and Z fixed/invertible, so finite-dimensional entropy Taylor expansion has an O(s^-2) remainder for each fixed source/filter. No uniform threshold near a singular baseline or scalar-filter degeneration is asserted.

The inverse success operator `sqrt(k)Z^-1` is a contraction. Its completion by a single erased failure outcome is CPTP. Applying it to the filtered baseline and tangent gives exactly success kB,kH and rejection baseline `beta I3`, with `beta=Tr(A0 F)`, and tangent `d(F^T-TrF I3/3)`, where F=Z*Z-kI. The transpose follows from the actual maximally entangled contraction. All trace factors agree.

BKM contraction follows by taking the second variation of relative-entropy data processing at the faithful baseline. Direct-sum additivity and homogeneous scaling receive `g_filtered>=k g_B+g_reject`. The scalar-baseline rejection metric is precisely `d^2 Tr(F-TrF I/3)^2 / Tr(A0F)`. For nonscalar Z*Z, F is PSD, nonzero and has a zero minimum eigenvalue; it cannot be scalar, so the numerator and denominator are strictly positive. This yields the stated strict positive limiting gap and hence a sufficiently-large-s anchored comparison for every fixed nonscalar filter. For Z*Z=kI, homogeneity and reference-unitary invariance give equality for all s.

The theorem is an asymptotic guard, not finite-noise monotonicity, a general reference-filter inequality, or a proof of the unresolved accepted-only GLS comparison.
