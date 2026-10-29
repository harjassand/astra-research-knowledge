# Independent review: collective Schur extraction of dark-direction programs

2026-10-29. **ACCEPT** the exact conditional extraction theorem, the scoped standard approximate-compiler reduction, the streaming support/memory result, and the stated IID finite-call lower bounds. This is not acceptance of a fully compiled d9 native circuit, approximate-common-kernel robustness, practical advantage, or the separately pending quaternion-program gate extension.

## 1. Actual operation and correctness

The input contract is load-bearing: one fixed unknown c and joint support W^tensorN⊗B, W=c-perp, throughout the actual acquisition history. The accepted commutator-acquisition full-joint promise supplies this in its stipulated exact model; observed Schur labels alone do not certify that promise under arbitrary noise.

Choose coordinates with W excluding the last basis vector. In a polynomial Schur block, the nonnegative last-coordinate number operator has kernel Q_lambda(W). A positive joint state supported on its zero eigenspace has no coherences to positive-weight sectors. Multiplicity/reference correlations do not change this statement. Partitions with d rows have no such zero-weight support and occur with zero probability.

For k=lambda_(d−1), the rectangle(k^(d−1),0) lies inside lambda. A sequence of removable corners outside the rectangle exists, for example by repeatedly removing an allowed outer corner in the skew diagram. Each selected predecessor mu has Q_lambda contained with multiplicity one in Q_mu⊗V. The **inverse** fundamental CG branch is an isometry from the entire Q_lambda, initialized with the known branch label. It is not forward projection with a missing success probability. Covariance preserves the sum of the two nonnegative last-coordinate weights, so both output factors have zero last-coordinate weight. Repetition reaches the rectangle with certainty conditional on lambda.

The rectangle's restricted U(d−1) representation is det(W)^k, a one-dimensional space. Any positive state supported on a one-dimensional factor times junk is its pure projector tensor a junk state. Thus the remaining register is exactly pure and decoupled from all retained bath/reference/path/peeled registers. This is the decisive reason arbitrary input correlations are permitted. U(d) covariance transports the result to arbitrary W.

The known representation equivalence Q_(k^(d−1),0)=det^k⊗Sym^k(V*) identifies that ray with |conj(c)>^tensork. The determinant contributes only a global phase within the measured-lambda branch. No antiunitary operation on an arbitrary supplied state is assumed. Inverse symmetric Schur encoding emits the pure product copies. If only a few are required, sequential inverse symmetric CG steps emit those and leave/discard the remaining symmetric register without harming the emitted copies.

## 2. GT phase and efficient-control reduction

The stated rectangle GT patterns and occupation mapping are correct. Row j has sum(j−1)k+t_j, so its weight is k−a_j. Raising E_(j,j+1) increases t_j by one, hence changes a_j→a_j−1 and a_(j+1)→a_(j+1)+1. Substituting rectangle entries in the standard positive GT raising formula gives squared coefficient a_j(a_(j+1)+1). The parity phase (−1)^(sum j a_j) changes sign under exactly this transition, yielding the dual-representation minus sign. Diagonal generators match after the det^k shift. These generators fix the representation equivalence, not just its dimension or weights.

I independently checked13014 exact rational GT raising-coefficient/phase transitions for d2–9 and k≤5, in addition to replaying the author's4998 weight/parity cases. The phase is essential; a phase-free occupation relabeling is not the asserted equivariant decoder.

