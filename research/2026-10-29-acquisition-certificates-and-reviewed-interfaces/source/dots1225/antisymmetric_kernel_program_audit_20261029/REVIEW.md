# Independent receiving review: correlated-record kernel gate programs

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`, not an author of frozen v1. Decision: **accept exact conditional capability, with the frozen common-single-label-support correction below**. No iid assumption is needed for correctness. No acquisition rate, robustness, practical architecture, historical novelty or operational advantage is accepted.

## Required precision correction (now frozen by the author)

`SUPPORT_WORDING_ERRATUM_v1.md`, bound by `ERRATUM_SHA256SUMS.txt`, incorporates this correction and is required with v1.

The v1 sentence 'If the joint occupied label support has dimension<8, this event has probability zero' must mean: **all eight label factors are supported in a common single-label subspace of dimension below eight**. Low rank of the joint eight-register density operator does not suffice: a pure normalized antisymmetric eight-label state has joint rank one and exterior-projection success one. The common-subspace reading is what the dimension argument and rank-deficient tests establish. This correction does not change the general correlated-state theorem or iid example.

## 1. Full memory and exterior projection

I read the actual one-call CP Kraus construction in `coherent_commutator_acquisition_20261029/GOVERNING.md`, rather than inferring a repeatable density-matrix oracle. For every acquisition Kraus amplitude, contraction of the fresh minus-label index with real c is proportional to sum_j c_j(K P_j-P_j K)=0 under the fixed full-joint commuting-swap promise. This is an operator equality on source memory, not only a scalar expectation on a sampled marginal. It therefore holds with arbitrary old-label/reference entanglement. Each new minus record lies in c-perp on that factor; subsequent source operations acting only on source memory/carriers cannot enlarge the support of an isolated earlier label. Successive retained labels are supported in (c-perp)^tensor8 without being iid or uncorrelated.

The normalized epsilon rows have 8! entries of magnitude1/sqrt(8!) with disjoint missing-label supports. Thus A_w A_w†=I9 and A_w† A_w=P_antisym. The exterior image of an eight-dimensional single-label subspace is one-dimensional. Its Hodge image is conjugate(c), not c for general complex c. The rotation coefficients here are real. Every positive joint output supported on this one-dimensional program factor has the form |c><c| tensor tau, so exact conditional decoupling includes all source memory, old records and references. Zero output is allowed. Preparing a second successful pure program leaves the first protected program in product with it, even if acquisition success events were correlated.

No claim applies to bath-controlled superpositions of different frames, a scalar Gram kernel valid on just one memory marginal, or leaked/subject-to-source label registers. The full-joint, fixed-real-frame premise remains essential.

## 2. Known-control circuit and decoder

Uniform radix selectors 8,7,...,2 supply 8! equally weighted strings in 17 encoded qubits. The Fisher–Yates choice-to-permutation map is bijective. Preparing selectors, applying permutation sign and controlled permutation, then unpreparing and postselecting produces exactly (1/8!)sum sign(pi)U_pi=P_antisym. This does not multiply a successful projection by an extra 1/8! in probability. The 28 addressed register swaps (excluding self-swaps) give 112 addressed bit swaps for four-qubit label encodings; these are multi-controlled primitives, not 112 native two-qubit gates.

Within the projected subspace labels are distinct. Coherently computing the missing label, sorting to its canonical complement while storing reversible choices, and erasing that known canonical list is an isometry on this subspace. The remaining selector amplitudes have the parity of the sorting permutation, independent of the missing label; reversing their known signed uniform preparation cleans them. The epsilon convention has additional phase (-1)^a for missing label a, which the stated correction removes. This realizes A_w after projection. The action can be extended arbitrarily to a full unitary on unused/invalid encoded states. Reversible comparison/search/ancillas, resets, rotations and routing are additional paid controls; the packet does not provide a complete native gate count for this decoder.

## 3. Transducer and gate orientation

The exact rational A has shape16×81. Replayed symbolic identities prove A vec(R(q))^tensor2=(q.q)vec(qq^T) for arbitrary real q. I separately derived R from R_ij=Tr[sigma_i V(q) sigma_j V(q)†]/2, with V=wI-i(xX+yY+zZ), and verified the same identity, checking orientation rather than reusing the displayed rotation formula.

The retained exact LDL factorization proves I16-AAᵀ positive definite. An independent exact spectrum is {1/4 once,1/2 nine times,0 six times} for AAᵀ, hence A is contractive on all inputs, not just rotation-program inputs. For normalized c=vecR/sqrt3, output is q tensor q /3 and success1/9. The operator may be dilated using known finite-dimensional algebraic controls; this existence is not a calibrated native implementation. The q↔-q ambiguity changes neither q tensor q nor the resulting unitary channel.

The basis map q↦|V(q)>>/sqrt2 is unitary from four quaternion labels to two-qubit Bell space. With the output/input Choi ordering fixed, projecting the payload and input half onto the identity Bell state gives exact Kraus V/2; therefore the all-input/reference-preserving successful subchannel is V rho V†/4. Other Bell outcomes are failures, not universally correctable known gates. The unchanged frozen A therefore gives1/36 for transduction plus one successful gate and1/144 for two gates. Failure can damage a payload; any error-detecting/erasure architecture remains a separate obligation.

## 4. Yield and exactness

For iid normalized rank-eight sigma, Tr(P_antisym sigma^tensor8) is the eighth elementary symmetric polynomial, equal to the product of the eight nonzero eigenvalues. AM–GM bounds it by8^-8. This bound is iid-specific, not an upper bound for arbitrary correlated input states. For unnormalized H^T/18 it is product_nonzero(H)/18^8, including all minus outcomes.

Exact two-axis source replay gives eigenvalues {0 once,1/2 three times,1 twice,3/2 three times}, minus probability4/9 and eight-call program probability1/26121388032. This establishes a nonzero example, not a uniform rate. Two batches require 16 source calls before subsequent gates; unrestricted retry may never finish. Common dark subspaces, identity sources and some one-axis sources can produce zero success. Approximate symmetry and false heralding are particularly dangerous because normalization can magnify contamination by inverse success probability. None of this is removed by exact conditional correctness.

## 5. Evidence and priority

All frozen author/core and primary-comparison manifests checked. Replayed exact symbolic/LDL transducer checks, 100 numerical transducer cases, 120,960 exact decoder permutation checks, complex correlated-memory exterior tests in dimensions3–5, and the exact physical two-axis example. Reviewer additions use exact d=9 Hodge minors for three nontrivial/identity rational frames without materializing9^8 space, independent symbolic adjoint orientation and teleportation contraction, and exact A spectrum. These are proofs and mathematical/computational tests, not laboratory acquisition.

Primary sources read directly on2026-10-29: Miyazaki–Soeda–Murao, https://arxiv.org/abs/1706.03481 and governing PDF https://arxiv.org/pdf/1706.03481 (Levi-Civita/conjugate representation machinery); Quintino et al., https://arxiv.org/abs/1909.01366 (heralded unitary transformations). These establish relevant conventional machinery, not novelty of this composition. An equally informed quantum controller can use the same records and exterior operation; classical tomography is not the only fair comparator.

A separate reviewer-originated symmetrized transducer candidate improves constants. It is deliberately excluded from this independent receipt and needs another reviewer; see `SYMMETRIZED_TRANSDUCER_CANDIDATE.md`. Acceptance here concerns the original A and probabilities, not that new construction.
