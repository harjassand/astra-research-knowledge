# Astra Interim Pro3 — Sharp precision frontier and native nonlinear transfer

**26 October 2026, Australia/Brisbane.** Self-contained mathematical continuation of `ASTRA_INTERIM_PRO3_EXPERIMENT_COMPILER.md`. All software tests documented below executed locally in this workspace. These are **conditional mathematical results and analytic/software experiments**, not a new physical law, working scientific instrument, discovery of an unknown source model, or established historical priority. A fully informed conventional optimal-recovery or retaining-program implementation can make the same experiments and attain the same limits.

## 1. Why continue beyond exact query rank?

The previous scalar-task theorem computed the minimum exact number of symmetric full-vector actions for `tr(T S)` from the inertia of `T`. But algebraic feasibility alone did not solve the earlier decisive failure: an exact-rank-optimal experiment may magnify errors so badly that two physically distinct sources fit its full noisy transcript.

The new result closes **one important quantitative version** of that gap: it computes the **globally sharp worst-case precision after a fixed number of full-vector experiments** for an *entire symmetric operator-norm uncertainty ball*, including worst-case adversarial measurement errors and deterministic adaptive alternatives. It then transports this task compiler to an exact acquired Loewner interval and to a truly nonlinear forward primitive. The latter transport is *sound but not claimed globally sharp* over all nonlinear source procedures.

The legacy files `ACQUIRED_POSITIVE_OPERATIONS(1).md` and `acquired_batch_conditioning(1).py` were inspected in the predecessor turn. The latter has unavailable historical imports and was not replayed. The prior note directly treats exact vector observations and the spectral completion family; nothing here upgrades its merely noisy outer intervals to exact posterior descriptions. Astra's N997 admits a more general norm-and-history dual but does not supply this specialized signed-spectrum closed form. N996 assumes a distinct exact linear vector/**transpose** interface and learned operator-defect grammar. N1003's finite-field fresh-source guards and N1011's conditional comparison experiments have incompatible native contracts and are not silently invoked.

## 2. Sharp deterministic minimax theorem

**Native interface and prior.** Let the unknown source be a fixed real symmetric `n x n` operator

\[
S=S_0+H,\qquad H=H^\top,\quad\|H\|_{\mathrm{op}}\le R.
\]

`S0` and `R>0` are supplied and justified independently. When positivity is physically required, choose a compatible `S0` satisfying `S0 >= R I` (e.g. `(a+b)I/2` for an actual `[aI,bI]` contract). Each selected real source input `q` has `||q||2 <= 1` and the native output is `z=S q+e` with **arbitrary**, possibly source-, time-, and adaptivity-dependent error `||e||2<=eta`. There is no stochastic independence assumption. Each vector output contains `n` scalar readings. The later scalar task is

\[
L_T(S)=\operatorname{tr}(TS),\qquad T=T^\top.
\]

Let `lambda^+_1 >= ... >= lambda^+_p > 0` denote positive eigenvalues of `T` and `lambda^-_1 >= ... >= lambda^-_r > 0` the *absolute values* of its negative eigenvalues. Empty tails have sum zero. Write

\[
N_T=\|T\|_* = \sum_{j=1}^{p}\lambda_j^+ +\sum_{j=1}^{r}\lambda_j^-,\qquad
\operatorname{tail}_k(T)=\sum_{j>k}\lambda_j^++\sum_{j>k}\lambda_j^-.
\]

**Theorem (sharp precision–query frontier).** With `k>=0` native vector actions, every deterministic, possibly adaptive, uniformly valid decoder has worst-case absolute scalar error at least

\[
\boxed{\mathcal E_k^*(T)=\eta N_T+(R-\eta)\operatorname{tail}_k(T)}\quad\text{if }0\le\eta\le R.
\tag{1}
\]

One fixed nonadaptive task-specific experiment program achieves equality. If `eta >= R`, no experiment improves the worst-case radius `R*N_T` and zero actions are optimal. The statement covers the *minimax error across all sources and permitted errors*, not the generally smaller information interval after a lucky noncentral transcript. It uses unrestricted real probes; rational-only inputs, restricted finite catalogues, or precision-dependent excitation costs can alter the attainable value.

