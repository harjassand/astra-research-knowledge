# Every minimal positive circuit has a global quadratic anchor

Exact internal derivation, 22 October 2026. Independent adversarial audit
requested. The anchor theorem is finite-dimensional convex geometry and
has no K-QC or quasiconvexity premise. The QC consequence at the end uses
the separately named quadratic-anchor K gluing theorem.

## Statement

Let m=r+1, let v1,...,vm be nonzero vectors spanning Rr, and suppose

    ker N=span{k}, k_i>0, N=[v1 ... vm].

Thus the vectors form a minimal positive circuit. Put

    Phi(z)=sum_i (vi.z)_-^2,    A=sum_i vi vi^T,
    Ai=A-vi vi^T=sum_{j!=i} vj vj^T.

There are weights theta_i>=0, sum theta_i=1, such that

    S=sum_i theta_i vi vi^T >=0,
    z^T Sz <=Phi(z) for EVERY z in Rr.                 (1)

Consequently, if the quadratic forms Hi=Q+vi^2 are all rank-one convex
on 2x2 matrices (the vectors vi represent linear forms in the circuit
normal space), then

    H*=Q+S=sum_i theta_i Hi

is a globally rank-one-convex quadratic, hence a polyconvex quadratic,
and H*<=F=Q+Phi globally. The weights depend only on the circuit vectors,
not on Q, the determinant signature of their plane, or local completion
multipliers.

## 1. Exact quadratic minorant cone of the circuit potential

For every symmetric S>=0,

    S(z)<=Phi(z) for all z
        iff S<=Ai for EVERY i.                       (2)

Here <= between matrices means positive semidefinite order. This is not
a statement for an arbitrary indefinite quadratic S.

Let B_+={a in Rm:a_i>=0,|a|<=1}, and K=-N B_+. Then

    h_K(z)=max_{a>=0,|a|<=1} -sum_i ai vi.z
          =sqrt(Phi(z)).

K is compact and convex. For any symmetric M>=0 write its centered
(possibly degenerate) ellipsoid as E_M={M^(1/2)y:|y|<=1}. Its support
function is sqrt(z^T Mz). Thus

    S<=Phi iff E_S subset K
             iff E_S subset K intersect(-K),          (3)

since E_S is centrally symmetric.

We claim the exact body identity

    K intersect(-K)=intersection_i E_Ai.              (4)

The sign in K is immaterial to its intersection with -K. Fix x in Rr,
and write all solutions of Na=x as

    a=b+t k,       b perpendicular k.

The vector b is uniquely determined. If b!=0, its weighted coordinates
b_i/k_i have both signs, since sum_i b_i k_i=0 and k_i>0. Therefore

    t_min=max_i(-b_i/k_i)>=0,
    x in N B_+ iff |b|^2+|k|^2 t_min^2<=1.

For -x the orthogonal solution is -b. Hence simultaneous membership of
x and -x is exactly

    |b|^2+|k|^2 max_i (b_i/k_i)^2<=1.                 (5)

On the other hand, any r columns of N are independent. The unique
solution of Na=x with ai=0 is

    a=b-(b_i/k_i)k,

whose squared norm is |b|^2+|k|^2(b_i/k_i)^2. The image of the full
unit ball in the coordinate hyperplane ai=0 is precisely E_Ai.
Consequently (5) is equivalent to membership in every E_Ai, proving
(4). This also covers x=0 directly.

By (3),(4), E_S subset K is equivalent to E_S subset E_Ai for all i.
Centered ellipsoid containment is equivalent to S<=Ai, proving (2).
This argument includes singular S; every Ai is positive definite.

## 2. Construct the anchor by a D-optimal design

Maximize log det W over probability weights omega_i>=0,sum omega_i=1,
where

    W=sum_i omega_i vi vi^T.

A positive definite W is feasible, so a maximizer exists and has W>0
(equivalently maximize the continuous determinant on the simplex, whose
maximum is positive). The elementary first-order optimality conditions are

    li:=vi^T W^-1 vi <=r for every i,
    li=r whenever omega_i>0.                         (6)

Indeed the directional derivatives of log det are li; their weighted
average is tr(W^-1W)=r. Moving weight to any index cannot increase the
objective at an optimum, giving li<=r and equality on the support.

Since W>=omega_i vi vi^T, a support index has

    r=li<=1/omega_i,

by the rank-one Schur criterion. Therefore EVERY omega_i<=1/r
(the zero weights obey it trivially). Define

    theta_i=1-r omega_i >=0.

