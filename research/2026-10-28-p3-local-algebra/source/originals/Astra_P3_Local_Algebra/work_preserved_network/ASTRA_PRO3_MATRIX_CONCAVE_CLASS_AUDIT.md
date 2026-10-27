# Astra Pro3 — Source-native physical-shape certification, model-independent continuous interventions, and a dose-threshold identification obstruction

**27 October 2026 — continuing research.** Research result and executable controls, not a physical discovery or claimed historical algorithmic priority. Scope: exact rational synthetic four-node passive conductance networks, 128 nonnegative interventions with combined dose `delta=1/5`, native *scalar* Schur reactions with deterministic correlated bounded errors. The previous 510-reaction model-based source remains preserved separately. The new mechanism does not assume affine, rank-one or known network dimension. It **does** require an independently warranted matrix-concavity and derivative-magnitude contract; that distinction is central.

## Scientific question

The earlier Pro3 mechanism learned a conditional rank-one affine-PSD response model from 510 scalar reactions, then compiled unknown future continuous costed intervention tasks from noisy Gram uncertainty. The unresolved assumption was that the real physical source belongs to the supplied affine rank-one model. Could an agent certify useful continuous interventions with much less structural identification, and how much can raw source experiments actually warrant the structural premise?

**Answer within precise scope:** a paid 128-direction finite-difference audit certifies global regret for any smooth, uniformly SPD, **Loewner-concave conductance matrix**, without learning the matrix, its rank, or the signs/orders of nonlinear responses. A source-only 290-reaction programme selected an intervention on a nonaffine source having rank-two actuators and certified all-continuous-action regret <= `0.00020436670977238956`. After a later price change, a zero-new-reading certificate was weak (`0.01638393978464412`); successive task-directed line-search/readout audits reduced it to `0.00030031088209332224` after 932 cumulative readings. An independent determinant/Cramer verifier replayed all 932 records and all six global derivative certificates (first task plus five price-task audits).

**Obstruction:** 124 different monotone passive, C² actuators satisfy *the same global first- and second-derivative magnitude bounds* and all 932 scalar historical reactions, but have threshold activations invisible at every historical dose. They violate Loewner concavity. Across this observationally compatible source family, **every single action** has worst-case regret at least `0.0005088883759957529` for the new task, so the concavity-class regret certificate cannot honestly transfer to the broader physical class. Owing to the total-dose limit, any allowed experiment can excite at most one hidden threshold; 124 additional high-dose experiments are necessary, in the worst case, to exclude all members of this *finite known* threshold alternative family. This is an information/actuation limitation, not a claim of a general causal-learning lower bound.

## 1. Observation and physical shape contract

The native action is a nonnegative vector `u in R_+^n`, `sum_i u_i<=delta=1/5`. A resettable, source-stable apparatus returns exactly one reported scalar `r(u)` satisfying

\[
|r(u)-R(u)|\le\epsilon=10^{-8},\qquad
R(u)=\frac32+\frac1{Z(u)},\quad
Z(u)=e^TQ(u)^{-1}e.
\]

The physical `Q(u)` is symmetric positive definite and twice differentiable on a neighborhood of the dose simplex. The learner is **supplied** (or an independent apparatus/circuit argument must certify):

1. `Q(u) succeq m I` uniformly (`m=1` in the experiment), and the native readout/reaction identity remains valid.
2. The full vector function `u -> Q(u)` is Loewner-concave: `Q(tu+(1-t)v) succeq tQ(u)+(1-t)Q(v)` for every admissible `u,v,t`.
3. Per-coordinate matrix derivative caps `||Q_i(u)||_2<=L_i`, `||Q_ii(u)||_2<=B_i`, for all allowed `u`. There is **no** supplied unknown microscopic coefficient array or network dimension.
4. Controlled intervention doses and reproducibility, fixed sensor error bound and reliable system reset. Correlated or adversarial errors are permitted.

**Neither finite success nor passive positive definiteness proves item 2.** That is the precise open physical warrant.

The native report `r` gives the sound interval

