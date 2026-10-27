# Astra Pro3 — Acquired spectral-memory families, universal extremal models, and task-shaped native experiments

27 October 2026. Original source-to-operation integrations, conditional exact proofs, executable synthetic-source controls, strong comparable methods, and explicit failures. This continuation uses the preceding causal-memory work (`ASTRA_PRO3_CAUSAL_MEMORY_AND_VALIDATION.md`) as a *distinct source class and instrument contract*. It does **not** claim that the old three-pole fixture satisfies the new spectral-positivity assumptions, or that the mathematical moment results are historically new.

## 1. Change of mechanism: from a supplied finite memory order to a positive spectrum of arbitrary complexity

A prior acquisition recovered a rational linear recurrence from `2r` impulse coefficients **after supplying the assumption of minimal finite order r**. Such a short prefix need not identify memory order. We instead assume a different, physically interpretable source family, namely a nonnegative mixture of relaxing modes:

\[
 g_j=\int_0^\rho \lambda^j\,d\mu(\lambda),\qquad \mu\ge0,\quad 0<\rho<1. \tag{1}
\]

The positive measure can have infinitely many atoms or a continuum; its total mass is `g_0`. No fixed state-space dimension or recurrence is supplied. The *positive spectral representation, spectral ceiling rho, additive causal response, and matched-trial reproducibility remain supplied scientific contracts*. They are **not inferred** from a few successful measurements. This is the discrete Hausdorff moment setting, with close antecedents in completely monotone sequences and Markov–Kreĭn / Gaussian-quadrature extremal representations.

### Charged physical observation interface

Retain the preceding full four-port Schur reaction, with a two-port boundary block, positive hidden inverse stiffness `H_t=diag(q_t,3/5)`, an unknown positive inverse instrument gain `h_t`, and a positive commanded coupling `lambda_t=1+u_t`:

\[
 R_t=\tfrac32+\frac1{q_t+h_t/(1+u_t)},\qquad
 q_t=q^{(0)}_t+\sum_{j=0}^{t-1}g_j u_{t-1-j}. \tag{2}
\]

All native scalar reactions are computed by **eliminating the full coupled stiffness matrix via the Schur complement**, not by returning a hidden `g_j` from an invented oracle. The nuisance trajectories `q_t^(0)` and `h_t` may be nonlinear and otherwise unknown, but are required to be identical across synchronized treated/sham trials.

With a single command `u_0=delta`, equal commands thereafter, and native reactions at elapsed times `1,...,N`, the measured reciprocal contrast gives

\[
 g_j=\frac{(R_{j+1}^{\rm treated}-3/2)^{-1}
 -(R_{j+1}^{\rm sham}-3/2)^{-1}}{\delta}.\tag{3}
\]

An `N`-coefficient acquisition costs **2N scalar native reaction readings across two matched experimental runs and one reset**; it also costs elapsed time and control/idle commands. The synthetic source uses `delta=1/5`, nonaffine rational nuisance trajectories, and all native shunt strengths remain positive. Future checker-only source observations are not counted as learner readings.

## 2. Theorem: three impulses determine sharp answers to infinitely many later operation types

Assume the exact acquired record is `m0=g0>0, m1=g1, m2=g2`, strictly inside the feasible moment region

\[
 0<m_1<\rho m_0,\qquad m_1^2<m_0m_2<\rho m_0m_1.\tag{4}
\]

Define two **explicit compatible spectral sources**:

\[
 \begin{aligned}
 c_-&=m_2/m_1,&w_-&=m_1^2/m_2,
 &\mu_-&=(m_0-w_-)\delta_0+w_-\delta_{c_-},\\
 c_+&=(\rho m_1-m_2)/(\rho m_0-m_1),
 &w_+&=(\rho m_0-m_1)/(\rho-c_+),
 &\mu_+&=w_+\delta_{c_+}+(m_0-w_+)\delta_\rho.
 \end{aligned}\tag{5}
\]

Both are positive, supported within `[0,rho]`, and have exactly the three recorded moments. For **every later** `f in C^3([0,rho])` with `f''' >= 0`, including functions chosen only after the source expires,

\[
 \boxed{\int f\,d\mu_-\ \le\ \int f\,d\mu\ \le\ \int f\,d\mu_+.}\tag{6}
\]

**The entire ranges are sharp.** The same two physical source alternatives attain both ends for *every member of this function class simultaneously*. Therefore these two atom lists form a reusable semantic summary of the whole compatible infinite-dimensional source family for these future questions; it does **not** mean that the actual source has two modes.

