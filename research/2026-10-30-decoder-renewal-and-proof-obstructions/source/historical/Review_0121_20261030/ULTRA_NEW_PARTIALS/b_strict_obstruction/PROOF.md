# A strict open obstruction to polynomial/regular heat decompositions

The degenerate endpoint obstruction persists for strictly rank-one-convex
quartics, even when a finite decomposition uses arbitrarily many different
constant mean-converging flows. The proof does not assert global closure
or convexity of the union of those flow classes. Instead it constructs a
closed outer class, proves that the endpoint is outside it, and uses the
pointed ROC cone to control all finite sums.

The conclusion is qualitative in its neighborhood radius. No numerical
epsilon0 or separating functional has been acquired. The full angular /
rational exact-form class remains OPEN and is not excluded.

## 1. Objects and precise conclusion

Let V be the real35-dimensional vector space of homogeneous quartic
polynomials on real2×2 matrices, with ordinary monomial coefficient norm
||F||∞. Write K for its ROC cone and P for its polyconvex cone; arbitrary
convex minor representatives are allowed for P. All integrand summands
are in V. Nonpolynomial integrand cancellations are not admitted here.

For constant real2×2 output matrices L11,L12,L22, put

    L(xi)=L11 xi1²+2L12 xi1xi2+L22 xi2².

Call L mean-converging if its eigenvalues have positive real parts for
each nonzero integer xi. This admits the actual constant flows used in
the preceding packet without assuming an unstated uniform PDE theorem.
For compatible Hessian coordinates h=(h0,...,h5), set

    B1=(h0,h1,h3,h4), B2=(h1,h2,h4,h5),
    D_F,L(A)[h]=sum_(j,l=1)² F''(A)[Bj,Ljl Bl],
    L21=L12.

L acts on output rows in the last display. Write C_F,L(A) for the
symmetric6×6 matrix representing this quadratic form in h, and W(Omega)
for the one representing Omega(B1,B2).

The origin-regular heat class H consists of F for which some
mean-converging L and closed 2-form Omega, whose coefficients are C²
near zero, satisfy

    C_F,L(A)+W(Omega(A)) >= 0 for every A.                 (1)

The form need not be homogeneous or polynomial initially. The Taylor
lemma in the frozen sibling POLYNOMIAL_BARRIER.md §1 applies verbatim
to this D_F,L: pure wedge positivity forces the constant and linear
Taylor terms to vanish, and scaling leaves a closed quadratic-coefficient
form satisfying (1). Conversely every closed quadratic-coefficient form
has the cubic Euler primitive (1/4)i_A Omega. Thus H is unchanged by
requiring Omega to have homogeneous quadratic coefficients. In particular
H includes every polynomial-primitive certificate, irrespective of degree.

Let

    S_actual=P+conic_hull(H),

where conic_hull means arbitrary FINITE nonnegative sums; the flows of
different heat summands may differ. The theorem is:

**There exists delta>0 such that the coefficient ball of radius delta
about**

    F*(A)=T²+12q²+4qx,
    T=|A|², q=ad−bc, x=a²+c²−b²−d²,                     (2)

**does not intersect S_actual. Consequently, for every sufficiently
small epsilon>0, F*+epsilon T² is strictly ROC and is outside this
combined class. A full35-dimensional OPEN set of strictly ROC quartics
is excluded.**

This is not non-QC, actual heat-monotonicity failure by every possible
argument, or incompleteness of the angular class with Omega merely C¹
at the origin. Those stronger assertions are not made.

## 2. A literal positive base for the ROC cone

K is closed: its defining acoustic inequalities are linear continuous
conditions on the coefficients. It is pointed. Indeed F and −F in K
make F rank-one affine. Coordinate rank-one directions force F to be
multiaffine, so a homogeneous quartic is a multiple of abcd. The
rank-one direction E11+E12 then forces that multiple to vanish.

There is an explicit strict positive functional, rather than an unpaid
compact-base assumption. Let

    E={e1,e2,e1+e2},
    Aset={e_i:1<=i<=4} union {e_i+e_j:1<=i<j<=4},
    ell(F)=sum_(A in Aset, eta,xi in E)
              F''(A)[eta⊗xi,eta⊗xi].                    (3)

All90 terms are nonnegative on K. If ell(F)=0, interpolation of the
quadratic dependence first in eta, then xi, then A shows that the whole
acoustic polynomial is zero; pointedness above gives F=0.

`acquire_coercivity.py` also acquires a quantitative bound by exact
Fraction elimination: the90×35 evaluation matrix has rank35, and a
selected35×35 inverse has maximum row l1 norm6. Since each selected
evaluation lies in [0,ell(F)] for F in K,

    ||F||∞ <= 6 ell(F),       F in K.                    (4)

The complete matrix, independent rows, inverse and coefficient functional
are in COERCIVITY.json. This is a universal coefficient calculation,
not a scientific source case or a sampled test of ROC.

