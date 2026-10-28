# A sharp change of lift regularity under arbitrarily weak quadratic regularization

This continuation leaves QC of the new strict-even-ROC/non-PC family
**UNKNOWN**. Its substantive positive result concerns the earlier accepted
strict-PC rational-selector energy. It constructs an exact smooth convex
representative near the entire minors graph after adding any positive
quadratic stiffness, while proving that no convex polynomial representative
exists at any degree. A separate finite stencil gives a quantitative
relative-quartic approximation barrier without requiring exact matching.

The original strict support and polynomial-selector obstruction are accepted
inputs, not re-audited. The completed C2 classification is also an input;
it is not being presented again as the new theorem. General loss of
representative regularity and ordinary convexification are prior tools.
Historical priority of the new regularization and approximation statements
is UNKNOWN after the bounded primary comparison in `SOURCES.md`.

## 1. Input and new regularization theorem

For real 2x2 matrices let T(A)=|A|^2 and q(A)=detA. Suppose a homogeneous
quartic F has a degree-six homogeneous polynomial p with

    k(A)=p(A)/T(A)^2, A!=0;             k(0)=0,
    B_F(A,X)-k(A)q(X)
       >=delta[T(A)|X|^2+|X|^4],       delta>0.       (1)

Let P>0 be the ordinary coefficient-l1 norm of p. Set L=10P.

**Theorem.** For every epsilon>0, the polynomial

    W_epsilon(A)=F(A)+epsilon|A|^2

has a globally finite convex representative g_epsilon in the five minors
which is C-infinity, with positive-definite Hessian, on an open neighborhood
of the ENTIRE minors graph. There is an explicit rational function h_epsilon
on R5 such that g_epsilon is its convex envelope and equals h_epsilon on
that neighborhood. For rational input and rational epsilon, h_epsilon has
rational coefficients.

Smoothness is asserted on the open graph neighborhood, not on every point
of R5. No efficient evaluator for the global convex envelope is claimed.

If F has no polynomial global minor-support selector, then W_epsilon has
no globally convex polynomial lift of any degree, for every epsilon>0.
Thus the regularization repairs the smooth local graph interface exactly
while leaving the global polynomial-lift obstruction intact.

## 2. Smooth the rational selector by a positive denominator shift

Define

    sigma=epsilon/(2P),
    k_sigma(A)=p(A)/(T(A)+sigma)^2.                    (2)

This is smooth on all matrices. It avoids a cutoff or a nonconstructive
smooth extension. Homogeneous coefficient bounds give

    |p(A)|<=P T^3,       |Dp(A)|<=6P T^(5/2).

For T>0,

    |k-k_sigma|
       <=P sigma T(2T+sigma)/(T+sigma)^2
       <=2P sigma.

The same bound holds at zero. Literal differentiation of (2) gives

    |Dk_sigma(A)|<=10P|A|=L|A|.                       (3)

Since |q(X)|<=|X|^2/2, adding the epsilon norm-square term absorbs the
selector error uniformly for every base point and every increment:

    B_(W_epsilon)(A,X)-k_sigma(A)q(X)
      >=(epsilon/2)|X|^2+delta[T(A)|X|^2+|X|^4].      (4)

This is a genuinely global support bound. Small A is not cancelled, and
large A does not require a different regularization scale.

## 3. Explicit smooth extension normal to the graph

Put M=2L^2/delta and define

    h(B,s)=W_epsilon(B)+k_sigma(B)[s-q(B)]
                            +M[s-q(B)]^2.            (5)

For each A let

    ell_A(B,s)=W_epsilon(A)
       +[DW_epsilon(A)-k_sigma(A)cofA]:(B-A)
       +k_sigma(A)[s-q(A)].

This is exactly the tangent plane to h at m(A)=(A,q(A)). Write
X=B-A, d=s-q(B). The determinant identity gives the exact difference

    h(B,s)-ell_A(B,s)
       =[B_(W_epsilon)(A,X)-k_sigma(A)q(X)]
          +[k_sigma(B)-k_sigma(A)]d+Md^2.             (6)

By (3),

    |k_sigma(B)-k_sigma(A)|^2
       <=2L^2[T(A)|X|^2+|X|^4].

Young's inequality in (6), with (4) and the chosen M, proves

    h(B,s)-ell_A(B,s)
       >=(epsilon/2)|X|^2
          +(delta/2)[T(A)|X|^2+|X|^4]+(M/2)d^2.     (7)

