# From one running experiment to certified future inference

## Status and decision

This investigation originated from the consequential task of using experiments on an interacting stochastic system to support many later prediction and intervention decisions. Its strongest concrete candidate is an **experimentally acquired region of certified tractability**: a retained data set and finite uncertainty certificate identify interventions for which digital inference is both fast and quantitatively faithful to the unknown system.

A complete elementary construction is given below. It needs no equilibrium samples, no experimental reset, no supplied global sampler and no exact downstream answer. It is a constructive synthesis of ordinary local model estimation, Dobrushin coupling and Markov-chain perturbation theory. **No new separation, historical novelty or major new organising theory is established.** The strongest ordinary retained-data route obtains exactly the same capability. This is a useful consequence-first target and a scientifically honest negative result for claims of novelty.

The implementation is a finite synthetic consistency check, not a physical experiment and not evidence of practical scaling. Its exact small-state comparator uses the same fitted local probabilities, retaining their statistical uncertainty.

## 1. Task before mathematical framework

The scientist observes a large locally interacting stochastic system. Later, possibly after seeing the original observations, they want to evaluate local activation probabilities, a spatial average, or an intervention response. They want absolute error at most tau, with specified failure probability, repeatedly for different interventions. Typical motivations include interacting binary sensors, cooperative materials and simplified cellular activation models. Applicability to a particular physical system requires validation of the local dynamics and the intervention mechanism; those applications are motivations, not validated demonstrations.

The task is not to return an exact probability, recover an exact microscopic Hamiltonian or distinguish infinitesimally close models. Both candidate and comparator receive the same finite observations, the same local model assumptions and the same tolerance.

The obstruction is twofold:

1. Local parameter estimation does not automatically make global equilibrium inference easy. A well-fitted model may mix slowly, and an intervention may move it into a regime in which a familiar sampler gives unreliable finite-time answers.
2. An approximate local model can have significantly different global behaviour. The downstream task needs a stability calculation, not merely a point estimate or a good fit on the original trajectory.

The desired reusable operation is: **accept a future intervention and query, either return a certified computational budget and error bound or explicitly decline to certify it.** Declining is not a proof of hardness. Nothing in this construction solves all inverse design or arbitrary global optimisation problems.

## 2. Strongest ordinary route, constructed first

Retain all observed local transitions, or their exact sufficient counts. Build simultaneous confidence intervals for the local update probabilities. For a proposed intervention, transform those intervals using the supplied intervention law. Check a classical contraction condition; if it passes, run an ordinary digital Markov chain and propagate the local uncertainty to the final query. If the small system permits it, solve the fitted chain's stationary equations directly. For structured models, an ordinary comparator may also exploit their structure, use exact dynamic programming, cluster methods, block coupling, correlation decay or the strongest applicable learning theorem.

This route already delivers the proposed capability. The finite certificate is an efficient summary of a conventional calculation, not a distinct source of information or power. Retaining the raw observations costs polynomial space and does not hurt the comparator. Exact stationary solution of the fitted chain does not remove uncertainty about the physical chain.

## 3. Fully stated acquisition model

There are n sites, each taking values in {0,1}. Site i has a supplied neighbour set N(i), of size d_i at most d. Each site has an independent rate-one Poisson clock. When its clock rings, it replaces its state by a fresh Bernoulli draw with unknown probability

    p_i(z),  z in {0,1}^{N(i)}.

Every local probability is in [kappa, 1-kappa] for a supplied kappa > 0. The local rule is time independent. There are no hidden variables or unobserved long-range dependencies in this model. The known topology and clock/readout interface are supplied assumptions, not acquired conclusions.

We observe a single running trajectory from an arbitrary initial state. We log the update identity, the preceding local context and the new value, including attempts that do not change the value. There is no reset and no equilibration period. Finite stochastic sampling is the imperfection treated by the main construction.

An optional narrow sensor-noise extension allows the new-value label to be independently flipped with known probability nu < 1/2 while the context and update identity are correctly observed. Then its conditional mean is nu + (1-2 nu) p_i(z), which can be inverted. This does not address noisy contexts, unknown readout noise, missed clock events or latent state. Treating those extensions as automatic would be invalid.

Let M = sum_i 2^{d_i} <= n 2^d be the number of local contexts. Retain the first m labels for each context. For clean labels, the empirical mean p_hat has a simultaneous confidence radius

    eta = sqrt(log(2 M / delta_stat) / (2m)).

