# Learned experiment access: a fully paid construction

Status: independent construction and proof sketch for the parent research task. This is not a claim of a new architecture, a separation from all retaining learners, or publication novelty. The general machinery is regenerative control plus sequential-testing change of measure; the small recovery-chain proposition below is derived here and should be checked as an elementary worked theorem. Temporary research notes, not a final deliverable.

## 1. What survives the strong-comparator requirement

The useful object is a learned **experiment-access procedure**. Old data need contain no information whatsoever about a future target parameter. It can nevertheless reduce the primitive cost of obtaining each future informative observation, because it identifies a controller that reaches the relevant experiment efficiently.

An ordinary retaining model learner is a matching construction: retain the state/action outcomes, infer the deterministic recovery action at each state, and plan with that model. Thus this is an experience-to-cost theorem. It is not evidence that a specialized cumulative architecture beats an equally capable retaining learner.

The right complete-lifetime target in the example is Theta(H^2 + T H), not a comparison against T H^2 obtained by forcing the ordinary learner to forget. A quadratic first acquisition and linear later learning costs are both charged.

## 2. General regenerative experiment-access theorem

Let beta be a fresh target parameter, independent of acquisition history H0. A shared controlled environment has an observable reset state s0. A completed experiment e starts at s0, follows a controller, returns one observation Y with law P_beta^e, and returns to s0. The target influences only Y; transitions and execution costs before Y are beta-independent. All failed attempts, retries, and resets count toward the experiment's primitive cost. After acquisition, suppose an experiment library has actual mean costs c_e < infinity, and fresh outcomes are conditionally independent across completed experiments.

For an adaptive target learner let N_e be the number of completed experiments of type e. Assuming integrability, the exact expected execution cost is

    E_beta C_exec = sum_e c_e E_beta N_e.