The five-dimensional distance is controlled by exactly these terms:

    |(B,s)-m(A)|^2
       <=|X|^2+4T(A)|X|^2+|X|^4+2d^2.

Consequently, with

    c=min(epsilon/2,delta/8,M/4)>0,

every graph tangent has a uniform GLOBAL quadratic gap:

    h(z)>=h(mA)+Dh(mA):(z-mA)+c|z-mA|^2.             (8)

In particular h>=ell_0=0. Since h is finite, its convex envelope
g=conv(h) is finite everywhere. At graph points ell_A<=g<=h gives

    g(A,q(A))=h(A,q(A))=W_epsilon(A).                 (9)

The graph Hessian has a useful direct check. Its determinant-coordinate
block is 2M, and its Schur complement is exactly

    D2W_epsilon(A)-k_sigma(A)D2q
         -Dk_sigma(A)Dk_sigma(A)^T/(2M)
       >=epsilon I+(7delta/4)T(A)I.

Here (4) supplies the first two terms and (3) bounds the outer product.
Thus positive definiteness along the graph is an explicit algebraic
property of the rational h, independently of any envelope computation.

## 4. Why convexification preserves smoothness on a whole neighborhood

The following elementary stable-tangent lemma is the additional step beyond
merely touching the graph.

**Lemma.** Let h be C2 on R^n and let x0 satisfy a global tangent gap
h(x)>=h(x0)+Dh(x0):(x-x0)+c|x-x0|^2 with c>0. Then h equals its convex
envelope throughout an open neighborhood of x0. If h is smooth there,
the envelope is equally smooth there and has positive-definite Hessian.

Proof: the global gap implies D2h(x0)>=2cI. Choose r>0 so D2h>=cI on
B(x0,2r), and K>=c bounding the Hessian norm there. For y sufficiently
close to x0, its tangent plane ell_y supports h on B(x0,r) by this local
convexity. Outside that ball, put R=|x-x0|>=r. The old global gap is cR^2,
while the change of tangent is at most

    K|y-x0| R+(K/2)|y-x0|^2.

Taking |y-x0|<=cr/(8K), and also <=r/4, leaves a positive gap outside
the ball. Thus ell_y is a global lower support for every such y. The
convex envelope is at least ell_y and at most h, so it equals h at each
y in this open neighborhood. Local Hessian positivity is inherited.

The choices are constructive: a bound on D3h in a unit neighborhood gives
a positive r, after which a Hessian bound gives K. For rational h with a
strictly positive denominator, finite rational coefficient/denominator
bounds produce rational conservative choices. No useful uniform radius
or evaluation complexity is claimed.

Applying the lemma to (8) at every graph point proves the theorem. The
union of these open neighborhoods contains the full unbounded graph.
The rational function h itself is a directly evaluable smooth local
representative there; global convexification is needed only to specify
its finite convex continuation away from that neighborhood.

## 5. Why every global polynomial lift still fails

Assume W_epsilon has a globally convex polynomial lift. Differentiating
it in the determinant coordinate on the graph supplies a polynomial k0(A)
with

    B_F(A,X)+epsilon|X|^2-k0(A)q(X)>=0              (10)

for all A,X. Simultaneous scaling (A,X)->(tA,tX), t->infinity, excludes
every nonzero homogeneous component of k0 above degree two: its leading
coefficient can be made negative by choosing the determinant sign of X.
Divide (10) by t^4 and take the limit. Its homogeneous quadratic component
k2 then satisfies

    B_F(A,X)-k2(A)q(X)>=0

globally, contradicting the accepted all-polynomial-selector obstruction.
The lower-order stiffness term disappears in precisely this limit. The
argument excludes polynomial lifts of arbitrary degree, not just one SOS
parameterization.

## 6. A quantitative approximation barrier without exact matching

Return to the accepted literal energy

    F=p0(u^2+v^2)+p2 uv+p3 w^2+L0 q(u-v),
    p0=55220381/10000000000,
    p2=114430029/625000000,
    p3=-801761987/5000000000,
    L0=118849817/4000000000.

Let G be ANY C2 convex function near the zero-minors point and set
E(A)=G(A,q(A)). It need not be polynomial or homogeneous. Define its
local relative quartic error

    e(G;F)=lim_(r down to 0) sup_(0<|A|<=r)
                          |E(A)-F(A)|/|A|^4.

Then

    e(G;F)>=eta0,
    eta0=23251991479965369/335009162080000000000
         =0.00006940703154385015... .                 (11)

