# Independent review: Type-II small-gradient implication

9 November 2026. Analytic reconstruction and primary-source reading only. No numerical, symbolic, optimization or PDE run was performed. This review followed receipt of the author's argument and prior discussions; it is not a blind rediscovery.

## Binding and disposition

Inspected governing source: `quartic_orbit_cone_20261109/TYPE_II_SMALL_GRADIENT_LEMMA.md`, SHA256 `f19819dfa7a09ff5d564d07b852c93acd02a266843d0e47740f399aa7875ecc9`. Its bytes are preserved separately. The original-J_r source remains `56bda4a48ac763013df9f5110e2ada9dd6d680a94edf5b6bebf8738b32566830`, with its own completed independent review.

**The abstract analytic implication passes under its explicitly stated assumptions.** The Hodge correction, finite-exponent mixed derivative inequality, cubic ideal bound, all coefficient factors and absorption radius check. No counterexample was found to that implication. The positive quartic reserve is essential to this proof and is now an explicit hypothesis, rather than silently attributed to the entire rank-one-convex cone.

**The whole-cone corollary remains conditional on the complete N806 algebraic contact classification.** I directly reread its Section 2.3 and the analytic sections, but did not independently reconstruct every classification branch and its cited joint-contact variation. This review must not be represented as an independent proof of that entire classification. Unlike that conditional generalization, the separate J_r review independently reconstructs the acoustic determinant and all degenerate means for the literal J_r polynomial.

The earned variational property is the displayed fixed-mean small-gradient inequality, called weak quasiconvexity in Kristensen (1999). It is neither arbitrary-amplitude quasiconvexity nor an extension agreeing locally with a globally quasiconvex integrand. No radius uniform over normalized means, coefficients, coordinate changes, or the boundary of the coercive cone is established.

## 1. Exact unconditional family

The analytic theorem applies to any homogeneous quartic F on real 2 by 2 matrices, whether or not left-SO(2)-invariance is separately imposed, at each specified mean for which all the following data are supplied in fixed gradient-compatible coordinates:

1. F(X) >= c_* |X|^4 with c_*>0.
2. Its exact Taylor quadratic, after subtracting a determinant null Lagrangian, is nonnegative and controls c^2+(d-lambda a)^2 by a positive constant nu_*; lambda is nonzero.
3. Its exact cubic restricts on c=0,d=lambda a to kappa a^3.
4. The cubic has no term quadratic or cubic in b: partial_b^2 C=0 identically in all matrix entries.

No pointwise projection of a gradient is assumed to remain a gradient. No hypothesis is replaced by testing a few matrix samples. The theorem makes no assertion that every rank-one-convex homogeneous quartic meets these conditions. The normal-form assumptions can cover rank larger than two as inequalities, although the intended application has rank two and kernel exactly the stated plane.

For a Type-I mean, the separate sufficient assumptions are a rank-one quadratic kernel, a positive quadratic lower bound on its transverse component, and a cubic containing at most one power of the kernel coordinate. The displayed pointwise estimate then follows directly. Noncontact means are handled by the classical strict Legendre-Hadamard argument, not by declaring the full Hessian positive definite.

Conditional on N806's classification, the union covers the strictly coercive, non-polyconvex members of the nine-coefficient planar homogeneous quartic cone invariant under left SO(2), at all their acoustic contacts. Adding strict noncontacts, zero, and the already quasiconvex polyconvex members yields the stated conditional all-mean weak-QC conclusion. It does not cover the entire cone without a reserve and does not cover arbitrary dimensions or arbitrary quartics.

## 2. Hodge map and mixed derivative estimate

Write r=d-lambda a. With zero mean for r,

    phi1^0=phi1+lambda^(-1) partial_1 Delta^(-1)r,
    phi2^0=phi2-partial_2 Delta^(-1)r.

Differentiation gives d0-lambda a0=r-Delta Delta^(-1)r=0. These corrections are actual derivatives of a modified potential. Each component of E=Dphi^0-Dphi is an order-zero multiplier, so finite p=2,3,6 estimates suffice. After removing constant vectors, the curl identity gives a periodic psi with phi1^0=psi_2/lambda and phi2^0=psi_1. Both signs and the factors lambda in the source are correct.

The required inequality is

    ||psi_12||_3 <= I ||psi_11||_2^(1/2)||psi_22||_6^(1/2).

It is the coordinate-swapped instance of the independently reconstructed inequality in the J_r review. On finite Fourier sums with frequency axes removed, the analytic family |D1|^(2z)|D2|^(2-2z)psi has the L2 endpoint at Re z=1 and L6 endpoint at Re z=0. Coordinate imaginary powers obey finite-p multiplier bounds with polynomial growth in Im z. Gaussian damping and three-lines interpolation give the geometric mean. Directional Hilbert transforms recover the signed mixed derivative. This uses neither an L-infinity multiplier estimate nor a full-gradient quadratic coercivity gap. Frequency aspect ratio and square side length do not enter the constant.

The bounds on r in p=3,6 follow from its L2 energy and the ORIGINAL pointwise bound |r|<=(1+|lambda|)epsilon. In particular, the proof never assigns such an infinity bound to E. The source's constants

    K0=(1+H2)/sqrt(nu_*), K1=|lambda|,
    K2=|lambda|H6(1+|lambda|)^(2/3)nu_*^(-1/6)

are valid. They yield exactly its A1,A2 and

    ||a||_3 <= A1 epsilon^(1/6)M^(1/12)Qbar^(1/4)
               +A2 epsilon^(1/3)Qbar^(1/3).

