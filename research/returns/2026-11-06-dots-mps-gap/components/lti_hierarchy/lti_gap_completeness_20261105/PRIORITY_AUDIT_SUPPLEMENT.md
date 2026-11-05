# Independent priority and assumptions audit

Checked 2026-11-05 against primary sources. This is a targeted literature audit, not a proof of novelty or an independent verification of the boundary-repair proof.

## Finding

I found no published theorem that directly implies exact convergence of the unrestricted Rai Eq. (17) hierarchy to the periodic finite-size gap limit under the candidate's proper injective-parent hypotheses. The standard parent-gap and finite-size-criterion theorems establish positive detection and lower bounds tied to open-chain gaps. They do not supply the final periodic comparison used by the candidate.

Crucially, **open-chain and periodic gap equality is false within the exact promised class**, including for entangled injective MPS. Therefore it cannot be used to turn the already published open-chain convergence into the claimed result.

## Exact source locations

### Rai et al., Quantum 10, 2065 (2026), arXiv:2411.03680v3

- [Eq. (17)](https://arxiv.org/html/2411.03680v3#S2.E17) is the unrestricted LTI dual with energy normalization and the nearest-neighbor objective used in the candidate.
- [Section 3.2, Eqs. (34)–(37)](https://arxiv.org/html/2411.03680v3#S3.SS2) proves inclusion of the previous finite-size criteria. Eq. (37) only bounds the hierarchy limit below by the open-chain gap limit. The following paragraph explicitly leaves convergence to the thermodynamic gap open. The martingale inclusion is formulated for their coarse-grained Hamiltonian, so it should not be silently treated as a same-level inclusion for an arbitrary unblocked interaction.
- [Section 5](https://arxiv.org/html/2411.03680v3#S5) again distinguishes detecting a positive gap from convergence to the actual gap and leaves completeness unresolved.

Consequently, one should not characterize positive-gap detection for proper parents as the proposed advance. The extra claim is exactness for the periodic gap.

### Rozmán, Molnár, Schuch, arXiv:2607.19078v1

- [Section 3.2](https://arxiv.org/html/2607.19078v1#S3.SS2) uses eventual equality of the open-chain kernel with the MPS boundary space as its parent hypothesis. It explains why a sufficiently large single-block equality can imply eventual equality and why normal parents have unique large periodic ground states.
- [Theorem 6](https://arxiv.org/html/2607.19078v1#Thmtheorem6) proves uniform gaps for both open and periodic normal/block-normal parents. This supplies the candidate's uniform open gap, without supplying equality of gap values.
- [Section 4.4, “Convergence to infinite system value”](https://arxiv.org/html/2607.19078v1#S4.SS4.SSSx2) proves convergence of the Lemma-2 periodic lower bound to limsup of the open-chain gaps. With equal weights the bound is (1−2γ_pq)ρ_pq Δ(H^OBC_(2p+q)); it is not asserted to converge to the actual periodic gap.

Thus the existing audit correctly distinguishes this paper's convergence claim from the candidate. It would be inaccurate to say this paper has no convergence theorem at all.

### Classical parent-gap background

[Nachtergaele, “The spectral gap for some spin chains with discrete symmetry breaking,” CMP 175, 565–606 (1996), arXiv:cond-mat/9410110](https://arxiv.org/html/cond-mat/9410110) has the directly relevant **Theorem 2**: positive finite-range interaction, the prescribed GVBS ground-state face, and eventual equality ker H_[M,N]=G_[M,N] imply a uniform open gap and a GNS gap lower bound. The paragraph immediately after the theorem warns that agreement of the infinite ground-state face does not imply the finite-interval kernel equality. **Proposition 12, Eq. (6.10)** supplies the quantitative gap estimate. These are positivity results, not equality of open, periodic, and GNS gap values.

The candidate's proper-parent assumption is therefore a classical substantive hypothesis, rather than an innocuous reformulation of “unique injective-MPS infinite ground state.”

## Explicit obstruction to an open/periodic shortcut

This calculation is independent of the cited papers.

Take qubits and h=I−|00⟩⟨00|. It is positive, nearest-neighbor, translation invariant, frustration free, and has norm one. For every open interval of length N≥2,

    ker H_N^OBC = span{|0⟩^⊗N} = S_N.

The tensor A^0=1, A^1=0 is an injective D=1 tensor, with primitive transfer map and faithful scalar fixed point. Hence every precise proper-parent assumption in the candidate is met.

The Hamiltonian is diagonal. Any nonvacuum bit string on an open chain violates at least one bond; a single 1 at an endpoint violates exactly one. Therefore Δ_N^OBC=1. On a ring N≥3, any nonvacuum string violates at least two bonds, and a single 1 realizes two. Therefore Δ_N^PBC=2. Both limits exist and differ.

This is not only a D=1 exception. Given any entangled proper injective parent H_A with uniform open and periodic gap lower bound g>0, form the decoupled tensor-product system

    H_total = H_A ⊗ I + ε I ⊗ H_product,

where 0<2ε<g. It remains a proper injective parent: its open kernel is S_N(A)⊗span{|0⟩^⊗N}, and its MPS bond dimension remains D_A. Since the spectra add, its large open gap is ε and periodic gap is 2ε.

The counterexample disproves a general open/periodic equality shortcut. It is **not** a counterexample to LTI completeness.

## Additional prior-art screen

- [Rao, arXiv:2510.08427v2, Section 6.2](https://arxiv.org/html/2510.08427v2#S6.SS2): finite-system convergence of a different representation-theoretic NPA hierarchy, with exactness at system-size-dependent level. This does not identify the thermodynamic fixed-window Rai limit.
- [Xu et al., arXiv:2606.03836v5](https://arxiv.org/html/2606.03836v5): Supplementary Theorem 2.5 is a complete upper-bound hierarchy; Theorems 3.1/3.2/3.6 concern general bulk-gap undecidability. None gives the candidate's proper-parent lower-bound conclusion. Their hypotheses and bulk definition must not be silently substituted for the candidate's.
- Newly located adjacent source: [Scheer and Khalaf, arXiv:2610.18854v1 (13 October 2026)](https://arxiv.org/html/2610.18854v1). Section I.1 restates the Rai approach as translation-averaged sums of squares. The work treats pseudopotentials, exact rational feasibility, and stability of a parameterized SDP limit. It does not state completeness or exact convergence of Rai's hierarchy for injective-MPS chains. “Exact lower bounds” here means rigorously certified values, not convergence to the exact gap.

## Recommended statement of the contribution

Subject to proof review and a wider novelty check: “Exact convergence of the existing unrestricted local-translation-invariant lower-bound hierarchy to the periodic finite-size gap limit for proper injective-MPS parent chains.”

Do not claim a general 1D completeness theorem, first positive-gap detection for MPS parents, equality with the open-chain gap, or an independently proved identification with the GNS gap. The candidate's decisive additional step is the dual-to-periodic excitation comparison; standard exponential transfer mixing and standard parent gappedness are inputs, not the novelty claim.

No external actions or author correspondence were undertaken. No access denial blocked this audit.
