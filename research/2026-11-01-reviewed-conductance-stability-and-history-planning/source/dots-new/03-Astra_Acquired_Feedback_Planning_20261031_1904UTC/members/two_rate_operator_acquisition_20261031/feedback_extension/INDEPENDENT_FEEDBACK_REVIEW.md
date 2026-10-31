# Independent whole review: acquired-block feedback planning

## Verdict

PASS, within the explicit-state, offline, time-dependent acquired-block Markov-policy interface, conditional on the stated fresh iid sampling and independently fresh probe premises. This is a separate review of the feedback extension, not a retroactive enlargement of the open-word receipt.

The final polynomial receiver genuinely reconstructs the local norm certificates, the uniform model-error bound, the exact Bellman policy, and the packed retained interface. No mathematical blocker remains. The code is a typed scientific API with assertions enabled, not a hostile-JSON authentication service. It does not authenticate source truth, independence or sampling chronology. In particular, seeded synthetic observations/probes do not establish those probabilistic premises.

I read the complete final PROOF, BLOCK_COMPARISON_PROOF, SCOPE, README, PRIOR_MATCH_AND_COSTS and all new Python bodies, including the final receiver and the two optional consumers/counterexamples. All 23 branch files and 16 dependencies match the final freeze manifest:

`FEEDBACK_FREEZE_MANIFEST.json`, 8,715 bytes,
SHA-256 `da0208fdba68e98e77da2d4cb25d2e0e5f452928cd7c08554dca213ed7da14fe`.

The exact per-file source binding is reproduced in the appendix. Frozen author sources/results were not modified. Test regeneration wrote to temporary locations or called nonmutating run() entry points.

## 1. Actual feedback operator family

For the block-average projection P=ZW in uniform H=I/n and Q=I-P, each block selector D_g commutes with P and Q. Row selection

    A_pi=sum_g D_g A_(pi(g))

is precisely the backward-value transition operator for a microscopic state whose block determines its current action. It is stochastic. Its coarse row is the corresponding row of the chosen action. Products describe time-dependent Markov feedback on acquired block labels, not arbitrary observation histories.

Disjoint selectors imply

    ||Q A_pi P x||_H^2
      =sum_a ||D_a Q A_a P x||_H^2
      <=sum_a e_in,a^2 ||x||_H^2.

Thus the implemented sqrt(m) times the maximum incoming bound is safe. The outgoing row and coarse row-error bounds are unchanged, since each row chooses one already controlled action. The same orthogonal-row argument bounds ||A_pi-C_pi|| by sqrt(m) times the simultaneous action observation radius. Neither the original single-action complement contraction nor an unproved feedback stability assumption is reused.

The finite collection has m^r one-step maps. Its horizon-L products need not be enumerated: the uniform operator event bounds every product. Randomized Markov policies are convex combinations of these maps; the norm/row estimates persist by convexity. This does not cover arbitrary microscopic-state policies, history-dependent policies with additional memory, or postselected trajectories.

## 2. Polynomial comparison geometry

Write Q_g for within-block centering. If u_gh bounds all ||Q_g C_a[g,h] Q_h||_2, then for x partitioned into blocks,

    ||(Q C_pi Q x)_g||_2 <= sum_h u_gh ||x_h||_2.

Taking the Euclidean norm proves ||Q C_pi Q||_2<=||U||_2, uniformly in pi. This is ordinary block norm domination; it works for unequal block sizes. No positivity or stochasticity of the observed C_a is needed. Uniform H differs from Euclidean norm only by a global scalar.

The implementation embeds a rectangular g,h block in the upper-right corner of a zero matrix of dimension d=|g|+|h|. The two centering projections act on the appropriate input and output blocks; its nonzero singular values are those of Q_g C_a[g,h]Q_h. The inherited norm routine normalizes counts by d/N_block, so multiplying by n*N_block/(d*N_coarse) exactly restores the original observed operator. This correction is essential and is present. An empty observed block is exactly zero only as an observed block; the full observation uncertainty remains in sqrt(m)*t.