**Direct procedure.** Diagonalize `T`. For each `j<=k`, pair the `j`th positive direction `u+` of eigenvalue `lambda>0` with the `j`th negative direction `u-` of eigenvalue `-mu<0`, whenever both exist:

\[
q_j={\sqrt\lambda\,u_++\sqrt\mu\,u_-\over\sqrt{\lambda+\mu}},\qquad
 y_j=\sqrt{\lambda+\mu}(\sqrt\lambda\,u_+-\sqrt\mu\,u_-).
\tag{2}
\]

This is an allowed unit source input, `||yj||=lambda+mu`, and

\[
\operatorname{sym}(q_jy_j^\top)=\lambda u_+u_+^\top-\mu u_-u_-^\top,
\qquad \operatorname{sym}(A)=(A+A^\top)/2.
\]

An unpaired signed eigenvalue uses the unit eigenvector as `qj` and its signed eigenvalue times the eigenvector as `yj`. If `Z=sum_j sym(q_j y_j^T)`, then `E=T-Z` is exactly the omitted signed spectral tail, and `sum_j ||yj||=N_T-tail_k`. The executable estimator

\[
\widehat L=\operatorname{tr}(T S_0)+\sum_j y_j^\top(z_j-S_0q_j)
\tag{3}
\]

satisfies

\[
|\widehat L-L_T(S)|\le R\|E\|_*+\eta\sum_j\|y_j\|
=\eta N_T+(R-\eta)\operatorname{tail}_k(T).
\]

This constructs the promised *procedure*, not merely its cost.

**Matching source-and-noise witness for the compiled plan.** In the eigenbasis of `T`, define `H` diagonally with entries `eta*sign(lambda)` on the acquired signed eigen-directions and `R*sign(lambda)` on the unacquired eigen-directions (zero on the nullspace). It obeys `||H||op<=R` and every compiled input obeys `||H qj||=eta`. The two sources `S0 +/- H` can produce **identical central reports** `S0 qj`, using measurement errors `-Hqj` and `+Hqj`. Their requested answers differ by exactly `2 E_k*`. Thus the compiled certificate is not a loose error-propagation upper bound.

### 2.1 Why no other deterministic plan can do better

For fixed probes `Q=[q1,...,qk]`, the exact worst-case minimax radius over the symmetric ball and Euclidean observation-error balls is

\[
r_T(Q)=\max\{\langle T,H\rangle:\ H=H^\top,\ \|H\|_{\rm op}\le R,\ \|Hq_j\|_2\le\eta\ \forall j\}.
\tag{4}
\]

This follows from the midpoint of the attainable task-value interval and an adversary returning the central reports `S0 qj`. Finite-dimensional convex duality, with a strictly feasible point for `R>0` and `eta>0`, gives

\[
r_T(Q)=\min_{y_1,\ldots,y_k}
\left\{R\Big\|T-\sum_j\operatorname{sym}(q_jy_j^\top)\Big\|_*
+\eta\sum_j\|y_j\|_2\right\}.
\tag{5}
\]

An explicit `yj` always gives a valid upper certificate regardless of whether an optimizer converged. The `eta=0` case follows from the exact annihilator theorem, or as a limit.

For **arbitrary** `yj`, set `Z=sum sym(qj yj^T)` and `E=T-Z`. With `F=span(q1,...,qk)`, the quadratic form of `Z` vanishes identically on `F^perp`; hence `Z` has at most `k` positive and at most `k` negative eigenvalues. Write `Z=Z_+-Z_-` with `rank Z_+, rank Z_- <=k`. Then

\[
E=T-Z_++Z_-\succeq T-Z_+,
\qquad -E=-T+Z_+-Z_-\succeq -T-Z_-.
\]

Eigenvalue interlacing under a rank-`k` positive perturbation implies that the sum of positive eigenvalues of `E` is at least `sum_{j>k}lambda_j^+`, and the magnitude sum of its negative eigenvalues is at least `sum_{j>k}lambda_j^-`. Thus

