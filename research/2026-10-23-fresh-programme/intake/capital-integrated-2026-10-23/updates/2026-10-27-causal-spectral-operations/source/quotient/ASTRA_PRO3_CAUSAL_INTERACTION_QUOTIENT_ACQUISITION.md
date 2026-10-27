# ASTRA Pro3 — Acquired sparse causal interactions and operation-specific factorial quotients

**27 October 2026.** Original research continuation with executed rational native-response experiments, proofs and deliberately adversarial source alternatives. The underlying sparse-graph query and factorial-interaction methods have substantial classical and current prior art. No historical priority, real hardware capability, general causal discovery, or advantage over equally informed retaining algorithms is established.

## 1. What the learner is allowed to measure

The native measurement is one real scalar boundary reaction from the four-port Schur source preserved in `verified_native_schur_dependency.py`. We independently checked its complete four-port Schur complement against the reusable identity

\[
R=\frac32+\frac1Z,\qquad Z=q+\frac{h_t}{1+u_t}.
\]

The experimental apparatus returns **only** `R`, not hidden response coefficients or the internal potential. At each fixed post-reset readout time `t=129`, it may send nonnegative intervention histories `u` of length 128, with **total intervention dose** `sum(u)<=1/5`; all source measurements in this continuation satisfy that constraint. Each raw reaction may have an unknown, correlated error of magnitude at most `10^-8`. If a reported reaction is `r` and `r-3/2>eps`, the compatible reciprocal value `Z` satisfies

\[
(\widehat R+\epsilon-3/2)^{-1}\ \le Z\le\ (\widehat R-\epsilon-3/2)^{-1}.
\]

The exact source used by the independent checker contains the continuum relaxation sequence `g_j=(3/4)^j/(j+1)`, plus the explicitly specified nonlinearities below. Four previously acquired *exact* impulse moments `(1,3/8,3/16,27/256)` are reused, with their earlier **eight native reactions still charged**. Under finite-error old recordings instead, their error intervals would also have to be propagated; the current new-noise test assumes the previously established exact control values.

A reusable response law is not proved by this interface alone. Its declared structural assumptions are exposed separately for the two acquisitions.

## 2. Learning a sparse pairwise nonlinear causal law

### Declared source class

At the fixed post-reset measurement time, assume the source's **reciprocal** response has the form

\[
Z(u)=z_0+\sum_{i=0}^{n-1}g_i u_i+\sum_{i<j}\beta_{ij}u_i u_j,
\qquad \beta_{ij}\in\{0\}\cup[\beta_{\min},\infty),\quad \beta_{\min}=1/12.
\]

All active `beta_ij` are nonnegative, and the model has no additional cubic or higher pulse interactions. These are **supplied source-class promises**, not inferred from a successful fit. The coefficients `g_i` are unconstrained by the pair-recovery proof, although the executed physical control uses the positive continuum sequence above. The response and instrument are assumed repeatable between matched trials apart from explicitly treated affine reciprocal-channel session drift.

For any pulse-position subset `S` with at least two elements, let `a=delta/(2|S|)`, where `delta=1/5`, and perform three **physical nonnegative intervention trials** at amplitudes `0`, `a 1_S` and `2a 1_S`, with the endpoint readout fixed. Then

\[
\boxed{Q(S)=\frac{Z(2a\mathbf1_S)-2Z(a\mathbf1_S)+Z(0)}{2a^2}
=\sum_{\{i,j\}\subseteq S}\beta_{ij}.}\tag{1}
\]

This is a response *obtained from reactions*, not an assumed native `Q` oracle. Every query charges three scalar reactions and three source preparations. The sum-dose of each of the three interventions is at most `delta`. Crucially, an affine nuisance `d(s)=alpha+nu*s` that changes the reciprocal reading across equally spaced successive session times `s,s+1,s+2` cancels from (1), without knowing either coefficient. Correlated raw-error intervals propagate through the reciprocal transformation and this linear combination.

### Sparse recovery theorem and proof

Write `E(S)=Q(S)` and for disjoint sets `A,B` write

\[
E(A,B)=E(A\cup B)-E(A)-E(B)=\sum_{i\in A,j\in B}\beta_{ij}.
\]

