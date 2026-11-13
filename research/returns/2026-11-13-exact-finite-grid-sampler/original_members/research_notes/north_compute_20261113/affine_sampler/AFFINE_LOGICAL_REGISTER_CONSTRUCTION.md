# Exact Z-affine logical-register sampler for the actual QD channel

Status: a constructive alternative to MPS, using established stabilizer/affine-support machinery. The small Gaussian-integer backend is implemented and exhaustively checked; the large component-wise logical-array sampler is a construction, NOT yet implemented. Flag-based resource probes do not establish scaling or a tail theorem.

## 1. Exact invariant, not an independence assumption

Maintain a partition of physical vertices into parity blocks C, each with a known constraint product_{v in C} Z_v = sigma_C. Initially each vertex is its own block. The state can have arbitrary amplitudes over the satisfying affine binary subspace. For every block choose one pivot bit; all other bits are free. The total number of logical bits is m=n−number_of_blocks.

This is a Z-stabilizer-subspace dimension, not a claim to have found every stabilizer or the true magic/stabilizer rank. Generic non-Clifford amplitudes remain inside the logical register.

D is diagonal and preserves all these constraints. A rare Q=(12I−5iXX)/13 on endpoints in distinct parity blocks drops their two separate constraints but retains their product: MERGE the blocks, increasing m by1. If the endpoints are already in the same parity block, Q preserves the constraints and acts within the existing logical space.

Measuring Z_v in a block of size>=2 adds one independent constraint. Extract v as a singleton and retain the parity constraint on the remaining block with its sign updated by the measured bit. This reduces m by1. In particular, measuring one vertex of a size2 block forces the other vertex into a known basis state as well, even when that other vertex has future rare gates. This extra inference is exact. Singleton measurements are deterministic. Pair reset is two such measurements followed by fresh known basis bits.

The measurement outcomes and constraint signs are retained. They cannot be replaced by independent random bits.

## 2. Separate entanglement groups

Parity blocks are NOT independent quantum states. A D gate can entangle two logical registers belonging to different parity blocks without changing either parity constraint.

Maintain separate quantum groups, each holding a full arbitrary logical amplitude array for all its nonsingleton parity blocks. Initially all sites are classical known bits. A rare Q merges its endpoint groups (including any newly activated basis sites). A D gate between two uncertain bits in different groups merges their groups before applying its phase. If one bit is known, D only acts diagonally within the other group; if both are known it is a global phase. A reset's preceding D may be skipped because tracing both endpoints erases it.

After a measurement, remove the measured singleton and any newly inferred known singleton from the quantum group, but retain the entire remaining joint amplitude array. Do NOT split surviving vertices simply because a measured site was removed. This retains all conditional correlations. Terminal-Q early measurement is the previously proved exact final-output rearrangement and can be used before these updates.

A group's logical dimension is m_C=|C|−number_of_parity_blocks_in_C. Its amplitude array has2^{m_C} entries rather than2^{|C|}. The group can be highly entangled; no low Schmidt-rank or area-law assumption appears.

## 3. Explicit constructive updates

Choose a pivot in each parity block. Free physical bits y determine the pivot through the block's parity sign. Then:
- D multiplies an amplitude by(3+4i z_u(y)z_v(y))/5.
- Q within a block maps y by a known XOR mask, updating amplitudes by12 psi(y)−5i psi(y xor mask), divided by13.
- Q merging blocks embeds the old support and its endpoint-flipped coset into the merged affine basis, with coefficients12 and−5i. The new logical dimension is one larger.
- Z measurement selects an affine linear equation in y, computes its squared-norm probability, and reparameterizes the remaining affine subspace by elementary binary elimination.
- Merging independent quantum groups first forms their tensor-product amplitude array. Measuring/extracting sites retains all remaining amplitudes jointly.

These are polynomial bookkeeping plus linear work in the current array dimension. If every intermediate group is capped at K logical bits, the state-storage/time cost is poly(n,M)2^K, not a tensor-network width assumption. Abort before a merge or expansion exceeding K; returning a fixed fallback changes full-output TV by at most the graph-only abort probability. No resampling of successful flags is allowed.

## 4. Exact arithmetic option

Keep amplitudes as UNNORMALIZED Gaussian integers and omit common denominators5 and13. D multiplies by3±4i; Q multiplies and adds using12 and−5i. Tensor products multiply Gaussian integers; measurement only selects amplitudes. A branch probability is an exact ratio of integer sums of squared real/imaginary parts. Sample it with uniform random integers/rejection, not floating thresholds.

For M gates, a crude amplitude bit-length bound is O(M): D grows coordinate magnitudes by at most7, Q by at most17, and merges add bit lengths of disjoint histories. Norm bit lengths add at most the logical support size exponent. Therefore capped exact simulation has polynomial bit cost in explicit circuit length and2^K. This does not claim small constants.

`exact_gaussian_backend.py/json` implements the tiny sparse global version. It sums ALL category choices and ALL reset/early outcomes on three overlapping qubits and three gates, at r=.03, epsilon=.02 and.05, both with and without early measurement. All eight final probabilities match the original rational density-channel computation EXACTLY. The ledger records1984 processed branches, maximum4 supported basis strings,18-bit amplitude integers and37-bit probability denominators. This validates arithmetic and chronology, not large-instance scalability.

## 5. Existing primary machinery and failed shortcuts

Aziz,Pan,Gullans,Pixley, arXiv2508.20252, develops low-rank stabilizer dynamics for non-Clifford monitored circuits. The logical-register perspective is established machinery; our specialization exploits the concrete Z-parity partition and actual QD/reset gates. That paper's empirical truncation procedure does not itself supply our required full-output TV certificate, and invalid-trajectory rejection must not be imported as unbiased sampling.

Pauli-path literature gives other powerful methods, but its hypotheses must be checked: Aharonov et al noisy random-circuit sampling assumes the relevant random ensemble/anticoncentration; González-García,Cirac,Trivedi, Quantum9,1730(2025), has beyond-average guarantees for local observables, not an automatic generic prefix-conditional full-output sampler. Actual QD preservesZZ, so it is not a local unitary2-design. An observable estimator cannot simply be relabeled a full sampler.

## 6. Consequence and decisive missing step

This construction can exploit large physical entanglement with few independent binary coherence variables, unlike an MPS-only method. It also gives exact inferred-basis retirement beyond the terminal-site test. But empirical resource probes show the target epsilon=.05 can still generate very large coupled logical groups. The decisive missing result is a rigorous tail/expected-cost bound on these groups, or another compression of their arbitrary logical amplitudes. Until then it is a restricted algorithmic construction, not a civilisation-changing primitive.
