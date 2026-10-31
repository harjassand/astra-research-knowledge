# From an acquired response law to later certified control

1 November 2026. Root construction, with a separate mathematical challenge in
`../physical/CONSUMER_REVIEW.md`. All prior Astra premises are pinned to
`51ce47ce39f976517d60e2f87bbe280b651f6056`.

## 1. Physical and information contract

Normalize the admitted fixed response to

    f(x)=h^T P(I+PCP)^(-1)Ph,
    P=diag(sqrt(x)), C>=0, C_ii<=q, |h_i|<=1,
    X={x>=0: sum x_i<=1}.

Its underlying physical gain is F(u)=L f(u/delta), L=delta G^2,
q=delta kappa. A single calibration event supplies an acquired rational
function hatf or the LP interval service with sup_X|hatf-f|<=zeta. Any one
feasible fitted ratio satisfies this when the whole-interval width is <=zeta.
Future commands, prices and constraint sets may be selected after the record.
This is static control of the same fixed source, with the same admissible dose
language. It is not a theorem for unknown evolving dynamics or new actuators.

The later task is to maximize f(x)-c.x over a supplied nonempty compact convex
set K contained in X. The price c is known. K comes with a feasible starting
point and an actual finite-cost linear optimization oracle. No arbitrary
nonconvex planner is assumed. Outputs are an intervention and a regret bound.

## 2. Concavity and curvature belong to the real source

Choose Gram vectors b_i with C_ij=b_i.b_j. They are proof objects, not acquired
data. Woodbury gives

    f(x)=min_z [||z||^2 + sum_i x_i(h_i-b_i.z)^2].        (1)

As the infimum of affine functions of x, f is concave. The minimizing z is
unique because its Hessian in z is positive definite. Put

    A_x=I+sum_i x_i b_i b_i^T, z_x=A_x^(-1)sum_i x_i h_i b_i,
    v_i=h_i-b_i.z_x.

The envelope derivative and its Hessian are

    partial_i f=v_i^2,
    partial_ij f=-2 v_i v_j b_i^T A_x^(-1)b_j.           (2)

Taking z=0 in (1) shows f<=sum x_i h_i^2<=1. Hence ||z_x||<=1,
|v_i|<=1+sqrt(q), and A_x>=I gives

    |partial_ij f|<=2q(1+sqrt(q))^2.                   (3)

Every difference between two points of X has l1 norm <=2. Therefore along
every segment from x to y in X the absolute second derivative is at most

    Ccurv=8q(1+sqrt(q))^2.                            (4)

These bounds include singular C and all dark couplings. The coefficients of
an LP-feasible rational fit need not define a concave function. Only f is
used in (1)--(4).

## 3. A fully charged offline Frank-Wolfe consumer

The simplex vertices are v_0=0,v_i=e_i for i=1,...,n. For step h in (0,1],
at current x in K evaluate the acquired record at x and at
x+h(v_i-x). Set

    a_hat_i=[hatf(x+h(v_i-x))-hatf(x)]/h-c.(v_i-x).

The true directional derivative a_i=(grad f(x)-c).(v_i-x) satisfies

    a_hat_i-a_i in [-Ccurv h/2-2zeta/h, 2zeta/h].     (5)

For every y in X, use its barycentric coordinates lambda_i(y), including the
slack coordinate lambda_0=1-sum y_i. Both true and fitted directional scores
at y are their respective barycentric averages. Use the supplied linear
optimization oracle over K to maximize sum lambda_i(y)a_hat_i, and call the
returned point y_t. Equation (5) implies

    (grad f(x)-c).(y_t-x)
      >= max_y_in_K (grad f(x)-c).(y-x)-nu,
    nu=Ccurv h/2+4zeta/h.                            (6)

The evaluations in (5) may leave the later K, but remain inside the full
simplex X covered by the same retained record. They cost computation, not
new source experiments.

Update x_(t+1)=x_t+gamma_t(y_t-x_t), gamma_t=2/(t+2), t=0,1,... .
Concavity bounds the objective gap by the maximal directional derivative,
and (4) supplies the usual quadratic step loss. Thus

    gap_(t+1) <= (1-gamma_t)gap_t+gamma_t nu+Ccurv gamma_t^2/2.

The first gamma_0=1 removes the initial gap, including any large linear price.
Induction gives for every t>=1

    gap_t<=nu+2Ccurv/(t+2).                           (7)

For q>0 and desired normalized regret epsilon>0, choose

    h=min(1,epsilon/(2Ccurv)), zeta<=epsilon*h/16,
    T=max(1,ceil(4Ccurv/epsilon)).                    (8)

Then nu<=epsilon/2 and (7) gives gap_T<=epsilon. The bill is at most
(n+2)T acquired-value evaluations and T linear-optimization calls. Evaluation
of one retained ratio uses its explicit monomial storage; computing tight
interval endpoints uses two ordinary linear-fractional LPs. Finite solver
errors must be included in zeta and any approximate linear-oracle error in nu.
This elementary sufficient algorithm is not an optimal convex-optimization
complexity claim.

When q=0, f is affine. Evaluate its vertex values and perform one linear
optimization. An arbitrary uniformly zeta-accurate vertex predictor gives
regret<=2zeta. This avoids division by Ccurv=0.

## 4. Stronger a posteriori certificates at full retained degree

For r=n, no rational truncation remainder is present. Let P be the positive
coefficient polytope from the acquisition theorem. For a proposed rational x,
obtain source-valid f_lower<=f(x)<=f_upper by linear-fractional LP. Since all
denominator coefficients are nonnegative, D_i(x)>=0. The exact derivative
formula supplies

    [N_i-f_upper D_i]/D <= partial_i f
                                  <=[N_i-f_lower D_i]/D.             (9)

