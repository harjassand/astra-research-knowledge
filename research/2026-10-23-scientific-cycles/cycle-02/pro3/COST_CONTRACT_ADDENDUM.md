# Cost-accounting strengthening after the frozen input

The original EXPERIMENT_CONTRACT.md is retained unchanged. It specified the
three-state input, alpha, horizons, accuracy thresholds, admission check and
current-state target cache before the principal outputs were examined.

The independent cost challenge identified full target-value memoization as an
ordinary capability that must not be withheld. The final principal calculation
therefore reports BOTH the original current-state-cache reward and the stronger
complete-memoization count, on the identical input and with identical accuracy
thresholds. This was a strengthening of the comparator, not a favorable retuning
of the scientific acceptance rule.

For complete memoization, the principal's implementation computes, for each
label, the probability that it has not been queried, using a substochastic
transition that deletes all query branches for that label. Summing one minus
those probabilities gives the expected number of distinct target values. It
counts a proposal's target evaluation even if the subsequent MH test rejects,
unless that label was already cached. First-stage rejection in delayed
acceptance avoids the target query. Initialization is always counted.

The independent four-state implementation instead explicitly enumerates the
joint law of current state and set of queried labels with exact fractions.
Its matched comparisons use complete memoization throughout.

Neither method treats the full diagnostic truth table as pre-supplied oracle
information. If it were supplied, direct finite discrete sampling would be an
additional stronger comparator. The tiny finite tables are diagnostic inputs,
not evidence for a practical application with an expensive unknown target.

The cost vector includes initial and subsequent global candidates, local Q
proposals, target queries, q/proposal-ratio evaluations, uniforms, cache memory
and implementation work. The scripts quantify the first three. They do not
assign a measured exchange rate to the remaining operations. A fixed number
of mixture steps has random component counts; their expectations are not
substituted into deterministic-count sampling laws.

For the tempered extension, eta is fixed in advance. Lowering eta admits more
local proposals and can increase target evaluations. No numerical eta sweep,
wall-clock optimization or application speed claim was performed. The analytic
result is separate from the original diagnostic's frozen full-screen input.
