# Independent additive review: normalization and coarse spectral records
2026-10-29, `producer-workspace/review_finite_quantum_sampler`.

## Decision
PASS both mathematical lemmas, with the explicit unclosed-operation limitations retained. This is **not** acceptance of approximate-central streaming recovery, nearby Clifford representations, finite native spectral pinching, inverse-support implementation, or historical novelty. Source originals were preserved and their manifest verified.

## Normalization and dilution
For S=(sum Delta_a^2)^(1/2) on its support, Delta_a^2<=S^2. Operator monotonicity of square root gives |Delta_a|<=S, and -|Delta_a|<=Delta_a<=|Delta_a| then gives -I<=S^(-1/2)Delta_a S^(-1/2)<=I. This does not assume that S commutes with Delta_a. Expanding the product proves sum A_a S A_a=S exactly.

For Hermitian A,S,
||[A,S]||_F^2=2Tr(S^2 A^2)-2Tr(S A S A).
The fixed-point identity gives sum Tr(S A_a S A_a)=Tr(S^2), so the claimed weighted Dirichlet equality is exact. Its left side is nonnegative despite E=sum A_a^2-I not being assumed positive. Tr(S^2 E)<=||E||op Tr(S^2) is valid for Hermitian E, yielding the bound without a dimension or inverse-gap factor.

If E=0, every commutator [A_a,S] vanishes. Adding normalized central anticommutators then implies centrality for Delta_a=S A_a, since the relevant commutator is multiplied by S^3. Conversely, exact centrality for Delta implies every Delta_a^2, and hence K and its supported functional calculus, commutes with every Delta_c. Thus A_a=S^-1 Delta_a, sum A_a^2=I, and normalized centrality follows. Both conditions are needed in the stated equivalence; the note correctly does not identify normalized centrality alone with the original promise.

Appending maximally mixed r-dimensional junk scales Delta by 1/r, S by 1/r and the raw centrality commutator by 1/r^3 in operator norm. The normalized tuple becomes A tensor I. Recovery optimum is exactly unchanged: attach the junk before any enlarged-output decoder for one inequality and discard it for the other. This is a valid warning against a raw absolute defect as a dimension-independent certificate, not an impossibility proof for all rank-paid approximate recovery theorems.

The support inverses remain mathematical only. Nothing here implements them or estimates their defects with the ordinary-source interface.

## Random coarse spectral records
Choose any eigenbasis of B restricted to the invariant support P. Pinching deletes entry X_ij precisely when its two eigenvalues are in different bins. A uniform offset modulo w separates them with probability min(1,|b_i-b_j|/w), including degeneracies. The continuous squared Frobenius expectation is therefore exact. Replacing the minimum by |b_i-b_j|/w and applying Cauchy--Schwarz to the ordered entries gives ||[B,X]||_F ||X||_F/w. Rank remains at most d after the subtraction, so ||Y||_1<=sqrt(d)||Y||_F followed by Jensen proves the trace bound.

For L equally spaced offsets, the separation event on the offset circle is an arc of relative length min(1,|b_i-b_j|/w). Its grid count exceeds its length times L by at most one, with the specified half-open boundary convention. Thus the added ||X||_F^2/L term is valid, including exact endpoint hits. L a power of two permits exact uniform selection with log2 L fair bits. This finite randomness is not finite spectral-measurement implementation.

The noncommuting telescope is correctly oriented:
I-E_q...E_1 = sum_j E_q...E_(j+1)(I-E_j).
There is no right-hand prefix multiplying X. Each subsequent pinching is CPTP, so it contracts the trace norm of the Hermitian difference X-E_j(X). This proves the pointwise bound by the original-X single-measurement disturbances and hence its expectation. Independence of offsets supplies the advertised marginals but is stronger than needed for this inequality. No commutation or joint diagonalization of B_j is required.

For the randomized record instrument, discarding all records gives the averaged product pinching. Fix an original optimal CPTP decoder R, which exists in finite dimension. By the Pauli response identity, its fidelity difference is at most (1/8)sum_a ||Delta_a-E(Delta_a)||_1: the dual R* is unital positive and maps each Pauli into the operator interval [-I,I]. Convexity and the preceding estimates prove the exact displayed Fopt retention bound. Retaining records cannot reduce this optimum because the decoder may ignore them. There is also some fixed set of offsets attaining at least the resulting averaged score, but neither this existence argument nor the optimum supplies a known executable decoder.

Arbitrary background outside P is harmless for these response differences because self-adjoint B preserving P reduces P, and X is supported there. No physical subtraction of the channel's background is used. Measuring the full records can still disturb other objectives and does not make the resulting approximate axes consistent or the response blocks two-dimensional.

## Independent diagnostics
`check_independent.py` checks 1,445 exact rational grid-separation cases for L=1,2,4,8,16, including degeneracies and boundary alignments. It also checks 48 independently generated Hermitian triples in dimensions 2,3,5,8 for contraction, fixed point, weighted Dirichlet identity and junk-replica normalization, and 48 noncommuting three-pinching telescopes. Largest arithmetic residual was 1.5e-12 in the Dirichlet equality; all passed. The author's five normalization replicas and 120 coarse-record cases were replayed from copies in the audit folder. These finite diagnostics supplement the analytic proof and are not controller, source-call or hardware evidence.
