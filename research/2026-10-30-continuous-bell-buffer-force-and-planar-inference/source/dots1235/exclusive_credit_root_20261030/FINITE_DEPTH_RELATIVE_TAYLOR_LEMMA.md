# Finite-depth relative Taylor lemma for conservative GKLS plus signed killing
2026-10-30. Root proof. Independent review pending. This is a general algebraic/locality lemma, not by itself the actual LOCC lifetime theorem.

## Assumptions
Consider N finite-dimensional sites on a bounded-degree interaction graph. Let

 L_c(O)=i[H,O]+sum_e (J_e† O J_e−{J_e†J_e,O}/2)

be a conservative Heisenberg GKLS generator. H=sum_e H_e with H_e Hermitian. Let Delta=sum_e D_e be Hermitian, with every D_e Hermitian but not necessarily positive. There are O(N) terms, each supported on at most a fixed-radius cone, with uniform bounds on ||H_e||, ||J_e|| and ||D_e||. All constants are independent of N.

Let X_i be self-adjoint bounded-support bounded-norm operators with bounded overlap. Partition them into D fixed colors such that supports in each color are pairwise disjoint. For fixed real weights w_i with |w_i|<=1 set

 Y(u)=product_colors [product_(i in color) exp(u w_i X_i/2)],
 G(u)=Y(u)†Y(u),       X=sum_i w_i X_i.

The order of colors is fixed. No commutation between different colors is assumed. Define

 B(u)=Y(u)^(-†) [L_c(G(u))−{Delta,G(u)}/2] Y(u)^(-1).

## Claim
For fixed u_0<infinity there is C independent of N such that, for |u|<=u_0,

 ||B(u)+Delta−u L_c(X)|| <= C N u².                    (1)

In particular B(u)<=−Delta+u L_c(X)+CNu² I. This requires no positivity of Delta or its individual local terms, and no special zero-sector corner property of X_i.

## Exact local formula
For any operator A write A(u)=Y(u) A Y(u)^(-1). Direct multiplication, with no approximation, gives

 B(u)=sum_e [J_e(u)†J_e(u)−(Gamma_e(u)+Gamma_e(u)†)/2]
       +sum_e i[H_e(u)†−H_e(u)]
       −sum_e [D_e(u)+D_e(u)†]/2,                       (2)

where Gamma_e=J_e†J_e. For example the gain term is

 Y^(-†)J_e†Y†YJ_eY^(-1)=J_e(u)†J_e(u).

At u=0 each dissipator contribution vanishes, each Hamiltonian contribution vanishes, and B(0)=−Delta.

## First derivative
Y(0)=I and Y'(0)=X/2, where X is self-adjoint. Thus G'(0)=X. Since L_c(I)=0, differentiating the relative L_c(G) term gives L_c(X) with no zeroth-order conjugation contribution. The killing term in (2) has derivative

 -([X,Delta]+[X,Delta]†)/4=0,

because X and Delta are self-adjoint. Therefore B'(0)=L_c(X). The cancellation is not a claim that X commutes Delta.

## Uniform second derivative uses finite cones, not global norms
Conjugate a single fixed-support A successively through the D color layers. In a layer, every gate whose support is disjoint from the current support commutes A and cancels with its inverse. Since same-color supports are disjoint, that layer enlarges the support by only one bounded neighborhood. After D layers the support and number M of relevant gates are bounded independently of N.

Thus A(u) is exactly a product of at most M exponentials, A, and at most M inverse exponentials. Their generators have uniformly bounded norm. Differentiating this finite product zero, one or two times yields

 ||A^(j)(u)|| <= C_j ||A||,      j=0,1,2,

uniformly for |u|<=u_0. The constants depend on D, the overlap/cone bounds and local X norms, never N. Applying the product rule to J_e(u)†J_e(u) gives the analogous bound C||J_e||². Equation(2) consequently gives ||B''(u)||<=C N. Taylor's integral remainder proves(1).

This is why the estimate is O(N), despite ||X||=O(N): no global norm bound on X or Y is used.

## Unequal proof strengths and actual application
Choose u=max_i |epsilon_i| and w_i=epsilon_i/u (the u=0 case is immediate). The first-order term is sum_i epsilon_i L_c(X_i), and the error is CN max_i|epsilon_i|². In the proposed native composition, debt strength is delta=sqrt(lambda)t and exposure/activity strengths are O(lambda t), so the error is O(lambda t² N). Dividing by the intended useful drift scale lambda t gives a small O(t) density.

For a positive physical raw observable W0, let S=W0^(1/2) and define L_w(O)=S^(-1)L^*(SOS)S^(-1), Delta=−L_w(I), L_c=L_w+{Delta,·}/2. When this conservative generator and Delta have the bounded local decomposition above, the physical dressed observable W=S G S satisfies exactly

 (Y S)^(-†) L^*(W) (Y S)^(-1)=B(u).

The proof does not establish that an arbitrary global W0 has a local tilt. The separate local-discount representation and actual raw-energy locality must earn that assumption. Nor does it establish the first-order useful-service estimate or the decoding/confinement bridge. Those remain separate load-bearing obligations.
