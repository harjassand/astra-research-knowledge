# Independent Astra result — source-certified dynamic port compression

**Status:** independently constructed research theorem and numerical pilot, **not** a claim of external mathematical acceptance, historical novelty, physical experiment, or device. 2026-11-02 (Brisbane). **Source freeze:** `harjassand/astra-research-knowledge` revision `5489b118101275c81500d823361592c670ec77bb`. No later Astra contribution is imported.

## 1. The consequential operation and the actual experimental contract

For a *fixed, unknown*, dissipative, linear, grounded RC/diffusive network

\[C\dot x=-Gx+Bu,\quad x(0)=0,\qquad y=B^{\mathsf T}x,\]

where `C` is symmetric strictly positive definite and `G` symmetric positive semidefinite, learn a reusable port-to-port **step operator** from finite scalar measurements. Neither the internal node count, `C`, `G`, `B`, pole locations, nor the effective rank is given to the learner. We allow arbitrary port combinations `v` in the actual experimental language below. The physical source is held fixed and reset to `x(0)=0` before each experiment.

A native experiment selects unit-norm `v=e_i` or `v=(e_i+e_j)/sqrt(2)`, applies a constant vector current `u(s)=v` from time 0 to time `t`, and measures the **single scalar** `q_v(t)=v^T y(t)/t` with a guaranteed error at most `eta`. Thus the exact outcome is

\[q_v(t)=v^{\mathsf T}R(t)v,\quad K(t)=B^{\mathsf T}C^{-1/2}e^{-At}C^{-1/2}B,\quad A=C^{-1/2}GC^{-1/2}\succeq0,\]
\[S(t)=\int_0^t K(s)ds,\qquad R(t)=S(t)/t.\]

Port-response samples can be scalar despite `y` being a multiport vector: the physical sensor need only resolve the weighted terminal voltage `v^T y`, under an independently warranted calibration for that setting. Applying the commanded `v`, obtaining the collocated readout, source reset, noise, timing, settling, and source stationarity are real experimental resources. An ordinary linear passive network with known `C,G,B` would be handled more efficiently by direct simulation.

**Full desired scientific capability:** reusing the same learned source to certify useful, previously unspecified *time-dependent* controls without reconstructing all hidden modes, and eventually extending it to qualified nonlinear, time-varying and non-collocated systems. The completed theorem below earns only the stated fixed linear passive interface and task policies.

## 2. Port acquisition with sound noisy residuals

Choose an observable reference time `t0>0` and future horizon `T>=t0`. Let `R0=R(t0)`. Acquire all `m` diagonal scalar values, `dhat_i`, each with absolute error `eta`. They give the **measured** source upper bound

\[M_0=\sum_{i=1}^m (\hat d_i+\eta)\ \ge\operatorname{tr}R_0\ \ge\|R_0\|_{\rm op}.\tag{1}\]

Discover `r` representative actual ports `J=(j1,...,jr)` adaptively. To acquire any column `j` of `R0`, use `m-1` genuine pair experiments:

\[\widehat{R}_{ij}=\widehat q_{(e_i+e_j)/\sqrt2}(t_0)-(\hat d_i+\hat d_j)/2,\quad i\ne j.\]

Each acquired off-diagonal entry differs from the true entry by at most `2 eta`; hence take `xi=2 eta` as a simultaneous **entrywise** matrix bound. For any real coefficient matrix `Z` of shape `r x m`, with `Z[:,j_a]=e_a` for selected ports, set `L=E_J Z` and `Q=I-L`. This is an abstract reconstruction map, not a new physical actuator. Define `z_i=Z[:,i]` and for unselected ports the observable estimate

\[\hat h_i=\hat d_i-2z_i^{\mathsf T}\hat R_{Ji}+z_i^{\mathsf T}\hat W z_i,\qquad\hat W=\tfrac12(\hat R_{JJ}+\hat R_{JJ}^{\mathsf T}),\]
\[\delta_i=\max\{0,\hat h_i+\xi(1+\|z_i\|_1)^2\};\tag{2}\]

for selected ports put `delta_i=0` exactly. The triangle inequality on the entrywise errors proves

\[(Qe_i)^{\mathsf T}R_0(Qe_i)\le\delta_i,\qquad D=\sum_i\delta_i.\tag{3}\]

