# Independent whole review: jointly tagged acquisition and population receiving

## Verdict, read scope and binding

**PASS within the declared statistical, software-source and task interfaces.** No source correction was required. I read both tagged proofs (`PROOF.md`, `GENERATIVE_JOIN.md`), all current joint-generation/receiving/check modules, the entire population proof/implementation/checker, and their relevant inherited sampler/radius interfaces. I verified all 38 freeze entries before and after review and ran both full nonmutating replays. This is a new receipt, not an extension inferred from old terminal-value results.

Manifest `TAGGED_POPULATION_FREEZE_MANIFEST.json`, 11,232 bytes, SHA-256 `7a52409145f6a16f1c4f6f055f87d75a5f3313cc406c381e693602beef0409eb`.

Principal sources:

- Tagged proof `e8d73ef3b11e0081aa896168c38af6b5f541eda24ce42ee4630afd354017563e`; generative join `0f7b2af4202a0251c511613bfd71790e891e0021cf6c9525c508d6db5ebef1e9`.
- Joint source `978cfddd1a6c60304d9dc8bc06d2748a8f3d6de37dc630ea74407cfef9991bef`; generator `2df833f2eabd8787117d9073d1b55d878323edcc78946a92676d183b73c7b141`.
- Tagged receiver `c8d5633dea4e920125652c13eb13f4bdbba7a328018566f0626e3b9f9378d007`; full checker `3c6e126dedc143052b22811c841e4dc4595974ffe4224846a84c359c61187557`.
- Population proof `70cc27ef897ad5fb134b36fdb6e0d35ff5fd31085dc947a046b656047f9d584d`.
- Population implementation `f12813101b79ba65f78d1cdc5b031964f99a44f4f93ba6d8b3c76787189d6e24`; checker `12c8645c6be103d4f0342a6bf0612020a350d3405cda302bf7def45c8f0263f8`.
- New joint transcript `cfc7c620b7aa352c382b722b880531c668fdfce94b545bd35e7dfa8c83629e45`; tagged result `e26f7dc2b027699219baa6a8123d989976fe0c2283a4f577692f9b91f3c29850`.
- Population plan `7b069f1352a127407d786d6079c0453dcce4cc29b1e5ba41453bca21b31253d3`; deployment `2c0ed4efe9ff693f5b9f0ce744bf4d1af0e6d6af7aaf6d1424da35affb6a669e`; MC comparator `3d9325b47b5b4ad48ed7dab3a1bbb0006cd9e33f09d1f8b158be2264d1bc4fa8`.

Tagged-row data are genuinely NEW. Missing historical pooled row tags remain missing. Old separately normalized incoming/pooled argument laws, obsolete intermediate files, interactive/monitor prototypes and subsequent task-diversity scouting are not silently received here.

## 1. Joint source law and actual observations

Choosing a source row uniformly before an ordinary transition makes that row legitimate available metadata. Conditional on the multinomial row counts, grouping outcomes by row and then by mixture branch has exactly the sufficient-statistic law of repeated iid pooled transitions. Neighbor multinomials update pooled microscopic counts and row-to-block counts with the same counts; global destinations update both deterministically; macro/reset destinations are actually generated and update both from the same labels. This is not independent sampling of marginals. Duplicate neighbor labels are correctly accumulated by `np.add.at`.

The code checks source-row totals, every row-to-block total and equality of the pooled and tagged block marginals. The full exact tiny enumeration executes the actual helper with exhaustive ideal sampling branches and compares its entire joint-statistic law to two independent ordinary transitions, including mixed source blocks. The large full regeneration reproduces the transcript hash and all generation metadata.

The old ordinary `_row_counts` law uses the first three binary64 branch arguments and the last remaining mass. The new helper sets that remaining dyadic mass explicitly and verifies exact representability. For the pinned n=4096, degree=16, block/group sizes 1024 and reset size 2048, the relevant uniform argument laws are dyadic; old column/coarse evidence and new tagged draws therefore share the declared ordinary argument law. Old separately normalized row-block/pooled evidence is not reused for the new validation.

