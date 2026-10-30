# Optional improvement after reviewed two-half certificate: no noise coloring needed
2026-10-29. Separate addendum; does not edit or supersede the hash-reviewed TWO_HALF_GOOD_SERVICE.md. The application below has not yet received independent review.

## Result
For independent state-independent Poisson kick sources, assume each source can affect at most b history neighborhoods. Then the control-spoil parameter can be taken as

   q_spoil=[1−exp(−Lambda Delta)]^(1/b),

without a bounded noise-conflict chromatic number or a fixed spatial range assumption for THIS counting step. The rate sum affecting one neighborhood is at most Lambda. This does not relax the separate geometry needed for local clean witnesses or bounded-degree DATA fault-cluster counting.

## Primary inequality checked
Gavinsky, Lovett, Saks and Srinivasan, *A Tail Bound for Read-k Families of Functions*, Theorem 1.1 (arXiv:1205.1478v1), bounds the upper tail of Boolean functions of independent source variables when each source is read by at most k functions. At the all-one endpoint, if all marginal probabilities are at most p, it yields

   Pr(Y_1=...=Y_r=1)≤p^(r/k).

Theorem 1.2 states the equal-marginal special case explicitly. Primary paper inspected: https://www.cs.toronto.edu/tss/files/papers/1205.1478.pdf . This is an application of an existing inequality, not a new concentration theorem.

## Application to actual fixed-grid Poisson records
Fix a finite set S of DISTINCT owner/window cells on one nonoverlapping deterministic grid. For each physical kick source e and grid window n, define the independent Bernoulli variable

   X_(e,n)=1 iff source e has at least one Poisson occurrence in that window.

For each selected candidate (h,n), its control-spoil indicator is the Boolean OR of X_(e,n) over sources whose physical support intersects support(B_h). Each independent source/window variable is read by at most b selected indicators because that source affects at most b history neighborhoods. It is irrelevant how many other sources a neighborhood reads or how large the resulting pairwise conflict graph is.

Each spoil marginal is at most p=1−exp(−Lambda Delta). The read-b inequality therefore gives

   Pr(every candidate in S is spoiled)≤p^(|S|/b).

For countably many incident sources with finite summed rates, first truncate to finitely many source variables. The spoil events increase to the full events and every finite truncation has the same marginal upper bound p. Monotone convergence gives the same result. The state-independent occurrence law makes this an initial-state-uniform CP event probability bound; arbitrary quantum effects of the kicks do not enter the counting.

For the dense all-pairs example with per-pair rate O(1/N), a source affects only two owner neighborhoods, so b=2 even though the conflict graph has N colors. The estimate remains size-independent and pays the correct shared-event exponent. More generally, a bounded-cardinality kick touches at most that cardinality times the bounded number of owner history neighborhoods meeting one physical site.

## How to use, and what is not claimed
Replace q_spoil in §§5 and 7 of the reviewed two-half certificate by this read-b value. Its shortfall/spoil union argument and mixed moment bounds remain unchanged. This removes the extra noise-coloring assumption from the availability-spoil part alone.

It does NOT establish spatial locality of long-range pair kicks, bounded-degree correction/fault geometry, or a memory threshold under dense nonlocal noise. Those obligations cannot be inferred from the read-b counting law. The reviewed fixed-range/fixed-P_N theorem remains a valid conservative certificate without using this addendum.
