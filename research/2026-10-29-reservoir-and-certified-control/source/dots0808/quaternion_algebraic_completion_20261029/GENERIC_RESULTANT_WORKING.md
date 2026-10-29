# Generic resultant completion — working, not accepted

2026-10-29. This does not supersede the accepted finite-grid oracle or claim a generic implemented bit-complexity result.

## Primary facts actually retrieved
Sodomaco, *The product of the eigenvalues of a symmetric tensor*, arXiv:1802.10173v2, https://arxiv.org/pdf/1802.10173, Definition 1.2, Theorems 1.3 and 3.8, Proposition 3.11: for a four-variable quartic the E-characteristic polynomial is Res((1/4)grad F-lambda Qq), generically degree40; for regular tensors its roots are the normalized eigenvalues. Its coefficient c_j has degree108-j in F's coefficients. Cartwright–Sturmfels supply the generic distinct eigenvalue count. These are prior mathematical assets, not Astra discoveries.

## Derived candidate bad-polynomial bound
Let R_F(lambda)=sum_{j=0}^{40} c_j(F)lambda^j. The ordinary degree40 discriminant has total coefficient degree78 and index-weighted degree40*39=1560. Substituting deg c_j=108-j makes its degree 78*108-1560=6864. Thus c_40 Disc(R_F) has degree6932. This improves the crude degree8532 bound.

The proposed fixed-chart exclusion polynomial is the ternary homogeneous resultant at q0=0 of f0, q1*f2-q2*f1, q1*f3-q3*f1, where fi=partial_i F. Degrees are3,4,4. Resultant multidegrees16,12,12 give coefficient degree40. It has extraneous potential roots at q1=0, but nonvanishing is sufficient for absence of any boundary eigenray. Nonvanishing has now been checked on the retained perturbed Choi–Lam quartic by exact Groebner[1] in all three projective charts of this exact three-polynomial system; see check_resultant_boundary_witness.py and resultant_boundary_witness.json (0.13s). Adding it gives degree6972.

## Remaining load-bearing obligations
1. Prove simple roots of R_F imply unique reduced projective eigenrays, not a hidden positive-dimensional fiber with one resultant root. A general smooth-resultant/incidence theorem may settle this but has not yet been supplied here.
2. CLOSED at executed exact-witness scope: the particular boundary resultant is not identically zero on quartic-gradient coefficient space. This uses its own three-equation chart check, not the earlier full-eigenboundary check.
3. Construct an executable eigenvalue primitive-element representation, or pay a separately bounded separating-projection search. An arbitrary fixed z projection need not separate the40 rays.
4. Supply actual fixed-degree elimination/root-isolation bit-cost bounds and input/output contracts; the completed matrix/net fallback only proves polynomial inverse-accuracy cost.
5. Keep current-source privacy: candidate-dependent retries or elapsed computation cannot be treated as neutral sampler aborts. Deterministic padding or a separate failure-bias analysis remains necessary.

Conditional on a nonzero bad polynomial of degree D, perturbing all35 coefficients independently on an N-point rational grid gives failure at most D/N by polynomial zero counting after affine translation. This conditional statement does not claim that D=6972 is already established. A perturbation with coefficient l1 norm at most epsilon/4 changes every unit-sphere objective by at most epsilon/4. These elementary perturbation facts alone do not close obligations1–4.

## Elementary simple-root uniqueness lemma (new derivation, awaiting review)
Let H=(H_0,...,H_3) be four homogeneous cubics and r(H) their universal resultant. Suppose q is a common projective zero. For each block i, every coefficient direction v_i satisfying v_i(q)=0 keeps q a common zero of H+t v, for all t. Therefore the coefficient gradient d_i r(H) annihilates the kernel of evaluation at q. It is consequently beta_i times the vector of degree3 monomial evaluations at q.

If two rays q and q' are common zeros and dr(H) is nonzero, a nonzero block must be proportional both to Veronese_3(q) and Veronese_3(q'). The cubic Veronese embedding is injective, so the rays coincide. In particular a simple root lambda of r(H(lambda)) has nonzero ambient gradient and exactly one projective common zero. This excludes all positive-dimensional fibers. No reducedness assertion was needed.

For H_i=(partial_i F)/4-lambda Q q_i, a nonzero resultant polynomial excludes an isotropic common zero: such a zero has Q=0 and grad F=0 and would remain a common zero for every lambda. Every root therefore gives a unique nonisotropic eigenray. If coefficients and lambda are real, conjugation fixes this unique ray; choosing its q0=1 representative makes every coordinate real.

Assume the boundary polynomial is nonzero, so q0!=0. For some block i the resultant derivative with respect to the q0^3 coefficient is nonzero. The ratios

    (partial r / partial H_i[q0^2 qj]) / (partial r / partial H_i[q0^3])

are exactly qj/q0 for j=1,2,3. Thus one can extract coordinates as rational functions of lambda using coefficient derivatives of the universal resultant, rather than a fixed separating z projection. Different blocks may be required at different roots; a finite four-block test suffices. Exact interval refinement can certify a nonzero denominator at every isolated simple real root. This is a finite symbolic construction, not yet an executed resultant-derivative implementation or a reviewed bit-cost theorem.

Reviewer refinement (derive_matching_survival_bound, independent provisional agreement): derivatives must be taken in the80 INDEPENDENT coefficients of four cubics, before substituting their quartic-gradient relation. Define A_i(lambda) from q0³ and B_ij(lambda) from q0²qj in block i. No root of R annihilates all four A_i, so gcd(R,A_0,...,A_3)=1. Extended Euclid constructs b_i with sum b_i A_i=1 modulo R. The single polynomial representative X_j=sum b_i B_ij modulo R then equals qj/q0 at every eigenvalue. This closes primitive-element extraction algebraically without a reduced critical-ideal assumption. Implementation and uniform bit-cost closure remain outstanding.