**Necessary executable scope qualification, confirmed by the author:** `TaggedPoolSource` nominally accepts some other n, such as 12, for which n/4 is not a power of two. Its integer-uniform macro law need not then coincide with the old floating multinomial uniform arguments. The old-evidence reuse in this receipt is ONLY for the pinned dyadic n=4096 fixture and the stated n=4 exact source test, not every constructor argument. The general probabilistic theorem is about actual joint iid forward calls, not an automatic numerical transport theorem for all n.

The N<2^52 bound makes the helper's float-weighted block-total diagnostic exact for these nonnegative integer sums; int64 counters/indices are guarded and the actual fixture is far below their limits. Counter allocation, multinomial work, macro/reset arrays and serialization remain paid. Reproducible pseudorandom seeds and count identities do not authenticate ideal iid semantics, independence, timing, or a physical source.

## 2. Statistical receiving with shared observations and unequal row totals

The column event is simultaneous over all columns/actions, so the acquired partition may depend on earlier discovery data without invalidating the pooled density bound max_j p_g(j)<=B/|g|. The inherited collision U-statistic gives the outgoing H-dual norm certificate with kappa=B*n/|g|. The stated variance inversion, outward square roots, fixed independent replicates and median tail are the previously reviewed operations; the current receiver recomputes them on the NEW pooled counts.

Fine B rows come from the same observations. Their empirical-Bernstein event need not be independent of outgoing statistics. Union bounding the events is sufficient. At a given prefix B/e use the current pooled round, while tagged empirical rows use cumulative row outcomes; the receiver correctly compares those cumulative rows to that current B, with the same uniform true block average underneath both.

For the incoming scalar, condition on prior discovery and all outcome-independent row choices/totals. Every fixed row then has its own N_i iid outcomes. Fix a true maximizer (a,i,g,S) of p_i(S)-pbar_g(S), using a deterministic tie rule, BEFORE outcomes. The maximizing subset can be unknown and need not be enumerated. This produces the scalar maximum total variation c, not simultaneous individual distribution estimates.

For any probability row B, if its largest entry is at least 1/2 then every subset mass is either at least that entry or at most its complement. Hence subset Bernoulli variance is at most bmax(1-bmax); otherwise 1/4 suffices. Since x(1-x) is 1-Lipschitz and subset deviations are bounded by TV, the computed empirical envelope min(1/4,vB+tau) bounds the fixed witness's empirical variance pointwise, even though B and tau are data dependent. Applying empirical Bernstein ONLY to the fixed true witness and replacing its denominator N_i-1 by the smaller N_min-1 gives the code's radius. The fine event supplies TV(pbar,B)<=d/2. Thus c<=tau+radius+d/2 is valid, with clipping at 1.

There is no n-row/subset union and no data-selected witness treated as fixed. The reported empirical witness is diagnostic; it is NOT the witness used in the confidence proof. N_min>=2 is checked. Outcome-dependent row allocation would break the conditional iid argument and is excluded. Conditioning used in this proof is not a posterior confidence claim after a rare PASS.

The allocations add correctly: column delta/8, outgoing over six rounds3delta/28, fine3delta/14, six incoming witnesses delta/2, total53delta/56<delta. Shared-data correlations do not require more independence. Old discovery/column events are combined unconditionally with fresh-event failures; their validity is not asserted with posterior probability1-delta after seeing a particular old archive.

## 3. Full block-record/history theorem, independently checked

For q in range(Q), PA_a q is bounded coordinatewise by e||q||_H<=e||q||_infinity. Stochastic A_a then gives ||Q A_a q||_infinity<= (1+e)||q||_infinity. For a block-constant [0,1] continuation, the difference between a true microscopic row and its uniform block-average row is bounded by c. This uses total variation rather than an unjustified global L2 contraction.

At each history-tree node, patch the separately chosen child functions on their respective blocks. Their centered residuals still concatenate to a vector in range(Q), and its sup norm is their maximum, not their sum. Because true values are in [0,1], z_next=min(1,c+(1+e)z) is valid even though 1+e exceeds1. The average error gains at most e*z plus d/2: the latter uses the zero total mass of the difference of probability rows and [0,1] test functions.

