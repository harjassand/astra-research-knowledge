# ASTRA FRONTIER — Completion-directed gate probing

**Research checkpoint: 14 October 2026**

## Status

The retained objective is consequential long-timescale molecular kinetics without waiting for rare transitions or supplying the important gate configurations. This checkpoint replaces transport-map acquisition by a model-completion acquisition problem.

The candidate mathematical result is an endpoint principle for exact one-edge interrogation: for an edgewise conductance uncertainty box, the worst remaining additive or multiplicative mean-lifetime uncertainty after measuring one edge is attained when the measured conductance equals one of its interval endpoints. This yields a closed-form, one-step minimax query rule. The rule is derived below and checked on finite rational systems. Historical novelty and external proof review are unresolved.

A working implementation selects microscopic rate queries, without a transport map, committor or trajectories, and then validates its kinetic interval with exact rational arithmetic. The benchmark is a relabelled softened East model, an established kinetically constrained microscopic model. It is not a calibrated molecular model or an atomistic energy/force benchmark. Its factorized equilibrium masses are known analytically. All microscopic states and possible single-spin moves are explicitly represented and charged.

The strongest fully acquired sparse solver and a structure-aware rule learner beat the candidate on the tested finite models. No optimized-WE, AIMMD, TAMMBER or atomistic head-to-head run was executed. There is no demonstrated scientific speed advantage or civilisation-changing capability.

What has changed from the previous checkpoint: the new procedure actually chooses what information to acquire and certifies the relevance of information it did not acquire. It does not assume a useful transport map. The unresolved cost is now global model coverage and compressed computation, rather than only map fitting.

## 1. Competing mechanisms examined

### 1.1 Multichart or branching currents alone

For a finite reversible network with source m, every feasible current J obeys divergence J=m. For a set S containing no absorbing vertex, conservation and Cauchy–Schwarz imply

    Energy(J) >= [sum_{i in S} m_i]^2 / [sum_{e crossing S} c_e].

Thus changing charts cannot by itself establish the unknown conductance across a gate cut. Branching can reduce representational distortion, but an unmeasured cut may still dominate the current cost. This observation does not prove that multichart discovery is impossible; it shows that it needs a coverage/acquisition mechanism rather than only a more expressive current parameterization.

### 1.2 Short-time or spectroscopic extrapolation

Consider survival laws

    S0(t)=exp(-t),
    S1(t)=(1-p)exp(-t)+p exp(-t/T).

Their absolute difference is at most p for every t>=0, whereas their means are 1 and 1-p+pT. For p=10^-6 and T=10^12, an absolute survival error tolerance 10^-6 cannot distinguish a mean near one from a mean near one million. This is an elementary explicit model of an unobserved slow component, not a universal lower bound for every experiment. Spectroscopy or short trajectories require an additional tail/observability guarantee to certify the mean.

### 1.3 Completion-directed local interrogation

Maintain every unqueried microscopic transition as uncertain, not absent. Compute the fastest and slowest admissible aggregate kinetics. Select a local rate query by its guaranteed reduction in this interval. Terminate only when all admissible unresolved pathways have collectively become irrelevant at the requested accuracy.

This is the mechanism developed and implemented below.

## 2. Exact model and information interface

There are N transient microscopic states, a grounded absorbing target, a known possible-move set E, and positive known unnormalized invariant masses m_i. Let d_e be the grounded incidence vector of edge e, and let its reversible conductance be c_e, so k_ij=c_ij/m_i. Set

    A(c)=sum_e c_e d_e d_e^T,
    M=sum_i m_i,
    F(c)=m^T A(c)^(-1)m,
    tau(c)=F(c)/M.

The initial law is m/M on the entire specified transient domain. This is the same equilibrium-conditioned mean-lifetime objective as the earlier current construction. It is not an arbitrary prepared-source MFPT or automatically an experimental dissociation constant.

The data provide intervals ell_e <= c_e <= u_e. We require A(ell) positive definite. Individual lower bounds may be zero if the known-positive subgraph still connects every transient component to the target. Otherwise the pessimistic mean can be infinite and a separate connectivity/coverage search is necessary. That search is not supplied free.

The prototype's rate oracle answers one selected microscopic transition query. In the softened East model this is an evaluation of the microscopic generator, not a rare-event rate estimated from a trajectory. For a real molecule, an oracle returning rates between already identified metastable basins could hide the original gate-discovery problem. No such atomistic oracle has been constructed here.

