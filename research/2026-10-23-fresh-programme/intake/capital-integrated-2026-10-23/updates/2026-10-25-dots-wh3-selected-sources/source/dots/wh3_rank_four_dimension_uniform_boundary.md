# Rank-four dimension-uniform boundary exclusion

24 October 2026. This is a new theorem extending the previous rank-three tightness result. It depends on the Kraus-span trichotomy proved in wh3_rank_four_kernel_obstruction.md and independently confirmed by the challenge worker. The historical rank-three proofs are unchanged.

## Theorem

Let R_n be arbitrary finite reference spaces, with no common dimension bound. Let X_n be faithful normalized states on C3 tensor R_n and let ξ_n be normalized states on the same spaces with rank ξ_n<=4. If ||X_n-ξ_n||_1 tends to zero, then

limsup_n Tr exp[2(W3 tensor id)(log X_n)-I tensor log (X_n)_R]<=1/3.

Equivalently, for every ε>0 there exists δ(ε)>0, independent of reference dimension, such that every faithful X within trace norm δ(ε) of the rank-at-most-four states has Φ(X)<=1/3+ε. This gives existence, not an explicit or effective numerical modulus.

If Φ(X_n) tends to 1/3, the approximants ξ_n must approach the union of the two previously identified saturation families: I3/3 tensor a pure reference state, and local-unitary images of the normalized antisymmetric rank-three projection. Thus no genuinely rank-four limit state saturates.

## 1. The exact dependency: rank-four Kraus-span geometry

For an output support P of dimension at most four, put

K=ker[2(W3 tensor id)(I-P)].

Its WH Kraus span S(K) lies in P. The referenced algebraic trichotomy states that dim S(K)<=4 implies at least one of:

(a) dim K<=1;
(b) K has a common physical support of dimension at most two;
(c) K is contained in C3 tensor a fixed reference line.

The coordinate transformations in that proof classify vector spaces only. No nonunitary reference filtering is used as an entropy invariance in the present argument.

For every normalized Y supported in K, define F(Y)=S(Y)+S(Y_R)-2S((W3 tensor id)Y). Each branch yields F(Y)<=-log 3:

- In (a), Y is pure. Its Schmidt weights λ give
  -F(Y)=2 log 2+sum_i[λ_i log λ_i-(1-λ_i)log(1-λ_i)]>=log 3.
  Equality requires uniform Schmidt rank three.
- In (b), the exact support-two channel decomposition is, up to local unitaries,
  (W3 tensor id)(Y)=(1/2)UYU-adjoint direct-sum (1/2)Y_R.
  Therefore S(output)=log 2+[S(Y)+S(Y_R)]/2 and F(Y)=-log 4 exactly.
- In (c), Y=A tensor |v><v|. The same scalar eigenvalue inequality gives 2S(W3(A))-S(A)>=log 3, with equality only at A=I3/3.

If K is zero, no normalized Y is supported there.

## 2. Apply dimension-uniform tightness with active reference dimension twelve

The proof in wh3_low_rank_dimension_uniform_boundary.md applies verbatim except that rank ξ_n<=4 implies dim supp (ξ_n)_R<=3*4=12 rather than nine. For clarity, its substantive steps are recorded here.

For the Gibbs maximizer Y_n, data processing gives

log Φ(X_n)<=F(Y_n)-D(NY_n||X_n), N=W3 tensor id.

The identity F(Y)=S(A|R)_Y-2S(B|R)_{NY} implies |F(Y)|<=3 log 3. On any subsequence with Φ(X_n)>=1/4,

D(NY_n||X_n)<=log 108.

Align supp (ξ_n)_R into a fixed C12 by local reference isometries, using the same embedding for inputs and outputs. This is legitimate because N acts only on the physical qutrit. Denote the projection onto C3 tensor C12 by Π_n. If q_n is the outside mass of X_n, then q_n<=||X_n-ξ_n||_1/2 tends to zero. Binary relative-entropy data processing forces the outside Gibbs mass p_n to satisfy

p_n<=log 216/log(1/q_n) ->0,

with p_n=0 when q_n=0 and the relative entropy is finite.

The normalized projected Gibbs state Yhat_n has trace distance at most sqrt(p_n) from Y_n. The elementary conditional-entropy modulus

f_3(t)=2t log 3+(1+t)h_binary(t/(1+t))

gives |F(Y_n)-F(Yhat_n)|<=3 f_3(sqrt(p_n))->0, independently of reference dimension.

Pass to convergent subsequences ξ_n->ξ and Yhat_n->Y in the fixed 36-dimensional space. A second binary test against supp ξ, using the same bounded relative entropy, forces supp NY subset supp ξ. Hence supp Y subset K(ξ).

The trichotomy in Section 1 now gives F(Y)<=-log 3. Taking limits in the Gibbs upper bound proves the claimed limsup inequality. This argument uses no continuity of relative entropy at a singular marginal and no compactness in an unbounded reference space.

## 3. Equality and saturation-family stability

If Φ(X_n)->1/3, the same compactness subsequence satisfies

0<=D(NY_n||X_n)<=F(Y_n)-log Φ(X_n)->0.

Pinsker, together with the truncation estimate, forces ξ=NY. Equality in Section 1 excludes the physical-plane branch, whose value is -log 4. The remaining cases require either maximally entangled pure Y or Y=I3/3 tensor |v><v|. Their WH images are exactly the two rank-three saturation families.

If ξ_n stayed a fixed positive distance from those families, an aligned compactness subsequence would contradict this classification. Therefore their distance to the union tends to zero. Local reference embeddings and physical unitaries are included when measuring that distance; no nonunitary filtering equivalence is asserted.

## Consequence and remaining frontier

A violation with any fixed positive gap above 1/3 must remain a dimension-uniform positive trace distance away from all rank-at-most-four states. Hidden reference dimensions, unequal vanishing eigenvalue rates and rotating supports cannot evade this conclusion.

This does not prove the unrestricted faithful Gibbs inequality, furnish a computable δ(ε), or rule out rank-five and higher boundary mechanisms. It excludes only the stated low-rank neighborhood frontier, using the newly verified rank-four trichotomy.
