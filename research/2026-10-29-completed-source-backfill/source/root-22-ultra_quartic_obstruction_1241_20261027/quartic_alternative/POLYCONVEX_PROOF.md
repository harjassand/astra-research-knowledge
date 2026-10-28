# An exact global determinant-support certificate

The specific principal candidate is polyconvex, with a strict quantitative
quasiconvexity estimate. This is an application of established SOS
polyconvexity to an input for which a different sufficient certificate class
was exactly excluded. It does not prove rank-one convexity implies
quasiconvexity for the full nine-coefficient cone.

## 1. Exact statement and certificate

For A=[[a,b],[c,d]], set

    u=a²+c², v=b²+d², w=ab+cd, q=ad−bc,
    F(A)=u²+v²+3w²+16q²+4q(u−v).

Define the explicit homogeneous quadratic scalar

    kappa(A) = (28297/5000)(u−v)+(57213/2000)q.              (1)

Use row-major coordinates A=(A0,...,A3), X=(X0,...,X3), and the 26-vector

    Z(A,X) = (A_i X_j : i=0,...,3 then j=0,...,3;
              X_i X_j : 0<=i<=j<=3 in lexicographic order).

The supplied rational symmetric 26-by-26 matrix R satisfies

    F(A+X)−F(A)−DF(A):X−kappa(A)det X = Z(A,X)^T R Z(A,X), (2)
    R−(1/200)I is positive definite.                       (3)

Every entry of R and the 26 positive LDL pivots for its shifted matrix are
in `EXACT_POLYCONVEX_SUPPORT.json`. Equation(2) has215 possible monomials:
100 of bidegree(A²,X²),80 of bidegree(A,X³), and35 of degree X⁴.
All 215 coefficient equations were imposed exactly. `verify_support.py`
independently reconstructs F in its displayed original form, differentiates
it using integer exponent dictionaries, reconstructs the entire Gram
polynomial, and computes/reconstructs the rational LDL factorization.
It imports no acquisition generator, symbolic algebra, NumPy or optimizer.

The standalone executed checker reports exact zero polynomial residual and
26 strictly positive pivots. Their largest numerator/denominator has 263bits.
These finite checks prove the explicit polynomial identity and positivity;
the analytic consequences are proved next.

## 2. Global polyconvexity

For each fixed A, put

    T(A)=DF(A)−kappa(A)cof A,
    ell_A(B,t)=F(A)+T(A):(B−A)+kappa(A)(t−det A).

The determinant expansion det(A+X)=det A+cof A:X+det X and(2),(3) give

    ell_A(B,det B)<=F(B) for all A,B,
    ell_B(B,det B)=F(B).

Thus G(B,t)=sup_A ell_A(B,t) is a convex lift with
G(B,det B)=F(B). G is finite everywhere, not merely on the determinant
graph. Indeed choose Y with det Y=t−det B. Then

    (B,t)=[(B+Y,det(B+Y))+(B−Y,det(B−Y))]/2.

Each affine ell_A is bounded above there by
[F(B+Y)+F(B−Y)]/2, uniformly in A. A fixed ell_A gives a finite lower
bound. Hence G is a real-valued convex function on all R^4×R.
This proves polyconvexity without requiring a convex polynomial lift.

The distinction matters: the primary SOS-polyconvexity paper proves that
some degree-four polyconvex energies have no convex polynomial lift.
No search for a polynomial lift or for F−gamma(det A)² convex is substituted
for the support construction above.

### 2.1 This F has no convex polynomial lift of any degree

A general homogeneous-quartic reduction makes that distinction exact.
Suppose G(A,t) is any real convex polynomial with G(A,det A)=H(A), where H
is homogeneous quartic. Give A weight 1 and t weight 2. Each weighted
component other than degree 4 vanishes on the determinant graph. Components
of weights 0 and 1 vanish identically. The weight 2 component is c(t−det A).
Its A-A Hessian at the origin is −c D²det, an indefinite matrix unless c=0.
Convexity of G therefore forces this component to vanish. The weight 3
component is (t−det A)ell(A), with ell linear; the A-A Hessian block of G
at the origin is now zero, so PSD of the full Hessian forces its A-t block
ell to vanish as well.

Thus all components below weighted degree 4 vanish. The convex polynomials
epsilon^(-4)G(epsilon A,epsilon²t) converge pointwise as epsilon decreases
to zero to their weighted-degree 4 part G4, which remains convex. Its form is

    G4(A,t)=H(A)+(t−det A)[Q2(A)+c t],

