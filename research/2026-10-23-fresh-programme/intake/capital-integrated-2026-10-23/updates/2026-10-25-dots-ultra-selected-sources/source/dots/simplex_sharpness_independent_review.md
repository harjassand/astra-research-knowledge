# Independent reconstruction of simplex sharpness

24 October 2026. This proof independently verifies the root's construction. It uses the established conditional group-twirl upper bound, not N675 or an assumed metric-order equivalence. Historical priority is not asserted.

## 1. Classical uniform-reset channel with a quantum reference

Let N≥2 and 0<λ<1. Consider K_{λ,N}=λI_N+(1−λ)J_N/N. Let the reference be R=C|0>⊕V with dim V=N−1. Choose unit regular-simplex vectors v₁,…,v_N∈V, satisfying

∑_i v_i=0,
(1/N)∑_i |v_i><v_i|=I_V/(N−1).

For example, realize V as the zero-sum subspace of C^N and take v_i=sqrt(N/(N−1))(e_i−(1/N)∑_j e_j), adjoining the orthogonal vacuum |0> as the remaining direction.

For 0<ε<1, define faithful reference states and Hermitian coherence tangents

σ_i=(1−ε)|v_i><v_i|+εI_R/N,
X_i=|v_i><0|+|0><v_i|.

Set the cq baseline and tangent to

Σ=(1/N)⊕_i σ_i,
H=(1/N)⊕_i X_i.

Every block is faithful. The marginal tangent is exactly zero because ∑_iX_i=0. The baseline marginal is

τ_R=(1−ε)I_V/(N−1)+εI_R/N.

Thus (Σ+tH,Σ) has identical reference marginals for every sufficiently small real t, not merely to leading order. Positivity holds whenever t²<ab, where a=1−ε+ε/N and b=ε/N, since each perturbed block has only the 2×2 nontrivial sector spanned by v_i and |0>.

The output block is σ_i′=λσ_i+(1−λ)τ_R and the normalized block tangent is λX_i. Define

c=λ+(1−λ)/(N−1).

On the v_i,|0> sector, the output baseline eigenvalues are

a′=(1−ε)c+ε/N,
b=ε/N.

This is an exact eigenbasis statement: τ_R is scalar on all of V, and the vacuum is orthogonal to V. There is no perturbative approximation or simultaneous-diagonalization assumption across different i.

## 2. Exact BKM quotient

For a diagonal 2×2 baseline diag(a,b) and tangent X with two offdiagonal entries equal to one,

g^B_{diag(a,b)}(X)=2(log a−log b)/(a−b).

The input cq metric equals the average of the normalized block metrics: g_{σ_i/N}(X_i/N)=(1/N)g_{σ_i}(X_i). All normalized blocks have the same metric, so the overall quotient is exactly

q_ε = (λ²/c)
  log[1+N(1−ε)c/ε] / log[1+N(1−ε)/ε].                (1)

Since c>0 is fixed,

lim_{ε→0} q_ε = λ²/c
 = (N−1)λ²/[1+(N−2)λ].                              (2)

For each fixed ε, the local-to-finite-pair BKM limit applies to the faithful pairs (Σ+tH,Σ) as t→0. Taking ε→0 and then choosing t sufficiently small proves that the equal-marginal relative-entropy coefficient is at least (2).

The universal conditional group-twirl theorem with the cyclic N-label group supplies the matching upper bound for arbitrary finite quantum references. Since equal-marginal tests are a subset of conditional tests, this proves

η_D^c(K_{λ,N}) = η_D^conditional(K_{λ,N})
 = (N−1)λ²/[1+(N−2)λ].                              (3)

Both suprema can be approached with reference dimension N. The statement concerns the supremum; faithful finite-pair attainment of the limiting value is not asserted. At N=2, c=1 and (1) is already λ² for every ε at the metric level. The endpoint channels λ=0,1 give coefficients zero and one by direct evaluation.

## 3. Bell encoding to quantum depolarization

Let N=d² and choose a complete orthonormal maximally entangled Bell basis on A⊗B, with dim A=dim B=d and projectors P_i. For any cq state with blocks ρ_i, encode

Θ(ρ)=∑_i P_i⊗ρ_i.

Orthogonal Bell sectors preserve relative entropy exactly. Their partial trace over A gives

Θ(ρ)_{BR}=I_B/d⊗∑_iρ_i,

so reference relative entropy and equality of reference marginals are also preserved exactly. Finally,

(D_{λ,A}⊗id_B)(P_i)=λP_i+(1−λ)I_{AB}/d².

The output Bell blocks are therefore exactly those of K_{λ,d²}. Applying this encoding to the simplex construction proves the lower bound (2) for d-dimensional depolarization. The already proved quantum upper bound gives

η_D^c(D_{λ,d}) = η_D^conditional(D_{λ,d})
 = (d²−1)λ²/[1+(d²−2)λ].                            (4)

