# Independent boundary construction and audit

Prepared for the root research agent, 5 November 2026. This is a working note, not a claim of a new physical device or a new general statistical theorem.

## 1. A matching resource boundary for a useful intervention decision

There are two controls, 0 and 1. While operating, either provides useful output at rate v > 0 and consumes the same declared bounded power. The unknown world is theta in {+, -}. Its catastrophic intensities are

| world | control 0 | control 1 |
| --- | ---: | ---: |
| + | epsilon | 2 epsilon |
| - | 2 epsilon | epsilon |

All other telemetry, task outputs, and actuator observations have the same conditional law in the two worlds. Arbitrary adaptive switching, private randomness, parallel copies, and independent initialized workspaces are allowed. Count aggregate active device-time T, not just elapsed wall-time. Replacement/reset after failures is permitted and separately paid.

Expected useful work under a fixed control is v/lambda. In fact the smaller-hazard control stochastically dominates for every useful-work target, so this example is not a mean-only or slowdown artifact. Adding a failed state repaired at rate mu > 0 gives stationary operating mass mu/(mu+lambda), so the interventions genuinely change the invariant law as well.

Let an acquisition procedure recommend the better control with error at most delta < 1/2 in either world. Write

L_delta = kl(1-delta,delta) = (1-2delta) log((1-delta)/delta).

The counting-process likelihood ratio, including adaptive actions, gives

D(P_+ || P_-) = E_+ integral [lambda_+ log(lambda_+/lambda_-) - lambda_+ + lambda_-] dt.

This identity is obtained by multiplying the likelihoods of event times and their survival intervals. Conditional action probabilities cancel because the same controller is run in both worlds. Independent extra telemetry contributes zero divergence. Each active device contributes at most

(2 log 2 - 1) epsilon

per unit operating time. Data processing to the final recommendation therefore proves

**E_+ T >= L_delta / ((2 log 2 - 1) epsilon).**

The same statement holds with the two worlds reversed. Parallelism cannot improve this aggregate-time lower bound.

There is also a destructive-sample lower bound. Dividing each local divergence by its true event intensity gives either 1-log 2 or log 2-1/2; the former is larger. Using the counting-process compensator,

**E_+ N_fail >= L_delta / (1-log 2).**

Thus high confidence needs logarithmically many expected catastrophic observations if ordinary operation is the only informative channel. A unique unrecoverable specimen cannot support arbitrarily high confidence in this class.

### Attaining operation

Run one device under each control with equal live time. In a paired interval, wait until the first of the two fails. Its label is Bernoulli(1/3) in one world and Bernoulli(2/3) in the other; the waiting rate is 3 epsilon. Replace/reset the failed device, pausing the survivor so subsequent live times stay equal. Stop after m independent event labels and choose the control with fewer failures. Hoeffding gives error at most exp(-m/18), so m >= 18 log(1/delta) suffices. Sequential likelihood tests improve constants.

Resource accounting:

- Aggregate active device-time: 2m/(3 epsilon) in expectation.
- Useful output obtained during acquisition: v times that active device-time in expectation.
- Two simultaneously operating devices.
- m resets/replacements; if each takes mean d and energy E_reset, add md elapsed reset time and m E_reset energy under the simple paired implementation.
- Constant-size event-label memory beyond the counter, and O(m) computation.
- The rare scale epsilon need not be known to this race/label rule.

This matches the lower bound in epsilon and log(1/delta). It is an ordinary sequential comparison, not an advantage over the strongest same-access direct method.

### Extra prepared diagnostics and the real crossover

Suppose an additional physically acquired diagnostic costs c units of the same resource and produces a bit with probabilities (1+d)/2 and (1-d)/2 in the two worlds. Its divergence is

k_d = d log((1+d)/(1-d)) = Theta(d^2) for d bounded away from 1.

For mixed ordinary exposure and diagnostic probes,

(2 log 2-1) epsilon E T + k_d E N_probe >= L_delta.

Consequently for B=T+c N_probe,

E B >= L_delta / max{(2 log 2-1) epsilon, k_d/c}.

Using only the better experiment attains the dependence

Theta(log(1/delta) min{epsilon^(-1), c/d^2}).

The preparation cost and diagnostic contrast, rather than the word “decision,” determine whether the rare-event cost disappears. An ordinary decision method with the same diagnostic gets the same benefit.

The construction can be appended as an independent catastrophic channel to an arbitrarily complicated otherwise functioning plant. Hence its scope is not limited by the two-state presentation: any claimed general easy-prevention theorem must rule out or assay such intervention-relevant channels.

## 2. Audit of the homogeneous nearest-neighbor useful-work controller