Every nonempty node of an induced-subgraph or bipartite-rectangle decomposition has **positive** weight, at least `beta_min`; an empty node has zero weight. The learner recursively bisects vertex subsets and, for each crossing rectangle, bisects its longer side until it isolates a single pair. It requests only `E(S)` values with the physical three-trial procedure and caches them. When the upper endpoint of a sound interval is below `beta_min`, the node is empty. When its lower endpoint is strictly positive, it is active. Otherwise it returns `UNKNOWN` and does not infer a false structural zero. In the exact setting, classifying zero versus positive is immediate.

If there are `s` active edges among `n` possible pulse positions, each active edge is carried through at most `O(log n)` induced-subset or crossing-rectangle splits. Every positive internal split generates at most two child tests, each crossing split only finitely many additional cached subset tests, and empty branches are discarded. Hence the procedure requests **`O(1+s log n)` distinct group queries**, versus `n(n-1)/2` direct pair tests. Reconstructing the *entire* linear impulse response separately requires up to `n` singleton native readings (fewer when old impulses are retained). There is no claim that this simple recursive method has optimal constants or matches the strongest sparse polynomial/weighted-graph recovery algorithms.

Because every archived interval encloses the true reaction and the positive-edge promise supplies the separation gap, the recovered support is rigorous for the declared class even under deterministic, correlated sensor errors. A saved erroneous midpoint alone is never used as a proof.

### Actual 128-lag execution

The hidden source has exactly five active edges, with weights `1/10,1/8,1/5,3/20,1/6`. The algorithm identified all five using **129 distinct grouped masks**, or 387 native reactions for the grouped tests. It then used 124 new singleton readings and one reusable reference reading for the remaining impulse response. Total: **512 new scalar reactions**, plus the eight previously charged old moment reactions, versus at least 8,128 *pair-specific* source readings for exhaustive pairwise identification before counting the linear calibration. Every native result, error allowance and intervention mask is saved.

In both exact and raw-error-`10^-8` executions, all five edge-support identifications passed source-aware checks. The noisy execution correctly enclosed **128 later source reactions**, including 64 newly specified histories deliberately activating recovered nonlinear edges. The learner performed zero native calls at deployment. The independently checked maximum interval width of these 128 predictions is small but finite; the full widths and exact rational endpoints appear in the JSON record.

An *additional future operation*, unknown when acquisition began, was to choose the nonnegative dose-constrained intervention maximizing the **quadratic nonlinear contribution**. The acquired support graph happens to be a matching. In that class,

\[
\sum_e\beta_e u_i u_j\ \le\ \beta_{\max}\Big(\sum_i u_i\Big)^2/4
\ \le\ \beta_{\max}\delta^2/4.
\]

This follows from `u_i u_j<=(u_i+u_j)^2/4` and disjointness of the recovered edges. Equality is attained by allocating `delta/2` to each endpoint of the strongest edge. The learned **intervals**, not the hidden source values, identify the uniquely strongest edge `(4,69)`. The proposed native intervention has `u_4=u_69=1/10`, all others zero, and the certified nonlinear gain is in **`[0.001999854203,0.002000363826]`**. The independently held source attains `0.002`. The allowed regret against the best source-compatible nonlinear intervention is at most **`5.10e-7`**, with zero source calls to propose the experiment.

### Fair competition

This saves calls against *exhaustive pair testing*, which is the wrong strongest baseline for sparse models. Classical weighted-graph reconstruction and the 2026 adaptive sparse Möbius transform have related or stronger sparse-query guarantees. An equally informed retaining algorithm can implement the same group recursion and tie its results. When the instrument is available at every future task, direct testing can be cheaper than paying the up-front acquisition cost; this work is most relevant when sources expire, future questions are numerous, or the resulting model enables interventions that cannot themselves be trialled later.

## 3. Learning higher-order effects without learning the full underlying source

The more broadly transferable representation is **operation-specific**. Pick two experimentally controllable anchor pulses at lag positions `i=1,j=2`, each applied at amplitude `A=1/20`. Let the other history coordinates be `w`, with their total dose at most `1/10`. Define the four-corner factorial contrast

\[
\begin{aligned}
D_{ij}(w)={}& Z(A,A,w)-Z(A,0,w)\\
&-Z(0,A,w)+Z(0,0,w),\\
H(w)={}&D_{ij}(w)/A^2.
\end{aligned}\tag{2}
\]

Any source background depending only on `w`, any arbitrarily nonlinear component involving the first anchor but not the second, and any component involving the second but not the first **cancels exactly** in this contrast. The source is *not* assumed linear or quadratic globally. The surviving, testable **factorial quotient** is promised to obey

