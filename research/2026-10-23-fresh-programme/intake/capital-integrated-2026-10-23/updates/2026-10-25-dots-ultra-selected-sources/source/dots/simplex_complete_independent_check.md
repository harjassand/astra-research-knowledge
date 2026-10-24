# Independent verification: simplex witnesses attain the complete conditional bound

24 October 2026. This is an analytic check plus a separate dense-matrix audit. Historical priority and external proof review remain open.

## Exact result checked

For N>=2, 0<=λ<=1, and the N-symbol uniform-reset channel K_{λ,N},
ηc_D(K_{λ,N})=ηΔ_D(K_{λ,N})=(N−1)λ²/[1+(N−2)λ].

Here ηc optimizes ordinary relative-entropy contraction over pairs with equal untouched reference marginals; ηΔ optimizes reference-subtracted relative-entropy contraction over arbitrary pairs. The existing conditional upper proof handles arbitrary finite quantum references. The construction below gives the matching LOWER bound using equal-marginal pairs with reference dimensionN.

Consequently exact Weyl/Bell transfer at N=d² gives
ηc_D(D_{λ,d})=ηΔ_D(D_{λ,d})=(d²−1)λ²/[1+(d²−2)λ]
for quantum depolarization of physical dimensiond. A reference of dimensiond³ suffices to approach both suprema. Neither equality for arbitrary channels nor an equality with the unconditioned mutual-information coefficient follows.

## Explicit simplex and positivity

Work in R=C^N. Let u=(1,...,1)/sqrtN and
v_i=(e_i−(1/N)(1,...,1))/sqrt(1−1/N), i=1,...,N.
Then ||v_i||=1, <u,v_i>=0, Σ_i v_i=0, and
(1/N)Σ_i |v_i><v_i|=P_{u⊥}/(N−1).

For 0<ε<1 put σ_i=(1−ε)|v_i><v_i|+(ε/N)I_R and X_i=|v_i><u|+|u><v_i|. Define cq baseline σ=(1/N)⊕_i σ_i and tangent H=(1/N)⊕_i X_i. Every σ_i has trace one, every X_i has trace zero, and Σ_i X_i=0. Thus H_R=0 EXACTLY, not merely asymptotically. The joint baseline is faithful with minimum eigenvalue ε/N².

Write a=1−ε+ε/N and b=ε/N. In span{v_i,u}, σ_i+tX_i has matrix [[a,t],[t,b]], so it is positive definite exactly when |t|<sqrt(ab). Outside this span its eigenvalue is b. Thus every sufficiently small nonzero t gives actual faithful states ρ_t=σ+tH and σ with exactly the same reference marginal.

## Exact BKM ratio

The reference marginal is τ=(1−ε)P_{u⊥}/(N−1)+(ε/N)I. After K, the normalized block is σ_i'=λσ_i+(1−λ)τ and tangent λX_i. On span{v_i,u}, its eigenvalues are
 a'=(1−ε)c+b, b'=b,
where c=λ+(1−λ)/(N−1).

With L(a,b)=(log a−log b)/(a−b), the BKM form of X_i is2L(a,b); all other components vanish. Homogeneity gives g^B_{σ_i/N}(X_i/N)=g^B_{σ_i}(X_i)/N, so averaging N blocks introduces no extra factor. Therefore

g^B_{Kσ}(KH)/g^B_σ(H)
= λ²/c · log[1+N(1−ε)c/ε]/log[1+N(1−ε)/ε].

For fixed0<λ<1 this tends to λ²/c as ε↓0. For N=2, c=1 and the ratio is already λ² at everyε. Endpointsλ=0 and1 follow directly from the channel. No BKM gauge identity or obsolete endpoint factor2 inequality is used.

## Order of limits and actual state pairs

For any desired toleranceδ>0, first fixε>0 sufficiently small that the displayed metric ratio is withinδ/2 of λ²/c. Then, keepingε fixed, choose nonzero t with |t|<sqrt(ab) sufficiently small. Analytic relative-entropy expansion at a faithful baseline gives
D(ρ_t||σ)=t²g^B_σ(H)/2+Oε(t³),
D(Kρ_t||Kσ)=t²g^B_{Kσ}(KH)/2+Oε(t³).
Hence the finite-pair ratio is withinδ of λ²/c. The reference relative entropies vanish identically because H_R=0. There is no unjustified uniformity of the Taylor remainder asε→0; the limits are deliberately sequential.

Balanced binary U selecting the two hypotheses has U independent of R exactly. The corresponding CMI and MI-with-reference increments have the same tangent ratio. This stronger operational independence condition was not present in the earlier unequal-marginal X-family.

## Bell-transfer audit

For N=d² use orthogonal maximally entangled Bell projectors B_i on physical A and an untouched d-dimensional B. Map a cq state ⊕_iρ_i,R to Σ_iB_i,AB⊗ρ_i,R. Orthogonality preserves total relative entropy; tracingA gives I_B/d⊗Σ_iρ_i,R and preserves reference relative entropy and the equality of reference marginals. Depolarization onA maps B_i to λB_i+(1−λ)I_AB/d², exactly K's block mixing. The transferred reference is BR of dimensiond·N=d³. In particular the qubit witness uses reference8 and approaches3/8 atλ=1/2.

## Independent numerical audit, not the proof

The script audit_simplex_complete.py/json constructs all matrices independently using the explicit simplex above, evaluates their BKM forms by spectral logarithmic means, and checks N=2,3,4,5. For N4,λ=.5, ratios atε=.01,1e−5,1e−8 are .34966927898,.36321254020,.36732344. A separate dense16×16 qubit Bell construction atε1e−5 gives .363212540197, with reference marginal tangent zero to floating roundoff and positive minimum eigenvalue6.25e−7. All agree with the analytic formula.

## Interpretation correction

The previously proposed factor2 zero-survival BKM inequality was false, and earlier R2/R3 optimizations were insufficient evidence. This simplex construction does not revive it. It instead saturates the proven group-cardinality conditional upper bound, using a different reference geometry. The earlier ternary and padding lower bounds remain valid but are now superseded for exact symmetric-channel coefficients.
