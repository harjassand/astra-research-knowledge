# A positive angular repair at the full quartic extreme endpoint

For all real2×2 matrices set

    T=|A|², q=det A, X=a²+c²−b²−d²,
    F*(A)=T²+12q²+4qX.                                  (1)

**Theorem.** The explicit homogeneous degree-three 1-form in EXACT_ALPHA.md
is smooth away from zero, C² at zero, and its exterior derivative Omega
satisfies the ORDINARY-HEAT completion inequality

    F*''(A)[B1,B1]+F*''(A)[B2,B2]+Omega_A(B1,B2)>=0       (2)

for every A and compatible Hessian pair

    B1=(h0,h1,h3,h4), B2=(h1,h2,h4,h5).

Consequently F* is quasiconvex. It is already proved positive off zero,
ROC-extreme in the full35-dimensional quartic polynomial cone, and non-PC
by the preserved ROOT28 packet. No ROC→QC theorem in general is claimed.

The proof below is an exact finite algebraic / univariate-Sturm proof,
not an inference from grid positivity or an inaccurate optimizer status.
The old no-origin-C²-form theorem remains intact: this Omega is C¹ at
zero; the polynomial/regular proof class and the angular one differ.

## 1. Actual primitive and regularity

The100 literal rational numerator monomials P_i(A) in
PRIMITIVE_CERTIFICATE.json define

    alpha_raw=sum_i P_i(A)/T dA_i, deg P_i=5.             (3)

An equivalent compact expression is printed in EXACT_ALPHA.md. It uses
the normalized Hopf coordinates

    (x,y,z)=(X,Y,Z)/T,
    Y=2(ab+cd), Z=2q,
    eta=(a dc−c da+b dd−d db)/T,

and has the form

    alpha=T²[f(x,z)eta+p(x,z)(y dx−x dy)
                           +r(x,z)(y dz−z dy)].           (4)

The exact six coefficients of cubic-odd f and four each of even-quadratic
p,r are fully specified there. The two primitives are related by

    alpha=alpha_raw−(1/4)d(i_E alpha_raw), E=A.            (5)

This is the Euler/radial gauge; it raises the displayed denominator from
T to T² but leaves Omega unchanged. The exact consumer checks the four
global polynomial identities obtained by clearing denominators in (5).
Root independently acquired the same compact gauge representation; it
is not a different coefficient proposal.

All coefficients of either primitive are homogeneous degree3 and smooth
on the compact sphere. Their derivatives of orders j<=2 are O(|A|^(3−j)),
so alpha(0)=0 gives a C² form on all R⁴. Omega=d alpha is C¹, with
degree2 coefficients and derivatives O(|A|). Exterior exactness and
Stokes at gradients attaining zero are therefore legitimate. Smooth
origin extension of higher order is not assumed or needed.

## 2. Literal closed density

Use Omega_ij=partial_i alpha_j−partial_j alpha_i. In the raw expression
(3), the denominator-cleared skew matrix is

    T² Omega_ij=T(partial_i P_j−partial_j P_i)
                       −2(A_i P_j−A_j P_i).              (6)

Let C(A) be the symmetric6×6 matrix of (2) and Ctilde(A)=T² C(A).
It is a homogeneous degree6 polynomial matrix with rational coefficients.
The producer used (6) to propose it. The independent receiver reconstructs
P, F*, all derivatives in (6), and the full matrix by elementary sparse
monomial operations without importing a producer, CAS, SDP or floating
library. It does not take the saved matrix as a premise.

If D is the positive common denominator of the P_i coefficients, the
receiver constructs the integer matrix 2D Ctilde. The factor2 exactly
pays symmetrization of the wedge quadratic form; it is not an omitted
normalization. All leading determinant identities are compared with
the corresponding factors multiplied by (2D)^k.

## 3. Symmetry and a compact global cover, with orientation signs

F* is invariant under left output rotations, A→C A C with
C=diag(1,−1), and A→A S with S=[[0,1],[1,0]]. The actual primitive obeys

    Phi*alpha=alpha for Phi(A)=Rtheta A,
    Phi*alpha=−alpha for Phi(A)=C A C or A S.             (7)

These are ANTI-pullback identities for the last two maps, not positive
invariance. The literal receiver checks the continuous rotation Lie
identity and both polynomial anti-pullback identities for P; T is
invariant. Taking d preserves (7) for Omega.

To spell out the domain-swap congruence, transform u(x,y) to u(y,x).
Then A'=A S and

    B1'=B2 S, B2'=B1 S,
    h'=(h2,h1,h0,h5,h4,h3)=P_h h.

