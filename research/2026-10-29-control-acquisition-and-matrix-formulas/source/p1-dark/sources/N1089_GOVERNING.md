# Astra Pro3 — Task-conditioned robust response acquisition and certified continuous intervention design

**27 October 2026. Research continuation.** All experiments below are exact-rational or outward-interval mathematical software calculations on a synthetic passive network, except the stated floating-point proposal optimizer. The final reported correctness and regret certificates do **not** depend on that optimizer's convergence. No new physical law, experimental device, newly acquired source-class specification, historical algorithmic priority, or advantage over equally informed retaining algorithms is claimed.

## 1. New operation and physical information boundary

Preserve the previous 510 native single-scalar reactions for a fixed unknown source

\[
 Q(u)=Q_0+\sum_{i=0}^{127}u_i v_i v_i^T,
 \qquad Q_0\succ0,
 \qquad u_i\ge0,\quad \sum_i u_i\le\delta=\tfrac15,
\]
\[
 Z(u)=e^TQ(u)^{-1}e,\qquad R(u)=\tfrac32+1/Z(u).
\]

Each acquisition reports one scalar `R` with deterministic, possibly correlated absolute error at most `1e-8`; independent noise and access to hidden matrices are **not** assumed. The learner is supplied the affine rank-one PSD actuator class and stable source. A separate physical argument would be needed to warrant that class in a real experiment.

The old finite-noise learner acquires response calibration intervals `z0,P_i`, intervals for two observed columns of a centered PSD Gram matrix, and sound residual diagonal upper bounds. It **does not** infer exact rank from noisy readings. With two certified SPD landmarks the unknown Gram factors as

\[
 S=S_0+E,\quad S_0=C^TW^{-1}C,\quad E\succeq0,\quad 0\le E_{ii}\le\rho_i^+.
\]

Let `S_*` be the nominal PSD projected Gram built from rounded midpoint landmark columns and midpoint inverse `W`. For every compatible physical source, componentwise interval calculations certify

\[
 |(S_0-S_*)_{ij}|\le \beta_{ij}.
\]

Write `d_i=u_iP_i` and `D=diag(d_i)`. The exact operational quotient is

\[
 Z(u)=\frac{z_0^2}{z_0+F(D,S)},\qquad
 F(D,S)={\bf1}^T(D^{-1}+S)^{-1}{\bf1},
\]

with zero-dose indices omitted. As before, the physical response is evaluated through the one scalar native reaction, not by observing the Gram matrix.

## 2. Task-conditioned sharp PSD completion theorem

**Theorem.** Fix any known `D>0`, positive-definite `A=D^{-1}+S_*` and nonnegative numbers `rho_i`. Over the **relaxed** completion class

\[
 \mathcal E_\rho=\{E\succeq0:E_{ii}\le\rho_i\},
\]

there is an exact, sign-independent variational formulation

\[
 \boxed{\min_{E\in\mathcal E_\rho}{\bf1}^T(A+E)^{-1}{\bf1}
 =\max_x \big\{2{\bf1}^Tx-x^TAx-(\sum_i\sqrt{\rho_i}|x_i|)^2\big\}.}
 \tag{1}
\]

Proof: write the inverse quadratic form as `max_x (2 1^T x - x^T (A+E)x)`. The elliptope-like residual class is compact by the PSD Cauchy inequality, and the payoff is affine in `E` and strictly concave in `x`. Restrict the maximizing `x` to a sufficiently large closed ball (uniform SPD coercivity), interchange `min_E max_x` by the convex-concave minimax theorem, and use

\[
 \max_{E\succeq0,\,E_{ii}\le\rho_i} x^TEx=(\sum_i\sqrt{\rho_i}|x_i|)^2.
\]

The equality on the right is attained for the rank-one matrix `E=ss^T`, with `s_i=sqrt(rho_i) sign(x_i)`. The maximization in (1) is a convex optimization problem after negating its concave objective, not necessarily a fixed-rank-one matrix substitution.

**Fast exact-saddle subcase.** Let `r_i=sqrt(rho_i)` and compute

\[
 x_+=(A+rr^T)^{-1}{\bf1}.
\]

If every active `x_{+,i}>=0`, then `E=rr^T` is **actually worst-case** over the entire relaxed completion class. Indeed for every admissible `E`, `x_+^T E x_+ <=(r^Tx_+)^2`, and evaluating the inverse variational identity at `x_+` proves

\[
 F(D,S_*+E)\ge F(D,S_*+rr^T).
\]

