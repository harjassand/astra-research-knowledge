# Independent audit of the planar receiver

4 November 2026.

Reviewed PLANAR_RECEIVER.md SHA-256: a14bd87344a1d5ba3f8e51ee382061b2d777e3775dc7c6c69cf9114d81b9ba1c.

Dependency PROOF.md SHA-256: c46f70d3ed6e5f4960bfb38fa1f5c3279eb4cecb3ad1c85b44d4820b67597b35. Its weighted relative-error theorem is audited separately in AUDIT.md.

## Verdict and earned extension

The receiver survives this independent adversarial review. It supplies a polynomial-time exact signed contraction oracle for the stated planar/cofacial assemblies, closing a computational gap left open by the abstract weighted stability theorem. Combined with that theorem, it gives the claimed relative normalization estimate and approximate output sampler from noisy isolated-boundary data. No missing Fourier normalization, support/deletion complement, field-parity obstruction, or global Pfaffian sign error was found after checking the actual graph construction.

The theorem is an assembly of established matchgate/FKT machinery with the audited perturbation guarantee. It is not a new general planar solver, does not cover arbitrary nonplanar contractions or interior fields, and does not establish priority, practical advantage or a transformative physical capability.

Before freezing the reviewed version, the author made the inherited sampler conventions explicit: epsilon range, zero-output case, rational-coin cap, positive fallback, nonpositive-root fallback on a failed estimation event, and the no-training M=0 case. These are completeness clarifications, not changes to the central algebra.

## 1. Fourier tensor and normalization

For each block the Fourier expansion already includes 2^−k_b. Introducing uniform measure on its distinct boundary spins and each explicit environment spin therefore leaves no unknown normalization beyond the isolated physical block partition factors, which are explicitly excluded. For each spin, averaging its total Fourier monomial gives one if its exponent is even and zero otherwise. This is exactly the even-parity gate, not twice that gate.

A known edge contributes one for Fourier occupation 00 and a_e for 11, with zero for unequal indices. A block contributes its corresponding principal Pfaffian. Probe occupation inserts the output spin into the same parity constraint. Thus the open tensor entries are the signed weighted output moments, and odd total probe occupation vanishes. This remains true for nonphysical empirical pair matrices because the argument is polynomial algebra, not a probabilistic positivity assertion.

## 2. The field closure avoids a genuine obstruction

An individual two-entry unary vector (1,z) generally violates matchgate parity. The receiver does not incorrectly use one. The entire open network has even probe parity, so closing with the even projection of the product of unary vectors changes no value. For H_z(s)=1_even product z_i^s_i, the matrix with upper entries z_i z_j has Pfaffian minors equal to these entries because Pf(J_S)=1 for even S. This supplies a legitimate even signature for every rational z, including mixed signs and zeros.

Cofaciality is essential to placing this single closing gate without crossing wires. The supplied probe order and reverse order on the closing disk give planar gluing. H_z's entries themselves are even products, so reversing the corresponding labels does not secretly introduce a fermionic permutation sign. This fact does not license arbitrary reorderings of general empirical block ports: their measured cyclic order is part of the input contract.

A source of possible overclaim is avoided: mixed-sign z values used internally for prefixes need not satisfy the weighted stability cone. They are evaluated exactly as algebraic queries. Only the final nonnegative physical t query uses the relative-error theorem.

## 3. Support versus deletion: explicit check

The cited matchgate convention evaluates perfect matchings after deleting external vertices indicated by ones. Its complete-graph/Pfaffian construction therefore initially returns Pf(M_complement(s)). Adding one unit leaf at every original external vertex, and declaring those leaves to be the new external vertices, complements the bits exactly:

- A retained leaf must match its original vertex, effectively deleting that original vertex from the old matching problem.
- A deleted leaf leaves its original vertex available to the old matching problem.

Consequently the new deletion signature is Pf(M_support(s)), with no coefficient or sign prefactor. This works for odd as well as even arity. The resulting support signature is even in either case.

The reference construction has polynomial graph size and uses rational matrix entries and fixed constants. Keeping its signed crossover contributions is indispensable. Replacing them with ordinary nonnegative crossings would give a different tensor. There is no need to project an empirical matrix back into a physical ferromagnetic model.

## 4. Gluing and global FKT sign

Connecting external vertices by a unit bridge implements equality of deletion indices. A perfect matching either uses that bridge, removing both endpoints from their respective internal matching problems, or leaves it unused, in which case both endpoints must be internally matched. These are precisely indices 11 and 00. Every matching is counted once; no factor of two is introduced.

Gate disks, spin parity gates, edge gates and the single exterior closure preserve planarity under the supplied ordered embedding. A planar Pfaffian orientation has a common combinatorial matching sign. Negative edge weights do not invalidate this statement: they multiply the matching monomials after the orientation has aligned their combinatorial signs. Zero weights may be retained as edges of the same topology.

At A_b=0, a_e=0 and z=0, block, edge and closure signatures force the all-zero Fourier assignment. Every remaining parity gate accepts it with weight one, so the closed contraction equals one. Evaluating the same oriented graph at those weights therefore gives its fixed global sign. Calibrating once and retaining topology corrects subsequent queries, including those with exact zero or negative contraction values. It would be invalid to discard zero-weight edges, change the ordering/orientation, and reuse an unrelated calibration; the proof explicitly instructs otherwise.

