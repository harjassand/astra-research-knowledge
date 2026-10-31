# Review and proof: acquired absolutely convex closure

31 October 2026. Root construction with source/precision costs.
This note supersedes the metric-cover branch only as the main proposed
mechanism; metric_review.md remains a valid simpler construction and failed
comparison baseline. No historical-novelty claim is established.

## Assessment

The construction is sound with the constants below. It avoids noisy Gram
inversion and never asks the source to prepare a normalized synthetic vector.
Its new retained state is a bounded signed coefficient vector, and every
transition preserves its l1 unit ball. This is the reason scalar Gram errors
and later execution errors do not acquire an unbounded coordinate-conditioning
factor.

The learned feature count is still controlled only by a metric packing bound
in the general theorem, exponential in real orbit dimension r. The broad
polynomial-in-r acquisition question remains OPEN.

The root correctly identified two essential boundaries:
1. a bad old Gram entry can poison arbitrarily many convex solves, so the
   previous off-event expected-growth proof requires an explicit atomic guard;
2. a supplied separation gap between actual orbit points does not make a
   near-convex-combination merge exact. All-horizon gap exactness belongs to
   the atomic-only branch unless a stronger hull-separation premise is supplied.

## 1. Source model and retained features

Use the fixed real-Hilbert contraction/seed/scalar-Gram contract of
metric_review.md. In particular:
- ||T_a||<=1 and ||f_i||<=1;
- source replies are fresh bounded [-1,1] readouts with the exact requested
  Gram mean conditional on the selected setting;
- scalar inner products are implemented by real adjoint-return words;
- all preparations, primitive word lengths, readouts and repetitions are paid;
- every retained feature v_j=T_(w_j)f_(i_j) has an actual literal witness word.

No inverse Gram oracle, normalized linear-combination experiment, or hidden
state vector is supplied.

Let V=[v_1,...,v_N] and

K=aconv{v_1,...,v_N}
 ={Vc : ||c||_1<=1}.

This is a compact symmetric convex set, contained in the Hilbert unit ball.
Start by retaining the s input seeds exactly. Their columns are standard
basis vectors, so initial-state approximation error is zero.
The algorithm is not required to know the actual finite orbit dimension r.

## 2. Cached Gram data and the atomic guard

Fix 0<rho<=1 and

tau=rho²/256,
J=ceil(256/rho²).

Each scalar geometry estimate is accurate within tau on its confidence event.
Maintain one fixed cache value for each unordered literal word/seed pair at
this precision, including norms. Literal feature labels are deduplicated.

For each current feature v_i and action a, form the candidate label
y=T_a v_i. If it is already a literal feature label, its transition is exactly
the corresponding unit column with no new data.

Otherwise acquire its squared norm and cross moments with existing features
as needed. Before relying on the convex optimizer, apply the explicit atomic
guard. Check c=0 and c=+/-e_j using

Rhat(c)=Ghat_yy -2 khat^T c+c^T Ghat c.

If any atomic candidate has Rhat(c)<=3rho²/4, merge with that column.
The positive e_j checks are sufficient for the off-event packing proof;
negative and zero atoms add useful free reuse.

If no atom passes, run the finite convex fit below. If its final estimated
residual passes the same threshold, merge with its coefficient column.
Otherwise add y as a new actual raw-word feature and use its new unit column.

When a new feature is added, its complete cross-Gram row with all old features
has been acquired. Thus the retained Gram matrix is always available for later
fits. Early atomic acceptance can avoid unnecessary cross moments and fitting.

Process every current feature/action pair, including every newly created
feature, until the complete table closes.

## 3. Uniform residual perturbation without a Gram eigenvalue

Let

G=V*V,
k=V*y,
g0=||y||²,
R(c)=g0-2k^T c+c^T Gc=||y-Vc||².

For ANY ||c||_1<=1, entrywise moment errors at most tau imply

|Rhat(c)-R(c)|
 <=tau+2tau||c||_1+tau||c||_1²
 <=4tau.                                                (1)

This holds uniformly over the ENTIRE coefficient ball on one moment event.
The c selected from those same estimated entries therefore requires no new
statistical union bound. It also does not introduce a minimum eigenvalue or
matrix condition number.

The estimated Gram matrix need not be positive semidefinite. The optimization
analysis uses the true convex R and treats the estimated gradient as an inexact
oracle.