As `E=rr^T` itself is feasible, equality is attainable. The sign condition is explicitly checked on the exact-rational learner side for each later request. Without it, use the sign-independent tangent bound

\[
 F(D,S_*+E)\ge F(D,S_*)-(\sum_i\sqrt{\rho_i}|q_i|)^2,
 \qquad q=(D^{-1}+S_*)^{-1}{\bf1},
\]

or solve (1) to higher accuracy with a certified convex solver. No false rank truncation or false fixed-sign optimality is inferred.

The actual learner does **not** know `D,P_i,C,W` exactly. It conservatively combines the sharp residual subproblem with previous outward-rounded response enclosures for `P,z0` and the independently justified weighted resolvent fit-uncertainty bound. Thus the word *sharp* refers only to the relaxed residual subproblem at fixed projected matrix and `D`, not to the full inverse image of all 510 finite-noise source readings.

### Executed 128-control source

`astra_psd_task_sharp.py` reread the identical 510 native scalar source records with the previous `1e-8` deterministic correlated error allowance. For 50 held-out mixed intervention histories, **every actual response was contained**, and the sufficient rank-one saddle sign check passed for all 50.

| Quantity | Previous PSD-resolvent interval | Task-conditioned completion interval |
|---|---:|---:|
| Median reciprocal-response interval width | `7.653005520166307e-5` | `4.552282646939716e-5` |
| Maximum width | `5.249257027522716e-4` | `3.11026211644106e-4` |
| Median reduction factor | — | `1.6836999629` |
| New native readings at deployment | 0 | 0 |

A second, freshly specified sequence of 20 objectives over **840 disjoint candidate interventions** used the same source readings. The largest certified finite-menu regret fell from `4.755538201301968e-5` to `4.19133316096464e-5`; the average bound fell from `6.6837850434575785e-6` to `5.888494416643108e-6`. Both methods selected the same 20 actions (all 20 matched the verifier-only finite-menu optimum), so the proven improvement here is precision of **guarantees**, not better realized choices.

### Decisive failure of removing the sign guard

Take `D=diag(1/10,1/10)`, `S_*=[[10,30],[30,90]]`, and `rho=(10,10)`. All indicated matrices are PSD and physically realizable as a centered passive-network Gram completion in sufficiently many hidden coordinates. The three completions give

- `E=10[[1,1],[1,1]]`: `F=3/85` and `q=(7/170,-1/170)`;
- `E=10[[1,-1],[-1,1]]`: `F=1/29`;
- `E=10I`: `F=1/30`, the **true** minimum over the PSD diagonal-envelope class.

The final claim is certified by the dual witness `x=(1/30,0)`, because `E_11<=10` for every feasible completion. A universally hardcoded all-positive rank-one completion would produce a dangerously optimistic lower bound. This is an explicit failure, not an implementation anomaly.

## 3. New capability: *continuous* globally certified intervention optimization

Let a **new**, not prespecified, task supply nonnegative linear prices `c_i` for interventions. Its physical reward is

\[
 G(u)=Z(0)-Z(u)-c^T u.
\]

**Passivity-concavity theorem.** `Z(u)` is convex on the entire nonnegative intervention simplex: the identity

\[
 e^TQ(u)^{-1}e=\max_y\big\{2e^Ty-y^T Q(u)y\big\}
\]

expresses it as the pointwise supremum of affine functions of `u`. Thus `G` is concave. For any candidate `x` and any feasible `y`,

\[
 G(y)-G(x)\le\nabla G(x)^T(y-x).
\]

The problem is therefore to acquire sound intervals for **every** derivative component at an arbitrary new `x`, despite unobserved interactions and bounded measurement noise. This does not require measuring native derivatives.

### Deriving derivative enclosures from the old scalar data

For a fixed compatible `D` define `q=(D^{-1}+S)^{-1}1`, zero on inactive indices, and for *all* indices (including zero doses)

\[
 k_i=1-(S q)_i.
\]

Differentiating the inverse-response quotient yields the exact identity

\[
 \boxed{\frac{\partial G}{\partial u_i}(u)
 =\left(\frac{z_0}{z_0+F}\right)^2 P_i k_i^2-c_i.}\tag{2}
\]

The corresponding surrogate `S_*` yields `k_i^*`, computable using a **two-by-two** inverse of `W_*+C_*DC_*^T` even for inactive coordinates. Interval arithmetic over `P_i` encloses each `k_i^*` without assuming exact singleton coefficients.

To bound the true-minus-surrogate derivative, let `d_i^+=u_iP_i^+`, `L=sum_i d_i^+`, and