\[
\|E\|_*\ge\operatorname{tail}_k(T).
\tag{6}
\]

Since `||qj||<=1`, `||sym(qj yj^T)||_*<=||yj||`; consequently `sum ||yj|| >= ||Z||_* >= ||T||_*-||E||_*`. If `eta<=R`, every candidate dual objective is therefore at least

\[
R\|E\|_*+\eta\sum_j\|y_j\|
\ge\eta\|T\|_*+(R-\eta)\|E\|_*
\ge\eta\|T\|_*+(R-\eta)\operatorname{tail}_k(T).
\]

Construction (2) attains this bound. The resulting equality proves **global** minimax optimality for fixed plans. Any deterministic adaptive policy has a fixed branch upon receiving the sequence of central reports; the sources `S0+H` and `S0-H` satisfying that branch's constraints follow exactly the same queries and reports, so adaptivity cannot escape (4). For `eta>=R`, choose `H=R*sign(T)`; every unit probe can be made consistent with its central report, leaving the full prior radius. This completes the lower bound.

The elementary constituents—spectral theorem, signed low-inertia approximation, interlacing, minimax linear optimal recovery—are established mathematics. We do **not** assert that theorem (1) has never been published in this exact measurement specialization.

### 2.2 A precision threshold compiler

For tolerance `epsilon`, return

\[
k_\min(\epsilon)=\min\{k\ge0:\mathcal E_k^*(T)\le\epsilon\},
\tag{7}
\]

or `IMPOSSIBLE_UNDER_CONTRACT` if the set is empty. This changes a planned experiment from *query-rank identification* to *exact task-precision resource allocation*. At `eta<R`, extra experiments are valuable exactly in proportion to the next omitted positive and negative spectral magnitudes; when both sequences are exhausted, the irreducible deterministic noise floor is `eta||T||_*`. The native procedure need only compute task eigenvectors once and issue the `k` highest-value paired actions.

## 3. Executed independent symbolic and numerical controls

`astra_sharp_precision_frontier.py` is standalone apart from `sympy,numpy`; `astra_sharp_precision_frontier_results.json` preserves the actual rational-orthogonal eight-dimensional task, algebraic experiment directions and decoders, source matrices, matching indistinguishable report vectors and gaps, and every task estimate.

In an eight-port control, `T` has signed eigenvalues `(16,9,4,1,-25,-16,-1,0)`, a rational orthogonal mixing, `R=1/4` and per-vector `eta=1/100`. Its exact theorem frontier is:

| New full-vector queries | Sharp absolute error radius | Native returned scalars |
|---:|---:|---:|
| 0 | 18 | 0 |
| 1 | 8.16 | 8 |
| 2 | 2.16 | 16 |
| 3 | 0.96 | 24 |
| 4 | 0.72 | 32 |

The saturated two-source separation is precisely twice each quoted radius. A tolerance of `1` needs three calls; `0.5` is impossible at the given fixed noise budget, even if the entire source is probed. A numerical stress test ran **1,500 independently sampled candidate decoder instances** (dimensions 2–8 and arbitrary candidate vectors) without finding a violation of the proved universal lower bound; it is only a software test, not an independent general proof.

**Old-information transfer.** If old *exact* responses to `F` equal `S0 F`, the surviving perturbations satisfy `H F=0` and are exactly an operator ball on `K=F^perp`. Compress `T` to `K` and apply (1). In a control with `T=diag(9,4,-16,-1)`, `R=0.5`, `eta=0.01`, one **aligned** old query `(3,0,4,0)/5` makes the optimal error after one new query `0.05`; one **misaligned** old query `e0` instead gives radius `0.70`. This is a central exact-history theorem; arbitrary historical noisy/noncentral sets are not silently replaced by such a ball.

**Restricted action grammar failure.** For `T=diag(1,-1)`, `R=0.5`, `eta=0.05`, one arbitrary real mixed experiment has exact optimal radius `0.10`. If the actual instrument offers only the two unit coordinate probes, the best one-call radius is `R+eta=0.55`. The indistinguishable-source witness is saved. Thus (1) is **not** a guarantee under a restricted catalogue; even the existence of a full-vector return does not grant arbitrary input directions.

