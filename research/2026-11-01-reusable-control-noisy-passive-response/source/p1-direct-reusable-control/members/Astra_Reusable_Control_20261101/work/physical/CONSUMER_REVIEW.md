# Review of the later constrained-control consumer

1 November 2026. Complementary mathematical check of the construction proposed
by the root investigator. This checks the stated finite optimization mechanism;
it is not a review of arbitrary hardware or a claim of optimal oracle complexity.

## Contract

Let the normalized physical response on the full simplex
X={x>=0,sum x_i<=1} be

    f(x)=min_z [ ||z||^2 + sum_i x_i(h_i-b_i^T z)^2 ],
    |h_i|<=1, ||b_i||^2<=q.

The previously acquired record supplies a deterministic function hatf with
sup_X |hatf-f|<=zeta on its simultaneous interval event. Such a hatf can be
one rational feasible pair, using its certified whole-law radius, or the
midpoint of querywise LP intervals. The former needs one fit and subsequent
polynomial evaluations; the latter pays two LP optimizations per value query.
Neither requires a new physical experiment after acquisition.

After seeing the record, a user may choose a nonempty compact convex C subset X,
a known linear price c, a feasible starting point x0 in C, and a linear
optimization oracle over C. The target is max_{x in C} f(x)-c^T x. All costs of
the supplied linear oracle and deployment are charged separately. No nonconvex
feasible set, unknown membership oracle, or physical command implementation is
implicitly supplied.

## Curvature

For the minimizer z_x, ||z_x||^2<=f(x)<=sum x_i h_i^2<=1. Put
v_i=h_i-b_i^T z_x and A=I+sum_i x_i b_i b_i^T. The envelope and derivative
identities are

    partial_i f=v_i^2,
    partial_ij f=-2v_i v_j b_i^T A^(-1)b_j.

Therefore |v_i|<=1+sqrt(q) and every Hessian entry has absolute value at most
beta=2q(1+sqrt(q))^2. For any two points x,v in X, ||v-x||_1<=2, hence

    |(v-x)^T Hess f(y)(v-x)|<=Cq:=8q(1+sqrt(q))^2

along the entire segment. In particular

    f(x+gamma(v-x)) >= f(x)+gamma grad f(x).(v-x)-Cq gamma^2/2.

The inverse A>=I remains regular at boundary points, so no interiority or
eigenvalue-gap assumption is needed.

## Approximate directional oracle from the same record

Let v0=0,v1=e1,...,vn=en denote the full-simplex vertices. At iterate x in C and
step h in (0,1], compute

    s_i=[hatf(x+h(v_i-x))-hatf(x)]/h.

Concavity plus the curvature bound gives

    s_i-grad f(x).(v_i-x) in [-Cq h/2-2zeta/h, 2zeta/h].

Any v in X is a convex combination of these n+1 vertices. Averaging the
estimates with its barycentric weights retains exactly the same error interval.
Maximizing the resulting affine score minus c^T(v-x) over C uses one linear
optimization call: the i-th coefficient of its nonconstant part is
s_i-s_0-c_i. Thus the selected v_t satisfies

    grad(f-c^T x)(x).(v_t-x)
      >= max_{v in C} grad(f-c^T x)(x).(v-x)-nu,
    nu=Cq h/2+4zeta/h.

The trial points may lie outside C but remain inside X. This is legitimate
because the acquired law is certified on the full simplex, and these are
offline evaluations. A record certified only on C would not automatically
supply them. An approximate linear oracle with additive score error chi adds
chi to nu.

## Iterations and regret

Set gamma_t=2/(t+2) for t=0,1,2,... and update

    x_(t+1)=x_t+gamma_t(v_t-x_t).

Convexity of C keeps the iterate feasible. If g_t is the true optimum gap,
concavity gives

    g_(t+1) <= (1-gamma_t)g_t+gamma_t nu+Cq gamma_t^2/2.

The first gamma_0=1 removes dependence on the initial gap and on the magnitude
of the known linear price: g_1<=nu+Cq/2. Induction yields for t>=1

    g_t <= nu+2Cq/(t+2).

For a target normalized regret epsilon and Cq>0 choose

    h=min(1,epsilon/(2Cq)),
    zeta<=epsilon*h/16,
    T=max(1,ceil(4Cq/epsilon)).

Then nu<=epsilon/2 and g_T<=epsilon. Each iteration requires at most n+2
evaluations of hatf and one linear optimization call. Therefore one sufficient
offline budget is (n+2)T value evaluations plus T linear-oracle calls. Multiply
the final response and price units by the original scale L as needed.

When q=0, f is affine. Its slopes are f(e_i), since f(0)=0 exactly. One linear
optimization using approximated vertex slopes with absolute error zeta gives
regret at most 2zeta; no finite-difference limit or division by curvature is
needed.

## Assessment

The consumer is sound with the explicit contract above. It closes a real
planning step: a single noisy experimental record supports later choices of
convex budgets, linear prices, and constraints without additional physical
experiments. The norming/acquisition theorem, not fitting quality alone, makes
adaptive reuse legitimate.

Frank-Wolfe optimization and finite-difference approximate oracles are ordinary
methods. The O(zeta^(-1/2)) noise-to-regret relation and the stated evaluation
cost are sufficient bounds for this elementary consumer, not optimal lower
bounds. Other equally informed convex optimization methods may improve the
costs. The rational fitted function itself need not be concave; the proof uses
concavity of the warranted physical source and uniform approximation error,
which is the correct distinction.
