# E9 derivation: near-idempotent, self-compatible channels

## Provenance and exact interface

Pinned Astra snapshot: `harjassand/astra-research-knowledge` commit `8aed7fd74eb14622ed5a0a3635a799374296e32a` (2026-10-10). The entrypoint is `work/sources/astra/00_START_HERE.txt`. `frontier/PRIORITIES.md` is absent from the sparse working tree but present in the pinned Git tree; read through `git show HEAD:frontier/PRIORITIES.md`. The relevant current record is gate `G-BQ-N533`, order 90, in `frontier/OPEN_PROOF_GATES.jsonl`; its status is open. The current-status row calls N533 `source_derived_unreviewed`, with proof text located but not completeness-audited. The evidence report hash is `4f2fcc30d6dedf19df4d770b92edf782ce33be789102e65807b570e2f8472580` (verified against the pinned blob). The report itself says its Kitaev import was not fully reconstructed and historical priority is unknown.

Use finite-dimensional Hilbert space H, d=dim H. Let Φ:T(H)→T(H) be CPTP and let C:T(H)→T(H⊗H) be a channel whose marginals Φ₁,Φ₂ satisfy `||Φ_j−Φ||⋄≤τ_j`; exact self-compatibility is τ₁=τ₂=0. Let `η=||Φ²−Φ||⋄`.

Kitaev, Theorem 12.3, applied to the Heisenberg dual of Φ, supplies a finite-dimensional C*-algebra A and CPTP maps D:T(H)→A_* and E:A_*→T(H), with universal but implicit constants β≤C₁η and γ≤C₂η such that

`||Φ−ED||⋄≤β`, `||DE−id_{A_*}||⋄≤γ`.

The first bound is the dual of the theorem's `||ΔΥ−Φ*||cb=O(η)`. For the second, set one argument to the unit in its multiplicative estimate to obtain `||ΥΔ−id_A||cb=O(η)`, then dualize. These are complete-norm statements; no constants or smallness cutoff are supplied in the Astra report.

## Transfer theorem reconstructed here

**Claim, conditional only on the stated factorization interface.** If

`τ₁ + τ₂ + 2β + 4γ < 1`,

then A is commutative, so Λ=ED is entanglement breaking and `||Φ−Λ||⋄≤β`. In particular, exact self-compatibility plus sufficiently small η gives a dimension-independent `O(η)` diamond approximation by a measure-and-prepare channel.

**Proof.** Suppose A has a summand M_m with m≥2. Embed a qubit into a two-dimensional corner using a channel i:T(C²)→A_*. Retraction r:A_*→T(C²) compresses to that corner and sends all remaining trace to a fixed qubit state; `r i=id`. Define

`Q=(rD ⊗ rD) C E i`.

This is a physical qubit broadcaster. Its jth marginal is `rD Φ_j E i`. Contractivity of channels in diamond norm gives

`||DΦ_jE−id||⋄ ≤ τ_j + ||D(Φ−ED)E||⋄ + ||(DE)²−id||⋄ ≤ τ_j+β+2γ`,

because `DΦE−id = D(Φ−ED)E + (DE)²−id`, and

`||(DE)²−id||⋄ ≤ ||DE(DE−id)||⋄+||DE−id||⋄ ≤ 2γ`.

Pre/post-composition with i,r preserves the bound. For any qubit broadcaster with marginal errors d₁,d₂ from identity, feed half of a normalized Bell pair Ω_RQ into Q and call the output ω_R12. With `P₁=Ω_R1⊗I₂`, `P₂=Ω_R2⊗I₁`, the diamond bounds give `Tr(P_jω)≥1−d_j/2`. The isometries `V₁x=Ω_R1⊗x₂`, `V₂y=Ω_R2⊗y₁` have cross-Gram `V₁*V₂=I/2`; hence `||P₁+P₂||=1+1/2=3/2`. Therefore

`2−(d₁+d₂)/2 ≤ Tr((P₁+P₂)ω) ≤ 3/2`, so `d₁+d₂≥1`.

But the constructed Q has `d₁+d₂≤τ₁+τ₂+2β+4γ<1`, a contradiction. Thus every summand is one-dimensional, A≅C^k. D is a POVM and E prepares a state per classical outcome, so ED is entanglement breaking. ∎

Taking β=C₁η, γ=C₂η, a valid exact-self-compatibility cutoff is any

`η₀ < min(η_K, 1/(2C₁+4C₂))`,

where η_K is the (implicit) range in which Kitaev's factorization applies. The output error is at most C₁η. This is a derived corollary, not a newly proved factorization theorem.

## Why full diamond control is necessary

For d≥3 define

`W_d(X)=(Tr(X)I−Xᵀ)/(d−1)`.