State i is damage, 0 <= i <= N, with N absorbing. At each cycle action a supplies positive reward r_a, moves up with p_a > 0, down with q_a >= 0, and otherwise holds. At 0 the attempted down move reflects to 0. There are finitely many actions and p_min=min_a p_a>0.

Define u_a=r_a/p_a, v_a=q_a/p_a, d_0=max_a u_a, and

d_i = max_a (u_a + v_a d_(i-1)).

Then V_i = sum_(j=i)^(N-1) d_j satisfies the Bellman equations exactly. For any action the inequality p_a d_i >= r_a+q_a d_(i-1) is precisely the Bellman super-solution inequality. Choosing an attaining action gives equality.

Every adaptive policy is absorbed in finite expected time: conditional on any history, N consecutive upward moves have probability at least p_min^N, so E tau <= N/p_min^N. Bounded rewards make the Bellman verification legitimate. The stationary deterministic maximizing feedback therefore attains the optimum over all randomized and history-dependent policies.

### Stronger controller-description fact

Let f(x)=max_a(u_a+v_a x). It is increasing and convex. The sequence d_i is nondecreasing because d_1>=d_0 and f is monotone. Along an increasing argument, active envelope slopes are nondecreasing. Choosing ties consistently therefore yields an optimal controller in which each active line occupies one contiguous damage interval, with at most |A|-1 switches. This is a bounded policy description, although the thresholds and the damage sensor still have physical representation costs.

If v_* > 1 is a unique largest slope, define

D = max(0, max_(a != *) (u_a-u_*)/(v_*-v_a)).

Since d_i grows at least geometrically under the star line, eventually d_(m-1)>D at a finite m independent of N. The star action is then uniquely optimal for every state i>=m. A finite collection of strict prefix and slope margins permits constant-precision local experiments to certify the full feedback for all N. The constants can be arbitrarily bad as margins vanish; a uniform family must declare positive margins and lower bounds on p and relevant holding probabilities.

Additional phase facts, if useful:

- If max v_a > 1, V_0 grows exponentially in N.
- If max v_a = 1, the largest intercept among slope-1 lines eventually dominates, and V_0 grows quadratically.
- If max v_a < 1, d_i converges to max_a r_a/(p_a-q_a), so V_0 grows linearly.

These follow directly from the envelope recursion. They are not asserted as historically new.

### Robust same-access forecast lower bound

On an open parameter cell with fixed strict policy margins, perturb only q_* by order eta/N and compensate the holding probability. Keep p_*, rewards, and all relevant probabilities bounded away from zero. The optimal feedback remains unchanged for large N, while

log V_0 = N log(q_*/p_*) + O(1).

Choosing perturbations with a sufficient constant makes the optimal values differ by more than 2 eta in log scale. Each one-cycle experiment has KL divergence O(eta^2/N^2). This remains true under adaptive action choices, arbitrary independent state preparation, observation of deployed trajectories, and parallel copies counted by total cycles; boundary reflection only loses information.

An estimator of the absolute optimal value to multiplicative exp(+-eta) accuracy with error delta must consequently use

Omega(N^2 eta^(-2) log(1/delta))

expected total cycles. Estimating the finitely many transition probabilities to precision O(eta/N) and applying ordinary dynamic programming gives the matching scale under this regularity contract.

This lower bound concerns this particular absolute-value forecast. It does not say every prediction problem costs N^2, nor does it give the proposed controller an advantage over an equally informed ordinary decision solver.

### Resource and robustness qualifications

Positive r_a must represent actual useful output, or an explicitly declared positive work-minus-priced-energy reward. Bound cycle duration and power, or restrict the admissible actions to a throughput/power envelope. Operating for an exponential lifetime consumes exponential total operating time and energy. A hard total fuel budget changes the state and is not covered by the recurrence.

State observations and action execution must be correct under the model. Noncatastrophic implementation noise can be included in the calibrated kernel when the declared homogeneity and transition support survive. Generic state-dependent misclassification cannot be absorbed into the same two probabilities. Bounded sensing errors may preserve the tail action away from the switch region, and thus preserve an exponent, without preserving exact optimality.

## 3. An explicit exponentially costly model-certification boundary

Take two unit-reward controls:

A: p=0.2, q=0.4; B: p=0.25, q=0.375.

Their affine lines are 5+2d and 4+1.5d. Hence A is strictly optimal at every state in the nominal nearest-neighbor model. The fixed-B expected work from 0 is

M_B(N) = 24(1.5^N-1)-8N.

Modify only action A: independently at each cycle, kill directly to N with probability h, otherwise perform its nominal transition. The reward is delivered at the start of a cycle. Let h=10/M_B(N), taking N large enough that h<1/2.

Always A now earns at most 1/h = M_B/10, while always B still earns M_B. Thus the nominal unique optimal controller is worse than a known feasible alternative by at least a factor ten.