Cubing costs at most the stated factor 4. The degeneracies M=0 or Qbar=0 require no division and are included.

## 3. Cubic ideal and constants

The coordinates (a,b,c,r) are independent because lambda is fixed. Vanishing of C-kappa a^3 when c=r=0 implies that each monomial contains a normal factor c or r. The no-b-squared identity is unchanged under d=r+lambda a. A remaining monomial has either at least two normal factors, or exactly one normal factor and a^2 or ab. Thus

    |C-kappa a^3| <= L_C[N^2|X|+N|a||X|], N=|c|+|r|.

For example, (1+|lambda|) times the absolute coefficient sum of C-kappa a^3 in these coordinates is a valid L_C. No positivity solver or optimization oracle is required for this finite bound.

The first term integrates to at most (2/nu_*)epsilon Qbar. Holder with exponents 2,3,6 controls the second because ||N||_2<=sqrt(2/nu_*)Qbar^(1/2) and ||X||_6<=epsilon^(1/3)M^(1/6). This gives the two mixed terms

    A=epsilon^(1/2)M^(1/4)Qbar^(3/4),
    E=epsilon^(2/3)M^(1/6)Qbar^(5/6).

With B=epsilon Qbar, E=A^(2/3)B^(1/3)<=(2/3)A+(1/3)B. All exponents and the factors sqrt(2/nu_*) agree. Combining this with the kappa a^3 bound gives exactly the displayed C1,C2. There is no discarded leave-and-return or high-frequency term: the estimates act on the entire gradient and its full Fourier representation.

## 4. Reserve, radius and domains

The linear term and determinant term integrate to zero for periodic gradients or zero-boundary tests. The positive quartic reserve then leaves

    Qbar+c_*M-C1 sqrt(epsilon)M^(1/4)Qbar^(3/4)-C2 epsilon Qbar.

The radius min(1,(2c_*/C1)^2,1/(9C1^2),1/(4C2)), after enlarging zero constants to positive ones, is sufficient: the mixed Young term costs at most c_*M/2+Qbar/4, and the last term costs Qbar/4. The claimed residual Qbar/2+c_*M/2 follows.

Mollification preserves the original gradient supremum bound. Zero extension of zero-trace Lipschitz tests on the admissible bounded Lipschitz domains gives a periodic test in a larger square; transformed compact supports can be treated identically. Fixed invertible left/right maps require the corresponding potential and domain transformation. No arbitrary nonintegral map is asserted to preserve the original periodic lattice.

All finite-p operator constants are declared rather than numerically evaluated. Consequently this is an existence theorem with a formula in those constants, not a certified numerical radius or a finite-bit algorithm for arbitrary real coefficient inputs. Constants can worsen as lambda approaches zero, as nu_* or c_* approach zero, or as coordinate maps become ill-conditioned.

## 5. Prior comparison and what is actually added

The strongest directly relevant inherited source is N806 `CONTACT_COMPENSATION.md`, at Astra pin bb16dbf0e9c9b9ecaacfd10f577aedef51bd2e0e, SHA256 f47796d9088b9a4b75c43d31f93b05d36dbe025c4db9d6a8ec02dbd6d0a8ca28. It already supplies the Type-II geometry, cubic closure, compatible Hodge correction and L2/L4 to L^(8/3) mixed interpolation. The present change uses L2/L6 to L3, the original small supremum bound, and the normal cubic ideal to obtain an absorbable small coefficient. It is an incremental consequence of that contact machinery, not a new general interpolation or Hodge method. N812's all-background Schur/concentration obstruction remains unresolved by a fixed-mean radius.

Primary sources checked:

- Kristensen, *On the non-locality of quasiconvexity* (1999), definitions pp. 3-4 and Proposition 1, https://www.numdam.org/item/AIHPC_1999__16_1_1_0.pdf. This establishes the terminology distinction and supplies the classical strict-Legendre-Hadamard comparison. The degenerate Type-II proof is not obtained merely by citing that strict result.
- Bruno-Pasqualotto, *Quasiconvexity for the Dacorogna-Marcellini Energy*, arXiv:2608.06367v1, Theorems 1-2 and introductory scope, https://arxiv.org/html/2608.06367v1. Their global result in the bi-SO(2) symmetry class is stronger in amplitude but does not directly cover the present one-sided invariant family.
- Gutierrez, *A Necessary Condition for the Quasiconvexity of Polynomials of Degree Four*, JCA 13 (2006), Proposition 3.3, Proposition 4.1 and Corollary 4.2, https://journalofconvexanalysis.com/articles/jca13004/jca13004.pdf?v=2. It already studies cubic cancellation at null acoustic directions and a resonant three-wave discriminant as a necessary condition. The inspected statements do not assert this uniform sufficient small-gradient bound for all compatible tests.
- Bandeira-Pedregal, *Quasiconvexity: the quadratic case revisited, and some consequences for fourth-degree polynomials* (2008), Sections 3-4 and Theorems 2-3, https://matematicas.uclm.es/omeva/wp-content/preprints/preprint10-08.pdf. Their displayed quartic criteria concern quasiconvexity at zero and a Fourier variational characterization, not this full-rank degenerate-background radius.

This was a targeted prior check, not a proof of historical novelty or an exhaustive literature search. No claim of practical impact is established. A sharp integrated discriminant for arbitrary amplitudes, a QC extension near the mean, and uniform control as the mean varies all remain outside the result.
