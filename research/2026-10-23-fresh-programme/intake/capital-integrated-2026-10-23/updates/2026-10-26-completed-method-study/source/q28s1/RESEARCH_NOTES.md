# Q28 stage 1 research notes

Started 26 October 2026, approximately 08:27 UTC. All study reads are limited to the Q28 assignment and public starting packet. External primary literature is allowed. No other trial or private evaluation material is used.

## Three mechanisms considered before selecting the main construction

1. **Selective materials assembly.** Retain a fragment handle and use a fuel-driven reverse pathway to remove wrong joins. The relevant missing operation is recognition of correct site/orientation in the actual covalent joining regime. The public packet does not supply it. Zhu, Du, King and Brenner's colloidal proofreading proposal uses local recognition rules and patchy particles; this is not yet a compatible covalent-polymer recognition operation. It would be unsound to assume this bridge. Primary source: https://arxiv.org/abs/2312.08619 . This mechanism is outside the inherited information-theoretic formalism.
2. **Reliable large atom arrays.** Add a continuously supplied reservoir and coherent replacement to obtain indefinitely maintained qubits. Strong incumbent operations already include reservoir loading, transport, initialization and coherence-preserving replacement: Li et al., https://arxiv.org/html/2506.15633v1 ; continuous operation of a 3,000-qubit system, https://doi.org/10.1038/s41586-025-09596-6 . Average occupancy is not joint reliable completion, but a mere repair scheduler would not create the demonstrated missing physical operation. The useful mathematical question would be joint completion with incomplete observations, for which optimal state-estimation/control is an incumbent rather than a straw comparator.
3. **Hybrid dissipative memories.** Change representation from one full matrix algebra to a classical/quantum direct-sum algebra with a biased reset. This models superselection labels or hybrid registers whose reset equilibrium is not uniform. The full-matrix Astra theorem explicitly does not settle arbitrary multi-matrix inclusions. The question is whether the complete-index law determines information loss here, and, if not, what the true governing quantity is. Primary operations are ordinary stochastic reset on labels, arbitrary untouched quantum side information, and relative-entropy distinguishability; no physical primitive is assumed.

## Selected initial question

Can the sharp complete-index reset law be extended to biased classical/quantum hybrid memories, giving a rigorous general information-loss law beyond full matrix inclusions?

This is a mathematical route to a consequential memory/noisy-computation target. It is not a claim to construct a hardware memory or to beat error correction. A complete answer must compare the established contraction-coefficient framework and ordinary scalar optimization. Any routine corollary, rediscovery, or unresolved estimate will be reported at that scope.

## Governing evidence

The exact public N967 governing source has been saved as `sources/N967_governing.md`. It attributes the needed unitary-basis theorem to Crann, Kribs and Pereira. Its noncommuting-reference simplex sharpness construction explains why ordinary scalar-channel contraction need not give the complete coefficient for three or more labels. It does not claim the biased hybrid extension.

Hirche, George, Nuradha and Wilde, https://arxiv.org/abs/2608.27171 , already introduce conditional contraction coefficients and connect relative entropy with conditional mutual information. This framework and its network applications are antecedents, not inventions of this trial.

## Construction log

The first proposed extension is to replace the full-matrix index by the weighted classical reset index `1/min(p_i)`. Before any theorem is asserted, the binary case will be tested by exact BKM generalized-eigenvalue calculations with noncommuting finite reference matrices. The purpose is to detect whether the index is sufficient and whether an explicit optimizing family can be constructed.

### Decisive failure and substantive pivot

The proposed index-only extension is false. For the biased binary reset with p=(1/4,3/4), lambda=1/2 and weighted commutative complete order index C=4, the exact conditional coefficient is `(19-sqrt(105))/32 = 0.2735327885637626`, while the transplanted formula is 3/8. This is outside the full-matrix ordinary-trace theorem's scope. It is not a refutation of N967 and does not require treating an internal accepted proof as inadequate.

The stronger construction is a general binary-input comparison theorem rather than another reset-parameter interval. Normalizing the two BKM superoperators X,Y by their sum produces Q,I-Q, which commute even when the underlying reference matrices do not. A complete operator square identity then lifts **any** scalar relative-entropy comparison between finite-output binary channels to arbitrary finite quantum conditioning, including unequal reference marginals. The ordinary scalar distributions already supply sharpness. The full proof is in `binary_channel_proof.md`.

This yields sharp CMI comparisons with arbitrary quantum auxiliary systems and product-register less-noisy order comparisons for every finite number of uses. It does not yield arbitrary Bayesian-network replacement or dimension-independent product contraction. The latter would already fail for a repeated bit sent through independent erasure channels.

### Executed diagnostics and numerical repair

The independent matrix-eigendecomposition/BKM calculations test seven channel comparisons, 2,800 finite matrix-state pairs across reference dimensions 1,2,3,5,8, and 168 whole-tangent-space local eigenvalue optimizations. Both equal and unequal marginals occur. An existing ternary simplex witness is a negative control: at epsilon=0.01 its matrix metric ratio is about 0.31657, exceeding the ordinary ternary coefficient 0.3. Thus the binary restriction is substantive.

The first numerical run emitted divide-by-zero/overflow/invalid warnings from BLAS matrix products although the returned comparison values were finite. It also overestimated the exactly flat BEC scalar optimum by about 3.1e-8 due to endpoint cancellation. These observations were not used as scientific evidence of a violation. The code was changed to explicit contraction for the relevant Gram products, all entries are checked finite, and scalar probabilities are evaluated as convex combinations. The rerun is warning-free and recovers the flat 0.72 BEC value. The original BLAS warning root cause has not been established. This numerical issue does not enter the analytic proof.

Four additional comparison bounds were certified with exact rational arithmetic and saved Sturm sequences. These certificates supplement the general theorem; the basic scalar rational-polynomial technique is an ordinary comparator operation, not a new invented search algorithm.

### Priority and mission assessment

Primary literature was searched beyond keywords and read at the relevant classical comparison, quantum-reference definition, CMI-equivalence, and metric-comparison boundaries. The classical KL/Fisher optimization, conditional-contraction framework, simplex witness, and complete-order tensorization technique are established antecedents. No failed keyword query is being used as proof of novelty. The binary operator lifting is independently constructed here, but historical priority remains UNKNOWN and there has been no independent audit.

This stage has a complete candidate mathematical unit and a decisive failed generalization. It has not constructed a device, an improved physical primitive, or a demonstrated civilisation-changing capability. The original broad mission remains NOT_ACHIEVED.