This is a proved positive lower bound, not a claim to have computed the
optimal distance over all possible smooth representatives.

To prove it, suppose the relative error is bounded by eta<eta0 near
zero. This implies E(A)=O(|A|^4), hence DG(0)=0 by its tangent plane on
the graph. The weighted blowups t^(-4)G(tB,t^2s) have nonnegative lower
bounds and uniform compact upper bounds from two-graph averages, just
as in the accepted C2 classification. Extract a locally uniform finite
convex limit H. Continuity of G_ss at zero makes H_ss constant and
nonnegative. Equal-s convexity forces its mixed coefficient to be affine;
the quartic growth on the graph kills its constant and linear parts.
Therefore

    H(B,s)=a(B)+alpha s^2,       a convex, alpha>=0,
    |a(B)+alpha q(B)^2-F(B)|<=eta|B|^4.               (12)

This approximation version does not assume that the limiting graph
energy is homogeneous or polynomial.

Let I=diag(1,1), E0=diag(1,0), D=diag(-1,1). For t>0 define the positive
convexity stencil

    C_t(P)=P(I+tD)+P(I-tD)-2P(I)
            +2P(E0+tD)+2P(E0-tD)-4P(E0).

For convex a, C_t(a)>=0; direct expansion gives C_t(q^2)=6t^4>=0.
Thus the left graph energy in (12) has nonnegative stencil. Set

    g0=L0-4p0=152486037/20000000000,
    f0=F(D)=2p0+p2=970660613/5000000000.

Literal quartic expansion gives

    C_t(F)=-12g0 t^2+6f0 t^4,
    sum |stencil_weights| |stencil_points|^4=24(1+t^2)^2.

Hence any eta in (12) must be at least

    (2g0 x-f0 x^2)/[4(1+x)^2],        x=t^2.

This entire stencil family is optimized exactly at x=g0/(g0+f0),
with value g0^2/[4(2g0+f0)]=eta0, contradicting eta<eta0. This proves
(11) without any derivative comparison between E and F.

## 7. A nonclosedness phenomenon and a precise stiffness tradeoff

The regularized W_epsilon have convex representatives smooth near the
entire graph, but converge to F in C-infinity on every compact subset
as epsilon goes to zero. In fact on |A|<=R,

    |W_epsilon-F|<=epsilon R^2,
    |DW_epsilon-DF|<=2epsilon R,
    ||D2W_epsilon-D2F||=2epsilon,

and every derivative of their difference above order two vanishes.
Nevertheless F has no local C2 convex representative. Thus smooth
representability in this exact minor interface is not closed even under
C-infinity convergence of the represented energies.

There is no conflict with (11). The approximating energies introduce a
nonzero quadratic stiffness: epsilon|A|^2/|A|^4 diverges at zero. Requiring
quartic flatness rather than allowing this lower-order regularization
retains the positive relative-error barrier. All W_epsilon still fail
the global polynomial-lift architecture by Section 5.

These local statements can be moved to any prescribed background Astar.
The minors of B-Astar are the affine transform

    (B,s)->(B-Astar,s-cof(Astar):B+detAstar).

It is invertible and preserves convexity and C2 smoothness of a lift.
Thus the same approximation barrier holds for F(B-Astar) at Astar,
measured relative to |B-Astar|^4. This is a mathematical coordinate
transport; it does not assert frame indifference or physical realizability.

## 8. Executed work and limits

`verify_regularization.py` independently reconstructs the literal F,p,
coefficient bound P, denominator-shift inequalities, graph tangent identities,
global-gap constants, and the finite approximation stencil. It records
exact constants for epsilon=1/100. The analytic stable-tangent argument
is proved above; finite code checks do not replace it.

Before this structural opening, `heat_search.py` implemented an independent
compatible Fourier heat-dissipation operation with analytic background
deflation and checked gradients. Its 24 bounded starts over three frequency
sets all stayed positive (best normalized dissipation about 2.67070).
Those outcomes neither establish heat monotonicity nor QC. The attempted
linear-flow normal-form reduction was recognized as already completed
prior work in the supplied output-flow extension, and is not counted new.

The new completed statements are (2)--(9), the no-polynomial persistence,
and the quantitative approximation/germ tradeoff. They do not resolve QC
for a non-PC target, yield a physical model, or supply a cheap global
convex-envelope algorithm. External priority remains UNKNOWN.
