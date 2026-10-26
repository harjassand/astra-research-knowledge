# Astra Pro3 — closed inverse-sector acquisition and constrained physical operations

26 October 2026. Continued from the acquired convex-dual experimental service. This is a new scoped *application and procedure construction* based on classical Kirszbraun extension, monotone-response and variational-inequality theory, not a historical-priority claim for those mathematical components. All reported numerical controls are executions of the accompanying code. Synthetic native sources and source-aware checkers are sharply separated from the learner's retained observations.

## 1. Why change representation?

The preceding convex-dual compiler retained native measurements of an unknown globally convex energy and its gradient, then answered force-controlled questions from its conjugate. This was effective but excluded sources with nonzero cyclic circulation and required a supplied global energy law. It also incurred very large rational polygon-area coefficients during joint task evaluation.

This continuation uses a different, explicitly supplied global *sector* contract on a fixed forward response source:

\[
  F:\mathbb R^d\to\mathbb R^d,\quad F(x)=m x+A(x),\quad
  \|A(x)-A(y)\|_2\le a\|x-y\|_2,\qquad 0\le a<m.
  \tag{1}
\]

The learner has only native **forward, full-vector** calls `x -> F(x)`; a call returns `d` real coordinates. There is no native inverse, transpose, derivative, energy, or analytic model interface. Constants `m,a`, Euclidean norms, source stability and truthful measurement-error envelopes are physical/source contracts, not conclusions from finite observations. Rational inputs and exact rational native-output controls are distinguishable from rounded/noisy reports.

The sector class is wider than conservative gradient models: `A` may include an antisymmetric, nonconservative interaction. It is narrower than the class of all strongly monotone Lipschitz maps; the *specific shifted Lipschitz bound* (1) is essential.

## 2. Exact closure of the source class under inverse operations

**Theorem 1 (bidirectional inverse-sector representation).** Under (1), `F` is globally bijective, its inverse `H=F^-1` exists, and

\[
 H(p)=c p+B(p),\qquad c=\frac{m}{m^2-a^2},\quad
 \operatorname{Lip}(B)\le b=\frac{a}{m^2-a^2}.                     \tag{2}
\]

Conversely every global map `H(p)=cp+B(p)` with `Lip(B)<=b` is bijective and its inverse belongs to (1).

**Proof.** For every prescribed `p`, the native equation `F(x)=p` is equivalent to `x=(p-A(x))/m`. This map is a contraction with factor `a/m<1`, giving a unique solution by Banach's theorem. Given two forces `p,q` with response locations `x=H(p),y=H(q)`, put `h=p-q,d=x-y`. The native law (1) is exactly

\[
 \|h-md\|^2\le a^2\|d\|^2.
\]

Completing squares with `D=m²-a²>0` gives

\[
 \boxed{\|d-(m/D)h\|^2\le (a^2/D^2)\|h\|^2.}             \tag{3}
\]

This is precisely the Lipschitz condition on `B=H-cI`. Reversing the same algebra proves the converse pair condition. Because `c>b`, `H=cp+B` also has a globally defined inverse by the same contraction argument. Its inverse satisfies the original native sector inequality. There is no inference of energy-conservation, symmetry, or hidden microscopic mechanism here.

### 2.1 What the learner acquires

Each old, exactly acquired native pair `F(x_i)=p_i` becomes an *inverse observation* `B(p_i)=x_i-cp_i`. For a later set of completely unspecified force tasks `q_j` and candidate equilibrium positions `z_j`, all old and new observations are jointly possible **if and only if**

\[
 \boxed{\|(z_u-z_v)-c(q_u-q_v)\|_2\le b\|q_u-q_v\|_2}
 \qquad \text{for every pair of old or future force labels},                 \tag{4}
\]

with old inverse positions fixed to their measured `x_i`. Here `(q_u,z_u)` denotes either a retained `(p_i,x_i)` or a future unknown `(q_j,z_j)`.

**Necessity** follows from Theorem 1. **Sufficiency** follows by extending the finite residual map `q_i -> z_i-cq_i` to a global `b`-Lipschitz map using Kirszbraun's theorem and taking the inverse of the resulting `H= cI+B`. Thus (4) describes the **complete compatible source family** over (1), not just separate prediction intervals. It does not require the unknown source's response at a new force to have been measured or even queried.