\[
Z(u)\in\Big[\frac1{r+\epsilon-3/2},\ \frac1{r-\epsilon-3/2}\Big],
\quad r-\epsilon>3/2.
\]

## 2. Physical concavity-to-response theorem

**Theorem 1 (shape transfer).** Set `G(u)=Z(0)-Z(u)-c^T u` for any nonnegative, task-selected vector of linear actuator prices `c`. Under the preceding physical assumptions, `G` is concave over the entire dose simplex, and

\[
-M_i\le \frac{\partial^2 G}{\partial u_i^2}\le0,\qquad
M_i=\|e\|_2^2\big(2L_i^2/m^3+B_i/m^2\big).
\]

**Proof.** Matrix inversion reverses Loewner order and is matrix convex on positive definite matrices. Combining it with `Q(tu+(1-t)v)>=tQ(u)+(1-t)Q(v)` yields `Q(tu+(1-t)v)^-1 <= (tQ(u)+(1-t)Q(v))^-1 <= tQ(u)^-1+(1-t)Q(v)^-1`. Taking the `e` quadratic form proves that `Z` is convex and `G` is concave. Put `p=Q^-1e`. Direct differentiation gives

\[
Z_i=-p^TQ_i p,\quad
Z_{ii}=2p^TQ_iQ^{-1}Q_i p-p^TQ_{ii}p.
\]

Since `Q_i` is symmetric, `p^T Q_i Q^-1 Q_i p>=0`; Loewner concavity gives `Q_{ii}<=0`, so `Z_ii>=0`. Uniform `||Q^-1||<=1/m` and the two derivative caps yield `Z_ii<=||e||²(2L_i²/m³+B_i/m²)`. Prices have no second derivative. QED.

This covers nonaffine saturation functions `a_i(u)=u/(1+k_i u)` multiplying arbitrary PSD actuator matrices `V_i`, including rank >1. It also covers more general cross-coupled matrices if their **joint** Loewner concavity and derivative caps are independently warranted.

## 3. From 129 scalar readings to all-actions regret

**Theorem 2 (source-only, no learned inverse).** For any candidate `x` with `sum x<=delta-max h_i`, query `R(x)` and the `n` separate reactions `R(x+h_i e_i)` with `h_i>0`. Let the old/new reciprocal intervals be `[a0,b0]` and `[ai,bi]`. Define

\[
\ell_i=\max\left\{-c_i,\frac{a_0-b_i}{h_i}-c_i\right\},\quad
u_i=\frac{b_0-a_i}{h_i}-c_i+\frac{M_i h_i}2.
\]

Then **simultaneously for all** `i=1,...,n`, `ell_i <= partial_i G(x) <= nu_i`, with no independence between the native errors. Moreover

\[
\boxed{\sup_{y\ge0,\ \mathbf 1^T y\le\delta}[G(y)-G(x)]\le
\max\Big\{-\sum_i x_i\ell_i,\ \max_j[(\delta-x_j)\nu_j-\sum_{i\ne j}x_i\ell_i]\Big\}.}
\]

**Proof.** Along the `i`th coordinate, integrate `G_i(x+t e_i)` from 0 to `h_i`. Because `-M_i<=G_ii<=0`, `G(x+h_i e_i)-G(x)` differs from `h_i G_i(x)` by a term in `[-M_i h_i²/2,0]`. Convert both native reports to reciprocal intervals and subtract; the linear price contributes `-c_i`. If actuation is monotone (as in the executed fixture), `-c_i` additionally bounds the benefit gradient from below; if monotonicity is not supplied, **omit the max with -c_i** and retain the raw finite-difference lower endpoint. In the software, monotonicity is physically warranted because each positive intervention adds PSD conductance. Finally, concavity gives `G(y)-G(x)<=nabla G(x) dot (y-x)`. The linear function on the right is maximized over the simplex at its vertices `0,delta e_j`; apply lower gradient endpoints to negative coefficients and upper endpoints to positive coefficients. QED.

The proposed `x` can come from any heuristic, external optimizer, earlier possibly mistaken model, or earlier scalar screening. *Only the audit* confers the numerical certificate. The apparatus must be available when auditing; this is not a no-new-readings source-expiry result.

