# Independent Astra research opening: bounded-likelihood rare-event intervention from partial physics

**Independent construction, 2 November 2026.** Starting public Astra corpus pinned at Git revision `5489b118101275c81500d823361592c670ec77bb`. This is an independent mathematical/computational research note, not a collaboration synthesis. The construction was selected before inspecting Astra or the literature; prior art and Astra were checked afterwards. No novelty or physical breakthrough is asserted.

## Intended scientific capability

Given an unknown physical system, make scientifically useful *risk decisions about intervention candidates* when consequential outcomes are so rare that passive tests cannot resolve them. Avoid learning the complete microscopic state transition model if that is not required to answer the decision. Desired output: a decision-level confidence certificate whose acquisition, actuation, stochastic information, time, precision and operating costs are explicit.

The first attempted opening was bounded-energy near-optimal control from uncontrolled paths. For controlled Brownian noise, the Boué–Dupuis variational identity gives an information-theoretic upper bound on maximum reward and can certify a fixed learned control without identifying the drift. A fairer model-based comparator using the same passive data, cubic drift fitting and **discrete-time dynamic programming** beat the direct conditional controller in our bistable toy experiment (mean net reward 0.33105 vs 0.32194; privileged true-drift DP 0.33231). It is not an algorithmic improvement. This route was used as machinery, then rejected as the strongest opening.

The developed opening instead uses an upper comparison dynamics *only as a proposal distribution for physical noise*, with likelihood correction evaluated on actual system observations. It addresses probability and decision certification, not unconstrained optimal physical control.

## Physically meaningful exact contract

For a duration `T=N Δ`, a scalar observable `S_k` (possibly the projection of arbitrarily complex latent physical states) obeys

    S_{k+1} = S_k + β_k Δ + σ sqrt(Δ) Z_k,   k=0,...,N-1,

where:

1. `σ>0`, `Δ>0`, initial `S_0=s0` and terminal threshold `a` are calibrated; `β_k` may depend on complete hidden state and past observations/randomness, but the physical class is warranted to satisfy **β_k ≤ B pathwise on every trajectory that the proposed intervention can create**. Only `B` is furnished to the algorithm. It is not inferred by a finite successful goodness-of-fit test.
2. The baseline exogenous input is independent standard Gaussian `Z_k`. A *real controllable random-force port* allows the experimenter to replace the input law, on every step, by the explicitly specified conditional density `q_k(z|S_k)` and log the actual `Z_k`. Equivalently, a finite-alphabet baseline can be switched to an exact rational conditional coin law. The port must be nonanticipative, and all noise entering `S` outside `β_k` must be included in the known random-input law. Other hidden randomness may affect `β_k`, with the same conditional laws under baseline and proposed experiments.
3. The environment's update rule, hidden memory and any internal random tape are invariant to the *choice of the noise law* except through the actual fed values `Z_k`. Replacing the noise generator must not introduce an unmodelled force, heating, response delay or protocol-dependent hidden transition.
4. Independent episodes are prepared from the same full initial hidden-state distribution; each has a real preparation, reset, acquisition and time cost. The mathematical theorem does not license this preparation for a laboratory by fiat.
5. Goal: determine `p_0 = P_baseline(S_N≥a)` or compare `p_{0,j}` for a finite set of mitigation variants, with simultaneous finite-sample confidence. This is a terminal observable: maximum-over-time hitting risk is a **different event** and requires a changed bounding harmonic function.

On the stated interface, the observer does **not** need the hidden drift, Markov state, microscopic generator, potential, exact rare-event conditional law or source history reconstruction. The global bound and noise port are much stronger physical inputs than ordinary uncontrolled observations.

## Representation-level theorem: tilt a solvable upper process, not the unknown system

The scalar Gaussian model below is an *executable instantiation* of a more general operation. On a partially ordered observable space, suppose each physical transition `s_{k+1}=T_k(s_k,h_k,z_k)` (with any hidden memory `h_k`) satisfies the **pathwise** dominance `T_k(s,h,z) ⪯ U_k(s,z)` for a known tractable upper process `U`. Let the baseline innovation have known density/mass `p(z)`, independently reprogrammable by the experimenter. Choose a positive monotone terminal score `F`, and suppose the functions

    H_N=F,
    H_k(s)=E_{z~p}[H_{k+1}(U_k(s,z))]

are exactly computable and monotone for every admissible state. Then the proposed conditional kernel

    q_k(z|s)=p(z) H_{k+1}(U_k(s,z))/H_k(s)