**There is no numerical rank-inference assumption:** choose any finite `Z`, for example ridge-regularized least squares on acquired columns; its coefficients are charged inside (2). If the noisy columns are ill-conditioned, `D` becomes large and the controller fails closed. A greedy pivot routine may use the largest computed residual bound, but the theorem does not assume it always finds a small rank. Cost is `m+r(m-1)` scalar settings, plus `O(m r^2+r^3)` ordinary arithmetic for small `r`, condition-dependent coefficient magnitudes and source resets. The producer/learner only observes scalar native results.

## 3. The passive transfer from one time to every future time

`K(t)` is positive semidefinite and **decreasing in Loewner order**, because each matrix `e^{-At}` is a decreasing spectral function of fixed `A>=0`. Consequently `S(t)` is PSD-increasing and `R(t)=S(t)/t` is PSD-decreasing. In particular,

\[0\preceq S(t)\preceq a(t)R_0,\qquad a(t)=\max\{t,t_0\},\qquad 0\le t\le T.\tag{4}\]

For `t>=t0`, this is simply `R(t)<=R0`; for `t<t0`, it follows from `S(t)<=S(t0)`. No upper bound on the fastest or slowest eigenvalue of `A` was assumed.

`Q^T S(t) Q` is PSD, its diagonal is at most `a(t)delta_i`, and its operator norm is bounded by its trace `a(t)D`. In addition, `||S(t)||op<=a(t)M0`. Expanding `L=I-Q` and using Cauchy–Schwarz in the `S(t)` semi-inner product gives

\[\|S(t)-L^{\mathsf T}S(t)L\|_{\rm op}\le a(t)\big(2\sqrt{M_0D}+D\big).\tag{5}\]

This is the central, *all-time* port-compression theorem. It is not a small-spectrum or exact-rank promise; it is an explicit residual paid from real scalar experiments. **It controls the integrated step response**, which is the correct object for actual bounded-variation pulses; a brief unseen fast transient can have large instantaneous amplitude without a large time-integrated effect.

### Stronger scalar task support

For any real original-port vector `v`, define quantities calculable after acquisition:

\[e_v=\sum_i |v_i|\sqrt{\delta_i},\qquad a_v=\sqrt{\max\{0,(Zv)^T\hat W(Zv)+\xi\|Zv\|_1^2\}}.\tag{6}\]

Minkowski's inequality in the semi-inner product of `R0` gives `||Qv||R0<=e_v`. The `W` observation gives `||Lv||R0<=a_v`. Then for all `w,v` and `t`:

\[|w^T[S(t)-L^TS(t)L]v|\le a(t)[a_w e_v+a_v e_w+e_we_v].\tag{7}\]

This bounds **the actual asked-for effect**, usually much better than the operator norm of every unasked-for effect. No future task direction is used in acquiring `J` or `R0`.

## 4. Learning *all intermediate times* without a pole count or rate cutoff

At `t>0`, the physically measured matrix is the normalized step operator:

\[R(t)=B_*^T f(tA)B_*,\quad B_*=C^{-1/2}B,\quad f(z)=(1-e^{-z})/z=\int_0^1e^{-sz}ds.\tag{8}\]

Consider its analytic log-time extension `R(exp(z))`. For a scalar unit port direction `v` and `|Im z|<pi/2`, positivity of its spectral measure shows

\[|v^T R(e^{x+iy})v|\le(\cos y)^{-1}v^TR(e^x)v.\tag{9}\]

For `h>0`, the integrated response monotonicity also implies `R(e^{-h}t0)<=e^h R(t0)` in PSD order. Partition the real log interval `[log t0,log T]` into `L=ceil(log(T/t0))` blocks of length at most one. For an order-`n` Chebyshev polynomial at `n+1` first-kind roots per block, the Bernstein ellipse of radius `rho=2` extends at most `1/8` to the left and `3/8` in imaginary height. Equations (1),(9) thus bound every normalized quadratic form throughout the ellipse by

\[C_*M_0,\qquad C_*=e^{1/8}/\cos(3/8).\tag{10}\]

The classical Bernstein-ellipse Chebyshev error theorem and the first-kind Lebesgue constant bound yield the *entire matrix* bound for the selected r ports:

