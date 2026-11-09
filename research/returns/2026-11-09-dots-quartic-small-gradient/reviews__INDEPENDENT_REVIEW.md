# Independent audit: original quartic small-gradient inequality

9 November 2026. Hand-derived mathematical review and primary-source reading only. No symbolic receiver, solver, optimization, Fourier search, PDE, or numerical experiment was run. File retrieval, copying and hashing are administrative preservation only.

## 1. Binding and disposition

Governing source: `quartic_orbit_cone_20261109/LOCAL_QC_DEGENERATE_CONTACT.md`, SHA256 `56bda4a48ac763013df9f5110e2ada9dd6d680a94edf5b6bebf8738b32566830`. A byte-identical snapshot accompanies this review. The exact original polynomial convention agrees with `PROOF_CANDIDATE.md`, SHA256 `bbb833483c12e6063f7f75103cc99ba536cb75ccfe37223244ad0d97382cd417`, and the pinned original ROC source.

**Disposition: the explicitly stated small-gradient theorem passes this independent analytic challenge.** The corrected quadratic, cubic cancellations, positive quartic reserve, finite-exponent interpolation/Hodge estimates, absorption constants and symmetry transfer are consistent for every fixed r>0. No concrete counterexample or unpaid mathematical assumption was found for that result. Section 7 below independently derives the required acoustic classification from the literal polynomial, removing the need to treat the old symbolic principal-minor receipt as a black box.

**Mandatory terminology qualification:** the earned property is *weak quasiconvexity*, in the terminology of Kristensen (1999), or simply the displayed small-gradient variational inequality. It is not a proof that the integrand agrees with a globally quasiconvex function in a neighborhood, which that paper calls *local quasiconvexity*. The frozen source defines its precise small-gradient claim correctly, but its title and any summary need this distinction. It is also not global quasiconvexity, a uniform normalized-mean radius, or a moving-background theorem.

This review was performed after receiving the author's proof and prior analytical discussions. It is independent reconstruction of the written argument, not a blind historical rediscovery or a proof-assistant certificate. A proposed broader Type-II extension is outside this binding and requires a separate disposition.

## 2. Literal polynomial and algebra

Use the source parameters k=(2r+1)/3>1/3, B=(3k-1)/(8(k+1)), F0=(5k+1)/(2(k+1)), m=3k+1, q=m/(2k), and D=(3k-1)(k+1)/4. For X=[[a,b],[c,d]], put u=a^2+c^2, v=b^2+d^2, j=ad-bc. The original density is

    J(X)=B[k^2u^2+v^2+2uv+4kuj-4vj]+F0 j^2.

At A=[[0,k],[1,0]], the expansion with lambda=-3k(k+1)/2 is exactly

    J(A+X)-J(A)-DJ(A):X-lambda det X = Q(X)+T3(X)+J(X),
    Q=(mb+2kc)^2/4+Dd^2,
    T3=[(3k-1)b^3+(9k+1)b^2c+4kbc^2
        +(3k-1)(b+c)d^2]/2 -(mb+2kc)ad.

I independently obtained the cubic from the positive identity below. In particular all a^2 terms cancel. This is essential: a generic term a^2 d would not be paid by the claimed argument. The surviving a term contains the controlled normal coordinate s=mb+2kc.

The identity

    J(X)=B(ku-v+2j)^2+2B(k+1)uv+j^2

is exact because F0-4B=1. Minimizing the first square plus j^2 in j gives

    J(X)>=[(3k-1)/(4(5k+1))]
           [k^2u^2+v^2+(3k+1)uv]
         >=c_k |X|^4,
    c_k=(3k-1)min(k^2,1)/(4(5k+1))>0.

Here u,v are nonnegative, and 3k+1>2>=2min(k^2,1). No assumption on the determinant sign or rank of X is used. The bound degenerates as r approaches zero; no parameter-uniform positive constant is claimed. At the excluded endpoint r=0, the density is det^2, so this particular strictly positive reserve cannot persist.

For periodic gradients and zero-boundary gradients, both the linear term and det Dphi integrate to zero. The determinant term is a genuine null Lagrangian; the proof never treats a determinant-balanced arbitrary matrix law as a compatible gradient.

## 3. Mixed derivative estimate: endpoint and anisotropy checks