## 4. Reuse over a genuinely acquired positive operator interval

The prior Astra positive-completion result obtains the *entire* operator family

\[
\mathcal S=[S_L,S_U]=\{S:S_L\preceq S\preceq S_U\}
\]

from **exact** old source vector observations plus an independently justified spectral contract. Put

\[
S_c=(S_L+S_U)/2,\quad D=S_U-S_L\succeq0,\quad W=\operatorname{ran}D.
\]

Every and only compatible source can be parameterized by

\[
S=S_c+\tfrac12 D^{1/2} X D^{1/2},
\qquad X=X^\top,\ \|X\|_{\rm op}\le1\text{ on }W.
\tag{8}
\]

This follows by taking the positive square root on `W`, using the interval inequalities and zero action on `ker D`. The unknown operator lives entirely on the *acquired uncertainty support*, not all `n` ports. The transformed later task is

\[
T'=\tfrac12D^{1/2}TD^{1/2}|_W.
\]

**Exact posterior query theorem.** If arbitrary real native probes `S q` are available noiselessly, the minimum new full-vector actions necessary for `tr(T S)` uniformly over the entire exact acquired interval is

\[
\boxed{q^*_{\rm posterior}=\max\{n_+(T'),n_-(T')\}.}
\tag{9}
\]

The reason is *not* that a new inverse or transformed-operator query primitive has become available. Querying `q` gives `S q-S_c q=D^{1/2} X D^{1/2}q/2`. On `W`, this is invertibly convertible (by known arithmetic and a known scale) to an `X u` vector query with `u=D^{1/2}q`. Conversely, any `u in W` can be realized up to nonzero scale through an allowed `q` in `W` because `D^{1/2}` is invertible there; scaling handles the `||q||<=1` constraint in the **exact** model. The previously proved inertia theorem applies to `X` and `T'`.

This provides a concrete bridge from **retained measurements** to *late unknown scalar operations* on a family of possible sources. It recognizes tasks fixed at zero new cost when `T'=0`, even if `T` itself is not zero. The dimension of the uncertainty support and signatures matter more than the number of historical samples.

**Sound noisy decoder over an exact or outer interval.** With native report errors `||zj-S qj||<=eta_j`, any `qj,yj` gives

\[
\begin{aligned}
\widehat L &=\operatorname{tr}(T S_c)+\sum_j y_j^\top(z_j-S_cq_j),\\
|\widehat L-L_T(S)|&\le \tfrac12\left\|D^{1/2}
\left(T-\sum_j\operatorname{sym}(q_jy_j^\top)\right)
D^{1/2}\right\|_*+\sum_j\eta_j\|y_j\|_2.
\end{aligned}\tag{10}
\]

This is a **certificate** for any interval containing the true sources; if it is an *outer approximation* of a smaller correlated noisy consistency set, it need not be sharp. The full exact-inertia lower bound (9) is **not** granted by an outer interval. In particular, the positive-completion note itself expressly forbids turning near-saturation or noisy endpoint estimates into exact forced actions.

### Executed Schur-complement completion

From a supplied `I <= S <=3I` and one exact old response `S e0=(2,1/2,0,0)`, the generalized Schur complement obtains the exact posterior endpoints

\[
S_L=\begin{pmatrix}2&1/2&0&0\\1/2&5/4&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix},\quad
S_U=\begin{pmatrix}2&1/2&0&0\\1/2&11/4&0&0\\0&0&3&0\\0&0&0&3\end{pmatrix},
\]

with `D=diag(0,3/2,2,2)`. The exact PSD compatibility was verified by **all rational principal minors** (not untrusted floating eigenvalues). A later `e0-e3` cross observable has `T'=0` and is known exactly with zero new source calls. A later task `T=diag(0,1,-1,0)` has transformed signature `(1,1)` and requires one new query. A normalized mixed probe and decoder give a sharp **new scalar error radius `0.002`** when its vector response error is `eta=0.001`, compared with a prior-only sharp radius `1.75`. Two sources within the **exact** acquired interval and compatible with the *same* new reported vector differ by `0.004` in the task, certifying the lower bound. That control paid **one historical vector call plus one new four-coordinate vector call**, with zero newly invented calibration calls. `astra_posterior_interval_compiler.py` and its JSON preserve the endpoints, PSD checks, decoder and adversarial witnesses.

