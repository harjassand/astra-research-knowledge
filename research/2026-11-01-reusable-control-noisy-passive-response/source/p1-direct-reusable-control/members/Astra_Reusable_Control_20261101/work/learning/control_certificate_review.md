# Scoped independent review: scalar-only offline control certificates

2026-11-01. Reviewed `../control/control_demo.py` and independently validated
its saved certificates. No historical novelty, physical experiment, or
large-system performance claim is assessed here.

## Verdict and actual scope

PASS for the declared normalized source contract and four released tasks.
The exact algebraic dual-certificate and global concavity-regret arguments
are sound. The independent checker consumed only:

* `../control/results/scalar_records.json`;
* `../control/results/dual_certificates.json`;
* explicit public specifications n=3,r=3,k=6,q=4,delta=G=1,eta=10^-6 and the
  four task cost/cap/budget definitions.

It did not import `control_demo.py`, read B or g, read the demo's source-truth
diagnostics, call a numerical optimizer, or use any floating value to decide
a certificate. Files:

* `validate_control_certificates.py`;
* `independent_control_validation.json`.

All 84 supplied settings were checked to be exactly the complete degree-six
simplex lattice, without duplicates. All 32 rational dual certificates were
validated. The exact task regrets, displayed as decimals, were:

| Task | Certified global regret |
|---|---:|
| All controls | 0.000013566046254835413 |
| Changed prices | 0.000019372492589270274 |
| Actuator 2 unavailable | 0.000008553456130896513 |
| Half budget | 0.0000023465831286934903 |

The largest exact dual residual-box repair was 219/25000000000000. The receipt
retains exact Fraction values for every conclusion. No source calls are
needed by this validation or by the four offline consumers.

## 1. Source isolation checked in the executable

`run()` uses B,g to generate the simulated scalar readings and to check
known-source diagnostics after proposal/certification. `IntervalLearner`
receives only n,r,q and the scalar records. Its constructor builds coefficient
boxes and observation constraints solely from those inputs. `propose_value`,
`certify_ratio`, `interval`, and `gradients` do not access B,g or the source
determinant coefficients. The learner's floating fit is not claimed feasible
by exact arithmetic; it is only a proposal source. That does not affect the
subsequent certificates.

The actual observation intervals are generated with exact rational errors
inside eta. This qualifies the emulated data, not an experimental apparatus.
The source-class and measurement-error contracts would have to hold in a
physical application. Future settings change budget, caps or price, while
the same physical response source remains fixed.

## 2. Exact LP-dual certificate

The original coefficient polytope is A theta<=b, 0<=theta<=U. At fixed u,
the denominator is D=1+m(u).d>=1. Under Charnes-Cooper, t=1/D and z=t theta.
The transformed constraints are

    [A,-b](z,t)<=0,
    z_j-U_j t<=0,
    [m,0,1].(z,t)=1,
    0< t <=1, 0<=z_j<=U_j.

The displayed finite box for z,t is valid. The explicit non-strict system
cannot have t=0, because z_j<=U_j t then forces z=0, contradicting the
normalization equation. Thus no spurious infinite-denominator point enters.

For any proposed rational nonnegative multipliers lambda, arbitrary rational
nu, and objective c, define

    residual = c-lambda^T A_transformed-nu*equality,
    bound = nu + sum_j max(residual_j,0)*box_upper_j.

Every transformed feasible point satisfies c.w<=bound. This follows directly
from the inequalities, exact equality, and coordinate box; numerical dual
optimality is not a premise. Rounding the solver multipliers and clipping
them nonnegative is therefore safe once the residual repair is included.
The checker recomputed all rows, residuals, repairs and bounds in Fraction
arithmetic and verified equality to the saved values.

## 3. Derivative certificate

Here r=n, so the physical response has exactly F=N/D with no truncation debt.
For every coordinate i,

    partial_i F = (N_i-F D_i)/D,  D_i>=0.

If the value interval is lo<=F<=hi, then

    (N_i-hi D_i)/D <= partial_i F <= (N_i-lo D_i)/D.

These are precisely the signed linear-fractional objectives in certificates
2+2i and 3+2i of each task block. The physical law is nondecreasing in every
nonnegative intervention coordinate, so intersecting derivative intervals
with [0,infinity) is valid. The physical law also lies in [0,L]=[0,1], making
the value-interval clipping valid. Neither property is asserted of every
relaxed rational model.

## 4. Global regret despite a possibly nonconcave surrogate

The true physical F is concave. For a feasible proposed x and any feasible z,

    F(z)-c.z-(F(x)-c.x) <= (gradient F(x)-c).(z-x).

With componentwise bounds gl<=gradient F(x)<=gu and x,z>=0,

    regret(x) <= max_{z in C}(gu-c).z -(gl-c).x.

The feasible set C is a box intersected with a total-dose simplex. Sorting
positive coefficients and filling available caps is an exact linear optimizer.
The checker independently recomputed this optimizer and the resulting
regret. The fit may be nonphysical or nonconcave, and SLSQP may find only a
local proposal; neither issue affects acceptance because this separate
global physical-gradient certificate supplies the bound.

The derivative inequalities hold simultaneously at arbitrary later-selected
points whenever the original observation intervals hold. No new statistical
union bound is needed merely because the proposal depends on those records.

## 5. Scope of the numerical demonstration

The experiment uses r=n=3 and k=2r. Thus E=B=0, and the fitted rational family
has exact full degree. It does not test low-degree factorial truncation when
n is much larger than r. Nor does a small certificate at four selected
actions establish uniformly tiny prediction intervals everywhere.

Indeed the generic uniform diameter theorem with these specifications gives

    C_6 A_3(4)^2 * 2eta = 0.5175426666666667,

before intersecting with the physical [0,1] range. The actual LP intervals
and derivative certificates at the selected actions are far tighter. The
four small numbers above are certified TASK REGRETS, not a claimed uniform
all-simplex prediction error. The held-out floating grid is an additional
diagnostic and is not used in this review's certificate.

## 6. Conventional-method credit

The implementation is a positive-denominator rational set-membership fit,
ordinary numerical proposal, and exact residual-repaired LP-dual check.
These computational tools are conventional. Astra's determinant coefficient
boxes and the new finite-noise whole-simplex theorem make their information
contract explicit for this physical source class. The prototype supplies no
measured superiority over an equally informed ordinary rational fit or
task-specific noisy convex optimizer.