where Q2 is homogeneous quadratic. The A-A Hessian contains the term
t D²(Q2−c det). For every fixed A it is PSD for arbitrarily positive and
negative t, forcing Q2=c det. Therefore

    G4(A,t)=H(A)−c(det A)²+c t², c>=0,

and H−c(det A)² is convex. Conversely such a convex subtraction obviously
supplies a convex polynomial lift. Hence, for every homogeneous planar
quartic, existence of a convex polynomial lift of any degree is equivalent
to existence of this single nonnegative determinant-square convex subtraction.
This is the weighted-scaling/Hessian mechanism used in the primary paper's
Proposition 2.4, here stated and proved for general homogeneous quartics.

For the present F, at A=I the Hessian restricted to diagonal directions of
F−c q² has determinant

    (68−2c)(20−2c)−(64−4c)²
      =−12[(c−14)²+32]<0 for every real c.                 (2a)

Thus this F, despite its strict global polynomial SOS support, admits no
convex polynomial lift of any degree. Equation(2a) is independently checked
by the standalone verifier. This is a representation separation, not a
failure of polyconvexity or quasiconvexity.

## 3. Quantitative compatible-gradient Jensen inequality

The feature convention gives

    |Z(A,X)|²=|A|²|X|²+sum_(i<=j) X_i² X_j²
               >= |A|²|X|²+(1/2)|X|⁴.

Consequently, for every bounded Lipschitz domain Omega in R², every constant
A and every phi in W^(1,4)_0(Omega;R²),

    integral_Omega [F(A+Dphi)−F(A)]
      >= (|A|²/200) integral_Omega |Dphi|²
          +(1/400) integral_Omega |Dphi|⁴.                  (4)

Proof: integrate(2),(3). The first gradient mean is zero, so the DF(A)
term integrates to zero. The determinant is a null Lagrangian and
integral det Dphi=0, so the scalar kappa(A) term also integrates to zero.
The feature norm estimate proves(4). First prove these identities for
smooth compactly supported phi; strong W^(1,4) approximation and quartic
growth pass both energy and determinant identities to the stated class.
The same proof applies to periodic W^(1,4) potentials with normalized
averages. No heat flow, derivative-order bound, Fourier bandwidth, small
amplitude or sign restriction on the determinant is imposed.

In particular this proof is independent of the candidate's previously
acquired rank-one-convexity certificate. Quasiconvexity and the displayed
uniform gap follow directly from a globally verified support inequality.

## 4. An explicit whole-profile storage

