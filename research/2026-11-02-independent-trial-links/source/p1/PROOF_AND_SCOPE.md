# Astra independent contribution: killed-excursion acquisition and task-only prediction under hidden kinetic memory

**Frozen public Astra reference:** `5489b118101275c81500d823361592c670ec77bb` (read-only). **Independent date:** 2026-11-02. **Evidence status:** new analytic construction, exact rational counterexamples, and synthetic executable tests, *not* externally peer-reviewed originality, physical acquisition, validated chemistry, or a civilisation-changing capability. No other trial role's materials were consulted.

## 1. Chosen obstruction and consequence

Consequence: select interventions for the yield of a long-lived multistep chemical/biological transformation when full successes are astronomically rare and experiments on individual stages are ordinary. Examples are sequential repair, molecular synthesis and protective pathways; none is demonstrated physically here.

Two separate obstacles: (i) hidden residence-time histories between *known complete* boundary microstates; (ii) hidden kinetic modes **carried across** successive stages. The first admits a classical exact-milestoning-style transfer; the second can make a projected boundary process invalid. A task-only sign decision turns out to need much less than full hidden-state identification, but only with additional structural qualification. Treat them separately.

## 2. Astra source route pinned before external transfer

- Initial route: `00_START_HERE.txt`, pinned blob SHA `8ce877e5f6f420d7ed057fb178498cc58447b069`; `agent/COMPOSITION.txt`, `knowledge/README.md`.
- `knowledge/current/packets/N1596.json` at the frozen revision describes a source-reported complete-excursion rowwise relative comparison for same-full-state same-support finite CTMCs, all deadlines, with non-free full-state preparation and rate acquisition. Its decisive original **visible prefix only** is `research/2026-11-01-native-excursion-thermal-interaction-and-spin-memory/source/p1/FINAL_PREFIX_TRUNCATED_20000.txt` (SHA256 `35c8a69d6fba95231519c34cd1b9aa52d57b31b4afb6ecb838131c9afe9e4131`, lines 1–488). No full source archive/producer audit acquired; no new acceptance claim.
- Negative transfer: `knowledge/current/packets/N1037.json` and governing `research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-completed-method-study/source/q63s1/PROOF.md` (SHA256 `9875ef6736d6f14c35e75b45dde114304e3abee8aec665cf8c723b09b470e5d9`). Exact SPD M-matrix one-port shunt tomography assumes *calibrated and addressable* physical shunts, not present in generic chemistry. The algebraic Schur complement cannot be imported as free kinetic control. Strong alternative is ordinary kinetic model fitting and full-state linear solve.
- External decisive primary: Aristoff, Bello-Rivas, Elber (2016), *A Mathematical Framework for Exact Milestoning*, `https://pmc.ncbi.nlm.nih.gov/articles/PMC4879838/`, especially §2.2: a milestone **point** with correct crossing state, not a lossy label, is required for exact semi-Markov reconstruction. This already owns the short-excursion/long-first-passage paradigm. Other established machinery: Jaeger (2000), *Observable Operator Models for Discrete Stochastic Time Series*, DOI `10.1162/089976600300015411`; Hsu, Kakade, Zhang (2012), *A Spectral Algorithm for Learning Hidden Markov Models*, DOI `10.1016/j.jcss.2011.12.025`; Brown, Johnstone, Macgibbon (1981), *Variation Diminishing Transformations*, DOI `10.1080/01621459.1981.10477730`. Existing total positivity / spectral theory has priority as a general method; the specific task-facing composition here is not claimed historically novel.

## 3. Exact killed boundary-excursion compiler

Let X be a time-homogeneous strong Markov process on full microstates. Let S be a finite set of *complete* prepared boundary states; let B be successful product; let D be independently and permanently absorbing degradation, e.g. an exponential rate µ>0. Start at i∈S, then define the first *return or arrival* to S following departure, or arrival to B/D. Define the sub-stochastic first-excursion boundary kernel