The possible-move set is a microscopic alphabet, not a list of important gate pathways. Nevertheless, representing it over every conformation can be exponentially expensive.

## 3. Sharp kinetic completion interval

Let

    F_hi = F(ell),  F_lo = F(u).

Since A(ell) <= A(c) <= A(u) in positive-semidefinite order,

    F_lo/M <= tau(c) <= F_hi/M.                         (3.1)

Both endpoints are admissible within the independent edgewise uncertainty class, so the interval is information-theoretically sharp for that class and the current transcript. No other method using exactly this transcript and no stronger structural assumptions can guarantee a smaller interval.

When the uncertainty box over-approximates a correlated model family, (3.1) remains valid, but it need not be sharp for that smaller family. This distinction is important in the East-model experiment: known one-parent structure can enable a much stronger specialized learner.

There is no path truncation in (3.1). All trajectories and revisits in every admissible completed network are included by the grounded inverse. This avoids pathway enumeration, not microscopic-state enumeration.

## 4. Endpoint theorem for acquisition

Fix an unresolved edge e. Write

    Delta = u_e-ell_e,
    v_- = d_e^T A(ell)^(-1)m,       R_- = d_e^T A(ell)^(-1)d_e,
    v_+ = d_e^T A(u)^(-1)m,         R_+ = d_e^T A(u)^(-1)d_e.

Define the reductions associated with the two possible endpoint answers:

    G_high = Delta v_-^2 / (1+Delta R_-),
    G_low  = Delta v_+^2 / (1-Delta R_+).                (4.1)

The second denominator is positive: A(u)-Delta d_e d_e^T >= A(ell)>0.

If the query returns u_e, the new interval for F is

    [F_lo, F_hi-G_high].

If it returns ell_e, the new interval is

    [F_lo+G_low, F_hi].

### Theorem: no interior query answer is worse

For every exact answer t in [ell_e,u_e], the remaining interval width is at most the larger width at these two endpoint answers. The same is true of the upper/lower ratio.

Consequently, the exact worst-case remaining ratio after querying e is

    Q_e = max{ F_hi/(F_lo+G_low), (F_hi-G_high)/F_lo }.   (4.2)

Among equal-cost single-edge queries, selecting an edge minimizing Q_e is exactly one-step minimax for multiplicative kinetic uncertainty. For additive uncertainty, the guaranteed reduction is

    min{G_low,G_high}.                                 (4.3)

The theorem does not establish a globally optimal multi-query policy. It does not make source masses uncertain, permit arbitrary changes in the initial law, or treat a joint physical parameter changing several edges as a rank-one query.

### Proof of the endpoint theorem

At t=ell_e, define

    B_-=A(ell),
    B_+=A(u)-Delta d_e d_e^T.

Then B_+>=B_->0. With p=t-ell_e, both post-query extremal matrices have the same rank-one update p d_e d_e^T. Let

    f(p)=m^T(B_-+p dd^T)^(-1)m,
    g(p)=m^T(B_++p dd^T)^(-1)m.

By the Sherman–Morrison identity,

    f(p)=f(0)-p a^2/(1+p r),
    g(p)=g(0)-p b^2/(1+p s),

where a=d^T B_-^(-1)m, b=d^T B_+^(-1)m, r=d^T B_-^(-1)d, s=d^T B_+^(-1)d. Positive-semidefinite order implies r>=s>0 for a nonzero edge vector.

For any lambda>=0,

    d/dp [f(p)-lambda g(p)]
      = -a^2/(1+p r)^2 + lambda b^2/(1+p s)^2.

Because (1+p r)/(1+p s) is nondecreasing, this derivative can change sign only from negative to positive, not from positive to negative. The zero-coefficient cases are monotone or constant. Therefore f-lambda g has no strict interior maximum and is bounded above by its endpoint maximum.

Taking lambda=1 establishes the additive-width statement. Taking lambda=max{f(0)/g(0),f(Delta)/g(Delta)} makes the two endpoint values of f-lambda g nonpositive, so they are nonpositive throughout the interval. This proves the ratio statement. Substituting the rank-one identities gives (4.1)–(4.3).

### Fixed batches

For a preselected batch of distinct edges, the worst remaining ratio occurs at one of the 2^k endpoint combinations of the measured edges: push one coordinate at a time to an endpoint using the theorem. This is an exact finite reduction, not an efficient arbitrary-batch algorithm. It does not prove that a general adaptive multi-step minimax policy only needs endpoint outcomes, because minimization over future query choices can destroy the requisite shape property.