**Proof.** Let `q_-(x)` be the unique quadratic Hermite interpolant of `f` at `0` (value) and `c_-` (value and derivative). The remainder theorem gives

`f(x)-q_-(x) = f'''(xi_x) x(x-c_-)^2/3! >= 0`

for `x in [0,rho]`. Similarly the quadratic interpolant `q_+` at `c_+` (value and derivative) and `rho` (value) satisfies

`f(x)-q_+(x)=f'''(zeta_x)(x-c_+)^2(x-rho)/3! <=0`.

Every admissible source has the same integral of any quadratic polynomial. Interpolants equal `f` on their corresponding two-atom supports, so integrating gives (6). Endpoint measures in (5) prove attainment. This is a classical Hermite/Markov–Kreĭn argument; the new work is the native-acquisition and later procedure-compilation usage.

**Important limitation:** (6) does **not** apply to arbitrary signed combinations of responses with sign-changing third derivative. This failure is explicitly tested below. No simultaneous independence of different future scalar answers is assumed.

### A true continuum-spectrum acquisition

The independent hidden synthetic source is uniform positive spectral mass on `[0,3/4]`, so **the learner is not given a finite pole model** and the checker computes `g_k=(3/4)^k/(k+1)`.

**Six original native scalar readings** acquired `(g0,g1,g2)=(1,3/8,3/16)` and produced

\[
 \mu_- = \tfrac14\delta_0+\tfrac34\delta_{1/2},\qquad
 \mu_+=\tfrac34\delta_{1/4}+\tfrac14\delta_{3/4}.\tag{7}
\]

Subsequently specified lagged impulses `g3,g4,g8,g16,g32`, discounts `sigma=1/2,3/4,1`, and a scalar static feedback gain were compiled without new native calls. For the **infinite-horizon step gain**

\[
 G(1)=\sum_{j\ge0}g_j=\int\frac{d\mu(\lambda)}{1-\lambda},
 \qquad\boxed{7/4\le G(1)\le2}.\tag{8}
\]

The independent continuum reference is `(4/3) log(4)=1.848392...`; both interval endpoints are attained by the explicit spectral alternatives, not by the continuum test source. The prior `m0=1` and ceiling alone would give `[1,4]` (width 3), whereas (8) has width 1/4, a **12-fold improvement in exact certified width**, not a claim of 12-fold physical efficiency. For a later known positive gain `kappa=1/4`, a stable scalar feedback gain `G/(1-kappa G)` has sharp range `[28/9,4]` by monotonicity of the transformation and the endpoint witnesses.

The same two spectra yield *simultaneously* sharp time-indexed response bounds for any finite causal **nonnegative-input** sequence because `lambda^j` has nonnegative third derivative for every `j>=3`, while the first three impulses are fixed. Further, the digital policy `u_t=p_t+(1/8)y_t` with nonnegative externally specified commands `p_t`, and `y_t=sum_{j<t}g_j u_{t-1-j}`, is order-preserving in the whole nonnegative kernel. At every step the two compatible endpoint sources bound the entire feedback trajectory. A 32-step later programme was executed against the independent continuous source and every actual output was enclosed. At the final step the source value was approximately `0.00692617`, within the sharp interval `[0.00624570,0.00799603]`. This is *specified digital response logic*, not acquisition of unknown physical kinetics.

## 3. The signed-task failure, exact repair, and an informative/no-value experiment contrast

A later task asks for

\[
 T=g_3-\tfrac23g_4=\int_0^{3/4}(x^3-\tfrac23 x^4)\,d\mu(x).\tag{9}
\]

The canonical two-atom sources in (7) **both output exactly `1/16`**, which might encourage a false zero-width estimate if one treats them as universal. The actual answer is `81/1280`, and other compatible sources produce different answers. The reason is that the task integrand has a third derivative that changes sign.

I constructed independent exact primal **source** witnesses and dual **polynomial** certificates proving the true sharp interval

\[
 \boxed{63/1024\le T\le 33/512}.\tag{10}
\]

The lower witness has mass `1/6` at `0`, `2/3` at `3/8`, and `1/6` at `3/4`. The upper witness puts equal mass at `(3-sqrt(3))/8` and `(3+sqrt(3))/8`. Both retain exactly `(m0,m1,m2)=(1,3/8,3/16)`.

Let `f(x)=x^3-(2/3)x^4`. Define the quadratic lower and upper dual polynomials