\[\sup_{t\in[t_0,T]}\|R_{JJ}(t)-\widetilde R_{JJ}(t)\|_{op}\le\eta_R:=4C_*M_0 2^{-n}+2r\Lambda_n\eta,\]
\[\Lambda_n\le1+(2/\pi)\log(n+1).\tag{11}\]

The operator norm follows by applying the scalar analytic theorem to every real unit `v` in the `r`-port subspace; symmetric matrix interpolants preserve the quadratic-form representation. Each sampled `r x r` matrix costs exactly `r(r+1)/2` scalar experiments, using the same polarization formula. This costs

\[\tfrac12r(r+1)(n+1)L\]

source settings, *independent of the hidden state dimension and the number or magnitude of relaxation rates*. More experiments and precision may be needed than this sufficient count. It is not a lower-bound or practical optimality claim.

Define the executable learned step operator

\[\widetilde S(t)=\begin{cases}0,&0\le t<t_0,\\t Z^T\widetilde R_{JJ}(t)Z,&t_0\le t\le T.\end{cases}\tag{12}\]

Combining (5), (11) and `||S(t)||<=t0 M0` for `t<t0` proves

\[\sup_{t\le T}\|S(t)-\widetilde S(t)\|_{op}\le
\Delta:=T(2\sqrt{M_0D}+D)+\|Z\|_{op}^2\max\{t_0 M_0,T\eta_R\}.\tag{13}\]

No nonphysical fitted response is asserted to be a real passive network; the certificate is on its **observable outputs**. Where physical realization of the surrogate is needed, a positive-measure fit and its own numerical validation must be charged separately.

## 5. All-protocol and task-conditioned control guarantees

For a right-continuous vector input `u` of bounded variation on `[0,T]`, extended as zero to negative times, let `du` include its jump at zero and denote its vector total variation by `V_u`. The exact physical output satisfies the integration-by-parts identity

\[y_u(t)=\int_{[0,t]}S(t-s)\,du(s).\tag{14}\]

Therefore the acquired predictor with `S~` satisfies **for every future waveform**, including unobserved pulses and new combinations of ports,

\[\|y_u-\tilde y_u\|_{L^\infty([0,T];\ell_2)}\le V_u\Delta.\tag{15}\]

If an unknown source-dependent objective `J(u)` uses a known linear output weight `w(t)` with `integral ||w(t)|| dt <= W`, and all candidate inputs have `V_u<=V`, a globally optimized surrogate control has true regret at most `2W V Delta + solver_gap`. The same uncertainty margin, multiplied by a known Lipschitz constraint factor, suffices to certify physical output constraints. The **global** certificate can be very loose; failure to pass is not an impossibility of useful decisions.

For *the genuinely new and sharper terminal task* `w^T y(T)-cost`, and a proposed protocol described by finite source-current jumps `(t_j,v_j)`, use the same `S~` without new source data. Define

\[E(t,w,v)=\begin{cases}
 t_0(a_w+e_w)(a_v+e_v),&t<t_0,\\
 t\left[a_we_v+a_ve_w+e_we_v+\eta_R\|Zw\|_2\|Zv\|_2\right],&t\ge t_0.
\end{cases}\tag{16}\]

Then the promised scalar score interval is

\[J\in[\hat J-\varepsilon_J,\hat J+\varepsilon_J],\quad
\varepsilon_J=\sum_j E(T-t_j,w,v_j).\tag{17}\]

For a finite menu of proposed protocols and any newly imposed, **known** costs, if one lower endpoint strictly exceeds every other upper endpoint, that protocol is the unique reward-maximizing menu action for **every** admitted physical source consistent with all measurement errors. This is a model-class theorem, not a finite holdout statistic.

### Theorem: a continuous policy class, not merely a finite menu

Fix any pulse shape `h(s)` which is a finite combination of known rectangular profiles (or an arbitrary known bounded-variation scalar waveform), and let the future controller choose *any* nonnegative fractional allocation `v` in the **full continuous simplex** `X={v>=0,sum_i v_i<=1}`. It commands `u(s)=h(s)v`. For a scalar terminal reward and an affine known actuator price,

\[J(v)=w^T y_{h v}(T)-c^T v=\sum_{i=1}^m v_i J(e_i),\]

