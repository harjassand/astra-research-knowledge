# Exact raw rank-monotone splitting and proposed integrated transfer

30 October 2026. Candidate, not independently reviewed as a whole. Uses the root forcing lemma `ROOT_RANK_MONOTONE_COHORT.md` SHA90e8b9d35918a062dabf70e1fb071b27b2b176ab92bad28191e8825cb9226b34 and the accepted completed phase-type-face compiler. No accepted file is edited.

## 1. Extract the maximal coefficientwise baseline from raw rates

For a proposed pool partition and each unit transfer i->j, divide its actual grouped positive-D operational rate by D. Binary residual structure gives an affine rate

    lambda_ij(x)=c0+sum_h c_h x_h.

The protected coordinate is Y_i=sum_{h in pool i}x_h-1_{i contains D}. On D>=1 substitute D=1+u_D. Require c_h>=0 and c0+c_D>=0, then set

    q_ij=min_{h in pool i} c_h.

Subtract q_ij Y_i. Every variable coefficient is nonnegative, and the constant after D=1+u_D remains exactly c0+c_D, because the protected offset cancels the subtracted D coefficient. Thus the remainder is nonnegative at EVERY actual positive-D state. The implementation verifies these coefficients again rather than relying only on the formula.

A nonzero remainder contributes an edge to the POSSIBLE excess graph, even if it vanishes at some tested population. Every q_ij>0 contributes a baseline edge. A rank certificate must make every remainder edge nonincreasing and give every non-a node a strict-lower baseline edge. An uphill edge is allowed only when its remainder vanishes identically.

This q is maximal in the coefficientwise affine cone for the selected pool. Smaller q cannot remove a nonzero remainder and cannot add a missing baseline edge; it can only introduce further excess constraints. Therefore choosing this maximal q does not lose a rank certificate within this particular affine cone and pool partition. This is not completeness beyond that cone or beyond the enumerated pooling architecture.

## 2. Actual labels, including the protected boundary

At Y_i>0, split the actual grouped physical intensity into baseline q_ij Y_i and the remainder. Assign baseline/excess transfers to abstract labels currently in pool i; choose the actual physical reaction from the available channel rates and reassign within-pool physical identities as needed. All channels in the group have the same unit pooled change, so this preserves the observable physical generator. It does not assert independent physical-species paths.

For an ordinary pool Y_i=0 means no physical source particle, hence no enabled outgoing unit transfer. For the protected pool Y_D=0 means one physical protected particle remains. A nonzero outgoing excess may then consume it. If it does, the actual D=0 output has zero PHYSICAL mass in that pool; pooled-neutral face dynamics cannot restore D. In the acquired phase-type branch every transient face species is in that same pool, so no face edge is enabled; in the one-hold branch no pooled-neutral restoring source is enabled. The output is true F and the raw terminal guard applies. Stop there BEFORE assigning a nonexistent label or negative pooled count. No rank argument is used past this stop.

For every nonterminal extra jump with a real source label, its rank is nonincreasing. A has unique rank0, so extras cannot remove an a label. The progress and residual clocks in the root lemma realize the baseline exactly. The finder reports q_min as the minimum over nodes of their largest available strict-lower edge rate, so each node has a selected edge of rate at least q_min, exactly matching that lemma's single-edge split. Q_max is the maximum total baseline row rate. Both are finite fixed rationals.

Actual extra rates need not have a uniform bound in population, but for fixed total population the conservative binary module has a finite state space and finite rates. Physical nonexplosion is proved independently by the existing total-count/connector estimate. Pool-neutral face excursions pause the D-clock and do not alter label types. These facts justify the stopped label construction without an unpriced infinite jump accumulation.

## 3. Rank acquisition and its scope

The copied finder implements the root's layer/pruning algorithm. Begin at {a}; reject excess leaving a. Eligible unranked nodes have a baseline edge into the processed set. Prune any eligible node whose excess successor lies outside the processed-or-eligible union. Add the surviving set as one equal-rank layer, or reject if it is empty.

Every accepted node has a strict-lower baseline edge and nonincreasing excess successors. Completeness FOR THIS rank criterion follows because the minimum remaining layer of any valid ranking is an eligible closed subset and cannot be wholly pruned. At most the number of types minus one rounds are needed. The root's exhaustive three-type graph comparison is a separate check, not the all-size proof.

The code still checks every raw unit transfer and sums all possible extra channels. It does not infer the excess graph from finite-population observations. The entire pool partition search, true-F terminal/hazard checks, trace/face-potential obligations and physical weak-reversibility check are retained.

## 4. Local forcing consequences and the global interface

The rank forcing event uses at least L progress rings and zero residual rings in a deterministic D-clock interval; destinations are chosen from the actual current type, so an equal-rank extra cannot invalidate a fixed prechosen physical path. Its probability is at least c t^L, independently across potential label clocks BEFORE any survival conditioning. Arbitrary correlated excess histories cannot defeat this event. Initial-a retention and last-unit forcing likewise remain valid, because excess cannot leave rank0. Actual seed marks remove only the already bounded number of cohort labels.

Consequently every accepted local estimate that uses those forcing/retention interfaces has the same proof with L=max rank: low-A arrival, original-A depletion, stopped reset/time/occupation exponents, all finite profile/grade lists and good-input ratios. Polynomial absorption moments are earned independently by a finite strict-rank baseline word and the existing face restoration-or-clearing blocks. The true-F boundary and trace estimates remain separately checked; rank forcing does not supply them.

No other global interface changes. The actual launch Green (including evolving hidden metadata), restoring exit envelope, connector-mediated low-output and post-launch bad-row bounds, finite-degree processor, complete positive source, negative word, physical activity indicator, complementary B-clock and two-direction Foster comparison are the accepted completed phase-type transfer. They depend on the newly supplied forcing interfaces, not on an unrecorded assumption that every excess lands directly at a. All connector/count identities are unchanged.

Subject to independent whole review, a returned certificate therefore carries the same restricted classwise recurrence and prescribed exponential invariant-moment conclusion. A rank alone, a local matrix alone, or finite tests alone are NOT that conclusion.

## 5. Actual executable distinction

`acquire_rank_face.py` is a separate copy. It accepts the previously accepted multi-step input. The corrected regression mutation uses the ALREADY EXISTING hidden-X input, adds E+D->C+D excess and C+D->X+D baseline progress, and changes no species. The rank finder assigns X rank1 and C plus the E/F/D pool rank2. Both rank2 types have a strict lower baseline edge; the extra pooled-to-C transfer is equal-rank. Its acquired L is2.

Removing C-to-X leaves a cyclic obligation: C must be above the pooled type to use its only baseline progress, while the pooled extra to C demands C no higher. The rank finder rejects it. This is a failed rank certificate, not a recurrence/transience verdict.

The initial attempted distinction added C-to-a instead. It was NOT new coverage: the old finder absorbed the supposed excess by merging C into the hidden pool. That failed distinction, including its original overclaim, is preserved in `failed_coarsening_test/` and is explicitly superseded here. The corrected witness is compared against the old finder as well as checked by the new one; a broadened-rate test must not merely be a coarser instance of the old pooling rule.

Pool neutrality of hidden face moves is STILL required. Rank-monotone excess enlarges the positive-D rate splitting; it does not make arbitrary rank-increasing hidden face motion safe. The abstract adverse-reset obstruction saved separately remains outside this accepted interface.