The untouched quantum reference has dimension d·N=d³. The total encoded baseline is faithful: the Bell projectors form a complete basis, and every corresponding reference block is positive definite. The perturbed encoded state is likewise faithful for sufficiently small t. No singular encoded state is substituted for a faithful witness.

Equation (4) establishes equality of the complete/equal-marginal and conditional coefficients for this depolarizing family. It does not establish equality with the mutual-information coefficient, nor equality of these notions for general channels.

## 4. Exact rational finite counterexample to the earlier 1/3 conjecture

For d=2, N=4, take tetrahedral vectors in R³,

v₁=(1,1,1)/sqrt(3),
v₂=(1,−1,−1)/sqrt(3),
v₃=(−1,1,−1)/sqrt(3),
v₄=(−1,−1,1)/sqrt(3).

Their projectors have rational entries. Scale each X_i by sqrt(3), so the coherence tangent also has rational entries, without changing its metric quotient. Choose

λ=1/2, ε=1/100, t=1/10000.

The two hypotheses are the cq states with blocks σ_i/4 and (σ_i+t sqrt(3)X_i)/4, followed by Bell encoding. They have equal reference marginals and rational matrix entries. The encoded reference dimension is eight.

Each active 2×2 input block has diagonal entries a=397/400, b=1/400 and squared coherence 3t². Its determinant ab−3t² is strictly positive. At the output a′=265/400 and the squared coherence is 3λ²t². All other eigen-directions are unchanged between the hypotheses.

For such a block, let

r_±=(a+b±sqrt((a−b)²+4z²))/2.

Its relative entropy against the diagonal baseline is exactly

r_+ log r_+ + r_− log r_− − a log a − b log b.

Using this scalar formula with outward-rounded interval arithmetic at 80 decimal digits gives

D_in ≈ 1.81331581012738030949×10^(−7),
D_out ≈ 6.34060455820848192488×10^(−8),
D_out/D_in ≈ 0.34966907158676746877887945922928,
D_out−D_in/3 ≈ 2.96218524450547559916×10^(−9) > 0.

simplex_finite_interval_check.py and its JSON retain the full enclosing intervals and positivity assertions. Thus the earlier proposed equal-marginal BKM upper 1/3 for half-depolarization is false for a finite faithful rational witness. The true supremum supplied by (4) is 3/8. Previous small-reference numerical searches and the PPT/two-component exclusion lemmas do not conflict with this eight-dimensional-reference construction.

## 5. Potential error checks that passed

- The simplex cancellation is vector cancellation, so it cancels the vacuum-coherence tangents exactly.
- The cyclic-group upper acts on classical labels; the simplex vectors reside entirely in the untouched quantum reference.
- The output reference average is scalar on V and preserves the vacuum eigenvalue, making the two-eigenvalue BKM calculation exact.
- Homogeneity of the block metric supplies a factor 1/N, not 1/N²; averaging cancels it in the quotient.
- Bell encoding preserves the full pair of divergences and reference marginal, rather than merely preserving a classical measurement statistic.
- Every finite ε>0 baseline and sufficiently small perturbation is faithful. Limits are used only to establish a supremum.
- The proof uses no claim that BKM and SLD lower witnesses are interchangeable.
- The construction has fixed finite reference dimension for each fixed d, even though reaching the limiting constant uses increasingly small spectral/precision resources.

## 6. The same construction resolves the earlier SLD gap

For the same offdiagonal tangent, the SLD metric is 4/(a+b), so the exact local SLD quotient is

q^S_ε=λ²(a+b)/(a′+b)
=λ²[(1−ε)+2ε/N]/[c(1−ε)+2ε/N].

It tends to the same constant λ²/c. Therefore the complete SLD upper bound is sharp as well, and the exact SLD reference gauge makes the conditional SLD coefficient equal to it. For depolarization, all of the optimized complete-SLD, conditional-SLD, complete-BKM/Umegaki, and conditional-BKM/Umegaki coefficients equal (4). This is equality of optimized channel coefficients, not equality of the metrics at a fixed state or tangent.

At N=4, λ=1/2, ε=1/100, the SLD quotient is exactly 199/532≈0.3740601504. Thus the previously unresolved [.343918…, .375] SLD interval is closed by this larger-reference family. The earlier X-state family remains correctly calculated but is not globally extremal.

## 7. Precision cost visible in the exact expression

Write C=λ²/c and L=N(1−ε)/ε. For N>2 and 0<λ<1, c<1 and

C−q_ε=C[log(1+L)−log(1+cL)]/log(1+L)
       ~ C|log c|/log(N/ε).

Thus this BKM witness family approaches the supremum only logarithmically in the inverse spectral floor. A small ratio-error target requires an exponentially small ε within this family, even though the reference dimension is fixed. This does not prove an optimal experimental sample complexity or that every witness family has the same cost. It does explicitly distinguish finite reference dimension from precision and absolute-signal resources.
