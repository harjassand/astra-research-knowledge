# Local C2 convex lifts of homogeneous planar quartics are rigid

This is an internally constructed theorem, with an independent challenge of
its proof spine by the parent. It is not a world-priority claim. Loss of
regularity between a polyconvex energy and its convex representatives is
established prior work; the bounded comparison is in `SOURCES.md`.

The previously accepted rational-selector energy is an input, not re-audited
here. The main theorem below does not use its certificate or its 24-atom
polynomial-selector obstruction. An elementary two-background Hessian
functional supplies the application.

## 1. A complete local smooth-lift classification

Put V=R^(2x2), q(A)=det A, and m(A)=(A,q(A)). Let F:V->R be a homogeneous
quartic polynomial, so F(tA)=t^4 F(A) for real t. Then the
following are equivalent.

1. There is a convex neighborhood U of (0,0) in V x R and a real-valued
   convex function g on U, of class C2 on a neighborhood of (0,0), such
   that g(A,q(A))=F(A) whenever A is sufficiently small.
2. There is an alpha>=0 such that A -> F(A)-alpha q(A)^2 is convex on V.
3. F has the globally defined convex lift

       g0(B,s)=F(B)-alpha q(B)^2+alpha s^2,

   which is a convex polynomial and therefore smooth.

In condition 1 it is enough that g is convex on an open ball and C2 on a
possibly smaller open ball; restriction to a ball removes any ambiguity
about its domain. The obstruction is genuinely local at the zero-minors
point. It does not assume that the original representative is homogeneous,
polynomial, or smooth outside that neighborhood.

### 1.1 The gradient at zero vanishes

We may shrink the domain so that g is C2 there. Its tangent plane at zero
has coefficients (v,k), and g(0,0)=F(0)=0. Thus, for every A and small real t,

    t^4 F(A) >= t v:A+t^2 k q(A).

Using both signs of t and then sending t to zero forces v=0. Division by
t^2 and the fact that q has both signs force k=0. Convexity consequently
gives g>=0 on its domain. In particular F>=0, first locally and then
everywhere by homogeneity.

Let c=partial_ss g(0,0). Convexity gives c>=0.

### 1.2 Weighted blowups have uniform bounds on every compact set

For t>0 set

    g_t(B,s)=t^(-4) g(tB,t^2 s).

The domains of g_t contain every fixed compact subset of V x R once t is
sufficiently small. These functions are convex and nonnegative. They all
agree with F on the part of the minors graph in their domain.

There is a uniform upper bound that does not use a derivative estimate.
Given (B,s), write d=s-q(B) and choose

    Y=diag(sqrt(|d|), sign(d) sqrt(|d|)),   Y=0 if d=0.

Then det Y=d, |Y|^2=2|d|, and the planar determinant identity gives

    (B,s) = [m(B+Y)+m(B-Y)]/2.

For a compact set of (B,s), the matrices B+Y and B-Y remain bounded, so
their scaled graph points lie in the domain of g for all sufficiently
small t, uniformly on the compact set. Convexity and homogeneity give

    0 <= g_t(B,s) <= [F(B+Y)+F(B-Y)]/2.                 (1)

The right side is bounded on each compact set. This handles the fact that
the original g is only a local lift; no remote values of g are used.

Convex functions bounded above and below on a slightly larger ball have a
uniform Lipschitz bound on each smaller ball, by their one-dimensional
secant slopes. Applying this to (1), followed by Arzela-Ascoli and a diagonal
subsequence on balls of integer radii, yields t_j down to zero for which
g_(t_j) converges uniformly on compact sets to a finite convex function h
on all of V x R. It satisfies

    h>=0,                 h(B,q(B))=F(B).             (2)

### 1.3 The limiting vertical curvature is constant

The determinant coordinate has weight two. This is the decisive point:

    partial_ss g_t(B,s) = partial_ss g(tB,t^2s)
                         -> c

