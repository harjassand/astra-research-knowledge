# An unnormalized Schur representation that retains weak and dark interventions

28 October 2026. New derivation and scoped challenge for the P1 continuation.
This proves a representation and uniform stability statement. It does not
assert that its parameters are uniquely or cheaply identified from a finite
scalar record. Physical calibration, source-class, and acquisition obligations
are unchanged.

## 1. Input and response

Let Q0 be a real symmetric positive definite d-by-d matrix, e a nonzero port
vector, and v1,...,vn arbitrary real intervention vectors. Nonnegative commands
u give the actual rank-one-shunted source

    Q(u)=Q0+sum_i u_i v_i v_i^T,  u_i>=0,
    z(u)=e^T Q(u)^(-1)e,  J(u)=1/z(u).

Define

    w=Q0^(-1/2)e,      a_i=Q0^(-1/2)v_i,
    z0=w^T w>0,       h_i=w^T a_i,
    c0=1/z0,          g_i=h_i/z0,
    B_ij=a_i^T a_j-h_i h_j/z0.

B is positive semidefinite: it is the Gram matrix of
`a_i^perp=a_i-(h_i/z0)w`. In particular no h_i, g_i, or B_ii is divided by.
An intervention can be exactly dark at the baseline, h_i=g_i=0, while its
orthogonal vector and its B couplings remain nonzero.

Let U=diag(u), P=sqrt(U), and M=I+PBP. Then

    J(u)=c0+g^T P M^(-1)P g.                         (1)

The only inverses in (1) are of a matrix bounded below by I and the positive
baseline scalar z0. Weak individual port-intervention couplings introduce no
singular normalization.

## 2. Two proofs of the identity

### Woodbury proof

Let A have columns a_i and b=Ph. Woodbury gives

    z(u)=z0-b^T [I+P A^T A P]^(-1)b.

Because `A^T A=B+h h^T/z0`, the bracket is `M+b b^T/z0`.
Put v=b^T M^(-1)b>=0. The rank-one inverse identity yields

    b^T(M+b b^T/z0)^(-1)b=v/(1+v/z0),
    z(u)=z0^2/(z0+v).

Taking the reciprocal proves (1). This remains valid for zero entries of u
or h; there is no inverse of U or any individual coupling.

### Constrained-energy proof

Cauchy-Schwarz in the Q(u) inner product gives

    J(u)=min_{e^T x=1} x^T Q(u)x.

Write `x=Q0^(-1)e/z0+y` with `e^T y=0`. Orthogonality gives

    J(u)=c0+min_y [y^T Q0 y+sum_i u_i(g_i+v_i^T y)^2].

In orthonormal energy coordinates on the orthogonal subspace, write the
projected intervention vectors as b_i, so `b_i^T b_j=B_ij`. Thus

    J(u)=c0+min_y [||y||^2+sum_i u_i(g_i+b_i^T y)^2].  (2)

Solving this strictly convex quadratic gives (1). Formula (2) also proves
monotonicity and concavity of J in u: it is an infimum of affine increasing
functions of the nonnegative commands.

## 3. Exact converse and sign gauge

For **every** c0>0, every real g, and every B positive semidefinite, choose a
Gram factor with columns b_i and `b_i^T b_j=B_ij`. Let

    Q0=diag(c0,I_rank(B)),  e=e0,  v_i=(g_i,b_i).

Direct substitution gives z0=1/c0, h_i=g_i/c0, the specified g, and the
specified B. This finite-dimensional positive source realizes (1) exactly.
If B=0, the hidden orthogonal space can have dimension zero. Extra inactive
coordinates may be added without changing the response.

This converse is within the stated positive quadratic-form/rank-one
intervention class. It does not show that a particular resistor-graph,
coordinate-shunt, local-actuator, or other restricted apparatus realizes
arbitrary v_i=(g_i,b_i) at no cost. Extra structural constraints on a physical
source must remain constraints on the compatibility family; PSD alone cannot
replace them.