\[
 \begin{aligned}
 q_-(x)&= f(x)+\tfrac23x(x-\tfrac38)^2(x-\tfrac34),\\
 q_+(x)&= f(x)+\tfrac23(x^2-\tfrac34x+\tfrac3{32})^2.
 \end{aligned}
\]

The quartic/cubic coefficients cancel: both `q_-` and `q_+` have degree at most two. On the allowed spectral interval, `q_- <= f <= q_+`. Their integrals, which are determined by the three acquired moments, are exactly the endpoints in (10); the witness sources have equality at every support point. Thus the interval is **jointly warranted and sharp**, not a numerical fit.

An additional two native scalar readings acquire `g3=27/256`. This reduces the *separate* sharp interval for `g4` from `[3/64,21/256]` to `[63/1024,135/2048]`, exactly **8-fold** in width. The second range follows from the Schur complement of the degree-two Hankel moment matrix and the `x(rho-x)` localizing constraint, and both endpoints have actual spectral witnesses. **But the `g3` reading does not narrow (10) at all:** both signed-task extremizers already have the same value `g3=27/256`. This is a precise failure of planning by generic response uncertainty instead of the requested future task.

### Finite sensor-error repair

A noisy record consists of centers `mhat_i` with individually certified bounds `|m_i-mhat_i|<=eta_i`, allowing adversarial or correlated errors. Fix *any* rational Hermite nodes in the spectral interval and construct pointwise valid quadratic bounds `q_- <= f <= q_+`. Writing their coefficients as `a_i^-/a_i^+`, a sound future-task certificate is

\[
 \sum_i a_i^-\widehat m_i-\sum_i|a_i^-|\eta_i
 \le \int f\,d\mu\le
 \sum_i a_i^+\widehat m_i+\sum_i|a_i^+|\eta_i.\tag{11}
\]

The executed implementation uses `eta_i=1e-5`, rational centers and the two exact source-derived Hermite nodes; it constructs and saves all rational coefficients and error budgets. A per-reaction reciprocal-reading error budget `delta*eta_i/2` is sufficient for those impulse-center intervals under the paired difference decoder. Bounds are **sound outer enclosures**, not claimed sharp over the full correlated noisy consistency set; numerical near-singularity cannot be thresholded into an exact finite-order law.

### A further decisive failure: finite moments do not establish a uniform decay ceiling

I tested whether the first three acquired moments alone could justify a DC-gain or long-time tail contract. **They cannot, even if every competing source is an individually stable positive mixture.** For each candidate ceiling `rho_N=1-1/N`, reconstruct the compatible upper two-atom measure from (5) using *the same exact three moments* `(1,3/8,3/16)`. Its slow atom lies at `rho_N<1`, so the individual source has a finite step response. Yet as `N→∞` this atom retains asymptotically positive mass and its contribution to `G(1)` diverges. All historical reaction measurements remain identical under the matched source interface.

Executed rational alternatives with spectral maxima `0.9`, `0.99`, `0.999`, `0.9999` had DC gains approximately **2.65, 12.30, 108.72, and 1073.01**, respectively, while every source produced the same three acquired impulse values. Hence there is *no finite universal upper DC gain* under a mere per-source “all modes decay below one” promise without a **common numerical decay ceiling**. The shaped-intervention tail guarantee (13) cannot be advertised absent such a ceiling. This is a separate model-contract obstruction from measurement noise or a missed finite-state order.

## 4. Finite-order acquisition without supplying order: conditional stopping theorem

For a positive spectrum of **unknown** atomic order `r`, if exact moments `g0,...,g_(2r)` are acquired and the `r x r` Hankel `H_(r-1)=(g_(i+j))_(0<=i,j<r)` is nonsingular but `(r+1) x (r+1)` Hankel `H_r` is singular, the measured moments **force** the source to have exactly `r` spectral atoms.

**Proof.** Every feasible moment matrix is Gram-positive. A nonzero `v in ker H_r` gives a polynomial `P(x)=sum_(j=0)^r v_j x^j` with `∫P^2 dmu=0`. Positivity implies that every compatible `mu` is supported on the real roots of `P` inside the supplied spectral interval. Since `H_(r-1)` has rank `r`, at least `r` support points are necessary; therefore `P` has exactly `r` distinct roots in the interval. Their weights are uniquely determined by the first `r` moments through a Vandermonde system. All future moments, discounted gains and causal responses are thereby uniquely determined. No model-order number was supplied to the learner. This is the classical univariate flat-Hankel moment argument, with an explicit native experimental stopping rule.