The r-by-r norm is acquired through the exact PSD bisection in norm_up, not by a free spectral oracle. The 32 local probes in the fixture are actual retained inputs to the replay. Sparse multiplication work, projection work, large-integer arithmetic and source calls must be distinguished. This is polynomial sufficient admission, not optimal switched-norm recognition.

The exact n=6 counterexample is sound: PSD checking certifies ||QAQ||<=15/16, while a nonnegative entrywise lower comparison matrix has a positive-vector squared norm ratio greater than one. Monotonicity of the norm for nonnegative matrices makes this a valid obstruction to a contraction certificate via exact block norms. It does not prove that every finite-horizon value certificate fails, nor that the other leakage/task hypotheses admit that example.

## 3. Probability, adaptive acquisition and old work

The fresh block probes are conditioned on the already fixed acquired data and partition. There are m*r^2 events, each assigned delta/(8*m*r^2), so their union occupies the old delta/8 norm slot. The original simultaneous full-observation, pilot, incoming/outgoing and fine-model events are retained. Reusing the same outgoing counts for fine transition probabilities and leakage is legitimate because their error events are union-bounded, not asserted independent.

The final receiver prespecifies the polynomial route. It does not choose the better of two separately delta/8-budgeted norm routes. The old per-action norm is replayed as part of the base record, but its probabilistic correctness is not needed for the new family proof. Even if that old quantity affected the acquisition stopping round, the retained simultaneous fresh-round bounds still cover the chosen round.

I also checked the optional finite-six-round joint calculation: column failure can be bounded by delta/16 using its actual one-sided schedule; the coarse/pilot and two new norm events each use delta/8; each of the two round families uses at most (delta/4)*(6/7). The total is 111 delta/112. That optional result requires the stated schedules and six-round cap and is not needed by the final prespecified polynomial receiver.

Confidence remains an unconditional false-admission guarantee, not a posterior guarantee for every admitted transcript or rare PASS. Fixed-before-validation row/support/sample schedules, genuinely fresh source calls and independent uniform probes are external premises. Checking stored arithmetic or a seed does not authenticate them.

## 4. Uniform values, new tasks and regret

The earlier mixed-norm proof applies to this newly certified family because all actual selected-row operators are stochastic. Full trajectories are sup-norm bounded even without a common stationary law or a global L2 contraction. With incoming e, outgoing f, complement alpha and coarse row error d,

    t_0=0, t_(j+1)=min(1,alpha*t_j+e),
    E=||ell||_1 ||b||_infinity [L*d+f*sum_(j<L)t_j].

This is simultaneous for all time-dependent block-Markov policies, including policies chosen from the acquired data. It also holds for every block-constant b with bounded sup norm and block-uniform probability initial law, without a new statistical union: the controlled operator event does not depend on those choices. Reading/checking a new microscopic task is still O(n), or O(r) for a task explicitly supplied over the acquired blocks.

Ordinary coarse Bellman DP maximizes the value over the stated class. The uniform value sandwich proves regret at most 2E relative to the optimal TRUE policy in that class. This remains valid even though the true aggregated state process need not itself be Markov: every candidate policy is still a well-defined microscopic row-selected product, and all such products have the value bound. There is no claim of optimality against microscopic or arbitrary-history policies.

The DP uses the exact lcm of empirical row denominators and integer values with denominator D^t. Comparisons and tie-breaking are exact. The returned rational interval, not the display float, is the numerical certificate. The polynomial E, rather than the slightly smaller historical enumeration E, is used by the final receiver.

The compatible-goal consumer is correctly labeled conditional on a received event. It is not a second certificate verifier. It executes all 16 indicator-goal DPs, covers 64 initial-block tasks, and pays their 12,288 planning products. Its floating full-world evaluations are posthoc diagnostics only. Uniform sampling from a block needs membership lists or actual rejection through the retained map; expected four draws here is a fixture property, not a free general sampler.

## 5. Receiving repair and external task binding

The initial plan_feedback.main was a trusted-generation diagnostic: it checked a norm-result hash/policy list but consumed scalar norm/error fields. I flagged that this was not full independent receiving. The author preserved that history and added replay_polynomial_feedback.py rather than promoting the old checks.

