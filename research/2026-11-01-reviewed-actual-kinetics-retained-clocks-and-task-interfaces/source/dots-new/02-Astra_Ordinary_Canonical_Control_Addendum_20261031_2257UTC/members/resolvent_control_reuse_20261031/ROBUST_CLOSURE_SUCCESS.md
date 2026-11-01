# Primary strengthening: acquired approximate closure earns a small ordinary LP

NEW unreviewed strengthening of PROOF.md. This result does NOT require the
unknown process to have any exact low-dimensional closure. Its premises are
finite-observation confidence inequalities already constructed in that proof.
No generic nonlinear-equilibrium oracle, R inverse, supplied stability norm,
or topological existence theorem is needed for the primary consumer.

Use H=(1-gamma)(I-gamma A0)^(-1)Z, t=gamma/(1-gamma), and the received event

 ||(A_a-A0)H-ZBhat_a||_(infinity->infinity)<=eta,
 ||hhat-h||_1<=delta_h,   h=mu H,   mu=(1/r)1^T W.

Bhat_0=0 and Bhat_a1=0. The actually acquired objective satisfies
hhat_j>=(1-gamma)/r>0 and hhat1=1. Define

 kappa=(1-gamma)/(1+gamma),  q=t eta,  d=kappa-q.

## 1. Stability geometry earned from stochasticity

For all x,

 (1-gamma)||x||_infinity
  =||(I-gamma A0)Hx||_infinity
  <=(1+gamma)||Hx||_infinity.

Thus ||Hx||_infinity>=kappa||x||_infinity. This is not a singular-value assumption
and remains true when R=WH is singular.

For ANY randomized block selector pi, let A_pi be its stochastic selected
transition matrix, Bhat_pi the same convex row selector, and
E_pi=(A_pi-A0)H-ZBhat_pi, so ||E_pi||_infinity<=eta. Put M_pi=I-tBhat_pi.
The identity

 (I-gamma A_pi)H=(1-gamma)Z M_pi-gamma E_pi

together with ||(I-gamma A_pi)v||>=(1-gamma)||v|| gives

              ||M_pi x||_infinity>=d||x||_infinity.    (1)

Consequently if d>0 every such M_pi is invertible and ||M_pi^-1||_infinity<=1/d.
The selector ranges over ALL rowwise randomized block policies; no exponential
enumeration or inheritance of a common reduced contraction is used.

## 2. An acquired positive LP-objective margin

Let G_pi=(I-gamma A_pi)^(-1). With the sign fixed by the definition of E_pi,

 H M_pi^-1=(1-gamma)G_pi Z-gamma G_pi E_pi M_pi^-1.       (2)

G_pi>=I entrywise, ||mu G_pi||_1=1/(1-gamma), and mu Z=(1/r)1^T. Therefore,
componentwise,

 hhat M_pi^-1
 >=[(1-gamma)/r-(q+delta_h)/d]1^T.                     (3)

Indeed the correction in h M_pi^-1 has row L1 norm at most q/d, and replacing h
by hhat contributes at most delta_h/d. No inverse of R is taken. Define the
COMPUTABLE margin

                    z=(1-gamma)/r-(q+delta_h)/d.

Require d>0 and z>0. These inequalities concern received error bounds, not an
asserted exact equality of the unknown source.

## 3. Ordinary finite LP constructs the nominal root

For any later g in [0,1]^r, solve

 minimize hhat w,
 w_j >= g_j+t[Bhat_a w]_j    for every j,a.             (4)

This r-variable mr-constraint rational LP is always feasible: w=1 works because
Bhat_a1=0 and g<=1. Its baseline constraints imply w>=g>=0. Positive hhat makes
objective sublevels bounded, so a finite optimum exists. Standard finite LP
strong duality applies; no hypothetical efficient root teacher is introduced.

Let lambda_ja>=0 be an optimal dual multiplier for constraint (j,a), and set
nu_j=sum_a lambda_ja. When nu_j>0 choose pi(a|j)=lambda_ja/nu_j; when nu_j=0
choose an arbitrary distribution. Dual stationarity is EXACTLY

                    hhat=nu^T M_pi.

By (1),(3), nu^T=hhat M_pi^-1>=z1^T, hence every nu_j>0 after all. Complementary
slackness then gives at least one active action constraint in every block.
Since all action constraints are satisfied, their maximum is active:

                   w_j=g_j+t max_a[Bhat_a w]_j.        (5)

This proves constructive existence through an ordinary small LP. It avoids the
incorrect inference that a generic piecewise-linear homeomorphism automatically
has a cheap solver. The positive objective-row margin is the extra structure.