At terminal depth, any payoff of the complete observed block/action record is constant on the leaf's current block, although different histories may have different payoffs. Thus the induction applies to every [0,1] record payoff and yields full observed-record TV<=E_L. Randomized block-history policies are handled by fixing independent private randomness and averaging. Intermediate block averages are algebraic decompositions, not claims that true conditional microscopic posteriors are uniform. Only the actual INITIAL law is block-uniform. No rare-history probability division, branch-count factor or microscopic-policy upgrade is present.

A table that chooses an action separately for each current block preserves the same c,e,d, because each relevant row or block-average row comes from one action. This is an exact selector argument, not a sqrt(m) norm estimate. The resulting all-table-word marginal TV certificate is uniform on the same event and is what the population theorem consumes. A local record-TV guarantee is not an N-independent guarantee for the complete joint transcript of N workers.

## 4. Population concentration and adaptive control

The population interface adds real assumptions: independent worker initial states with the specified allowed law, fresh noises independent across workers/times and acquisition, and common finite stochastic kernels under chosen actions. These are not learned from a row sampler. The executable actually draws iid initial labels from the public support; it does not replace those draws with an exact deterministic occupancy.

On a proof-only probability space, iid uniforms implement every fixed table word through inverse CDFs. For each fixed word, N worker memberships in a block subset are iid Bernoulli. Hoeffding and TV=max_S(empirical(S)-true(S)) give the factor 2^r. There are at most (L+1)J^L prefix words, J=m^r for table broadcasts. No independence between words or subsets is required for their union.

On that common event, the actual adaptive controller's realized sequence is one of the words. Using the same worker noises, induction shows actual trajectories equal the counterfactual trajectories for that realized word, even though the word depends on observed occupancies. This is an analysis coupling, not an accessible common-random-number oracle, and no counterfactual trajectories are executed by the implementation. The bound does not condition on a rare realized history.

The finite arithmetic uses .7 times an upper bound on the binary logarithm of this union cardinality/risk, so it exceeds the natural logarithm. Outward square roots give eta. The bound is TV(empirical occupancy, coarse law of realized word)<=E_t+eta, clipped at 1. Ambient n is absent from the population concentration factor, but remains fully present in source acquisition, labels, initialization and map storage.

For linear utilities, ordinary Bellman induction maximizes componentwise over all fixed table words without enumerating m^(rL). Every adaptive population controller's realized coarse word has value at most this optimum. Together with the selected policy lower bound and bounded bad-event contributions, the conservative expected regret 2*kappa*(E_L+eta)+2*delta_pop is valid on the learning event. A nonlinear utility needs an actual Lipschitz constant and an earned planner gap; no efficient nonlinear planner follows merely from small r. The stated grid/table costs are not hidden.

The shared-noise, discontinuous-threshold and product-transcript counterexamples correctly delimit the conclusion. Worker independence, a service margin, and the aggregate observable are substantive, not dispensable technicalities.

## 5. Actual implementation, external task and distinct risks

The population task digest binds horizon, action count, worker count, reward vector, threshold, confidence, deployment risk, model tolerance and source/initial/observation interface. The receiver selects B and E FROM THE SAME first admitted prefix. It does not charge an earlier prefix and use later improved operators. Rational integer Bellman arithmetic, denominators, values and tie convention are recomputed. Policy execution reverses the remaining-steps table in the correct order.

`run` receives the fixed original source task while allowing compatible new block reward vectors in the population task; the mathematical model event is uniform for those block tasks. Indicator rewards can receive service thresholds; nonindicator rewards are not mislabeled as service-count indicators. The cheap MC helper in this freeze is the fixed TASK goal, not a generic new-goal confidence service.