For completeness, the finite Lipschitz extension step can be proved directly. Given old sites `s_i`, outputs `v_i` with `||v_i-v_j||<=b||s_i-s_j||`, and a new site `s`, minimize the convex, coercive function `max_i(||v-v_i||²-b²||s-s_i||²)` over `v`. At its minimizer `v*`, the subgradient condition gives `v*=sum lambda_i v_i` with nonnegative weights supported on active constraints summing to one. The corresponding active average equals

\[
 \frac12\sum_{i,j}\lambda_i\lambda_j\|v_i-v_j\|^2
 - b^2\sum_i\lambda_i\|s-s_i\|^2\le 0,
\]

by the Lipschitz pair conditions and the variance identity
`sum lambda_i||s-s_i||² >= (1/2)sum lambda_i lambda_j||s_i-s_j||²`. Hence the new compatible value exists. Iterating on a dense countable set and completing by continuity gives the whole-domain map. This is the standard finite-dimensional Kirszbraun mechanism.

**Computation:** for `N` retained force points and `k` new force questions, (4) is a finite family of `O((N+k)^2)` *convex second-order cone* constraints in `kd` unknown scalar coordinates, with no source calls. A linear later task `sum_j w_j·z_j` can therefore have its exact extrema over this model class computed by a conic optimizer. Numerical solver output needs separate residual/dual validation; the code here instead verifies closed-form instances and explicit sparse rational outer certificates. Do not relabel a numerical search proposal as an exact optimizer.

### 2.2 Joint information is different from independent predictions

For one previously retained call `F(0)=0`, set `m=3,a=1` so `c=3/8,b=1/8`. Consider two later forces `p1=(2,0)`, `p2=(2,1/50)`. Their relative vertical equilibrium displacement obeys the **sharp** interval

\[
 \boxed{[F^{-1}(p_2)-F^{-1}(p_1)]_2\in[1/200,1/100]}.    \tag{5}
\]

The two globally admissible sources `F_+(x,y)=(3x,4y)` and `F_-(x,y)=(3x,2y)` agree on the old call and attain the two endpoints. Treating the sharp marginal inverse balls separately gives a naive difference interval of width at least `1`; (5) has width `1/200`, a **200-fold reduction** from retaining the fact that both tasks involve one source. Much of the relative bound follows from the **supplied sector contract itself**, not from learning an unobserved microscopic relation; the acquisition-specific gains below must be distinguished from it.

## 3. A fixed-size proof certificate for a single future scalar question

For a *single* future force `p`, (4) reduces to an intersection of Euclidean balls:

\[
 X(p)=\bigcap_i\mathbb B\left(
  c_i=x_i+c(p-p_i),\qquad
  r_i=b\|p-p_i\|_2\right).                                      \tag{6}
\]

This pointwise family is exact under (1). It is not a product family for multiple future forces; the cross-task constraints in (4) must also be retained.

**Theorem 2 (sparse supporting certificate).** If the intersection `X(p)` has nonempty interior, the sharp upper endpoint of any scalar question `v·H(p)` admits a certificate involving at most `d` of the retained balls, regardless of the total number of old experiments.

Indeed, at the maximizer `z*` the KKT condition under Slater is `v=2 sum_i lambda_i(z*-c_i)` with nonnegative multipliers on active balls. Conical Carathéodory reduces this representation to at most `d` active normals. For their normalized weights `w_i=lambda_i/sum lambda`, define

\[
 \bar c=\sum_iw_i c_i,\qquad
 R^2=\sum_iw_i r_i^2-\sum_iw_i\|c_i-\bar c\|^2.        \tag{7}
\]

The weighted sum of the selected squared-ball inequalities proves `||z-bar c||²<=R²` for **every** compatible source; therefore

\[
 \boxed{v\cdot z\le v\cdot\bar c+\|v\|R}.                  \tag{8}
\]

At the optimizing weights, the KKT condition and active-ball equalities show that `z*` attains (8). This proves sparse existence. If the intersection has no interior, a limiting argument is needed and the at-most-`d` exact-attainment statement is not made.

