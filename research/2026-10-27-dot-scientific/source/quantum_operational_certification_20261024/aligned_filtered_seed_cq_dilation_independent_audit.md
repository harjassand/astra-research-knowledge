# Independent audit: aligned filtered-seed value by actual CQ dilation

**PASS — 26 October 2026.** Governing note: `aligned_filtered_seed_cq_dilation_value_theorem.md`. This receives homogeneous value of the non-TP aligned filtered seed, not a throughput-charged comparison with its unfiltered predecessor.

Choose d>=max h_i, d>0. The displayed six-dimensional V has orthonormal columns because different physical labels are orthogonal and each column has norm one. Its source has trace `3d+3TrA+9M` and physical input marginal equal to one third that trace times I3. Thus every finite M is an actual normalized channel after homogeneous scaling.

The controlled logical rotations are genuine output/reference unitaries: independently for each physical output label they send its two-component success vector to the same logical state. The reset remains a direct sum of three PSD 2x2 logical blocks, with no cross-physical coherence. The received arbitrary mixed-CQ-reset theorem therefore applies exactly, not by convex combination or an unreceived non-TP extension.

The low source block is exactly the requested aligned seed, high block is `MI9+P_(psi_(d-h))`, and the cross block is bounded independently of M. Reference partial trace and WH preserve this low/high reference splitting. For A>0, all three low entropy blocks have fixed positive lower bounds; their high blocks have uniformly positive order-M identity baselines.

For a block matrix with such bounds, determinant Schur complementation expresses the entropy difference from block pinching as the integral of a negative log determinant. Its argument differs from I by a matrix of norm bounded by `const/[(c+s)(c'M+s)]`; for sufficiently large M this is uniformly below one. Trace matching cancels boundary terms. The integral is O(logM/M), receiving the stated entropy estimate without a free pinching inequality for the deficit.

At the high baseline MI9 the deficit is zero. Its first variation in any Hermitian direction cancels exactly: the input coefficient is logM+1, the reference coefficient log(3M)+1, the output coefficient -2(logM+1), and the trace constant -log3. The bounded high pure perturbation therefore contributes O(1/M). This gives the claimed limit of the paid finite-source values.

For singular A, replace it by A+epsilon I, apply the established faithful-low result, then use continuity of xlogx. Zero Schmidt weights are already feasible in V and can alternatively be obtained by continuity. The all-zero pure component is the zero-deficit reset source. No interchange requiring a uniform M threshold as epsilon tends to zero is used.

The actual source-limit checker was rerun and passes. For commuting reset/filter Gram, matched covariance gives precisely this aligned form; noncommuting filters generally destroy the CQ acquisition and are not received. No accepted-only GLS inequality or factor-lambda_min comparison follows merely from nonnegative filtered-seed value.