\[
\boxed{H(w)=\beta+\sum_{k\ne i,j}\gamma_k w_k,\qquad
\gamma_k\in\{0\}\cup[\gamma_{\min},\infty),\quad \gamma_{\min}=2/5.}\tag{3}
\]

This *quotient-affinity and sparsity* is the remaining supplied contract. It is strictly weaker than imposing any global polynomial response law. In the executable source, the arbitrary background contains rational nonlinear saturation terms and other pair interactions, as well as unknown one-anchor responses.

### Grouped triple-interaction discovery

The four-corner trial order is `(both on, i only, j only, neither)`. With equally spaced session times, its coefficients `(+,−,−,+)` annihilate an unknown affine reciprocal-channel session drift. For a candidate set `C` with each position set to `c=(1/10)/|C|`, subtract the **retained four-corner baseline** `H(0)` to obtain

\[
\boxed{\Gamma(C)=\frac{H(c\mathbf1_C)-H(0)}c=\sum_{k\in C}\gamma_k.}\tag{4}
\]

A binary group-splitting routine finds every positive modifier. In the executed 128-lag source, there are **126 possible additional positions** and two real modifiers, `gamma_11=1/2` and `gamma_90=5/8`. The algorithm needed 27 nonempty candidate group tests, four raw scalar reactions each, plus four initial anchor readings: **112 new native reactions** versus **508** for testing each candidate separately with four-corner readings. The 100 later unseen weighted-history interactions are all enclosed correctly with no more learner source calls; the maximum group-estimate error radius on the executed noisy history was approximately **0.13403**, whereas each recovered isolated modifier interval is much tighter.

The derived future intervention operation was to maximize the two-anchor interaction using the remaining dose. For `w>=0`, `sum(w)<=1/10`, (3) is maximized at the strongest modifier. The noisy retained intervals have disjoint ranges for the two recovered modifiers and select `k=90` without source-aware access. Its proposed intervention allocates `1/20` to each anchor and `1/10` to lag 90; the factorial quotient is guaranteed in **`[0.187351984799,0.187670858561]`**. The independently checked source gives `3/16=0.1875`, and the certified worst-case regret is at most **`0.000318874`**. It took **zero additional native readings to synthesize** this future experiment.

### A detected failure rather than a false discovery

The compiler additionally checks additivity of the parent group result against the sum of its two children. The test source was amended with a fourth-order term `600*u_i*u_j*u_11*u_90`. It violates the quotient-affinity contract but can still produce plausible individual grouped readings. The learner detected **joint nonadditivity after 16 native scalar reactions**, labelled the source class rejected, and did not report the two-modifier conclusion. This is a falsifier for the particular contradiction, not a universal test of causal order.

## 4. What finite observation cannot establish

Three distinct, executed obstructions are retained.

**Signed cancellation.** If `beta_01=1/8` and `beta_23=-1/8`, the full-set quadratic aggregate (1) equals zero exactly, just as it does for the zero-interaction source. The algorithm's root-pruning step would be false if the nonnegative interaction contract were removed. A different intervention distinguishes the sources. Signed sparse recovery requires a genuinely different, cancellation-safe design or additional randomized/code assumptions.

**Adversarial precision floor.** Change a single pair coefficient from zero to `10^-6`, leave every other source aspect fixed, and keep the maximum total nonnegative dose `delta=1/5`. For every allowed intervention, `|Delta Z|<=10^-6 delta^2/4`. Because the background reciprocal response is bounded below, the resulting **raw** reaction difference is less than `2*10^-8`. Thus a pair of adversarial bounded-error sensors can return exactly the same readings to *any deterministic adaptive learner, for arbitrarily many trials*. Repetition cannot resolve the pair without a stronger noise or minimum-signal contract.

**Finite tests do not prove quotient affinity.** The 112 successful acquired native readings query only finitely many amplitudes of lag 90. Choose a later unvisited amplitude `w_90=1/17`. A `C^infinity` compactly supported bump of this amplitude, vanishing at every previously queried level but equal to one at `1/17`, can be added as `1/5*u_i*u_j*bump(w_90)`. It changes **none of the historical physical reactions**, yet changes the new factorial quotient by `1/5` and the raw reaction by more than twice the sensor-error allowance. The bump's support is explicitly chosen inside a measured rational gap, and the source remains within the physical response positivity margin. Successful finite experimental agreement cannot establish the unrestricted causal law.