## 5. A compiler for native nonlinear *forward* experiments

It would be invalid to claim that a nonlinear physical or software source automatically offers `S q` as one primitive. The next construction instead uses only a native forward map `F: R^n->R^n`, stable near a chosen operating point `x`, with **independently justified** third-derivative and error bounds:

\[
\|D^3F(z)[q,q,q]\|_2\le M_3\quad(\|q\|_2\le1,
\ z\text{ on the admitted probe segment}),
\]

and each forward report within Euclidean error `delta` of the true `F(z)`. It seeks the action of the local Jacobian `S=DF(x)`, which is known to be symmetric **only when a separate source contract justifies that** (for example, an exact gradient-source law). Two *actual forward* calls supply

\[
\widehat z(q,h)={\widehat F(x+hq)-\widehat F(x-hq)\over2h}.
\]

Taylor's theorem and the deterministic output-error triangle inequality imply

\[
\boxed{\|\widehat z(q,h)-S q\|_2\le
\eta_{\rm eff}(h)={M_3 h^2\over6}+{\delta\over h}.}
\tag{11}
\]

For positive `M3,delta` and permitted `0<h<=hmax`, the continuous optimal step for this **particular central-difference certificate** is

\[
h_* = \min\{h_{\max},(3\delta/M_3)^{1/3}\}.
\tag{12}
\]

Finite rational probes and steps can be rounded and the resulting certificate recalculated exactly. For `k` desired native Jacobian-vector actions, issue `2k` actual `F` calls, then use (3) with `eta=eta_eff(h)`. This is a *sound reduction* from a nonlinear source into the symmetric uncertainty compiler. It is **not** proof that central differencing is globally optimal among all nonlinear algorithms or that a third-derivative bound was empirically acquired.

**Executed six-port nonlinear source.** The source-aware checker contains a positive symmetric but hidden `S`, a hidden coefficient `alpha_true=3/20`, and a genuinely nonlinear gradient law `F(u)=S u+alpha_true*u^{\odot3}`. The learner is supplied only a valid `||S-2I||<=1/4`, `M3=6/5`, forward observation error `delta=10^-6`, symmetry/gradient contract and a maximum input step of `0.1`. An unknown later aggregate task has signed eigenvalues `(144,9,-25,-16,0,0)` under a rational orthogonal mixing. The compiler issues **two rational unit response directions** through **four rational native forward evaluations** at `±h q` with `h=7/500=0.014`, close to the certificate optimum `0.013572...`. It stores all four actual noisy outputs and their independently charged error vectors. The obtained action bound is `eta_eff=0.000110628571...`.

The resulting task has **certified error <=0.02146194286** against requested tolerance `0.03`; the checker-computed actual error was `0.00463536390`. A one-response-action version has certified bound greater than `0.03` in the declared abstract spectral compiler. Four full-vector forward readings each return six scalars: **24 returned scalars**. Central-differencing all six Jacobian columns would issue twelve forward calls and return 72 scalars. This is a source- and task-conditional workload reduction; a retaining program with the same contracts can use this exact procedure and tie. The private source formula, chosen `S`, and true output are used **only** by the checker, not as the learner's observations.

## 6. A smooth strongly convex no-go theorem for unguarded transfer

A simple analytic obstruction exposes a serious source-law-acquisition limit even within conservative, monotone physical response classes. **For every finite list of old query locations, including possibly the future operating point itself, there exist two smooth, strongly convex one-dimensional potentials whose gradient values agree at all those locations but whose Hessians differ at the future point.** Their gradients can therefore be perfect matches for the entire old source transcript, while their local linear-response laws disagree. One obtains a multidimensional analogue by adding independent positive quadratic coordinates.