The simulator follows the SAME branch argument law as joint acquisition and updates every worker individually at every step, with actual block/action lookups and occupancy counts. Full replay binds saved plans and simulated trajectories, but it does not test a 1e-9 frequency empirically. Checker equality and assertions are scientific typed-API receiving, not an arbitrary adversarial-file/provenance security boundary; immutable manifests and exact task binding remain necessary.

For the frozen task, E_L=0.010973914234489705, uniform adaptive-table eta=0.006873863542750769, fixed-goal scalar eta=0.0032403703498857794. The certified fixed-policy service lower bound is 0.6103236970946206>0.6. The acquired-model adaptive-population expected regret bound is 0.03569555755448095.

**Probability distinction:** deployment risk 1e-9 is conditional on the valid learning event. Learning failure is bounded by 0.001 (more sharply 53/56 times that from the displayed allocation). The reported unconditional joint bad-event upper bound is 0.001000001, NOT 1e-9. No posterior guarantee for an arbitrary observed PASS follows. Repeated deployments require their actual extra source updates and risk union/accounting.

## 6. Strong ordinary comparator and all costs

The ordinary cheap proposal uses only retained discovery counts and obtains the SAME exact policy table. Equality is checked before sharing evaluation conclusions; the cheap method does not require buying the expensive certificate to propose that table. A fresh 250,000-worker single-policy evaluation uses 6,000,000 actual transitions. Its resulting population service lower bound is 0.6163289517475794 and passes the same 0.6 threshold.

Its prospective acquisition/evaluation cost is **37,588,352** calls, versus **2,535,588,352** for the reusable model certificate at the .02 request. This is an important ordinary win for the fixed one-goal feasibility question. It is not automatically an all-adaptive-feedback regret certificate or a reusable full-record model. Conversely, the reusable model's broader scope cannot be used to hide this cheaper success on the concrete goal. Actual future diversity would have to justify amortization; none is inferred here.

All three new acquisition rounds were actually generated: 2,504,000,000 represented logical calls, in addition to the original 3,298,951,680 old calls and norm work. First-prefix prospective stopping does not refund later saved work. New joint generation actually produced 100,186,909 macro/reset destination labels, while local multinomial compression represented the dominant other calls. Extra metadata requires 40,960 streaming counters (327,680 nominal uint64 bytes before runtime overhead); the compressed joint transcript is 3,830,533 bytes. The retained transcript, exact arithmetic, source wiring and simulator arrays are additional. No historical tags are reconstructed.

The population run executes 24,000,000 worker updates plus 1,000,000 iid initial draws; the cheap evaluation adds 6,000,000 updates. Source/map/action lookups and 25,000,000 occupancy-count contributions in the main deployment are paid. The declared largest categorical-array bytes are NOT peak process memory. Bellman costs 768 scalar products for the main linear task, with actual integer-bit growth; this does not represent total acquisition or deployment cost.

## 7. Executed review evidence and primary comparator

The following were run nonmutating and reproduced all expected non-timing results:

- `check_tagged.run`: 354,127 exact checks and 12 refusals, three receiving runs and full regeneration of 100,186,909 macro/reset labels.
- `check_population.run`: 354,895 exact checks and 12 refusals, full regeneration of 30,000,000 worker updates, including the cheap same-policy comparator.
- Reviewer `extra_checks.py`: 1,792 exact independent tests of arbitrary subset variance envelopes and COMPLETE block-history-record total variation under unequal blocks, unrelated child-history actions and rational microscopic kernels.
- Nine additional task/type substitutions refused.

These fixtures support the implementation and detect regressions; the confidence statements still depend on authentic sampling/freshness premises. Replaying seeded data is not new independent evidence.

I opened the primary Gast–Gaujal paper https://arxiv.org/pdf/0903.2352, including its independent-particle controlled model and finite-horizon mean-field optimization scope. It is a strong ordinary prior for the population-control headline. Standard empirical Bernstein, collision statistics, projection bounds, Bellman planning and Hoeffding concentration also remain credited. This receipt accepts the concrete acquired-model/full-record/population conjunction, not a historical novelty or practical advantage claim. Later scouting, tagged-population variants and physical-sensor claims remain outside the freeze.