\[
 \kappa_f=\sum_{ij}\sqrt{d_i^+}\,\beta_{ij}\sqrt{d_j^+},
 \quad\kappa_e=\sum_i d_i^+\rho_i^+,
 \quad\kappa=\kappa_f+\kappa_e.
\]

The first expression bounds the weighted operator norm of the uncertain landmark projection; the second follows because the unknown weighted residual is PSD and its spectral norm is at most its trace.

Working on active coordinates, the scaled inverse-response vector is

\[
 x=D^{-1/2}q=(I+D^{1/2}SD^{1/2})^{-1}D^{1/2}{\bf1},
\]

so `||x||_2 <= sqrt(L)` since `S>=0`. For the surrogate vector `x_*` with the same true `D`, the resolvent identity gives

\[
 \|x-x_*\|_2\le\kappa\sqrt L.
\]

Decompose

\[
 (Sq)_i-(S_*q_*)_i
 =[(S_0-S_*)q]_i+(Eq)_i+[S_*(q-q_*)]_i.
\]

Weighted Cauchy on the first and third terms, and the PSD Cauchy inequality on the middle term, prove the simultaneous **all-coordinate** bound

\[
 \boxed{|k_i-k_i^*|\le
 \sqrt{L\sum_jd_j^+\beta_{ij}^2}
 +\sqrt{L\rho_i^+\kappa_e}
 +\kappa\sqrt{L\sum_jd_j^+(S_*)_{ij}^2}.}\tag{3}
\]

The inequality holds also when the target coordinate has zero dose. Together with interval bounds for `z0`, `F`, `P_i` and `k_i^*`, (2)–(3) produce intervals `[g_i^-,g_i^+]` enclosing the physical gradient of `G` at `x`. No source-aware gradient, sign, independent noise, or true rank enters the compiler.

### Global all-actions regret dual

On `y>=0, sum y<=delta`, the extreme points are the zero action and `delta e_i`. Consequently an exact source-independent upper bound for *all future interventions* is

\[
 \boxed{\sup_{y\ge0,\,\sum y\le\delta}[G(y)-G(x)]
 \le \max\left\{-\sum_jx_jg_j^-,\ 
 \max_i\left[(\delta-x_i)g_i^+-\sum_{j\ne i}x_jg_j^-\right]\right\}.}\tag{4}
\]

Only the gradient intervals at the chosen `x` are needed. The task-specific numerical optimizer merely proposes an admissible rational dose vector; a failed numerical optimizer may produce a less useful certificate but cannot invalidate (4). Every final reward, derivative, and regret calculation uses rational arithmetic and outward interval quantization (`1e-14` grid).

### Actual executed *continuous* tasks

`astra_psd_continuous_opt.py` ran **four** newly specified 128-dimensional price objectives through the same 510-reaction learner. The candidate proposal uses SciPy SLSQP and is rounded back into a physically allowed rational dose vector. Independently, the exact hidden four-node source calculated both the actual chosen reaction and **all 128 native physical gradient components** for each task; all 512 gradients lay inside the learner's intervals.

| Task | Nonzero actuator doses in chosen action | Certified global continuous regret | Hidden-source tangent gap (verification only) |
|---|---:|---:|---:|
| 0 | 2 | `8.851700058621296e-5` | `6.277025391836922e-10` |
| 1 | 3 | `1.1361230573139773e-4` | `4.302624317070987e-9` |
| 2 | 5 | `8.028347099727881e-5` | `8.4010228984256e-7` |
| 3 | 8 | `1.2617181476021398e-4` | `2.367026930630487e-7` |

All four task certificates bound regret against the **entire continuous simplex**, not a finite action menu. All later source calls by the learner: **zero**. The hidden-source tangent gaps are independently computed *upper bounds* on realized regret, **not** learner certificates and not directly measured optimality gaps.

The final fifth candidate optimization from an initial exploratory five-task run was abandoned when numerical SLSQP stalled. The four-task controlled rerun completed and wrote its results. No fifth-task claim is made.

## 4. Second attack: an information-optimal task-directed experiment

The earlier fixed-two-landmark information-limit construction has four passive controls and two sources `+` and `-` that return **the same 14 acquisition reactions**, even in exact arithmetic. A newly specified two-action decision chooses either no intervention or equal doses `u_2=u_3=1/10`, paying a fixed task cost `2/25` for the latter.

Source `+`: `Z(pair)=105/106`; net pair gain `1/106-2/25=-187/2650 <0`, so *do nothing* is optimal. Source `-`: `Z(pair)=5/6`; net pair gain `1/6-2/25=13/150 >0`, so *perform the pair* is optimal.