The required inequality is

    ||psi_xy||_3 <= I ||psi_xx||_6^(1/2)||psi_yy||_2^(1/2).

The exponents are correct: 1/3=(1/2)/6+(1/2)/2. For a finite Fourier sum after removing the frequency axes, the analytic family |Dx|^(2z)|Dy|^(2-2z) psi is legitimate. The imaginary-power factors are tensor products of one-dimensional multipliers. On a dyadic frequency interval their total variation is bounded by a fixed polynomial in the imaginary exponent, uniformly in frequency and period. One-dimensional Marcinkiewicz estimates and Fubini therefore give finite endpoint L2 and L6 bounds. Gaussian strip damping permits the three-lines argument; scalar exponential normalization gives the geometric mean of the two endpoint norms. Two periodic Hilbert transforms recover the signed mixed derivative at finite exponent 3.

The axis projection is bounded at the finite endpoint exponents and changes no mixed derivative. Its norm is included in I. There is no L-infinity endpoint and no claim that a Riesz or Hodge projection preserves an L-infinity bound. Isotropic square-size scaling cancels on both sides with unnormalized Lebesgue norms. The bound is also independent of frequency aspect ratio: the two coordinate multipliers act separately. Large-frequency or highly anisotropic trigonometric tests therefore do not invalidate it. Smooth approximation supplies the endpoint-derivative version used below.

This is standard complex interpolation/multiplier machinery, not a new harmonic-analysis theorem. The source gives a valid proof of the needed specialization rather than relying only on a named inequality.

## 4. Hodge estimate and all constants

Let delta=||X||_infinity, M=int|X|^4, and E=int Q(X). The source's elementary estimates follow directly from Q and |s|<=ell delta, ell=m+2k:

    ||s||_2<=2 E^(1/2),  ||d||_2<=D^(-1/2)E^(1/2),
    ||s||_3^3<=4ell delta E,
    ||s||_6<=2^(1/3)ell^(2/3)delta^(2/3)E^(1/6),
    ||a||_6<=delta^(1/3)M^(1/6).

For w=(phi1,-phi2/q), curl w=-s/m has zero average. Its periodic Hodge decomposition w=constant+grad psi+e with e=grad_perp eta is valid. The order-zero operators D grad_perp Delta^(-1) are bounded in p=2,3,6. Thus ||De||_p<=H_p||s||_p, H_p=K_p/m. The component identities in the source have the correct signs and q factors.

Consequently

    ||psi_yy||_2<=L E^(1/2),
    ||psi_xx||_6<=delta^(1/3)M^(1/6)+h delta^(2/3)E^(1/6),

with exactly the source L and h. Cubing the interpolation inequality and using (x+y)^(3/2)<=sqrt(2)(x^(3/2)+y^(3/2)) gives its U bound. The cubic e errors each cost at most 4ell H_3^3 delta E. Multiplying by the component factors 1 and q^3 and by |x+y|^3<=4(|x|^3+|y|^3) yields exactly its P and R:

    int(|b|^3+|c|^3)
      <=P delta^(1/2)M^(1/4)E^(3/4)+R delta E.

The first three cubic coefficients have absolute sum 8k. Their monomials are bounded by |b|^3+|c|^3. The d^2 term costs at most (3k-1)delta E/D; the sad term costs at most 2delta E/sqrt(D). This verifies the stated C1 and C2 without dropping a factor from the Frobenius norm or Hodge correction.

K_p and I are declared finite harmonic-analysis constants, not numerically evaluated constants. Thus the supplied radius is a positive analytic expression, not a numerical certificate. Standard effective multiplier bounds could in principle instantiate it, but this audit does not claim to have extracted those numerical bounds.

## 5. Absorption, zero cases and function classes

The final bound is

    gap >= E+c_k M-C1 sqrt(delta)M^(1/4)E^(3/4)-C2 delta E.

With M^(1/4)E^(3/4)<=(M+3E)/4, the source radius

    delta_k=min(1,(2c_k/C1)^2,1/(9C1^2),1/(4C2))

indeed gives gap>=E/2+c_k M/2. The two E losses are separately at most E/4. The M loss is at most c_k M/2. There is no division by M, E or a Fourier frequency, so their zero cases are included. In particular, an exactly zero quadratic energy does not conceal a negative cubic mode.

