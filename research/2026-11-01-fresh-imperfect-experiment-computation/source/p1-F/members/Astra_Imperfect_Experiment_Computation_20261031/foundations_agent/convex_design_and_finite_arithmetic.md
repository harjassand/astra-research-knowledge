# A constructed downstream optimization task and an arithmetic-safe interface

Date: 2026-10-31. Complement to the root's live-source, reusable Galerkin
construction. This note uses its actual residual certificate as an interface;
it does not assume exact solves. The optimization method is ordinary
Frank-Wolfe, not a claimed new optimization algorithm. The useful conclusion is
that acquired operator actions can support a certified global design task with
an explicit planning algorithm and all experimental errors exposed.

## 1. Downstream problem

Let B_1,...,B_k be unknown Hermitian positive semidefinite matrices with known
bounds 0 <= B_j <= L_j I, and put L=max_j L_j. Let alpha>0, b in R^n or C^n,
and c in R^k be known. For theta in the probability simplex Delta_k define

    A(theta) = alpha I + sum_j theta_j B_j,
    F(theta) = c^T theta + b^* A(theta)^{-1} b.

The objective is real. The vector b may be real or complex. A(theta)>=alpha I
for every feasible theta, regardless of exact algebra dimension or commutation
relations. The task is to output a feasible theta and a rigorous bound on
F(theta)-min_Delta F. This is a consequential convex allocation/compliance
problem; it does not imply efficient arbitrary planning.

No B_j matrix, reduced basis or exact inverse is supplied. A call to the root's
constructed audited solver provides a finite vector x_tilde and a certified
absolute residual bound

    ||b-A(theta)x_tilde|| <= rho.

Its source experiments, unsuccessful corrections, cache precision and arithmetic
are charged there. Quadratic forms are computed from those same cached B_j
actions when available; otherwise their source actions must be charged here.

## 2. Convexity, gradient, and curvature

Write x=A(theta)^{-1}b. The variational identity

    b^*A^{-1}b = max_z [2 Re(b^*z)-z^*A z]

shows that F is convex: each expression inside the maximum is affine in theta.
Differentiation gives

    g_j(theta) = c_j - x^*B_j x.

For a simplex chord d=s-theta and D=sum_j d_j B_j,

    d^2/dt^2 F(theta+t d) = 2 (D x_t)^* A(theta+t d)^{-1} (D x_t) >=0.

Both sum_j s_j B_j and sum_j theta_j B_j lie between 0 and L I. Therefore
-L I<=D<=L I and ||D||<=L, not merely 2L. Also ||x_t||<=||b||/alpha. Thus

    d^2/dt^2 F(theta+t d) <= C,
    C := 2 L^2 ||b||^2 / alpha^3.                                      (1)

Consequently, for gamma in [0,1],

    F(theta+gamma d)
      <= F(theta)+gamma g(theta)^T d+(C/2)gamma^2.                       (2)

If L=0 or b=0 the nonlinear part is constant or zero; choosing a cheapest c_j
solves the design task without these experiments.

## 3. Gradient intervals earned from imperfect solves/actions

Let h=rho/alpha. Coercivity gives ||x-x_tilde||<=h. Suppose y_tilde_j is an
available approximate action on x_tilde with

    ||y_tilde_j-B_j x_tilde|| <= eta_j ||x_tilde||.

This may come from a cached action matrix with a certified operator error
eta_j, or from a fresh action. Columnwise errors alone do not establish this
matrix operator bound. If the cached coordinates are d and column error bounds
are epsilon_i, a directly valid alternative is

    ||y_tilde_j-B_j x_tilde|| <= sum_i |d_i| epsilon_i,

which is usable in the formula below without inventing an operator certificate.

Define

    qhat_j = Re(x_tilde^* y_tilde_j),
    ghat_j = c_j-qhat_j,
    delta_j = eta_j ||x_tilde||^2 + L_j h(2||x_tilde||+h).               (3)