Anti-pullback says Omega_AS(B1 S,B2 S)=−Omega_A(B1,B2).
The exchange of B1,B2 supplies the second minus, so

    Omega_AS(B2 S,B1 S)=Omega_A(B1,B2),
    P_h^T Ctilde(A S)P_h=Ctilde(A).                      (8)

The heat terms have the same congruence by invariance of F* and the
sum of the two derivative directions. Similarly A→C A C has
h'=(h0,−h1,h2,−h3,h4,−h5); its spatial reflection and the primitive's
anti-pullback again cancel. Output rotations give their ordinary
compatible-Hessian congruence. Thus positivity transports in (7).

For any A≠0, swap its columns if necessary so the first has at least
the norm of the second. Rotate output rows by an SO(2) matrix so the
first column becomes (a,0) with a>0, and divide A by a. The representative
is

    A(b,d)=[[1,b],[0,d]], b²+d²<=1.                     (9)

Homogeneity and the congruences above preserve positivity. This compact
disk therefore covers ALL nonzero gradients; it is not a sampled test
set. At zero, C(0)=0 by continuity. For the certificate it is enough to
prove positivity on (9).

## 4. All six principal minors, as exact polynomials

Let u=b²>=0. The six leading principal minors of Ctilde(1,b,0,d) factor
over Q[b,d] as recorded completely by sparse coefficients in
PRIMITIVE_CERTIFICATE.json. All outer rational constants are positive.
The factorizations have the following structure:

| k | Total degree | Factors, excluding positive constant | Coefficient sign checks |
|---|---:|---|---:|
| 1 | 6 | (u+7d²+6d+3)(u+d²+1)² | 4 |
| 2 | 12 | (u+d²+1)² Q2 | 7 |
| 3 | 18 | Q3a Q3b | 11 |
| 4 | 24 | Q4 | 13 |
| 5 | 30 | (u+d²+1)² Q5 | 16 |
| 6 | 36 | (u+d²+1)⁴ Q6 | 16 plus the discriminant |

The exact factor degrees Q2,Q3a,Q3b,Q4,Q5,Q6 are respectively
8,6,12,24,26,28 in (b,d). No factor or coefficient is rounded in the
governing data. This table merely summarizes those fully given identities.

`receive_literal.py` independently obtains all six determinants in ONE
fraction-free Bareiss elimination of the actual integer polynomial
matrix. Exact polynomial division and factor multiplication check the
identities coefficient by coefficient. Nonzero leading polynomial
pivots are checked; no numerical pivot or determinant is used.

For every factor expand

    Q(u,d)=sum_j p_j(d) u^j.

There are68 nonzero slices across all factors. All except the single
slice p1 of Q6 are proved STRICTLY positive for −1<d<1. In particular
the constant-u slice of every factor is strictly positive there.
For each of these67 univariate polynomials the exact receiver:

1. removes factors at the endpoints d=±1;
2. constructs the full integer primitive Sturm sequence;
3. checks equal endpoint sign variations (zero interior roots);
4. verifies the ORIGINAL polynomial is positive at d=0.

It follows that each is positive throughout the open interval, with
nonnegative endpoint limits. Zero slices, if any, are simply zero.

## 5. The exceptional determinant coefficient is repaired, not ignored

Write Q6=p0+p1u+p2u²+sum_(j>=3)p_j u^j. The p1 slice has two roots
in (−1,1), so coefficientwise positivity fails. It is not used.
Instead the receiver reconstructs EXACTLY

    D(d)=4p0(d)p2(d)−p1(d)².                            (10)

It has degree52 and endpoint factors (d−1)^4(d+1)^4. The remaining
degree44 polynomial has no roots in (−1,1) and positive sign there:
its Sturm endpoint variations are22 and22. The original D(0)>0.
The full degree / sign lists are retained in LITERAL_REPLAY.json.
Thus D(d)>0 for −1<d<1.

Since p2>0 on that interval,

    p0+p1u+p2u²
      =p2[u+p1/(2p2)]²+D/(4p2)>0                       (11)

for every real u. The remaining slices p_j u^j are nonnegative for
u>=0. Therefore Q6>0 on u>=0,−1<d<1. This fixes the only failed
coefficientwise sign condition without changing the primitive.

The Sturm implementation does not call symbolic root isolation. In
pseudo-division it multiplies each intermediate remainder by the
ABSOLUTE leading coefficient of the divisor and removes positive
contents only. Consequently every remainder is a positive multiple
of the true rational remainder, and the next Sturm polynomial is its
negative. All signs, endpoint divisions and variations are exact
integer arithmetic. The result is reproducible from the supplied
polynomials and elementary algorithm, not a root-count oracle.

## 6. Global completion and quasiconvexity