Periodic mollification preserves the original gradient supremum bound and converges in all relevant finite norms. Quartic polynomial integrals pass to the limit. Compactly supported tests may be extended by zero into a square; zero-trace Lipschitz tests on bounded Lipschitz domains have the required Lipschitz/Sobolev zero extension. No domain-dependent smallness constant is introduced. No claim is made for arbitrary W1,4 fields without the essential L-infinity smallness condition.

## 6. Symmetry and positive radii at the two contact classes

Left multiplication by O in SO(2) preserves u,v,j and therefore J. For R=A, direct substitution gives

    J(FR)=k^2J(F),  R^2=kI,
    J(I+X)=k^(-2)J(A+XR).

If X=Dphi, then XR is an actual gradient after x=Ry and replacing the potential by phi(Ry). Jacobians are positive absolute factors; a negative determinant of R causes no sign problem. The transformed test has compact support in a transformed domain, where the zero-extension version already applies. No unsupported identification of two periodic lattices is needed.

A valid radius at I is delta_k/max(k,1). Homogeneity and target rotation give positive radii at every nonzero scalar multiple of OA or OI. These two classes have opposite determinant signs and are both necessary. Nothing in this argument gives one radius uniform over all normalized affine means.

## 7. Independent acoustic matrix, strictness and exhaustive classification

This section independently supplies the extra premise used in the source's all-mean corollary. It does not execute the inherited ROC code.

Let H_t=e1 tensor (1,t), f=F0/(2B)=2(5k+1)/(3k-1), and h=1+f=(13k+1)/(3k-1). Direct differentiation of the literal J gives D^2J(H_t)=4B M(t), where in (a,b,c,d) order

    M(t)=[ 3k^2+t^2,  2t,          -2kt,       3k-t^2;
           2t,         1+3t^2,      -k+3t^2,   -2t;
          -2kt,       -k+3t^2,      k^2+h t^2, -f t;
           3k-t^2,    -2t,          -f t,       h+t^2 ].

Writing z=t^2, its first three leading principal minors are

    3k^2+z,
    3[(z-k)^2+(3k-1)(k+1)z],
    [3z(k+1)/(3k-1)]
      [4z^2+(3k^2-6k-1)z+k^2(3k+1)^2].

The final bracket in the third minor equals

    [2z+(3k^2-6k-1)/4]^2
      +(3k-1)(k+1)(9k+1)(5k+1)/16,

which is strictly positive. Thus the first three minors are positive whenever t is nonzero.

For completeness, the fourth minor can be derived without a long symbolic determinant expansion. Let D0(t)=det M(t). It is an even polynomial of degree at most eight. Evenness follows from the exact invariance J(SFS)=J(F), S=diag(1,-1). The right-A identity yields

    t^8 D0(k/t)=k^4 D0(t).

At t=0, M has rank three and kernel n=(0,k,1,0). Write M=M0+tM1+t^2M2. Then

    M1 n=(0,0,0,-(2k+f)),
    n^T M2 n=3k^2+6k+h,
    (M1n)^T M0^dagger(M1n)=(2k+f)^2/(h-3).

The last two quantities agree because h(3k-1)=13k+1. The quadratic coefficient of the scalar kernel Schur complement vanishes, hence so does the t^2 coefficient of D0. Its constant term is zero. Reciprocity then eliminates the t^6 and t^8 terms as well, leaving D0(t)=c t^4.

At t=sqrt(k), congruence by diag(k^(-1/2),1,k^(-1/2),1) gives two blocks after simultaneous symmetric/antisymmetric diagonalization. The symmetric scalar factors are 3(k+1) and k+1. The antisymmetric two-by-two determinant is

    (3k-1)(k+1+2f)-16k=3(k+1)^2.

The congruence determinant factor is k^(-2). Therefore D0(sqrt(k))=9k^2(k+1)^4 and

    det M(t)=9(k+1)^4t^4,
    det D^2J(H_t)=9r^4t^4.

Sylvester's criterion proves strict positive definiteness for every finite nonzero t and every r>0. At t=0 the two axis blocks have the source's rank-three form and kernel span{A}; at E12 the kernel is span{I}, either by direct differentiation or the right-A transform.

