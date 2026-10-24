# Dimension-uniform exclusion near support rank at most three

24 October 2026. Root's proposed extension, independently verified with explicit embeddings and an elementary dimension-free continuity argument. This extends wh3_low_rank_boundary_arbitrary_paths.md beyond fixed reference dimension. It does not establish the general faithful Gibbs inequality.

## Theorem

For each n let R_n be any finite-dimensional reference, X_n a faithful normalized state on C3 tensor R_n, and ξ_n a normalized state on the same space with rank ξ_n<=3. Suppose ||X_n-ξ_n||_1 tends to zero. Then

limsup_n Φ(X_n)<=1/3,

where Φ(X)=Tr exp[2(W3 tensor id)(log X)-I tensor log X_R]. There is no uniform upper bound assumed on dim R_n, no prescribed eigenvalue rates, and no fixed-support assumption.

Equivalently, for every positive ε there exists a positive δ, independent of reference dimension, such that every faithful normalized X within trace norm δ of some normalized rank-at-most-three ξ satisfies Φ(X)<=1/3+ε. This existence statement does not provide a numerical modulus δ(ε).

If additionally Φ(X_n) tends to 1/3, then the approximating ξ_n approach the known saturation families, allowing local reference embeddings: I3/3 tensor a pure reference state, and local-unitary images of the normalized antisymmetric rank-three projection. The precise subsequential form is proved below.

## 1. Uniform Gibbs penalty and the right entropy functional

Let N=W3 tensor id and let Y_n be the normalized Gibbs maximizer for X_n. Define

F(Y)=S(Y)+S(Y_R)-2S(NY)
    =S(A|R)_Y-2S(B|R)_{NY}.

Both physical dimensions equal three, so |F(Y)|<=3 log 3, independently of the reference. The exact Gibbs identity and data processing imply

log Φ(X_n)=F(Y_n)-2D(NY_n||X_n)+D((Y_n)_R||(X_n)_R)
          <=F(Y_n)-D(NY_n||X_n).                   (1)

If the limsup of Φ is at most 1/4, the theorem is immediate. Otherwise choose a subsequence realizing that limsup with Φ(X_n)>=1/4. Along this subsequence,

D(NY_n||X_n)<=C:=3 log 3+log 4.                    (2)

All Gibbs expressions are defined on the original finite spaces. Later isometric embeddings are used only for comparisons, not to assign logarithms to their added zero subspaces.

## 2. Align the low-rank reference supports legitimately

A bipartite state of rank at most three on C3 tensor R has reference support dimension at most nine: decompose it into at most three pure states, each of Schmidt rank at most three.

Choose a reference isometry V_n:R_n -> C9 direct-sum E_n mapping supp (ξ_n)_R into C9 and its orthogonal complement into E_n. This is always possible with finite E_n. The same V_n is used for X_n, ξ_n, Y_n and their outputs. Since N acts only on the physical qutrit, it commutes with this reference embedding. Entropies and relative entropies on the original supports are unchanged.

Write Π_n=I3 tensor P_C9. The embedded ξ_n are all states in the same fixed 27-dimensional subspace. Their rank remains at most three.

## 3. Binary relative entropy gives Gibbs tightness

Let q_n=Tr[(I-Π_n)X_n] and p_n=Tr[(I-Π_n)Y_n]. The reference marginal is unchanged by N, so p_n is also the outside probability for NY_n. Because ξ_n is entirely inside Π_n,

q_n<=||X_n-ξ_n||_1/2 ->0.

Binary measurement data processing and (2) give d(p_n||q_n)<=C. For q in (0,1),

d(p||q)>=p log(1/q)-h_binary(p)>=p log(1/q)-log 2.

Therefore p_n<=(C+log 2)/log(1/q_n) tends to zero. When q_n=0, finiteness of the relative entropy forces p_n=0 directly.

Normalize the projected Gibbs state:

Yhat_n=Π_n Y_n Π_n/(1-p_n).