The final receiver binds externally supplied task vectors, horizon, tolerance, confidence and action count, as well as exact base-result bytes/hash. Its fixture run pins the base and observations independently. It calls the previously reviewed repaired base replay, reconstructs every local count matrix, checks actual totals/dimensions/labels, replays each stored probe and rounding ledger, rescales the norms, recomputes U, alpha, incoming/outgoing quantities and E, and reruns exact DP. It verifies actual packed map, policy and original task-mask bytes.

The count/probe algebra does not certify iid provenance. The callable API is typed, assertions must remain enabled, and malformed arbitrary JSON is not the advertised security contract. Historical artifact fields used only for cumulative work reporting are not new admission evidence. New goals consume a verified certificate under this contract; they do not independently validate it.

## 6. Independent executions

The following were actually executed without rewriting frozen author results:

- 214 supplied exact small-case algebra/DP checks.
- 59 additional independent exact checks with m=3, three unequal blocks of sizes 1,2,3: all 27 one-step policies satisfy block comparison/incoming bounds, and five Bellman stages match a separate rational recurrence.
- All 32 block norm computations regenerated; every non-timing field matched the saved artifact exactly, including 146,865,304 sparse integer products.
- All 16 historical explicit-policy norm computations regenerated; every non-timing field matched, including 1,174,922,432 products.
- Historical exact planner regenerated in a temporary output directory: all four packed files and all non-timing result fields matched, including its 51 independent Bellman checks.
- Final polynomial receiver run: 9,806 exact checks and 12 adversarial preflight rejections; exact non-timing result match.
- Fourteen additional positive/negative receiver checks after the genuine full replay: rejected corrupted comparison matrix, alpha, E, product ledger, status, local total, local norm/scalar fields, altered probe, and corruption of each packed interface file. These negative tests cache only exact previously replayed operator/probe inputs and the unchanged base, rather than recomputing hundreds of millions of products each time. This limited acceleration is explicit in REVIEWER_RECEIVING_PROBES.py.
- Seven exact sufficient-comparison failure checks; full result match.
- 833 compatible-goal checks; full non-timing result match.

## 7. Actual outcome and paid resources

The final polynomial error is approximately 0.014402306334221847 at requested epsilon .02, with alpha approximately .8802806861. Its within-class regret bound is twice that error. The original-task coarse optimum is approximately .6244843518542954. The .6244814231890704 true-world value is a floating diagnostic, not an acquired input or a certified exact-world calculation.

The retained experiment charges 3,298,951,680 represented source calls. Aggregate multinomial simulation is not individual execution of billions of calls. Original norm work is 132,498,046 products; historical exponential-family work adds 1,174,922,432; polynomial block work adds 146,865,304. Cumulative norm products are 1,454,285,782, with no refund for the discarded route. The current receiving replay accounts for 279,363,350 such products. These are not complete gate, bit-operation or wall-time bounds.

The original Bellman computation uses 768 scalar products with a 669-bit peak accumulator and D=240,000,000. The retained map/policy/task masks occupy 2060 packed bytes beyond the 468-byte model, count/certificate data and metadata. A rollout pays its microscopic state-label register, 24 ordinary source transitions and map/action lookups. A physical block sensor, hidden-state estimator, actuator, physical model calibration or deployment is not acquired by an offline simulator policy.

## 8. Strong ordinary comparison and stopping scope

Ordinary reduced-MDP Bellman planning given the same acquired certificate and retained observations obtains exactly this planning capability. The block comparison inequality is established matrix analysis, not a newly discovered norm principle. I directly opened Feingold--Varga's primary paper and checked its block norm setup and nonsingularity proof context; it is a relevant ingredient, not a theorem-level identity with this entire statistical receiver:
https://msp.org/pjm/1962/12-4/pjm-v12-n4-p08-s.pdf .

