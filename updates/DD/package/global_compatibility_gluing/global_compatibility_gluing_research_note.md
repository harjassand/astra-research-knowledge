# Sharp Local-to-Global Compatibility via Packing and Reference-State Broadcasting

**Research note | 11 October 2026 | unsubmitted, unaudited manuscript**

**Status.** The arguments below are independently developed in this session, not formally verified or externally peer-reviewed. Claims of priority or novelty are **not established**. In particular, the two-output golden-ratio threshold appears in related 2026 bosonic pure-loss literature; channel/state marginal correspondence, quantum no-broadcasting, symmetric extendibility, and the matching polytope are established subjects. This note does **not** settle general quantum marginal consistency or any complexity separation.

## 1. Problem and conventions

All Hilbert spaces are finite dimensional. For a system family `V`, an observed context `C⊆V` has density matrix `ρ_C`. A consistent marginal family has the same reduced state on overlaps. For a graph, vertices are systems and edges are measured bipartite marginals. Let `τ_v=ρ_{v}`, `τ_S=⊗_{v∈S}τ_v`. Operator order is the usual Löwner order. The **universal product-domination radius** of a marginal system is the largest `t∈[0,1]` for which *every* locally consistent family `σ_C ≽ (1−t)τ_C` has a global positive semidefinite extension. A radius is uniform over all local marginals and leaf dimensions, subject to the specified central-system dimension. When `τ_v` is singular, restrict algebraic inverses to its support.

## 2. Fractional matching extension theorem

**Theorem 1.** Let `G=(V,E)` be a simple finite graph, with locally consistent two-system density matrices `ρ_e` and one-system states `τ_v`. Assume that `p∈[0,1]^E` is in the matching polytope of `G` and `ρ_e≽(1−p_e)τ_e` for all `e`. Then a global density operator `Ω` with `Ω_e=ρ_e` for every edge exists.

**Proof.** Write `p_e=Pr[e∈M]` under a probability law on matchings `M` (the definition of the matching polytope). For `p_e>0` set `ω_e=[ρ_e−(1−p_e)τ_e]/p_e`. This is a state with single-site marginals `τ_u,τ_v`; when `p_e=0`, domination and marginal normalization force `ρ_e=τ_e`, so no active ω is needed. For matching `M`, form `Ω_M=⊗_{e∈M}ω_e⊗_{v unmatched}τ_v`, with appropriate subsystem order. On edge `e`, the reduced state is `ω_e` if selected; if unselected the endpoints belong to disjoint factors and the reduced state is `τ_e`. Thus `Ω=E_M Ω_M` satisfies `Ω_e=p_eω_e+(1−p_e)τ_e=ρ_e`. QED.

**Spectral certificate.** For full-rank `τ_e`, the minimal required `p_e` is `γ_e=1−λ_min(τ_e^(−1/2)ρ_e τ_e^(−1/2))`. A rational vector `p_e≥γ_e` in the matching polytope is a directly checkable witness. On a simple graph the matching polytope is characterized by nonnegative edge weights, the constraints `∑_{e∋v}p_e≤1`, and odd-set constraints `∑_{e⊂S}p_e≤(|S|−1)/2` for odd `S`. With explicit rational certificates, verification and exact matching-mixture decomposition can be carried out in polynomial time, subject to standard bit-complexity treatment of the local matrices. This is a sufficient certificate, not an exact compatibility characterization.

## 3. Centered interaction decomposition and conflict-free packing

Let `𝒞` be downward-closed and let all `ρ_C` be mutually consistent. For `S∈𝒞` define `D_S=∑_{T⊆S}(−1)^{|S|−|T|} (ρ_T⊗τ_{S\T})`, with `ρ_∅=τ_∅=1`. Then `D_∅=1`, `D_{v}=0`, and for `|S|≥2`, `Tr_v D_S=0` for every `v∈S`: terms `T` containing `v` cancel those missing `v` using `Tr_vρ_T=ρ_{T\v}`. Möbius inversion gives `ρ_C=τ_C+∑_{S⊆C,|S|≥2}D_S⊗τ_{C\S}`.

On the set `𝒮={S∈𝒞: |S|≥2, D_S≠0}`, form a conflict graph `H` by joining `S,T` when `S∩T≠∅`, or when *some* observed context `C∈𝒞` contains `S∪T`. Let `γ_S=−λ_min(τ_S^(−1/2)D_Sτ_S^(−1/2))` for full-rank reference on S, with the inverse restricted to support otherwise. Each nonzero `D_S` is traceless and Hermitian, so γ_S>0 under full-rank τ.

