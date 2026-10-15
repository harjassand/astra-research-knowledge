# An exact decision formulation without a polynomial-lift restriction

This note does not solve the full heat-plus-polyconvex inclusion. It gives an
exact quantified formulation, so that a restricted SOS failure is not
silently identified with failure of true polyconvexity.

The support characterization below is already Proposition 2.3 of
[Fantuzzi et al., v1](https://arxiv.org/html/2604.11124v1), credited there to
Dacorogna's Theorem 5.6. Formula (1) is its differentiable planar elimination.
The quantified formulation is a standard real-algebraic corollary; no novelty
is claimed for either ingredient.

## 1. An unrestricted support test

For any continuously differentiable finite function `P:R^(2x2)->R`, P is
polyconvex if and only if

\[
 \boxed{\forall A\ \exists\lambda\in\mathbb R\ \forall H:
 P(A+H)-P(A)-DP(A):H-\lambda\det H\ge0.}               \tag{1}
\]

**Proof.** If `P(A)=g(A,det A)` with g convex, g is finite throughout R5.
Indeed, every point `(A,z)` is the midpoint of two graph points: use
`A+/-tI` for `z>=det A`, and `A+/-t diag(1,-1)` for `z<=det A`, with
`t^2=|z-det A|`. Convexity bounds g above there by finite graph values.
Thus g has a supporting affine function at every graph point. If its
support coefficients are `(p,lambda)`, differentiating on the graph gives
`DP(A)=p+lambda cof A`. The identity

\[
 \det(A+H)-\det A-(\operatorname{cof}A):H=\det H
\]

turns that support into (1).

Conversely, choose one lambda(A) for every A satisfying (1), and take the
supremum of their affine functions on `(Y,z)`, with coefficients
`p(A)=DP(A)-lambda(A)cof A`. This is convex. Every such function lies below
P on the determinant graph, and the support indexed by A=Y attains P(Y).
Hence its supremum is a convex lift of P. The same midpoint argument makes
the lift finite everywhere. QED.

For a homogeneous quartic, (1) is a first-order polynomial statement with
four universally quantified A coordinates, one existential scalar lambda,
and four universally quantified H coordinates. It makes no assumption that
the convex lift itself is polynomial or that any support remainder is SOS.
This is the usual supporting-plane geometry of polyconvexity specialized
and explicitly eliminated to the planar determinant; novelty is not claimed.

## 2. Full cone inclusion as a real-algebraic sentence

Let `ROC(p)` denote the exact lift in `ROC_CLASSIFIER.md`. Let
`Heat(h,D,Q,omega)` mean:

* D is a real symmetric positive definite 2 by 2 scalar input metric;
* Q is a symmetric positive semidefinite 24 by 24 matrix;
* omega has 60 homogeneous-quadratic two-form coefficients and satisfies
  the linear closedness equations;
* for every compatible jet, the polynomial identity
  `Z^T Q Z = sum D_ik D2H(A)[B_i,B_k]+omega_A(B1,B2)` holds.

Polynomial coefficient comparison makes the last item a finite list of
polynomial equalities in h,D,Q,omega; PSD can be expressed by principal
minors. Let `PC(p-h)` be the unrestricted formula (1). Then the precise
single-component universality question is

\[
 \forall p\in\mathbb R^9:\quad
 ROC(p)\Longrightarrow
 \exists h,D,Q,\omega\;[Heat(h,D,Q,\omega)\land PC(p-h)]. \tag{2}
\]

This is a first-order sentence over a real closed field and is decidable by
quantifier elimination. Individual membership in the sum class is likewise
decidable for specified algebraic coefficients. This is an in-principle
algorithmic classification, not a practical complexity guarantee. No such
quantifier-elimination calculation was executed here.

If the intended heat class instead allows a positive sum of components with
different metrics, state that class separately. In the finite-dimensional
coefficient space, a point of the conic hull of admissible heat components
needs at most nine components by conic Carathéodory. A positive scalar can be
absorbed into a component. Consequently replacing the one Heat clause by at
most nine Heat clauses also has an exact finite quantified formulation.
Closure of that conic hull is a separate operation; a limit-only
representation must not be silently treated as an attained finite sum.

This avoids the known issue that polynomial polyconvexity need not be
captured by an arbitrarily chosen convex polynomial-lift ansatz. Relevant
primary work is [Fantuzzi et al. (2026)](https://arxiv.org/abs/2604.11124).
Its Proposition 2.4 gives a quartic without a convex polynomial lift. This
must be distinguished from SOS support certificates: Remark 2.1 leaves open
whether every planar polyconvex quartic is SOS polyconvex.

## 3. What the sharp section contributes

The exact `12+8sqrt(3)` section calibrates the Heat clause: F25 passes with a
rational certificate, F26 fails for every positive constant input metric and
every closed quadratic form, and both pass PC by an explicit lift. Thus
neither F26 nor the inherited heat-increase polyconvex example can separate
the sum in (2).

An actual separation of (2) needs either an exact certificate of
non-membership in this unrestricted sum or a constructive theorem proving
inclusion. Failure of a fixed metric, a finite SDP, a chosen polyconvex
module, or a restricted polynomial lift is insufficient. An actual negative
compatible gradient would be required for a non-QC conclusion.