For the optional known label flip channel, divide eta by (1-2 nu) and clip the corrected mean to [0,1]. The intervals are [p_hat-eta,p_hat+eta] intersected with [0,1].

### Why correlated trajectory observations do not invalidate this estimate

The times at which a specified local context is visited depend on the past. At each such time, however, its newly sampled value has conditional Bernoulli law p_i(z), and uses fresh randomness. The first m retained outcomes are therefore a Bernoulli sample with this fixed conditional law (equivalently, use the bounded martingale Hoeffding proof). A union bound covers all M contexts. No claim that whole configurations are independent is needed.

### Explicit acquisition cost without reset or mixing

Fix a site i and context z. In a unit time window require:

- each neighbour of i rings exactly once in the first half and not in the second half;
- i rings exactly once in the second half and not in the first half;
- every neighbour update sets its prescribed value in z.

The Poisson-clock part has probability (exp(-1)/2)^{d_i+1}; the assignments have conditional probability at least kappa^{d_i}, regardless of the past and of outside-site activity. Therefore the window contains an observation of (i,z) with conditional probability at least

    q_i = exp(-(d_i+1)) 2^{-(d_i+1)} kappa^{d_i}.

Set q = exp(-(d+1)) 2^{-(d+1)} kappa^d. Across disjoint windows the success indicators need not be independent, but their conditional success probabilities are bounded below by q. The usual conditional Chernoff argument gives P(S_T < qT/2) <= exp(-qT/8). Consequently

    T >= q^{-1} max(2m, 8 log(M/delta_cover))

unit windows suffice for m observations of every context with probability at least 1-delta_cover. The total number of site-update attempts has expectation nT. This is an explicit, conservative worst-case cost; it is exponential in d and in log(1/kappa) times d. It is not dimension-free experimental preparation.

In practice the algorithm simply records counts and knows when each context has m observations. The bound proves eventual acquisition without assuming the unknown global mixing time. It can be very pessimistic, and better model-aware conventional estimators can improve it.

## 4. The future intervention interface

An intervention u is a supplied, efficiently evaluable transformation of each local probability. The running example is an odds tilt,

    F_r(p) = r p / (1 + (r-1)p),   r > 0,
    q_i^u(z) = F_{r_i^u(z)}(p_i(z)).

Both field changes and specified local interaction changes can be represented this way in an Ising heat-bath model. The transformation is a known causal/physical law in the model, not an empirical consequence of observing only the baseline. If the intervention mechanism is unknown, two systems can have identical baseline trajectories and arbitrarily different intervention responses. Baseline observations alone cannot fix that identifiability problem.

Apply the monotone F_r to each interval endpoint to get lower and upper local probabilities l_i^u(z), h_i^u(z), and to p_hat to get q_hat_i^u(z). This computation is O(M). Define the local error budget

    epsilon_i(u) = max_z max(h_i^u(z)-q_hat_i^u(z),
                             q_hat_i^u(z)-l_i^u(z)).