**Theorem 2.** If `γ∈STAB(H)`, the stable-set polytope, the entire observed marginal family has a global extension.

**Proof.** Choose random independent set `J⊂𝒮` with `Pr[S∈J]=γ_S`. Define `ω_S=τ_S+D_S/γ_S`; it is positive, trace one, and has every proper marginal equal to the product reference. As supports in J are disjoint, `Ω_J=⊗_{S∈J}ω_S⊗_{v unmatched}τ_v` is a density matrix. Restrict to observed C. All intersecting-but-not-contained selected supports contribute no deviation because proper marginals of D vanish; by construction, no two selected supports lie wholly within C. Consequently `(Ω_J)_C=τ_C+∑_{S⊂ C,S∈J} D_S/γ_S ⊗τ_{C\S}`. Average and use Möbius inversion to get `ρ_C`. QED.

An explicit `q`-colouring of H provides a simple polynomially verifiable sufficient condition: `τ_S+qD_S≽0` for all S. Choose a colour uniformly and activate every S in that colour. This avoids a potentially NP-hard stable-set-polytope oracle at the cost of a stronger positivity requirement.

## 4. Exact universal radius on complete-graph pair marginal systems

**Theorem 3.** On `K_n` with arbitrary finite-dimensional local systems, the universal product-domination radius is

`R(K_n)=1/(n−1)` for even n, and `R(K_n)=1/n` for odd n.

**Sufficiency.** For even n, a 1-factorization partitions the edges into n−1 perfect matchings; for odd n, an edge-colouring partitions them into n matchings. Uniformly sample a matching and apply Theorem 1 with `p_e=1/(n−1)` or `1/n`.

**Necessity.** Take a qubit at each vertex, `τ_i=I/2`, and edge densities `σ_ij=(I−t Z_i Z_j)/4`. They dominate `(1−t)I/4` and have consistent uniform singletons. Any global extension, measured in the Z basis, yields signs `X_i∈{±1}` with `E X_i X_j=−t`. Therefore `E(∑_i X_i)^2=n−n(n−1)t`. For even n this is ≥0; for odd n it is ≥1 because a sum of an odd number of signs cannot vanish. These inequalities give the respective upper bounds. QED.

## 5. Optimal centered quantum broadcasting: a dimension dichotomy

For a d-dimensional quantum system, a fixed density matrix τ, and `0≤t≤1`, define `D_{τ,t}(X)=tX+(1−t)Tr(X)τ`. Let `b_{d,k}` be the largest t such that `D_{τ,t}` is k-self-compatible for *every* density matrix τ of dimension d.

**Theorem 4.** For integer k≥2:

`b_{1,k}=1`, `b_{2,k}=2/(1+√(4k−3))`, and `b_{d,k}=1/k` for all `d≥3`.

**Qubit construction.** For pure reference τ=|0><0| define |W_k>=k^(−1/2)∑_{i=1}^k|e_i>, where |e_i> has one 1 at site i. Put `a=1−t−(k−1)t²`. For `t+(k−1)t²≤1`, define Kraus maps from C² to (C²)⊗k:

```
K0 = |0^k><0| + t*sqrt(k)*|W_k><1|
K1 = sqrt(a)*|0^k><1|
K2 = sqrt(t-t²)*|1^k><1|
```

They satisfy `∑K_j†K_j=I`, since |0^k>⊥|W_k> and `k t²+a+(t−t²)=1`. Every one-site reduced channel has four matrix-unit actions: `|0><0|↦|0><0|`, `|1><1|↦(1−t)|0><0|+t|1><1|`, `|0><1|↦t|0><1|` and its adjoint. Hence every reduced channel is D_{|0>,t}. Conjugate by a qubit unitary for other pure τ; linearly combine these broadcast channels according to a spectral decomposition of arbitrary mixed τ. The resulting CPTP broadcaster has all k marginals D_{τ,t}.