uniformly on every compact set. The C2 hypothesis is used precisely here.
Uniform convergence on compact sets and integration against a compactly
supported smooth test function show that partial_ss h=c in distributions.
Equivalently, one may integrate the preceding second-derivative identity
twice on each vertical line and use secant slopes to identify the linear
term. Continuity of h then gives continuous a,b:V->R with

    h(B,s)=a(B)+s b(B)+(c/2)s^2.                       (3)

No differentiability of a or b is needed.

### 1.4 Global convexity forces the mixed coefficient to be affine

Fix B1,B2, theta in [0,1], and Btheta=theta B1+(1-theta)B2. Convexity of h
between (B1,s) and (B2,s), using (3), says

    0 <= theta a(B1)+(1-theta)a(B2)-a(Btheta)
         +s[theta b(B1)+(1-theta)b(B2)-b(Btheta)]

for every real s. The coefficient of s must be zero. Therefore b is
Jensen-affine, and its continuity makes it affine in the usual sense:

    b(B)=beta+v:B.

By (2), a(0)=F(0)=0. Nonnegativity of h(0,s) for every s forces beta=0.
Evaluating (3) on the minors graph now gives

    a(tB)=t^4[F(B)-(c/2)q(B)^2]-t^3 q(B)(v:B).

But a(tB)=h(tB,0)>=0 for both signs of t. The cubic coefficient therefore
vanishes for every B. Since q is nonzero on a dense open set, v=0. Hence

    h(B,s)=F(B)-(c/2)q(B)^2+(c/2)s^2.                  (4)

Its restriction to s=0 is convex, proving condition 2 with alpha=c/2.
Conversely, condition 2 makes the displayed lift convex and C2 for any
quartic polynomial F, proving condition 1. This completes the proof.

In fact (4) identifies every cluster limit, since c is fixed by g. Thus
the weighted blowups converge locally uniformly to (4), without choosing
a subsequence in the final conclusion.

## 2. A small exact obstruction for the accepted energy

Use the accepted input

    F=p0(u^2+v^2)+p2 uv+p3 w^2+L q(u-v),
    u=a^2+c^2, v=b^2+d^2, w=ab+cd, q=ad-bc,

    p0=55220381/10000000000,
    p2=114430029/625000000,
    p3=-801761987/5000000000,
    L =118849817/4000000000.

Let I=diag(1,1), E=diag(1,0), and D=diag(-1,1). For an arbitrary real
alpha, put H_alpha=F-alpha q^2. Literal differentiation on the diagonal
line gives

    D2 H_alpha(I)[D,D] =24p0-4p2+4alpha,
    D2 H_alpha(E)[D,D] =12p0+2p2-6L-2alpha.

Consequently

    D2 H_alpha(I)[D,D]+2 D2 H_alpha(E)[D,D]
        =12(4p0-L)<0.                                 (5)

The determinant-square term cancels exactly. Both summands would be
nonnegative for a convex H_alpha, so (5) excludes every real alpha, even
without the theorem's alpha>=0 restriction.

The exact gap is

    L-4p0 = 152486037/20000000000 > 0.

The accepted energy therefore has no C2 convex representative in any
neighborhood of the zero-minors point. Its independently accepted finite
convex lift and quantitative PC/QC property remain valid. This regularity
obstruction does not require its all-polynomial-selector obstruction.

### 2.1 Full35 stability of this separate obstruction

Define the linear Hessian functional

    T(P)=(1/4)D2P(I)[D,D]+(1/2)D2P(E)[D,D].

Then T(q^2)=0 and T(F)=12p0-3L=-3(L-4p0). In the ordinary 35-monomial
quartic basis of (a,b,c,d), the only nonzero coefficients of T are

    T(a^4)=9,       T(a^3 d)=-3,       T(d^4)=3.

Thus its exact coefficient-l1 norm is 15. If every quartic coefficient of
a perturbation P differs from F by at most

    epsilon=(L-4p0)/10=152486037/200000000000,

then

    T(P)<=-3(L-4p0)+15epsilon
         =-(3/2)(L-4p0)<0.                             (6)

Every such P has no local C2 convex lift. Intersecting this box with the
already accepted smaller PC/QC box gives a full-dimensional open set of
strict PC/QC polynomial energies with no local C2 lift. Equation (6) does
not assert PC outside the separately certified PC box.