is normalized and positive. Its exact likelihood `L=∏p(z)/q(z|s)` obeys

    L F(s_N) ≤ H_0(s_0)                                      (A)

**pathwise for every hidden-memory law in the dominance class**. For any upward-closed target set on which `F(s)≥f_min>0`, the unbiased importance weight `L 1{target}` lies in `[0,H_0(s0)/f_min]`. This removes the need to solve the actual system's committor, generator or optimal-control PDE: one solves the *upper comparison process*. It does **not** remove the potentially hard task of verifying pathwise dominance or finding an explicitly solvable monotone `H`. The theorem follows by telescoping the likelihood and applying monotonicity at each dominated transition, as proved in the scalar case below.

The full ability to reprogram the input law is a structural intervention assumption; the theorem does not magically create a force/noise port. The transformation of transition probabilities by a positive harmonic function is the established **Doob h-transform**, not a newly invented operation.

## Construction: exact Doob envelope kernel

For parameters `c<a`, `η>0`, `C>0`, define `Φ` as standard Gaussian CDF and

    F(s) = 1 + C Φ((s-c)/η).
    H_k(s) = 1 + C Φ((s+B(T-kΔ)-c)/sqrt(σ²(T-kΔ)+η²)).

Because convolution of Gaussian tails is Gaussian,

    H_k(s) = ∫ φ(z) H_{k+1}(s+BΔ+σ sqrt(Δ) z) dz,        (1)

where `φ` is the standard Gaussian density. Consequently

    q_k(z|s) = φ(z) H_{k+1}(s+BΔ+σ sqrt(Δ) z)/H_k(s)       (2)

is a normalized, everywhere-positive conditional density. It is computed from `B,σ,Δ,T,c,η,C,s,k` only: **no β is evaluated or fitted**.

It has an exact, constructive one-step sampler. Put

    R_k = σ²(T-kΔ)+η²,
    p_k(s) = Φ((s+B(T-kΔ)-c)/sqrt(R_k)).

With probability `1/H_k(s)`, draw an ordinary N(0,1). Otherwise (probability `C p_k(s)/H_k(s)`), draw `Y~N(0,1)` truncated below `(c-s-B(T-kΔ))/sqrt(R_k)` and independently `V~N(0,1)`, and return

    Z = ρ Y + sqrt(1-ρ²) V,   ρ=σ sqrt(Δ)/sqrt(R_k).

This is a direct Gaussian conditional sampler, **not acceptance/rejection of a rare target event**. It uses conditional continuous sampling, CDF/inverse evaluations and state feedback, whose hardware/bit costs are not free.

The baseline-to-proposal path likelihood, computable from *observed S and logged Z*, is

    L_N = ∏_{k=0}^{N-1} [ φ(Z_k)/q_k(Z_k|S_k) ]
        = ∏_{k=0}^{N-1} [ H_k(S_k)/H_{k+1}(S_k+BΔ+σ sqrt(Δ) Z_k) ].    (3)

### Theorem A: exact bounded-weight estimation without a drift model

For the complete physical interface above and every hidden/historical drift process satisfying `β_k≤B`, define the indicator `A_N=1{S_N≥a}` and weighted output `Y=L_N A_N`. Then

    E_q[Y] = P_0(S_N≥a)=p_0,
    0≤Y≤K = H_0(s0)/F(a)  on EVERY trajectory.           (4)

**Proof of unbiasedness.** On each fixed native hidden random tape, both experimental laws generate the same physical response as a measurable function of the *applied* noise tape. The sequential joint density of the noise tape under the proposal is `∏q_k(Z_k|S_k)` and under baseline is `∏φ(Z_k)`. All other conditional physical factors agree by the native-channel invariance assumption and cancel. Equation (3) is the Radon–Nikodym derivative on complete histories; integrating the indicator gives the baseline probability. No independence of hidden `β_k` and the recorded past is needed; the baseline innovations must remain correctly specified and independent of that past.

**Proof of the pathwise cap.** `β_k≤B` gives

    S_{k+1} ≤ S_k+BΔ+σ sqrt(Δ) Z_k.

Each `H_{k+1}` is monotone increasing, so its value at the actual next state is bounded by its value at the upper-envelope next state. Therefore

    L_N H_N(S_N)
      = [H_0(S_0)/H_1(upper_1)]
        [H_1(S_1)/H_2(upper_2)] ...
        [H_{N-1}(S_{N-1})/H_N(upper_N)] H_N(S_N)
      ≤ H_0(s0).

