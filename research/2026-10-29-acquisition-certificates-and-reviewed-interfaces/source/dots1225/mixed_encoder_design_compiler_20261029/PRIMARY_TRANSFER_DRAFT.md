# Common-design preparation of the compressed irrep
2026-10-29. Proposed additive compiler upgrade, not yet independently received.

After symmetric-group multiplicity extraction, prepare one known highest-weight vector in the small U(d) irrep, inverse small-d Schur, then apply the SAME random U(d) to every output register. Haar averaging replaces that irrep by its maximally mixed state and preserves the multiplicity, including external references. Thus no uniform enumeration of all Gelfand–Tsetlin patterns is intrinsically necessary. Independent random unitaries on individual outputs would NOT implement this operation.

For t output registers, an approximate unitary t-design controls this whole preparation channel. With logical k and padded junk rank powers of two, d is a power of two; the number of qubits per output is q=log2 d. If physical output dimension D is too small for the padding, D=O(kr) and direct small-dimensional tomography is available instead.

Primary source checked: Brandao, Harrow and Horodecki, arXiv:1208.0692v4, Definition2, Lemma3, Corollaries6–7. Their design definition implies diamond twirl error at most twice its error parameter. Corollary7 gives polynomial gate-length existence for a fixed inverse-closed universal algebraic SU(4) gate set, but its gate-set-dependent constant is not numerically specified. Corollary6 gives an explicit bound with Haar two-qubit gates. https://arxiv.org/pdf/1208.0692

This supports a polynomial gate-count existence transfer; it does NOT by itself supply an executable fixed budget or certified finite classical sampler. An explicit numerical gap for a chosen finite gate set, or a bounded finite-precision Haar-two-qubit sampler with charged error, is still needed for that stronger contract. The existing fixed-d enumeration compiler remains the completed fallback. No full uniform-rank runtime or actual native implementation is asserted by this draft.
