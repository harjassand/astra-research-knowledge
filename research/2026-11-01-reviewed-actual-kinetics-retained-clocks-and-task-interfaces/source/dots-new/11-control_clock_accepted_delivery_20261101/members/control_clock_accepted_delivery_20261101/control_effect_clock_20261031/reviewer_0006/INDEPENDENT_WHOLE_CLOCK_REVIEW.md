# Independent whole review: acquired control-effect clock

Date: 2026-11-01 UTC. Reviewer: `producer-workspace/challenge_graph_profile_compiler`.

## Verdict and binding qualification

**PASS within the stated classical generative-access scope, with one explicit confidence-range qualification.** I read the complete proof, frontend, test harness, ordinary comparator, replay entry point, README and comparison ledger, checked their joins to the previously reviewed canonical consumer, and reran the frozen replay. No false admission or substantive mathematical obstruction was found.

The exact finite lower bounds in Section 6 are sound. Their shorthand consequence `Omega(log(1/delta)/(epsilon(1-gamma)))` must be read in a fixed small-failure regime, for example **0 < delta <= 1/4**. The interface elsewhere permits delta in (0,1), but this asymptotic assertion does not extend to that entire interval. At delta >= 1/2 a zero-query fair choice of the two appropriate deterministic policies can meet the two-instance success requirement. The displayed exact log((1-delta)/delta) bound then correctly becomes vacuous. This qualification changes neither the upper construction nor its code, nor the claimed small-confidence obstruction. I reported it to root and the author before writing this receipt. Frozen source files have not been edited.

This is a new source-bound receipt, not an extension by assumption of any old receipt. The result is a valid no-gap, capped response acquisition and ordinary decision-consumer composition; it is not an executed useful small-error acquisition, an exclusive advantage over ordinary retaining methods, a physical access certificate, or a novelty determination.

## Exact source binding

Directory: `control_effect_clock_20261031/`.

Manifest `REVIEW_FREEZE_MANIFEST_20261031_2348UTC.json`, 4,899 bytes:
`245ef5fdb6fee5dd55ae8eaa33c6839ae3176cd28585be7d485eced517e7151d`.

All 14 branch files and 9 dependencies were verified against byte counts and SHA-256 before replay and again in the independent checks. Main files:

- `PROOF.md`: `085e889e1c8879941b98d22d823ea85f37d6eb4eea284e5934927b2bbb0d8a77`.
- `clock_response.py`: `a31912dde689204caa63ddfb93bd80ead9301309d807be3568bc1e4ba86bcece`.
- `check_clock_response.py`: `d33e907b833e45f9611494f83e8d9ff7225ca2d94fcd46bd888eeee59475e079`.
- `ordinary_coupled_geometric.py`: `2ff64987c6846a1241d40b43982c00b9fdffa5664a3beddd4432b66db946aab2`.
- `replay.py`: `98d94cf8c0d9b55e900a7818969c4964813220656a009c619bd3c64080a9a006`.
- `README.md`: `27ef6309bdac3bafd9c7d40493900a6b9d3821727a5a7ce48816b3903c8d82d4`.
- `SOURCES_AND_COMPARISON.md`: `afabb87bb197bbfb1016223e340a4cc8d896fa15c68bcac12183f0a1849115f7`.
- Saved paths: `1a17c93579cca9ff0c7e8878db1eb98bd9a57f8836776eae79a6a26b5a8299b9`.
- Current observed response v2: `27f386df8896eb07e8191012f8e87f9178113344e5a0f6f0425f9d5f83a438cb`.
- Ordinary matched result: `cdefc1b837dea4a7084391e7015a4309e8ef251e5f2fbb725cb2e01ee7c2e8df`.
- Current harness v3 result: `6ba56b7563a7ddc26bf7de0cb919fc84261d9d1a10aa39048c47e736e1cdbbb9`.

The earlier response/test JSONs remain historical, as labeled in the manifest. They are not silently relabeled as current-source outputs.

The reused direct canonical code is `8b57cfec3a16b764fd287c153bdb32272f8998e9ea3b0ebaba62de73067978b9`, its corrected proof is `c74a86d0de64d29acfc106082497c6ab60dc1a77f43628de22a9b12f1283162a`, and its whole receipt is `415d90f8660ce447de3043e7d127525f1ad1da5020f5fcaeca8dbf0a28145117`. In particular, the withdrawn max-gap/min-C_X equivalence is not reinstated here.

## 1. Actual observation and no-gap tail

With row-stochastic matrices, H=(1-gamma)(I-gamma A0)^(-1)Z and t=gamma/(1-gamma), the target is U_a=t(A_a-A0)H. The displayed discounted series has the correct initial gamma and powers.

