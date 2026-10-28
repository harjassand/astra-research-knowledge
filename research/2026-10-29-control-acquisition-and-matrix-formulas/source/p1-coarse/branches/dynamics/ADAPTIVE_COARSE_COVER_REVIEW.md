# Scoped review of the fresh adaptive-prefix comparator

## Verdict

`core/adaptive_coarse_cover.py` passes the new acquisition, confidence-budget, queue and resource-ledger review. It executes an ordinary adaptive-prefix comparator on the same private source and coarse alive/absorbed interface, using independent fresh data and no lifetime pilot or earlier receipts.

The completed cover has 38 nodes, maximum depth five, 18 branch nodes and 20 terminal nodes. It supplies the stated all-word absolute survival error of 1/16 at failure probability at most 0.001 through the already accepted midpoint-terminal theorem. This review checks that theorem's new operational and statistical inputs; it does not re-audit the theorem or the earlier balanced-cover acquisition.

An independent exact replay verified all 38 batch budgets, every recorded node and queue decision, and all source costs. **No trajectories were generated.**

## Predictable selection and fresh confidence budgets

The queue selects the next word using only previously completed batches. Before requesting any observations for selected node j, the program fixes that word and pays a batch of

\[
N_j=\left\lceil\frac{2}{\epsilon^2}
\log\frac{2j(j+1)}{\delta}\right\rceil,
\qquad \epsilon=1/16,\quad\delta=1/1000.
\]

Every trial in this batch receives a fresh preparation. Conditional on the earlier history, the selected word is fixed and the batch's endpoint survival indicators are independent Bernoulli samples of its true survival probability. A trajectory absorbed before the word ends is a zero in the fixed denominator N_j; it is not removed from the statistic.

Conditional two-sided Hoeffding gives

\[
\Pr\{|\widehat f_j-f(w_j)|>\epsilon/2\mid\text{prior history}\}
\le 2e^{-N_j\epsilon^2/2}
\le\frac{\delta}{j(j+1)}.
\]

The selected word may vary with the earlier data; predictable selection does not invalidate this conditional statement. The deterministic allocation sums to delta over all possible j. Hence the random number of selected nodes and the data-dependent stopping of the queue are covered without a predeclared maximum node count. The reported confidence is the global delta bound; it is not obtained by substituting the observed node count into a post hoc confidence formula.

The implementation uses an upper rational enclosure of the logarithm to determine the paid batch. The independent replay uses a separate, longer rational logarithm enclosure. For all 38 receipts it verifies

\[
N_j-1 < \frac{2}{\epsilon^2}\log\frac{2j(j+1)}{\delta}\le N_j,
\]

with both sides certified by exact enclosures. Thus the actual batches meet the confidence requirement and, for these receipts, equal the true mathematical ceilings. No floating logarithm is trusted.

## Queue completeness and terminal semantics

The replay reconstructs the queue from the roots 0 and 1. Each receipt must match the next queued word. It recomputes the clipped interval centered at the observed proportion with radius epsilon/2, the terminal test U≤2epsilon, every prediction and every saved error bound.

At a branch, both children are enqueued and the saved prediction is the interval midpoint. At a terminal prefix, the saved prediction is U/2 for that prefix and every extension. This is precisely the accepted midpoint-terminal rule. The independent replay verifies that both children of every branch are present, terminal nodes have no queried children, every record is unique, and the final queue is empty. The counts satisfy terminal nodes = branch nodes + 2, as expected for the two-root full binary forest.

The completed tree therefore provides the finite covering object required by the accepted theorem. This execution does not claim that arbitrary absorbing processes always admit a finite tree for the same target. The current complete queue is an observed and verified result.

The terminal value can remain positive at arbitrarily large repetition length. That is allowed by the specified uniform absolute-error task. It does not claim an exact asymptotic absorption probability, a normalized conditional-state model, or a fitted two-state substochastic realization.

## Source information and actual costs

Inspection of `acquire()` shows that it uses only the fixed accuracy/confidence targets, prior fresh-batch counts and the selected words. It does not read the source's microscopic state, slow-level parameters, prior cover, pure curves or lifetime receipt. The imported private source code implements the simulator; its analytical probability function is used only in post-inference checking.

As an executable isolation check, the independent replay disables source construction, queries and private probability functions, then reproduces the complete `infer()` output from the new raw receipts alone.

The query loop performs one primitive and one report for every currently living trajectory at each requested step. It stops charging absorbed trajectories, while retaining them as zeros in the endpoint denominator. No coarse live label is used as a fresh preparation. For every batch, the replay verifies the full survival-count sequence and the identity

\[
\text{applications}=\text{reports}
=\sum_{t=0}^{|w|-1}\text{number alive after }t.
\]

All fresh preparation counts equal their paid N_j. The complete totals are:

| Resource | Fresh adaptive comparator | Earlier balanced pipeline |
|---|---:|---:|
| Primitive applications | **458,449** | 1,086,180 |
| Coarse alive/absorbed reports | **458,449** | 1,086,180 |
| Fresh preparations | **255,220** | 540,672 |

The earlier total includes its paid pure curves. No earlier data or pilot are used by the new acquisition. These are therefore comparable complete source-operation counts for the same declared uniform scalar-survival accuracy and confidence target on the same source/interface. The new execution uses 627,731 fewer applications and reports. This is an improvement over that specified executed pipeline, not an optimality claim or a measured hardware-time result.

The predictor's representation and terminal extrapolation differ from the separately certified two-state candidate. Its lower source cost certifies the scalar task directly; it does not independently certify that two-state model.

## Preserved review

The checker is `replay_adaptive_coarse_cover_review.py`; the saved receipt is `ADAPTIVE_COARSE_COVER_REVIEW_RESULTS.json` in this directory.

Reviewed result SHA256:

`c5c8b1ac9056f7699316a56aa85d3a96e0823d81e7c9cd71528291c4364d242a`

Reviewed raw-receipt SHA256:

`8551784f0ff21b4c19c0a585a733484968307a57aa272a61cb72ecb6603946e6`

Reviewed compiler SHA256:

`3c490983f5b9a82ad5cff00644c5e7ddf03fe42db6b000adc82dbf6b640c176a`