`verify_smooth_lift_obstruction.py` reconstructs all quantities in this
section from the literal quartic with exact rational symbolic arithmetic;
it checks all 35 monomials, (5), the rational gap, and the comparison with
the accepted PC-box radius. It does not replace the analytic blowup proof.

## 3. Necessary ordinary comparator: this phenomenon is already present
##    in the classical ADM energy

The theorem is not an effect unique to nonlinear rational selectors.
The classical Alibert-Dacorogna-Marcellini energy

    F_ADM(A)=|A|^4-2|A|^2 detA

is PC and even has a polynomial SOS support in the pinned primary source.
Nevertheless it has no local C2 convex lift. For example F_ADM(I)=0, so
convexity and nonnegativity of F_ADM-alpha q^2 force alpha=0. But at
A=diag(1,2), X=diag(3,1), literal differentiation gives

    D2F_ADM(A)[X,X]=-20.

The phenomenon also persists for explicitly strict PC examples. Since
F_ADM is PC and |A|^4 is uniformly convex in the quartic support sense,

    F_eta=F_ADM+eta|A|^4

is strictly PC for eta>0. At the same A,X,

    D2(F_eta-alpha q^2)(A)[X,X]
        =-20+400eta-122alpha.

This is negative for every alpha>=0 when 0<eta<1/20. In particular eta=1/100
is an ordinary strict-PC example with no local C2 lift. This prevents the
new accepted certificate from being credited with a regularity separation
that does not depend on its stronger no-polynomial-selector property.

## 4. Consequences and precise limits

* A globally convex polynomial lift of any degree is C2 near zero and is
  excluded. Independently, a polynomial lift would supply a polynomial
  selector partial_s g(A,q(A)), so the previously accepted selector
  obstruction already excluded it.
* For homogeneous planar quartics there is an exact, strict hierarchy:

      local C2 convex lift
        <=> convex polynomial lift of some degree
        <=> F-alpha det^2 convex for some alpha>=0
        => polynomial global support selector
        => polyconvexity.

  The last two implications are both strict. The classical ADM energy
  separates polynomial support from C2 liftability. The accepted rational
  energy separates PC from every polynomial support selector. Increasing a
  polynomial lift's degree or changing its smooth non-polynomial formula
  cannot repair the first restriction at zero.
* The theorem supplies a complete test for C2 liftability of a homogeneous
  quartic: find alpha>=0 making the quadratic-matrix Hessian of
  F-alpha q^2 positive semidefinite for every A. It is a single scalar
  feasibility problem, not an unrestricted functional extension problem.
  Exact fixed-dimensional real quantifier elimination is an in-principle
  decision method; no practical QE implementation is claimed here.
* A constitutive architecture convex and C2 in the raw five minor inputs
  cannot represent these quartics exactly on any neighborhood of the zero
  matrix. This statement concerns the chosen input interface and exact
  equality. It does not exclude approximation, extra non-minor features,
  or a representation only on detA>0 away from the zero matrix.
* The zero matrix is a collapsed deformation, not the undeformed identity
  configuration. No claim about physical material realizability or a
  smooth lift localized near an invertible background follows.
* The proof uses continuity of the second derivative of g near zero. It
  does not exclude mere twice Frechet differentiability at that single
  point, a C1 lift, or a C1,1 lift. Parent work separately addresses the
  positive regularity attainable from the accepted strict rational jet.
* This theorem does not classify all PC quartics or the even-six ROC cone,
  and supplies no compatible-gradient counterexample to quasiconvexity.

## 5. Contribution boundary

The substantive new internal result here is the local C2 classification,
proved by a weighted convex blowup, together with a three-monomial exact
separator for its failure at the accepted energy. General loss of lift
regularity is established prior work. The classical ADM comparator already
exhibits no-C2 liftability under this classification, so that particular
phenomenon cannot be claimed as machinery-exclusive or a first discovery.
External novelty of the classification remains UNKNOWN after the bounded
primary-source check.