Since `H_N=F` and on `S_N≥a` we have `F(S_N)≥F(a)`, it follows that `L_N 1{S_N≥a}≤H_0(s0)/F(a)`. The cap does not depend on unknown hidden dimension, the detailed drift, or waiting for a naturally rare outcome. QED.

### Finite-sample confidence and intervention decision

For `n` independent acquired episodes, let `Y_i∈[0,K]`, empirical mean `m` and unbiased sample variance `v` (n≥2). The two-sided empirical Bernstein confidence interval used in the code, using a union of one-sided bounds, is

    p_0 ∈ [m-r,m+r] intersect [0,K],
    r = sqrt(2 v log(4/δ)/n) + [7K log(4/δ)]/[3(n-1)].   (5)

The standard Hoeffding alternative is `r=K sqrt(log(2/δ)/(2n))`. These are *mathematical coverage statements* only if the exact input-channel and bound premises hold. For `m` intervention candidates, use per-candidate `δ/m` and union bound, and declare intervention `j` safer than `i` only if the former upper endpoint is strictly below the latter lower endpoint.

For relative accuracy `ε`, `Var(Y)≤Kp_0` implies by Bernstein that a sufficient number of independent experiments is

    n ≥ [(K/p_0)(2+(2/3)ε)/ε²] log(2/δ).                (6)

Thus **if** a separately warranted regime ensures `K/p_0≤R` as events become rarer, the *number of complete experiments* for fixed relative accuracy does not have to grow like `1/p_0`. This is a conditional sample-count result: it does **not** eliminate the duration, feedback, implementation precision or physical entropy needed to make the event frequent. A loose `B` destroys the regime.

On the comparison process `β_k=B`, the product in (3) telescopes with equality to `L_N F(S_N)=H_0(s0)`; it is the ordinary zero-variance Doob transform for the *positive surrogate outcome* `F`. The independent construction's substantive conditional boundary is the weaker **inequality** for unknown history-dependent `β_k≤B`, not a novel optimal proposal for the known comparison model. A strongest conventional Doob method with the same comparison process reconstructs precisely the same sampler.

### Information and computational limits, not hidden for free

1. **Zero-experiment conventional comparator.** If the experimenter also warrants `β_k≥b_low`, shared-noise pathwise domination gives

       Φbar((a-s0-b_low T)/(σ sqrt T)) ≤ p_0 ≤ Φbar((a-s0-BT)/(σ sqrt T)).

   No experiment is necessary for questions already settled by these two bounds. In the synthetic test, bounds `[-1.0,-0.6]` on drift produce `0.00042906 ≤ p_0 ≤ 0.00383038`; the desired risk threshold `0.0005` lies inside this interval, so a more informative operation is needed there.
2. **KL price of making rare outcomes common.** If the baseline rare probability is `p` and proposal success is `r`, the data-processing inequality for binary success/failure gives

       D(Q||P) ≥ r log(r/p)+(1-r) log((1-r)/(1-p)).      (7)

   At fixed `r>0` and `p→0`, this is order `r log(1/p)`. Sampling avoids rare *waiting* by paying a nonzero, increasing *distribution-control information* budget. Physical energy to realize this distribution is NOT equal to KL by definition and needs independent thermodynamic/hardware characterization.
3. **No uniform relative guarantee from a one-sided bound alone.** Let a valid constant hidden drift tend to `−M` with `M→∞` while the sampler is still built with a fixed `B`. The baseline `p_M→0`, and for any fixed finite-horizon `q` here the proposal success `r_M→0` as well. By Cauchy–Schwarz, `(E_q Y)^2 ≤ Q(A) E_q Y²`, hence `Var(Y)/p_M² ≥ 1/r_M−1→∞`. A one-sided upper bound does not confer rarity-independent relative sample complexity.
4. **Numerical implementation error.** Gaussian CDF/inverse arithmetic is floating point in the demonstration. The exact theorem requires exact `q`; production code requires a finite-precision, detector and generator error budget. A sufficient *strong* contract, for every physically reachable input, is

       exp(-ε_k) q_k(z|s) ≤ qtilde_k(z|s) ≤ exp(ε_k) q_k(z|s).

   Using actual `qtilde` likelihoods preserves unbiasedness and raises the pathwise cap only to `K exp(Σ ε_k)`. If weights instead use `q` while sampling `qtilde`, unbiasedness can fail. On unbounded Gaussian support, a global multiplicative density approximation is highly nontrivial. The exact finite-alphabet construction below avoids this arithmetic assumption but changes the physical noise contract.
