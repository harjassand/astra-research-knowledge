# Independent review: orbit-frame mean recovery and source-weight transfer

28 October 2026. Accepted at the scopes below, conditional on the separate representation/circuit-access review of the orbit frame and the received soft-polar recovery lemma. This receipt does not certify a compiled decoder, an encoder two-design algorithm, a hardware operation or a positive-throughput universal protocol.

## Rectangular moment identity

The reviewer independently derives the Haar projector second moment from its trace K² and swap trace K, obtaining the two scalar coefficients in `MEAN_TRANSFER_DERIVATION_v1.md`. Applying that identity to each weighted Gram entry gives exactly

    beta=(dK−1)(dN/D−1)/(d²−1).

This is the rectangular formula, not the d=D special case. Both orthonormality Tr(F_a†F_b)=d delta_ab and the complete output-isotropy sum F_b F_b†=(dN/D)I are needed. They imply a scalar partial logical trace of the averaged Gram square, so arbitrary positive error weights T are allowed without commuting with G. For a nonzero frame, dN>=D follows from full output support, so beta is nonnegative. With K<=d, the displayed upper bound beta<=KN/D−K/d is correct. The N=0, d=1 and K=1 scopes are handled by the author's explicit clarification/trivial-output cases rather than division by an invalid denominator.

The mean statements require the physical coefficient weight to be fixed independently of the random code. Conditioning on a selected random seed, cherry-picking a successful code or renormalizing a code-dependent branch would require a new analysis. The author's complete-outcome caveat is load-bearing.

## Redundant labels and null modes

With A=F V†, V†V=I_N, the coefficient weight is lifted as VTV†. Up to the explicit permutation between logical-first and label-first conventions, W_A=W_F J†, G_A=J G_F J†, R_A=J R_F J† for the isometry J. Consequently the weighted quadratic defect transfers exactly. Although G_A has forced null directions, R_A annihilates their orthogonal complement. Arbitrary redundant coefficients are not interchangeable with the canonical lift.

For odd singular-value filters, f(0)=0 and the success contraction is the same isometric lift. Tracing the enlarged error register leaves the logical operation unchanged; the output-side W W† and failure completion also agree. No inverse of the null spectrum, hidden multiplicity basis, or smallest-singular-value promise is used in this transfer.

Independent checks include 36 complex weighted rectangular/square fixtures with deliberately redundant labels. Defect transfer agrees within 6e−16 and soft-filter isometric lifts within 1.1e−15. A preserved counterexample shows that replacing the correct lifted weight by a uniform redundant weight creates spurious defect1/2 when the orthogonal-frame defect is zero.

## Error MASS and approximate designs

The selected good component need not be TP for an individual code. The new clarification correctly uses an ideal purification of norm²t and an actual one of norm²p_C. Its Bell success mass is at least |z|²/t, so the error mass is bounded by p_C+t−2 Re z. This supplies the same spectral penalty without a pointwise TP assumption. Numerical independent subnormalized fixtures check this distinction explicitly. The t=0 case contributes zero.

The 2epsilon Haar remainder follows from weighted Cauchy–Schwarz on the joint code/spectral distribution, using E Tr(RG)=t. It does not rely on T and G commuting. For approximate designs the source conservatively retains the uniform 2alpha epsilon remainder; this is valid and avoids silently importing the exact first moment.

The author's approximate-two-design budget is valid for the stated diamond distance between two-copy twirling channels. In an orthonormal frame, each F_i has operator norm at most alpha from the supplied orbit synthesis and its coefficient isometry. For positive trace-one T, sum_ac|T_ca|<=N. Summing the intermediate error index gives a quadratic coefficient norm at most N²alpha^4. The normalized two-copy projector input contributes K², and the logical trace normalization contributes 1/K. The linear contribution is at most 2Nalpha². Replacing N by M only in the upper bound yields eta[K M²alpha^4+2Malpha²]. The one-copy error follows by inserting a maximally mixed second input and tracing it. An operator-moment norm or entrywise design error cannot be substituted without its conversion factors.

The separate reviewer derivation offers another valid, sometimes weaker bound using Hilbert-Schmidt norms, (K N d²+2d)delta t, and a refined sqrt(1+d delta) remainder. It is explanatory working mathematics, not a substitute for the frozen author's bound or an assertion that the author implemented a design. Polynomial gate access still requires an actual design/code-isometry circuit whose precision cost is controlled. Exponentially small numerical tolerance in d is inexpensive only when the relevant synthesis/design dependence is logarithmic, not inverse tolerance.

## Physical source restriction and contamination promise

Linear bad-mass accounting is valid for a positive selected/rejected block decomposition. It does not follow for arbitrary off-diagonal coherence between selected and rejected sectors. The author explicitly restricts to the environment-sector block structure supplied by the source protocol and leaves arbitrary cross-sector weights outside this claim. Within selected sectors, arbitrary positive weights and multiplicity coherence remain allowed.

The new binomial domination is correct. A basis string with n0 occurrences of a fixed dominant eigenvalue symbol is invariant under the subgroup permuting those positions. A central Specht projection preserves this invariance. By branching, its nonzero irreducible components satisfy nu_1>=n0. Mixing basis strings from the iid diagonalized source therefore couples Schur defect to at most the number of non-dominant symbols. Stochastic domination by Binomial(k,c/k) follows whenever the largest eigenvalue is at least1−c/k. No knowledge of the eigenbasis is used by this probability proof or supplied to the decoder.

Independent exact Schur-Weyl spectral-law checks for18 rational spectra, k=3,...,8, verify69 tail comparisons. These supplement the subgroup argument and are not a finite-data certificate for the source promise. The orthogonal-contamination pure-block trace distance is exactly1−(1−c/k)^k. Thus the fixed-defect regime is not identical to approximating the entire block by a pure tensor power.

This remains a near-pure triangular-array/finite-block promise. Fixed positive contamination or a joint vanishing-error limit generally requires growing defect cutoff and the stated k^(O(j)) cost. A supplied local Schur-dimension lower quantile, retained source mass, code-block residue and actual outcome law remain necessary for useful rate/yield. A pure product source can meet the impurity promise without supplying entanglement. The note correctly does not infer positive throughput from low environmental rank or contamination alone.

## Gate and significance scope

This review checks the normalization-dependent mean guarantee using the declared alpha=sqrt(LM), source support and complete CPTP failure completion. The explicit subgroup orbit, all-multiplicity access, coefficient-projector computation, tableau circuits and projected-unitary synthesis are the other reviewer's responsibility. Finite whole-circuit errors need their actual gate/precision ledger. An unknown source forward channel does not grant inverse access; the claim instead uses the constructed known reference frame and an explicitly supplied encoder circuit.

Accepted here: weighted rectangular moments, redundant-frame null-mode transfer, subnormalized error-mass bound, stated approximate-design budget, source block-scope restriction and binomial contamination promise. Not established here: general efficient positive-entropy decoding, an efficient design generator supplied by this note, actual Schur probabilities from an unknown experimental source, a compiled QSVT sequence, historical priority or practical advantage over equal-information conventional algorithms.
