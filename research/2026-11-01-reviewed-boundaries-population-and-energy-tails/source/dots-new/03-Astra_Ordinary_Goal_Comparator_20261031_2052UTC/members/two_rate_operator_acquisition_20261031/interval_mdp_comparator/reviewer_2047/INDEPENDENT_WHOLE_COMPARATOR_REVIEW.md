# Independent whole review: ordinary fixed-goal hazard / interval-MDP comparator

## Verdict and immutable binding

**PASS, scoped to this fixed task, ideal sampling interface and full receiving operation.** This is an ordinary comparator win against the earlier sufficient acquisition ledger, not a new learner or a retrospective invalidation of the earlier wider operator certificate. I read the whole proof, README, current generation, hazard, transport and full-check code; inspected the relevant inherited radius/sample-schedule/source implementation; verified the freeze; and executed nonmutating full receiving. No correction was required. This uniquely named reviewer directory does not replace author files or previous receipts.

Manifest `COMPARATOR_FREEZE_MANIFEST.json`: 7,577 bytes, SHA-256 `b28037ae396ae394113ed2406da2c01a56cf77ee76dc473315ac7f2ee93852fc`, all 28 current/historical/dependency entries verified.

Principal current sources:

- `PROOF.md`: `6fd8b306fb65f730ea487287c94b17db467335438b558cabf256f84b9f49fb2c`.
- `interval_comparator.py`: `6fe5da96d894039fd5a783f46b75195104b2fc42a3cd66885a11f07d1362b0d0`.
- `goal_hazard.py`: `875fdb90249e032e6442c8c80d0f7c0687c089810e2005fc580f93a9c08432cb`.
- `check_comparator.py`: `d27d06bce511a3ecdfd420023cb6d0871c7bd4d6fc89c551423bb13082ebbea2`.
- `check_source_transport.py`: `a916b2b905d8918e5b7eb0919506314aa26d6c81ada0b6fa33fcd2d61551ed2b`.
- Interval result: `a328365b68a579033fa6283abba4bc0cb10a7a23db607f56c86bee32cb5e3991`.
- Hazard result: `ccfd1d05f8b985789b45f764f04693df9be86fc8d9e64c719bd45f05ceb9ff87`.
- Source transport result: `571918ca9189f6513ba9eb682faf32e7a7b71169c49bda9a94959b152a2c4f23`.

The original model and observations remain pinned to `dc7583f0aa94e06f7440a6109a2dbef128b1db35538664a1880f8a5c4c146568` and `f9ec8eedc6465e9b552f48fdbe15f9f6e3e7ca9e2f78553e4d954d6b697fdd85`. Historical untransported interval envelopes and the source-audit NumPy scalar overflow are preserved but not passing current sources.

## 1. Fixed true maximizer: why no row union is needed

Condition first on the already acquired partition and other information fixed before the pilot/incoming row samples. The public goal is fixed and is a union of these blocks. Each row/action then has a fixed observed-law goal probability p_(i,a). Choose a deterministic true maximizer (for example lexicographically resolving ties) before these row observations. The proof never needs to discover this maximizer.

For common N, the supplied radius is the empirical-Bernstein radius with Bernoulli sample variance c(N-c)/(N(N-1)). The count upper bound U_N(c) is nondecreasing: c(N-c) is increasing until N/2, outward fixed-grid square-root rounding is monotone, clipping is monotone, and the branch after N/2 is exactly one. Pointwise, for every joint count realization,

    U_N(max_(i,a) C_(i,a)) >= U_N(C_(i*,a*)).

Therefore failure of the maximum upper bound is contained in failure of the ONE fixed maximizing row's upper bound. No union over rows/actions and no independence between rows is needed for this implication. It does require each fixed row's accumulated N trials to have the declared iid Bernoulli law. It does not give simultaneous per-row intervals, work with an adaptively selected goal for free, or justify using the same monotonic comparison at unequal unadjusted sample sizes.

The fixed-prefix schedule is real: the inherited source code prescribes Nin=512*2^turn and a replicate count determined by delta/turn, not observed row values. Pilot N=2048 is fixed. Each action/row has total N=13312, 39936, 93184 at the three observed prefixes. Six possible prefix events receive delta/2 in total; overlapping observations at successive prefixes need not be independent for that union. The evaluation allocation covers the THREE implemented candidate attempts. Extending to further evaluated candidates would require a new allocation; the unused row-prefix budget alone is not free rollout confidence.