5. **Pilot selection.** Choosing `C,c,η` from the same evaluation trajectories invalidates uncorrected confidence. Tune using separate pilots or use uniform confidence sequences/other appropriate multiple-testing control. Reported tests fixed parameters before separate evaluation.

## Exact finite-alphabet representation: no Gaussian primitive

For a digital random-input source, let baseline `Z_k∈{-1,+1}` be exact fair bits, `r=σ sqrt(Δ)` a rational increment and `BΔ` rational. Choose `F(s)=1+C 1{s≥a}` for integer `C>0`. Then

    H_k(s) = 1 + C 2^{-(N-k)} Σ_{j=0}^{N-k} binom(N-k,j)
                     1{s+(N-k)BΔ+(2j-(N-k))r≥a}.

All `H_k(s)` and

    q_k(+1|s) = H_{k+1}(s+BΔ+r)/(2 H_k(s)),
    q_k(-1|s) = H_{k+1}(s+BΔ-r)/(2 H_k(s))

are exact positive rationals; recursion and cap work identically with `K=H_0(s0)/(1+C)`. This removes the Gaussian inverse-CDF and continuous-density bit precision from the *mathematical/executable* mechanism. Binomial tables can be precomputed in `O(N²)` integer additions and `O(N)`-bit rationals; per episode, exact conditional bits can be drawn using fair-bit integer rejection with finite expected bit cost and **unbounded worst-case random-bit time**. The binary device's physical baseline must actually be digital; this does not reproduce an intrinsic Gaussian diffusion without an extra approximation/error theory.

`exact_binary_twist.py` enumerates **all 4,096** length-12 noise tapes, with hidden-memory state `h <- (5h+(3 if Z=+1 else 1)) mod17` and a history/state-dependent drift decrement. All probabilities and weights are `fractions.Fraction`; it verifies EXACTLY:

    ∑_{tapes} q(tape) = 1;
    ∑_{tapes} q(tape)L(tape)1{event} = 1/2048;
    max_tape L(tape)1{event} ≤ 24241/1048576.

The conditional proposal's event probability is about 0.1342 versus baseline `1/2048`; the exact probability estimate is unbiased and pathwise bounded. This is an exhaustive finite model check; the general theorem is the analytic argument above, not the enumeration.

## Executed numerical experiments

### A. First attempted model-free optimal control, with a fairer comparator

A one-dimensional double-well diffusion with drift `b(x)=2(x-x³)` held hidden from learning, `σ=.9`, `T=2`, `Δ=.01`, initial `−1`, goal `X_T>0.5`, `λ=.4`, bounded `|u|≤3`. 25,000 passive training episodes, 25,000 independent passive certification episodes, and 25,000 independent on-policy episodes per policy. The unrestricted Brownian variational value is **an upper bound, not the attained capped-actuator optimum**.

- Direct conditional estimator controller: objective 0.321936, rare/success event frequency 0.5574, certified upper-minus-lower gap ≤0.043688 (95%).
- Fair equal-data cubic drift fit + full **discrete-time DP**: objective 0.331052, certified gap ≤0.034296 (95%); **better than the direct method**.
- Privileged true-drift DP: objective 0.332307, used only as diagnostic. It is not an allowed same-information comparator.

This failure redirected the scientific task from claiming a better controller to a different certified rare-event intervention operation. Code: `run_experiment.py`; numerical outputs `results.json`, diagnostics `diagnostics.npz`.

### B. Adaptive Gaussian noise experiment with unknown drift

Hidden physical test dynamics `β(s)=−0.8−0.2 tanh(2s)`, actual bounded within `[−1,−0.6]`; the algorithm receives ONLY upper bound `B=−0.6`, not the drift expression. `T=1`, `Δ=.005` (`200` steps), `σ=.6`, `s0=0`, `a=1`, `c=.92`, `η=.05`, `C=500`. The goal is **terminal** `S_T≥1`.

At **50,000 independent runs per method**, conventional passive sampling gave 41 target events (estimate 0.00082). The fixed Gaussian-shift importance sampler, using the same drift bound and `u=(a-s0-BT)/(σT)=2.66667`, gave 14,806 target events (proposal frequency 0.296), weighted estimate 0.00067934. The adaptive envelope kernel gave 15,854 target events (proposal frequency 0.317), weighted estimate 0.00068094. Both importance samplers used exact likelihood formulas for the specified numerical input law and the same global `B`.