where the omitted mass `v_0=1-sum v_i` has zero reward. Source linearity earns this identity for the actual physical response; the controller does **not** assume a fitted model is accurate elsewhere. Apply (16)–(17) at the `m` unit actuator vertices and include `v_0=0`. If for some `j`, the certified lower endpoint `L_j` is strictly greater than `max(0,max_{i!=j} U_i)`, then `e_j` is the **unique global maximizer over every fractional actuator allocation** `v in X`, for every admitted source consistent with the native measurement intervals. Proof: `J(v)` is the convex combination of vertex values and zero, and every other vertex has strictly lower actual value. No extra source measurements or optimization oracle are needed. This is a continuous convex control policy (fixed waveform shape), not yet arbitrary time-profile optimization.

One can also certify *approximate* global optimization over a continuously varying pulse start time. For a fixed pulse of length `ell>0`, `u_i(s)=v_i*1_[s0,s0+ell](s)`, with `v in X` and `s0` in a declared compact interval satisfying `T-s0-ell>=t0`, terminal benefit is `w^T[S(T-s0)-S(T-s0-ell)]v`. Since `0<=K(t)<=R0` for every `t>=t0` and `||R0||<=M0`, each vertex score as a function of s0 is `2M0||w||`-Lipschitz (plus any known price-time Lipschitz constant `Lc`). On a grid of spacing h including interval endpoints, use the acquired vertex intervals (17), take `U_grid=max_{i,k} U_i(s_k)` and `L_pick` for a feasible chosen `(i*,s_k*)`. The rigorous **whole continuous-dose-and-timing regret certificate** is

\[\sup_{v\in X,\ s_0\in I}J(v,s_0)-J(e_{i_*},s^*_{k})\le\max(0,U_{\rm grid})+\tfrac12(2M_0\|w\|+L_c)h-L_{\rm pick}.\tag{18}\]

This bound can be loose but is executable with **zero further source measurements** once the acquisition record is frozen. The direct source, not the interpolated polynomial, supplies its Lipschitz guarantee. The separately executed timing pilot below passes a 0.01 absolute-reward regret threshold, even though the global **all-waveform** operator certificate remains useless.

## 6. Verified numerical pilot: what passed and what failed

`prototype.py` creates a grounded symmetric conductance matrix on a connected 180-node RC graph with positive capacitors; the physical oracle computes scalar terminal step responses. The learner never receives its 180 hidden eigenvalues, eigenvectors, graph, true response matrix, or the four generating port-mixing patterns. Four columns are adaptively acquired; an extremely weak independent port component prevents an exact low-rank assumption. All 24 physical port diagonals and each selected column are measured with absolute normalized scalar error at most `1e-7`.

Execution (`results.json`): 24 ports, four selected, eight log-time blocks, polynomial degree 22, 1,956 scalar experimental settings, earliest time `0.004`, horizon `5`. Minimum required raw output accuracy equals `eta*t0=4e-10` **in the benchmark's voltage/response units**. The sum of experimental input durations is `1310.6` time units **excluding resets, setup, sensor averaging, and manufacturing**. A generic dense per-time full-port acquisition would use 55,200 scalar settings, but **this is not the strongest ordinary comparator**: adaptive pivoted Cholesky can also learn the relevant port columns with O(mr) readings, and must receive credit for that machinery.

The uniform all-action error bound (13) is `2.5442`, much larger than useful decision margins; it is explicitly **not** a successful all-control performance certificate at this tolerance. The maximum withheld full-matrix step error on a 221-point diagnostic grid is `1.6205e-5`. This diagnostic cannot replace (13). A strong ordinary cubic spline applied to the identical low-rank readings has max withheld error `1.5180e-5`, slightly **better** than this construction. AAA with its fixed demonstrated parameters has error `9.16e-4`; this does not establish superiority over optimized rational fitting.

The task-specific theorem **does** decide a genuinely later, previously unmeasured 24-action menu. At terminal `T=5`, the goal is the current-induced response of port 7. Exactly one unit current is applied to one chosen original port during `[3.5,4.5]`. All actions have the same current duration; a newly specified known extra port-7 price of `0.1` reward units changes the best port. The exact/source-hidden optimum is port 4 and the learned choice is also port 4. The source-consistent certified lower score for port 4 is `0.114915335698`, and the maximum certified upper score for any competitor (port 7) is `0.106645569401`; **the strict certificate margin is `0.008269766298`**. By the preceding theorem, port 4 is also the certified unique optimum over the **entire continuum of nonnegative fractional 24-port allocations with total amplitude at most one and the same pulse window**, not merely the 24 vertices. It uses zero new physical/source measurements. All 24 simulated true menu values were checked to lie inside their acquired intervals. The actual port-4 reward is `0.119049355165` but this true value was never passed to the learner.