K_ij = Pr_i(next boundary S_j occurs before B and D),
g_i = Pr_i(success B occurs before any boundary return or D).

On the event of returning to S_j, the Markov property makes the next success probability u_j independent of prior history, **provided S_j identifies the actual entry microstate** (if S_j is just a lossy macro-label this is false). Thus

    u = g + K u,     u = (I-K)^(-1) g = Σ_{k≥0} K^k g.

Assume spectral radius ρ(K)<1. For independent Exp(µ) D and completion time τ_B this is precisely u_i=E_i[exp(-µ τ_B)1_{τ_B<∞}]. Neither a deterministic deadline CDF nor conditional survival beyond a fixed time is obtained by this computation.

If a chosen boundary microstate i has known outgoing physical CTMC rates q_ij toward other boundary states, q_iu toward hidden gateways u, and independent death µ, define locally *acquired* gateway-discounted return probabilities H_uj=E_u[exp(-µ τ_S)1_{X_τS=j}]. Then

    K_ij = [q_ij + Σ_u q_iu H_uj]/[µ+Σ_{k≠i}q_ik].

Similarly any direct successful exit contributes to g_i (and hidden-to-product excursions can be included explicitly). The physical experimental service must be able to prepare **each u in its actual microstate** and observe boundary/death/product outcome; changing boundary q_ij must leave all corresponding H_uj unchanged. Physical action gain, hidden gateway access, experimental death and reset cannot be supplied by matrix algebra. Each gateway native experiment ends in a competing return or death; its mean duration is finite when µ>0, but preparation costs remain external.

### Uniform learned intervention bounds

Independent Bernoulli gateway assays estimate each H_uj. Exact Clopper–Pearson intervals plus a union bound yield a single 1−δ confidence event for all H entries; its validity does not depend on selecting a downstream intervention after looking at the data. If the known intervention changes only outgoing boundary rates and K is monotone in each H, evaluate all candidate designs at simultaneous H lower and upper endpoints. The matrix inverse expansion proves elementwise validity for all of them. A design maximizing the conservative lower yield has guaranteed true yield at least (max candidate lower)/(max candidate upper) times optimal true yield. A strong conventional implementation can do the same: this is **not** a unique algorithmic win.

### Rowwise relative transfer, for already complete and qualified boundary states

Extend K,g with absorbing success/death to a stochastic kernel on a finite boundary chain. Suppose two kernels have identical positive support and each affected row i satisfies 0<m_i≤ \tilde P_{ij}/P_{ij}≤M_i for all positive j, including success/death. If eventual absorption is almost sure and success probabilities are positive, then

    Π_i (m_i/M_i) ≤ \tilde u_x/u_x ≤ Π_i (M_i/m_i).

Proof: change one row i. Let A,D be probabilities that the *first complete excursion away from i* terminates in success/death before returning to i. Since the rest of the generator is unchanged, each is a nonnegative linear function of the outgoing row. Hence A',D' ∈ [m_i A,M_i A] and [m_i D,M_i D]. Then u_i=A/(A+D) and m_i/M_i≤u'_i/u_i≤M_i/m_i. From another x, success is α_x+β_x u_i with nonnegative α,β unchanged, giving the same bound. Iterate rows. This preserves the once-per-row advantage of complete excursions rather than paying per return. It needs **all** admitted failure routes and is not a substitute for Astra N1596's deterministic-deadline theorem; the interface is different.

## 4. Synthetic gateway experiment: results and comparator

`test_compiler.py` uses 40 stage boundary states S_i and 40 hidden transient trap states T_i, with all native rates specified in the tester but hidden return probabilities only *experimentally* acquired by the learner. µ=.30. Sample M=20,000 independent competing-return/death experiments per trap, 800,000 total; observed total gateway duration 844,245.882 model units, **not including** microstate preparation or shunt calibration. Simultaneous 99% Clopper–Pearson gateway intervals (SciPy double-precision reported endpoints, not formal outward numeric certification) yield:

- Exact true success 3.1252712734563865e−12.
- Independent full 80-state killed-generator solve 3.1252712734563857e−12.
- Specialized conventional O(N) stage recurrence 3.125271273456385e−12, **a comparator tie** at full acquisition/evaluation information.
- Learned point 3.1315488780963023e−12; 99% interval [2.3636956840890978e−12, 4.140915997821416e−12].
- One exactly specified action doubles exactly two forward rates. All 780 possible pairs evaluated using the *same* gateway confidence event. Conservative maximization selected stages [34,35] (0-index), also the actual optimum in this instance. Exact true yield 6.330741969943553e−12, 2.02566 times baseline. Confidence-certified performance ratio to best admissible design ≥0.5765; no general optimality claim from the lucky exact match.
- Doob success-conditioned chain P*_{ij}=P_{ij}u_j/u_i, g*_i=g_i/u_i generated 1,000 rare-success boundary skeletons with mean 57.2 transitions, but it **requires u already known**; it is not an independent rare-event oracle. Sampling conditional paths does not simulate cost-free physical success.
- An unmodeled direct shortcut of rate 1e−7 raises the output to 7.789806169e−8 (factor 24,925). Unknown support remains a fatal interface.

## 5. Persistent hidden kinetic mode: separate task and precise access

For each **fresh specimen** draw latent Z once at preparation. Z persists throughout the whole sequence. Given Z, each baseline stage succeeds conditionally independently with probability P_Z∈[0,1] and any action a replaces exactly one stage with success probability a_Z∈[0,1], while conditional-independence/response laws stay invariant across stage positions and specimens. Failure of any stage ends the run. Product yield of L stages with one action a is

    Y_L(a)=Σ_z w_z P_z^(L−1) a_z.

What native assays observe from fresh specimens, without latent labels: a_0=E[a_Z], b_0=E[b_Z], a_1=E[P_Z a_Z], b_1=E[P_Z b_Z]. Assays with suffix baseline-then-action stop at first failure and thus require at most two real stage attempts. All native observations count as Bernoulli indicators. **No kinetic mode or conditional action response is supplied to the learner**; only the structural number of modes, persistence, conditional independence and stationarity are admitted. Four assay types can be sampled independently by fresh preparation.

### Two-mode task-only sign theorem

Assume precisely two distinct persistent mode propensities 0≤p_s<p_f≤1, with weights w∈(0,1) and 1−w. Let Δ_f=a_f−b_f, Δ_s=a_s−b_s and define

    d_n=Y_{n+1}(A)-Y_{n+1}(B)
       =w p_f^n Δ_f+(1−w)p_s^n Δ_s.

Then **if d_0<0 and d_1>0, d_n>0 for every integer n≥1**, regardless of weights/propensity values. Proof: let U=wΔ_f, V=(1−w)Δ_s, so d_0=U+V and d_1=p_f U+p_s V. This yields

    U=(d_1−p_s d_0)/(p_f−p_s)>0,
    V=d_0−U<0.

For n≥1,

    d_n=p_s^(n−1) d_1 + p_f U (p_f^(n−1)−p_s^(n−1))>0,

with the n=1 / p_s=0 values interpreted directly. Notice **no full recovery** of p_f,p_s,w,Δ_f,Δ_s is needed; a full 75-stage yield can remain exponentially rare. The output is a conditional ordering, not its rare probability, and this result is a concrete instance of established single-crossing / variation-diminishing machinery.

### Data and finite sampling certificate

At p_f=.7, p_s=.05, w=.5, a=(.8,.065), b=(.72,.22):

    a0=.4325; b0=.47; a1=.281625; b1=.2575
    d0=−.0375; d1=.024125.