Changing v_i to -v_i does not change its physical shunt. For any diagonal
sign matrix D, the resulting parameters are `g->Dg`, `B->DBD`; since D
commutes with U and P, (1) is invariant. Consequently one can choose g_i>=0.
For g_i=0 the sign is free and its B row/column must still be retained.

Two parameter triples compared by an entrywise metric must be placed in a
common/aligned gauge. The nonnegative-g convention can jump when a coupling
crosses zero; this is not an acquired continuity theorem for B. A feasibility
family should retain the legal sign branches near a dark coupling rather than
silently selecting one.

## 4. Uniform finite-error theorem under a total-dose budget

Assume two triples satisfy c0,c0'>0, B,B'>=0 and

    |c0-c0'|<=ec0,
    max_i |g_i|, max_i |g_i'| <= G,
    max_i |g_i-g_i'| <= eg,
    max_ij |B_ij-B_ij'| <= eb.

For every u>=0 with `sum_i u_i<=delta`,

    |J(u)-J'(u)| <= ec0+2 delta G eg+delta^2 G^2 eb.   (3)

This bound contains no explicit n. It is uniform over weak/dark couplings,
singular B, zero commands, and arbitrary rank of B.

**Proof.** Set `M=I+PBP`, `M'=I+PB'P`. Both inverse operator norms are <=1.
At fixed B, factor the quadratic-form difference:

    |(Pg)^T M^-1(Pg)-(Pg')^T M^-1(Pg')|
      <= ||P(g-g')|| ||P(g+g')|| <= 2 delta G eg.

For the B change, the resolvent identity gives

    M^-1-M'^-1=M^-1 P(B'-B)P M'^-1.

The weighted entry bound has no dimension penalty:

    ||P(B'-B)P||_2 <= ||P(B'-B)P||_F
       <= eb sqrt(sum_ij u_i u_j) <= delta eb.

Since `||Pg'||^2<=delta G^2`, the remaining quadratic-form change is at
most `delta^2 G^2 eb`. Add the c0 difference. The same derivation with the
actual dose t=sum u_i gives the sharper pointwise expression
`ec0+2tG eg+t^2 G^2 eb`.

**Why the premises matter.** B and B' must remain PSD, or a resolvent can
approach a pole. The budget is total dose, not an individual coordinate cap.
With n commands each at delta, g_i=G, B=0 and B'=eb*11^T, the responses
differ by `G^2 eb(n delta)^2/(1+eb n delta)`. Replacing total dose n delta
by the coordinate cap delta would therefore be false.

This is a continuity theorem conditional on parameter enclosures. It supplies
no universal acquisition count for ec0,eg,eb and does not turn a noisy
indistinguishable family into a unique model.

## 5. Gradients, concavity, and uncertainty in a proposed control

Define

    r(u)=(I+BU)^(-1)g
         =g-BP(I+PBP)^(-1)Pg.

The nonsymmetric matrix `I+BU` is invertible for all u>=0; the second
formula proves this without an inverse of U. In the Gram realization,
the minimizer of (2) has residuals `r_i=g_i+b_i^T y_*`.
The envelope theorem, or direct differentiation, gives

    partial_i J(u)=r_i(u)^2 >=0.                      (4)

This formula is valid at zero commands as the continuous right derivative.
Writing C=I+sum_i u_i b_i b_i^T and K_ij=b_i^T C^-1 b_j gives

    partial_i partial_j J(u)=-2 r_i r_j K_ij,
    Hessian J=-2 diag(r) K diag(r) <=0.               (5)

The derivative is not necessarily zero at a baseline-dark intervention once
other interventions are active.

### Dimension-free gradient bound

Suppose additionally `max_i B_ii<=kappa`. PSD then gives
`|B_ij|<=kappa`. If t=sum u_i<=delta, write
`w=P(I+PBP)^(-1)Pg`. Cauchy-Schwarz gives `||w||_1<=tG`, hence

    ||r||_infinity <= G(1+kappa delta),
    ||grad J||_infinity <= G^2(1+kappa delta)^2.       (6)

