# Independent rank-monotone forcing and integrated-transfer review

30 October 2026. This review separately challenges the root forcing lemma, raw affine decomposition, rank finder and whole transfer. Prior integrated acceptance is used only for its explicitly unchanged interfaces.

## Verdict and frozen scope

**Accept the rank-monotone forcing lemma, the restricted maximal-affine/rank finder, and the completed integrated whole transfer.** No false-positive rate split, rank certificate or boundary/clock counterexample was found under the retained hypotheses.

Five new frozen sources are copied to `rank_sources/` and identified in `RANK_SOURCE_SHA256.txt`:

- root lemma: 90e8b9d35918a062dabf70e1fb071b27b2b176ab92bad28191e8825cb9226b34;
- raw split/transfer: ce95b39d3ae87c02a441fa47e4d935d530bd941ae62a70afa017823aa63b994f;
- finder: 19e958f46e1a580438154ce2094e8cb3909c8d94fe38f9e187d98249e28ab531;
- output: 03a8370f8dbabe7757cb555c9717dc998d0292092257f9c97cc56e50bb6b1d78;
- raw inputs: 66d0687587dc34cbe423f3f09167e00f07224281ffa296e5348fcb5b124042e2.

The phase-type finder and completed carried/face-potential foundations remain dependencies. The new conclusion is a sufficient restricted recurrence/exponential-moment transfer, not general recurrence, unrestricted completeness, efficient synthesis, or novelty. Population resets remain positive-D-start only.

## 1. Progress clocks really withstand adapted equal-rank motion

For each non-a type choose one strict-lower baseline edge with rate at least q_min. A rate-q_min potential progress clock selects that edge from the label's CURRENT type; at a it is a no-op. Subtract that rate from the chosen edge and use an independent residual potential clock at rate Q_max, with thinning/no-ops, for the remaining baseline rates. At a subtract nothing. Since Q_max bounds every original baseline row sum, all residual probabilities are nonnegative and total at most one. The observable baseline generator is exact.

On at least L progress rings and no residual rings, each non-a progress event lowers the integer rank by at least one. Adapted extras may move the label around its current rank or lower it, but cannot undo progress or move it out of a. Thus the event succeeds from ANY starting type. It is not the invalid assertion that a fixed preselected physical path survives an equal-rank extra.

The potential clocks are independent across labels, yielding the stated explicit probability at least exp(-(Q_max+q_min)t)(q_min t)^L/L!. Actual label histories may be correlated through arbitrary adapted extras. The argument uses a deterministic forcing event sufficient for success, not independence of those histories or of survival-conditioned particles. Fixed-population finite-state bounds prevent extra-jump accumulation in the intended stopped process.

An initial-a tag stays at a on no residual rings; extras cannot leave the unique rank-zero type. For later times, a last-unit forcing interval works regardless of the adapted starting types. Seed-deleted tags may be continued fictitiously with the same baseline clocks and no extras; at most two deletions per mark are paid separately. The downward reference crossing intensity is bounded by the original cohort size times Q_max. These facts recover the exact concentration/retention interfaces required by the stopped-module proof.

## 2. Rank acquisition: sound and complete for its stated graph criterion

Every added layer has a baseline edge to a prior layer. Pruning ensures every excess successor lies in a previous or the same layer. Returned ranks therefore have strict baseline progress and nonincreasing extras. Excess leaving a is correctly rejected.

For completeness, take any valid integer ranking and compress unused levels. Inductively, by the end of algorithm round k all vertices of valid rank at most k have been included. Each still-unprocessed rank-k vertex has a baseline edge to a processed lower rank, so is eligible. Its excess successors have rank at most k; they are already processed or are in that same valid layer, which is an eligible subset closed under pruning. Such vertices cannot be removed. Consequently the algorithm cannot terminate with empty candidates while a valid ranking exists. This is an all-size argument, not a finite-test extrapolation.

The code computes q_min as the minimum, over non-a nodes, of their largest strict-lower edge rate. Choosing a maximizing edge at each node realizes the single-edge split above. Q_max is the maximum ORIGINAL baseline row sum, which is conservative for the residual clock. The reported L is the maximum acquired rank, not an unjustified shortest-path exponent.

## 3. Maximal affine splitting is exact

For each unit pooled transfer, the raw binary source gives an affine divided rate. In the positive-D coordinates D=1+u_D, the code checks every variable coefficient and the shifted constant. Subtracting qY_i with q=min_{h in pool i} c_h leaves nonnegative coefficients. For a protected source pool, the added constant q cancels the subtraction from the D coefficient after substitution, so the shifted constant remains c0+c_D. For a nonprotected source it remains that same constant without any offset. The implementation rechecks the remainder rather than merely trusting this algebra.

Every nonzero affine remainder is inserted into the possible excess graph, including rates vanishing on some populations. Detection is in the full positive-D orthant, not from a sampled state set. The extracted q is maximal in this coefficientwise cone. Reducing it cannot add a baseline edge or eliminate an excess constraint; it can only lose a baseline or introduce extra remainder. Therefore maximal splitting loses no rank certificate within this cone and fixed partition. This is not completeness for alternative nonlinear/weighted decompositions.