| Method | 95% interval (risk probability) | Width | Sampled pathwise weight ceiling | Approx proposal KL/episode |
| --- | --- | ---: | ---: | ---: |
| Passive (Clopper–Pearson) | [0.00058851, 0.00111226] | 0.00052375 | 1 | 0 |
| Constant Gaussian shift (empirical Bernstein) | [0.00065347, 0.00070522] | 0.00005175 | 0.02856550 | 3.562 |
| Envelope Doob noise kernel (empirical Bernstein) | [0.00066538, 0.00069650] | 0.00003112 | 0.00822612 | 3.385 |

Adaptive interval about 16.8 times narrower than passive and 1.66 times narrower than restricted constant Gaussian shift. The equal-information **unrestricted Doob h-transform importance sampler** on the comparison process is exactly equation (2) and therefore TIES, not loses. The numeric comparison is not an advantage over strongest established methods. KL in nats is measured as `-E_q log L`; it does not fix the actual device energy, control bandwidth or preparation effort. See `dominated_twist.py`, `dominated_twist_results.json`.

### C. Task-level mitigation choice at a declared risk budget

Two physical response variants were given **the same upper B, same observation/actuation class, same q sampler**, and **25,000 active and 25,000 passive independent episodes per variant**. The learner did not observe their drift formulas. The mitigation lowers the hidden drift by `0.08` (simulator-only information). We used one-sided-risk threshold `τ=0.0005` and Bonferroni `δ_i=.025` per arm for a joint 95% statement.

- Untreated: active weighted `p=0.00068658`; joint 95% interval `[0.00066161,0.00071154]`, **above τ**.
- Mitigation: active weighted `p=0.00042330`; joint 95% interval `[0.00040459,0.00044200]`, **below τ**.
- Thus the active experiments CERTIFY (conditional on actual contract) both a risk reduction and the mitigation satisfying the risk budget. The simultaneous intervals imply a **minimum relative reduction of 33.19%** (using `1 − upper(mitigation)/lower(untreated)`), with 95% joint coverage.
- Passive equal-run intervals were `[0.00048369,0.00135259]` and `[0.00014570,0.00073507]`: neither certifies its arm with respect to the threshold, nor a strict ranking.

The endpoint has not been physically actuated or measured; this is a completed *synthetic decision* with full randomized sampling. See `decision_test.py`, `decision_results.json`.

## Strongest ordinary solution and Astra source cross-check

The direct method is **not novel**. The log-partition control identity follows from Boué & Dupuis (1998), `https://doi.org/10.1214/aop/1022855876`. The control/desirability transform and transition-probability tilt are established in Todorov (2006), `https://papers.nips.cc/paper/2006/hash/d806ca13ca3449af72a1ea5aedbed26a-Abstract.html`, and Todorov (2009), `https://doi.org/10.1073/pnas.0710743106`. Adaptive/state-dependent importance sampling and subsolutions were developed by Dupuis & Wang (2004), `https://doi.org/10.1080/10451120410001733845`, and Dupuis & Wang (2007), `https://doi.org/10.1287/moor.1070.0266`. Variance-adaptive confidence builds on Maurer & Pontil (2009), `https://arxiv.org/abs/0907.3740`. The conditional bounded-weight comparison is an independently derived composition of this machinery; no comprehensive priority audit was performed, and no unique novelty is claimed.

Astra sources at exactly revision `5489b118101275c81500d823361592c670ec77bb` were fetched using GitHub's pinned file endpoint (the optional live Astra research retriever was not connected):