The pair begins with independent action/baseline outputs from the same requested row, then uses independent baseline steps until the two **microscopic** labels coincide. From equality, a common continuation exists and both marginals remain correct; it need not be generated because every subsequent difference vanishes. Merely equal block labels would not justify stopping. The supplied counterexample and exact pair-chain tests correctly preserve that distinction.

The cap K includes the terminal pair at K. The prefix ends at K-1, and tau=K contributes zero to its omitted continuation. Thus P(tau>K), not an erroneously shifted event, controls every omitted summand. Absolute discounted summability holds even when meeting never occurs. The bound 2 gamma^(K+1) P(tau>K)/(1-gamma) follows without a gap, stationary distribution, or undiscounted integrability assumption. The call count 2+2 min(tau,K) is exact, including K=0.

This access model pays named-state preparation and label sensing. Genuine independence and correct requested action execution are premises. A source able to continue two physical trajectories could have a different preparation cost, but that additional operational ability is not inferred.

## 2. Confidence arithmetic and common-data receiving

Each subset sum of a prefix lies in [-L_K,L_K], with L_K=gamma(1-gamma^K)/(1-gamma). Prefix row errors sum to zero, so their L1 norm is twice the largest subset sum. Hoeffding with the stated subset logarithm gives the factor 8 in the squared radius. No subset enumeration is executed.

For the empirical-Bernstein option, each coordinate range has length 2L_K. Rescaling and applying both signs gives the stated variance term and 14 L_K log/(3(N-1)) range term. Summing coordinate bounds is safe. Taking the minimum of two already paid simultaneous bounds is safe. Neither zero empirical variance nor the realized longest observed path is substituted for the known range.

For the tail, zero observed survivors give the exponential no-success bound. Otherwise solving h >= p-sqrt(2pb) yields p <= h+b+sqrt(2hb+b^2). Upward roots and truncation at one are conservative. The prefix/tail statistics may be dependent; their error probabilities are union-bounded rather than multiplied. The integer logarithm upper bounds are conservative on the arguments actually used, all greater than one.

Let Uhat be empirical prefix rows. The maximum within-block empirical discrepancy plus the maximum row confidence radius bounds ||U-Z W Uhat||_(infinity->infinity) by the triangle inequality. Exact closure, when present, makes the measured discrepancy at most twice the row error and hence the total at most three times it. Exact closure is not assumed for validity: a nonclosed source can receive a larger or refusing certificate.

The returned status `PASS_RESPONSE_CONFIDENCE_ARITHMETIC` means the formula and data/design consistency have been received; it is not a small-regret PASS, a posterior guarantee for the particular observed dataset, or authenticated source provenance.

## 3. Canonical control consumer and all-goal scope

The scaling Bhat=B_Uhat/t and eta=eta_U/t gives exactly t Bhat=B_Uhat and t eta=eta_U. The reused direct canonical theorem therefore supplies 2 eta_U C_X, or the task-specific residual form 2(rho+eta_U ||w||_infinity). No sampled hhat, hidden inverse of WH, supplied contraction, or new policy enumeration is introduced.

The acquired canonical transform is computational decision geometry, not predictive block transition probabilities. Its LP proposal, exact sign/column/inverse checks, nominal Bellman checks and reward/task hashes remain paid. A valid positive candidate is enough; backend optimality is not needed for admission. An ordinary correct polynomial-time LP is a theoretical implementation; the installed simplex can fail or take too long. The finite search has a grid budget, not an installed hard per-LP timeout or a guaranteed worst-case runtime.

The event is uniform over the bounded final block/action reward table, so later adaptive choices of such tasks do not need a new probability union. They do not expand the source family, action set, discount, partition/sensor, or confidence request. Pointwise regret is relative to the original source's optimal discounted control, while the returned implementable policy is a stationary block table. It is not a newly acquired hidden-state or uncharged deployment-learning interface.

## 4. Retained grid, adaptive selection, and refinement

For i>=1,j>=0, the budgets delta_total 2^(-i-j-1) sum to delta_total. Each grid point reads a fixed prefix N_i of independent conceptual pairs at its fixed cap K_j. An analysis-only infinite bank can be revealed in an adaptive order because fresh independent source calls supply each unobserved transition. Sharing prefixes and extending censored paths does not require grid-point independence. A union over the predeclared grid permits subsequent adaptive point selection and stopping; it does not justify arbitrary new outcome-dependent N,K with an unchanged fixed-point confidence.

The cost bound uses N_i(K_j+1)=2^(i+j), d points on diagonal d, and sum_{k<=d} k 2^k=(d-1)2^(d+1)+2. This proves the stated O(F d 2^d) upper cost even without reuse. Actual stored trajectories and all failed proposals remain charged.