Any deterministic learner that makes this decision from those 14 readings without another query suffers worst-case regret at least

\[
 \min(187/2650,13/150)=187/2650\approx0.0705660
\]

across the two equally compatible sources; the minimax randomized maximum **expected** regret equals `2431/62500≈0.038896`, still strictly positive.

A **single additional** allowed scalar experiment at precisely that pair gives native reactions differing by `4/21`, overwhelmingly more than twice the allowed raw error `1e-8`. The learner converts its new raw reading and the already retained baseline to sound response intervals. In both sources the net reward interval has an unambiguous sign: the post-reading choice is **certifiably optimal** over the two-action menu. Therefore 1 query is necessary and sufficient for this exact task with this two-source ambiguity; it is *not* sufficient for unrelated interventions or for acquiring the unrestricted network.

This demonstrates why sensing should be **task-directed** if a source remains available: full global rank identification is neither always needed nor always affordable.

## 5. Precision stress and strong alternative

`astra_psd_sharp_noise_stress.py` ran twelve additional synthetic reports at absolute raw-reaction tolerances `1e-8`, `1e-7`, `1e-6`, and `1e-5` (three correlated error patterns each). All 12 acquired usable intervals, all 144 held-out responses were covered, and all checked saddle signs passed in this fixture. Larger noise produced wider, sometimes weakly informative intervals. This finite stress test is not a theorem that these tolerances suffice on arbitrary source geometries. At still poorer precision, the underlying singleton or landmark inversion may have to return `UNKNOWN`.

**Strong alternative.** Fully informed active noisy-PSD completion and adaptive Nyström methods, including Bhargava–Ganti–Nowak (AISTATS 2017, <https://proceedings.mlr.press/v54/bhargava17a.html>), are important pre-existing comparators. A general robust convex optimizer may solve (1) without our positive-saddle shortcut and tighten the completion bound further. Another retaining learner with the same observations, physical class, and computational resources can run the very same global gradient/compiler method and tie these results. A source that remains available may permit much cheaper direct task-directed experiments than the paid 510-call upfront programme. The geometric elliptope arguments, robust optimization, concavity and gradient-dual certificates have significant established ancestry; no algorithmic priority claim follows.

## 6. Actual remaining obstacle

The strongest new operation is **continuous, globally guaranteed intervention choice from finite-noise scalar measurements, without knowing the source's internal dimension, its exact rank, or the later prices at acquisition time**. It changes what retained experience can *do*, but only within a **supplied** affine rank-one passive-network class. A finite archive of seemingly correct responses cannot establish that class globally: a smooth hidden activation can agree on all acquired histories and differ later while preserving passivity. There is no general self-certifying causal invention agent, physical demonstration, or 9–10/10 civilisation-level breakthrough.

The scientific next attack should therefore target **acquiring or warranting the admissible physical source class** with appropriate operating-range and regularity contracts, or reducing the number of source readings with an equally strong finite-noise continuous certificate. Within the given class, adaptive source querying when task-specific regret is high is the more promising extension than accumulating more fixed synthetic examples.

## 7. Executable science (files actually created)

- `astra_psd_task_sharp.py` and `_results.json`: 50 sound held-out nonlinear responses, exactly checked rank-one saddle, previous-interval comparison.
- `astra_psd_task_sharp_decisions.py` and `_results.json`: 20 future tasks, 840 disjoint menu choices, robust bounds with no new calls.
- `astra_psd_continuous_opt.py` and `_results.json`: globally valid gradient enclosures and full-simplex regret, independent exact physical response and physical derivative checks (512 components).
- `astra_psd_optimal_active_probe.py` and `_results.json`: two-source indistinguishability and the source-native, information-optimal single extra reading.
- `astra_psd_saddle_counterexample.py` and `_results.json`: exact sign-guard failure and convex-dual witness.
- `astra_psd_sharp_noise_stress.py` and `_results.json`: twelve source-noise settings, 144 held-out checks.
- Retained unmodified prerequisite `astra_noisy_psd_tube.py`, `astra_noisy_psd_tube_results.json`, and `astra_rankone_one_pair_results.json` contain the actual source data and original finite-noise acquisition.

**Data separation:** Independent hidden-source calculations are made after acquisition and excluded from the prediction or gradient oracle. All source call counts refer to one scalar `R` from one reset intervention. Source replication, the 510 initial calls, subsequent optional single paid probe, vector arithmetic, exact rational bit cost, solver evaluations, and file storage cannot be treated as free physical resources. **No GitHub repository write was performed.**
