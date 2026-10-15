# Independent Heat18 monotonicity proof check

## Finding

**PASS, for the stated G and the certified constant heat operator.** An independently authored standard-library Python replay has checked the entire rational certificate, without importing or executing any source author's code. Combined with the analytic argument below, it establishes energy decrease for every affine background and every rectangular periodic cell, including affine-quasiperiodic displacements. No numerical search or AI audit status is a premise.

The certified operator is L = (4897/5000)∂xx + (5103/5000)∂yy. The result also holds for a common positive scalar multiple of this operator. This certificate does **not** by itself establish monotonicity for arbitrary independently chosen diffusion coefficients, or for a heat flow with nonperiodic boundary conditions on a bounded domain.

Inputs: [existing Heat18 proof](../../../../updates/FT-direction-transport-20261015/synthesis/nonlinear_qc/G_QUASICONVEXITY_PROOF.md) and its local JSON certificate. The proof reports repository pin b7cada92d2eb304578be5ed974f1e44b10a89928; this review verifies the supplied local proof and certificate, not provenance against a remote repository. `certificate_as_received.json` preserves the original bytes. `replay.py` is the new checker and `receipt.json` its output. No source author scripts were executed.

## 1. G and its derivatives

Write A = [[a,b],[c,d]], u=a²+c², v=b²+d², j=ad−bc, s=u+v−2j. Then

G(A)=3s²+(35/24)u²+j²−(5/2)ju.

For any increment H, use δ for directional differentiation at A. Direct differentiation gives

DG(A)[H]=6s δs+(35/12)u δu+2j δj−(5/2)(u δj+j δu),

D²G(A)[H,H]=6(δs)²+6s δ²s+(35/12)[(δu)²+u δ²u]+2(δj)²+2j δ²j−(5/2)[u δ²j+2δu δj+j δ²u].

Here δ²u=2(H11²+H21²), δ²v=2(H12²+H22²), δ²j=2det H, and δ²s=δ²u+δ²v−2δ²j. These formulas have no omitted factors of two. The replay independently constructs G as a sparse polynomial with rational coefficients and differentiates its coefficients twice; it does not parse a supplied Hessian formula.

## 2. Finite exact checks and sum of positive squares

For z=(z0,…,z5), set B1=(z0,z1,z3,z4) and B2=(z1,z2,z4,z5) in matrix-entry order (a,b,c,d). Set Z=(a z0,…,a z5,b z0,…,d z5). Independently reconstructed polynomial arithmetic proves exactly

ZᵀQZ = d1 D²G(A)[B1,B1] + d2 D²G(A)[B2,B2] + ω_A(B1,B2).

All 10 quadratic A monomials times all 21 quadratic z monomials were compared, giving 210 exact zero residual coefficients. The replay also verifies all 576 entries of Q=C S Cᵀ, symmetry of S, and rank(C)=18 by rational elimination.

It derives, rather than trusts, the factorization S=Ldiag(p0,…,p17)Lᵀ, with unit lower triangular L, and reconstructs all 324 entries. Every rational pivot p_i is strictly positive. Exact pivot values are in the receipt and agree with the supplied pivot list. Thus with Y=LᵀCᵀZ,

ZᵀQZ = Σ(i=0,…,17) p_i Y_i² ≥ 0.

This is a rational positive-weight sum of squares; the weights need not be rational squares. No approximate eigenvalue or floating tolerance is involved. Q has rank 18.

The replay checks all four coordinate components of dω=0. With α_k=(1/4)Σ_i A_i ω_ik(A), it checks all six coefficients of dα=ω directly. This independently verifies the global polynomial primitive, not merely an abstract claim of exactness.

## 3. Correction integral and boundary requirements

Let R=[0,P]×[0,Q], P,Q>0. Let w(x,y)=B(x,y)ᵀ+ψ(x,y), where ψ is smooth and periodic with these periods; B is any real 2×2 matrix. Put F=Dw. Then F and all its derivatives are periodic, even though w itself need not be. Compatibility gives ∂xF=B1 and ∂yF=B2 in the pattern above.

The pullback one-form is

F*α = α_F(∂xF) dx + α_F(∂yF) dy.

Both coefficients are periodic. Therefore

ω_F(∂xF,∂yF) = ∂x[α_F(∂yF)] − ∂y[α_F(∂xF)],

and its integral over R vanishes by cancellation on opposite sides. There are no corner terms. No condition B=0 is needed.

More generally, a smooth displacement satisfying w(x+P,y)=w(x,y)+c1 and w(x,y+Q)=w(x,y)+c2, for constant vectors c1,c2, has precisely this form with B's columns c1/P and c2/Q. Hence every compatible affine-quasiperiodic loop is covered. If only values on opposite edges are identified but the first derivatives do not match, the smooth torus argument is not automatic. For Sobolev loops the correct hypothesis is periodic ψ∈W¹,⁴ on the torus; smooth periodic approximation then supplies the extension.

