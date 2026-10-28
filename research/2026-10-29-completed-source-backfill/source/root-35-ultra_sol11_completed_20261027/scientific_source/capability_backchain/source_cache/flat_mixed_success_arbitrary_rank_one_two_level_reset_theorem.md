# Whole VALUE: flat mixed success and every white plus/minus arbitrary rank-one reset

Status: analytic proof with exact finite polynomial receiver; awaiting independent receipt for the new arbitrary positive-bump part. The arbitrary-hole part is independently received.

## Whole theorem
Let r≥1 be finite, ψ any unit vector in reference C³⊗Cʳ, and

Y=aI_(3r)+b|ψ><ψ|,   a≥0, a+b≥0,
X=P_Ω3⊗I_r+I₃⊗Y,

where Ω₃ is unnormalized. Then Δ(X)≥0, with equality exactly when Y=0 (a=b=0). The main may have any finite flat logical multiplicity. The reset projector may have any Schmidt allocation and arbitrary coherent orientation.

These are actual TP-channel Choi sources after division by r+TrY. The theorem is NOT for arbitrary projector rank, arbitrary mixed logical spectrum, or arbitrary PSD reset. The input generally has more than two or three spectral levels.

For b<0 the already-received `flat_mixed_success_arbitrary_reset_hole_theorem.md` applies with p=−b/a. For r=1 the received pure-main/qutrit-reset theorem applies. It therefore remains to pay b≥0 for r=2,3; higher r follows by an actual orthogonal logical direct sum.

## 1. Keep the actual two-pole source clock
For b≥0 set

K_b(u)=u^-1 I_(3r)+[(u+b)^-1−u^-1]|ψ><ψ|, u>0.

The exact homogeneous source determinant identity gives

Δ(a,b;ψ)=∫_a∞ F_r(K_b(u))du,                    (1)
F_r(K)=2logdet[I+(W₃⊗id)K]−3logdet(I+K/3)−logdet(I+Tr_codeK).

Thus white reset mass a only removes an initial segment of ONE original shared clock. This is not a spectral-overlap average or an independently varying matrix clock.

We prove that, for every b≥0 and every Schmidt allocation, the integrand in(1) changes sign exactly once, from negative to positive. The already-paid a=0 source then pays every tail.

## 2. Exact positive-denominator numerators
Put s=u, w=s+b, and A=2(s+1)w−b.

### Logical rank2
Let e=λ₁λ₂∈[0,1/4] for the two Schmidt probabilities. Define
A₂=4(s+1)²w²−2b(s+1)w+b²e,
B₂=(s+3)²w²−b(s+3)w+b²e.
Then

exp F₂(K_b(s))
 =3^18 s^5 A²A₂²(s+1)^6 /
  [64w(3w+1)^3(3s+1)^15 B₂].                    (2)

### Logical rank3
Let e=Σ_(i<j)λ_iλ_j, f=λ₁λ₂λ₃. Define
A₃=A³+bA²+b²eA+b³f,
B₃=(s+3)³w³−b(s+3)²w²+b²e(s+3)w−b³f.
Then

exp F₃(K_b(s))
 =3^27 s^9 A₃²(s+1)^12 /
  [64(3w+1)^3(3s+1)^24 B₃].                     (3)

The denominators are strictly positive. B₂ and B₃, divided by positive powers of s,w, are the actual reference determinant heads; equivalently their factors are1+3/s−bλ_i/[s(s+b)]>0. All other displayed factors are positive.

Let N_r(s) be numerator minus denominator in(2)/(3). These are polynomials of degrees21 and31, respectively, received exactly by `flat_mixed_success_arbitrary_bump_one_crossing_certificate.py`. Since the denominator is positive, F_r and N_r have the same sign.

## 3. A finite exact sign-propagation certificate
Write N_r(s)=Σc_j s^j. The following are not sampled coefficient claims: the adjacent JSON proof object and pure-rational replay expand every transformed polynomial and verify all signs.

For r=2, use homogeneous coordinates h₀,h₁≥0, not both zero, with

e=h₁/[4(h₀+h₁)],
H_j=(h₀+h₁)² c_j(e).