At L=75, true Y_A=1.3782085898611701e−12 and Y_B=1.240387730875053e−12, ratio 1.1111111111. A naive iid fit from one-stage marginal prefers B; the acquired two-stage correlation shows A benefits a fast persistent subpopulation. With n=20,000 independent fresh specimens per assay type, a seeded binomial experiment yields 99% *simultaneous* Clopper–Pearson intervals (Bonferroni δ/4 per assay):

    d0 in [−.06189481843550665, −.019279003876793877]
    d1 in [.009049870860578069, .04723195522641943].

Thus a 99%-confidence **all-length** sign certificate holds **conditional on two-mode physical law**. Total 80,000 fresh specimens and at most 120,000 stage attempts (some terminate early); stage execution time, preparation, and readout overhead are not given by the synthetic model. Source data are aggregate synthetic binomial sufficient counts, **not** physical observations.

### Stronger monotone-effect theorem without a finite-rank promise

Let arbitrary latent distribution ν have P∈[0,1], and let conditional action contrast Δ(P)=a(P)−b(P) be nondecreasing in P. If E[PΔ(P)]>0 and E[P]>0, then **E[P^n Δ(P)]>0 for every n≥1**, regardless of the number of hidden modes. Proof: tilt ν_n(dp)=p^nν(dp)/m_n, m_n=E[P^n]>0. The distribution ν_{n+1} is ν_n reweighted by increasing p; because Δ is nondecreasing, Cov_{ν_n}(P,Δ)≥0. Hence E_{ν_{n+1}}Δ≥E_{ν_n}Δ, starting with E_{ν_1}Δ=d1/m1>0. This is a total-positivity / monotone-likelihood-ratio principle. The monotonicity premise itself is **not** acquired from the four aggregated tests; it needs independent physical justification, e.g. a mechanism-specific action-response law or contextual assays. The two-mode sign theorem *infers* the relevant monotone two-point contrast from the two observed signs, so does not assume it separately in its two-mode scope.

### Integrated continuous-time implementation: the bridge is actually exercised

`composed_ctmc_trials.py` builds one 300-transient-state **continuous-time Markov reaction model**, rather than treating the independent stages as a black-box Bernoulli simulator. There are 75 stages, two persistent unobserved modes, and at each stage a boundary state and a reversible hidden trap state. Every boundary has competing forward progression, hidden-trap entry and independently running degradation (µ=.3); traps return or degrade. On progression, the mode is retained and the trap is left behind. The exact one-stage killed-excursion reduction gives conditional survival p_z^action = r_z^action/[r_z^action+µ+t_z µ/(γ_z+µ)]. Set trap-entry t=(.8,1.1), trap-return γ=(.7,.2), and choose *physical forward reaction rates* r_z^action by inverting this equation for baseline p=(.7,.05), A=(.8,.065), B=(.72,.22). Thus the earlier phase's **discounted first-excursion transfer supplies the physical short-stage probabilities used in the memory theorem**; no mismatch between stopped-clock and discrete-stage interfaces remains in this declared CTMC.

With a fresh unobserved mode drawn for each specimen, the executable script runs Gillespie *physical reaction clocks*, not just analytical binomial counts, on the four permitted assays. M=40,000 fresh specimens for each assay (160,000 total), at most 240,000 stage attempts, 338,144.323 model time units of actual simulated reaction duration, and 377,972 individual CTMC reaction events. The four exact 99% simultaneous Clopper–Pearson intervals yield

    d0 ∈ [−.043306196636060335, −.013184704204972364],
    d1 ∈ [ .007366040667104168,  .03422725327899245].

The task-only decision **A preferred to B for every L≥2** is statistically certified under the declared two-mode/unchanged-physics law. Independently, a *strong conventional explicit 300-state sparse killed-generator solve* produces Y_A=1.3782085898612028e−12 and Y_B=1.2403877308750822e−12 at L=75, agreeing with the acquired-excursion/latent-mode formula. This is a working composite synthetic mechanism and a **full-information oracle numerical validation**, **not** an equal-data prediction advantage over a conventional CTMC solver. The solver is deliberately given the exact hidden generator, which the short-assay learner is not. The proper equal-data incumbent is an ordinary confidence-interval comparison of the same four short Bernoulli assay outcomes, coupled to the same structural two-mode or monotonicity theorem; it can produce the same task-only certificate once that theorem is known. It is also not an experimental qualification of the exact two-mode assumption in nature. Per-specimen preparation/reset, physical actuation changes, and monitoring calibration are omitted from the simulated reaction-time total and would have to be charged in a real implementation.

