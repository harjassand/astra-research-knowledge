# Sparse valid syndrome filling for signed known-state preparation
2026-10-30. Focused derivation; not a claim of a new Tanner filling theorem.

## Result first
The actual single-shot Tanner proof contains a useful partial bridge: if the mismatch induced by a sparse valid syndrome is decomposable by its local algorithm, that syndrome has a small preimage modulo the FULL normalizer. The distance/small-data-error assumption is unnecessary for this particular conclusion. However, the published sufficient condition for decomposition is a small ROW/COLUMN DECOMPOSITION NORM, not small syndrome weight or small mismatch Hamming weight. That missing conversion is precisely the new global filling obligation. No Tanner-specific counterexample or proof of that conversion was established here.

## Exact target and nearest-valid-syndrome reduction
Let H map Z errors to X-check syndromes, S=im H, and define

    ell(v)=min{|z|: Hz=v}=min_{k in ker H}|z0+k|.

The needed property is: constants C,tau>0 independent of N such that ell(v)<=C|v| for every v in S with |v|<=tau N. This is a restricted global coset-filling property: it quantifies over syndromes, not over a pre-existing small representative modulo stabilizers.

If y=s+e and shat is an exact closest element of S to y, then |shat-s|<=2|e|. For arbitrary choices of absolute frame preimages a(s),a(shat), their difference has syndrome v=shat+s. A small filling z of v implies a(s)+a(shat)+z belongs to ker H. On the target |0_L>, Z-type stabilizers AND logical Z act trivially (up to phase), so this is exactly the harmless quotient for this source state. Hence a guaranteed filling would bound the residual physical error by 2C|e| despite an extensive absolute frame. This algebra does not implement nearest-codeword projection, preimage acquisition, or fault-tolerant frame storage.

## Reading the actual Tanner proof
Primary source: [Gu et al., Single-shot decoding of good quantum LDPC codes, arXiv:2306.12470](https://arxiv.org/html/2306.12470), §§4.1–4.3, Definition4.4, Theorem4.10, Lemmas4.12–4.15. The published guarantee assumes small stabilizer-reduced data errors. Its mismatch decomposition norm counts local row/column codewords; theorem4.10 requires few active vertices in such a decomposition. Lemma4.14 distinguishes vanishing syndrome from stabilizer equivalence, using distance only for the latter. Lemma4.15 establishes decomposition via data-error bounds. The discussion explicitly distinguishes mismatch soundness from ordinary syndrome soundness.

## Actual attempted derivation
Use the paper's X-error convention and interchange X/Z for the desired source. For valid v choose ANY preimage e, not assumed small. Each vertex takes its local minimum correction epsilon_a. Because zero local syndrome admits epsilon_a=0, and each local view has at most Delta² qubits,

    sum_a |epsilon_a| <= Delta² |v|_V,
    Z=sum_a epsilon_a,       |Z|<=Delta² |v|_V.

Validity ensures Z lies in the span of local row/column codewords. Let g0=sum_(a in V01) epsilon_a; then |g0|<=Delta² |v|_V. Suppose the mismatch algorithm fully decomposes Z with parameter delta<1. Its flips f_i satisfy

    sum_i |f_i| <= |Z|/[kappa(1-delta)].

The proof's local syndrome identities show H(e+g0+sum_i f_i)=0, WITHOUT needing |e| small. Thus

    z=g0+sum_i f_i,
    Hz=v,
    |z| <= Delta² [1+1/(kappa(1-delta))] |v|_V.

This is the sought filling conditional on complete decomposition. No logical-correctness assumption is needed because we deliberately quotient by the full kernel.

## Where the proof stops, quantitatively
Let ||Z|| denote minimal row/column decomposition norm. While greedily reducing Z, robustness and total descent give a sufficient bound

    active_vertices <= ||Z|| + |Z|/[kappa Delta(1-delta)].

To invoke theorem4.10, this must be <=

    2^-12 d_r² delta³ kappa |V00|.

A bound ||Z||<=C'|v| (or another uniform small-linear-radius version) would close this argument. The published proof instead reaches this threshold by substituting a bound in terms of |e|_R. For arbitrary absolute syndrome or an arbitrary preimage, that quantity can be extensive. Local corrections epsilon_a are NOT themselves row/column codewords; their small total support does not supply the missing small decomposition. The identity expressing Z as local codewords uses e_a+epsilon_a and can involve extensively many terms.

This is a genuine failed proof step, not evidence that the desired property is false for these Tanner families. No appeal to linear distance repairs it: distance only distinguishes normalizers from stabilizers after a correction has been constructed.

## Why validity and bounded check degree alone are insufficient
A self-contained counterexample to that generic implication is the binary cycle incidence map: data on cycle edges, checks at vertices. A valid syndrome comprising two opposite vertices has weight two. Its preimages are the two connecting paths, and adding the full kernel (the whole cycle) merely switches the paths. The minimum preimage has weight floor(N/2). Thus even quotienting by the entire kernel does not make sparse valid syndromes generally fillable. This is NOT a counterexample to quantum Tanner codes or their expansion hypotheses.

## Operational boundary
Even proving the missing norm inequality would only remove a geometric obstruction. The nearest-valid-syndrome map and extensive frame must be computed, communicated, and maintained during actual noisy elapsed time. No instantaneous classical decoder, noiseless long-lived absolute syndrome, or small physical-error assumption on an extensive frame is supplied by this derivation. The separate alternating-Tanner-graph known-state-preparation comparator reported by the parent should be assessed on that same feedforward-time boundary; it is not contradicted by this note.