### What is and is not new

Rayleigh monotonicity, grounded network representations, resolvent identities, matrix inversion updates and uncertainty-directed kinetic exploration are established ingredients. The proposed result for priority investigation is the endpoint principle and its exact one-step minimax kinetic acquisition rule, together with transcript-based completion certification. No exhaustive historical novelty clearance or external proof audit has been completed.

## 5. Actual discovery algorithm and costs

1. Initialize all unqueried edge intervals and both extremal grounded inverses.
2. Calculate v_-,v_+,R_-,R_+ for candidate edges.
3. Choose a query using (4.2), acquire its rate, and make its two interval endpoints coincide.
4. Update both inverses by rank-one formulas and periodically rebuild them.
5. Stop when the candidate completion ratio is at most 1.1, then independently validate the endpoints exactly. Report failure instead of a certificate if the validation fails.

The implementation uses floating-point arithmetic to choose queries. It does not certify every argmin comparison, so the mathematical one-step optimality theorem is not a claim that every floating-point query selection was exactly optimal. The final kinetic interval is checked independently with rational arithmetic.

For N explicitly represented states, E possible edges, Q queries and an inverse refresh every r queries, the implemented dense version uses approximately

    O(N^3(1+Q/r) + Q(N^2+E)) arithmetic operations,
    O(N^2+E) memory,

in addition to rate acquisition, mass construction and exact endpoint validation. There is no explicit simulated-waiting-time factor in this expression. There is an exponential configuration-space factor when N grows as 2^n. Approximate effective-resistance algorithms might reduce overhead, but no such backend was implemented or certified.

The oracle can return exact rational endpoints in the model test. In a physical experiment, finite measurement uncertainty must remain as an interval. Measuring an exponentially small rate to fixed relative accuracy by observing transitions need not be cheap. A query theorem does not eliminate that acquisition cost.

## 6. Numerical certification without a spectral gap

Let K=-Q be an exact killed Markov generator and v a positive trial MFPT field obtained numerically. Recompute its residual using exact rational arithmetic and establish

    (1-delta)1 <= K v <= (1+delta)1,    delta<1.

Inverse positivity of K gives

    v/(1+delta) <= K^(-1)1 <= v/(1-delta).

Average against the exact initial mass distribution to enclose the mean. This verification requires all entries of each extremal model, including the supplied endpoints of unqueried rates; it does not query their true values.

Every floating entry of v is converted to its exact IEEE-754 rational value. The benchmark probabilities q and softness epsilon are interpreted as exact decimal rationals. Residuals and source averages are computed with Python Fraction arithmetic, and displayed decimal bounds are rounded outward. Thus the finite-model enclosure is not a Monte Carlo confidence interval or a floating-point point estimate passed off as a certificate.

Several low-temperature solves emitted ill-conditioning warnings. They are retained in the logs. The reported final enclosures pass the independent exact residual check; the warnings still caution against interpreting the floating acquisition ordering as exact.

## 7. Independently specified gated benchmark

The softened East model is a published kinetically constrained model [1]. Here it has L=10 binary variables n_i, an open facilitating left boundary and an absorbing event n_L=1. Before absorption n_L=0, leaving N=2^9=512 transient configurations and

    E=9*2^8+2^9=2816

possible undirected internal/grounded moves.

The physical generator is

    k_i(0->1 | n)=q a_i(n),
    k_i(1->0 | n)=(1-q) a_i(n),
    a_1=1,
    a_i=epsilon+(1-epsilon)n_{i-1} for i>1.

This is a rescaled standard soft-East parameterization. The energy gives a product Bernoulli(q) equilibrium law. The initial law is that equilibrium law conditioned on n_L=0. Its masses are computed analytically, not sampled.

The non-target coordinates are relabelled using a fixed seed before acquisition. The candidate sees the state labels, possible single-bit moves, q, epsilon, masses and per-edge intervals; it does not receive the facilitating-parent ordering. The final experiment passes a public dictionary without the private gate ordering or true-rate array, plus an explicit rate-query callback. The callback computes the selected rate on demand. The verifier uses only the returned query transcript and the supplied prior bounds.

Thermodynamics factorizes; the kinetics does not. This isolates hierarchical kinetic-gate discovery but makes equilibrium-mass acquisition much easier than in a real molecule. The full-state representation also makes these models easy for a specialized sparse solver once all rates are available.

### Canonical results