## 6. Exact counterexample: even infinite short data cannot replace the structural interface

Let three latent propensities p=(1/10,1/2,9/10), each weight 1/3. B has conditional action success vector (9/10,3/20,1/2). Consider TWO physically distinct laws for A:

    Law minus: A=(1/10,17/20,2/5)
    Law plus : A=(3/10,9/20,3/5)

Both laws yield **exactly the same** observable values:

    (a0,a1,b0,b1)=(9/20,53/200,31/60,41/200),
    d0=−1/15 and d1=3/50.

At L=75, Y_A−Y_B is approximately −1.370327722e−5 in law minus and +1.370327722e−5 in law plus. Differences in A are (1/5,-2/5,1/5), a null direction of the 0th and 1st moment maps for p=(.1,.5,.9). This is an **exact rational nonidentifiability** result: repeated observations of these four assays cannot resolve the long decision without a structural promise.

In general, with k+2 distinct latent p values and positive weights, the first k+1 mixed action moments E[P^j a(P)] (0≤j≤k) have a nonzero weighted Vandermonde null direction. At any n>k the high moment can vary along that direction (the extended Vandermonde is linearly independent). Small admissible perturbations yield two action laws with exactly matching supplied short moments but distinct long outputs; selecting an action B at the midpoint can make their preferences opposite. This is a classical truncated-moment information obstruction, here applied to program-length intervention decisions.

### Rare contaminant falsifier

Even an ε=10^−9 third mode with p=.99 and a=.4,b=.5 changes every short Bernoulli assay probability by at most 10^−9 compared to the clean two-mode system, but at L=75 flips the action preference. Exact rational calculation gives contaminated Y_A≈1.915142254e−10 versus Y_B≈2.389104087e−10, whereas the clean two-mode system favors A. Eighty thousand short observations cannot plausibly qualify absence of this latent population. The **support/model-class guarantee**, not just estimator design, is the hardest unpaid obligation.

### Exact flat-Hankel rank bridge, and why it is insufficient with finite noise

The baseline moments m_j=E[P^j], j=0..4, form positive-semidefinite H2=(m_{i+j})_{i,j=0..2}. If exact H2 has rank exactly two, a nonzero quadratic q in its nullspace satisfies E[q(P)^2]=0, so the latent support lies at q's at most two roots. Thus exact fourth-order moments could *logically* establish a two-point mixture without supplying its atoms. Exact rational fixtures: clean two-mode det(H2)=0, tested three-mode det(H2)=256/421875>0. But **finite noisy tests cannot certify exact zero determinant** or rule out a 10^−9 contaminant. A small measured quadratic residual can give finite-horizon approximate bounds, yet not a free all-horizon sign theorem.

## 7. Strongest ordinary, equally informed alternatives