Sections4–5 make ALL six leading principal minors positive for u>=0
and −1<d<1. The actual matrix is symmetric, so Sylvester's criterion
gives Ctilde>0 there. At d=±1 take the continuous matrix limit: it is
positive semidefinite. This proves (2) on the compact canonical disk,
then at all gradients by Section3. T²>0 away from zero, so clearing
the denominator changes no sign. At zero the completion is its C¹
limit. The conformal acoustic zero orbits retain their legitimate
null vectors; no uniformly coercive seed margin is claimed.

For completeness the ordinary-heat bridge is the admitted
Bruno–Pasqualotto exact-form mechanism. For u=Mx+phi, phi compactly
supported smooth, evolve phi_t=e^(t Delta)phi. Integration by parts
gives the derivative of the relative quartic energy as minus the
integral of the uncorrected heat density. The pullback of d alpha has
zero integral by Stokes, so (2) makes that derivative nonpositive.
The relative energy tends to zero as t→infinity by heat decay.
Thus its value at0 is nonnegative, proving QC. Boundary terms vanish
using heat decay and the degree3 growth of the globally C² primitive;
no singularity at gradients attaining zero is excluded. Smooth
approximation extends the quartic inequality to W1,infinity_0 tests.

The same argument can be made on finite Fourier polynomials on a torus
and then periodized/approximated; neither a numerical PDE integration
nor a trajectory sampling law is an input.

## 7. Positive export and what is genuinely repaired

For every epsilon>0, the SAME alpha certifies

    F_epsilon=F*+epsilon T²,
    C_Fepsilon+Omega >=4epsilon |A|² |h|².               (12)

Indeed T² is convex and its heat density is at least
4|A|² sum|Bj|²>=4|A|²|h|². This pays actual global coercivity, not a
grid margin. For a homogeneous quartic perturbation G with coefficient
norm rho, ||G''(A)||op<=1680rho |A|². Consequently

    H=G+420rho T²

is convex. If rho<epsilon/840, then

    F_epsilon+G=F*+(epsilon−420rho)T²+H

has the SAME angular completion, with margin at least
2epsilon |A|²|h|². This is an explicit FULL35-dimensional positive
coefficient neighborhood for every epsilon>0, irrespective of whether
it lies inside the earlier negative-method neighborhood.

It is strongly QC with the quantitative lower bound

    integral [F_epsilon+G](M+Dphi)−[F_epsilon+G](M)
       >= (epsilon/8) integral (|M|²|Dphi|²+|Dphi|⁴).      (13)

The F* term is QC, H convex, and the remaining norm4 coefficient is
at least epsilon/2. The elementary norm4 Bregman inequality is

    |M+X|⁴−|M|⁴−4|M|²M:X
        >=(1/4)(|M|²|X|²+|X|⁴).

Writing X unit and M=sX+V, V perpendicular to X, the difference is
(23/4)s²+(7/4)|V|²+4s+3/4>=5/92. This proves (13).

The preserved ROOT28 negative theorem has its OWN unevaluated radius
delta0 for PC-quartic plus origin-C² heat decompositions. For every
sufficiently small epsilon and appropriately small ball, (12)–(13)
therefore provide positive ANGULAR proofs inside that excluded regular
class. No explicit named epsilon is asserted inside the old negative
ball merely because an explicit positive ball is now available.

There is also an immediate infinite-family resolution using the fully
admitted polyconvex determinant term. For b=|beta|<=1,r>=4,

    F_(beta,r)=b F*_(sign beta)+(1−b)T²
                          +[4(r−1)−12b]q².              (14)

All coefficients are nonnegative; F* with the opposite beta sign is
an orthogonal column-reflection transport. Thus this WHOLE aligned
region is QC. In particular the old sol9 family r4,
beta_m=(m²−1)/(m²+1), m>=197, previously strictROC/non-PC with QC
unknown, is now strongly QC with modulus2/[3(m²+1)] multiplying
integral|Dphi|⁴. This does not assert heat dissipation for q².

## 8. Scope and ordinary comparison

The original BP AppendixA already supplies complete QC for its
left-and-right rotationally invariant quartic cone by polynomial heat
plus PC decomposition. ROOT25 already supplies a rational P5/T heat
example beyond PC. Both are admitted at full scope. This construction
uses the same legitimate angular regularity class but repairs the
particular FULL35 extreme endpoint at which every origin-regular
mixed constant-flow decomposition fails. It does not present a generic
rational hierarchy, a numerical failure or the Shield transform as
the new operation.

The full general ROC quartic cone, the aligned region R(beta)<=r<4
outside previously proved parts, and arbitrary nonlinear/nonpolynomial
decompositions are not classified here. Historical priority remains
UNKNOWN. No physical acquisition, computational speed advantage or
Morrey resolution follows from the positive seed and its exports.