See final_results.json and final_run.log for exact query transcripts, residual bounds, timing and validation. Four parameter settings were tested with the same 512-state size. The exact one-step multiplicative criterion was used; the requested final upper/lower ratio was 1.1.

| q | epsilon | Reference mean, approximately | Queried rates | Certified lower | Certified upper |
|---:|---:|---:|---:|---:|---:|
| 0.05 | 10^-6 | 88,348.7312 | 1,476 | 82,120.607428069 | 90,234.170660260 |
| 0.02 | 10^-8 | 3,618,407.8275 | 1,397 | 3,340,321.3850920 | 3,660,673.8097263 |
| 0.01 | 10^-10 | 58,669,247.5730 | 1,271 | 53,925,484.933710 | 59,286,281.228498 |
| 0.005 | 10^-12 | 943,912,475.6149 | 952 | 872,910,896.94266 | 956,911,477.13432 |

Times are in the model's microscopic time unit, not seconds for a real material or molecule. The exact reference intervals are also stored, and become wider at low temperature owing to numerical residuals; the final reference remains much tighter than the acquisition interval.

In the coldest setting, the final ratio is at most 1.0962304176588. The geometric midpoint has a worst-case multiplicative error below sqrt(1.0962304176588)-1, approximately 4.71%. No trajectories were simulated. 1,864 of 2,816 true microscopic rates, about 66.2%, were never queried. Their collective possible effect is covered by the completion interval.

Relabelling seeds 1,23 and 45 required 962,953 and 960 queries respectively, versus 952 for the primary seed. These are robustness checks on labels, not new independent physical models. q and epsilon co-vary in the table; this is not a two-axis asymptotic scaling experiment or proof of barrier-independent complexity.

### Total resource comparison

For the coldest primary-seed model:

- Completion-directed multiplicative policy: 952 queries; about 1.22 s including acquisition and exact validation.
- Full acquisition and sparse solve: 2,816 queries; about 0.028 s including acquisition and exact validation.
- Random query order with the same completion certificate: 2,796 queries; about 3.47 s.
- Structure-aware single-parent learner and sparse solve: 37 queries; about 0.028 s, conditional on its stronger structural premise.

These are single-process, single-run container timings with OPENBLAS_NUM_THREADS=1, not a statistically controlled hardware benchmark. Common microscopic state/edge construction is separately recorded. Development, literature search and exploratory executions are not included in per-run timings; no end-to-end research-compute advantage is claimed. The full solver is the decisive exact comparator at this size and wins wall-clock time.

The simple optimistic acquisition heuristic used fewer queries than the minimax policy in several warmer settings; the minimax policy used fewer in the coldest setting. One-step worst-case optimality is not optimal average-case or total-query performance.

Given these particular timings, a constant added rate-query cost around 0.64 ms would offset the coldest candidate's extra arithmetic relative to full independent-edge acquisition. This is only a break-even calculation in the stated oracle interface. It is not an atomistic speedup claim and does not beat the structure-aware learner where that learner's premise holds.

## 8. A hidden-gate falsification of sparse rule learning

As a strong specialized comparator, assume each flip is either constantly facilitated or depends monotonically on one unknown non-target bit. An all-zero probe detects the constant rule; binary group probes identify the parent. At most L[1+ceil(log2(L-1))] probes suffice, and the actual implementation uses 37. The parent relation is learned, not supplied. Once learned, all rates can be generated and the sparse kinetic equation solved.

This comparator defeats the new general-box procedure on the genuine soft-East class. However, its certificate is conditional on the one-parent premise, not evidence that the premise is true everywhere.

For a separate adversarial falsification experiment, change one unqueried microscopic flip: at configuration x=8, set the target-flip facilitation to one instead of epsilon. All 37 sparse-rule queries and their answers remain identical. This test was deliberately selected after inspecting the learner and the full model; it is NOT an independent performance benchmark.

At q=0.005 and epsilon=10^-12, the certified true mean changes from

    [943,910,545.91717, 943,914,405.32057]

to

    [78,913.166407819, 78,913.167817368].

The ratio is provably greater than 11,961.38. The perturbation preserves detailed balance and the equilibrium masses; only one symmetric microscopic conductance changes. It creates a bypass that the sparse representation does not contain.

The broader completion-directed procedure queried that edge and produced

    [78,106.473943106, 85,912.735819174]

using 890 local rate queries, with a ratio below 1.1. At the warmer setting q=0.05, epsilon=10^-6, the analogous sparse-rule failure is a factor greater than 87.43; the robust audit also found it.