A sharper fixed-source residual bound follows from (2). For
X=[sqrt(u_i)b_i], z=Pg, the optimizer is
`y_*=-(I+XX^T)^(-1)Xz`. Every singular value of the middle operator is
`sigma/(1+sigma^2)<=1/2`. Therefore

    |r_i| <= G[1+(1/2)sqrt(kappa delta)].             (7)

The simpler bound (6) is convenient for comparing uncertain models.

### Gradient perturbation bound

If both B and B' have maximum diagonal <=kappa, and the parameter errors
are as in (3), then

    ||grad J-grad J'||_infinity
       <=2G(1+kappa delta)^2(eg+delta G eb).          (8)

Indeed for `w=P M^-1 Pg`, `w'=P M'^-1 Pg'`,

    ||w-w'||_1<=delta eg+delta^2 G eb,
    ||r-r'||_infinity
       <=eg+eb||w||_1+kappa||w-w'||_1
       <=(1+kappa delta)(eg+delta G eb).

Multiply by the bound `|r_i|+|r_i'|<=2G(1+kappa delta)`.
There is no c0 contribution to the gradient.

Equations (5)-(6) also give the simple within-source smoothness estimate

    ||grad J(u)-grad J(v)||_infinity
       <=2 kappa G^2(1+kappa delta)^2 ||u-v||_1       (9)

for u,v in the same dose simplex. This uses `0<=K<=B` and integrates the
entrywise Hessian bound along the segment between u and v.

For a retained family Theta, `F(u)=inf_theta J_theta(u)` is concave in u.
When the infimum is attained at theta_u, `grad J_theta_u(u)` is a
supergradient of F. An epsilon-suboptimal inner minimizer supplies an
epsilon-supergradient. This does not claim that finding the worst compatible
parameter triple is convex or inexpensive; acquisition constraints can make
that inner problem hard.

## 6. A dark intervention that cannot be dropped

Take c0=1, g=(1,0), and B=[[1,1],[1,1]]. This is PSD and has the exact
canonical realization v1=(1,1), v2=(0,1), Q0=I. Formula (1) gives

    J(u1,u2)=1+u1(1+u2)/(1+u1+u2).

The second intervention is invisible in every baseline-only sweep:
`J(0,u2)=1`. Yet when u1>0,

    partial_2 J=u1^2/(1+u1+u2)^2 >0.

For u1=1/2, increasing u2 from 0 to 1/2 changes J from 4/3 to 11/8,
an exact gain of 1/24. Deleting a dark row/column on the basis of its single
intervention response loses this capability. Both points respect total dose
at most one. The unnormalized representation retains it without dividing by
the zero baseline coupling.

### A whole singles-and-pairs record can miss a legal joint task

For the main physical total-dose budget delta=1/5, take c0=1, g=(1,0,0), and

    B_plus  = [[1,1/2,1/2], [1/2,1, 1/4], [1/2, 1/4,1]],
    B_minus = [[1,1/2,1/2], [1/2,1,-1/4], [1/2,-1/4,1]].

Both are strictly positive definite: their leading principal minors are
1,3/4,9/16 and 1,3/4,5/16 respectively. A fully rational six-dimensional
canonical source uses Q0=I6, e=e0, and v_i=(g_i,b_i), where

    b1=(1,0,0,0,0), b2=(1/2,1/2,1/2,1/2,0),
    b3_plus =(1/2, 1/2,-1/2,0,1/2),
    b3_minus=(1/2,-1/2,-1/2,0,1/2).

Their Gram matrices are B_plus and B_minus exactly. No irrational source
coordinates or source-fitting approximation is involved.

Every intervention supported on at most two coordinates gives the same J
for these sources, at every nonnegative amplitude, not only on a finite
design. If coordinate 1 is absent, the active g is zero. If coordinate 1
is present with at most one other coordinate, the relevant principal
submatrices of B coincide. Inactive coordinates have zero P rows/columns
and cannot affect (1). The claim therefore covers every legal adaptive
singleton/pair transcript under delta=1/5.

At the legal joint command u=(1/15,1/15,1/15), however,

    J_plus=1103/1038,  J_minus=1069/1006,
    J_minus-J_plus=1/261057.