Then |ghat_j-g_j|<=delta_j. Proof: the first term bounds the action error;
writing x=x_tilde+e with ||e||<=h bounds the quadratic difference by
2 L_j ||x_tilde||h+L_j h^2. Any certified dot-product rounding error is added
to delta_j. No statistical independence between x_tilde and the cached actions
is required on their simultaneous accuracy event.

The exact Frank-Wolfe gap is

    G(theta)=g(theta)^T theta-min_j g_j(theta).

Convexity gives F(theta)-F*<=G(theta). Therefore the entirely computed quantity

    U(theta)=sum_j theta_j(ghat_j+delta_j)
                         - min_j(ghat_j-delta_j)                       (4)

is a rigorous upper bound on global suboptimality. It may be clamped below by
zero. A simpler (possibly looser) version is

    U_simple=ghat^T theta-min_j ghat_j+2 delta,
    delta=max_j delta_j.                                               (5)

Stopping when U<=epsilon_design proves an epsilon_design-optimal design for the
true unknown matrices. This is a constructive global certificate, not a good
prediction of an objective and not a supplied planner.

## 4. Explicit algorithm and finite iteration bound

For each iterate theta_t:

1. Invoke the root's actual audited solver to get x_tilde and rho.
2. Obtain the cached or measured B_j x_tilde and compute certified intervals (3).
3. Refine the solve/action precision if needed until all delta_j<=delta_bar.
4. Compute U_t by (5); stop if U_t<=epsilon_design.
5. Let j_t be any index minimizing ghat_j (scan the k entries).
6. Set gamma_t=2/(t+2) and theta_{t+1}=(1-gamma_t)theta_t+gamma_t e_{j_t}.

The linear minimization operation in step 5 is explicit O(k) comparison work.
No optimization oracle is hidden in the construction. The initial theta_0 is
any simplex point. Assume a common certified bound delta_bar<=epsilon_design/16.

Let h_t=F(theta_t)-F*. Since a simplex chord has l1 norm at most two,

    g(theta_t)^T(e_{j_t}-theta_t) <= -G(theta_t)+2 delta_bar.

Using (2), G>=h_t and gamma_t=2/(t+2), induction gives, for t>=1,

    h_t <= 2 C/(t+2)+2 delta_bar.                                      (6)

The first step has gamma_0=1 and h_1<=C/2+2delta_bar, so no unknown initial
objective gap is needed in (6). Large linear costs c change the selected vertex
but not C.

For the computed certificate (5), the chosen direction also obeys

    g(theta_t)^T(e_{j_t}-theta_t) <= -U_t+4 delta_bar.

Sum the resulting descent inequality over t=m,...,2m-1. Put

    S=sum_{t=m}^{2m-1} gamma_t >= 2m/(2m+1) >= 2/3,
    Q=sum gamma_t^2 <= [2/(m+2)] S.

Then

    min_{m<=t<2m} U_t
      <= h_m/S+4 delta_bar+(C/2)Q/S
      <= 4 C/(m+2)+7 delta_bar.                                       (7)

Choose

    m=max(1, ceil(8 C/epsilon_design)).

The right side of (7) is at most 15 epsilon_design/16. Thus the algorithm must
encounter a valid stopping certificate in at most 2m audited iterates. This is
an O(C/epsilon_design) iteration bound using an explicit finite-dimensional
optimizer. If using the tighter interval certificate (4), stopping occurs no
later, since it is bounded above by (5).

For a finite number of future design tasks, the total number of audited linear
solve instances is the sum of these explicit caps. The root's cumulative
acquisition theorem can then bound shared refinements over all such instances.
The bound is conservative and is not evidence of a practical speedup.

## 5. Choosing source and solve tolerances without knowing x

If the root solver certifies a relative residual

    ||b-A x_tilde|| <= tau ||x_tilde||,       tau<=alpha/2,