This demonstrates an important distinction: accurately learning a presumed local rule is not the same as ruling out a consequential off-model pathway. The completion certificate addresses the latter within its declared microscopic move set and global bounds.

## 9. Why the source law cannot be silently changed

For an arbitrary initial distribution rho, the mean is rho^T A(c)^(-1)m, not the quadratic form m^T A(c)^(-1)m/M. The monotonic completion endpoints need not apply.

Example: two transient states with masses one, sink conductances 1 and epsilon, and internal conductance t. Starting at the first state,

    u_1(t)=(epsilon+2t)/(epsilon+(1+epsilon)t).

For 0<epsilon<1, this increases with t: opening a connection to the slow state can lengthen the mean. The equilibrium-conditioned quadratic mean instead has Rayleigh monotonicity. Any transfer to binding-induced or other prepared initial ensembles must explicitly handle this difference.

## 10. Exact information needed to compress a hidden region

Partition the microscopic variables into represented boundary/exterior O and hidden interior H. Write the grounded A in blocks. Exact elimination gives

    K = A_OO - A_OH A_HH^(-1) A_HO,
    b = m_O - A_OH A_HH^(-1) m_H,
    gamma = m_H^T A_HH^(-1)m_H,

and

    F = gamma + b^T K^(-1)b.                            (10.1)

This is the standard Schur-complement identity, not a new claimed theorem. Its significance here is that a hidden-region representation must retain a source load and an internal residence term, not just a boundary conductance map. Total mass is also needed for normalization.

For a boundary state of mass one with a unit sink conductance, attach a dead-end state of mass delta through conductance delta*epsilon. Eliminating the hidden state gives

    K=1, b=1+delta, gamma=delta/epsilon,
    tau=1+delta+delta/[(1+delta)epsilon].

The reduced homogeneous boundary conductance does not reveal the arbitrarily large hidden residence contribution. A source-blind boundary compression can therefore miss a gate that dominates the equilibrium-conditioned mean.

A prospective compressed completion method must bound the full affine-quadratic hidden-region response, including gamma. It must acquire these bounds from local information without already solving the hidden-region kinetics. That is a precise remaining obstruction, not an available oracle.

## 11. Coverage lower bound for an unrestricted local oracle

Consider one transient state with N possible parallel absorbing channels. Each rate is in [a,b]. Compare a baseline in which every channel has rate a with alternatives having one unknown channel of rate b. Their mean lifetimes are

    tau0=1/(Na),
    tau1=1/[(N-1)a+b].

Before the exceptional channel is queried, its transcript is identical to the baseline. Choosing b sufficiently large makes the desired approximation intervals disjoint. A deterministic guaranteed procedure must query all N possibilities in the worst case. With the exceptional location uniformly random, Q local queries distinguish the alternatives with total-variation advantage at most Q/N; achieving error at most delta on both alternatives requires Q>=N(1-2delta).

This is a restricted black-box coverage lower bound, not a no-go theorem for molecular science. A known sparse interaction law, regularity theorem, symmetry or certified geometric cover can constrain many channels from one observation. But such structure must actually be established or be an explicit input premise. Smooth local force samples without a global coverage/regularity argument do not automatically provide it.

## 12. Comparator and prior-art assessment

- Optimized weighted ensemble already uses estimated local MFPTs and their conditional variance to improve trajectory allocation [2]. The new method's potential distinction is deterministic completion coverage and interrogation of unvisited microscopic transitions, not merely discovering a good reaction coordinate. No optimized-WE implementation was run here.
- Descriptor-free AIMMD combines learned committors and path sampling, with a recent preprint reporting protein–ligand kinetic applications [3]. Its abstract was retrieved; full HTML access failed. No benchmark comparison to it was executed.
- TAMMBER already optimizes kinetic-model exploration and uses Bayesian estimates of missing transition rates [4]. Uncertainty-directed acquisition is therefore not new by itself. The endpoint minimax criterion differs in assuming a finite microscopic move set and deterministic conductance envelopes; it does not replace TAMMBER's atomistic discovery machinery.
- Temperature-accelerated dynamics has a mathematical theory using quasistationary distributions and idealized assumptions [5]. It is a serious route to gate acquisition, not a comparator that must wait at the target temperature.
- Graph transformation already calculates finite-network first-passage quantities without simulating paths once the necessary network information is supplied [6,7]. The present fully acquired sparse solve demonstrates that the small explicit benchmark is not beyond specialized existing computation.
- First-principles adaptive kinetic Monte Carlo already discovers transitions using saddle searches and transition-state approximations [8]. The prototype does not obtain those atomistic inputs.