**Executed:** A distinct hidden synthetic source with nodes `(1/8,3/8,5/8)` and weights `(1/5,1/3,7/15)` used **14 scalar Schur reactions** (seven matched impulse coefficients over two runs). The learner found `rank H2=3`, `rank H3=3`, a degree-three null polynomial with those roots, and recovered all three weights in exact arithmetic. It then calculated future impulses at lags `7,10,20,40` without additional native reactions.

Crucially, the **six-reading-prefix-of-impulses** `g0,...,g5` did **not** already force this three-mode law: the positive `x` and `(rho-x)` 3x3 localizing Hankel matrices are both strictly positive definite. More decisively, the script constructs from those six moments a *different four-mode positive spectrum*, including endpoints `0,rho` and two interior algebraic roots, with exactly the same six acquired impulses. Its next impulse `g6` differs by exactly `21/237568`. The seventh impulse is therefore actually distinguishing in this particular fixture.

A separate pair of **seven-mode positive spectra** has identical first six moments, with next-moment separation `45/1048576`; this uses binomial finite-difference weights on the seven-point rational grid `{0,1/8,...,3/4}`. This is an exact finite-prefix nonidentifiability control independent of the chosen three-mode fixture.

**Noise obstruction.** Add a spectral mode of weight `1e-8` to a two-atom source while rescaling its existing atoms. The first seven impulse values change by at most `1e-8`, but the corresponding 3x3 Hankel changes from exactly singular to positive definite. Both are compatible with a single suitably noisy record. Hence a near-zero determinant is not a certificate of exact finite memory. At nonzero noise the sound result is a measure/moment *consistency family*, not a thresholded exact recurrence.

## 5. Further changed experiment: task-shaped native intervention histories

The same linear causal response has a physical operation that was absent from a compiler that queried only isolated impulses. For an arbitrary new **polynomial** task `P(x)=sum_(j=0)^(T-1)c_j x^j`, choose a physical treated intervention history

\[
 u_{T-1-j}=\beta c_j,\quad u_T=0,\quad
 \beta\max_j|c_j|\le1/5.
\]

Then **one pair** of native Schur scalar reactions at time `T` (treated/sham, with one reset) gives

\[
 \boxed{\frac{z_T^{\rm treated}-z_T^{\rm sham}}{\beta}
 =\int P(x)\,d\mu(x)}.\tag{12}
\]

The result follows from the exact causal convolution and cancellation of the common nuisance, not from the spectral-positivity assumption. The procedure still needs physical actuation at all nonzero command times, elapsed time `T`, identical reset conditions, and two native scalar readouts. It is **one matched pair of readouts**, not one instantaneous free experiment.

For the previously unforeseen signed task (9), the executable compiler used just **two active commands at offsets 3 and 4**, two newly charged scalar reactions at elapsed time five, and one reset. It measured the exact answer `81/1280`. Measuring `g3` and `g4` separately instead would use four scalar reactions (but would retain two generally reusable coefficients). With reciprocal sensor error at most `eta` per reading, the direct decoder's absolute error is at most `2 eta/|beta|` if the stated common-nuisance model holds; a more general source prior might tighten this, so no universal optimality is asserted.

For a future **discounted infinite-horizon** response `G(sigma)=int (1-sigma*x)^(-1) dmu` with `0<=sigma<=1`, a finite shaped history with coefficients `c_j=sigma^j` exactly measures its first `T` impulse terms and incurs the rigorous prior-only tail

\[
 0\le G(\sigma)-\sum_{j<T}\sigma^j g_j
 \le \frac{g_0(\sigma\rho)^T}{1-\sigma\rho}.\tag{13}
\]

A 35-step intervention produced a finite verified DC-gain enclosure using exactly two scalar endpoint reactions, **but required 35 active treated commands and 35 time steps**. A separate 24-step discounted response test also passed.

### A third attack: retained moments shorten the *next experiment*

For `T>=3`, the unseen discounted tail function `x^T/(1-x)` itself has nonnegative third derivative. Before the next measurement, the two canonical spectra from the previously acquired three moments give sharper exact tail bounds:

\[
 \frac32(1/2)^T\le
 G(1)-\sum_{j<T}g_j
 \le(1/4)^T+(3/4)^T.\tag{14}
\]