It lives on C3 tensor C9. Its trace distance from Y_n is at most sqrt(p_n). One proof is to purify Y_n and project its purification; the normalized projected purification has overlap sqrt(1-p_n) with the original, and trace distance contracts under partial trace.

## 4. Dimension-free continuity of F, derived by flagged mixtures

For states ρ,σ with physical dimension d and δ=||ρ-σ||_1/2, define

f_d(δ)=2δ log d+(1+δ)h_binary(δ/(1+δ)).

Then |S(A|R)_ρ-S(A|R)_σ|<=f_d(δ), regardless reference dimension.

For completeness, use the positive and negative parts ρ-σ=δ(τ_+-τ_-). The common state

γ=(ρ+δτ_-)/(1+δ)=(σ+δτ_+)/(1+δ)

has two flagged-mixture descriptions. For either description, conditional entropy minus the weighted conditional entropies lies between zero and the binary flag entropy: the difference is I(A:flag|R), bounded between zero and H(flag). Subtract the descriptions, use the range -log d<=S(A|R)<=log d, and obtain f_d. This proves the required modulus directly rather than assuming ordinary entropy continuity with a bounded total dimension.

Since N contracts trace distance and both physical dimensions are three,

|F(Y_n)-F(Yhat_n)|<=3 f_3(sqrt(p_n)) ->0.         (3)

Thus reference leakage cannot carry a hidden finite contribution to F.

## 5. Fixed-dimensional compactness and support forcing

Pass to a further subsequence with ξ_n -> ξ and Yhat_n -> Y inside C3 tensor C9. The limit ξ has rank at most three. By (3) and finite-dimensional continuity,

F(Y_n)->F(Y).

Let P be the support projection of ξ, acting as zero on each extra E_n. The probability Tr[(I-P)X_n] tends to zero, because X_n is close to ξ_n and ξ_n tends to ξ. A second application of the binary relative-entropy estimate, now using this joint physical-reference projection P and (2), shows

Tr[(I-P)NY_n]->0.

Trace-distance contraction and ||Y_n-Yhat_n||_1->0 then imply Tr[(I-P)NY]=0. Hence supp NY is contained in supp ξ. Equivalently, supp Y is contained in the Kraus-support kernel K(ξ) classified in wh3_low_rank_boundary_classification.md.

That classification and its entropy calculation prove F(Y)<=-log 3. Taking limits in (1), while dropping the nonnegative relative entropy, gives limsup log Φ(X_n)<=-log 3, proving the theorem.

No relative-entropy continuity with a singular marginal has been used. The two binary measurements and the conditional-entropy modulus replace the missing global compactness.

## 6. Saturating subsequences

Suppose Φ(X_n)->1/3. Along every compactness subsequence above, (1), (3), and F(Y)<=-log 3 imply

0<=D(NY_n||X_n)<=F(Y_n)-log Φ(X_n)->0.

Pinsker and truncation therefore give ξ=NY. Equality in the already-proved kernel entropy bounds forces one of two possibilities:

- Y is a maximally entangled qutrit state and ξ is its WH image, a local-unitary normalized antisymmetric projection;
- Y=I3/3 tensor |v><v|, in which case ξ=Y.

Thus every aligned convergent subsequence has a saturation-family limit. In particular, if the distance of ξ_n to the union of these families failed to tend to zero, a subsequence bounded away from them would produce a contradiction by the same compactness argument. Conversely, the existing uniform white-noise paths at these families attain boundary value 1/3.

## Scope

This is a dimension-uniform boundary exclusion near rank at most three, not a proof of the unrestricted faithful Gibbs inequality. It allows arbitrary finite reference dimensions, eigenvalue rates and support rotations because the physical channel dimensions stay fixed and the approximating low-rank reference supports have dimension at most nine. It does not claim an explicit neighborhood radius, exact upper semicontinuity to the uniform-path value at every nonsaturating state, or control near higher-rank states.