**Construction and proof.** Let the future location be `x_*`, choose `r>0` smaller than the distance from `x_*` to every *other* distinct queried location, and put `f(s)=s^2(1-s^2)^6/2` on `|s|<1`, zero outside. Let `Phi0(t)=lambda*t^2/2` and

\[
\Phi_1(t)=\Phi_0(t)+\begin{cases}
\gamma r^2 f((t-x_*)/r),&|t-x_*|<r,\\0,&\text{otherwise}.
\end{cases}
\tag{13}
\]

The bump and its first five derivatives vanish at its endpoints, so `Phi1` is globally `C^5`. At `x_*` its *gradient perturbation* is zero but its **second derivative perturbation is exactly `gamma`**, because `f'(0)=0, f''(0)=1`. At every other old query the bump is identically zero, so *all* old native gradient responses coincide. The explicit polynomial derivative

\[
f''(s)=91s^{12}-396s^{10}+675s^8-560s^6+225s^4-36s^2+1
\]

obeys `|f''(s)|<=1984` on `[-1,1]` by the coefficient absolute-sum bound. If `lambda>1984 gamma>0`, both potentials are uniformly strongly convex, with gradient-derived local response positive. Their native old data still cannot distinguish their future Hessians. The finite benchmark used `lambda=2`, `gamma=1/1024`, `x_*=1/2`, `r=1/8`, and six retained locations including `x_*`. It verified **exactly identical** old gradients and different future local response values `2` versus `2+1/1024`, with conservative convexity lower bound `1/16`.

This is an indistinguishability theorem, not a claim that the difference cannot become small. A **genuine uniform smoothness bound** changes the permitted bump magnitude as `r` shrinks; in particular, the fourth derivative of the potential (third derivative of its gradient) scales as `gamma/r^2`. The new nonlinear reduction deliberately **supplies** a suitable higher-derivative contract; finite measurements alone cannot justify its unrestricted validity. An old pointwise measurement at the same bias is not a derivative measurement.

## 7. Information limits, remaining gaps and fair comparison

**What the learner actually obtains:** The original positive-response work acquires a *complete operator consistency family* from exact historical actions and a spectral promise; the new query theorem compiles that family and a previously unknown late scalar task into a minimal noiseless vector procedure and a sound noisy decoder. The source-fidelity bound, error budget and instrument-language permissions remain external contracts. The nonlinear bridge obtains *bounded local Jacobian actions* through actual permitted forward calls, without assuming native derivatives. No unseen physical derivative, instrument contract, unknown task distribution or universal mechanistic explanation is inferred from finite records.

**What fails:** The real unrestricted-field precision formula need not hold for rational-only or catalogue-restricted actions, total energy constraints, heterogeneous action errors, non-symmetric matrices, drifting sources, strongly coupled observation errors beyond individual enclosure semantics, or nonconvex/branching posterior classes. Historical noisy outer Loewner intervals generally only support upper estimates, not sharp query lower bounds. Smooth positive-gradient sources can still hide different future derivatives from finite earlier pointwise records. The reported forward-source compiler's optimality is limited to its declared *derived Jacobian-vector* experiment model, not all clever nonlinear native procedures or source-aware algorithms.

**Equally informed competitor:** A conventional optimal-recovery procedure, retained code, or source-model search with precisely the same prior, action grammar, old readings, actual error contract and late task can construct the same signed spectral pairs, same interval compression, same central differences and same minimax estimator. That method **ties** the theorem. An incumbent granted source formulas or a richer derivative/transpose instrument may beat the measured call counts. Thus this contribution is an explicit reusable *representation-to-experiment compiler* with sharp scoped information limits, **not** evidence of a proprietary architecture beating the strongest retaining baseline.

**Most leverageable next unresolved programme:** the learner would need to **acquire and falsify usable source contracts**, particularly symmetry, convex uncertainty geometry and derivatives/error calibrations, from interventions whose costs can be amortized over a semantically restricted future task family. Without a promise on which future tasks matter, no `k<n` old vector measurements can improve the *uniform worst-case* error over all normalized rank-one future tasks: choose a unit vector in the untouched input orthogonal complement and task `T=vv^T`. This elementary no-free-lunch barrier makes scientifically meaningful task languages or task distributions essential, rather than optional engineering. The conditional exact-interval theorem is most useful when real source observations genuinely shrink the width `D` on future relevant directions.