Quartic tensor symmetry gives D^2J(F)[H,H]=D^2J(H)[F,F]. Every nonzero rank-one H is reducible by a proper output rotation and scalar to H_t or E12. The strict calculation and axis kernels therefore prove that the nonzero means with an acoustic zero are exactly

    F=t O A or F=t O I,  t!=0, O in SO(2).

This includes both determinant signs and excludes all other nonzero means, not just a tested grid of frequencies. At every remaining nonzero F, compactness of unit rank-one directions gives a strictly positive Legendre–Hadamard constant. Fourier/Plancherel and a cubic Taylor estimate then give the ordinary small-gradient inequality. At F=0, pointwise quartic coercivity applies at every amplitude. This completes the all-affine-mean weak-quasiconvexity conclusion without a conditional imported acoustic assertion.

## 8. Optional expansion

The optional tau=1/N ansatz is consistent with the exact gradient components

    a=tau^2 psi_xx, b=tau^3 psi_xy,
    c=-q tau^3 psi_xy+tau^4 chi_x,
    d=-q tau^4 psi_yy+tau^5 chi_y.

Thus s=2k tau^4 chi_x. Q contributes the stated order-eight square terms and order-nine cross term. J contributes Bk^2 tau^8 psi_xx^4 with no order-nine term. Substituting c=-q b in the leading cubic yields coefficient -D/k times tau^9 psi_xy^3. This verifies the displayed expansion for fixed smooth profiles. It is not a uniform remainder estimate over varying profiles and is not needed by the main theorem.

## 9. Prior, terminology and scope

I directly read Kristensen, *On the non-locality of quasiconvexity*, Ann. IHP C 16 (1999), pp. 3–6: https://www.numdam.org/item/AIHPC_1999__16_1_1_0.pdf . The paper distinguishes weak quasiconvexity (small gradient perturbations at each mean) from agreement with a globally quasiconvex extension near the mean. It also proves the familiar strict-Legendre–Hadamard case, and shows in higher dimensions that even the stronger local-extension property does not imply global quasiconvexity. The new work here concerns the degenerate contacts; the strictly elliptic part is classical.

At Astra pin bb16dbf0e9c9b9ecaacfd10f577aedef51bd2e0e, I retrieved the following primary internal sources and preserved their content:

- N806: `updates/FJ/package/quartic/CONTACT_COMPENSATION.md`, Git blob c389a2da5e5ece51be6dd7768344bd4136712fa5. Sections 2–5 already derive the contact cubic cancellation, finite-p Hodge correction, complex-interpolation mixed derivative bound, and contact-ray positivity under relative transverse-norm conditions. The present L6/L2-to-L3 estimate is a change of exponent in that established proof architecture. The extra original-gradient L-infinity hypothesis enables the present absorption and removes the relative-direction restriction. Neither Hodge decomposition nor interpolation is new.
- N812: `updates/FJ/synthesis/contact_global/REPORT.md`, Git blob 83e35f966b0d0ad582162acf59f41e171468cbd4. Its Schur-denominator and moving-background obstruction is not resolved here. Small gradient at one fixed mean does not control optimization over all means for an arbitrary field.
- N880: `updates/FZ-positive-memory-genesis-20261016/package/originals/sources/positive_core_RESEARCH_REPORT.md`, Git blob d89fdc30da6ea743aff7dd0fb0a554a8725f55f6. Its unchanged J_r already has arbitrary-amplitude quasiconvexity at every singular mean and an open cone of backgrounds. It explicitly leaves the conformal full-rank contact. The current increment is small-gradient control at full-rank degenerate means, not the singular-background result.

I also directly read Bruno–Pasqualotto 2608.06367v1, Theorems 1–2 and the heat/exact-form strategy: https://arxiv.org/html/2608.06367v1 . It proves global results for the bi-rotational quartic cone, while J_r has only the relevant one-sided rotational invariance. The separate orbit-cone exclusion is not needed for this positive local proof. A source-reported full J_1 quasiconvexity statement is likewise not needed and is not independently reconstructed here.

No comprehensive historical-priority clearance is asserted. The best earned description is a checked, concrete weak-quasiconvexity extension at the remaining degenerate contacts of this fixed anisotropic family, using closely related existing harmonic-analysis machinery. It leaves the unrestricted original J_r quasiconvexity question open.