**Qubit converse.** Suppose a CPTP broadcast B has all k marginals D_{|0>,t}. Since B(|0><0|)=P=|0^k><0^k| is pure, positivity of the 2×2 Choi block `[ [P,K], [K†,ω] ]` for `K=B(|0><1|)` and `ω=B(|1><1|)` forces `K=|0^k><v|`, with `ω≽|v><v|`. The reduction onto output i demands `⟨e_i|v⟩=t` (up to harmless conjugation). Let `N=∑_i |1><1|_i`. From the marginals, `Tr[(kI−N)ω]=k(1−t)`. The positive operator (kI−N) and ω domination yield `k(1−t)≥⟨v|(kI−N)|v⟩≥k(k−1)t²`, since its one-excitation diagonal entries are (k−1) and v has amplitude t on all k such basis vectors. Rearranging proves optimality at the positive root.

**Higher-dimensional achievability.** Select one output uniformly, send the entire input to it, and prepare τ at other outputs. Each marginal is D_{τ,1/k}. Mixture with the all-replacement map gives smaller t.

**Higher-dimensional converse.** Take τ=|0><0| and a two-dimensional subspace `S=span{|1>,|2>}` orthogonal to |0>. Restricted to inputs supported in S, D_{τ,t} is an erasure channel with unaltered transmission probability t and distinguishable erasure flag |0>. If k outputs broadcast it, measuring `P_S` at the outputs registers surviving messages. For any pure |ψ>∈S, whenever two outputs both survive their joint conditional density is supported on |ψψ>. This would define a trace-nonincreasing CP map exactly and probabilistically cloning every pure |ψ> in S. Such a CP map is zero: each Kraus operator would map |1> into span{|11>}, |2> into span{|22>}; its action on |+> would then lie in span{|11>,|22>}, which has zero intersection with span{|++>}, forcing the Kraus operator to vanish on S. Thus any two survival events have zero overlap. Since each output survives with probability t, `k t≤1`. QED.

**Caveat.** For d≥3, the no-cloning argument relies essentially on the existence of a two-dimensional orthogonal subspace S; it does not apply to a qubit pure-reference channel, where the orthogonal subspace is only one-dimensional.

## 6. Sharp universal marginal gluing on a star

**Theorem 5.** Let B be a d-level center connected to arbitrary-dimensional A₁,…,A_k. Assume bipartite density matrices σ_{BA_i} have a common B marginal τ_B, and let τ_i=Tr_Bσ_{BA_i}. Whenever `σ_{BA_i}≽(1−b_{d,k})τ_B⊗τ_i` for every i, there is a global state with those exact pair marginals. The coefficient b_{d,k} of Theorem 4 is optimal as a *uniform constant*, even when τ_B is required to be full rank.

**Construction.** For t=b_{d,k}>0 set `ρ_i=[σ_i−(1−t)τ_B⊗τ_i]/t`. Each ρ_i is a state and has the required one-site marginals. For full-rank τ_B choose the canonical purification |Ψ_τ>_{BR}=∑_j√λ_j |j>_B|j>_R in an eigenbasis of τ_B. The Choi–Jamiołkowski correspondence with this nonmaximally entangled reference supplies CPTP maps `T_i:R→A_i` such that `(id_B⊗T_i)(|Ψ_τ><Ψ_τ|)=ρ_i`. Crucially, `Tr_B|Ψ_τ><Ψ_τ|=τ_B^T` and `T_i(τ_B^T)=τ_i`. Apply the joint broadcaster for D_{τ_B^T,t} to the R half of |Ψ_τ>, then independently apply each T_i to its corresponding output. Its BA_i marginal is `tρ_i+(1−t)τ_B⊗T_i(τ_B^T)=σ_i`. Singularity of τ_B is handled by restricting the whole problem to supp τ_B.

**Sharpness.** For every d, consider full-rank τ_ε tending to pure τ_0 and let each leaf have dimension d, with original bipartite ρ_i the pure canonical purification |Ψ_{τ_ε}><Ψ_{τ_ε}|. Set σ_i=tρ_i+(1−t)τ_ε⊗τ_ε^T. If a global extension existed, inverse filtering of its B system by τ_ε^(−1/2) would produce the normalized Choi matrix of a broadcasting channel whose marginals are D_{τ_ε^T,t}. If this existed for an arbitrary sequence ε→0 with a fixed t>b_{d,k}, compactness of normalized Choi matrices would give a broadcast channel for D_{τ_0,t}, contradicting the pure-reference optimality in Theorem 4. Thus for some ε>0 the family is incompatible. QED.