1. **Full-state CTMC/exact milestoning**: if the true microstates or exact boundary kernel are acquired, ordinary Schur complement, first-passage linear algebra, or exact milestoning computes the killed success probability. Our first 40-stage test *ties* the O(N) conventional recurrence **with equal acquired H data**. The integrated 300-state solve gets the hidden true generator as a separate *stronger-information oracle correctness check*, not an equal-data benchmark. No new computational superiority is claimed.
2. **Spectral HMM / observable operators / Prony**: standard full-model moment identification reconstructs a two-mode latent mixture from baseline m0...m3 (nondegenerate determinant) and action mixed moments. `latent_memory.py` implements this. At 200k, 1m, 5m and 20m per assay type, recovering tiny long-yield intervals is severely ill-conditioned; the recorded conservative intervals still overlap and do not certify the action ordering in the tested setup. The task-only sign test asks a weaker, meaningful question and can succeed with 20k per short assay. A conventional task-focused confidence-interval test of the *same four data* plus the same two-mode monotone-weighting theorem ties exactly; full spectral estimation is an unnecessary stronger output and can be poorly conditioned.
3. **Nonparametric truncated-moment robust optimization**: optimize the unknown measure/response over all models consistent with four observed probabilities and statistical intervals. This valid conventional baseline cannot choose between the exact three-mode observational aliases. It may beat a simple polynomial bound when additional moments are available and must not be treated as a weak strawman.
4. **Direct complete-run Monte Carlo**: for 10^-12 success, this demands approximately 10^12 independent runs per expected success, but it is not the strong incumbent. Local kinetics, rare-event importance sampling, and verified models are the fair comparators.

## 8. Computational/physical/precision accounting

- Assays: 800,000 gateway trials for the first compiler, 80,000 fresh specimens for the abstract task-only sign test or 160,000 for the integrated CTMC short-assay test. The abstract sign test has at most 120,000 stage attempts. The integrated CTMC uses at most 240,000 stage attempts and measures 338,144.323 model time units, plus unknown real specimen preparation, reset, and calibration.
- Exact synthetic arithmetic for alias/contamination: Python `fractions.Fraction`. Statistical intervals: Clopper–Pearson formula with SciPy beta quantiles; double-precision numeric endpoints, not formal interval arithmetic. Linear inverse uses floating-point SciPy solves. Fixed-seed randomized tests are diagnostics, not proofs.
- All-length sign certificate: confidence is simultaneous for four fixed Bernoulli expectation parameters on a preset assay family; the extrapolation to every future sequence length follows from the supplied two-mode theorem, not new observations at each length. It provides an ordering, **not** an accurate success probability or physical yield/cost improvement.
- Target-specific grammar: baseline stage, alternatives A/B, exact two-mode promise or monotone action-response shape, and stable independence are necessary physical hypothesis. They are not learned automatically from finite generic observations. Runtime to compute sign is constant once data exist; exact physics execution cost remains separate.
- No claim of a device, working wet lab, biological proof, universal efficient rare-event solver, or new historical mathematical priority.

## 9. Reproduction

Run in a Python environment with NumPy and SciPy:

```bash
python test_compiler.py
python latent_memory.py
python task_only_decision.py
python composed_ctmc_trials.py
python three_mode_falsifier.py
python identical_shorts_counterexample.py
python hankel_and_contamination.py
python theorem_stress.py
```

The scripts write matching JSON result files and assertions. Seeded result files are distributed alongside the code. `theorem_stress.py` tests 300,000 two-mode random models and 150,000 monotone-effect mixtures at seven horizons; it has zero observed violations, but these checks do not replace analytic proofs. All outputs are synthetic.

## 10. Scientific status and the next real gate

**Earned:** (a) a working finite-data killed-excursion compiler and a combined 300-state CTMC/Gillespie realization of the memory-sign transfer, with full-state / classical ties and physical costs visible; (b) task-only long-sequence sign prediction under two stable latent modes or known monotonicity, with finite 99% short-assay evidence; (c) an exact indistinguishability barrier under three latent modes and a one-in-a-billion latent contaminant that can reverse the decision; (d) a precise acquisition target: demonstrate sufficient *physical* rank/response structure and perturbation robustness on a real, costly multi-stage process.

**Not earned:** an actual verified physical two-mode mechanism, elimination of hidden catastrophe paths, robust finite-sample detection of exact rank, a better-than-strong-conventional comparison on a real process, or a civilisation-changing end-to-end scientific capability. For a credible breakthrough the next step is not a better synthetic score; it is a physically grounded process where short interventions can establish a sufficiently complete predictive state and bound the effect of unseen, high-propensity, low-abundance modes. If this cannot be earned, the theorem is a useful conditional tool but not the sought foundation.
