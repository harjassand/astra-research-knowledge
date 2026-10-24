# A dimension-independent conditional relative-entropy upper bound for depolarization

24 October 2026. Independently reconstructed from the root's proposed proof. This argument is self-contained in finite-dimensional metric and entropy identities and uses no N675 undecidability or order-equivalence claim. External historical priority is not established.

## Theorem

Let A have dimension d≥2, let 0≤λ≤1, and define depolarization

D_λ(X)=λX+(1−λ)Tr(X)I_A/d.

For every finite reference R and faithful states ρ_AR,σ_AR,

D((D_λ⊗id_R)(ρ)||(D_λ⊗id_R)(σ))−D(ρ_R||σ_R)
≤ c_d(λ)[D(ρ||σ)−D(ρ_R||σ_R)],

where

c_d(λ)=(d²−1)λ²/[1+(d²−2)λ].                         (1)

Consequently the conditional Umegaki contraction coefficient is at most c_d(λ). For d=2 and λ=1/2, the bound is 3/8. For 0<λ<1, c_d(λ)<λ, so it improves the direct mixture/Doeblin bound λ. Equality of the exact coefficient with (1) is not claimed.

The same inequality extends by common faithful regularization to finite-dimensional pairs for which all relative entropies displayed here are finite. Infinite-minus-infinite expressions are not defined by this note.

## Definitions and normalization

For a faithful state a, define Ω_a(X)=(aX+Xa)/2 and

g^S_a(H)=Tr H Ω_a^(−1)(H).

This is the SLD metric, with spectral kernel 2/(a_i+a_j). Define the BKM metric by

g^B_a(H)=Tr H Dlog_a(H),

whose spectral kernel is (log a_i−log a_j)/(a_i−a_j), with diagonal value 1/a_i. For a bipartite baseline σ and Hermitian tangent H, put

Q^S_σ(H)=g^S_σ(H)−g^S_{σ_R}(H_R),
Q^B_σ(H)=g^B_σ(H)−g^B_{σ_R}(H_R).

These are nonnegative by data processing under the partial trace. They are conditional metric deficits, not the unrestricted full-metric ratio, which has a reference-only direction with contraction one.

## Step 1: exact SLD reference gauge

For arbitrary Hermitian H, set

L=Ω_{σ_R}^(−1)(H_R),
V=Ω_σ(I_A⊗L),
H₀=H−V.

Partial trace gives H₀,R=H_R−Ω_{σ_R}(L)=0. The SLD bilinear pairing satisfies

⟨H₀,V⟩_σ=Tr H₀(I_A⊗L)=Tr H₀,R L=0.

Furthermore

g^S_σ(V)=Tr σ(I_A⊗L)²=Tr σ_R L²=g^S_{σ_R}(H_R).

Hence

Q^S_σ(H)=g^S_σ(H₀).                                  (2)

Let Φ act on A only. Because multiplication by a reference observable commutes with Φ⊗id_R,

Φ_R(V)=Ω_{Φ_R(σ)}(I_B⊗L).

The output reference marginal is still σ_R, so the same L is its reference gauge. Thus

Q^S_{Φ_R(σ)}(Φ_R(H))=g^S_{Φ_R(σ)}(Φ_R(H₀)).           (3)

Consequently a uniform equal-marginal SLD metric bound for all finite references is automatically a uniform conditional SLD metric bound with the same constant. Conversely, equal-marginal tangents are a subset, so the corresponding two optimized SLD coefficients coincide. This identity is specific to the SLD arithmetic-mean gauge used here; it is not a claim that the analogous naive BKM subtraction works.

## Step 2: Weyl-mixture SLD bound on zero-reference tangents

Let U₀=I,U₁,…,U_{d²−1} be a unitary Weyl error basis on A. Complete twirling gives

∑_{j=0}^{d²−1}(U_j⊗I)H₀(U_j*⊗I)=d I_A⊗Tr_A H₀=0,

so the sum over nonidentity unitaries equals −H₀. Write n=d²−1 and

p₀=(1+nλ)/(n+1), p=(1−λ)/(n+1).

Then D_λ=p₀ id+p∑_{j=1}^n Ad_{U_j}.

The SLD metric is jointly convex in its positive baseline and Hermitian tangent. One direct proof is its variational representation

g^S_a(H)=sup_{X=X*}[2Tr HX−Tr aX²],

which is a supremum of affine functions of (a,H). Unitary invariance is immediate.

Choose real constants u,v satisfying p₀u−pv=λ. Joint convexity applied to the baseline branches and tangent branches uH₀ and vU_jH₀U_j* gives

g^S_{D_λσ}(λH₀)
≤(p₀u²+npv²)g^S_σ(H₀).

Minimizing that scalar quadratic under its one linear constraint gives

min(p₀u²+npv²)=λ²/[p₀+p/n]
              =nλ²/[1+(n−1)λ]=c_d(λ).               (4)

For example, u=λ/[p₀+p/n] and v=−λ/[n(p₀+p/n)] attain the minimum. The endpoint λ=1 is immediate; λ=0 has zero output tangent and can also be read directly from the channel.

Combining (2)–(4) yields, for arbitrary H,

Q^S_{D_λσ}(D_λH)≤c_d(λ)Q^S_σ(H).                    (5)

## Step 3: an explicit qubit-reference SLD integral for BKM

Introduce an additional untouched reference qubit C. For s>0 set

τ_s=diag(1,s)/(1+s),
X_C=|0><1|+|1><0|,
K=H⊗X_C.