Baseline or excess moves at Y_i>0 are assigned to abstract source-pool labels, with actual physical channels selected proportionately to their available rates. All grouped channels have the same pooled unit change, so this preserves the observable generator; within-pool physical identities can be reassigned. Physical-species chain independence is not asserted.

An empty ordinary pool has no enabled unit outgoing reaction. At Y_D=0 the protected pool has one physical D particle; a possible excess that consumes it reaches D=0 with zero physical mass in that pool. Pool-neutral restoration cannot recreate D. In the acquired phase-type branch, every transient face species lies in the D pool by its path to D and neutrality, so all face sources are disabled; the one-hold branch has the analogous source obstruction. This is true F and the actual terminal guard applies before any nonexistent label is assigned. The rank argument is never continued through a negative pooled coordinate.

## 4. Local estimates do not hide an a-directed-excess assumption

The new forcing event supplies c t^L low-arrival probabilities and uniform last-unit target occupation just as required by the previous local proof. Extra non-a transfers cannot create new a departures because a has rank zero and is a singleton pool. Thus high-a reference crossings still come only from residual baseline departures and separately counted seed deletions. The predictable true-F compensator, not the rank, continues to pay terminal rewards.

Polynomial episode moments are earned independently by a strict-rank baseline word. A selected label has a required positive baseline jump rate bounded below; all physical totals remain O(n^2). A face interruption is completed by restoration or clearing within the earned bounded face block with fixed positive probability; seeds may be counted as trial failures. The finite word gives the same polynomial fixed-time-block success estimate. No concentration argument is used to assume its own horizon moment.

All trace/face-potential and direct true-F ingress checks are recomputed on the actual input, including any new excess reactions. Hidden face moves must STILL be pooled-neutral. They pause the D-clock without changing label ranks. Neither rank-monotone hidden motion nor arbitrary adverse face dynamics is licensed. The physical common factor and bounded ingress A shifts are unchanged, so no operational/physical clock substitution is added.

## 5. Whole-transfer audit

A diff against the accepted integrated implementation shows the substantive replacement is the positive-D rate split/rank check. Raw connector recognition, conservative binary offset, seed/pivot requirements, a-born edge, active true-F outputs, linear true-F hazard, summed trace potential comparison, phase-face acquisition and physical weak reversibility remain checked.

The changed local forcing/retention interfaces are sufficient for the same reset/time/occupation exponents with L=max rank, all finite grades, actual profile transport, same-episode good-input ratios and weighted true-F rarity. No full independence of pooled histories is imported.

The non-small launch Green still uses the exact projected A/B path with evolving hidden metadata, not a false diagonal-fiber claim. Its restoring exit envelope is unchanged. The carried processor must still use the connector-mediated low-output/head bridge and post-launch bad-row bound from the completed receipt; small true-F return alone is insufficient. Rank forcing supplies their local R inputs but does not replace those operator constructions.

After that processor is earned, connector degree identities, complete positive source, actual finite negative word, actual-output bad-block domination, activity preservation, bounded-face B-clock, and physical stopped-value/Foster patch are unchanged. All fast reactions still conserve total count; weak reversibility still supplies closed classes. Thus the restricted whole conclusion follows from verified changed interfaces plus the completed retained foundations, not from a rank graph in isolation.

## 6. Independent adversarial implementation checks

`test_rank_challenge.py` compares the new rank finder with brute-force rank assignments on ALL 4,112 directed baseline/excess graph pairs for two and three types, plus2,000 seeded random four-type graphs with rational baseline rates. All6,112 comparisons agree. These tests support the code, while Section2 supplies completeness for arbitrary size.

The same script independently runs BOTH old and new raw finders on the corrected frozen networks:

- old multi-step: accepted by both;
- corrected rank-extra input: rejected by the old finder, accepted by the new one with X rank1 and C plus the E/F/D pool rank2, q_min=1 and Q_max=3;
- removing C-to-X: rejected by both.

The corrected input uses existing species and a genuinely equal-rank non-a excess. Without C-to-X, C's progress requires rank(C)>rank(pool), whereas pool-to-C excess requires rank(C)<=rank(pool), giving the stated obstruction for that decomposition; the executable also searches the other pool partitions before rejecting.

The failed earlier C-to-a distinction is NOT evidence of new coverage: coarsening allowed the old finder to accept it. That preserved failed example/overclaim is explicitly excluded from this receipt. The successful corrected old-versus-new comparison was reproduced rather than trusted from its filename or description.

## Limits

Completeness applies only to the given finite rank criterion and maximal coefficientwise affine cone for a selected partition. It is not completeness for stable controlled chains, chemical recurrence, weighted pools or arbitrary face dynamics. A rejection is not evidence of transience. All source bytes and earlier accepted implementations remain unchanged; no prohibited source or external/physical action was used.
