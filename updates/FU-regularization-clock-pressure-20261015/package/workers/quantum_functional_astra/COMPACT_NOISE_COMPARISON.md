# Independent comparison of the two compact-noise proofs

Date: 2026-10-15. This is a new comparison artifact. Neither frozen proof nor the earlier polynomial packet is modified. The root explicitly authorized cross-comparison after both derivations were frozen.

## Frozen inputs

1. Astra spectral-gap proof: `workers/quantum_functional_astra/COMPACT_NOISE_COMMUTATIVITY.md`; SHA-256 `b26fc0183066ba380b30049d352b6c7d547942cdb75a4f798e7a6967b726eb24`.
2. Independent operator-adversary entire-function proof: `workers/operator_adversary/COMPACT_NOISE_PROOF_PL.md`; SHA-256 `d4faf34610df74b94508852da54c12a8a3b4b7f0dc3df479541dc2a7c28db147`.

Both paths are relative to the research packet at `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-regularization-clock-pressure-v1`. Both files were read in full. The hashes were checked against the freeze records. The independent reviewer also reported that the Astra spectral-gap proof has no material gap; that report is corroboration, not a substitute for the written proof.

## Shared theorem and shared reduction

For a finite tuple of bounded self-adjoint operators on an arbitrary complex Hilbert space, existence of a positive normalized weak POVM satisfying

\[
\widehat M(t)=\widehat\nu(t)\exp\!\left(i\sum_jt_jA_j\right)
\]

with compact scalar probability noise is equivalent to pairwise commutativity. No finite-dimensional compression, eigenbasis, trace, or separability hypothesis is needed.

Both derivations independently use the same effective reduction. Positive one-dimensional marginal identities supply actual exponential integrals. When the noise transverse to a tilt is bounded, the tilted POVM has a uniformly bounded transverse first moment. Differentiation of the exact scalar multiplier contract gives

\[
J(s)=\int_{-1/2}^{1/2}e^{usA}Be^{-usA}\,du,
\qquad \sup_{s\geq0}\|J(s)\|<\infty.
\]

The derivative is justified by the bounded transverse coordinate and a uniform Taylor remainder against the positive exponential weight. This does not require analytic continuation of a distributional identity to unbounded test functions. Scalar noise coordinates may be dependent.

## Audit of the independent entire-function route

No material gap was found in the operator-adversary proof.

- The extension `J(z)` is entire in operator norm. Self-adjointness of `A` gives the exponential-type bound `||J(z)|| <= ||B|| exp(||A|| |Re z|)`.
- On the imaginary axis the integrands are unitary conjugates, so `||J(it)|| <= ||B||`. On the real axis the tilted first-moment argument supplies the required bound.
- The quadrant damping factor is valid: with the stated branch, the real part of `exp(-3 pi i/8) z^(3/2)` is at least `cos(3 pi/8) |z|^(3/2)` throughout the closed first quadrant. It dominates the linear exponential growth on a sufficiently large arc and does not enlarge the boundary-ray bound. The origin is a boundary corner where the damped function is continuous; holomorphy across that corner is unnecessary.
- Applying the maximum-modulus principle in quadrant disks, then taking the damping parameter to zero and rotating, establishes a global bound. Liouville applies to each scalar matrix coefficient. Separation by matrix coefficients gives `J(z)=B` as an operator identity.
- The Taylor coefficient is correct: `integral_{-1/2}^{1/2} u^2 du / 2! = 1/24`, so constancy forces `[A,[A,B]]=0`.
- With that double commutator zero, the full unitary orbit is exactly `exp(itA) B exp(-itA)=B+it[A,B]`. Its constant norm then forces `[A,B]=0`.

The proof remains valid on nonseparable Hilbert spaces. Its commuting converse with a smooth compact scalar density is also valid: spectral integration of translations of a compact smooth bump yields a positive norm-continuous compactly supported density. Its continuous image has separable range, providing the required Bochner measurability.

## What is independent about the spectral-gap route

The Astra proof closes the same reduction by actual reducing spectral cuts of `A`. For separated high and low parts, the Sylvester operator `D(Z)=A_H Z-Z A_L` has `||exp(-sD)|| <= exp(-s delta)`. The exact identity

\[
(I-e^{-sD})HBL=sD e^{-sD/2} HJ(s)L
\]

forces `HBL=0` from uniform boundedness of `J(s)`. Sending the separation gap to zero strongly makes `B` commute with every spectral cut of `A`.

This is a genuinely different closing argument from quadrant complex analysis and Liouville. It also directly provides the quantitative growth witness

\[
\|J(s)\|\geq
\frac{(1-e^{-s\delta})e^{s\delta/2}}{2s\|A\|}\,\|HBL\|
\]

for any nonzero separated block. The two proofs share the first-moment insight and their standard measure-theoretic reduction, so they should not be described as independent in every ingredient. Both explicitly avoid transferring the full multiplier contract to a finite-dimensional compression.

## Reconciled refinements and quantifiers

The directional theorem needs only bounded noise in the `B` coordinate and all **positive exponential moments** in the `A` coordinate. All negative exponential moments are unnecessary. The frozen entire-function proof states the stronger two-sided hypothesis, but its argument immediately admits the one-sided refinement because

\[
J(-s)=J(s)
\]

by changing the symmetric integration variable. Thus the real-axis bound needed there follows from positive tilts alone. Finite exponential moments at an unbounded sequence of positive parameters suffice, by interpolation. Neither proof removes exponential-moment assumptions in favor of ordinary moments alone.

For every fixed exact pair `(M,nu)` on a nonzero Hilbert space, compact support of `M` is equivalent to compact support of `nu`: coordinate marginals are positive convolutions with bounded spectral laws. Consequently, **existence** of a compact-output exact representation is another equivalent condition on the tuple. Commutativity does not say every exact representation has compact noise or output; noncompact scalar convolution is also allowed.

If an exact scalar noise law has exponential moments in every direction, every direction of bounded scalar noise must correspond to an observable commuting with the entire tuple. This is a necessary condition. No converse for arbitrary partially bounded support geometry is supplied by these proofs.

## Assessment

The arbitrary-Hilbert compact-noise commutativity theorem is established at the level of two internally reviewed written arguments with different closing mechanisms. The spectral-gap proof is shorter as the main proof and supplies a quantitative separated-block witness; the entire-function proof is useful as an independent analytical check.

Formal verification, external mathematical review, and historical priority remain unestablished. This comparison does not imply a new general joint-measurement impossibility theorem under weaker coordinate-marginal contracts, an approximate-error lower bound, an optimal tail theorem, or a practical measurement advantage.
