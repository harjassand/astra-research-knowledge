# Independent analytic reconstruction of the angular-form bridge

This derives the complete implication consumed by the review. It does not use a
nearby polyconvex energy, numerical positivity, or a new compatible-gradient fixture.
The literal source is F=T²+(252/25)q²+(99/25)qx in row-major A=(a,b,c,d), with
T=|A|²,q=ad-bc,x=a²+c²-b²-d². The independently consumed certificate is bound in
EXACT_CONSUMER.json; no producer Python module was imported.

## 1. Compatibility, exterior derivative, and exact positivity

For A=Dv, the two derivatives are B1=(h0,h1,h3,h4) and B2=(h1,h2,h4,h5).
Six real Hessian entries are arbitrary, and their repeated positions enforce the
two spatial mixed-partial identities. Treating B1,B2 as eight independent entries
would be the wrong certificate problem; restricting to six loses no actual jet.

For P=sum_s P_s dA_s, define alpha=P/T on A!=0. Exterior differentiation gives

    T² d(alpha)=T dP-dT wedge P.

For r<s, its coefficient is
T(partial_r P_s-partial_s P_r)-2A_r P_s+2A_s P_r, multiplying
(B1_r B2_s-B1_s B2_r). This includes each exterior component once, without a
hidden factor2. The consumer constructs precisely this expression by independent
symbolic differentiation and compares its whole polynomial coefficient dictionary
to z^T Q z. All1281 nonzero coefficients match exactly.

For supplied integer L and denominator10^10, the consumer separately verifies
Q=(1/1000)I+LL^T+E with symmetric E and row bound
123436226613/10^19. Since |x^T E x|<=max_i sum_j|Eij| |x|², Q>I/2000 follows.
No floating Cholesky or eigenvalue is consumed as a premise.

The120 monomials z are exactly all20 degree3 A monomials times each h entry.
The degree3 multinomial coefficients are at most6, giving

    |z|² >= T³ |h|²/6,
    D_nu F+dalpha(B1,B2) >= T |h|²/12000.          (A1)

## 2. The origin is paid

Each P_s/T is homogeneous of degree3 and smooth on the sphere. Derivatives of
orders0,1,2 are respectively O(|A|³),O(|A|²),O(|A|). Setting alpha(0)=0 therefore
gives derivative0 at zero, then derivative0 for its first derivative at zero, and
continuous second derivatives there. This is genuinely C². It is not claimed C³.
Thus dalpha is C¹ globally, vanishes at0, and(A1) extends continuously at0.

For periodic A(x), A*alpha is a periodic C¹ one-form and
d(A*alpha)=A*(dalpha). Its integral over the torus vanishes by Stokes. This holds
even when A crosses0. It is a pullback exact-form identity, not the generally
false assertion that a variable scalar multiple of a null Lagrangian integrates0.

## 3. Skew/output diffusion and signs

Let J=[[0,-1],[1,0]] act on the output, and evolve the periodic part by

    phi_t=Delta phi+2nu J phi_12.

Every Fourier coefficient has propagator
exp(-|xi|²t) exp(-2nu xi1 xi2 J t). The second factor is a real orthogonal output
rotation. Hence this is a globally defined smoothing real linear flow with heat
decay; it preserves mean and periodicity and sends every nonconstant derivative
to0 smoothly. This supplies its own parabolic/long-time argument. A positivity-
preserving scalar heat kernel or a symmetric scalar spatial diffusion was not
silently imported. Real Fourier symmetry is preserved since the symbol is real
and even in xi. No physical implementation is claimed.

Let A_t=A0+Dphi_t and E(t)=integral[F(A_t)-F(A0)]. The scalar Laplacian contributes
-integral sum_j F''[B_j,B_j]. For the mixed term, integrate one copy of nu J A_12
in x1 and the other in x2. They contribute

    -nu integral{F''[B1,J B2]+F''[B2,J B1]}.

The signs are those of E'; the same bracket has positive sign in -E'. Thus
E'=-integral D_nu F. Combining with Stokes and(A1) proves -E'>=0. Integration
from0 to infinity and the explicitly paid heat limit prove periodic Jensen.

## 4. The quantitative margin

For G(A)=|A|⁴, G''=4T I+8 A A^T, so ||G''||<=12T. Therefore

    |D_nu G|<=12(1+|nu|)T(|B1|²+|B2|²)
             <=24(1+|nu|)T|h|².

With kappa1/300000 and the actual rational nu102669769/10^12, the exact remaining
coefficient in(A1) is124691990693/37500000000000000>0. The same alpha and flow
therefore prove quasiconvexity of F-kappa G. Independently,

    G(A+X)-G(A)-4|A|² A:X-|X|⁴/3
      =2(|A|²|X|²-(A:X)²)+6(A:X+|X|²/3)² >=0.

The mean of Dphi is0, so the linear term integrates0. This proves the claimed
1/900000 strong quartic Jensen constant for F. Direct integration of E and G also
gives the slightly stronger constant31250000/27002772083763, but the weaker
declared bound suffices and is the one accepted.

## 5. All bounded Lipschitz domains and full perturbation class

First extend a compactly supported smooth phi in Omega by0 into a periodic box.
Only its INITIAL energy needs support in Omega; the smoothing flow is allowed to
spread through the box. The integrand outside Omega is initially0 and the final
gradient is A0, so the periodic inequality yields the original-domain inequality.
This avoids any unjustified boundary preservation of the flow. Finally use the
defining C_c^infinity density in W0^(1,4). Quartic growth and Holder give continuity
of the energy under strong W1,4 convergence. The result covers arbitrary amplitude,
all backgrounds A0 (including singular/zero), and all determinant signs. No Fourier
cutoff, rank restriction or finite-dimensional gradient ansatz is retained.

## 6. Original non-polyconvexity is not confused with a control

The source strict-ROC theorem is the already independently accepted sol9 Hopf
theorem, whole-read again at its stated scope. The actual three positive rational
atoms at A=diag(36,35) and their weights were independently re-evaluated here.
They preserve the mean matrix and mean determinant, but their energy deficit is
-13534664264487807/296890944920312500. This contradicts Jensen for EVERY convex
minor lift. It is a genuine non-PC source, not failure of a chosen SOS ansatz.
Those atoms are not asserted to be a compatible gradient law. The new QC theorem
therefore has no conflict with that witness and does not refute Morrey2x2.
