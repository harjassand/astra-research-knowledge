# Independent audit: majority-insertion uniform Green transport

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review. Reviewed MAJORITY_INSERTION_UNIFORM_GREEN.md, check_majority_collar_degrees.py, MAJORITY_COLLAR_DEGREES.json, and the imported phase offsets.

## Verdict

The conditional uniform comparison theorem and its three concrete finite tests pass. The max-plus computation is valid rate-form Schur elimination, including its denominator updates and self-loop deletion. One assumption should be made explicit: EVERY retained R-preserving transition must have |Delta C|≤1, not only the phase-preserving fast reactions. This is satisfied by the concrete network; otherwise a wider collar and corresponding finite test would be required.

The result is a constant comparison under the specified insertion map, not a near-identity shift or a global feedback estimate.

## 1. Matched states and untouched rates

Removing c=m,m+1 from shell R and c=m,m+1,m+2 from shell R+1 leaves equal numbers of states and the stated phase-preserving bijection. For all sufficiently large R, the collar is strictly interior for every fixed offset h_j. On the lower retained side, A increases by one and is bounded below by a fixed multiple of R. On the upper side, C increases by one and has the same property. The other population is unchanged.

With nearest-neighbor retained C transitions, no direct retained edge crosses the removed band; both endpoints of every matched direct retained edge lie on the same side. Its stoichiometry is therefore preserved by the map. Falling-factorial ratios in the increased coordinate lie in [1,1+C/R], uniformly. The unchanged coordinate preserves every enabled/disabled condition, including at true low-count endpoints. Positive sums and residual-changing killing rates inherit these bounds.

## 2. Exact positive rate-form Schur arithmetic

For current non-self transition rates q_ij and killing q_i0, eliminate v with total q_v=sum_(j≠v)q_vj+q_v0. The effective rates are

    q'_ij=q_ij+q_iv q_vj/q_v, i≠j,v,
    q'_i0=q_i0+q_iv q_v0/q_v.

The original edge to v is removed. A return i→v→i is NOT a new jump. Summing the displayed effective non-self rates and killing yields

    q'_i=q_i−q_iv q_vi/q_v,

which is exactly the negative Schur diagonal. Thus rebuilding the diagonal from the new outgoing rate list implements the apparent diagonal cancellation identically, without subtracting leading asymptotic coefficients.

Every current rate is a positive sum/product/quotient of original positive rates. Its leading degree is therefore propagated by maxima for sums, addition for products, and subtraction for quotients. The denominator degree is the maximum over the CURRENT outgoing non-self/killing edges, after previous return self-loops were discarded. This is exactly what the script implements. Negative effective degrees are permitted and are correctly retained.

Each removed state reaches killing by repeatedly attempting immigration, so all intermediate eliminated blocks are transient and their denominators are positive. The script's assertion of nonempty outgoing dictionaries is consistent with this separate reachability proof; that assertion alone would not establish transience in a general graph.

## 3. Completeness of the finite collar test

Inside the collar, A and C are both proportional to R. All primitive enabling decisions depend only on the fixed phase: immigration is always enabled, activation requires B>0, and clearing/fast conversion require B≥4. Their degrees are respectively 0,1,3,3, as encoded.

The only entries into or exits from the removed collar are fast C moves at B≥4. The script includes both boundary layers and all such degree-three entry/exit edges. Direct edges among retained states are omitted from the finite calculation intentionally: they do not enter any eliminated-state denominator, and adding them afterward preserves the comparison because their own rates already match with 1+O(1/R) ratios. The finite calculation therefore captures every Schur-created support and degree, rather than an incomplete subgraph.

Re-ran the script. It reproduces MAJORITY_COLLAR_DEGREES.json byte-for-byte:

- K=4: 4 nonzero effective rates, equal support and degrees;
- K=8: 100 nonzero effective rates, equal support and degrees;
- K=12: 324 nonzero effective rates, equal support and degrees.

For m/R in a compact subset of (0,1), primitive leading coefficients are strictly positive continuous functions of this ratio. Finite positive Schur operations preserve that property; denominators are bounded below on the compact set. Matching nonzero degrees thus gives uniform upper/lower constant ratios. No eigenvalue approximation or numerical sign extrapolation is used.

## 4. Positive forests give a uniform kernel constant

The exact Schur-complement generators have matching state sets and off-diagonal/killing supports. Their determinant and every nonzero inverse-entry numerator admit positive forest expansions. Each forest selects at most one outgoing edge per vertex. The O(R) unmodified rows each cost at most 1+C/R, giving an overall bounded factor. Only O(1) boundary rows carry the Schur-generated constant-factor costs. Lower bounds follow in the same way.

Thus every corresponding forest term has a two-sided constant ratio, independent of R and the queried retained states. Positive summation preserves this for numerator and denominator, and division gives the stated uniform Green comparison. Matching supports also preserves zero entries. Full Green restrictions equal inverse Schur complements exactly.

## Scope retained

Removed-row queries are not covered. High-side transport inserts a C particle and is not a physical fixed-C residual shift. The constant need not approach one and cannot be used as a small commutator error. Constants depend on fixed phase width and finite tests; widening-alphabet uniformity and global forcing contraction remain unproved.

Reviewed hashes:
f92f0ffb3c3aa62a8d73b7106d04df3e9c3969448f5d289c3e81df66d65b8654  producer-workspace/MAJORITY_INSERTION_UNIFORM_GREEN.md
9668092640c61e29cda30f838ad3f9433fdc771f4c1ffcafd7328d5bd8463710  producer-workspace/check_majority_collar_degrees.py
0d62329c0325cc4dff8b29d9ddd0237f783f5769d636cd7755bcd47a63ebc2fe  producer-workspace/MAJORITY_COLLAR_DEGREES.json