Refinement starts from native reward-feature equality. If a stable target refines the current partition, current indicators factor through target indicators, and so do H and U. Target-equal rows cannot be split on the confidence event. If distinct exact signatures are separated by Delta and e<Delta/6, estimated between-signature distances exceed 4e while within-signature distances are at most 2e. The connected-component rule then recovers the exact next refinement. At most n-r0 strict changes occur; a finite-precision stall is UNKNOWN.

Changed partitions require fresh validation banks and outer confidence allocation, as the proof says. The frontend provides initial/refinement receiving and the fixed-partition grid search; it has not executed or claimed a successful complete multiround acquisition. Old paths can remain available to discovery and ordinary comparators without being mislabeled as fresh validation.

## 5. Favorable success and canonical neighborhood

The exponential pair-tail assumption in Section 5 is an analysis condition, not an input substituted into the receiver. The supplied N bounds give a Hoeffding prefix at most e/4 before rounding and ell/N <= e(1-gamma)/96. Together with p <= e(1-gamma)/64 and the root budget, the empirical upper tail is at most 9e(1-gamma)/64 on the additional success event, hence tail error at most 9e/32. The slack covers rounding. The claimed sufficient schedule follows; all success-event, dimension and grid logarithms still have to be paid.

For the canonical neighborhood, every original coefficient column sums to one. Subtracting (lambda/r)11^T from (1-lambda)X0 therefore gives strict off-diagonal slack. The displayed lambda yields column sums at least delta0/2. Row-L1 perturbations at most e change an entry by at most J e and a column sum by at most r J e. Rescaling by 1+Je earns the claimed positive gap. Baseline columns bound X diagonals by one; a correct maximum-gap LP therefore gives a finite C_X bound without claiming it minimizes C_X. The resulting 48e/delta0 sufficient regret follows from eta_U<=3e.

These are conditional sufficient schedules, not executed data acquisition, necessary sample counts, a simplex runtime guarantee, or a claim that pairwise meeting captures every useful control effect. Identical uniform kernels give zero true action effect but an independent pair meeting time of n-1; this is a genuine limitation of this particular access/coupling construction.

## 6. Decision-task and expected-cost lower bound

The two-source construction gives H=I, U=c[[-1,1],[0,0]], c=8 epsilon, and a simple canonical gap at least 2/3. Thus a good static canonical witness does not bound the physical persistent-response clock.

For a stationary randomized output table using action 1 with probability theta, solving the actual two-state Bellman equations yields exactly the two displayed values. On p0, epsilon optimality requires theta<=1/2. On p1 every such theta has regret strictly larger than epsilon for 0<epsilon<=1/16. This establishes disjoint required output events, not merely different parameter values.

Only probes of (state 0, action 1) reveal p. Conditional on any learner randomness and any finite p0 stopping transcript, its probability under p1 along the same all-zero informative outcomes is multiplied by (1-p1)^N0. Arbitrary adaptive requested rows/actions do not change this likelihood statement. Summing over finite stopping transcripts proves the change-of-measure inequality. For an almost surely terminating learner, this also covers unbounded random stopping; finite expectation permits the Jensen step, and infinite expectation already satisfies the conclusion. With G the p0-good output event, q=P0(G)>=1-delta and E[N0 1_G]<=E[N0], monotonicity of q exp(-a M/q) gives the displayed expected-cost bound.

The exact bound is valid as written. The positive asymptotic Omega(log(1/delta)/(epsilon(1-gamma))) conclusion is bound here only for delta<=1/4, as explained above. It concerns certification/return of the stated stationary-table decision task before deployment. It does not lower-bound a controller granted uncharged online learning, inspectable source probabilities, stronger sampling access, or a different success requirement. The p0 source meeting instantly does not invalidate the bound: one must still rule out rare persistent effects. Direct Bernoulli estimation is an ordinary strong method on this very simple instance.

## 7. Executable receiving and independent checks

I read all executable files in the freeze. The receiver recomputes the external design, checks its exact digest and strict integer types, requires complete distinct row/action coverage, validates every retained label, forbids continuing after actual meeting, rejects prematurely censored requested paths, replays every stored path's call ledger and sums every attempt's paid calls. It can receive an earlier fixed grid prefix from a larger retained bank. The first N paths, not a selectively favorable subset, are used. It reconstructs the empirical rows, variances, tail counts, confidence allocation and canonical core.

The attempts metadata is a replayable arithmetic ledger, not authenticated predeclaration evidence. Neither it nor hashes prove fresh iid randomness, source identity, correct action execution, genuine reset ability, or absence of omitted experiments. Internal helper functions are scientific typed APIs; the externally bound `receive` entry point and its explicit protocol premises are the reviewed receiving claim.

Nonmutating full replay reproduced **707 exact checks and 14 refusals**, and added **214 simulated source calls**, including the six-attempt failed search's 100 calls. Saved replay itself used zero new calls. All 23 manifest entries matched. I did not regenerate or overwrite the original observation bank or JSONs.