With the native known boundary baseline r0=3/2, raw R=r0+J gives

    R_plus=1330/519,  R_minus=1289/503,
    R_minus-R_plus=1/261057.

The exact midpoint task threshold is

    J_threshold=277405/261057,
    R_threshold=1337981/522114.

Equivalently, compare doing nothing with executing the joint intervention
at cost `C=16348/261057` in the same response units. The gain-minus-cost
is `-1/522114` for B_plus and `+1/522114` for B_minus. Thus the two sources
require opposite choices on this explicit two-action task. No number of
singleton/pair observations can resolve that choice. Every deterministic
choice based only on such a transcript has regret 1/522114 on one source.

One additional triple raw reaction distinguishes this two-source family if
the absolute raw error eta satisfies `2 eta<1/261057`. For a certificate
that simply compares the acquired raw interval with the midpoint threshold,
the stronger `4 eta<1/261057` guarantees that **every** allowed noisy report
still has its entire interval on the correct side. The exact saved test uses
eta=1e-7 and the worst perturbations toward the threshold. A separate
uncertainty in the calibrated r0 or a baseline-derived cost must be included
in the corresponding interval; it is not removed by this witness.

This is necessity/sufficiency of one extra triple query for the displayed
two-source/two-action ambiguity, not one-query recovery of an unrestricted
network. The difference is a cycle-sign invariant, not an arbitrary sign
gauge. The unnormalized representation retains the unresolved family; it
does not claim pair-only identifiability. Higher-order queries or additional
justified source structure are necessary for a sharp joint-task answer.

`DARK_INTERVENTION_ORDER.md` extends this to every finite simultaneous
intervention order and proves a complementary dimension-free finite-accuracy
boundary using a common Taylor polynomial and one-sided PSD remainders.

## 7. Coercive Hilbert-space extension

Let V be a real Hilbert energy space with a continuous symmetric coercive
bilinear form q0. More generally, use a densely defined closed coercive
quadratic form and its complete form domain with the energy norm. Let the
port ell and the finitely many intervention functionals v_i be bounded in
that energy norm, with ell nonzero. Define

    q_u(x,y)=q0(x,y)+sum_i u_i v_i(x)v_i(y).

Riesz/Lax-Milgram gives unique representers w and a_i satisfying
`q0(w,x)=ell(x)` and `q0(a_i,x)=v_i(x)`. Put

    z0=q0(w,w), h_i=q0(w,a_i),
    c0=1/z0, g_i=h_i/z0,
    B_ij=q0(a_i,a_j)-h_i h_j/z0.

The response is `z(u)=ell(w_u)`, where `q_u(w_u,x)=ell(x)`. The
constrained-energy proof applies in the complete form domain, giving exactly
(1). Only the finite span of the orthogonalized a_i participates in its
nonconstant part; the ambient state space may be infinite dimensional. Thus
(3)-(9) remain valid whenever their actual scalar/matrix bounds are warranted.

For example, bounds `z0>=z_min>0` and `||v_i||_(q0-dual)<=M` imply
`|g_i|<=M/sqrt(z_min)` and `B_ii<=M^2`. An operator coercivity lower bound
plus bounded functional norms can supply the latter dual bounds. A baseline
measurement interval can supply a finite positive z_min if its calibration
and conversion are justified. These are sufficient premises, not quantities
learned automatically by fitting finite data.

The extension does not apply to a resonance-frequency indefinite wave
operator merely because that system is passive, nor to unbounded point
evaluation functionals outside the form dual, nor to active/negative shunts.
For those cases an appropriate well-posed domain and resolvent contract must
be established separately. The original reciprocal wave receiver has not been
silently identified with this coercive Schur problem.

## 8. Executable scope

`unnormalized_representation_checks.py` compares (1) with exact inversion of
the canonical source, checks the uniform and gradient perturbation bounds on
rational PSD sources including singular/zero cases, and retains the dark
intervention example. These finite checks support their tested instances;
the general identities and dimension-free estimates rest on the proofs above.