For any state preparation and any chosen action, the modified kernel dominates (1-h) times the nominal kernel, so

D(P_nominal(one cycle)||P_modified(one cycle)) <= -log(1-h) <= 2h.

The adaptive chain rule and final-decision data processing imply that exact optimal-policy certification uniformly over these two model worlds requires

E_nominal K >= M_B(N) L_delta/20.

This is exponential in N although the per-cycle model discrepancy is exponentially small. It is a limitation on extending the certified class, not a contradiction of the within-class constant-evidence theorem.

**Exact-policy scope:** this lower bound is for exact optimal-policy certification. The displayed factor-ten loss concerns the nominal always-A policy in the altered world. I have not proved that every approximately optimal adaptive policy must be distinguishable between the worlds, nor a matching exponential lower bound for an arbitrary fixed approximation factor. A controller can trade some nominal value for robustness, so those stronger statements need a separate argument.

The dependence is attainable. Prepare/reset to state 0, apply A for one cycle, and inspect whether a direct jump to N occurred. For N>=2 such a jump is absent under the nominal model. Repeating O(h^(-1)log(1/delta)) times detects the alternate world with error at most delta, after which its optimal policy can be computed by ordinary finite-state dynamic programming. Reset and metrology costs are additional; no inexpensive probe that magnifies h has been assumed.

The same mechanism covers unmodelled common-cause faults and catastrophic controller/sensor failures. “No bypass channel” is a substantive structural premise. Constant ordinary transition data cannot certify it at an exponentially small lifetime scale.

## 4. Repair-capacity route: useful cautions

For the alternative birth-death model b_k=lambda(N-k), d_k=min(mu k,cN), with failure at k about (1-rho)N, the saturated-region quasipotential

V=c/lambda-rho-rho log(c/(lambda rho))

requires both equilibrium and the barrier to lie in the saturated part: lambda rho < c < lambda mu/(lambda+mu), hence rho < mu/(lambda+mu). In that region healthy count is an immigration-death process with immigration cN, death lambda h, and local Poisson stationary weights of mean Nc/lambda.

Writing Delta=c/(lambda rho)-1, N V is about N rho Delta^2/2. The escape prefactor is about exp(NV)/(lambda sqrt(N rho) Delta), not merely exp(NV). From an all-healthy start there is also relaxation time of order log(1/Delta)/lambda, becoming log N/(2lambda) in the critical window Delta=O(N^(-1/2)). Predictions derived only from NV should not be extrapolated through that window. A clean exponential-dominated moderate-deviation statement can require N Delta^2 much larger than log log N, or simply fix positive slack.

An all-safe-start mean theorem does not imply high-probability survival from all safe starts. One step below the failure boundary there remains a constant probability of immediate failure. A verified reserve margin is needed for a high-confidence mission guarantee.

## 5. Primary prior art and attribution

1. Kaufmann, Cappe, Garivier (2016), “On the Complexity of Best-Arm Identification in Multi-Armed Bandit Models,” JMLR 17. Lemma 1 is a general adaptive change-of-measure inequality. https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf

2. Garivier, Kaufmann (2016), “Optimal Best Arm Identification with Fixed Confidence,” COLT/PMLR49, 998–1027. Tight characteristic-time bound and asymptotically optimal Track-and-Stop in their one-parameter bandit setting. https://proceedings.mlr.press/v49/garivier16a.html

3. Nitinawarat, Veeravalli (2013 preprint; 2015 publication), “Controlled Sensing for Sequential Multihypothesis Testing with Controlled Markovian Observations and Non-Uniform Control Cost.” Controlled observation costs and asymptotically optimal tests already exist. https://arxiv.org/abs/1310.1844

4. Wijngaard, Stidham (1986), “Forward Recursion for Markov Decision Processes with Skip-Free-to-the-Right Transitions, Part I: Theory and Algorithm,” Mathematics of Operations Research11(2),295–308. Its abstract explicitly describes forward recursion for maximum total reward to state i. The scalar recurrence is a specialization of this established lineage, not an invented planning principle. https://pubsonline.informs.org/doi/10.1287/moor.11.2.295

5. Dupuis, Katsoulakis, Pantazis, Plechac (2016), “Path-Space Information Bounds for Uncertainty Quantification and Sensitivity Analysis of Stochastic Dynamics,” SIAM/ASA JUQ, DOI10.1137/15M1025645. Supplement gathers standard path-relative-entropy and Fisher-information formulas for Markov processes. https://epubs.siam.org/doi/10.1137/15M1025645

The explicit combinations and physical-resource accounting above can be presented as results derived in this run. Their historical novelty has not been established, and the general KL, sequential testing, and skip-free control machinery must retain its prior attribution.