then ||x_tilde||<=2||b||/alpha and h<=tau||x_tilde||/alpha. If all action errors
are bounded by eta, (3) yields

    delta_j <= 4 eta ||b||^2/alpha^2
                          +10 L tau ||b||^2/alpha^3.                   (8)

Thus it is sufficient, when L>0 and b!=0, to request

    eta <= delta_bar alpha^2/(8||b||^2),
    tau <= min(alpha/2, delta_bar alpha^3/(20 L ||b||^2)).               (9)

These conditions expose the physical/numerical conditioning cost. They cannot
be replaced by uncharged small residuals. If the root cache uses eta=tau/16,
an equally explicit sufficient choice follows from

    delta_j <= tau||b||^2[1/(4alpha^2)+10L/alpha^3].                    (10)

An implementation may use actual x_tilde norms in (3) to avoid this worst-case
over-resolution. Every refinement and its source price remains charged.

## 6. Objective value interval, if desired

For any x_tilde, let r=b-A x_tilde and

    V=2 Re(b^*x_tilde)-x_tilde^*A x_tilde.

The exact identity

    b^*A^{-1}b-V=r^*A^{-1}r

gives V<=b^*A^{-1}b<=V+rho^2/alpha. If an approximate A action makes Vhat have
certified error e_V, a valid objective interval is

    [c^Ttheta+Vhat-e_V,
     c^Ttheta+Vhat+e_V+rho^2/alpha].                                    (11)

This retains the quadratic residual benefit. Any finite arithmetic enclosure
for scalar products is added to e_V. The gap certificate (4) does not require
an exact objective evaluation.

## 7. A finite-arithmetic-safe specification for the root solver

This subsection is an implementation contract with explicit margins. It is
not a formal Turing-model complexity theorem or a tested interval solver.
Ordinary floating-point experiments alone do not establish the contract.

### 7.1 Avoid normalizing numerically insignificant task directions

Let U be the retained basis and P_U its orthogonal projector. Set

    b_perp=(I-P_U)b.

Include b_perp/||b_perp|| in the current Galerkin space only if its norm is
certifiably greater than beta||b||. Otherwise omit it, with

    beta <= min(1/2, tau/[16(M_A+sigma)]),                              (12)

where M_A is an admitted upper bound on ||A|| and sigma bounds the current
cached action-matrix error. Suppose the exact Galerkin equation for the
projected right-hand side is H z=V^*b, ||H||<=M_A+sigma, and V contains U.
When b_perp is omitted,

    ||P_U b|| >= sqrt(1-beta^2)||b||,
    ||x|| >= ||P_U b||/(M_A+sigma).

Therefore

    ||b_perp||/||x||
       <= beta(M_A+sigma)/sqrt(1-beta^2) <= tau/8.                      (13)

The last inequality follows from beta<=1/2 and (12). Thus omission has an
explicit residual budget; no useful direction is silently discarded. The zero
right-hand side is returned as zero without normalization.

If the root's source/cached error is sigma=tau/16 and its residual acceptance
test includes that error, a rejected candidate still has a nontrivial outside
component of its raw normalized action. In the exact-arithmetic derivation the
available margin is at least 3tau/4 after the omitted-b contribution, as root
specified. Set the insertion threshold to g=tau/2, leaving tau/4 for certified
projection, scalar-product, solve and normalization rounding. The insertion
test should use this gap, not equality at a single threshold.

### 7.2 Keep a certified well-conditioned coordinate system

A finite stored matrix U need not be exactly orthonormal. One implementable
invariant is

    ||U^*U-I|| <= chi,       chi<=1/4.                                 (14)

The Frobenius norm supplies a computable conservative upper bound on the
operator norm. Use the actual projector U(U^*U)^{-1}U^*, with verified linear
solves, rather than silently treating a nonorthogonal U as orthogonal. Its Gram
matrix has spectrum in [3/4,5/4], so this operation has no hidden singular gap.
If needed, recondition U with a certified approximation to (U^*U)^{-1/2}; the
spectrum already lies in a compact interval away from zero. Recheck (14).