For fixed B and any smooth periodic U:T->R², define

    P_B(U)=DF_1(B).E U+(kappa(B)/2) E det(U,U').             (5)

For every smooth periodic velocity V, differentiation and integration by
parts give

    DP_B(U)[V]=DF_1(B).E V+kappa(B)E det(V,U').

Apply(2) to X=(V|U') and average. The DF_2(B).U' term has zero mean.
Thus DP_B(U)[V] <= E[F(B+(V|U'))−F(B)]. Integrating along any compatible
smooth strip gives storage domination. Moving transverse means are retained
through the affine term in(5). This is the ordinary determinant-area
storage permitted by N830's finite-jet characterization once polyconvex
support has actually been acquired. It contradicts neither that rigidity
theorem nor the no-universal-coefficient-linear-selector theorem.

## 5. A complete finite interface for polynomial SOS support

The following reduction concerns SOS polyconvexity, not all polyconvexity.
It is useful for the entire nine-coefficient cone, with four rather than
two multiplier coefficients. Its ingredients are homogeneity, symmetry
averaging and the established SOS Gram characterization.

### 5.1 No hidden polynomial-degree escape

Let H be any homogeneous quartic on R^(2x2). If a polynomial map of minors
provides a global first-order support, differentiating its inequality at
the touching point shows that it has exactly the determinant-support form

    H(A+X)−H(A)−DH(A):X−k(A)det X>=0.                       (6)

Here k is polynomial if the original minor-support map was polynomial.
Decompose k into homogeneous parts k_d. Substitute(tA,tX). The quartic
Bregman part scales as t⁴, while each remaining term is
−t^(d+2) k_d(A)det X. If the largest nonzero degree d exceeds2, choose A
where k_d(A)!=0 and choose the sign of det X to make this leading term
negative as t tends to infinity. This contradicts(6). If the smallest
nonzero degree is below2, the same argument as t decreases to zero gives
a contradiction. Thus every polynomial selector is homogeneous quadratic.
The zero selector is included.

Suppose now the residual is SOS. Since it is homogeneous of degree 4,
each squared polynomial can be chosen homogeneous quadratic: highest- and
lowest-degree squared parts cannot cancel in a sum of real squares.
Moreover the residual vanishes for X=0 at every A, so every individual
quadratic square vanishes on X=0. Therefore it contains no A_i A_j terms.
The exact26 features in(2) span every possible square. Conversely a PSD
Gram on those features is such an SOS. Consequently no larger polynomial
degree in the selector or the squares enlarges this homogeneous-quartic
SOS-support existence class.

### 5.2 Left-output rotations and the candidate's additional symmetries

If H is left-SO(2)-invariant, average any support/SOS identity over these
rotations acting simultaneously on A and X. Congruence preserves Gram
positivity. The averaged homogeneous quadratic selector lies in

    span(u,v,w,q).

For the special class invariant also under AS, S=[[0,1],[1,0]], and under
JAD with J=D=diag(1,−1), the selector may additionally be averaged with
the determinant's transformation sign. It must be antisymmetric under AS
and invariant under JAD. These conditions leave exactly

    k(A)=alpha(u−v)+delta q.

This includes the present F. It is not a restriction to guessed forms:
averaging any candidate SOS support yields one in this two-parameter space.
No orthogonality of the unscaled quadratic feature basis is needed; each
transformed Gram is a positive congruence and the finite/Haar average is PSD.

### 5.3 Implemented scope and costs

`poly_support.build(coefficients, multiplier='auto')` compiles any rational
nine-vector in the order

    (u²,v²,uv,w²,uw,vw,qu,qv,qw).

It uses26 features,215 coefficient equations and either four left-SO(2)
quadratic multiplier coefficients or the two coefficients when the above
extra symmetries are present. Thus there are355 or353 real unknowns:
351 symmetric Gram entries plus the multiplier coefficients. This is an
exact fixed-dimensional representation of this SOS-polyconvex support
class. The numerical arrays used for acquisition are floating-point;
the exact polynomial objects and final standalone verification retain the
correctness boundary. The default compiler and acquisition were tested on
the present candidate. No universal numerical convergence, rational
boundary certificate, polynomial bit bound or optimum-acquisition guarantee
is claimed.

The existence of an SOS support implies polyconvexity. The converse for
general2-by2 degree-four polynomials is explicitly left open in the primary
paper cited below. Therefore an infeasible SOS support does not establish
non-polyconvexity, and neither condition is a characterization of the
quasiconvex cone. Known N794/N797 quasiconvex non-polyconvex energies already
show why this sufficient class cannot cover the entire acoustic cone.

## 6. Prior machinery, source scope and retained failure

The ordinary support/SOS method is from Fantuzzi, Henrion, Kružík, Murali &
Weis, *Polyconvexity with Moments and Sums of Squares*, arXiv2604.11124v1:
Proposition 2.3, Definition 2.5 and Theorem 2.2. Remark 2.1 explicitly retains
the2-by2 quartic polyconvex-versus-SOS gap. It is a primary comparator,
not a newly invented method. Equation(2) is the actual independently
acquired certificate for the present input. The finite homogeneity/symmetry
interface above is derived here; historical novelty is UNKNOWN.

The cleared helper audit exactly excludes a constant-SPD spatial
heat/closed-quadratic/bilinear-SOS certificate for this F, even after any
nonnegative determinant-square subtraction. That is a failure of a
sufficient method, and is entirely compatible with the direct proof here.
The root's broader output-coupled-flow investigation is separate and is not
a premise of any result in this file.

A proposed extrapolation to all normalized trace-free orientation terms
was screened once with the strongest ordinary comparator. For

    H_(r,t,L)=u²+v²+2r w²+t q²+Lq(u−v),

at r=3/2,L=4, full acoustic8 and support26 SDPs gave numerical minimum t
values11.2311116 and11.4395467 respectively. This is not an exact boundary,
non-polyconvexity witness or QC counterexample. It is a reason not to
extrapolate the present certificate into an unproved universal sector
theorem. The raw diagnostic and costs are retained.

The global nine-coefficient rank-one-convex-to-quasiconvex implication
remains unresolved here. The correct use of this construction is to remove
an acquired polyconvex case from that unresolved target, and to retain a
complete ordinary-support screen for subsequent inputs.