Minimize the left and maximize the right over the same P. Each is a
linear-fractional objective in the unknown coefficients and so has a standard
LP transform. Monotonicity of the actual source permits clipping the lower
bound to zero. Denote the resulting vector intervals by g_lower,g_upper.

For any proposed x in K, true concavity gives

    max_y_in_K [f(y)-c.y] - [f(x)-c.x]
      <= max_y_in_K (g_upper-c).y-(g_lower-c).x.       (10)

All coordinates of x,y are nonnegative. This proves (10) even if the fit is
nonphysical or nonconcave, or the proposing optimizer found a local optimum.
An arbitrary proposer is allowed; acceptance depends on (10).

For box-constrained simplexes the linear maximization in (10) is exact greedy
allocation after sorting coefficients. For other K use its paid oracle.
For r<n, (9) cannot simply differentiate the value tail. Use the uniform-value
consumer above or acquire a separate valid derivative-remainder bound.

## 5. Exact numerical certification without trusting floating stationarity

For a ratio with D(x)=1+m(x).d, use t=1/D(x), z=t theta. The transformed
data constraints are linear, t+m.d_z=1, 0<=t<=1, and
0<=z_j<=U_j t<=U_j. Here U are the finite coefficient boxes.

For a linear objective c.z with constraints A z<=0 and e.z=1, take ANY
nonnegative rational lambda and any rational nu, and define
r=c-A^T lambda-nu e. Then

    c.z <= nu + sum_j max(r_j,0) U_j.                 (11)

The t coordinate has U_t=1. Equation (11) is an ordinary weak-duality proof
with an explicit finite-box repair. Numerical duals only propose lambda,nu;
their exact rational nonnegativity, residual and bound are checked. No exact
floating optimality or stationarity is assumed. Saved duals and scalar
records are sufficient to replay every demonstration certificate without
loading the source matrix, generating code or true objective.

## 6. How intervals can actually be acquired under a sensor model

The deterministic theorem requires correct simultaneous intervals. One
supplier is a calibrated report of known absolute error. Another is a
bounded, conditionally unbiased sensor of range width W. With independent
trials, or a valid bounded martingale-difference version, N repeats at each
of M commands give simultaneous raw mean error at most a with failure alpha
when N>=W^2 log(2M/alpha)/(2a^2).

For gain tasks, acquire the actual zero-dose reading R(0), rather than assuming
unknown offsets are individually known. Set y_i=[Rhat(u_i)-Rhat(0)]/L.
Raw error a=L xi/2 on each mean gives gain radius xi, including the shared
baseline error. Thus a sufficient number of repeats per setting is

    N>=2 W^2 log(2M/alpha)/(L^2 xi^2).                (12)

The zero command is one of the M settings. Source calls cost MN. Repetition
does not remove an unknown fixed sensor bias, drift, actuation error or
settling error. Those need independent caps and consume the same xi budget.
For general admitted sources, an l1 dose error eps_u with nominal and actual
commands inside the simplex contributes at most
G^2(1+sqrt(q))^2 eps_u to F error. For the unit-voltage passive resistor
subclass, the envelope derivative is an actual squared voltage drop <=1,
so eps_u is a valid bound in physical response units. These are consequences
of (2), not free metrological capabilities.

## 7. Near-parametric accuracy lower bound, separated from control geometry

Already n=1,B=0 admits f_a(x)=a x, 0<=a<=1. With adversarial absolute
error eta, two slopes separated by 2eta admit identical midpoint reports at
every command. Uniform error below eta is impossible.

For a statistical supplier, let Z=4(Bernoulli(1/2+a x/4)-1/2), so E Z=a x
and the report range width is4. Compare a_+=1/2+2epsilon and
a_-=1/2-2epsilon, 0<epsilon<=1/4. The Bernoulli KL per arbitrary adaptive
query is at most (16/3)epsilon^2. Uniform error <=epsilon on each source
allows a test with the same failure alpha because their endpoint values are
separated by4epsilon. The chain rule and two-point testing inequality give

    T >= [3/(16epsilon^2)] log[1/(4alpha)].            (13)

This is a worst-case noise-model lower bound, not a lower bound for noiseless
or calibrated analog measurements. It does not remove the separate
binomial(n+k,k) settings, storage, precision or experiment-order costs.

## 8. Executed examples and the retained miss

`control_demo.py` builds an exact rational interval emulator. The primary
`--fixture network` is the four-node resistor family in the root lower-bound
note, endpoint attached to the high rail, kappa4,delta1, baseline current1/4.
Its normalized source has n3,q4,g=(1,0,1), tridiagonal B with diagonal4 and
offdiagonal-2. Physical gain scale is L=1/4. It pays84 degree6 commands,
168 nonzero setting writes,84 resets, and corresponding clearing operations.
The supplied raw current radius is1/8,000,000 and the shared measured
baseline is explicitly retained; normalized intervals have radius1e-6.

The learner receives only these scalar intervals and the public source bounds.
The fit has14 free coefficients, r=n3. Four later tasks require zero new
source measurements. The exact normalized regret bounds are:

    all controls:           2.1901794413051278e-5
    changed prices:         2.8157768589753130e-5
    actuator2 unavailable:  1.0774361251274800e-5
    half budget:            9.1904411486352050e-6.

The first two miss the earlier2e-5 normalized target; the data and parameters
were not tuned after that result. Exact certificate validity passes all four.
The separate `gram` fixture retains four regrets below2e-5. Both are emulated
sources, not physical measurements. The full-degree test does not demonstrate
efficient factorial truncation with n much larger than r. Its generic uniform
diameter bound is388157/750000=0.5175426667, so the small task regrets must not
be relabeled uniformly tiny prediction error. The held-out floating grid is
only diagnostic.