Its normalized Choi state is `(I−F)/(d(d−1))`, supported on the antisymmetric subspace. The maximally mixed state on Λ³C^d has this state as each two-body marginal and maximally mixed one-body marginal, so W_d is self-compatible.

Let `D(X)=Tr(X)I/d`, T be transpose, and a=1/(d−1). Then `W_d=D−a(T−D)` and direct multiplication gives

`W_d²−W_d = a(T−D)+a²(id−D)`.

For every unentangled density input ρ, both `T(ρ)` and `D(ρ)` are states, as are ρ and D(ρ); hence

`||(W_d²−W_d)(ρ)||₁ ≤ 2a+2a² → 0`.

Yet the antisymmetric-projector probability is 1 on the Choi state of W_d and at most 1/2 on any separable state (on a product vector it is `(1−|⟨x,y⟩|²)/2`). Every entanglement-breaking channel has separable Choi state. Thus `inf_{EB Λ}||W_d−Λ||⋄≥1`. Indeed the same witness shows `||W_d²−W_d||⋄≥d/(d−1)`. So product-input or statewise idempotence tests cannot replace the complete diamond premise; the apparent small defect hides an order-one reference-system failure.

## A small proof repair checked independently

The pinned report identifies a real issue in directly summing component unitary 1-designs for A=⊕_j M_{m_j}. For independent block indices, the (j,k) off-diagonal block of the proposed diagonal contains `E(U_j†)⊗E(U_k)`, which need not vanish; taking the one-element design `{I}` in two blocks already fails the desired centrality identity. Replace each block ensemble `{U}` by the sign-symmetrized ensemble `{+U,−U}` with half weights. Its diagonal term `U†⊗U` is unchanged, so each component design identity survives, while `E(U)=E(U†)=0`. Independence then kills every j≠k cross-block term, restoring the direct-sum identity. This repairs that local step; it does not audit the rest of the 48-page imported theorem.

## Resource interface and capability ceiling

The structural payoff is concrete: once a full channel C witnesses self-compatibility and a complete-norm certificate verifies η, every invocation of Φ can be replaced by the measure-and-prepare Λ with diamond error β. A hybrid argument gives error at most `tβ` for any t-use adaptive protocol with arbitrary quantum memory/reference. Also, for any k≥1, `ΛΦ^{k−1}` is EB and within β of `Φ^k`. This yields an operational channel-classicality statement, not automatically a classical computer simulation: the POVM, prepared states, and their implementation may still be expensive.

Dense-input model: a d→d channel Choi matrix has O(d⁴) entries; a d→d² broadcasting extension has O(d⁶) Choi entries. Self-compatibility is a convex/SDP feasibility condition on the extension, and diamond norms admit SDP formulations, but these matrix dimensions are exponential in qubit count n when d=2^n. The primary Kitaev theorem gives universal O(η) existence bounds, not numerical constants, bit complexity, or a system-size-efficient map from a succinct circuit to D,E. Thus the exact missing computational primitive is:

> Given a succinct finite-dimensional circuit/oracle description of Φ, a certified two-extension C, and an efficiently verifiable complete-norm upper bound η, construct a POVM/preparation representation Λ with a certified `||Φ−Λ||⋄≤Cη+ε`, with runtime and query/sample costs polynomial in the succinct input size and log(1/ε), under an explicit structural promise that avoids full Choi expansion.

The first two certificates alone are already expensive for generic n-qubit channels: the N533 W_d family rules out replacing the complete-norm premise by unentangled statewise tests. Any practical route needs an explicit locality, tensor-network, symmetry, or oracle promise and must charge entangled probes, preparation, estimation precision, and memory. The theorem is finite-dimensional; no direct extension to the infinite-dimensional thermal attenuator or its energy-constrained capacity follows.

## Literature and validation status

- Primary source: A. Kitaev, *Almost-idempotent quantum channels and approximate C*-algebras*, arXiv:2405.02434v2 (11 Feb 2025), Theorem 12.3, printed pp. 44–46: https://arxiv.org/abs/2405.02434v2 and https://arxiv.org/pdf/2405.02434v2 . It states the UCP factorization/multiplicativity bounds with universal O(η); I have reconstructed only the transfer after those bounds, not the full source proof.
- Primary compatibility reference: M. Girard, M. Plávala, J. Sikora, *Jordan products of quantum channels and their compatibility*, Nature Communications 12, 2129 (2021): https://doi.org/10.1038/s41467-021-22275-0 . It formulates channel compatibility as an SDP/convex feasibility problem. This supports the dense finite-dimensional certificate model, not polynomial efficiency in qubit count.
- Targeted searches found these primary sources and related compatibility work, but did not establish historical priority for this corollary. The Astra status remains source-derived, unreviewed, externally unverified, and priority-unknown.