**Executable version:** a bounded scalar optimizer only *proposes* rational weights on one or two historical balls. The complete-square inequality (7) is recomputed in exact `Fraction` arithmetic, and the square root in (8) is enclosed upward using integer square-root operations. Optimization failure can weaken but cannot invalidate a certificate. In two-port controls six actual history readings supported unforeseen scalar inverse queries using at most two old readings per endpoint. The largest reduction in width over the best single historical-ball certificate in the finite test was **1.1331×**; selected certificate integers had at most **103 bits**. This is proof compression, not a demonstrated dramatic accuracy gain, and the proposals are not asserted globally optimal.

## 4. A new exact saturation threshold—and why near saturation is dangerous

Let `m=3,a=1`, and acquire **only** two one-dimensional-direction native readings in a two-port source:

\[
 F(-e_1)=-s e_1,\qquad F(e_1)=s e_1,
 \quad s=2+\varepsilon,\quad 0\le\varepsilon\le2.          \tag{9}
\]

For the *unqueried* future inverse task `F^-1(0)`, (6) gives two equal disks with centres `±(1-3s/8)e1` and radii `s/8`. Their exact intersection has the sharp transverse support

\[
 \boxed{|[F^{-1}(0)]_2|\le
        \sqrt{\frac{\varepsilon(2-\varepsilon)}8}}.       \tag{10}
\]

Both endpoints are attained over the source class: add a candidate inverse point `(0,±t)` with `t²=eps(2-eps)/8`; all finite residual Lipschitz inequalities hold, and the extension theorem supplies a global response realizing it. Rational candidate witnesses can approach the endpoints arbitrarily closely.

When `eps=0`, the disks are tangent and the **entire unmeasured equilibrium is exactly forced to be zero** by two native observations, with zero new source calls. But for every positive `eps`, an `O(eps)` saturation defect permits an `O(sqrt(eps))` hidden transverse equilibrium shift. The exact controls executed at `eps=0,10^-2,10^-4,10^-6,10^-8`, including explicit pairs of compatible but distinct global sources. A noisy near-saturated report must never be rounded into an exact forced-response claim.

This sensitivity has an analogue in classical positive-operator completion; the present result concerns a different native source interface and an inverse operation.

## 5. Honest observation errors and persistent limits

If a native observation at known `x_i` reports `phat_i` with Euclidean error at most `eps_i`, exact inverse consistency produces the sound **outer** ball

\[
 \left\|H(p)-[x_i+c(p-\widehat p_i)]\right\|
 \le b\|p-\widehat p_i\|+(b+c)\varepsilon_i.                \tag{11}
\]

Proof: substitute the true native response in (6), then use the triangle inequality on both ball centre and radius. It is not an exact description of correlated noisy histories.

A separate adversarial-noise obstruction uses the two sources `F_±(x)=mx±eps e1` and the **same** report `phat(x)=mx` at every possible query. Both satisfy the global contract, each report has error `eps`, but their inverse responses differ by `2eps/m`. No method can guarantee worst-case equilibrium error below `eps/m` for this observation contract, irrespective of the number of additional native calls. This does not apply to independent zero-mean stochastic errors.

**Source-contract identifiability failure:** the sector law is not established by finite pairwise checks. A compactly supported `C³` perturbation of `F_0(x)=3x` placed far away from old sites `[-1,1]` agrees with every old reading but becomes locally decreasing near `x=39/4`. A separate two-point native test would detect it, but the old measurements alone cannot establish global monotonicity or Lipschitzness.

## 6. Actual nonlinear nonconservative forward-source execution

The first test source was a rational-evaluable two-port response

\[
 F(x,y)=3(x,y)+\frac12(-y,x)
 +\frac18(\phi'(x),\phi'(y))
 +\frac1{16}\phi'(x+y)(1,1),\quad
 \phi(t)=\frac{t^2}{1+t^2}.                                 \tag{12}
\]

Since `|phi''(t)|<=2`, the nonlinear gradient contribution has global Jacobian norm at most `1/2`; the antisymmetric component has norm `1/2`. Therefore `F-3I` is **globally 1-Lipschitz**, satisfying exactly the supplied `m=3,a=1` contract. The learner's inference code is given `m,a` and native observations, **not** the formula (12) or its derivatives. A separately charged 32-call rational cycle yields cyclic-monotonicity sum `373/400=0.9325>0`, falsifying the convex-gradient interpretation.

The source-aware test setter selected a previously unannounced force by evaluating (12) at hidden `x=(3/2,-1)`. A native learner acquired `F(0)` once, then made **five additional full-vector calls** at query inputs rounded to a 12-bit dyadic grid. Native outputs remained exact rationals. Each query/rounding step used the certified update