## 3. Polynomial witness boundedness, with explicit constants

Normalize L by

    sum_(ij=11,12,22) ||Lij||_F²=1.                     (5)

Positive scaling of L and Omega preserves (1); every nonzero admissible
flow permits this normalization. In particular each ||Lij||op<=1.

If M=||F||∞, each Hessian entry is bounded by420 M |A|² (35monomials,
second derivative coefficient at most12). Hence

    ||F''(A)||op <=1680 M |A|²,
    ||C_F,L(A)||op <=6720 M |A|².                       (6)

The latter follows from (|B1|+|B2|)²<=2sum|Bj|²<=4|h|².

Use the six rank-one compatible h with eta=e1,e2 and xi=e1,e2,e1+e2.
Their frame matrix is diag(S,S), where

    S=[[2,1,1],[1,1,1],[1,1,2]], Tr diag(S,S)=10.

S−I/4 is positive definite: its successive Sylvester determinants are
7/4,5/16,3/64. Every pure wedge has zero quadratic value on these
six vectors, so Tr[diag(S,S) W]=0. If W>=−k I, then P0=W+k I>=0 and

    Tr[diag(S,S) P0]=10k,
    ||P0||op<=Tr P0<=40k,
    ||W||op<=39k.                                      (7)

The negative eigenvalues of W are at least −k; its positive ones are
at most40k−k. This justifies the last constant without adding two norms.

For a feasible completion take k=6720 M |A|² in (7). Each of the six
Omega entries is twice a UNIQUE off-diagonal entry of W, up to sign:
the distinguishing monomials are h0h2,h0h4,h0h5,−h2h3,h1h5,h3h5.
Thus

    |Omega_ij(A)|<=78*6720 M |A|².

Evaluations at e_i and e_i+e_j determine all quadratic coefficients.
Each mixed coefficient is a difference of three such values, giving

    ||Omega_coeff||∞ <=4*78*6720 M
                      =2096640 M <2^21 M.              (8)

No symmetry of F or L was used in this bound. It controls the full60
coefficient witness space, including its closed subspace. It prevents an
unbounded normalized witness sequence for bounded F and normalized L.

## 4. Actual heat classes lie in K

On a rank-one h=eta⊗xi⊗xi all wedge terms vanish, so (1) implies

    sym[B_F(A,xi)L(xi)]>=0,

where B_F is the ordinary2×2 acoustic matrix in eta. For any integer
xi≠0, mean convergence gives Re spec L(xi)>0. The elementary Lyapunov
identity is

    B_F = integral_0^infinity exp(−t L^T)
                    (L^T B_F+B_F L) exp(−t L) dt >=0.   (9)

Consequently the acoustic matrix is positive on integer xi, then rational
xi by homogeneous scaling, then all real xi by continuity. Hence H⊂K.
This uses a finite-dimensional identity, not a free convergence theorem
for a potentially nonuniform infinite-mode PDE.

Mean convergence also implies Tr L(xi)>0 on nonzero integer and rational
xi, so Tr L(xi)>=0 for every real xi. Degenerate limiting flows need
not remain mean-converging; they are handled next rather than ignored.

## 5. A closed OUTER class, not an assumed closed flow union

Define Hrel as the set of F∈K for which there exist L satisfying (5),
Tr L(xi)>=0 for all real xi, and a closed quadratic-coefficient Omega
with (1). Explicit ROC admission is part of this OUTER definition.
No claim that every element of Hrel is a valid heat proof is made.
H⊂Hrel by Section4.

Hrel is a cone, possibly nonconvex. It is CLOSED: for F_n→F, normalized
L_n lie in a compact sphere and (8) uniformly bounds Omega_n. Subsequence
limits preserve closedness, all positive inequalities, normalization and
the nonnegative trace condition. This gives a witness at F. The claim
does not assert that the actual union H is closed or convex.

### F* is not in Hrel

The frozen sibling THEOREM_REDUCTION.md proves the following identities
from the literal symmetries of F*. Its closed-form transport is
alpha_new=det(R) Phi*alpha for Phi(A)=C A R; this orientation sign is
retained for reflections. Symmetry averaging of any feasible pair gives

    Lbar(xi)=ell0 |xi|² I+2nu xi1xi2 J,
    ell0=(Tr L11+Tr L22)/4,
    J=[[0,−1],[1,0]].                                   (10)

Here ell0>=0, because Hrel's trace condition implies nonnegative traces
on the two coordinate axes. At A=[[0,1],[1,0]], xi=(1,t), the determinant
of the averaged acoustic positivity matrix is

    256t²(1+t²)[4ell0²t⁴+4ell0²t²−9nu²t²−nu²].          (11)

Its t² coefficient forces nu=0, also when ell0=0.

If ell0>0, the averaged certificate divided by ell0 is an ordinary-heat
closed quadratic certificate. The frozen POLYNOMIAL_BARRIER.md proves
this impossible, without an SOS assumption: its complete equivariant
class has parameter z, and two density values have positive weighted
sum−8, independently of z.