## 4. Inexact Frank-Wolfe/Gilbert construction with explicit constants

Initialize c_0=0. For t=0,...,J-1, compute

ghat_t=2 Ghat c_t-2 khat.

Choose a signed coordinate atom s_t minimizing <ghat_t,s> over ||s||_1<=1:
pick a coordinate of maximum absolute gradient and take the opposite sign.
Ties use any fixed deterministic convention.

Set

gamma_t=2/(t+2),
c_(t+1)=(1-gamma_t)c_t+gamma_t s_t.                     (2)

All iterates remain in the l1 unit ball. The algorithm uses only the cached
moments and classical arithmetic.

Let g_t=grad R(c_t)=2Gc_t-2k. Since ||c_t||_1<=1,

||ghat_t-g_t||_infinity<=4tau.                          (3)

The selected atom satisfies the true linear minimization bound

<g_t,s_t> <= min_(||s||_1<=1)<g_t,s>+8tau.              (4)

The factor8 comes from at most4tau error at the selected atom and at a true
minimizer.

For d=s_t-c_t, ||Vd||<=2. Exact quadratic expansion yields

R(c_t+gamma d)
 <=R(c_t)+gamma<g_t,d>+4gamma².                         (5)

Let R*=min_(||c||_1<=1)R(c), and h_t=R(c_t)-R*.
Convexity and (4) therefore give

h_(t+1) <= (1-gamma_t)h_t+8tau gamma_t+4gamma_t².        (6)

Induction with gamma_t=2/(t+2) proves

h_t<=16/(t+2)+8tau.                                    (7)

The base case is safe because c_0=0 gives h_0<=1.
For the induction, subtract8tau and use
(t+1)(t+3)<=(t+2)².

Our chosen J and tau imply

h_J <=rho²/16+rho²/32=3rho²/32.                         (8)

This is a bound for the actual true convex residual, despite possible
nonconvexity of the entrywise-noisy estimated quadratic.

## 5. Accept/reject separation

Accept a column c when Rhat(c)<=3rho²/4.

By (1),

R(c)<=3rho²/4+4tau=49rho²/64<rho².                     (9)

Every stored column therefore has a true local vector residual less than rho
on the simultaneous good event.

If all atomic guards fail and the final FW fit fails, then

R* >=R(c_J)-h_J
   >3rho²/4-4tau-3rho²/32
   =41rho²/64
   >rho²/2.                                           (10)

Hence an added candidate is farther than rho/sqrt2 from the entire old
absolutely convex hull, and therefore from every old raw feature.

The root's constants are correct. There is an intentional ambiguity band:
near enough candidates must merge, far enough candidates must add, and the
middle band can follow either branch. No exact hull-membership decision is
claimed.

## 6. Finite rational coefficients have small denominators

There is no need to multiply all step denominators or to round coefficients.
For t>=1, recurrence (2) has the exact form

c_t=z_t/D_t,
z_t=sum_(j=0..t-1)(j+1)s_j,
D_t=t(t+1)/2.                                         (11)

The vector z_t is integer and ||z_t||_1<=D_t.
Update z by z_(t+1)=z_t+(t+1)s_t.
Consequently final coefficients have one common denominator
D=J(J+1)/2 and O(log J) bits per numerator/denominator, apart from indexing.
Signed atom and zero columns can be stored using that same denominator.

This is a genuine finite-bit realization of the fitted l1-contractive column,
with no synthetic source calls and no coefficient-rounding failure.

For binary +/-1 scalar readouts, use power-of-two shot blocks if a common
dyadic moment denominator is convenient. Upward-rounding the Hoeffding
block size to the next power of two costs less than a factor2. All sample means
then have a common dyadic denominator bounded by the largest block.
Exact gradient comparisons and residual arithmetic are rational/integer.
If the underlying readout is an arbitrary real in [-1,1], its finite digitization
must have an explicit bounded-bias budget; bounded range alone does not
supply infinitely precise recorded numbers.

## 7. O(N) arithmetic per fitting step

A naive dense multiplication Ghat c_t at every step is unnecessary.
Maintain

h_t=Ghat z_t.

Selecting s_t=sign*e_j updates

h_(t+1)=h_t+(t+1)sign*Ghat[:,j].