Independent `reviewer_0006/extra_checks.py` passed **655 exact checks and 12 refusals**, with **zero source calls**. It exercises synthetic paths meeting before, exactly at, and after every selected cap; three actions; small and large discounts; retained longer paths; prefix indexing, tail counts and calls; unseen-tail/range costs despite every observed path meeting instantly; external design/type/substitution and real censoring refusals; exact Bellman inverses for the lower-bound task; dyadic budget/cost identities; and all frozen hashes. Synthetic path arrays are algebra/receiving fixtures, not iid observations. A reviewer test initially miscounted its own synthetic paths' call total by a factor two; the production receiver correctly rejected that test input, and the test ledger was corrected before running the passing suite. This was not a production defect.

Reviewer evidence, all uniquely named:

- `full_replay.json`: `1b3c11d88b247bb520587c9d8be5337b9289ae52d0310cd78d9d2aa751655880`.
- `extra_checks.py`: `434b7b8645d9b7adee64e2d29fc716471dd32862092cbccef2c2402998ebc746`.
- `extra_checks.json`: `462bd6cc3e42e6fd6fd36f5a29b00d8d95805c2dad950b1f44cf659669277e53`.

## 8. Actual outcome, costs and ordinary alternatives

The actual saved bank contains 512 pairs and **2,142 forward calls**. Its response radius is
`85314737102334314020000827/8589934592000000000000000`, about 9.93. The requested 0.01 all-goal regret remains **UNKNOWN**. The small retained search also remains **UNKNOWN** after six attempts and 100 calls. The small canonical PASS in the tests is explicitly a coefficient/error unit fixture, not observation-based successful learning.

The matched ordinary coupled-geometric receiver uses zero additional source calls and reproduces eta_U=1485/128. Its 1,888-call shorter stopped realization is counterfactual: the actual 2,142-call bank remains paid. Conditioning publication on having completed retained paths does not turn its fixed-N confidence into a conditional-on-completion confidence. Its unconditional failure event, intersected with the event on which it returns, remains bounded. Seeds/coins must not be selected for favorable answers after inspection without a further event. Prefix and ordinary endpoint estimates have separately allocated budgets; taking their best result needs their joint union budget or ordinary reuse of the already certified prefix.

The coupled-geometric mean, variance and cost statements are correct: with independent internal T geometric on nonnegative integers, Xi=t[Z(X_T)-Z(Y_T)]1{T<tau} has mean U and costs 2+2min(tau,T). Since P(T<tau)<= (1-gamma)E tau, its coordinate variance is bounded by gamma^2 E tau/(1-gamma). Thus it already has inverse-linear discount acquisition in the favorable regime. Conditional expectation over T gives the full paired Poisson sum; the capped prefix is a partial Rao–Blackwellization with a paid tail. These are ordinary tools available to all competitors.

I freshly opened [Douc–Jacob–Lee–Vats, Definition 5](https://arxiv.org/pdf/2206.05691): it directly uses sums of observable differences until meeting to estimate Poisson-solution differences. That is a strong primary match for the core estimator; the present proof supplies its particular discounted capped/confidence/control receiving. It does not establish historical priority for that composition.

I also read the separate post-freeze note `control_clock_prior_followup_20261031/NOTE.md`, hash `cf9bd59edb2e75e1d8d65792abe3ccd70bcc539f785ce4eab5ce8edc750fb4b6`, and freshly checked [Li–Wei–Chi–Chen, Theorems 1–2](https://arxiv.org/pdf/2005.12900v8). Its full unnormalized accuracy range allows substituting epsilon/(1-gamma), yielding inverse-linear discount sample scaling for normalized fixed-goal planning. The note's finite reward-net deduction is sound at paper level: a simultaneous union over net tasks on the same data and perturbation array requires no task independence; normalized reward Lipschitz continuity transfers to later rounded goals. The net need not be enumerated in execution. Finite-bit planner realization remains separately paid. This is not a review or implementation of every additional span/mixing source cited in that note.

Consequently neither inverse-linear discount scaling nor many-task retention is an exclusive capability. The possible remaining interest is a small nonpredictive decision representation and instance-sensitive response/accuracy-tail tradeoffs, after the full n-state acquisition, map, calls, storage and exact arithmetic are paid. No measured total-work or practical superiority follows here.

## Final scope

Accepted: the qualified theorem, exact finite receiving, retained grid/refinement logic within its declared implementation limits, same-data ordinary comparator, and the correctly refusing actual experiments, bound to the listed freeze.

Not accepted by implication: provenance authentication; physical preparation/sensors; arbitrary adaptive partitions without new confidence; undocumented optional stopping; useful observed 0.01 admission; complete multiround execution; guaranteed simplex timeout/optimality; new prior literature claims; or subsequent constructions outside this manifest.
