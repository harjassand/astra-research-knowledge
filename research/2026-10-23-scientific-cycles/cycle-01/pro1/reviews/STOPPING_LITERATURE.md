# Targeted predecessor check: expected stopping cost and quantum feedback

Reviewer: `/root/stopping_literature`. Date: 21 October 2026.

Scope: compare the new expected-use operation with primary literature. This is not a fresh audit of the settled tree capacity, a general priority search, or external certification. No people were contacted.

## Main conclusion

The lottery mechanism and failure of a strong converse under an expected-length constraint have direct classical predecessors. They should not be described as a newly discovered information-theoretic phenomenon. The scientifically useful addition in the current tree programme is the stopped, unnormalized quantum subchannel bound for an adaptive correlated memory process, and its extension to every fixed normal coherent bath without incorrectly comparing unbounded expected costs after truncation.

The formula proposed by the owner, minimum expected uses asymptotic to `f log2(K)/(3/2)` at fixed entanglement fidelity `f`, is the quantum tree analogue of a familiar classical epsilon-capacity law. The tree-specific proof remains necessary: the cited classical theorems do not prove this quantum statement.

## Closest explicit length/error predecessor

Y. Polyanskiy, H. V. Poor and S. Verdú, *Feedback in the Non-Asymptotic Regime*, IEEE Transactions on Information Theory 57(8), 4903–4925 (2011). Primary author-hosted manuscript:

https://www.mit.edu/~6.454/papers/vbf_journal.pdf

Theorem 1 gives variable-length epsilon-capacity `C/(1-epsilon)` for non-anticipatory classical channels having a fixed-blocklength strong converse. Theorem 2 gives that first-order law for DMC feedback codes; Theorem 4 supplies a converse. The proof of Theorem 2 explicitly randomizes between immediate termination and a longer code. Footnote 6 says the decoder can implement that choice using stop feedback, so initial common randomness is unnecessary. The Appendix proof of Theorem 1 also uses send-or-send-nothing randomization and a bounded stopping cutoff.

These are classical message-decoding results. The present task uses entanglement fidelity for an arbitrary quantum logical system, a closed infinite memory, and a cost uniform over logical input states. Those distinctions prevent importing their conclusion without the owner's quantum proof. Nonetheless, the same `1/(1-epsilon)` law and elementary randomization are clear predecessors.

Retrieval: primary PDF, Theorems 1–4, Theorem 2 proof and Appendix Theorem 1 proof read. Useful browser refs: `turn60view0`, `turn61view0`, `turn63view1`, `turn63view2`.

## Inherited Schmidt-number facts

Barbara M. Terhal and Paweł Horodecki, *A Schmidt number for density matrices*, Physical Review A 61, 040301(R) (2000):

https://arxiv.org/pdf/quant-ph/9911117

Proposition 1 proves LOCC monotonicity. Lemma 1 bounds the maximally entangled overlap of a state of Schmidt number at most `k` on `N x N` by `k/N`. The bounded Schmidt-number classes are compact convex sets in finite dimension. These directly precede the fidelity and measurable-mixture ingredients. They do not by themselves justify rearranging an adaptive causal device: that is the supplied frozen-transcript lemma's responsibility.

Primary PDF read; useful refs: `turn59view0`, `turn60view2`.

Dariusz Chruściński and Andrzej Kossakowski, *On partially entanglement breaking channels*, Open Systems & Information Dynamics 13, 17–26 (2006):

https://arxiv.org/pdf/quant-ph/0511244

Theorem 1 and its proof state the finite-dimensional equivalence between a channel Choi state's Schmidt number at most `r` and a Kraus representation whose every operator has rank at most `r`. Their vector/operator correspondence also makes the rank-preservation mechanism transparent. This is an established invariant, distinct from the number of Kraus operators.

Primary PDF read; useful refs: `turn60view1`, `turn61view3`, `turn63view3`.

## Infinite-dimensional caution that materially affects scope

M. E. Shirokov, *The Schmidt number and partially entanglement breaking channels in infinite dimensions* (2011):

https://arxiv.org/pdf/1110.4363

The abstract and Sections 1 and 5 show that the finite-dimensional equivalence above fails for general infinite-dimensional channels: even entanglement-breaking channels can have only infinite-rank operators in every countable Kraus representation. Countable pure-state decompositions can likewise be insufficient.

This does not obstruct the current proof. At each fixed cutoff horizon, the external input/output block and the logical Choi space are finite-dimensional. The tree bath is infinite, but an explicit vertex-indexed Kraus family is already supplied. Measurable mixtures are taken in a finite-dimensional closed cone. No infinite-dimensional equivalence is needed, and the text should say so.

Primary PDF introductory statements and theorem context read; useful ref: `turn59view1`.

## Adjacent quantum expected-cost literature, not the same operation

Anurag Anshu, Ankit Garg, Aram Harrow and Penghui Yao, *Expected communication cost of distributed quantum tasks*:

https://arxiv.org/abs/1605.04601

The primary abstract describes expected-length entanglement-assisted classical communication for distributed pure-state tasks and related fully quantum redistribution results. It confirms that expected quantum communication cost is an established research subject. Its ensemble/source and resource contract differ from transmitting an unknown reference-entangled logical state through this fixed closed reservoir. Only the primary abstract was read here; no theorem from its full manuscript is used.

Useful ref: `turn63view0`.

## Assessment of the proposed new proof operation

The proposed cutoff inequality is more than an analogy to classical Fano or optional-stopping proofs. It uses a positive subchannel whose Schmidt-number bound holds before normalization, and evaluates its overlap with one fixed maximally entangled projector. The complementary long branch is bounded by its probability. Consequently it need not assume a branch probability independent of input or a tensor-product channel across uses.

For a coherent normal bath, bounded-prefix trace-distance continuity is the correct order of operations. Applying initial-state continuity directly to the mean of an unbounded stopping time would be unjustified: trace distance controls bounded tests, not arbitrary unbounded cost observables. A finite vertex-coordinate cutoff followed by a bounded stopping cutoff avoids that error. The owner and the separate converse reviewer must establish this formally; literature comparison does not certify it.

The upper construction should explicitly distinguish deterministic transmission (the all-branch logical map is trace preserving) from deterministic duration or zero error. A randomized run-or-abort code can be deterministic in the first sense while having a positive average error. Its abort branch must remain in the entanglement fidelity, and its two possible durations must both be charged. The construction does not increase reliable capacity; it refutes a strong-converse claim for that changed cost contract.

## Search limits and novelty language

Four rounds of focused searches were used, followed by primary-source retrieval. Queries targeted variable-length quantum feedback, expected communication cost, strong converse and Schmidt number. Routine search had poor coverage, so stronger search was used. Retrieved variable-length quantum source-coding and QKD papers concern different output/resource definitions and were not used as task theorems.

No exact prior theorem for this tree device's expected-use frontier was found in this bounded search. That is not evidence of historical priority. Appropriate claim: a proved model-specific extension using established Schmidt-number and variable-length ideas, with the full mathematical contract stated. Inappropriate claims: first failure of a strong converse under an expectation constraint, a new Schmidt-number invariant, or a general theorem that classical feedback cannot help quantum communication.

Observed work: primary-source search and reading; no numerical experiment, hardware operation, external compute job or outreach. Model compute, energy and complete monetary costs were not measured.
