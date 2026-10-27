# Rigidity of a full-Schmidt singular-output vector at relative peak 3/2

27 October 2026. Exact structural theorem, not a new entropy sign assertion.

Let X≥0 on C3⊗C3, τ=EX faithful, and X≤(3/2)τ. Suppose NX has a zero vector ψ with Schmidt rank three. In Schmidt coordinates ψ=Σsqrt(r_i)|ii>, put R=diag(r_i)>0. Then for some c>0,

X=c(I⊗R^(−1/2))P_sym(I⊗R^(−1/2)),
τ=(2c/3)I⊗R^(−1).

Conversely all these sources have relative peak exactly 3/2 and have ψ in the kernel of their actual WH output. No claim is made here for rank-deficient Schmidt ψ or larger reference dimension.

## Proof

Set A=(3/2)τ−X≥0. Since E(A)=τ/2,

(3E−N)(A)=NX.

The CP complement has adjoint

(3E−N)^*(Pψ)=(I⊗R+Pψ^(T_A))/2
 =K P_sym K,   K=I⊗sqrt(R).

The zero output expectation implies Tr[A K P_sym K]=0. Both operators are positive, so B=K A K is supported on the antisymmetric subspace. Also A≤(3/2)τ=3E(A); conjugating by the reference-only K gives

B≤3E(B)=I⊗Tr_A B.                              (1)

We show a positive operator B supported on wedge²C³ satisfies (1) only if it is a scalar multiple of P_asym. Any unitary on this three-dimensional antisymmetric space is induced by U⊗U, up to an irrelevant scalar phase: in a standard wedge basis the representation is det(U) conjugate(U), and this map is surjective on U(3). Conjugating both physical and reference systems by the same U preserves (1), so diagonalize B in that wedge basis. Let its eigenvalues a≥b≥c≥0, with a assigned to |12>−|21>. Its partial trace has entries (a+b)/2 and (a+c)/2 on the corresponding two reference coordinates (the naming of b,c is immaterial).

On span{|12>,|21>}, the operator I⊗Tr_A B−B has the matrix

(1/2) [[b,a],[a,c]]

up to swapping b,c or changing the off-diagonal sign. Positivity forces bc−a²≥0. But a≥b≥c≥0 implies bc≤a², with equality only when all three coincide (or all vanish). Thus B=cP_asym.

Therefore A=cK^(−1)P_asym K^(−1), and Tr_A P_asym=I gives τ=2E(A)=(2c/3)I⊗R^(−1). Subtracting A from (3/2)τ yields the claimed X. Faithful τ excludes c=0.

For the converse, E(X)=(2c/3)I⊗R^(−1), and the congruence-normalized source is (3/2)P_sym. Moreover

N(P_sym)=(3/4)(I−P_Φ),
NX=(3c/4)K^(−1)(I−P_Φ)K^(−1).

Its kernel contains KΦ, proportional to ψ. This checks the original channel output, not merely the CP-complement relaxation.

## Implication and limit

At the first zero-output relative peak, the sharp universal floor has rigid full-Schmidt saturation geometry: an arbitrary input cannot realize that floor without taking this filtered symmetric-projector shape. The marginal may be arbitrarily ill-conditioned. This is a candidate starting point for joint-curvature estimates or a separate VALUE receiver, not an extension of entropy whitening and not yet a quantitative stability theorem.

## Exact VALUE interface for the rigid family (not yet signed)

Write T=R^(−1)=diag(t_i). The nonzero input eigenvalues are c t_i and c(t_i+t_j)/2 for i<j. Its marginal is (2c/3)I⊗T. The actual output is

NX=(c/4)[3I⊗T−|v><v|],  v=Σsqrt(t_i)|ii>.

The off-correlated output eigenvalues are 3ct_i/4, twice for each i; the remaining three are c/4 times the eigenvalues of 3diag(t)−sqrt(t)sqrt(t)^*. One of the latter is zero. Thus the entropy inequality on this family reduces exactly to two homogeneous scalar ratios and one rank-one 3×3 log block. This reduction does not itself certify the sign.

Equivalently, the nonzero eigenvalues can be represented using the linear compressions P_sym(I⊗T)P_sym and (I−P_Φ)(I⊗T)(I−P_Φ), multiplied by c and 3c/4 respectively. The linear-compression representation may be useful for Hessian comparisons. It does not imply entropy is invariant under reference congruence, which would be false.

## VALUE corollary received from the existing low-Schmidt spectral theorem

The general entropy sign of this rigid family does not require a new scalar analysis. Section 4 of index_six_maximum_principle_and_rank_two_anchor_theorem.md proves the actual anchored gradient for an arbitrary source whenever its chosen top eigenvector has Schmidt rank at most two. Section 6 proves VALUE whenever there is an orthonormal eigenbasis of such vectors, by fixed-eigenbasis spectral lowering.

For the present source, choose |ii> and, on each pair {i,j}, the normalized vectors

sqrt(t_j)|ij>+sqrt(t_i)|ji>,
sqrt(t_i)|ij>−sqrt(t_j)|ji>.

The first pair-vector has eigenvalue c(t_i+t_j)/2 and the second has eigenvalue zero; every vector has Schmidt rank at most two. Together with the three product vectors |ii>, these form a complete orthonormal eigenbasis. Degeneracies cause no difficulty because the fixed chosen eigenbasis need not change. Every cumulative top-level projection is the sum of its rank-one low-Schmidt projectors, and spectral lowering remains covered even when the intermediate source leaves the filtered-symmetric family.

Consequently Δ(X)≥0 for every reference-filtered symmetric projector above, and thus for every source in the rigidity theorem. This is a direct application of the already received arbitrary-source anchor, not entropy whitening, a convex-mixture extension, or a new scalar sign proof. The earlier 'not yet signed' spectral interface records the state before this existing receiver was identified; this corollary supersedes that open sign status.