## 13. Exact checks and reproducibility status

The final exact_checks.py run passed 5,740 rational assertions on 32 finite networks, including the rank-one identities, denominator positivity, additive and multiplicative endpoint bounds at rational interior answers, and 256 sampled rational network completions. These finite checks supplement the mathematical proof; they do not substitute for it or constitute external review.

A final replay reconstructed all 15 canonical completion intervals across seven settings from public inputs and recorded query answers alone; every exactly verified upper/lower ratio remained at most 1.1. This was a same-session verifier replay, not external review. Results are in audit_results.json.

Canonical finite-model results are in final_results.json. The final rate-acquisition driver excludes private rate arrays and gate orderings from the learner and records every queried rate. Endpoint certification uses exact rational residuals and outward-rounded decimals. Full code, warnings, exploratory outputs and falsification results are preserved. The first long final-experiment shell invocation was interrupted after several settings; unfinished settings were rerun synchronously and the completed canonical JSON contains all seven settings. Duplicate partial timing lines in final_run.log reflect that interruption, not independent repeated benchmarks.

No external reviewers, formal proof assistant, experimental molecule, high-dimensional atomistic integral, quantum computation, physical intervention, or energy-consumption benchmark was used.

## 14. Retained objective and decisive continuation

The retained scientific objective is still reliable molecular residence/reaction-time prediction with unknown gates, not a smaller matrix-query theorem.

The next missing operation is a compact, physically justified outer description of all kinetic models consistent with acquired atomistic evidence. It must retain source-aware hidden-region residence contributions and permit decision-directed refinement without expanding every microscopic conformation. A proposed representation should face the off-model shortcut test above and the dead-end residence-term test, not only held-out trajectory prediction.

The current endpoint principle supplies an exact acquisition rule once such coverage exists. It does not acquire that coverage from unrestricted atomistic energy/force access. That distinction is the main unresolved barrier.

## Primary sources and access ledger

[1] Y. S. Elmatad and R. L. Jack, *Space-time phase transitions in the East model with a softened kinetic constraint*, arXiv:1210.1614 (2012). Full HTML accessed: https://arxiv.org/html/1210.1614v1 . The benchmark uses an open-boundary, globally time-rescaled parameterization.

[2] W. H. Ryu et al., *Reducing Weighted Ensemble Variance With Optimal Trajectory Management*, arXiv:2504.21663v3, 9 February 2026. Full HTML accessed: https://arxiv.org/html/2504.21663v3 .

[3] S. M. Lichtinger and R. Covino, *Accelerated descriptor-free path sampling for protein-ligand binding kinetics*, arXiv:2607.15101, 16 July 2026. Search-index abstract accessed; full HTML fetch failed: https://arxiv.org/abs/2607.15101 . Claims were not replicated.

[4] T. D. Swinburne and D. Perez, *Self-optimized construction of transition rate matrices from accelerated atomistic simulations with Bayesian uncertainty quantification*, Physical Review Materials 2, 053802 (2018). Publisher abstract accessed: https://link.aps.org/doi/10.1103/PhysRevMaterials.2.053802 .

[5] D. Aristoff and T. Lelievre, *Mathematical Analysis of Temperature Accelerated Dynamics*, arXiv:1305.6569. Full HTML accessed: https://arxiv.org/html/1305.6569v2 .

[6] S. A. Trygubenko and D. J. Wales, *Graph Transformation Method for Calculating Waiting Times in Markov Chains*, arXiv:cond-mat/0603830 (2006). Abstract accessed: https://arxiv.org/abs/cond-mat/0603830 .

[7] D. J. Sharpe and D. J. Wales, *Graph transformation and shortest paths algorithms for finite Markov chains*, Physical Review E 103, 063306 (2021). Publisher abstract accessed: https://link.aps.org/doi/10.1103/PhysRevE.103.063306 .

[8] Henkelman Group EON documentation, *Adaptive kinetic Monte Carlo*. Official method documentation accessed: https://henkelmangroup.github.io/eon/akmc.html .

Inherited project source: the conversation's uploaded RESEARCH_NOTE.md and cumulative-mass transport checkpoint. No result from either optional GitHub repository is a load-bearing mathematical premise of this continuation.