The extended baseline σ⊗τ_s is faithful. If σ has eigenvalues a_i, the only nonzero auxiliary blocks of K are the two offdiagonal blocks. Using Hermiticity of H to exchange i,j in one sum gives

g^S_{σ⊗τ_s}(H⊗X_C)
=4(1+s)∑_{i,j}|H_ij|²/(a_i+s a_j).                   (6)

For positive a,b,

∫₀^∞ ds/[(1+s)(a+sb)]
=(log a−log b)/(a−b),                                (7)

with the continuous value 1/a when a=b. Therefore

g^B_σ(H)
=∫₀^∞ g^S_{σ⊗τ_s}(H⊗X_C) ds/[4(1+s)²].             (8)

All factors in (6)–(8) are essential. For a commuting diagonal tangent the identity reduces to ∫₀^∞(1+s)^(−2)ds=1, checking the normalization.

The same identity holds for σ_R,H_R and for the channel output. Partial trace over A sends K to H_R⊗X_C, while Φ on A leaves τ_s untouched. Subtracting the reference identity yields

Q^B_σ(H)
=∫₀^∞ Q^S_{σ⊗τ_s}(H⊗X_C) ds/[4(1+s)²].             (9)

There is no uncontrolled interchange or infinity cancellation. In finite dimension with σ≥mI, (6) is bounded by 4||H||_HS²/m uniformly over s, and the integration weight has total mass 1/4. The corresponding reference and output terms are likewise finite on their fixed supports. Each conditional integrand is also nonnegative. Thus ordinary dominated integration, or positivity together with the individual finite integrals, justifies (9).

Apply (5) at every s to the reference R⊗C, then integrate (9):

Q^B_{D_λσ}(D_λH)≤c_d(λ)Q^B_σ(H).                    (10)

This is a general transfer mechanism: ANY uniform equal-marginal SLD metric constant for a channel, valid for arbitrary finite references, bounds its conditional BKM metric by this construction. Only one extra reference qubit is needed at each integration parameter. It does not transfer an SLD lower witness into an equal-marginal BKM lower witness.

## Step 4: integrate the conditional BKM inequality to relative entropy

For faithful ρ,σ set H=ρ−σ and σ_t=σ+tH, 0≤t≤1. The relative-entropy Bregman identity is

D(ρ||σ)=∫₀¹(1−t)g^B_{σ_t}(H)dt.

Applying the same identity to the reference marginals gives

D(ρ||σ)−D(ρ_R||σ_R)
=∫₀¹(1−t)Q^B_{σ_t}(H)dt.

The corresponding output path is D_λσ_t. Integrating (10) along this path proves the theorem. If the conditional input divergence vanishes, the inequality directly forces the conditional output divergence to vanish; no division by zero is performed.

For λ=0 the conditional output divergence is zero because the channel replaces A by I/d. For λ=1 the inequality is equality. Thus all endpoints in the stated range are covered.

## Checks against prior context and limits

The primary literature inspected supplies the surrounding established machinery:

- Lesniewski–Ruskai, “Monotone Riemannian metrics and relative entropy on noncommutative probability spaces” (1999), is foundational for monotone metrics and relative-entropy Hessians. https://doi.org/10.1063/1.533053 . The present proof explicitly evaluates its kernels rather than importing an unreviewed equivalence theorem.
- Hirche–Rouzé–Stilck França, “On contraction coefficients, partial orders and approximation of capacities for quantum channels,” Quantum 6, 862 (2022): https://quantum-journal.org/papers/q-2022-11-28-862/ . This is prior framework for contraction and order comparisons, not evidence that (1) is new.
- Hirche–Tomamichel, “Quantum Rényi and f-divergences from integral representations,” https://arxiv.org/html/2306.12343v3 , develops integral-representation contraction methods. Its statements about its chosen f-divergence family must not be silently substituted for the SLD/BKM conditional metric statement here.
- George–Tomamichel, “A Unified Approach to Quantum Contraction and Correlation Coefficients,” https://arxiv.org/html/2505.15281 , develops noncommutative weighted L², variance, and χ² contraction structure. This is close methodological context for the SLD gauge and dual variance viewpoint.
- Hirche–George–Nuradha–Wilde, “Conditional contraction coefficients and their applications to quantum networks,” https://arxiv.org/html/2608.27171 , defines the conditional relative-entropy coefficient, discusses Doeblin upper bounds, and leaves the separation questions in Eq. (3.66) open. The theorem above does not establish those separations or an exact depolarizing coefficient.

A targeted primary-source check has not established whether the precise bound (1), or the explicit one-qubit SLD integral transfer in this conditional form, already appears elsewhere. No historical novelty claim is warranted on this search alone. The proof above is the substantive result and is independent of that unresolved priority question.

## A directly sourced consequence for two copies

HGWN26, https://arxiv.org/html/2608.27171 , Corollary 14 / Eq. (6.19), proves

η_D(N⊗M)≤η_D(M)+η_D^conditional(N)−η_D(M)η_D^conditional(N),

and the same bound with N,M exchanged. Its Eq. (6.20) specializes this using the Doeblin estimate for qubit depolarization. At survival λ=1/2, η_D(D_λ)=1/4 and the new conditional bound is 3/8. Substitution gives

η_D(D_{1/2}⊗D_{1/2})≤1/4+3/8−(1/4)(3/8)=17/32,

instead of that paper's displayed 5/8 upper bound at the same parameter. The paper's displayed lower bound at this parameter is 2/5. Thus the bounds supplied by this combination are 2/5≤η_D(two copies)≤17/32. This is a deduction using their product-channel inequality, not a tensorization claim or an exact two-copy value.