## 5. Independent graph-level adversarial checks

The independent checks did not stop at verifying a tensor formula. A six-vertex signed crossover was explicitly reconstructed with four external vertices 1,2,3,4, two internal vertices L,R, unit edges 12,34,1L,4L,2R,3R, and edge LR of weight −1. Its nonzero deletion entries are exactly the required 0000,0101,1010 entries of value one and the 1111 entry of value minus one.

Using that gadget to planarize the crossing of K4, then adding complement leaves, exhaustive perfect-matching enumeration reproduced all 16 principal-Pfaffian support entries for a rational matrix with both positive and negative entries. A complete block, spin-parity, known environment-edge and collective-field assembly was then constructed. A planar embedding and an independent face-parity linear system produced a Pfaffian orientation. Its calibrated exact rational Pfaffian agreed with direct spin summation for all 81 choices z in {−1,0,1}^4. This exercises zero fields, hard positive and negative probes, signed intermediates and cancellation. Additional arity-one, -two and -three closures passed 39 analogous queries, including the odd-output case.

These finite checks are not a proof for all sizes. They directly attack the claimed convention, gluing and normalization joins; the general proof relies on the stated matching identities and the cited synthesis theorem. Test programs and numerical records are excluded from the proof-only packet.

## 6. Prefixes, stability and sampling

The prefix formula follows by replacing already fixed field factors by (1+t_i u_i), then inserting the indicator factors (1+u_i x_i)/2. Thus the 2^−j factor and the mixed-sign arguments of Z_A are correct, with no double-counted field factor. Marginalizing internal spins before or after this identity gives the same result.

For a physical nonnegative field query, the full edge-and-field weight has nonnegative Fourier coefficients and is pointwise nonnegative. Uniform explicit environment spins can either be included as independent one-spin blocks or integrated out; both preserve the hypotheses of the earlier weighted bound. The joint expansion must use the true independent block laws, not successively regard signed reconstructed neighbors as physical environments. The receiver correctly uses the joint theorem.

Weighted L1 error cannot increase when internal spins are summed out. The relative partition estimate and normalized signed output-law error therefore have the displayed constants. Positive-flow repair is applicable because the root is positive on the good estimation event and every reached prefix has positive signed mass. Exact rational evaluation handles forbidden or negative children without a numerical near-zero decision oracle.

For K>0 the displayed cap R gives total coupling error at most K 2^−R, safely within epsilon/4. On cap failure, choosing a positive-mass child preserves valid continuation. The ideal repair and the actual capped sampler are distinct distributions; the proof budgets their difference and supplies an evaluator for the actual transition probabilities. K=0 and a failed-estimation nonpositive root are explicitly handled.

## 7. Sampling and bit complexity

With M total estimated pairs, pair error at most epsilon/(32M) gives D_total≤epsilon/32. Hoeffding for {−1,+1} observables and a union bound justify the displayed per-block sample count. Its total cost is at most B times that number. Independence within a snapshot's different pair observables is unnecessary. M=0 needs no training. Reusing a learned block in several physical copies still incurs its error once per occurrence; sharing the training data cannot remove that systematic accumulation.

The conservative O(sum k_b^4 + sum d_v^4 + |E| + K^4) synthesized size is polynomial in the supplied description. The known graph may be large and is fully charged; only the unknown block interior volumes are absent from the arithmetic input. Each edge weight has polynomial rational bit length. Clearing denominators and bounding Pfaffian degree and coefficient height give polynomial output and intermediate bit complexity using appropriate exact elimination. Severe cancellation can create small values but does not create an exponential bit-length requirement in this rational contract.

Thus the runtime statement is an exact rational bit-complexity theorem, not a fixed machine-word or floating-point stability theorem. It does not prove that ordinary floating-point Pfaffian software will safely choose clipping signs. Each query requires a polynomial-time Pfaffian evaluation, plus reusable topology/sign preparation; sampling uses at most two such queries per output spin. Physical mixing, independent data acquisition, model validation and assembly calibration are outside that arithmetic cost.

## 8. Strongest prior and significance boundary

The decisive exact-computation baseline is [Cai and Gorenstein, Matchgates Revisited, Theorem 5.1 and Section 5 (2014)](https://www.theoryofcomputing.org/articles/v010a007/v010a007.pdf). It provides the principal-Pfaffian synthesis and signed crossover machinery. Planar matching contraction by FKT and matchgate networks is established, rather than a new algorithm here. Exact boundary reconstruction and boundary-field evaluation also have the primary precedents recorded in PROOF.md and AUDIT.md.

The earned extension is narrower and concrete: the previously abstract relative-error certificate now has a polynomial contraction and output-sampling receiver for supplied planar assemblies with cofacial fields. Signed empirical block descriptions are permitted, so model projection is not silently required. The finite-sample summary can be reused over admissible queries subject to its total error budget and occurrence counting.

An existing matchgate/FKT implementation given the same empirical signatures and the same stability analysis can perform the same contraction. No matched-resource lower bound or benchmark establishes superiority over that strongest adapted baseline. Novelty of the combined robust data-interface contract is unresolved. Arbitrary nonplanarity, general interior fields, sampling every hidden spin, unknown absolute block free energies, physical deployment and civilisation-scale consequence remain outside the proved result.