If ell0=0, Lbar=0. The averaged completed density is a positive pure
wedge, hence identically zero by the acoustic spanning/injectivity
argument. But it is an average of positive densities. At each fixed
(A,h), every transformed density is a continuous nonnegative function
of the compact symmetry group and has zero average. Each is zero,
including the identity. Thus the ORIGINAL completed density is zero
for every A,h. In particular

    sym[B_F*(A,xi)L(xi)]=0 for all A,xi.                 (12)

This does not merely state that the flow's average is zero.

At A=E11, literal differentiation gives

    B(x,y)=[[12x²+4y²,8xy],[8xy,4x²+28y²]],
    det B=48x⁴+288x²y²+112y⁴>0 for (x,y)≠0.            (13)

B is nonscalar for every nonzero (x,y): its off-diagonal forces xy=0
if scalar, and equality of the diagonals then forces x=y=0. Left row
rotation invariance of F* makes R B R^T another acoustic matrix at the
SAME xi. Taking R=I,J in (12) and using B+J B J^T=(Tr B)I gives sym L=0.
Thus L(xi)=b(xi)J. The nonscalar B does not commute with J, so (12)
forces b(xi)=0. Hence L(xi)=0 for every xi, contradicting (5).

Both cases are impossible, so F*∉Hrel. This pays the possible collapse
of mean trace to zero rather than assuming a positive limit.

## 6. Polyconvex closure and all differently-flowed finite sums

P is closed. Here is a direct proof allowing arbitrary convex lifts.
PC is equivalent to every finite minors-Jensen inequality

    F(A0)<=sum lambda_i F(A_i)
    whenever sum lambda_i(A_i,det A_i)=(A0,det A0).       (14)

Here lambda_i>=0 and sum lambda_i=1 throughout.

Necessity is convex Jensen. For sufficiency form the convex roof of F
on the minors graph. Every z=(B,s) is the average of graph points B±Y
with det Y=s−det B, so the roof is bounded above everywhere. Condition
(14) fixes its value to F on every graph point. It cannot be −infinity
at some z: choose z' so that a graph point is the midpoint of z and z',
represent z' by two graph points, and combine with successively lower
finite representations of z to contradict (14). Thus the roof is a
finite convex representative. Each inequality (14) is closed under
coefficient limits, proving P closed. Also P⊂K because each rank-one
line maps to an affine line in the minors.

Define the outer combined cone

    S=P+conic_hull(Hrel).

It is a CLOSED convex cone inside K. Indeed (4) makes both P and Hrel
compact on the affine base ell=1. The union of their two bases is
compact. Its convex hull is compact in V by ordinary finite-dimensional
Caratheodory (at most35 points because the base has affine dimension34).
Coning this compact subset of ell=1 is closed. This is the required
closed-sum argument; neither pointedness alone nor arbitrary sums of
closed sets would suffice.

The frozen full35 endpoint face calculation proves that F* is an extreme
ray of K and is not polyconvex. If F* belonged to S, every nonzero term
of a finite generating decomposition would therefore be a positive
multiple of F*. A P term would contradict non-PC. An Hrel term would
contradict Section5 and conicity. At least one term is nonzero, so

    F*∉S,     S_actual⊂S.                              (15)

This covers arbitrarily many heat parts with different flow matrices.

## 7. Strictness, openness, and the unevaluated quantitative gate

Because S is closed and (15) holds,

    delta=dist_in_coefficient_inf_norm(F*,S)>0.

No numerical value of delta is claimed. The monomial coefficient norm
of T² is2. For every 0<epsilon<delta/4,

    F_epsilon=F*+epsilon T²

lies outside S and obeys, for every rank-one R,

    F_epsilon''(A)[R,R]>=4epsilon |A|²|R|².              (16)

In particular it is uniformly strict ROC on normalized nonzero A,R.
Each coefficient ball about F_epsilon of radius

    r<min(delta/4, epsilon/840)

remains outside S and has LH lower bound2epsilon |A|²|R|², by the
1680coefficient Hessian bound. Thus the obstruction contains a genuine
full-dimensional OPEN strict-ROC family; it is not just a degenerate
ray or a lower-dimensional face. F_epsilon itself is also positive
away from zero because F* is.

Finite-dimensional separation supplies a linear functional nonnegative
on S and strictly negative at F*. A rational strict separator exists
after adding a sufficiently small multiple of ell to put it in the
dual interior, then rationally approximating. This is an EXISTENCE
statement only: that separator and a numerical admissible epsilon were
not compiled or claimed free. The exact acquired constants are (4),
(6)–(8), and the orbit data (13).

The theorem concerns polynomial integrand summands and origin-C²
corrections. Arbitrary angular/rational corrections, nonpolynomial
integrand decompositions, nonlinear flows and independent QC arguments
remain outside it. No nonquasiconvex example or Morrey resolution has
been obtained.