The same proof works on any flat lattice torus in the original Euclidean coordinates, since a constant differential operator and all pullbacks descend to it. Changing coordinates is permissible only with the corresponding transformation of the diffusion and gradient; holding a unit-coordinate diffusion fixed after anisotropic coordinate rescaling changes the operator and is not justified by this certificate alone.

On R², the correction integral likewise vanishes for F=B+Dψ with ψ Schwartz: the coefficients of F*α are polynomials in the bounded F times a positive-order derivative of F, hence decay rapidly. On a bounded nonperiodic domain, arbitrary boundary conditions need not annul the correction. In particular, this proof does not assert energy decrease along a bounded-domain Dirichlet heat flow merely from ψ=0 on its boundary.

## 4. Exact energy dissipation

For ψ_t solving ∂tψ_t=Lψ_t on the rectangle torus, F_t=B+Dψ_t solves ∂tF_t=LF_t. For every t>0, smoothness and periodic integration by parts give

E(t)=∫_R G(F_t),

E′(t)=∫_R DG(F_t):LF_t
      =−∫_R [d1 D²G(F_t)[∂xF_t,∂xF_t]+d2 D²G(F_t)[∂yF_t,∂yF_t]]
      =−∫_R Z_tᵀQZ_t ≤ 0.

There is no extra factor 2: the Hessian is the second directional derivative, and one integration by parts generates exactly one Hessian contraction. The correction contributes zero integral, as proved above. Averages instead of integrals simply divide this identity by PQ.

Fourier eigenvalues for the nonconstant modes are −4π²[d1 m²/P²+d2 n²/Q²], strictly negative for (m,n)≠(0,0). Consequently Dψ_t→0 smoothly as t→∞ and E(t)→PQ G(B). Thus ∫_R G(B+Dψ)≥PQ G(B). Rectangular aspect ratio changes the decay rate but not the conclusion, the coefficients of G, or the certificate.

For ψ∈W¹,⁴, periodic heat is strongly continuous on its gradient in L⁴. Quartic polynomial growth and Hölder give convergence of E(t) at t=0; smoothing proves monotonicity for positive times, and continuity extends it to time zero. The dissipation identity is asserted classically for t>0; its integrated version follows by time integration. This covers all affine backgrounds without any bound on |B|.

## 5. Whole-space and bounded-domain quasiconvexity check

For compactly supported smooth ψ on R² use the relative energy ∫[G(B+Dψ_t)−G(B)−DG(B):Dψ_t]. It is finite, obeys the same derivative formula, and tends to zero as t→∞. Indeed the remainder is bounded by C(|B|²|Dψ_t|²+|B||Dψ_t|³+|Dψ_t|⁴). In dimension two the Gaussian Young estimate is ||Dψ_t||_p≤C t^{−(1−1/p)}||Dψ||_1 for p=2,3,4. Each integrated remainder term therefore tends to zero. Strong heat continuity gives the initial energy and ∫Dψ=0 removes the linear term. W¹,⁴_0 approximation then proves the stated bounded-domain Jensen inequality. This last argument proves quasiconvexity; it does not impose the earlier bounded-domain heat-flow claim.

## 6. Hash discrepancy, resolved without changing the input

The supplied local file's SHA-256 is

4c19497572a7dd79e4dc64f9726a1e4bfd15e518fd1424129fdf2022ce98a104.

It has two final newline bytes. Removing exactly one extra terminal newline gives

4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000,

which is exactly the hash quoted by the proof. Both supplied local copies have the same original bytes and parse to the same object. The receipt transparently reports the original-byte mismatch and the matching single-newline digest. The algebra check uses the original file as received and passes independently of this bookkeeping issue.

## Reproduction and limits

Run `python replay.py` from any directory. It uses only Python's standard library, reads the certificate, and writes `receipt.json` next to itself. All arithmetic affecting acceptance is exact. The analytic argument above is a written mathematical check, not a formal proof-assistant verification. No claim of historical novelty, external peer review, arbitrary anisotropy, or validity of a separate storage construction is made. The specific load-bearing global Heat18 monotonicity statement on periodic-gradient fields is established by the verified certificate and the explicit integration argument.


Integration evidence status: `source_derived_unreviewed`. Audit verdicts and primary-source reading statements above are attributed to the supplied research, not new external review. This intake replays only its three own exact verification scripts. The conclusion applies to the particular certified Heat18 quartic G, not the full quartic cone, PR97’s newly exposed ROC ray, or general Morrey questions.
