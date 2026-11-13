# Full-output TV accounting with terminal-Q measurement and dynamic MPS order

Scope: the actual fixed-grid diagonal-D / rare-QD / fully mixed pair-reset circuit, basis input and final Z outputs. This is an exact representation/measurement rearrangement plus conventional trace-distance accounting. It does not prove low rank or efficient scaling.

## 1. Exact early measurement under presampled flags

Condition on the complete physical reset/rare flags, sampled from their correct distribution independently of Born outcomes. Partition each site's wire into intervals ending at its next reset or final Z readout. Immediately after the LAST actual Q touching that site in an interval, it can be measured in Z and its outcome recorded.

All subsequent operations before the interval ends commute with its Z projectors: D gates are diagonal, Q on other physical endpoints acts trivially on that site, and resets on other sites commute with its local measurement. At the ending reset, partial trace makes any previously removed offdiagonal terms irrelevant. If the interval ends at final readout, the inserted Z measurement is exactly the deferred final measurement. Thus, after discarding auxiliary early records, the FULL final Z-output distribution is unchanged. This is a law identity, not an assertion that intermediate coherent density matrices are identical.

The statement holds in the diagonal frame as well: a site that is only a control in dressed Q appears through Z-diagonal factors, so its Z projector commutes; reset feedforward phases also commute. Its measured value must still supply subsequent classical control signs. Early measurement does NOT erase surviving-neighbor entanglement or allow independent resampling of their states.

If a later reset occurs, its fresh basis bit replaces the old value; the earlier outcome is not automatically the final output. An actual reset's old Z measurement is deterministic on an already known-basis site. Initial and reset-prepared basis bits can be tracked without redundant sampling. If physical SWAP routing is added, the criterion must follow logical tokens, not fixed hardware positions; that is outside this fixed-grid implementation statement.

The future flags may be used because they are sampled independently of the quantum state. A schedule that selects future gate categories from measurements requires a separate causal argument; do not peek into undefined future feedback.

## 2. Correct exact reference for the error proof

Define the exact comparison process to include the same early projective instruments and their complete records. Its final output law equals the original circuit by section1. The approximate MPS process implements that augmented process with compressions. Applying the joint classical-quantum proof from TRAJECTORY_TV_CERTIFICATE.md gives

TV(P_original,P_MPS) <= E_approx[sum sqrt(w_j)].

Every branch must retain the early outcome and apply all later operations using that outcome. Comparing an early-collapsed approximate state to the original NOT-yet-collapsed pure trajectory is not a valid conditional-state test. Dense validation should either apply the same early measurement to the reference, or compare unconditional final distributions.

## 3. Dynamic order is a representation change, not a physical SWAP

An exact adjacent tensor-site SWAP followed by the corresponding swap of the physical-label-to-MPS-position map leaves the represented physical state unchanged. Forgetting the label-map update changes the circuit. Each SVD truncation used during reordering incurs its usual sqrt(discarded-weight) cost; QR-only canonicalization and exact label bookkeeping incur no mathematical approximation.

The ordering rule can depend on earlier sampled outcomes and on the current approximate tensors. With a fixed algorithm, those tensors are deterministic functions of the full classical transcript (including any heuristic random seed). For the comparison proof, use the same transcript-dependent representation choice in the exact process. This is an identity operation on physical states, regardless of the rule. The contraction/error argument therefore remains valid; it does not require a fixed order or access to the exact Schmidt spectrum.

## 4. Exact removal of a terminal measured site

After projection to known bit b, a canonical MPS site tensor has only the b physical slice nonzero. That slice is a virtual-index matrix C. To remove the quantum site, absorb C into an adjacent tensor, preserving all remaining amplitudes and virtual correlations. Do not drop C or split its two virtual sides: its surviving neighbors can remain entangled. A known-basis site can later be reinserted as |b> times an identity virtual map. Charge any optional rank truncation after absorption; exact absorption is error-free but has its actual arithmetic cost.

This can reduce active tensor count and routing distances without forcing the remaining Schmidt ranks small. It is not equivalent to deleting the old site's historical component.

## 5. Budget policy when future reordering work is outcome-dependent

A flags-only precomputed SVD count is valid for a static deterministic order and the associated known-basis schedule. It need not bound an adaptive-order implementation whose future routing choices depend on measurement outcomes.

Safe implementable options:

(a) Reserve delta/M for each of the M physical operation slots (plus a designated readout/cleanup slot if needed). Before each slot choose its full reordering and gate implementation, count its J local compressions, and allow amplitude loss <=delta/(M J) at each. Include all reordering, MPO application, postmeasurement compression, and cleanup work. The total on every path is <=delta.

(b) Maintain a remaining budget. At each slot reserve at most remaining_budget/remaining_slots, and divide it among the chosen compressions. If the within-slot operation count itself is adaptive, use a summable within-slot allowance schedule or a proved maximum. Do not silently add unbudgeted tensor sweeps.

(c) A universal compression-index schedule delta/[j(j+1)] requires no operation-count prediction and sums to delta, but becomes very stringent for large j.

Strict rank-cap abort must occur BEFORE exceeding an assigned tolerance or the total budget. Exact hypothetical continuation on that abort yields

TV(P_original,P_fallback) <=delta+Pr_approx(abort)+numerical_error.

The algorithm may instead grow ranks and finish, preserving delta but losing its runtime guarantee. Neither option proves a practical fixed-rank sampler.

## 6. Resource and confidence report required

For each frozen algorithm and fresh independent holdout sample report:
- full-output truncation budget and actual cumulative path loss;
- rank cap, maximum active quantum sites, maximum bond rank;
- SVD count split into physical gates, reordering, and compression/cleanup;
- total wall time including planning, early measurements and output;
- maximum live tensor/temporary storage, not merely final tensor storage;
- abort count and a valid confidence upper bound, or a deterministic analytic bound.

Use the same circuit, flags distribution, target TV budget, early measurement, operator simplifications and permitted ordering optimization for direct and frame baselines. Policy changes across trials define a new algorithm: freeze the final version before its holdout evaluation. Reusing tuning seeds for its confidence report is invalid without a separate selection correction.

The exact-integer verified abort_confidence.py provides fixed-N upper limits and confidence spending across predetermined checkpoints; adaptive sample-count checking must spend across every possible N. The result is a stated confidence guarantee, not absolute certification of floating-point arithmetic. Five or thirty successful trajectories cannot establish tiny abort error or scalable rank behavior.