With K=(7/10)ceil(log2(2*6/(delta/2)))=21/2, K exceeds the required natural logarithm. The argument 7/10>ln 2 is valid. Counts above N/2 use the deliberately conservative upper bound one rather than extending a potentially nonmonotone expression.

## 2. Hazard and stronger comparison class

After adding the deterministic transport reserve, h bounds every target row/action's probability of entering G from outside G. For any causal microscopic-state/history-dependent randomized policy, the conditional next-step hazard before first hit is bounded by h, as a mixture of such row/action hazards. Induction gives survival at least (1-h)^L. The initial support is checked disjoint from G; terminal membership implies a previous hit even if the chain subsequently leaves/reenters. Thus every allowed policy has terminal expected reward at most H=1-(1-h)^L.

This is an upper bound against the stronger information class, not acquisition or deployment of a microscopic controller. It does not require a uniform microscopic posterior within a block. It permits arbitrary causal history use, not anticipation of future source randomness. The same broad upper bound can be loose for other tasks; no universal planner claim follows.

For a candidate table fixed before its evaluation batch, fresh independent episodes give a value lower confidence bound. The candidate may depend on all previous data; conditional freshness suffices. Three batches at delta/6 each cost at most delta/2. Combining with the prescribed hazard event gives total failure at most delta, without using any interval-envelope event. The final admitted method is the hazard/evaluation combination, not a post hoc minimum with an unbudgeted independent certificate. A rare observed PASS does not acquire posterior confidence or model truth.

## 3. Ordinary interval-MDP candidate and legitimate refusal

The simultaneous row/action/block intervals allocate their own delta/2 over all six prefixes. True block transition rows are enclosed by taking the minimum lower and maximum upper endpoints over current microscopic states, and adding the transport reserve. Intersecting with the simplex and filling remaining mass in value order solves each row extremization by the standard exchange argument. The optimistic finite-horizon induction bounds every microscopic/history policy; pessimistic induction bounds the chosen block-Markov table. Stochasticity handles arbitrary within-block posteriors, so the proof does not assume exact lumpability.

The generated table is fixed before each fresh evaluation. Reversing `policy_by_remaining_steps` during rollout is the correct remaining-horizon convention. Fresh evaluation can sharpen its lower bound. The separate interval/evaluation certificate is still about 0.06928292060187181, above the requested 0.0565: it honestly refuses. Its confidence event is not needed for the goal-hazard success, although constructing its table and all attempts remains paid.

## 4. Source-law transport: precisely what is certified

The historical `row_block_batch` supplies normalized binary64 vectors to a multinomial operation. The target rollout adapter instead samples four branches using the integer counts (95998,4000,1,1)/100000, then uniform degree-16 neighbors, 1024-state groups, or 2048-state resets. Their argument laws must not be called exactly identical.

The audit reconstructs all 8192 historical row/action probability arguments for the received partition. Each binary64 component is converted to its exact rational value, with the final category defined by remaining mass. It compares these with exact target BLOCK probabilities from the integer-branch law. The maximum L1 difference is about 1.903e-16, below eta=1e-9. Python-int conversions prevent the preserved historical scalar-overflow error.

This is a block-law audit, not a full microdestination-law identity or a PRNG correctness test. Block laws are exactly what the reused row counts and fixed union-of-blocks goal need. An L1 error eta implies goal-probability and individual block-coordinate errors at most eta (indeed a smaller TV bound is possible). This explains the outward interval reserve and h=U_N(Cmax)+eta.

Crucially, this correction is DETERMINISTIC kernel/value transport. The statistical confidence event is proved under the historical iid argument-law semantics; the inequality then transfers the resulting probability bound to the target kernel. It does not assert that the entire billions-sample historical transcript distribution is within eta of the target-data distribution. No such joint-data assertion is needed, and no unproved omission of an N*eta data-law cost is being used. Conversely, this check does not retroactively authenticate any old confidence assertion about a different source interpretation. Ideal iid argument-law sampling, partition-before-validation ordering, and fresh evaluation remain external premises.

The source-side audit may inspect private wiring to prove this interface relation. The planner and hazard estimator do not obtain that wiring or an optimal-value oracle. The coarse proposal can be arbitrary/data-derived: no correctness of its hidden grouping is required beyond the subsequently checked task compatibility and confidence events. No source transport for its hidden clustering truth is needed to make the fixed-goal hazard proof work.

