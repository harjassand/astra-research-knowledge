# Independent review of the paid coarse switching cover

## Verdict and exact scope

The acquisition, selected-prefix statistics, finite-cover certificate and complete resource ledger in `core/coarse_switching_cover.py` pass this scoped review. The finite tree gives an absolute survival error at most 1/16 for every switching word on its simultaneous confidence event. It uses chosen controls, fresh preparations and coarse alive/absorbed reports; no microscopic state label is supplied to inference.

An independent replay verified the 168 confidence endpoints used by the selected 84 nodes, all 32 pure-curve upper endpoints, every potential-prefix denominator and count partition, finite-tree completeness and the exact resource totals. It generated **no trajectories**. The general weak-Poincare implication from pure repetition curves to switching tails is assigned to the scalar branch; this review checks its saved statistical inputs and recurrence arithmetic, not that general lemma.

## Why balanced prefix counts are binomial

The control design is fixed before the corresponding trajectories: each of the 2^10 length-10 binary tapes receives 512 independent fresh preparations. Consequently each fixed length-h prefix w has exactly

\[
N_w=512\,2^{10-h}=524288/2^h
\]

assigned trials. The initial hidden-state distribution is identical for all tapes. Assignment does not inspect the prepared microstate or slow level.

For every assigned trial, the first h controls are exactly w. Under causal dynamics, the future tape suffix cannot affect survival through that prefix. Thus the survival indicators for this fixed prefix are independent Bernoulli variables with common mean f(w), and their sum is binomial with denominator N_w.

The denominator is **all assigned trials**, not the number alive at the parent. A trajectory that died earlier contributes zero to each longer prefix on its already assigned tape. The implementation obtains the same unconditional count by grouping the remaining active trajectories while retaining N_w as the denominator. It never refreshes a hidden state after a coarse live report.

Counts for different prefixes share trajectories and are dependent. No independence between prefix counts is used. There are exactly

\[
\sum_{h=1}^{10}2^h=2046
\]

potential prefix intervals. A union bound over both endpoints at every potential node permits subsequent data-dependent selection and pruning. Charging only the 84 selected intervals would not justify the same adaptive-selection argument; the executable charges all 2,046 potential intervals.

## Confidence allocation and exact numerical acceptance

The pure experiments use 8,192 independent preparations for each of the two operations, monitored through a fixed cap of 32 steps. The even times 2m, m=1,...,16, give 32 predeclared one-sided upper bounds with exponent 12. Selection of m after those observations is covered by their simultaneous event.

The balanced tapes use two-sided intervals with exponent 18 at each potential prefix. The combined failure bound is

\[
32e^{-12}+2(2046)e^{-18}<0.001.
\]

The exact rational bound used by the executable, and independently replayed, has floating diagnostic approximately 0.0002589358724. Dependence between times within a pure trajectory and dependence between tree nodes do not affect this union calculation.

The interval routine proposes endpoints numerically but accepts them only through an exact rational Bernoulli-KL lower enclosure. The independent replay checks all 200 actually used endpoints with a separate rational logarithm enclosure, including their direction relative to the empirical proportions. It does not rely on floating-point confidence diagnostics.

The selected pure-curve input is m=4 and

\[
s=19749452843/500000000000\approx0.039498905686.
\]

The replay verifies every candidate and the selected recurrence

\[
z_0=1,\qquad z_{h+1}=s+\frac{m-1}{m}(z_h-s).
\]

It first reaches the target by the selected half-length h=13, giving the saved length-26 switching-tail conclusion conditional on the separately reviewed general lemma. No hidden source value enters this selection.

## Why the finite tree covers all future words

The selected tree contains both one-letter roots. Each branch node has both children; each terminal node has no selected descendant. The independent replay verifies these properties, the absence of unresolved branches, the exact parent-child relationships and the recorded maximum depth of seven. There are 41 branch nodes and 43 terminal nodes, as required for a full binary forest with two roots.

At an exact branch word, the output is its interval midpoint and the half-width is at most 1/16. At a terminal prefix, its survival upper bound is at most 1/16, and the predictor returns zero for that prefix and every extension.

Irreversible absorption makes total survival nonincreasing along every extension of a fixed control prefix: appending operations cannot revive an absorbed trajectory. Therefore a terminal prefix's upper bound also bounds every longer word that begins with it. Every word either ends at a branch node or reaches a terminal prefix within seven symbols. The empty word has survival one exactly. This proves the all-word absolute-error guarantee on the simultaneous confidence event.

The finite-cover proof itself needs absorbing-event monotonicity and valid prefix intervals. It does not use the private source's rank, rates, slow-level weights or the pure-curve tail lemma. The separately paid pure curves support the broader termination argument; their costs remain included rather than being dropped because the observed finite tree terminates earlier.

## Source isolation and full costs

Code inspection confirms that the microscopic state and slow-level variables stay inside the simulator. The initial tape assignment is deterministic and independent of the source preparation. Hidden activation variables implement the declared source dynamics; they do not select which tape, length or confidence rule the learner uses.

As an executable isolation check, the replay disabled the source constructor and private truth-check functions, then reproduced `infer_cover` from only the tree depth and observable prefix counts. Its output is identical to the saved cover. The private finite-level source enclosure is a post-inference check and is not an input to the statistical certificate.

Every active trajectory incurs one primitive application and one coarse report at each executed step. Absorbed trajectories need no later physical application, but remain statistical zeros in their assigned prefix groups. The recorded step total is the sum of alive counts before each step. All preparations are fresh; no coarse label is treated as a hidden-state reset.

| Paid acquisition | Applications | Coarse reports | Fresh preparations |
|---|---:|---:|---:|
| Pure operation 0 | 20,119 | 20,119 | 8,192 |
| Pure operation 1 | 14,237 | 14,237 | 8,192 |
| Balanced depth-10 tapes | 1,051,824 | 1,051,824 | 524,288 |
| Complete total | **1,086,180** | **1,086,180** | **540,672** |

The replay verifies all pure and balanced survival-count sums, all prefix assignment counts, child-survival consistency, and every entry in this ledger. The result is an executed integer-RNG software acquisition, not a hardware calibration. Fresh preparation of the declared distribution and truthful nonintrusive alive/absorbed reports remain interface premises.

## Preserved review

The independent checker is `replay_coarse_switching_cover_review.py`, with saved output `COARSE_SWITCHING_COVER_REVIEW_RESULTS.json` in this directory.

Reviewed result SHA256:

`2431a4c2da4f7b17e24d96dfbe3613e657f7f2c731dd078bf7876093e0ee4a57`

Reviewed compiler SHA256:

`5386bb40ac6e837238721c2e2f2dfa5622998bf214a1f3fc527672368045baca`

Reviewed raw-receipt SHA256:

`4e24b5694e20f0ff47dbf0a2bae2f462a2276f13c3a2807e40be3ac82ef0b7e8`