As m=r+1,

    sum_i theta_i=m-r=1.

Let S=sum_i theta_i vi vi^T=A-rW. It is PSD as a positive combination.
The other part of (6) says vi^T(rW)^-1vi<=1, or equivalently

    rW>=vi vi^T for every i.

Thus

    S=A-rW<=A-vi vi^T=Ai for every i.

The exact minorant criterion (2) proves (1). This completes the anchor
theorem. No numerical optimization or strict-interior design hypothesis
is used: two- or lower-support optima are allowed.

## 3. Relation to physical hinge coefficients

For F=Q_R+sum_i ci(ell_i)_-^2, represent the normalized circuit normals
by ni and set vi=sqrt(ci)ni. If sum_i alpha_i ni=0 with alpha_i>0,
then k_i=alpha_i/sqrt(ci)>0. Hence all preceding hypotheses hold for
any positive ci. The global quadratic anchor is

    H*=Q_R+sum_i theta_i ci ell_i^2
      =sum_i theta_i (Q_R+ci ell_i^2).

All maximal local quadratics Hi are globally R1C whenever F is globally
R1C, because the corresponding open chambers are nonempty. Conversely
the usual C1 rank-one-line gluing gives global R1C from those quadratics.

This construction includes balanced coefficients that have no original
maximal-cell anchor. For r=2, sum_i ni=0 and equal ci, theta_i=1/3 is
one valid choice, independently of the shape of that normalized circuit.
Equal ci alone does not suffice when the positive dependence instead
has unequal coefficients alpha_i; either retain the D-optimal weights
or first normalize the normals and adjust the ci accordingly.

## Explicit weights for a normalized three-circuit

For r=2 and n1+n2+n3=0, put ai=1/ci. If some ai>=aj+ak,
theta_i=1 and the other weights zero give the usual harmonic anchor.
Otherwise the ai are the side lengths of a strict triangle. Define

    Delta=2(a1*a2+a1*a3+a2*a3)-(a1^2+a2^2+a3^2)>0,
    theta_i=(ai^2-(aj-ak)^2)/Delta.

These weights are strictly positive and sum to one. They coincide with
theta_i=1-2omega_i for the D-optimal weights

    omega_i=ai*(aj+ak-ai)/Delta.

One can check the PSD caps without optimization. In the basis (nj,nk),
write p=ai+aj-ak and q=ai-aj+ak. The exact factorization is

    Ai-S=(q*nj-p*nk)(q*nj-p*nk)^T/(ai*Delta)>=0.

Thus this explicit rational formula (when the ci are rational) also
provides the universal three-cut anchor certificate. At a triangle
boundary it reduces to the single-cell harmonic choice.

## 4. Conditional QC consequence for minimal circuits on 2x2 matrices

Use the separately audited root extension of the K bridge with

    Hi-H*=vi^2-S,     S>=0.

For every maximal-cell background B, F(B)=Hi(B) and vi(B)<0. Also
F>=H* everywhere and F>=Hi on {vi<=0}. If Hi(B)>H*(B), that bridge
provides a global QC touching minorant. If equality holds, H* itself
is already a QC touching minorant. Thus all maximal cells are covered.

For completeness, fix a smooth compact test gradient V of mean zero.
Its quadratic Jensen gap E Q_R(V) is independent of background, even
with arbitrary quadratic cross couplings. For scalar mean-zero X,

    d(t)=E(t+X)_-^2-t_-^2

is concave on t<0, since d''=2(P(t+X<0)-1)<=0 in distributions.
At a background with several negative cut values, hold the positive
ones fixed. The negative values vary in the compact weighted simplex

    x_i<=0,      sum_{negative i} alpha_i x_i
               =-sum_{positive i} alpha_i x_i.

The fixed-test Jensen gap is concave on this simplex. Its minimum is
therefore attained at a vertex, where only one cut is strictly negative.
Those vertex backgrounds are in closures of the maximal cells. Walls
and the all-zero cut background follow by continuity. Hence Jensen
holds at every background.

Provided the named PSD-subtraction K bridge and inherited K-QC theorem
hold, every globally rank-one-convex central negative-hinge integrand
whose normals form ONE minimal positive circuit is globally QC, with
arbitrary quadratic Q_R and every determinant signature of the normal
space. In 2x2 matrices the circuit rank is at most 4, so m<=5.

This does not establish that arbitrary larger hinge networks decompose
into minimal-circuit integrands and convex/PC terms. The full Morrey
problem remains NOT_ACHIEVED; external correctness and novelty remain
unassessed.