## 5. Actual whole receiving and task binding

`goal_hazard.run` binds the independently fixed task digest, horizon 24, action count two, confidence 1/1000, and a positive requested regret. It checks the pinned base/count files, exact pilot and incoming coverage, per-row totals, prefix equality, goal exclusion of the initial support, exact radii, outcome lengths/hash/counts and prospective totals.

However, `goal_hazard.run` alone is NOT a complete validator of the policy/rollout relation: it consumes the interval result's evaluation metadata and stored bits. Whole acceptance here binds `check_comparator.run`. That operation regenerates the data-derived partition, interval envelopes, policies and all actual fresh transitions, compares the regenerated result with the saved full payload excluding only top-level timing, then checks the stored endpoint bits through the hazard receiver. JSON-text equality rejects bool/int and float/int substitutions in recomputed payloads. This chain binds the stored outcomes to the actual table and target adapter; a standalone endpoint count/hash check would not.

The full checker is a fixed-public-task scientific typed-API operation, assertions enabled, with unchanged pinned dependencies. It is not an unrestricted hostile-file or provenance-security service. External task changes are rejected; this is not a generic adaptive-goal frontend. The numerical request and stored regret arithmetic are rational; floats are display fields only. Known fixed mock seeds permit reproducibility but do not prove statistical independence.

## 6. Independent executions

The full nonmutating checker completed and regenerated all 18,000,000 evaluation transitions. It reproduced the saved non-timing payloads and reported:

- 17,026 exact checks and 16 negative receiving checks;
- all 8192 source argument laws audited, with 16,384 exact assertions;
- three candidate attempts, including two refusals;
- 4,608 interval Bellman scalar products across all attempts;
- maximum serialized rational component 2,052 bits.

Additional reviewer code in `reviewer_2047/extra_checks.py` executed 3,303 exact checks: monotonic count bounds for N=2 through 64, pointwise domination for arbitrary joint row counts, and full-state Bellman optima bounded by the first-hit hazard for 3/4/5-state, three-action rational chains over horizons 1 through 8. Five additional bool/float/task-digest substitutions refused. These are independent mathematical/code checks, not sampling-provenance evidence. Reviewer outputs are uniquely stored in this directory and frozen author files were not overwritten.

## 7. Result, costs, ordinary consequence

Final certified regret is 0.056432232574415674 against all admitted microscopic/history policies, slightly below the previous block-history guarantee 0.05650530389526265. The three hazard attempts give about 0.1296167091, 0.0763331303 and 0.0564322326; only the third meets 0.0565.

Prospective cost is 31,588,352 proposal/column calls + 763,363,328 pilot/incoming calls + 18,000,000 fresh rollout transitions = **812,951,680**. Both failed prefixes and their rollouts are included. The earlier actual experiment still paid 3,298,951,680 represented calls and its norm work; this comparison refunds nothing. Aggregate multinomial generation of old counts represents logical calls rather than executing them individually. Here each fresh rollout batch, and this independent replay, actually executes every transition in the vectorized source adapter.

Retained counts, 93,750 outcome bytes, 375,558-byte interval result, 9,540-byte hazard result, 4,167,029-byte conservative original compressed transcript, map/task/table storage and O(n*degree) source-side state all remain paid. Exact radii, sorting, integer arithmetic, validation and I/O are not free merely because Bellman scalar-product counts are small. This is a sufficient-budget comparison, not a lower bound on the earlier method or a claim of practical efficiency.

I freshly opened the primary Maurer–Pontil paper https://arxiv.org/pdf/0907.3740 and the Givan–Leach–Dean paper https://engineering.purdue.edu/~givan/papers/bmdp99.pdf. The former supplies the empirical Bernstein radius; the latter explicitly treats interval transition parameters, aggregation and optimistic/pessimistic planning. The finite-horizon and monotone-maximum arguments are supplied directly here; no invented planner or novelty claim is accepted.

This ordinary goal-specific method defeats a necessity/advantage claim for the earlier ledger ON THIS fixed task, while leaving the earlier uniform compatible-goal/operator result valid. It does not prove that goal-specific methods replace that larger reusable interface. Tagged-row, full-record, population and any later branch are expressly outside this freeze and receipt.