- `00_START_HERE.txt`: Git blob `8ce877e5f6f420d7ed057fb178498cc58447b069`; current packet navigation and pinned source guidance.
- `knowledge/current/packets/N1596.json`: Git blob `00172e244b859006eb48f3f7d204f2e99d06dbc3`. Its governing `research/2026-11-01-native-excursion-thermal-interaction-and-spin-memory/source/p1/FINAL_PREFIX_TRUNCATED_20000.txt` was read from lines 1–120. Existing result compares **relative all-deadline failure probabilities for finite CTMCs** under local rate perturbations with the SAME full state graph. Rates and complete-state access are furnished, unlike our noise-channel operation. The surviving source is only a truncated prefix; unacquired producer files stay unacquired.
- `knowledge/current/packets/N1602.json`: Git blob `aec72ea134adf4b4f6813fcb0aa161dc047b2300`. Governed by `research/2026-11-01-reviewed-actual-kinetics-retained-clocks-and-task-interfaces/source/dots-new/04-Astra_Ordinary_Langevin_Mean_Passage_Time_20261031/members/audit_constant_spd_mfpt_theorem_20261031_2239/received_candidate.md`, read lines 1–85. Internally accepted final scope reports full Gibbs-basin mean and separate CDF bounds for **specified high-dimensional quartic Langevin potentials/mobilities**, not uncontrolled unknown drift with programmable random-force selection. Its original source alone is a candidate; acceptance is at later narrowly reviewed freeze, not retroactively at the original draft.
- `knowledge/current/packets/N1276.json`: Git blob `5cf13169ba0d960a5548da3463a2f3c739d80eec`. Its `research/2026-10-29-physical-control-and-persistence/source/p1-stationary/new_science/continuation3_20261029/BOUNDED_STATIONARY_CHANGE_OF_MEASURE.md` was read lines 1–98. It reweights the **invariant endpoint law** using a physical counter and a bounded number of native calls; does not supply independent rare-event experiments, a controlled Gaussian noise port or a terminal risk estimator.
- `knowledge/current/packets/N1312.json`: Git blob `30d85c2018dd62355786e04dd8769277fd03b568`; governing `research/2026-10-29-controlled-transport-and-operation-debiasing/source/p1-transport/new_science/continuation7_20261029/CONTROLLED_MACROSCOPIC_ACTION.md` read lines 1–90. Its source-qualified controlled ring current large-deviation action depends on actual selective phase/clock controls, own-swap symmetry and time scales; it does not acquire our noise channel or yield this endpoint probability certificate.
- `N547`–`N551` Astra stationary-generator tomography packets were also read at the pinned revision; their exact stationary density, full-state and known-control assumptions are not silently imported.

These are different **input/operation/output contracts**, not automatically composable discoveries. No quantum-channel undecidability premise is used or challenged.

## Achieved scope versus unpaid obligation

**Achieved:** Exact mathematical construction of a drift-independent, likelihood-corrected conditional noise intervention with pathwise bounded weights, an explicit adaptive sampler, and rigorous finite-sample risk ranking under declared experimental access; an exact exhaustive hidden-memory, finite-alphabet verification; several synthetic Gaussian experiments, a fairer control baseline, analytic zero-experiment comparator and an information-theoretic resource lower bound.

**Not achieved:** (a) a practical actuation port meeting the noise-only intervention law without changing hidden physics, (b) an independently established controlled-reachable one-sided drift bound for a consequential molecular, biological or energy system, (c) fully validated finite-bit Gaussian channel/likelihood precision, (d) a physical preparation/time/energy cost comparison, (e) a proof of full-dimensional scalable rare-event efficiency, (f) a new state-of-the-art algorithm versus an equally informed adaptive Doob/subsolution baseline, or (g) any civilisation-changing scientific capability in practice.

**Hardest next scientifically real obligation:** Select a real experimental platform in which the *entire stochastic innovation driving the measured risk observable can be independently injected and logged*, and produce a blinded empirical verification of the global drift dominance and protocol invariance across all proposed noise policies. A digital stochastic electronic or programmable Brownian emulator is a plausible first *apparatus qualification* (not evidence of chemistry/biology applicability). Establish device-level precision, bandwidth, injection energy and reset cost and compare with conventional accelerated-stress testing and best Doob/IS control **on identical physical ports and resources**. Without this acquisition, the impressive numerical certificates remain conditional synthetic results.

## Reproduction

`python exact_binary_twist.py` — exact rational exhaustive proof check (4096 paths).

`python dominated_twist.py` — three independent candidate/no-control batches at `n=2000,10000,50000`; writes `dominated_twist_results.json`. Requires NumPy/SciPy.

`python decision_test.py` — independent two-intervention tests at 25k episodes per method per arm; writes `decision_results.json`. Requires NumPy/SciPy.

`python rare_event_bridge.py` — conventional constant Gaussian shift and first-passage event variant; writes `rare_event_results.json`.

`python run_experiment.py` — earlier path-integral control/certification and equal-data/privileged model-based comparisons; writes `results.json` and `diagnostics.npz`. May require considerably more CPU.

Pinned root does NOT include this independent contribution; it has deliberately not been published into the Astra repository before the three-role selection, so other independent roles cannot accidentally inspect it.