I directly checked Theorem 8 of Diakonikolas--Gouleakis--Peebles--Price: bounded-L2 two-sample closeness testing already has the square-root-domain rate used in the author's elementary leakage reductions:
https://arxiv.org/pdf/1611.03579 .
The outgoing relabelling and incoming joint-law reductions have the stated scaling. For unequal blocks the incoming condition is a sufficient stronger L2 admission, not an equivalence of all weighted proximity regimes. Within-block relabelling and sampling costs remain paid. This does not transfer a generic tolerant-TV guarantee or prove a new testing exponent.

No denied publisher source was retried. No novelty, minimax optimality, end-to-end practical advantage or superiority over equally informed adaptive/variance-aware/model-reduction competitors is established. Conversely, ordinary methods being able to consume the derived uniform certificate does not invalidate the certificate. The completed result is the scoped acquired feedback guarantee and its actual exact receiving implementation.

## Appendix: final byte binding

### files

- `two_rate_operator_acquisition_20261031/feedback_extension/README.md`: `5a2b13d127d4899572e52b37655acb97c2e26d6eba163a180cc98c5375e1497d` (6349 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/SCOPE.md`: `884fb59804082687ce5ce24fe992104710ce42f5996d9a3b567ef73a14cbd9b3` (1761 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/PROOF.md`: `8c21b1a7103145b6f86257b0144d201657a41bdcdada68fdecea6cc7532257da` (11731 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/BLOCK_COMPARISON_PROOF.md`: `7fcb83a9dd8dbec482a46071eb0925f9e51a2e8c1d34f1eef8f8175e642e93f8` (3356 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/PRIOR_MATCH_AND_COSTS.md`: `2ba683e3745f012d924a3a38ee29230f66d73a5382c62e1935435aa7515210c1` (6837 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/check_feedback_norms.py`: `dff17d890645960b306e87901a5c2063d6464d82373aabb0207af43a9dedbf73` (3269 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/feedback_norm_results.json`: `434c3652eaf84fc34ae24daeb65ff9bdd9b4b70e67bffec3e1f0fb78d60f4223` (1176918 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/plan_feedback.py`: `57449bf5297ed37f2569d622f7228def6c4437f03b40602933f7d4a9cd83bb3b` (7098 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/feedback_plan_results.json`: `99e94213bea7ad9e231632ac8aa845fb064468ad8f3c246829f733b45946b2d0` (18940 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/check_block_comparison.py`: `59c071731dadaa6e827d78c261df5be7b2ef00eecea3d36ee5cd4a6223793b4c` (4328 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/block_comparison_results.json`: `23a652acfe88b99d040d229fc29a26a5b310dfa1a9d0c8f806dbe6867e4c63e5` (1214994 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/replay_polynomial_feedback.py`: `444feb3c9906f7a195a7e877b36729907e1bafb14e00f776341e0571c45e1403` (11645 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/polynomial_feedback_received.json`: `0d9894fe538333d87b66147075e2f69201fee135b9361ef8a65be0d5e17ee98f` (18420 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/check_feedback_algebra.py`: `0f7ab6c4c0df342fe2c04e2aa4d7557bb7dd97d13940b8e15fa6badd9ed9ae6b` (3765 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/feedback_algebra_checks.json`: `faa9fc87565e9968299bafb6a2fa3697f3d1f9203e5aa4fe0df0005bafc02d07` (504 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/check_comparison_failure.py`: `e93e780cb8dc35950f4adc338d067b4c4fa11d98ca04f7b388f74d2adefb91ac` (2332 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/comparison_failure_checks.json`: `0560be913335c619ff6661e5be61dd909ad45377fd822204abcad0f44c80ae0e` (1744 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/compatible_goals.py`: `ed0ca5413d54a87a93921f7a70ea910391b7432fc8a9ec2f4bf5dea85246da01` (5270 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/compatible_goals_results.json`: `7c4adefb54888148eea0a74982aae9c88193e8aeb15e3a0fa9672b0c91a0120a` (338266 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/block_map.bin`: `74dd76b2c8ee99675ec9d2be7338bdbd291a561a51dffdd7437672480caf28f0` (1024 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/policy_by_remaining_steps.bin`: `a4c75b6f12cf42dd86778be6159587407a2192eb6e994b2f7c24333a6e4eaa74` (12 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/initial_support.bin`: `d5122528f63d351f3c9ef3202874aa5fb85fa5e4537bdd55edd11f69189464d3` (512 bytes).
- `two_rate_operator_acquisition_20261031/feedback_extension/terminal_indicator.bin`: `d4a6c99f11f36947930b987eff2cf7916c8ecb244595a58bad8c0b33e6a515e6` (512 bytes).
### dependencies

- `two_rate_operator_acquisition_20261031/LARGE_AMBIENT_MIXED_CERTIFICATE.md`: `229a17b7d8a661f610fb44b09b8749edbb5445ebd5f98b54e2f4fb3ca8cb1c67` (8575 bytes).
- `two_rate_operator_acquisition_20261031/QUADRATIC_LEAKAGE_VALIDATION.md`: `2dc65ccac348218e974247554fb07fb01fa4f8cff5f1f7790683c87cfcb8e964` (8752 bytes).
- `two_rate_operator_acquisition_20261031/MATRIX_CONCENTRATION_ACQUISITION.md`: `9f6c83b88a2d604841f733a95245f39b9dfdbc6593225ea8ed61936828724d8b` (9397 bytes).
- `two_rate_operator_acquisition_20261031/LARGE_PRIOR_AND_LIMITS.md`: `2a8f742d46fc19d61ce9dd142432f38c22a695e3c497ffd34ccae4562ffda17d` (7042 bytes).
- `two_rate_operator_acquisition_20261031/retained_large_acquisition.py`: `75659fc54671083d3b4cdfec6567bb3d8ef5d7f745e2396d9cdf36373897b260` (13023 bytes).
- `two_rate_operator_acquisition_20261031/check_retained_large_acquisition.py`: `c159e83e3444062d68e6a1b47f2c35f6514e586ed11dd2c0ade37442c99cb220` (11519 bytes).
- `two_rate_operator_acquisition_20261031/large_routing_source.py`: `68cb5c46258d5d3434fa1938cc5c4cb9f2feb8390f4668a85cac8359f50144db` (7776 bytes).
- `two_rate_operator_acquisition_20261031/quadratic_leakage.py`: `a43284985190605f3ce90e582f7a7d4790f1df9a2764032b02f79644a59513cb` (5745 bytes).
- `two_rate_operator_acquisition_20261031/sparse_norm_probe.py`: `be7363f76e547e51d94f9756819397d1f066ac1a88ed319fcc3244eb194153fb` (6336 bytes).
- `two_rate_operator_acquisition_20261031/history_sensitive_4096_result.json`: `dc7583f0aa94e06f7440a6109a2dbef128b1db35538664a1880f8a5c4c146568` (358363 bytes).
- `two_rate_operator_acquisition_20261031/history_sensitive_4096_observations.json.gz`: `f9ec8eedc6465e9b552f48fdbe15f9f6e3e7ca9e2f78553e4d954d6b697fdd85` (4167029 bytes).
- `two_rate_operator_acquisition_20261031/LARGE_REVIEW_FREEZE_MANIFEST_20261031_1824UTC.json`: `e0e3c8a2f521b1dddc09ab6b28382961f569dfb0cf2c65a12d6e7cf959253e1d` (7287 bytes).
- `two_rate_operator_acquisition_20261031/RETAINED_LARGE_INDEPENDENT_REVIEW.md`: `70f5f843fd22034bb60d85ae2bb1bf75cfecb9c1c8d12867c102484e365ae9ca` (20282 bytes).
- `robust_operator_reuse_20261031/finite_observation/robust_replay.py`: `78ecc56dded4dac4df6e5dc60cd298893226a2a28d5e098fc09b5271ba35b2c8` (15084 bytes).
- `robust_operator_reuse_20261031/learn.py`: `e274c04f20d81e478c033d606bfe9dd886a9a3f049a971e216575bb8c75b98ce` (8363 bytes).
- `robust_operator_reuse_20261031/verify.py`: `ed8dc7773c8728ce9d3a7432187684ce74be89c86e4533584f8c02483af61867` (3469 bytes).