Then ghat_t=2h_t/D_t-2khat, with the t=0 initialization handled directly.
The gradient scan, integer coefficient update and h-vector update take O(N)
arithmetic per iteration. Final residual evaluation uses

Rhat(c_J)=Ghat_yy
          -2 khat^T z_J/D
          +z_J^T h_J/D²,

also O(N).

Thus a candidate fit costs O(NJ)=O(N rho^-2) arithmetic.
At most mN candidates gives total fitting work
O(m N² rho^-2), with encountered rational bit lengths charged.
Existing Gram storage is O(N²) scalar estimates; no inverse or eigensystem
is computed.

This count is arithmetic, not automatically a hardware-time bound.
Gradient scans, cache construction, shot generation and actual word execution
remain in the complete bill.

## 8. Retained operators and all-future compositional error

After closure, let M_a have the acquired coefficient columns for action a.
Every column has l1 norm<=1, so

||M_a||_(1->1)<=1.                                    (12)

Let E_a=T_a V-V M_a. By (9), every column has Hilbert norm<=rho, hence

||E_a||_(1->Hilbert)<=rho.                             (13)

For an exact seed feature e_i and future word w=a_1...a_L, define

z_t=M_(a_t)...M_(a_1)e_i,
x_t=T_(a_t)...T_(a_1)f_i.

Since ||z_t||_1<=1, the error e_t=x_t-Vz_t satisfies

e_t=T_(a_t)e_(t-1)+E_(a_t)z_(t-1).

Physical contraction and (13) give

||e_L||<=Lrho.                                        (14)

Acquire finite readout rows b_j whose entries are <g_j,v_i>, with ||g_j||<=1,
and estimates bhat_j having entry errors<=beta. Then

|<g_j,T_w f_i>-bhat_j z_L|
 <=Lrho+beta||z_L||_1
 <=Lrho+beta.                                         (15)

There is NO factorN and no coefficient-condition amplification.

For rho=epsilon/(2H), beta=epsilon/2, this certifies every length<=H word
simultaneously. Later words may be selected adaptively. The same single
source/measurement confidence event controls all deterministic uses.

The surrogate vector Vz need not be a physical state and coefficients can be
negative. This is a scalar prediction/program compiler, not a promise to
physically prepare that vector or sample an arbitrary output distribution.

## 9. Deployment and output costs

Metric-net deployment used one discrete transition lookup per step.
The absolutely convex construction instead uses signed matrix-vector products.

Each column has support at most min(N,J), aside from an optional trivial atom,
so a length-L explicit word costs

O(L N min(N,J))

arithmetic in a simple sparse-column implementation, plus a readout dot product.
Dense matrices give O(LN²). This is source-free execution, not unit-time
evaluation of an arbitrary word.

Using common coefficient denominator D, exact execution after L steps has
common denominator D^L and bit length O(L log D), plus readout sample precision.
Thus bit growth is linear in L in the common-denominator representation,
rather than exponential encoded bit length. A finite-precision rounded
executor could be cheaper, but its additional per-step error must be paid.

Table storage is O(mN min(N,J)) coefficient entries, plus the Gram cache,
feature witness parent links and finite readout rows.

## 10. Why the atomic guard is essential off the confidence event

One inaccurate old off-diagonal Gram entry can corrupt every later FW gradient
and estimated residual. Without the independent atomic checks, a single bad
old estimate could cause many near-duplicate candidates to be rejected.
It would then be invalid to assert N<=s+packing+2B merely because good FW
rejections are separated.

The explicit positive-atom guards repair this. Any candidate added after all
branches has, in particular, failed every positive e_j check. If the candidate's
norm, old feature's norm and their cross moment are good, that failed guard
implies

||y-v_j||²
 >3rho²/4-4tau
 =47rho²/64
 >rho²/2.                                            (16)

This pairwise implication uses no other old Gram entries and no optimizer.

For a finite execution prefix, remove all nonseed features associated with a
bad norm estimate, and both feature endpoints of every bad cross estimate.
At most2B features are removed, where B counts bad scalar geometry jobs.
All remaining nonseed features are rho/sqrt2-separated by (16).

With real orbit dimension r, let

P=(1+2sqrt2/rho)^r,
M=s+P.

Then, deterministically on every finite prefix,

N<=M+2B.                                             (17)