For uniqueness, the difference of maxima between any w,v is a convex combination
of their action-row slopes, separately in each block. Thus the difference of
f(w)=w-t max_a Bhat_a w equals M_pi(w-v) for some randomized selector. Inequality
(1) yields ||f(w)-f(v)||>=d||w-v||. The root in (5) is unique, and since f(0)=0,

                         ||w||_infinity<=1/d.          (6)

The prototype uses y=w-g to match PROOF.md. A checked dual's grouped nu_j are
recorded explicitly, and the zero nominal residual is recomputed. Exact primal/
dual conditions protect against solver errors. Ordinary rational LP theory
supplies polynomial bit complexity; the implemented simplex backend's actual
work is charged, with no polynomial worst-case claim for simplex.

## 4. Uniform near-optimal control without an exact closure promise

Choose a nominal maximizing action in each block. Equation (5) makes rho=0 in
the universal posterior receiver, so the true policy's normalized pointwise
regret is at most

                            2q/d.                     (7)

This holds against optimal microscopic/history control in the actual fully
observed discounted MDP, despite the output policy using only the acquired block.
It follows from the two ORIGINAL-process Bellman contraction bounds, not a
stochastic interpretation of Bhat or a Markov law on the blocks.

If z>0 and 2q/d<=e_req, the retained certificate admits EVERY g in [0,1]^r on the
same acquired confidence event, including an adaptive sequence of future goals.
No per-goal statistical union or new source calls are needed. LP execution,
coefficient reading, exact checking, table output, retained map and actual
sensor/source execution still cost. Failed acquisition/refinement attempts and
independent full re-audits remain paid.

If the scalar admission fails, no all-goal guarantee is earned. A candidate from
the older robust LP or another ordinary method may still pass the more flexible
posterior certificate. It must pay its measured rho and ||w||; no failed admission
is converted into a proof that no useful low-dimensional control knowledge exists.

## 5. Explicit finite acquisition success condition

The fixed-design truncated-geometric endpoint receiver in PROOF.md directly
supplies eta and delta_h. On a true exact-closure success class it has eta<=6eps,
delta_h<=gamma eps, and one convenient sufficient precision is

 eps <= min{(1-gamma)^3/[28r gamma(1+gamma)],
             e_req(1-gamma)^2/[24gamma(1+gamma)]}.

Then q+delta_h<=7gamma eps/(1-gamma)<=kappa(1-gamma)/(4r), which also implies
q<kappa/2. Hence z>=(1-gamma)/(2r)>0 and
2q/d<=4q/kappa<=24gamma eps(1+gamma)/(1-gamma)^2<=e_req.
The earlier cap/root-bit/N construction gives an explicit finite schedule.
For approximate classes, admission depends on the actually measured limiting
defect and may succeed without any exactly closed nearby process. The schedule
is sufficient, conservative and possibly prohibitive; it is not a lower bound.

## 6. Scope and relation to the earlier route

This is the primary all-source, acquired-error success theorem. The older
exact-class robust LP proof remains valid but conditional on that class. A
historical exploratory draft used a topological root existence argument and a
looser robust-LP fallback; it is preserved separately and is not needed here.
The initially written plus sign in an intermediate identity was corrected to
the minus sign in (2) before this proof/code freeze. Absolute margin constants
are unaffected; the corrected orientation is the one used throughout.

The result does not invent successor features, ALP, constraint aggregation or
Bellman residual theory. The candidate contribution is the concrete acquisition,
refinement, earned stability/objective margins and efficient many-goal join in a
class where predictive aggregation can fail. Historical originality and an
important economical workload remain unestablished. Strong retaining ordinary
methods receive the same source metadata and can use the same certificate.

## 7. Same acquired core also admits action-dependent reward/cost goals

The primary LP does not actually need a common reward across actions. For any
later table g_a in [0,1]^r, use actual reward Zg_a when action a is taken and solve

 minimize hhat w,       w_j>=g_a[j]+t[Bhat_a w]_j.

The SAME acquired margin, endpoint data and policy map apply. Feasibility w=1,
nonnegativity from the baseline constraint w>=g_0, compactness, dual grouping
and complementarity are unchanged. At the root, an active selector pi gives
M_pi w=g_pi, so (1) implies ||w||<=1/d. The nominal maximizing policy now uses
g_a+tBhat_a w. Its two actual Bellman residuals are at most gamma eta||w||, hence
regret is again <=2q/d, uniformly over all future mr-entry bounded reward tables.

For a non-root candidate define rho=max_j |w_j-max_a(g_a[j]+t[Bhat_a w]_j)|;
the general posterior bound is 2(rho+q||w||). This admits changing action prices
as well as state goals without relearning dynamics. Initial native features may
include action-specific task features; the starting partition groups states
with identical full native feature tuples. This is an explicit extension of the
common-reward fixture, not a claim that arbitrary microscopic rewards or an
unbounded new reward scale are covered. The additional task input costs mr
entries. Ordinary ALP/SF methods receive the same extension and information.