Every nonzero coefficient of H_j in b,h₀,h₁ is negative for0≤j≤6 and positive for14≤j≤21. For j=7,...,12, the polynomial

(C_j b+D_j)H_(j+1)−(A_j b+B_j)H_j

has ALL24 coefficients strictly positive, with weights(A_j,B_j,C_j,D_j):

j7: (182,718,98,1)
j8: (264,567,169,1)
j9: (308,456,235,2)
j10:(0,566,361,73)
j11:(0,412,502,86)
j12:(0,376,367,257).

For r=3, by symmetry order the Schmidt weights and use nonnegative gaps g₀,g₁,g₂, not all zero:

(λ₁,λ₂,λ₃)=(g₀+g₁+g₂,g₀+g₁,g₀)/D,
D=3g₀+2g₁+g₂.

Homogenize H_j=D^6 c_j(e,f). Every nonzero coefficient in b,g₀,g₁,g₂ is negative for0≤j≤12 and positive for19≤j≤31. For j=13,...,17, the same adjacent combination has ALL224 coefficients strictly positive, with weights:

j13:(2249,6100,1642,10)
j14:(3390,4407,2193,10)
j15:(4136,2993,2861,10)
j16:(0,5709,2968,1324)
j17:(0,4300,4143,1557).

In every chain the multiplier C_j b+D_j is strictly positive, and A_j b+B_j is positive. Strict pure-gap monomials are also checked, so the conclusions remain valid on every closed Schmidt boundary, including zero Schmidt weights. The exact receiver checks144+1120 positive chain coefficients, as well as the entire low/high coefficient blocks and both actual determinant ratios.

Therefore c_j≥0 at any ambiguous index forces c_(j+1)>0. The descending nonzero coefficient sequence has exactly one sign variation: a positive high block, possibly some ambiguous entries, then a negative low block. This is an actual all-domain coefficient implication, not a grid over b or Schmidt probabilities.

## 4. Receive the one crossing
The leading coefficients are positive. For b>0 the constant coefficients are

N₂(0)=−64b³(3b+1)³(e+6)<0,
N₃(0)=−64b³(3b+1)³(3e−f+18)<0.

For b=0 the first nonzero low terms are−576s³ and−1728s³. Descartes' rule consequently gives exactly one positive root, counted with multiplicity, hence a simple root s_*>0. Thus

F_r(K_b(s))<0 for0<s<s_*,
F_r(K_b(s))>0 for s>s_*.

Both endpoint singularities are received by the actual finite-source entropy identity: logarithmic behavior at zero is integrable, and the infinity tail is O(s^-2).

## 5. Pay every tail from a genuine source anchor
At a=0,b>0, Y=b|ψ><ψ| is rank one and the logical main is flat of rank r. The received `flat_logical_success_arbitrary_flag_uniform_theorem.md` gives strict VALUE for this fully inside flag. Its normalized channel weights are r/(r+b) and b/(r+b), with logical rank r and flag overlap θ=1. At a=b=0 the pure mixed-isometric source has Δ=0 exactly.

If0<a≤s_*, equation(1) removes only a strictly negative initial segment from that paid anchor, so Δ(a,b)>Δ(0,b)≥0. If a≥s_*, equation(1) is a strictly positive tail integral. Therefore every a>0,b≥0 is paid strictly; the a=0 endpoint was already received.

For arbitrary r≥3, choose a logical three-dimensional subspace containing ψ's logical Schmidt support. The actual source is the direct sum of the r=3 source just paid and r−3 qutrit sources P_Ω3+aI₉. The latter are received pure-main/white-reset sources. Additivity of the original input, reference and output block entropies pays the sum. This is not a physical measurement or discard of an inaccessible label. Logical rank2 uses its own certificate above; rank1 uses the prior pure-main theorem.

Combining the bump argument with the independently received arbitrary-hole theorem proves the stated full parameter domain and exact zero set.

## Scope guards
The identity component of the logical main is essential here. Arbitrary nonflat C, multiple coherent reset eigenvectors, higher-rank holes, general filtered-source anchors, complete-instrument order, and unrestricted WH₃ positivity remain open. The previously certified generic endpoint failures remain valid. This construction uses the rigid common source pencil and exact sign propagation, rather than restoring any of those disproved shortcuts.