\[
 z_{t+1}=z_t+\frac{p-F(z_t)}m,
 \qquad R_{t+1}\le\frac am(R_t+\delta_t),                  \tag{13}
\]

where `delta_t` bounds the discrepancy between the exact planned probe and the allowed dyadic query. This bounds precision loss explicitly and prevents uncontrolled rational coefficient expansion. Initial one-observation radius was about `0.69513`; after the five new calls the certified error radius was **0.00289396**, and the independently known true location satisfied every retained ball and every execution certificate.

Fifty further force questions were supplied **after acquisition**. The same six retained vector observations certified every corresponding inverse location with zero new learner source calls; the mean radius decreased from `0.6894653` using only the first old call to `0.0396821` using the entire bank, a **17.37×** gain. Their 50 source-aware setter/reference evaluations were counted separately. Each acquired vector has two returned scalars.

## 7. Next operation: fixed-dose constrained equilibrium without any energy law

The preceding inverse `F^-1(p)` need not stay in the physically admissible input set. Let `C` instead be a closed, convex set on which native forward experiments are permitted. A more realistic new operation is the constrained **variational equilibrium**: find `x* in C` satisfying

\[
  \langle F(x^*)-p,z-x^*\rangle\ge0 \quad\forall z\in C.       \tag{14}
\]

Unlike the inverse, this always exists and is unique for any `p` when the residual sector contract holds on `C`:

\[
 x^*=\Pi_C\!\left(x^*+\frac{p-F(x^*)}{m}\right),\quad
 \operatorname{Lip}\left(\Pi_C\circ\left[x\mapsto x+\frac{p-F(x)}m\right]\right)
 \le\frac am<1.                                             \tag{15}
\]

This follows from the metric projection characterization, nonexpansiveness and Banach contraction. No native inverse, energy, off-dose actuator or global potential is available.

**Retained first-order ball.** For each old native reading `F(x_i)=p_i` and `mu=m-a>0`, every constrained equilibrium satisfies

\[
 \boxed{\left\|x^*-\left[x_i+\frac{p-p_i}{2\mu}\right]\right\|
 \le \frac{\|p-p_i\|}{2\mu}.}                           \tag{16}
\]

Take `z=x_i` in (14) and combine with `mu`-strong monotonicity of `F`, then complete squares. This is a sound outer ball, **not** the exact joint inverse posterior of section 2: a constrained variational equilibrium may have `F(x*)!=p`. Projecting its centre onto `C` preserves the radius. Each additional native forward reading applies (15), reducing the radius by `a/m`, plus an explicitly charged dyadic projection-rounding error.

### Native simplex run

The second test source is a nonpolynomial, three-component response, with a skew coupling between its first two coordinates, restricted to

\[
 C=\{x\in\mathbb R_{\ge0}^{3}:x_1+x_2+x_3=1\}.
\]

Its globally checked shifted Jacobian Lipschitz bound is `1/2+1/4+3/16=15/16 <=1`, with supplied `m=3,a=1`. All actual native probes satisfy the nonnegative fixed-dose constraint. A separately charged **64-call** cyclic test yields positive circulation `0.055546875`, excluding a conservative convex-gradient explanation on the simplex.

Four native initial readings at three simplex vertices and the centroid were retained. Four later load tasks (two interior, one vertex and one edge) each used five additional native forward calls. The vertex/edge loads include nonzero normal forces, so they are genuinely constrained variational equilibria rather than presumed unconstrained inverse evaluations. Every estimate, rounding update and source-aware true solution was checked with exact rational arithmetic.

| Later task | Certified position radius, history-aware | Equal-budget domain-only projection radius |
|---|---:|---:|
| Interior load 1 | 0.00086948 | 0.00354297 |
| Vertex load | 0.00336141 | 0.00336141 |
| Edge load | 0.00360549 | 0.00360549 |
| Interior load 2 | 0.00092976 | 0.00374335 |

Both procedures use five new calls per later task; the domain-only comparison is a **weaker** equally budgeted classical baseline that ignores the old outputs. A fully informed projected-VI/bundle algorithm can adopt the same history-aware initialization and tie these guarantees. The cost across all four tasks is `4` common initial calls plus `20` additional learner calls, each returning three coordinates. The 64-cycle falsifier, four task-setting source-aware calls and the 20 comparator calls are separate work, not free sources.