A further failure was tested in the session-nuisance dimension. Grouped second differences and four-corner measurements remove affine drift, not arbitrary drift. An additional quadratic reciprocal-session drift violated the inferred affine baselines in **127 checked readings**, causing explicit rejection. Even after successful historical affine checks, arbitrary subsequent drift cannot be excluded from finitely many observations without a stability contract.

## 5. Acquisition architecture and future transfer

The learner acquires **(i)** a signed-off observational instrument (`R` plus a raw-error enclosure and fixed dose language); **(ii)** a conditional consistency class (positive sparse quadratic lag graph, or sparse affine factorial quotient); **(iii)** certified experiment operators (three-level difference and four-corner contrasts), with native calls charged; **(iv)** sound interval coefficients and an exact recovered support *conditional on the stated gap*; **(v)** new task compilers for arbitrary later allowed histories or interaction-specific intervention designs; and **(vi)** explicit `UNKNOWN` or `CONTRACT_REJECTED` paths when the measurement or structural evidence is inadequate.

Nothing here identifies arbitrary unknown nonlinear causal mechanics, establishes a physical spectral contract, warrants all later intervention-history lengths, or provides a native transpose/inverse interface. The stationary lag class applies to the specified 128-position history and fixed source readout time. Future time changes, irreversible physical backaction and unrestricted model drift require separate evidence.

The strongest remaining research path is **discovering reliable causal interaction quotients without a preset order or sign contract**, while preserving useful finite-horizon operations under calibrated adversarial noise. In exact arithmetic, sparse polynomial/Möbius transform methods already address much of the combinatorial reconstruction; the important physically consequential difficulty is whether the required excitation and signal-to-noise separation can actually be achieved.

## 6. Executable provenance and existing methods

Saved executable investigations:

- `sparse_causal_interaction.py`: native 128-lag source, complete two-amplitude grouped recovery, correlated raw-noise interval propagation, 128 unseen histories, dose-constrained new-experiment synthesis. Actual files `sparse_recovery_exact_results_128.json`, `sparse_recovery_noisy_results_128.json`.
- `affine_drift_self_calibration.py`: reuses no-stimulus grouped readings for reciprocal affine-drift self-calibration and 100 later-session queries; rejects quadratic drift. Actual files `drift_affine_results_128.json`, `drift_quadratic_results_128.json`.
- `anchored_higher_order.py`: arbitrary nonlinear background, two-anchor factorial quotient, grouped third-interaction discovery, 100 later interactions, optimal future modifier design, fourth-order source falsification. Actual files `anchored_recovery_exact_128.json`, `anchored_recovery_noisy_128.json`, `anchored_remainder_results_128.json`.
- `information_failures.py`: two-source raw-noise indistinguishability, signed cancellation, unobserved smooth intervention-history activation. Actual file `information_failure_results_128.json`.
- `independent_verify.py`: separate raw four-port Schur reconstruction, every saved source reading and later-task calculation checked against exact rational source formulas, source class and dose constraints.
- `clean_replay.py`, `SHA256_MANIFEST.json`: isolated code replay and archived input/output hash checks.

All saved numerical outputs are **synthetic-source calculations**, not physical data. Independent checker values are explicitly excluded from learner inputs. Complete rational values, rather than only displayed decimal summaries, are included in the saved result records.

Important equal-information and historical comparators:

1. Y. E. Erginbas, *Adaptive Sparse Möbius Transforms for Learning Polynomials*, UC Berkeley technical report (30 April 2026), https://www2.eecs.berkeley.edu/Pubs/TechRpts/2026/EECS-2026-19.html ; develops adaptive sparse polynomial recovery from Boolean function values with `O(s d log(n/d))` queries.
2. N. H. Bshouty and H. Mazzawi, *Reconstructing weighted graphs with minimal query complexity*, Theoretical Computer Science **412** (2011), 1782–1790, https://doi.org/10.1016/j.tcs.2010.12.055 ; established graph-reconstruction and additive-query methods.
3. *Identification of Sparse Volterra Systems: An Almost Orthogonal Matching Pursuit Approach*, https://pmc.ncbi.nlm.nih.gov/articles/PMC9038084/ ; an established sparse nonlinear-system identification comparator.

These precedents exclude priority claims for group testing, sparse polynomial acquisition, factorial contrasts and polynomial nonlinear system identification. The present scientific focus is their **native experimental interface, physically paid resource contracts, conditional transfer, independent source compatibility and explicit failure controls**.