The same fixed-rho literal-pair cache and exact literal-label deduplication
requirements from metric_review.md apply. Convex-fitting branches can reduce
growth, while the atomic guard controls all anomalous growth.

## 11. Adaptive confidence, a.s. termination, and expected source bill

Assign job k conditional error budget delta_k=delta/[k(k+1)] and use fresh
bounded shots. If E_k indicates a bad job and B=sum E_k, then

E exp(tB)<=exp(delta(exp(t)-1)) for t>=0,
E binom(B,b)<=delta^b/b!.

These statements follow by successive conditional expectations, not by assuming
independent adaptively selected source settings.

Thus B is finite almost surely and has bounded moments of every fixed order.
Equation (17) makes N finite almost surely, so exhaustive finite-action
processing terminates. No input rank bound is needed by the algorithm.
A known rank/packing bound may instead supply a literal resource cap.

For geometry, each distinct moment costs
O(rho^-4 log((k+1)/delta)) scalar readouts.
There are at most O(mN²+s) geometry jobs, plus qN readout jobs at precision beta.
A tested candidate has actual word length<=N, so Gram-return primitive length
is at most2N. Existing seed readouts have fixed preparation length zero in this
word model; a new readout represented by a longer actual word must additionally
pay that readout word length on each shot.

Consequently the full expected primitive bill, for fixed-cost seed/readout
preparation, is bounded by

O( [ (m+1)(M+1)^3 rho^-4
      +q(M+1)^2 beta^-2 ]
    log((m+q+s+1)(M+1)/delta) ),                       (18)

using (17) and the first four bounded moments of B as in metric_review.md.
Training FW arithmetic adds expected
O(m(M+1)² rho^-2) finite rational operations.

This expected bound is polynomial in the packing number, NOT in r.
The high-probability no-error bound replaces N by M. Rare bad estimates can
increase the finite table, but the factorial tail controls that increase.
A cap at M+2b has overflow probability at mostdelta^b/b!, with UNKNOWN on
overflow, if M is available as a supplied bound.

## 12. Cumulative extension

At unchanged rho and source semantics, new action columns are acquired on all
old features; any new features are expanded under every action. Old columns
are padded with zero entries and keep their residual and l1 guarantees.
No refitting of old source evidence is mathematically required.

Adding a new readout requires its measurements on current features.
Adding a new seed can retain it exactly as a feature, or acquire a bounded
coefficient representation and charge its initial residual separately.

Continue the confidence-job index across extensions. A new operator may
increase the orbit dimension/packing number; the old rank bound is not
inherited automatically. A finite final action/readout/seed collection has
the bound with its actual final orbit.

For smaller rho, old residual tolerances are not upgraded for free.
Recompute/recheck every required column and pay finer moment precision.
Keep prior versions if earlier compiled programs must remain reproducible.

## 13. Exact global orbit-gap branch stays separate

A supplied gap gamma between distinct ACTUAL reachable vectors guarantees
exact merges only when the accepted candidate is an actual orbit vector:
the atomic-only positive-center branch of metric_review.md.

It does not imply that a candidate within rho<gamma of a signed convex
combination equals that combination. The combination may lie between well
separated orbit points and need not itself belong to the orbit.
Therefore the FW compiler retains Lrho error accumulation.

If an all-horizon exact finite-orbit theorem is desired, run the separately
defined atomic-only algorithm, or supply and prove a stronger relevant
hull-separation premise. Do not silently give the convex route the atomic
gap corollary.

## 14. Comparison and scientific scope

This refinement passes the immediate ordinary signed-reuse challenge:
-f can be represented from f at coefficient cost1 without a new feature.
More generally it keeps any acquired stable signed combination rather than
requiring a nearby single actual state.

It does not prove an advantage over all equally informed retaining learners.
Ordinary stable dictionary learning, convex-hull approximation, Frank-Wolfe/
Gilbert methods, and nonexpansive model reduction can adopt this construction.
The justified contribution under investigation is the joined acquisition
interface: actual adjoint Gram words -> bounded signed coefficients -> checked
approximate closure -> reusable source-free scalar programs, with precision,
failed search, word execution, and later matrix arithmetic all charged.

No general polynomial-in-r theorem, arbitrary new physical operation,
historical priority, or measured practical advantage has been established.