The [Bacon–Chuang–Harrow primary manuscript](https://arxiv.org/pdf/quant-ph/0601001) was read, including its inverse-isometry interpretation in Eq32, multiplicity-free one-box rule in Eq33, and circuit construction. These support use of known fundamental CG transforms and their inverses rather than a generic arbitrary-irrep product oracle. The standard approximation complexity applies to the supplied primitives; O(N) such steps can receive allocated synthesis-error budgets. Joint instrument errors compose, including adaptive use, but normalized errors after rare conditioning need acceptance accounting. An ideal exact representation theorem does not provide an exact finite Clifford+T realization or a d9 hardware resource estimate.

## 3. Streaming and memory

Sequentially CG-coupling each fresh minus record and measuring the new partition keeps the current representation in its zero-last-coordinate-weight space. For a memory-bearing source this is an induction on the actual measured history: the measurement may steer the bath, but the next record must still satisfy the same full-joint fixed-W promise. This proves correctness, not IID yield for an adaptive source.

For an IID source the multiplicity-path measurements are compatible with the final partition measurement and do not affect future independent record preparation. The final partition distribution is unchanged. Storing the lower GT rows requires d(d−1)/2 integers bounded by N; hence36ceil(log2(N+1)) qubits for d9 is a valid representation-register upper bound. It excludes fresh records, acquisition and CG workspace, routing, protection, classical history, and emitted physical programs, as the author states. It is not a complete peak-memory or device-cost claim.

## 4. IID finite-call bounds

Schur partition probabilities equal f_lambda s_lambda(p), also the RSK shape law for IID letters. [Knuth's primary RSK construction](https://msp.org/pjm/1970/34-3/pjm-v34-n3-p09-s.pdf) was inspected for the word/tableau convention (weak rows, strict columns). For eight letters, a strict decreasing subsequence of length8 must contain all letters in reverse order. Greedy completion is optimal for finding one such subsequence. Its waiting time is a sum of eight independent geometric waiting times. Completing k successive full decreasing subsequences yields k disjoint subsequences; Greene's invariant forces the first k columns to have height8, hence lambda8≥k. This is only a lower bound for k>1, because Schur extraction can succeed without that sequential greedy event.

The Greene citation was located through the author's institution and MIT primary-reading link; the publisher's full paper returned HTTP403. I checked the actual used special consequence mathematically and exhaustively for9841 words over three letters of length≤8. This is an access limitation, not a claim to have read the blocked paper.

For the retained memoryless two-axis example, the accepted Gram eigenvalues give normalized minus probabilities{1,1,1,2,2,3,3,3}/16 and per-call marked-letter probabilities with denominator36. Plus outcomes are already paid as no advancement. I independently reproduced **all39 exact rational rows** using successive geometric waiting-time mass distributions, structurally different from the author's per-call progress-state update. In particular:

-576 ordinary calls: P(k≥2)≥0.9737402949272663;
-512 calls: P(k≥2)≥0.9280742951439552;
-1024 calls: P(k≥4)≥0.9765548339473412.

These are ideal Schur-event bounds for the explicitly IID informative source, not arbitrary correlated-source rates. The fictitious eigenbasis letters are a probability proof device; no measurement or knowledge of those letters is required in the actual controller. Unknown local twisting leaves the partition law invariant. The separate gate-success arithmetic is conditional on its external extension and is not accepted here as an independently verified gate claim.

## 5. Executed evidence

All author files were copied before execution. Both core and streaming SHA256 manifests verify. Full replay reproduces every stored output exactly, including the RSK Monte Carlo. Those samples are classical distribution simulations, not executed quantum Schur circuits or rigorous probability certificates.

My `independent_checks.py` also reconstructs the d3,N3 decoder without the author's SVD-selected irrep basis. It uses central symmetric/antisymmetric projectors and two Kraus operators from the wedge map and a transposition. The summed effect equals P_(2,1) to9.27e−16. Twenty-four complex dark-direction fixtures with bath/reference dimension5 give residual outside the conjugate program ray at most3.76e−16. This tests retained correlations and the conjugation convention. The general exact proof above, not finite floating precision, establishes arbitrary-dimensional correctness.

## Scope and significance

Accepted new capability within the exact promise: measured partition k directly heralds k pure unknown dark-direction programs, using actual quantum records and known controlled processing, with no source inverse, bath tomography, IID correctness premise, or hidden successful-projection factor in peeling. Streaming prevents tensor-product storage of all raw records from being intrinsically necessary. This materially improves the previously rare exterior-event implementation in the stated IID example.

Not established: positive rate for every source, a guarantee for identity/rank-deficient source histories, stability under imperfect common support, practical control/storage/error costs, an advantage over equally informed conventional quantum processing, historical novelty, a complete native d9 circuit, or an end-to-end encoder/recovery architecture. A source can validly produce k=0 forever. The standard Schur machinery is openly credited.