The reduced Galerkin matrix has an inherited positive lower bound. For an
exactly orthonormal V and action error sigma,

    lambda_min(H)>=mu-sigma.

For (14), use the corresponding generalized/actual Gram factors and reserve
rounding so the verified reduced matrix remains >=mu/2 in coordinate norm.
Its conditioning is controlled by admitted mu, M_A and chi, rather than an
unknown algebraic eigengap. Check the linear-solve residual with outward error
bounds; increase precision until it fits its allocated residual budget.

### 7.3 Use interval margins and a finite call horizon

Every norm, inner product, projector, reduced solve and acceptance comparison
can be accompanied by an outward error enclosure. The root's thresholds have
strict slack: retain/omit b with a two-threshold guard inside the budget (13),
accept a solve only when its upper residual bound meets the target, and insert
a raw action only when its lower orthogonal-distance bound exceeds g. If a
comparison is uncertain, increase arithmetic precision; if it remains inside
the guard interval, either permitted branch must satisfy the same budget.
This avoids infinite refinement at exact threshold equality.

All divisions used to form a new retained direction have a certified denominator
at least g (or beta||b|| for a deliberately included task direction). Reduced
linear solves have a certified lower spectral bound. Standard stable algorithms
therefore need precision set by n, the finite retained dimension R, admitted
norm bounds, mu, g, beta, residual budgets and input dynamic range. They do not
need to resolve a hidden exact-algebra eigengap. A rough logarithmic dependence
of working precision on reciprocals of these positive margins is plausible,
but an exact bit-complexity statement requires specifying the source's finite
bit encoding and proving an end-to-end rounding construction. This note does
not claim that missing theorem.

For a fixed finite collection of tasks, maintain a finite operation/error
ledger and allocate rounding error within the available slack. This establishes
a reproducible finite-arithmetic specification once implemented with certified
linear algebra. A double-precision prototype can illustrate behavior but is
not the specification's proof.

## 8. Probability and adaptivity

If the source provides deterministic norm guarantees, all preceding results
are deterministic and need no fresh independence assumption. If an experiment
at call ell supplies its requested bound only with conditional failure
probability delta_ell, choose a finite-budget allocation or the summable rule

    delta_ell=6 delta_total/(pi^2 ell^2).

The conditional guarantees, even under adaptive query/precision selection,
then imply one simultaneous event of probability at least 1-delta_total by the
union bound. Every reuse and adaptive downstream optimization is valid on that
event. Source cost must include the actual dependence on delta_ell; it cannot
be removed by treating repeated uses of a cached estimate as fresh evidence.
Unknown or uncontrolled systematic bias is not covered by an averaging claim.

## 9. Established components and scope of contribution

The convexity and compliance gradient are standard matrix-fractional convexity.
Frank-Wolfe on a simplex and its O(1/t) curvature analysis are established:

- Martin Jaggi, *Revisiting Frank-Wolfe: Projection-Free Sparse Convex
  Optimization*, ICML 2013, PMLR 28(1):427-435.
  https://proceedings.mlr.press/v28/jaggi13.html

Greedy reduced spaces and width/determinant arguments are also established:

- Peter Binev, Albert Cohen, Wolfgang Dahmen, Ronald DeVore, Guergana Petrova,
  Przemyslaw Wojtaszczyk, *Convergence Rates for Greedy Algorithms in Reduced
  Basis Methods*, SIAM J. Math. Anal. 43(3):1457-1472, 2011.
  https://www.igpm.rwth-aachen.de/Download/reports/pdf/IGPM310.pdf
  https://doi.org/10.1137/100795772

What the joint construction can earn is a complete noisy experimental path from
operator actions to a reusable cache, actual audited solves, and a globally
certified downstream optimization task, with the cumulative cache cost shared
across its iterates. It is not a new generic optimizer, a generic planning
theorem, or evidence of superiority over strong recycling/reduced-basis methods.