**Continuous scheduling beyond that fixed window.** The additional `test_continuous_time.py` freezes the identical 1,956 scalar records, then optimizes a completely new **infinite action set**: all nonnegative port-current mixtures with total instantaneous amplitude at most one, one rectangular pulse of duration 1, and an arbitrary continuous start time `s` in `[0,3.996]` (at `T=5`, every resulting step-response lag is at least `t0=.004`). A 4,001-point offline time grid and (18), using source-derived temporal Lipschitz bounds, select pure port 7 at start `s=3.996`, rather than port 4 at the *previously fixed* pulse time. The certified global upper reward is `0.380366049839` and the chosen intervention's certified lower reward is `0.370736031853`: therefore **global regret is at most `0.009630017986` over every fractional port mixture and every continuous permitted onset time** under the source and sensor premises. Withheld simulation gives the chosen true reward `0.374774281494`; its grid optimum coincides, but that finite withheld grid is not the basis of the certificate. No additional source data were acquired. This demonstrates why selecting a controller among fixed pulses and optimizing the timing jointly are different operations, and why the task-specific proof is materially stronger than the failed `Delta=2.544` all-waveform radius.

These are **simulated, idealized, finite-precision calculations**, not real RC measurements, formally interval-verified floating arithmetic or a demonstration of realistic sensor precision. The analytic bounds are exact-real conditional on the stated error intervals; a deployed implementation must add explicit timing and floating-point enclosure costs. The numerical output is only a pilot of the derived algorithm.

## 7. Strongest conventional solution and the honest comparison

The substantial old ingredients are: complete-monotonicity/operator-valued spectral measures for RC ports (Zemanian 1974); positive-kernel Nyström/pivoted Cholesky from measured Gram columns (existing matrix methods, including Tropp et al. 2024/2025); classical Chebyshev/analytic approximation (Bernstein, Trefethen); and measured-transfer rational interpolation, Loewner/AAA/vector fitting (Antoulas, Aumann–Gosea). The strongest equally informed alternative is **adaptive low-rank Gram acquisition followed by a noise-aware passive Loewner or positive matrix-measure fit**, with control objectives optimized and a task-specific generalized-moment dual certificate. It can consume essentially the **same** source information as this algorithm, not a more expensive full dense matrix; its fit may be better, and its optimal-consistency intervals may be tighter than (17). We have **not** run a complete comparable passivity-enforced Loewner/matrix-measure SDP and cannot claim it loses.

For the source-consistency comparator, each scalar measurement imposes a linear interval constraint on a nonnegative matrix-valued spectral measure `dSigma(lambda)`:

\[q_v(t)=\int_{[0,\infty)} \frac{1-e^{-\lambda t}}{\lambda t}\,v^T d\Sigma(\lambda)v.\]

Every future linear terminal task is another linear functional of the *same* measure. Sharp minima and maxima are therefore generalized moment-cone optimizations, potentially more informative than the Cauchy–Schwarz relaxation (17), but requiring a charged solver and, for finite numerical discretization, a **certified discretization error**. Our concrete advantage is an explicit low-dimensional **source-warranted certificate** with no hidden pole bound or general-purpose SDP. Historical novelty and better end-to-end cost remain **unknown**.

The pinned Astra N1571 source provides a stronger-than-ordinary **static** passive resistor-network source-response compiler under controlled conductance additions, including noisy acquisition and convex consumer proofs. That is distinct from this dynamic **current-to-terminal-time response** source; using it does not grant our actuator/sensor interface. It motivated direct physical and information-cost accounting rather than implying a transfer of its result.

## 8. Hardest unpaid obligations and decisive failure boundary