For any alternative beta', the transcript chain rule gives

    KL(P_beta^transcript || P_beta'^transcript)
      = sum_e E_beta N_e KL(P_beta^e || P_beta'^e).

Acquisition contributes zero to this target KL because H0 is independent of beta. A delta-correct identification rule therefore obeys

    sum_e E_beta N_e KL(P_beta^e || P_beta'^e)
      >= kl(1-delta, delta)

for every alternative beta' whose correct answer differs. Here kl is binary relative entropy. Hence execution cost is at least the linear program

    min_{n_e >= 0} sum_e c_e n_e
    subject to sum_e n_e KL(P_beta^e || P_beta'^e)
                 >= kl(1-delta,delta), for all relevant beta'.

For one binary experiment this reduces to

    E_beta C_exec >= c * kl(1-delta,delta)
                         / KL(P_beta || P_beta').

For multiple binary experiments, the corresponding information-per-primitive-cost upper envelope is max_e KL(P_beta^e || P_beta'^e)/c_e. This is an information-rate statement after acquisition, not an oracle that supplies the costs or controllers. A sequential likelihood-ratio test for one fixed experiment matches the lower bound asymptotically (bounded log-likelihood increments give a bounded overshoot term). A fixed-sample majority test suffices for the fully explicit binary-symmetric example below and avoids floating-point issues.

Here e must index a complete access procedure, including procedures that stochastically choose which physical source they reach. For a randomly reached tagged source J, its kernel is P_beta^e(J,Y), and its KL averages the tagged-source divergences over the target-independent access randomness. Indexing only individual source locations and charging each location's separate shortest-path cost can be wrong when a mixed route opportunistically accepts whichever source it reaches. To lower-bound every primitive policy, include every admissible regenerative procedure (possibly an infinite class), or prove that the specified library is without loss. Optimizing over that class can itself be computationally difficult; the notation supplies no free planner. The chain avoids this issue because there is only one source and its optimal access value is explicit.

### Lower bounds when access itself remains unknown

The displayed LP is an omniscient-access lower bound: giving the learner the correct controller can only help. It does not charge the cost of discovering that controller. A separate cold-access lower bound is needed. The recovery chain below supplies one and matches a constructive retaining learner up to constants.

Do not mechanically add two lower bounds if the same transitions can serve both acquisition and target learning. In the chain, the first terminal access is bounded separately, and each subsequent sample is bounded using the omniscient regenerative cost; these disjoint intervals support an additive lower bound.

### Uncertain learned controllers must be charged

A confidence statement that a learned policy is good is not enough for an unconditional expected-cost guarantee: on its exceptional event it might never reach the experiment.

One safe wrapper is: cap a learned attempt at L primitive steps; if it has not reached an observable valid sampling endpoint, reset at cost r and run an always-valid baseline with mean cost at most c0. If a capped learned attempt has mean cost a and failure probability q, the wrapper's true mean cost is

    c <= a + q (r+c0).

If acquisition certifies a <= abar and q <= qbar with probability at least 1-delta0, then for a fixed number N of target observations,

    E total cost <= E acquisition cost
       + N [abar + qbar(r+c0) + delta0(L+r+c0)].

This expression exposes the issue when c0 is exponential: a merely polynomially small calibration failure probability can still destroy the claimed expected-cost gain. All validity checks must be based on an observable sampling endpoint; a controller's own claim of success does not certify the target kernel. This wrapper protects execution cost, not an unverified observation model.

The explicit chain avoids this caveat: recovery actions are deterministic and exactly certified by observable transitions (including elimination of the other binary action). The physical forward failures remain stochastic and are fully paid.

## 3. Explicit recovery-chain family

Parameters: depth H >= 1, physical forward-success probability p in (0,1), and independent unknown control bits kappa_1,...,kappa_{H-1}. Recovery at the root layer is already known: both buttons at f_0 return to g_0. For the clean minimax statement p is any fixed constant bounded away from 0 and 1, for example p=1/2. The learner does not need to know p to execute the algorithm.

Observed states are g_0,...,g_H and f_0,...,f_{H-1}. The reset state is g_0. State identities are observable, of O(log H) bit length. This is a fully observed finite control problem, not latent-representation discovery.

At g_i, i < H:

- FORWARD costs one primitive step and reaches g_{i+1} with probability p, otherwise f_i.
- PROBE costs one step and deterministically reaches f_i. This is a physical action available equally to every learner; it is not a state-reset oracle.
- RESET costs one step and reaches g_0.

At f_i:

- For i >= 1 there are two primitive recovery buttons 0 and 1. Button kappa_i costs one step and returns to g_i. The other button costs one step and sends the learner to g_0. At f_0 both buttons return to g_0 in one step; their identities are irrelevant and require no acquisition.
- RESET also costs one step and reaches g_0.

There is no action to jump to another state or query an unvisited state's recovery key. All forward random outcomes are independent. No information about kappa_i is available before visiting layer i.

At g_H an experiment for the currently announced target j costs one primitive step, returns Y, and resets to g_0. The fresh target beta_j is independent of all control bits and of the complete earlier history. For the exact primary theorem, Y = beta_j is noiseless. In the noisy extension, Y = beta_j XOR Z with independent Z ~ Bernoulli(eta), eta < 1/2.

## 4. Exact cost after recovery acquisition

Once kappa_i is known, an attempt to advance one layer uses FORWARD. A physical failure uses the known recovery button and retries locally. If tau is its expected primitive cost,

    tau = 1 + (1-p)(1+tau),
    tau = (2-p)/p.

Therefore the optimal known-model mean access cost to g_H is exactly

    H tau.

The lower bound is direct: every layer needs an expected 1/p FORWARD attempts and (1-p)/p returns from f_i; RESET cannot shorten a known recovery. A valid target observation costs exactly H tau + 1 in expectation, including its reset.

For p=1/2 this is 3H+1. The observed target is statistically new: before its first source observation, I(beta_j ; H0)=0 and no retained-data predictor has accuracy better than 1/2 under a fair prior. The reduction is wholly in acquisition cost, not reuse of old target labels.

## 5. Fully charged acquisition algorithm

Start at g_0, where recovery is already known, and advance to g_1 with expected cost tau. At each g_i for i >= 1, earlier recovery bits are already known.

1. PROBE to f_i, at cost one.
2. Randomly choose one of the two recovery buttons, at cost one.
3. If it returns to g_i, its identity is kappa_i. If it sends the learner to g_0, the other button is kappa_i by the public deterministic binary promise. In the latter case, replay the known earlier controller to g_i, at expected cost i tau.
4. Use the now-known local recovery and FORWARD to reach g_{i+1}, at expected cost tau.

Each unknown bit is learned exactly; there is no confidence failure, numerical inversion, spectral gap, hidden representation oracle, or uncharged failed search. Randomizing the first button makes its failure probability exactly 1/2 for every fixed key assignment, not only under a random-key average.

The exact expected acquisition cost, ending at g_H, is

    A_H = tau + sum_{i=1}^{H-1} [2 + (i tau)/2 + tau]
        = H tau + 2(H-1) + tau H(H-1)/4.

Resetting to g_0 for a separate later task costs one further step. At p=1/2,

    A_H = 5H - 2 + 3H(H-1)/4.

The implementation updates a bit table in constant-time word operations per primitive transition. It stores H-1 recovery bits and state indexing, plus target counters. Bit-level costs add only O(log H) factors for state identifiers. Planning is the explicit forward/recover loop; no exponential search is hidden in a planner call.

## 6. Cold-start lower bound against every retaining learner

Take the recovery bits independent and uniform. Consider any learner required to reach g_H almost surely, with finite expected cost. The learner may retain every past transition, update any model, plan adaptively, choose PROBE whenever it wants, and randomize arbitrarily.

For i >= 1, at the first arrival to g_i, no data about kappa_i have been seen. Before the first arrival to g_{i+1}:

- If the learner tries to acquire recovery first, its first recovery button is wrong with probability 1/2, or it explicitly resets and loses layer i immediately.
- If it tries FORWARD first, with probability 1-p it enters f_i without recovery information. Its first nontrivial recovery attempt is wrong with probability 1/2; an explicit RESET is at least as bad for the event under consideration.

Thus the probability of at least one reset losing i layers before the first arrival to g_{i+1} is at least (1-p)/2.

Use layer index as a potential. Every successful FORWARD increases it by one; every reset from layer i loses i. If R_i is the number of resets from layer i before first reaching g_H, then the number of successful FORWARD transitions satisfies pathwise

    N_success = H + sum_i i R_i.

Every failed FORWARD also requires at least one subsequent action to leave its failure state. If F is the number of FORWARD attempts, their independent success coins give E N_success = p E F. The number of physical failure-recovery actions is at least F-N_success, so primitive cost is at least F+(F-N_success) in expectation. Consequently, with no double counting of overlapping replay intervals,

    E first-access primitive cost
      >= tau [H + (1-p) H(H-1)/4].

The independence/Wald step is valid whenever expected cost is finite; otherwise the desired lower bound is immediate. For constant p in (0,1), the bound is Omega(H^2). It applies by Yao's distributional argument to the worst-case expected cost of every randomized cold learner. The constructive acquisition algorithm supplies O(H^2), so this is a matching minimax order. At p=1/2 this lower bound is 3H + 3H(H-1)/8, within asymptotic factor two of the explicit acquisition upper bound.

For T sequential noiseless independent target bits, any zero-error learner must obtain at least one source observation for each bit. The first such access has the preceding cold lower bound. Every later target begins from g_0 and costs at least H tau +1 even with all recovery keys revealed for free. Therefore

    E total cost >= tau[H + (1-p)H(H-1)/4] + 1
                   + (T-1)(H tau+1).

The constructive learner can acquire all recovery keys on the first task, read its bit, and then reuse the controller:

    E total cost <= A_H + 1 + (T-1)(H tau+1).

Thus the full-lifetime minimax cost is Theta(H^2 + T H) for fixed p. The upper and lower bounds refer to all retaining learners, not a reset baseline.

With a separately paid warmup, later exact acquisition costs H tau+1 each, and the complete ledger is A_H+1 + T(H tau+1). A task budget B therefore supports depths of order B after acquisition, while a cold zero-error learner needs order H^2 budget for its first task. The earlier H^2 acquisition is still recorded; it has not disappeared from the lifetime budget.

## 7. Noisy fresh targets and information-rate optimality

Let eta < 1/2 be a known binary observation-flip rate. At fixed recovery depth, the access cost remains H tau+1; observation noise is independent of execution failures.

A majority vote using

    n = ceil[ 2 log(T/delta)/(1-2 eta)^2 ]

observations per target has joint failure probability at most delta across T targets by Hoeffding plus a union bound. The full expected cost after a separate acquisition phase is at most

    A_H + 1 + T n (H tau+1).

There is no floating-point conditioning in this implementation: count binary observations and compare to n/2. Updates and execution are paid.

For one target, any delta-correct sequential test, even with the recovery keys supplied, has

    E_beta execution cost
      >= (H tau+1) kl(1-delta,delta) / d_eta,

where

    d_eta = (1-2 eta) log[(1-eta)/eta]

is the KL between the two binary-symmetric observation laws. A sequential likelihood-ratio test is asymptotically tight in delta for this known observation kernel. For fixed eta bounded away from 0 and 1/2 the majority upper bound has the same logarithmic-confidence and linear-access dependence. When eta approaches 0, majority with the displayed generic bound need not be constant-optimal; the noiseless theorem already uses one observation.

The exact Theta(H^2+TH) full-lifetime lower theorem above is stated for noiseless, zero-error target bits. The noisy section supplies a fully paid upper bound and an omniscient-access information lower bound; do not assert the same additive cold-acquisition lower bound for arbitrary error-tolerant stopping rules without a separate argument.

## 8. Why local recovery is the substantive operation

If physical failure at layer i sends the system to g_0 and there is no local recovery route, even a completely known correct forward controller has expected hitting time

    sum_{k=1}^H p^{-k} = (p^{-H}-1)/(1-p).

For p=1/2 this is 2^(H+1)-2. Learning an accurate forward policy alone does not remove this physical cost. A primitive-failure probability bounded away from zero produces an exponential end-to-end cost.

The acquired recovery procedure changes this to H(2-p)/p in the explicit environment. That is a statement about the resource provided by the operation. It is NOT a lower bound against a strong learner in the recovery-enabled environment: that learner can acquire the same recovery keys, as the construction explicitly shows.

## 9. Established context and source checks

Primary sources opened during this investigation:

1. Cai, Ma, Du (ICML 2022), *Near-Optimal Algorithms for Autonomous Exploration and Multi-Goal Stochastic Shortest Path*. https://proceedings.mlr.press/v162/cai22a.html . Defines acquisition of policies to incrementally L-controllable states, connects it to multi-goal stochastic shortest path, and gives near-minimax guarantees in the stated regime. Retrieval ref: turn22view0.
2. Chen, Tirinzoni, Lazaric, Pirotta (ICML 2023), *Layered State Discovery for Incremental Autonomous Exploration*. https://proceedings.mlr.press/v202/chen23z.html . Defines a layered state-expansion operator and proves efficient acquisition of reachability policies, with a near-minimax result under its identifiability condition. Retrieval ref: turn22view1.
3. Jin, Krishnamurthy, Simchowitz, Yu (ICML 2020), *Reward-Free Exploration for Reinforcement Learning*. https://proceedings.mlr.press/v119/jin20d.html . Acquires exploratory coverage before arbitrary later reward functions; establishes efficient exploration and near-matching lower bounds. Retrieval ref: turn22view2.
4. Kaufmann, Cappe, Garivier (JMLR 2016), *On the Complexity of Best-Arm Identification in Multi-Armed Bandit Models*. https://www.jmlr.org/papers/v17/kaufman16a.html . Lemma 1 is the standard adaptive change-of-measure inequality underlying the experiment-access KL lower bound. Official PDF: https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf . The lemma was directly located and read on PDF page 7. Retrieval refs: turn35view0, turn35view1, turn35view2.
5. Garivier, Kaufmann (COLT 2016), *Optimal Best Arm Identification with Fixed Confidence*. https://proceedings.mlr.press/v49/garivier16a.html . Establishes a characteristic-time optimization and asymptotically matching Track-and-Stop rule for its one-parameter bandit setting. Useful as a model of the standard information-allocation machinery, not a theorem about unknown access controllers. Retrieval ref: turn28search1.

These are strong conventional model-based baselines. The parent must open any source itself before citing a subagent's retrieval ref in a root final response.

The general KL calculation is standard sequential experimental-design/change-of-measure machinery. The short regenerative composition and recovery-chain calculations here should be presented as a worked derivation, not a claimed new field or an uncited general breakthrough.

## 10. Remaining research opening

The worked theorem demonstrates a real cost-shaping effect on statistically independent future capabilities and survives a strong retaining comparator. A research contribution would be a general *acquisition-aware* experiment-access theorem for unknown controlled environments, where the algorithm discovers and validates the access library, target experiments and useful recoveries may themselves be unknown, and the end-to-end bound is close to the best adaptive retaining model/planner. The challenge is not merely learning a representation: it is learning which operation changes the future information-per-primitive-cost frontier, including policy errors and acquisition opportunity cost.

General history-emulation obstruction: if all old acquisition experiments remain available, a cold learner can perform the same acquisition internally at its charged cost. External temporal order alone cannot yield a total-cost separation from all retaining learners. Legitimate cumulative benefits are amortization across future tasks, shorter conditional budgets after acquisition, new physical/source access, or a sharper algorithmic tradeoff within a specified learner class.

## 11. Floating-point numerical diagnostics

The companion `fresh_opening_check.py` applies NumPy floating-point value iteration to the exact finite Bayesian stochastic-shortest-path model over (physical state, known-recovery mask) for small H. Unknown key identities can be quotiented out by symmetry, so the model allows an optimal learner to choose FORWARD, PROBE, RESET, or a recovery trial and retain every outcome. This is a stronger comparator than the explicit acquire-all policy. The numerical iteration stops when the maximum absolute change between successive iterates is below 1e-11; this stopping residual is not a certified error bound on the optimal value. The script is a floating-point diagnostic, not an exact rational solve or a proof certificate. It compares the approximate value with the analytical cold lower bound, the explicit acquisition upper bound, and the closed-form fully-known value. It also Monte Carlo checks the acquisition ledger. Results and explicit method metadata are in `fresh_opening_check.json`, under `floating_point_ssp_checks`.

All 36 floating-point SSP comparisons passed for H=1,...,6; p in {1/4,1/2,3/4}; and T in {1,3}. At H=6,p=1/2,T=1, the rigorous lower bound including the target observation is 30.25, value iteration estimates the optimal Bayes cost as 32.0299883, the simple acquisition algorithm upper bound is 51.5, and the closed-form already-acquired access cost is 19. At T=3 the corresponding values are 68.25, an estimate of 77.3914693, 89.5, and 57. Acquisition Monte Carlo checks at H=2,5,12 agreed with the analytic means 9.5,38,157 within one standard error. The finite Bayesian model has exponentially many masks and is used only for small-instance diagnostics; the proposed polynomial upper bound does not call that solver. The analytic proof and its bounds are unaffected by the diagnostic's floating-point precision.