**Examples.** For k=2 the guaranteed optimal qubit-star t is `(√5−1)/2≈0.618034` instead of the matching guarantee 1/2. For k=3 it is 1/2 instead of 1/3. For k=10 it is ≈0.282376 instead of 0.1. Conversely, d≥3 has exactly the matching threshold 1/k. For any classical central random variable B, however, *all* locally consistent star marginals can be glued at t=1 by conditioning independent leaves on B: `p(b,a₁,…,a_k)=p(b)∏_i p(a_i|b)`.

## 7. Representation and computational cost

The star extension exists as an explicit compact *quantum channel circuit or matrix-product operator (MPO)*; it need not be written as a 2^k-by-2^k density matrix.

- The optimal pure-reference qubit broadcaster has exactly three displayed Kraus operators (some zero at boundary). An arbitrary mixed qubit reference requires a mixture of at most two such channels, hence at most six Kraus branches.
- The only entangled multi-output vector required is the single-excitation W_k state (and its basis-flipped version), which has MPS bond dimension 2 and an O(k)-size sequential state-preparation circuit using standard continuously parameterized local gates. Product states |0^k> and |1^k> have bond dimension 1.
- Each Choi-purification output branch has MPS bond dimension at most 3 (a conservative bound), giving MPO bond dimension at most 9 for its pure-state projector. Combining at most six branches gives the conservative global bound **54**. Applying the independently specified T_i locally does not increase the virtual bond dimension. Thus for a qubit-star with all local leaf dimensions arbitrary, the constructed extension has MPO bond dimension at most 54, independent of k. This is an *existence-and-construction guarantee*, not a claim that every compatible global state has low bond dimension.
- A product observable or a prescribed bounded-bond tensor-network observable can be evaluated in time polynomial in k and the explicit local matrix dimensions using standard MPO contractions. Dense global observables, general compatibility problems, and #P-hard counting tasks are not covered.
- Each local channel T_i is acquired from the provided ρ_i by inverse filtering the central qubit (or d-level) marginal. This is not free: its numerical condition depends on λ_min(τ_B) and local input precision. Rational 2×2 τ_B and rational local matrices permit algebraic/symbolic exact descriptions; physical approximate implementations must budget finite-precision error and gate synthesis. For a fixed positive lower eigenvalue and fixed local output dimensions, the number of arithmetic/circuit operations grows polynomially in k and the requested precision bits. In the near-pure witnesses needed for sharpness, this condition number may diverge, and **no uniform conditioning claim** is made.
- The general packing theorem has a different representation cost: at most one product preparation per support-independent-set sample, with a potentially hard step to acquire an appropriate independent-set law. An explicit colouring gives a polynomial witness instead.

## 8. Scope, prior art and status

(1) Theorems 1–3 and 5 offer *sufficient and sometimes sharp universal radii*, not necessary-and-sufficient compatibility tests for arbitrary given marginals. No QMA-complete quantum marginal instance is solved in general.

(2) Theorem 4 is an exact k-self-compatibility computation for a particular state-centered identity/replacement family, as opposed to optimal state cloning of arbitrary inputs or general channel compatibility.

(3) Prior art requiring focused comparison includes: Girard, Plávala and Sikora, *Jordan products of quantum channels and their compatibility*, Nature Communications 12:2129 (2021), https://doi.org/10.1038/s41467-021-22275-0 ; Heinosaari and Miyadera, *Incompatibility of quantum channels*, arXiv:1608.01794; Chen, Ji, Kribs, Lütkenhaus and Zeng, *Symmetric Extension of Two-Qubit States*, arXiv:1310.3530; Catalano et al., *Convex combinations of bosonic pure-loss channels*, arXiv:2604.26874 (2026), which reports the inverse-golden-ratio threshold in a related two-output non-antidegradability setting. The general-k formula and its global universal-star interpretation are not shown to have priority over all literature.

(4) Astra's public repository (https://github.com/harjassand/astra-research-knowledge) separately records EPR matchgate/determinantal and composition constructions (N190–N193, N635, N637) with open global relative-variance acquisition; they are *not* the assumptions of these proofs. Their source statuses are unreviewed. This note closes none of those gates.

(5) Research assessment: The statements appear mathematically self-contained and the explicit broadcast construction has been checked for k=2–5 by a finite numerical Choi/marginal test, but independent expert proof and priority review are absent. They are potentially specialist theorems, **not an established historic 9–10/10 discovery**. A more consequential theorem would require a qualitatively broader compatibility characterization or computational complexity consequence, not only sharper radii on selected incidence structures.