1. **Scientific qualification of linear passive truth.** A real network may contain state-dependent conductivity/capacitance, active components, aging, thermal drift, hysteresis, metastability, faulty resets, or noncollocated sensors. None is inferred from good interpolation. Even two different nonlinear devices can agree at every admitted small probe but disagree at an untested large waveform. Physical law/source qualification must precede safety-critical use; without it, (4) can fail.
2. **Metrological throughput.** The native experiments require known current waveform, same-source reset, calibrated *collocated* scalar readout and stable `eta`, including gain/offset/carryover/timing. A raw scalar signal error at time `t` is amplified by division by `t`. At short `t0` this can make the all-controller certificate financially or physically useless. Sample repetition does not eliminate systematic drift.
3. **Useful-scale control.** The broad uniform radius (13) failed in the completed pilot. Task-specific continuous fractional allocation **and continuous single-pulse onset** passed a 0.01 source-model regret bound; this is still not a globally optimized robust regulator over arbitrary multi-pulse, feedback, nonlinear or state-dependent policies. Need a stronger task-conditioned program over a continuous space of bounded-variation inputs; optimize the source-consistency dual before claiming a general controller.
4. **Strong conventional comparator.** Implement the matrix-valued moment-cone/PSD spectral fit with the **same 1,956 scalar reports and source assumptions**, and optimize identical menus/time budgets. A close match or a tighter conventional certificate would make this a useful composition, not a unique breakthrough.
5. **Execution precision.** Chebyshev sample-time and coefficient rounding, timestamp error, source response digitization, rational/interval arithmetic for endpoint comparisons, current and energy bills, noise distribution, and real hardware measurement must all be charged. A laboratory demonstration and independent proof check remain absent.

**Scope earned:** source-independent, dimension-independent finite-**setting** acquisition and sound future waveform/terminal-task certificates for a declared stable, linear, collocated passive class, with a successful unique 24-port *continuous allocation* decision at fixed timing and a source-certified `<0.01` global regret over continuous single-pulse timing and allocation, despite failure of the all-waveform uniform performance certificate. **Not earned:** a novel universally dominant method, an empirical device, a nonlinear reactor/fusion/biological controller, or civilization-scale deployment.

## 9. Readback and primary provenance

Starting Astra SHA: `5489b118101275c81500d823361592c670ec77bb`.

- `00_START_HERE.txt` fetched verbatim at start, Git blob SHA `8ce877e5f6f420d7ed057fb178498cc58447b069`.
- `knowledge/current/packets/N1571.json`, Git blob `25aeacda2c98bf24743df582a5c39955570ccdaa`.
- `research/2026-11-01-reusable-control-noisy-passive-response/source/p1-direct-reusable-control/members/Astra_Reusable_Control_20261101/work/physical/PASSIVE_NETWORK_BINDING.md`, Git blob `13da0a5a319c31ca9cd22e0417b0f522a7284bd2`, source SHA256 `cbb2995c62c7fbfa23447318dfb25bbd795aad440c9f8ba952a48ed2050fcd2d` recorded by the pinned packet.
- `.../work/comparators/INTERVENTION_ORDER_LOWER_BOUND.md`, Git blob `b6e183344a0ae3e5a02d265d8ec960b864bfeb56`, source SHA256 `6e8cb95c2ae293e192a6215423a59bd9351081921944c7bc88e7a0ae314c843` in packet.
- `.../work/control/CONTROL_CONSUMER_PROOF.md`, Git blob `991bf3ef5fd2e590a360f1fcda2ae16a7e57b285`, packet SHA256 `e56af153ae64557f4f60712dbf14579cf21e45fc820fd6ba25f46c37df612987`.

Primary external comparators, with URLs:

- A. H. Zemanian, **Relaxive Hilbert Ports**, SIAM J. Control Optim. (1974), https://doi.org/10.1137/0312010.
- **Randomly Pivoted Cholesky** theory, Communications on Pure and Applied Mathematics, https://doi.org/10.1002/cpa.22234.
- Aumann–Gosea, **Practical challenges in data-driven interpolation** (published online 2023), https://doi.org/10.1002/acs.3691.
- Ionita–Antoulas, **Data-Driven Parametrized Model Reduction in the Loewner Framework**, https://doi.org/10.1137/130914619.
- Trefethen, Chebfun approximation theory, https://www.chebfun.org/docs/guide/guide04.html.

Exact source contents were inspected at the fixed Astra starting revision; this new artifact is independent of other roles' proposed results. Other sources have not been used to claim an unsupported bridge.