## 4. Executed nonaffine, rank-two source

The held-out exact network has four nodes and 128 actuator coordinates:

\[
Q(u)=Q_0+\sum_{i=0}^{127}\frac{u_i}{1+\kappa_i u_i}V_i,
\qquad\kappa_i\in\{2/5,3/5,4/5,1,6/5,7/5\},\quad V_i\succeq0,
\]

where certain `V_i` have rank two. `Q_0>=I`. Every source reading is a rational 4x4 Schur reaction; the learner receives only the reported `R` (quantized to 12 decimals) and ±`1e-8` adversarial error. Before the source-aware verifier checks anything, the learner receives only the coarse caps

- `L_1=L_2=6`, `L_i=3` for all other controls;
- `B_i=30` for all controls, `m=1`;
- global Loewner-concavity, plus monotone PSD actuator response.

The cost-free first task selects two actuator coordinates from the **129 paid screening readings** (`R(0)` and 128 readings at individual amplitude `0.1`). A scalar reaction-only concave line-search requires 32 further new readings. At the proposal, all 128 coordinate finite differences require 129 more distinct native readings. All planned doses respect `sum u<=0.2`. Exact-rational sensor intervals certify the final continuous all-actions regret `0.00020436670977238956`. The true (verifier-only) concavity tangent gap is `0.000016874940709919353`; this is a physical numerical check and **not** the learner certificate. All 128 exact physical gradients are independently contained in the acquired intervals.

The next cost objective changes the prices for controls 1 and 2 to `1/4`, keeps control 90 free, and charges `1/50` for the others. The initial reused measurements give a correct but weak worst-case certificate (`0.01638393978464412`). A sequence of task-directed Frank–Wolfe-like vertex choices and native-reaction ternary searches chooses new continuous actions, then requests complete audits before certifying them:

| New task stage | Cumulative native R calls | Certified global continuous regret |
|---|---:|---:|
| Old observations and first new-task audit (all cached) | 290 | 0.01638393978464412 |
| After 1 directional refinement | 452 | 0.001246759430469442 |
| After 2 | 614 | 0.0005719544927154956 |
| After 3 | 773 | 0.0005317233554483875 |
| After 4 | 932 | 0.00030031088209332224 |

All six independent exact gradient-verifier checks passed (768 gradient components), and each native reading's exact source value lies in its reported adversarial `R` enclosure. **No objective optimum was supplied to the learner.** Source-aware tangent gaps in results are independent verifier-only bounds, not performance guarantees transferred to arbitrary sources.

Calls per stage include all new line-search and finite-difference readings; reused observations are not charged twice. Each physical experiment returns one scalar, not a hidden potential or latent Gram coefficient. Deterministic error signs are allowed to be correlated, so repetition does not improve the nominal noise contract. Near-optimal interventions are source/task-specific; no uniform improvement over the earlier model-dependent 510-reading transfer follows.

## 5. Necessary scientific failure: 124 hidden monotone gates

The omitted physical regularity class matters. Fix any one of 124 as-yet-unexcited controls `j in {3,...,127}\{90}` and define a second source

\[
Q^{(j)}(u)=Q^{(0)}(u)+50(u_j-1/10)_+^3e_0e_0^T.
\]

Every extra source is **passive, C², coordinatewise nondecreasing, uniformly SPD and obeys the same supplied matrix derivative magnitude caps**. Proof: the gate derivative is `150(u_j-0.1)_+²<=1.5`, the second derivative is `300(u_j-0.1)_+<=30` over `u_j<=0.2`. For all 124 chosen `j`, the original source's `V_j` is supported entirely on coordinates 1,2,3 rather than e0; therefore the gate and original actuator derivative matrices occupy orthogonal blocks, so their operator norms combine as a maximum, not a sum. `||Q_j||<=max(||V_j||,1.5)<=3` and `||Q_jj||<=max(2k_j||V_j||,30)<=30`. Other coordinates retain their caps. The added term is PSD and monotone. It is **not Loewner-concave**: its second derivative is positive on the e0 direction.

