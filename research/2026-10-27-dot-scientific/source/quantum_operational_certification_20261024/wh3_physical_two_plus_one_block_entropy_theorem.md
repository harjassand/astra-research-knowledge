# Full WH3 entropy theorem on every physical two-plus-one block cone

2026-10-25. Exact pointwise entropy theorem, arbitrary finite reference dimension and arbitrary noncommuting reference blocks. Uses the new audited product-top theorem and its physical-CQ spectral-lowering corollary.

## Theorem

Let A>=0 be block diagonal across a fixed decomposition C^3=C^2 direct-sum C:

A=X direct-sum Y,

where X>=0 acts on C^2 tensor R and Y>=0 acts on R. No rank, spectral, commutation or reference-marginal alignment condition is imposed. Then for N=W3 tensor id and E=I3/3 tensor Tr_A,

Delta(A)=D(A||EA)-2D(NA||EA)>=0.                     (1)

The decomposition can be in any orthonormal physical basis, by WH covariance. This does not cover a general qutrit input with coherences connecting all three physical labels.

## 1. The acquired diagonal receiver

Let Pi be full pinching in the chosen physical basis, tensored with identity on R. Then Pi A is physical-classical with three arbitrary positive reference blocks. Section6 of nonaligned_product_top_full_anchor_theorem.md proves

Delta(Pi A)>=0.

That proof uses actual-N product-top anchored gradients integrated along finite spectral flattening in the physical-CQ algebra; it does not replace the reference by a classical variable.

## 2. Actual WH output and the exact coherence coefficient

Put R_X=Tr_(C^2) X. The qubit identity

Tr(Z)I_2-Z^T=U Z U*, U=[[0,-1],[1,0]],

holds for every two by two matrix and therefore for operator-valued blocks. The actual qutrit WH output splits as

NA = (1/2)[(U tensor I)X(U* tensor I)+I_2 tensor Y]
      direct-sum (R_X/2).

Define physical coherence C(Z)=D(Z||Pi Z)=S(Pi Z)-S(Z), with unnormalized entropy. Its homogeneity and direct-sum additivity imply

C(A)=C(X),
C(NA)=(1/2) C((U tensor I)X(U* tensor I)+I_2 tensor Y).

The added operator I_2 tensor Y is Pi-invariant. Joint convexity and homogeneity of relative entropy give

C(Z+W)<=C(Z)+C(W)=C(Z)

whenever W is Pi-invariant. Since U exchanges the two physical labels up to phases, it preserves C. Consequently

C(NA)<= (1/2) C(A).                                  (2)

No general coherence half-contraction is asserted; the coefficient here follows from this exact block output and its actual incoherent noise.

## 3. Exact entropy assembly

The conditional expectation is unchanged by physical pinching, E(Pi A)=EA, and N commutes with this pinching up to the harmless basis permutation. Therefore

Delta(A)=Delta(Pi A)+C(A)-2C(NA).

Combining the acquired diagonal theorem with (2) proves (1). All identities hold on supported subspaces; alternatively add epsilon I and pass to finite-dimensional entropy continuity. Unnormalized A is allowed by homogeneity.

## Scope

This closes every input with only one possible physical off-diagonal pair, including arbitrary entanglement within that two-dimensional physical block and an arbitrary third reference block. It does not establish all qutrit inputs, nor an anchored-gradient maximum principle on this cone merely from its pointwise entropy positivity.

## Distinct open rank-two anchor interface

For a Schmidt-rank-two top vector psi in the X block, a physical-only phase twirl of an arbitrary A removes its couplings to the unused third physical label while keeping P=|psi><psi| and EA fixed. It cannot increase the actual anchored gradient. Let rho=Tr_(C^2) P and assume Xpsi=psi, 0<=X,Y<=I. The exact remaining anchored quantity is

g_N=log(4/3)+Tr rho[log(R_X+Y)-log R_X]
     -<psi,log(X+I_2 tensor Y)psi>.

This formula keeps arbitrary nonaligned R_X and arbitrary reference dimension. For Y=0 it equals log(4/3). The pointwise entropy theorem above does NOT alone prove nonnegativity of this derivative for Y>0. Independently replacing R_X by its norm bound or replacing X in only one logarithm is not justified.

A simple partial anchored certificate survives even without marginal alignment: put y=Tr(rho Y). Operator monotonicity gives Tr rho[log(R_X+Y)-log R_X]>=0, and scalar Jensen on psi gives <psi,log(X+I tensor Y)psi><=log(1+y). Thus

g_N>=log[4/(3(1+y))]>=0 whenever y<=1/3.

This is an anchored exclusion for that low-overlap subregion only, independent of the full-value cone theorem. The remaining overlap interval is not covered by this elementary bound.