The unconstrained inverse-sector model and constrained VI model must remain distinct: projecting inverse solutions and asserting that `F(x)=p` survives an active constraint is invalid.

## 8. Scientific assessment, equal-information comparator and next frontier

What was acquired: finitely many real forward response vectors, their original input sites, and exact or explicitly inexact consistency constraints. What must be supplied: source stability, Euclidean norm/vector-port semantics, the sector parameters and their global/local physical validity, the native allowed input set, and correct measurement-error envelopes. No experiment in this continuation discovers those structural premises.

What transfers: (i) exact joint posteriors for arbitrary finite sets of future **unconstrained inverse forces** in the sector model; (ii) sharp relative inverse questions and compact, rational, future-specific bounds; (iii) adaptive native forward procedures with certified precision and quantization; (iv) constrained variational equilibrium on a nonnegative fixed-dose simplex even for forces without an admissible unconstrained inverse. Everything preserves same-source coupling and charges actual forward calls. One-point noisy outer balls, same-class posterior sharpness, and constrained-VI outer balls have **different logical scopes**.

Equal-information comparison: Kirszbraun interpolation, Banach fixed-point iteration, conventional strongly-monotone variational inequality solvers, ball-intersection conic optimization, and classical retaining algorithms can all reproduce the core mechanism. The original naive independent interval decoder and a domain-only projected baseline lose information that these informed alternatives can use. No distinct architecture wins against an equally informed algorithm, and there is no new physical law or historically novel mathematical theorem demonstrated.

Revealing failures: an unrestricted global sector law cannot be certified from finite readings; an approximately saturated source need not have a forced inverse; adversarial noise imposes a nonzero precision floor; exact naive rational iteration and unrestricted numerical sparse-certificate searches led to impractical coefficient growth or runtime limits, motivating bounded dyadic arithmetic and fixed-size rational proof witnesses; the simplex constrained operation is *not* unconstrained inverse interpolation. Global agreement of a microscopic physical source with a Lipschitz model remains externally unestablished.

**Best next scientific attack:** obtain useful **local and testable sector/monotonicity warranties** from repeatable physical excitation under a declared causal/regularity primitive, and develop an exact joint consistency language for **constrained** variational equilibria without pretending that their feasible set is the inverse map's convex SOCP family. These are substantive open problems. The research here identifies the information needed for those operations and executes a new source-to-operation bridge without assuming an energy potential.

## Reproducible files

- `astra_pro3_sector_joint.py` and `astra_pro3_sector_joint_results.json`: complete inverse family, 32-call nonconservative falsifier, 6-call native inverse transfer, fifty later tasks, coherent relative-operation witnesses, bounded-noise control.
- `astra_pro3_sparse_inverse_certificate.py` and `astra_pro3_sparse_inverse_certificate_results.json`: at-most-two-reading weighted-ball rational certificates and six late-task checks; bounded numerical proposal, exact outward verification.
- `astra_pro3_sector_saturation.py` and `astra_pro3_sector_saturation_results.json`: forced inverse, sqrt defect, exact rational indistinguishable source witnesses, global-law finite-evidence failure.
- `astra_pro3_sector_constrained_vi.py` and `astra_pro3_sector_constrained_vi_results.json`: all-simplex nonconservative three-port native source, inverse-to-VI change of operation, exact rational projection, honest query/rounding limits and equal-budget baseline.

All four scripts completed in an independent clean directory; the four JSON files matched their original saved outputs **byte for byte**. Scripts use Python standard library plus SciPy for bounded *candidate-weight proposals only* in the sparse evaluator; correctness certificates are exact rational and do not depend on numerical optimizer validity.

### Mathematical antecedents

- Kirszbraun extension theorem, e.g. [Naor, *Kirszbraun's Extension Theorem*, exposition](https://web.math.princeton.edu/~naor/homepage%20files/embeddings_extensions.pdf).
- Convex projection and strongly monotone variational inequalities, e.g. [projected-gradient existence/uniqueness discussion](https://link.springer.com/article/10.1186/s13660-018-1941-2).
- Classical conical Carathéodory, Slater/KKT, second-order cone optimization, Banach contraction. This note supplies the needed scoped proofs rather than claiming novelty or relying on an unverified numerical optimizer.