For neighbours j in N(i), define an upper influence coefficient

    C^+_ij(u) = max_{z,z' differing only at j}
                   max(h_i^u(z)-l_i^u(z'),
                       h_i^u(z')-l_i^u(z), 0).

Other entries are zero. All models in the confidence intervals have their true influence matrices entrywise bounded by C^+. The estimated model does too. Computing this sparse matrix costs O(sum_i d_i 2^{d_i}), not an exponential global-state calculation.

The elementary certificate accepts an intervention when

    max_i sum_j C^+_ij(u) <= 1-gamma(u),   gamma(u) > 0.

It returns gamma, the local error budgets and the matrix. It may reject systems that are easy for other methods. Weighted norms, block dynamics and stronger finite-size conditions belong to the conventional comparator and should be investigated before declaring this test a fundamental boundary.

## 5. What the acquired certificate proves

For f:{0,1}^n->[0,1], define its coordinate oscillation

    osc_i(f) = max_{x,x' differing only at i} |f(x)-f(x')|,
    L(f) = sum_i osc_i(f).

A one-site activation probability has L=1. The mean activation fraction also has L=1. A function of k sites has L<=k. A general global event may have L as large as n. These are task-specific sensitivity quantities, not an accuracy requirement invented to create a separation.

### Theorem (ordinary local data to certified reusable inference)

On the simultaneous experimental confidence event, every intervention accepted by the test, including an intervention chosen after viewing the observations, has all of the following properties:

1. Its true and fitted digital chains have unique stationary laws, denoted mu_u and mu_hat_u.
2. From any initial state, after k random-site digital updates,

       |E f(X_k)-mu_hat_u(f)| <= L(f) exp(-gamma(u) k/n).

   In particular their total-variation mixing bound is n exp(-gamma k/n).

3. Their stationary query discrepancy satisfies

       |mu_u(f)-mu_hat_u(f)|
          <= L(f) ||epsilon(u)||_infinity / gamma(u).

   A sharper computable bound is

       sum_i osc_i(f) [(I-C^+(u))^{-1} epsilon(u)]_i.

4. If B independent digital trajectories are run for k updates and their f-values averaged, then with probability at least 1-delta_query the error relative to the true stationary query is at most

       L ||epsilon||_infinity/gamma
       + L exp(-gamma k/n)
       + sqrt(log(2/delta_query)/(2B)).

The same statement covers any finite or countable adaptively chosen sequence of future queries by assigning summable query failure budgets and using fresh simulation randomness. The data confidence event itself is uniform over all accepted interventions, because it covers the local probability table before the future intervention is chosen.

### Proof

Couple two chains using the same update site and the same uniform random number at every update. If r_i denotes the probability their ith coordinates disagree, the influence telescoping bound yields

    r_i' <= (1-1/n) r_i + (1/n) sum_j C^+_ij r_j.

Hence ||r'||_infinity <= (1-gamma/n)||r||_infinity. Repeating gives the mixing statement after coupling one initial state to an independently stationary initial state. The oscillation telescoping inequality |f(x)-f(y)| <= sum_i osc_i(f) 1{x_i!=y_i} transfers the coupling to f.

For a true chain coupled to the fitted chain, the analogous inequality includes epsilon_i/n. The coupled finite chain has a stationary law, with stationary marginal laws mu and mu_hat, so its disagreement vector satisfies r <= C^+ r + epsilon. Nonnegativity and spectral radius(C^+)<1 imply r <= (I-C^+)^{-1} epsilon. The row-sum bound gives ||r||_infinity <= ||epsilon||_infinity/gamma. This proves perturbation stability. Finally apply Hoeffding to the B independent simulated f-values and add the two biases. Digital restarts initialise an explicitly known finite local simulator; no physical reset is assumed. QED.

### Resource ledger

For fixed degree, positivity, margin and requested precision:

- observations: at most the acquisition time bound above, in expectation nT update attempts;
- retained summary: O(M) counts and interval endpoints, with finite integer/precision bit costs;
- certificate query: O(nd 2^d) elementary operations for the elementary test;
- inference: B=O(tau^{-2} log(1/delta_query)) independent runs, each k=O((n/gamma) log(L/tau)) updates, provided the experimental uncertainty contribution is below the requested error;
- exact fitted-chain route: an explicit 2^n-state stationary calculation, usable at small n but not claimed scalable;
- optional sharper matrix error bound: a sparse linear solve, or a convergent nonnegative Neumann iteration, with its cost and conditioning charged.

If local uncertainty already exceeds the requested final tolerance after amplification, no amount of digital simulation repairs it. More experimental data or a sharper valid structural argument is needed.

## 6. Why this does not establish a novel advantage

The local confidence table and certificate are computable from the original observations. An ordinary algorithm retaining those observations can run exactly the same computation. This emulation preserves the input, tolerance, failure probability and all acquisition costs. There is no information-theoretic, computational or physical separation in the construction.

The organising idea—learn the conditions that make future computations stable—is useful, but its mathematical ingredients are established. Dobrushin and Shlosman already supplied constructive finite-size criteria for an analyticity/mixing regime. Classical influence criteria already yield rapid mixing, including weighted and block variants. Learning local Ising dynamics from a nonstationary trajectory has an extensive literature, including algorithms with weaker observations than used here. Wasserstein perturbation bounds already turn transition error and contraction into distributional stability.

A credible next advance must therefore do more than rename the confidence table. Examples of consequential unresolved targets are:

- acquire useful certificates in a wide physically relevant regime where one-site contraction fails, without solving exponentially large blocks;
- handle partial/noisy observations and unobserved update attempts with full uncertainty and physical acquisition costs;
- learn and validate the intervention law as well as the baseline dynamics;
- establish a cost advantage over the strongest ordinary algorithms using the same observation interface;
- obtain certificates for phase-specific or rare-event computations whose requested error cannot be met by the current Lipschitz bound.

None is proved here. In particular, adding a supplied block sampler, exact phase label or arbitrary conditional sampling routine would hide the unresolved work rather than solve it.

## 7. Focused older Astra reading and its role

Pinned commit: cb87e72296824ae2a677ccd337025d02d20cbb0a. Followed 00_START_HERE.txt and agent/ACCESS.txt; read N540 and N550 packets and their relevant governing source passages. No current work folder or other agent's draft was inspected. No old theorem is imported into the proof above.

- [N550 governing source, section 6 and failure modes](https://github.com/harjassand/astra-research-knowledge/blob/cb87e72296824ae2a677ccd337025d02d20cbb0a/updates/BV/package/astra_static_generator_tomography/RESEARCH_HANDOFF.md): its reported computations distinguish exact synthetic stationary draws and numerical stationary PDE solutions from a charged physical experiment. This motivated the explicit no-reset single-trajectory acquisition argument here. Its comparison also openly reports that one numerical baseline was weaker than the strongest possible competitor.
- [N540 governing source](https://github.com/harjassand/astra-research-knowledge/blob/cb87e72296824ae2a677ccd337025d02d20cbb0a/updates/BS/package/evidence/GAUSSIAN_CONDITIONING_PROOF.txt): the supplied conditional-sampling interface can retain a hard counting problem and require exponentially rare preparation. Its results were treated as source-reported and not independently reverified here. It was used only as a warning against supplying a sampler as an oracle; this construction instead explicitly simulates learned single-site updates.

## 8. Primary literature and scope of use

1. Dobrushin and Shlosman, *Completely Analytical Interactions: Constructive Description* (1987). [Author-hosted paper](https://www.cpt.univ-mrs.fr/~shlosman/papers/132.pdf). The opening statement and constructive finite-volume programme show that finite local checks identifying a globally well-behaved regime are old. No full equivalence theorem from this paper is needed for the elementary proof above.
2. Dyer, Goldberg and Jerrum, *Dobrushin conditions and Systematic Scan* (2005/2006 report). [Primary manuscript record](https://eccc.weizmann.ac.il/report/2005/075/). The influence criteria and rapid-mixing connections are explicit conventional predecessors.
3. Bresler, Gamarnik and Shah, *Learning graphical models from the Glauber dynamics* (2014). [Primary preprint](https://arxiv.org/abs/1410.7659). Establishes an existing efficient learning route from dynamics, in a model class different from the elementary arbitrary-table construction.
4. Dutt, Lokhov, Vuffray and Misra, *Exponential Reduction in Sample Complexity with Learning of Ising Model Dynamics* (ICML 2021). [Published paper](https://proceedings.mlr.press/v139/dutt21a.html). Reinforces that correlated, nonequilibrium observations can be statistically useful and do not require equilibrium sampling first.
5. Gaitonde, Moitra and Mossel, *Better Models and Algorithms for Learning Ising Models from Dynamics* (2025). [Primary preprint](https://arxiv.org/abs/2507.15173). Addresses the stronger observation issue of seeing changes without all null update attempts; shows the elementary observation model here is not the strongest conventional baseline.
6. Rudolf and Schweizer, *Perturbation theory for Markov chains via Wasserstein distance* (2015/2017). [Primary preprint](https://arxiv.org/abs/1503.04123). General perturbation theory predates the simple coupling bound proved here.
7. Hsu, Kontorovich, Levin, Peres and Szepesvari, *Mixing time estimation in reversible Markov chains from a single sample path* (2017). [Primary preprint](https://arxiv.org/abs/1708.07367). Gives fully data-dependent mixing-time confidence intervals in a general finite-state setting; its state-coverage costs clarify why local structure, rather than a claim that mixing is unlearnable, is the distinguishing assumption here.

## 9. Preserved work and evidence limits

The elementary arbitrary-table theorem above has not been given a separate numerical benchmark. The follow-up `PHASE_RECONSTRUCTION.md` and `phase_experiment.py` develop and check the more consequential task of inferring unseen phase weights from a single trajectory. That implementation retains the transition observations, uses an ordinary conditional-likelihood estimate and explicitly simulates/counts a finite polymer gas. True unknown parameters are used only to generate synthetic observations and assess errors; they are not given to either learner or future inference routine. The full-state validation calculation and spectral check use floating-point arithmetic, not formal verification or a physical experiment. The first finite test, which switched phase eight times, is retained alongside the later no-switch trajectory. Neither test establishes novelty or asymptotic scaling.

**Research outcome:** a concrete reusable capability and an explicit acquisition-complete ordinary construction; no breakthrough claim and no separation surviving the strongest matched comparator.