All 932 recorded source experiments, including the line-search proposals, applied `u_j<=0.1` at each of these 124 candidate positions. Every source `Q^(j)` therefore returns the **exact same noiseless native reaction** on every historical experiment, not merely the same within the error tolerance. The earlier 510 protocol also kept each coordinate <=0.1, so it would not eliminate any gate.

For `u=delta e_j` the scalar port reaction changes by **exactly** `R^(j)(u)-R^(0)(u)=1/20`: the new shunt contributes `1/20` directly to the Schur effective boundary conductance. The 124 compatible alternatives have previously unspecified post-task witness rewards at least

\[
A_{\min}=0.01727138260600682.
\]

Using only the native noisy interval at the final baseline action and the **rational** all-actions regret certificate for the concave base source, an upper bound on *any* baseline source reward is

\[
U_0=0.016762494230011065.
\]

**Theorem 3 (operational indistinguishability with regret).** Let `P` be the 124 previously unexcited gate positions. For *every* single action `u>=0, sum u<=0.2`, at most one `j in P` can have `u_j>0.1`, so some gate position `j` remains unactivated. For that physically compatible source, `G^(j)(u)=G^(0)(u)<=U_0`, whereas `G^(j)(0.2e_j)>=A_min`. Hence

\[
\boxed{\sup_{j\in P}\big[\max_yG^{(j)}(y)-G^{(j)}(u)\big]
\ge A_{\min}-U_0 > 0.0005088883759957529.}
\]

The inequality is uniform over **all single deterministic actions**, including ones chosen using unlimited computation on the 932 observations. It does **not** assert a randomized expected-regret lower bound or apply beyond the specified compatible family without further proof.

**Native-query lower bound.** Every allowed reaction query excites at most one candidate position above the gate threshold, because the total dose is `0.2` while each excitation requires strictly more than `0.1`. Consequently an adaptive deterministic or randomized strategy that must *certify absence of all 124 candidate gates in the null source*, under a worst-case correctness contract, must inspect every candidate above threshold. Its worst-case number of additional gate-sensitive source preparations is at least 124. A full-dose test of each position has raw-reaction gap `0.05`, far exceeding twice `1e-8`; in the *specified known two-form candidate family* such tests are sufficient to distinguish the gates. This does not establish a 124-test sufficient strategy when the benign source baseline responses are themselves uncalibrated or the allowed deviations include arbitrary unknown mechanisms.

This counterexample disproves the tempting inference that many passive, monotone, smooth-in-magnitude experiments can **self-certify** the missing global concavity shape. To evade the lower bound one needs a stronger independently justified actuator-shape contract, a physically different excitation interface or a larger dose budget permitting pooled threshold activation. Merely running the old model fitter harder cannot supply those missing observations.

## 6. Equal-information competitor and prior art

An equally informed retaining learner can implement the finite-difference intervals, convexity/concavity dual certificate, adaptive line-search and gate tests *exactly*. They are based on classical inverse-matrix convexity, zeroth-order optimization, Lipschitz-gradient finite differences and resource-limited group testing. Related sources: Vandenberghe–Boyd, *Semidefinite Programming* (1996), <https://web.stanford.edu/~boyd/papers/sdp.html>; Bach–Perchet, *Highly-Smooth Zero-th Order Online Optimization* (2016), <https://proceedings.mlr.press/v49/bach16.html>; Karabag–Neary–Topcu, *Smooth Convex Optimization Using Sub-Zeroth-Order Oracles* (2021), <https://ojs.aaai.org/index.php/AAAI/article/view/16499>. No priority, scientific-device, general-intelligence or architecture advantage is claimed.

The meaningful advancement of this continuation is *operation scope*: a 128-control nonlinear physical intervention can be audited for optimality using scalar physical reactions without learning the full source matrix or assuming rank-one/affine actuator action, while an explicit compatible family proves which part of the resulting knowledge cannot be purchased by those readings. It is a finite-noise, finite-dose operational theorem with honest class-dependence, not a global physical discovery.

## 7. Next mathematical attack

