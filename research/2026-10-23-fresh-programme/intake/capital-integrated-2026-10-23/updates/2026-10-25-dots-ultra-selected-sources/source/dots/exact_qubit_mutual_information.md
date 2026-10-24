# Exact quantum mutual-information contraction of qubit depolarization

24 October 2026. Analytic derivation. Uses the separately proved binary cq conditional contraction theorem; no N675 premise. Historical priority remains unverified.

## Theorem

For0<=λ<=1, let Dλ(ρ)=λρ+(1−λ)I_2 Trρ/2. Then

η_MI(Dλ)=sup_{finite R,ρ_AR:I(A:R)>0} I(A':R)_{(Dλ⊗id)ρ}/I(A:R)_ρ
=2λ²/(1+λ).

The upper bound allows arbitrary finite quantum reference dimension. A reference qubit suffices to approach the lower bound. Atλ=1/2 the coefficient is exactly1/3.

Together with the independently proved simplex/group-twirl result,
ηc_D(Dλ)=ηΔ_D(Dλ)=3λ²/(1+2λ),
so for every0<λ<1,
ηc_D(Dλ)−η_MI(Dλ)=λ²(1−λ)/[(1+2λ)(1+λ)]>0.

Thus for this channel family the first comparison in HGWN26 Eq3.66 is equality and the second is strict. This does not establish either relation for arbitrary channels.

## 1. Coherence decomposition of mutual information

Fix anyρ_AR. Choose a physical qubit basis diagonalizingρ_A, and letΔ be dephasing in that basis onA only. Thenρ andΔρ have identical A and R marginals. The pinching entropy identity yields

I(A:R)_ρ=I(A:R)_{Δρ}+C(ρ),
C(ρ):=D(ρ||Δρ)=S(Δρ)−S(ρ).

Depolarization commutes withΔ and maps a diagonal marginal to a diagonal marginal. Consequently the SAME identity holds after the channel:
I(A':R)_{Dλρ}=I(A':R)_{DλΔρ}+C(Dλρ).

This basis choice does not assumeρ_A is maximally mixed. It is permitted because depolarization is unitarily covariant.

## 2. The diagonal classical-quantum part

On a state diagonal inA, Dλ acts as the binary uniform-reset channel K_{λ,2}. Its complete relative-entropy contraction coefficient, allowing arbitrary quantum R and equal reference marginals, is exactlyλ², as proved in conditional_expectation_upper_proof.md and simplex_complete_independent_check.md.

Apply its upper bound to the cq pair Δρ andρ_A⊗ρ_R. They have equal R marginals, and their output pair is DλΔρ and Dλ(ρ_A)⊗ρ_R. Therefore

I(A':R)_{DλΔρ}<=λ² I(A:R)_{Δρ}.

No classicality of R or uniformity ofρ_A is assumed. This is precisely why the complete binary-channel theorem, rather than a scalar binary SDPI, is needed here.

## 3. The coherence part

Let X swap the two chosen physical basis states. Put
k=(1+λ)/2, θ=λ/k=2λ/(1+λ),
Γθ=θ id+(1−θ)Δ.

Writingρ in physical qubit blocks [[A,C],[C*,B]] verifies the exact identities

Dλρ=k Γθρ+(1−k)XΔρX,
ΔDλρ=k Δρ+(1−k)XΔρX.

Indeed the output diagonal blocks are kA+(1−k)B and kB+(1−k)A, and the offdiagonal block isλC. Both mixtures have the same second component. Joint convexity of relative entropy gives

C(Dλρ)<=k D(Γθρ||Δρ).

For binary dephasing,
D(Γθρ||Δρ)<=θ²D(ρ||Δρ).
This follows already from the N0=2 conditional-expectation theorem. An independent direct BKM proof follows below. Hence

C(Dλρ)<=kθ² C(ρ)=2λ² C(ρ)/(1+λ).

Crucially, this argument does NOT require the false operator inequalityI⊗ρ_R−ρ>=0. The swapped DIAGONAL state XΔρX is positive for everyρ, including entangled states.

## 4. Combine the two pieces

Becauseλ²<=2λ²/(1+λ), summing Sections2–3 gives

I(A':R)_{Dλρ}
<=λ² I(A:R)_{Δρ}+[2λ²/(1+λ)]C(ρ)
<= [2λ²/(1+λ)]I(A:R)_ρ.

This also gives a stronger state-dependent bound: the diagonal cq information contracts at mostλ², while the coherence contribution contracts at most2λ²/(1+λ).

## 5. Direct proof of the binary coherence bound

For a faithful stateρ, setσ=Δρ,H=ρ−σ, andF(t)=D(σ+tH||σ), |t|<=1. LetZ be the physical phaseflip; ZσZ=σ andZHZ=−H. Thus the BKM Hessian g^B_{σ+tH}(H) is even int. It is also convex int because the BKM metric is jointly convex in its baseline and tangent (equivalently, differentiate joint convexity of relative entropy). An even convex function is nondecreasing on[0,1].

The entropy Hessian integral gives
F(θ)=θ²∫_0^1(1−s)g^B_{σ+θsH}(H)ds
<=θ²∫_0^1(1−s)g^B_{σ+sH}(H)ds=θ²F(1).

Common faithful regularization extends to arbitrary finite-dimensional states. Pinching guarantees the needed support inclusion forC(ρ), and finite-dimensional entropy continuity removes boundary ambiguity.

## 6. Matching lower bound and limit order

Use the explicit family from mi_product_baseline_obstruction.md:
τ=diag(p,1−p)_A⊗diag(1−s,s)_R,
ρ_t=τ+t(|00><11|+|11><00|).
Both marginals equal those ofτ, and positivity holds for|t|<sqrt[p(1−p)s(1−s)]. For fixedp,s, let t→0. The MI ratio tends to
λ² L(p'(1−s),(1−p')s)/L(p(1−s),(1−p)s),
p'=λp+(1−λ)/2,
L(a,b)=(log a−log b)/(a−b).
Then s→0 givesλ²p/p', and p→1 gives2λ²/(1+λ). For every desired tolerance choosep, then s, then a sufficiently small nonzerot. This constructs actual faithful finite witnesses without exchanging nonuniform limits. The physical/reference dimensions remain2 throughout.

Endpointsλ=0 and1 are immediate. The exact supremum need not be attained by a faithful state. The explicit finite interval witness in mi_biased_product_certificate.py/json reaches .3272311987 atλ=.5; its tiny absolute information is not advertised as a practical protocol.

## Scientific scope

The decisive ingredient is a basis-adapted split into a binary cq correlation term and coherence, not twirling the marginal to uniformity. The argument preserves arbitrary bias inρ_A. Gao–Zhao's smaller fixed-equilibrium bound remains compatible because its maximally mixed physical marginal restriction excludes the lower family.

Primary comparison: Hirche–George–Nuradha–Wilde, https://arxiv.org/html/2608.27171v1#S3.SS3 , Eq3.66 explicitly poses the hierarchy comparison. Earlier complete entropy-contraction terminology sometimes refers instead toD(ρ||Eρ); that different functional must not be identified withη_MI here. Priority requires additional external review.

## Higher-dimensional extension: strict separation, not an exact MI formula

For every physical dimensiond>=2, the same method gives

dλ²/[1+(d−1)λ] <= η_MI(Dλ,d)
<= U_d(λ):=d(d−1)λ²/[1+(d²−d−1)λ].

The lower bound follows from the product-baseline construction supported on a dominant physical level and one rare physical level, with a qubit reference, followed by faithful regularization of any unused physical levels. It is the exact local product-baseline supremum as established in mi_product_baseline_obstruction.md. Equality of the two bounds holds ford2, but is NOT claimed ford>2.

To prove the upper bound, choose a basis diagonalizingρ_A and dephase withΔ in that basis. The identity Iρ=IΔρ+Cρ is unchanged. The diagonal cq term contracts by at most
C_d(λ)=(d−1)λ²/[1+(d−2)λ],
using the exact complete coefficient of the d-symbol uniform-reset channel.

LetS cyclically shift the chosen basis, k=λ+(1−λ)/d, θ=λ/k, andΓθ=θid+(1−θ)Δ. Blockwise,

Dλρ=k Γθρ+[(1−λ)/d]Σ_{j=1}^{d−1} S^j Δρ S^(−j),
ΔDλρ=k Δρ+[(1−λ)/d]Σ_{j=1}^{d−1} S^j Δρ S^(−j).

The corresponding terms have identical weights and the same positive second components, so joint convexity gives C(Dλρ)<=k C(Γθρ). Full dephasingΔ is the average of d conjugations by powers of a diagonal phase unitary. The finite-group conditional-expectation bound therefore gives
C(Γθρ)<=C_d(θ) C(ρ).
Consequently the coherence coefficient is
k C_d(λ/k)=(d−1)λ²/[k+(d−2)λ]=U_d(λ).
SinceU_d(λ)>=C_d(λ), summing proves the upper bound.

The exact complete/conditional coefficient isC_{d²}(λ). Direct algebra yields

C_{d²}(λ)−U_d(λ)
=(d−1)λ²(1−λ)/{[1+(d²−2)λ][1+(d²−d−1)λ]}>0

for everyd>=2 and0<λ<1. Thus the MI-versus-complete separation is established for ALL these depolarizing channels, even though the exact MI value has only been identified here forqubits. At d3,λ=.5, the bounds are3/8<=η_MI<=3/7<4/9=ηc=ηΔ.

This extension uses an actual d-element phase-twirl conditional expectation on the full quantum matrix algebra, distinct from cyclic permutations on a cq block algebra. Both qualify for the group theorem, but their roles should not be conflated.