## 8. Executed and preserved work

All following files exist in `/mnt/data` and were executed in this turn. Their results are not just advertised future filenames. No old `/workspace/scratch/...` link is treated as current.

- `astra_sharp_precision_frontier.py` — exact rational/algebraic task compiler, sharp matched adversaries, central exact-history comparison, restricted input grammar counterexample and 1,500 numerical lower-bound stress cases.
- `astra_sharp_precision_frontier_results.json` — complete exact symbolic matrices, probes, decoders, reports, matching error witnesses and precision threshold decisions.
- `astra_posterior_interval_compiler.py` — full Schur-complement reconstruction, exact rational PSD principal-minor tests, late zero-/one-query tasks, and an actual sharp two-source noisy witness.
- `astra_posterior_interval_compiler_results.json` — acquired endpoints, task transformations, full finite certificates and the outer-posterior failure.
- `astra_nonlinear_precision_bridge.py` — native nonlinear central-difference protocol and exact finite-history smooth convex nonidentifiability construction.
- `astra_nonlinear_precision_bridge_results.json` — native four-call measured data, error vectors, bound, actual task check, and explicit pair of matching old-gradient sources.

**Relevant established antecedents**, for scientific context rather than a claim of a complete novelty search:

- Smolyak-style exact optimality of linear recovery under convex symmetric priors with bounded deterministic observation errors; see the statement of Proposition 6 in [Near-optimal estimation of linear functionals with log-concave observation errors](https://academic.oup.com/imaiai/article/12/4/2546/7277041) (the deterministic part does **not** require log-concave errors).
- The inertia of `sym(QY^T)` is bounded by `rank(Q)`, appearing as Theorem 3.1 in [The inertia of the symmetric approximation for low rank matrices](https://mat.upc.edu/en/people/marta.casanellas/CasFerGar_Submission.pdf).
- Matrix-vector trace sketching with randomized statistical guarantees, a distinct oracle/noise/goal model: [Hutch++](https://pmc.ncbi.nlm.nih.gov/articles/PMC8553228/); [Optimal Sketching for Trace Estimation](https://research.google/pubs/optimal-sketching-for-trace-estimation/).
- Astra historical source-derived procedures and positive-completion arguments in the user-supplied `ACQUIRED_POSITIVE_OPERATIONS(1).md`, plus pinned repository sources N996/N997/N1003/N1011 at Git revision `56d4aebfb8a43cd1a31fdf0f4e14da765ed6f950`.

## 9. Executed subsequent attack: task-sufficient **scalar readouts** versus reusable memory

After completing the sharp vector-precision theorem and native nonlinear bridge, the next question was whether the learner really needs the full `n`-coordinate response to answer a *single, not previously known* scalar task. This leads to a positive theorem **and** a revealing information-retention failure.

**Changed native instrument.** Suppose a genuinely available measurement can accept **two** separately programmable real unit-bounded directions `q,v` and return the one scalar `m(q,v)=v^T S q+e`, with `|e|<=eta`. This is not the same interface as `q -> S q`, and it cannot be granted merely by postprocessing an already returned full vector. It may require a physical detector implementing the weighted readout. The error budget must be certified for this **actual scalar channel**; it cannot be borrowed without justification from a different detector.

**Theorem (no task-precision penalty for scalar readout).** With the same symmetric prior `||S-S0||op<=R`, real unit-bounded inputs and the same error level `eta` in their respective norm models, the optimal deterministic worst-case scalar-task risk after `k` native **scalar** readings is **exactly** the previously derived `E_k^*(T)` in (1), the same as after `k` full-vector readings.

**Constructive upper bound.** Keep the vector-optimal pairs `(qj,yj)` of (2). Set `beta_j=||yj||`, `vj=yj/beta_j`. These are allowable unit scalar-readout directions. Since

\[
T=E+\sum_{j=1}^k\beta_j\operatorname{sym}(q_jv_j^\top),
\]

ask only the `k` scalars `zj = vj^T S qj + e_j`, and output

\[
\widehat L=\operatorname{tr}(T S_0)
 + \sum_{j=1}^k\beta_j\bigl(z_j-v_j^\top S_0q_j\bigr).
\]

Its certified error is `R||E||_*+eta sum beta_j = E_k^*(T)`. No full vector is returned. **Lower bound.** A full-vector oracle with Euclidean error `<=eta` could simulate *any* scalar policy with `||v||<=1` by projecting each returned vector onto that policy's chosen `v`, producing scalar error `<=eta`. The full-vector oracle is therefore at least as informative, so the already proved full-vector minimax lower bound applies to the scalar channel as well. The scalar construction attains it. This proves exact minimax equality, including against deterministic adaptive scalar policies.

**Executed exact six-port scalar instrument control.** For a rationally rotated `T` with signed eigenvalues `(144,9,-25,-16,0,0)`, `R=1/4` and `eta=1/10000`, both programmable `q` and `v` are *rational unit vectors*. At `k=0,1,2` the sharp risks are respectively `48.5`, `6.2669`, `0.0194`. The source pairs `S0 +/- H` and their exact scalar error readings are retained; the differences in answers equal twice these radii. At `k=2`, the genuine scalar oracle returns **two numbers**, whereas the full-vector oracle returns **twelve numbers**. A shared transducer, measurement-time, detector-noise or energy benefit is **not** established by the external scalar count alone. The full-vector hardware model retains more off-task information even when its immediate scalar-task performance is identical.

**Future task information-loss theorem.** Consider the old scalar task `T1=diag(1,-1)` in two ports, with its optimal one-query `q=(e0+e1)/sqrt(2)` and `v=(e0-e1)/sqrt(2)`. The two positive sources `Splus=(2+R)I` and `Sminus=(2-R)I` return the same exact old scalar `v^T S q=0`; their *full-vector* readings `S q` are different. A new, unanticipated task `T2=q q^T` has values `2+R` and `2-R`, so the old scalar record leaves uncertainty radius **`R`** even without noise. The corresponding exact full-vector old record determines the new task at **zero new calls**. This is not a decoder failure: the original scalar measurement discarded legitimately useful reusable scientific information.

**Exact all-future-task trade-off.** An `n x n` real symmetric source has `d=n(n+1)/2` independent parameters. With a source class containing an open symmetric ball, fewer than `d` total scalar bilinear observations cannot determine *every* later scalar task exactly: the `k` recorded scalar linear forms have a nonzero symmetric null direction `H`, and sources `S0 +/- eps H` produce the same central history but different late `T=H` results. This also defeats finite deterministic adaptive scalar acquisition before unknown future tasks, by following its central transcript. The lower bound is attained by the `d` coordinate bilinear readings covering all `S_ij`. By contrast, `n` full-vector measurements on basis inputs determine the entire symmetric `S`, while returning `n^2` scalar coordinates. The native call counts and bandwidth counts measure **different resources**:

| Fully universal exact recovery | Native calls | Returned scalar measurements |
|---|---:|---:|
| Scalar bilinear instrument | `n(n+1)/2` | `n(n+1)/2` |
| Full-vector instrument | `n` | `n^2` |

The n=3 exact control reproduces six versus three calls and an explicit five-scalar-record indistinguishable source pair. This is a useful conditional *task-information/bandwidth Pareto tension*: a task-specific scalar readout can be sufficient and payload-efficient after the task arrives, but full-vector acquisition retains a more versatile observation for questions that arrive still later. Neither strategy dominates without a source-and-future-task distribution, or an explicit multiobjective measurement cost. A strong same-information retaining strategy can choose the same scalar or full-vector interface and tie.

**New executed files:** `astra_scalar_readout_transfer.py` and `astra_scalar_readout_transfer_results.json`. They are independent of prior Astra missing modules and preserve rational input/readout vectors, signed-spectrum decoders, source/report indistinguishability witnesses, and the off-task reuse failure.