The learner chose a future required certified DC-gain **interval width at most `1/5000`**. The prior-only tail (13) requires `T>=35`. The historical-moment-informed tail width from (14) requires only **`T>=30`**, so one new matched scalar-reaction pair can be executed five actuation steps earlier. The 30-step native source readout and the final certified interval passed exact-rational and independent continuum checks. **After conditioning on the newly measured partial sum, (14) remains valid but is not claimed jointly sharp**: the canonical sources need not reproduce the newly measured partial sum. The extra six earlier acquisition readings remain charged, rather than declared free.

This is actual experiment procedure generation driven by previously acquired scientific evidence. A strong equally informed numerical quadrature or classical system-identification algorithm can adopt it and tie the result.

## 6. Equally informed alternatives, scope, and priority

1. **Hausdorff/Markov–Kreĭn moment theory:** all positive-mixture and principal-representation mathematics is classical. The constructive dual proofs above are self-contained; priority for the pure theorems is not claimed. See: [Hausdorff moment notes, QMU](https://webspace.maths.qmul.ac.uk/a.sodin/teaching/moment/clmp.pdf); [Kreĭn and Nudelʹman, *The Markov Moment Problem and Extremal Problems*](https://doi.org/10.1090/mmono/050); [Lasserre, *Moments, Positive Polynomials and Their Applications*](https://www.nzdr.ru/data/media/biblio/kolxoz/M/MC/MCat/Lasserre%20J.B.%20Moments%2C%20positive%20polynomials%20and%20their%20applications%20%28ICP%2C%202010%29%28ISBN%201848164459%29%28371s%29_MCat_.pdf).
2. **Prony/Ho–Kalman:** on the truly three-atomic source, classical exact Hankel/flat-moment identification matches the programme; the new distinction is stopping by data-supported positivity rather than *assuming* minimal order three. An equally informed retaining programme can do exactly the same.
3. **Matched differential causal experiments:** these inherit the established native Schur interface and the supplied linearity/reset contracts from the preceding Pro3 work. The source with a negative decay pole from that prior three-state experiment is **not** in this positive relaxation class: its `g2=5/64` exceeds `(3/4)g1=3/64`, so a basic necessary spectral moment inequality already rejects it.
4. **Native cost accounting:** six raw reactions for three impulse coefficients, eight if the fourth coefficient is acquired, fourteen for seven impulses in the separate source, or two raw reactions for each new task-shaped pair. Preparing intervention histories, time horizon, actual actuation count, resets, widths of returned scalar values, exact rational operations, and source-aware checker calls remain real costs. The physically executable continuum kernel is **synthetic software**, not an experimentally verified material or device.
5. **Validity limit:** finite compatible observations cannot prove the positive-mixture class or a spectral ceiling; signed/nonpositive spectra, hidden modes, and reset-dependent drift can invalidate the conclusion. The noisy certificate does not claim exact rank or source recovery. Direct single-task readouts lose reuse across unrelated later tasks. Not all signed functionals or mixed feedback policies share the same extremizers.
6. **Scientific mission:** there is a real changed procedure: from passively fitting short recurrences to retaining an entire positive spectral family and **compiling future operations or interventions** from it, even if future task identities were unknown during acquisition. Nonetheless no foundational physics discovery, novelty of Hausdorff moment theory, hardware advantage or exclusive superiority over an equally informed alternative is established.

## 7. Actual saved files and verification

- `acquired_spectral_memory.py`: exact synthetic four-port Schur source, two-run acquisition, canonical moment extrema, signed-task dual certificates, positive digital feedback, noisy outer certificates, order-free atomic identification, and explicit positive-source twins.
- `acquired_spectral_memory_results.json`: actual native scalar reactions, full exact rational bounds, source witnesses, future tasks and counterexamples.
- `task_shaped_native_experiments.py`: new intervention-history compiler, signed task, finite discounted response, and prior-informed 30-versus-35-step design.
- `task_shaped_native_results.json`: actual raw Schur reactions, intervention commands, exact task values and finite-horizon certificates.
- `verify_spectral_memory.py` / `independent_verification_results.json`: independent verification of raw observations, exact symbolic dual identities, positive-source witnesses, moment-rank arguments, adversarial compatible mixtures, and experiment scheduling, without importing producer procedures.
- `clean_replay_spectral.py`, `clean_replay_results.json` and `SHA256_MANIFEST.json`: isolation replay and reproducibility checks.

All claims above refer only to the exact source classes and actually executed controls. No mutation of the Astra GitHub repository is implied by the local files.