The strongest missing capability is to warrant shape information by another *physically cheap* observation channel, rather than infer it from finite boundary responses. One concrete attack is a circuit/actuator-level test producing certified Loewner upper bounds on `Q''(u)` over the whole dose domain from component specifications (or alternatively a source-wide operator envelope that leads to a nonconcave robust regret certificate). Another is a variable-dose-budget information theorem quantifying when group activation becomes physically possible and how additive response signals survive deterministic noise. Neither has been established for real hardware here.

## Reproduction and scope of preserved files

- `astra_matrix_concave_audit.py`: acquisition/calibration, exact-rational native source, 128 finite-difference audit, future price task reuse, first gate counterexample; writes `astra_matrix_concave_audit_results.json` and `_raw_trace.json`.
- `astra_matrix_concave_active.py`: independently specified price task, source-only directional refinement, all-audit certificates and 124-gate lower bound; writes `astra_matrix_concave_active_results.json` and `_raw_trace.json`.
- `astra_matrix_concave_independent_verify.py`: separate determinant/Cramer's-rule source checker (does not call the learner's inverse/derivative routines); reads the saved 932-scalar trace, reconstructs six all-actions rational certificates and their 768 true gradients, checks all derivative magnitude caps and verifies the 124-source indistinguishability and regret lower bound; writes `astra_matrix_concave_independent_verify_results.json`.

Only exact-rational math is used for observation creation, learner bounds, external costed actions and verifier checks; decimals in summaries are displays. The true physical gradient/matrices and exact source rewards are never input to the learner. All results are synthetic-source calculations; physical instrument realization, newly established concavity of any actual device, and safe zero-query transfer after source expiry remain open.

## 8. Next executed attack: dose-constrained pooling transition (changed physical interface)

The 124-query lower bound arose specifically because no allowed input could activate two gate locations simultaneously. Consider the **hypothetical stronger instrument** that accepts total dose `D` rather than `1/5`. Keep each gate's activation threshold at `tau=1/10`, and assume **at most one gate is present**, with its position unknown among the 124. Also supply a **trusted exact null-source reaction predictor for each proposed grouped action**. This predictor is an extra information contract, *not* acquired from the historical 932 scalar reactions.

At amplitude `a=101/1000` on every position of a set `A`, the extra shunt contributes to the actual four-node scalar port reaction

\[
\Delta R=50(a-\tau)^3=\frac1{20{,}000{,}000}=5\times10^{-8}
\]

if and only if the unique hidden gate lies in `A`; otherwise it contributes zero. This strictly exceeds `2epsilon=2e-8`, so a deterministic bounded-error raw-reaction observation can classify the group with no independent-noise premise. Physical feasibility requires `|A|a<=D`. Therefore each query can test at most `b=floor(D/a)` positions, and block scanning plus binary subdivision of a positive block has worst-case query count at most `ceil(124/b)+ceil(log_2 b)`.

`astra_activation_pooling.py` executed this on the exact-rational nonlinear four-node source at each newly stipulated dose budget, using Schur determinant evaluations (not mock sensor values), and reported correlated bounded-error scalar reactions:

| Hypothetical total-dose budget | Gates per group | Tests if no gate | Worst observed tests for selected hidden gates | Proved worst-case ceiling |
|---|---:|---:|---:|---:|
| `0.2` (original) | 1 | 124 | 124 | 124 |
| `0.4` | 3 | 42 | 42 | 44 |
| `0.6` | 5 | 25 | 27 | 28 |
| `1.0` | 9 | 14 | 17 | 18 |

The improvement does **not** contradict the 124-query obstruction: the observation/actuation interface has changed, the component derivative bounds used in earlier all-actions certificates are not extended automatically to the larger domain, and the exact null-reaction predictor is an additional supplied capability. The experiment clarifies which new scientific instrument properties would make grouped identification possible. It does not show that the original Astra source can safely receive higher doses or that a real device supplies a trusted null predictor.

Files: `astra_activation_pooling.py`, `astra_activation_pooling_results.json`. This line is independent of the previous zero-query future transfer objectives; it is a forward-experiment identifiability control.
