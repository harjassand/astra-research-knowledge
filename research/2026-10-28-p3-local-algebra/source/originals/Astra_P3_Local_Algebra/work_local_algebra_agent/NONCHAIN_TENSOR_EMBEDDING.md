# Why a general local Frobenius centroid is not itself an evaluator

This is an exact embedding obstruction to a proposed generalization of the chain-ring counter. It does not prove a #P-hardness theorem or a lower bound against a different representation. It shows that replacing the chain-ring condition by an arbitrary local Frobenius algebra merely moves an arbitrary symmetric trilinear sum into the acquired multiplication table.

## Construction

Fix a finite field F of characteristic two, |F|=q, let U=F^k, and let S:U³ -> F be any symmetric trilinear form. Define the explicit F-vector space

    A=F·1 ⊕ U ⊕ U* ⊕ F·omega,

of dimension 2k+2. The identity acts as usual. On the other summands define

    u v = S(u,v,-) in U*,
    u phi = phi u = phi(u) omega,
    phi psi = 0,
    omega J = 0,

where J=U⊕U*⊕F·omega. Products extend bilinearly.

This algebra is commutative. The only potentially nontrivial associativity check within J is (uv)w=u(vw), and both sides are S(u,v,w)omega by symmetry. Therefore it is associative and unital. It is local, with nilpotent maximal ideal J and J^4=0.

Let lambda_A be the field trace of the omega coefficient. The pairing lambda_A(ab) is nondegenerate: 1 pairs with omega and U pairs perfectly with U*. This does not require S to be nondegenerate. Thus A is a finite local commutative Frobenius algebra. Its multiplication table has polynomial description length O(k³ log q) and is constructed directly from S.

For k>1 the algebra is not a chain ring. If rho is the dimension of the span of all S(u,v,-), then J² has dimension rho+1, so dim_F(J/J²)=2k-rho>=k>1. Thus the rejection by the chain recognizer is substantive.

## Full centroid of the scalar volume

Consider p_A(X,Y,Z)=lambda_A(XYZ) on A³. Its third binary difference is the scalar alternating A-volume tensor. Its radical is zero because lambda_A(ab) is nondegenerate. The argument in `CHAIN_ALGEBRA_ACQUISITION.md`, Section 6, works over any commutative Frobenius algebra: repeated-coordinate test vectors kill off-diagonal blocks, and setting one argument to the unit makes all remaining maps common scalar multiplication. Therefore its full balanced input-slot centroid is exactly A.

The algebra is not just a structure supplied alongside an unrelated hard function. It is the complete centroid acquired from the raw scalar cubic itself, with a free rank-three module over it.

## Exact character-sum reduction

Let psi(a)=(-1)^Tr_F/F2(a), and define

    Z_S = sum_(u,v,w in U) psi(S(u,v,w)),
    Z_A = sum_(X,Y,Z in A) psi(top_omega(XYZ)).

Then

    Z_A = q^(3k+3) Z_S + 3(q-1) q^(4k+3).

To prove this, write X=(a,u,phi,c), Y=(b,v,eta,d), Z=(f,w,theta,g). The top coefficient of their product is

    abg + afd + bfc
    + a(eta(w)+theta(v))
    + b(phi(w)+theta(u))
    + f(phi(v)+eta(u))
    + S(u,v,w).

Summing c,d,g by character orthogonality imposes ab=af=bf=0 and contributes q³. In a field, at most one of a,b,f is nonzero.

If all three vanish, phi,eta,theta are unconstrained and contribute q^(3k), leaving Z_S. This gives q^(3k+3)Z_S.

If exactly one scalar is nonzero, say a, the sums over eta and theta force w=v=0. All three dual vectors contribute q^(3k), while u is free and contributes q^k. The original top coefficients contribute q³. There are 3(q-1) such scalar choices. This yields the second term above.

Thus an exact evaluator for arbitrary acquired local Frobenius volumes would give

    Z_S = (Z_A - 3(q-1)q^(4k+3))/q^(3k+3)

for every symmetric trilinear S, in only a constant-factor larger number of independent field coordinates. The reconstruction has polynomial-bit arithmetic. The algebraic acquisition step alone has not simplified these arbitrary tensor sums.

## Executed validation

`nonchain_embedding.py` instantiates binary symmetric tensors of dimensions k=1,2,3,4, including mixed coefficients, constructs their algebras, checks associativity on every algebra basis triple and nondegeneracy of the Frobenius pairing, then acquires the full centroid of the raw scalar volume cubic. The centroid dimensions are exactly 4,6,8,10 and the original input counts are 12,18,24,30.

It checks the character-sum identity independently using

    Z_S=2^k #{(u,v):S(u,v,-)=0},
    Z_A=2^(2k+2) #{(X,Y):XY=0},

with exhaustive pair enumeration in these finite tests. There are 1,118,464 tested ring pairs in total, plus 5,632 raw scalar point identities. The k=1 test is the chain ring F2[t]/t^4; k>1 cases are correctly rejected as non-chain.

The construction belongs to the established setting of short local Gorenstein algebras and trilinear multiplication data. No priority claim is made. The explicit proof here avoids importing characteristic-zero classification statements into characteristic two. Related primary literature treats these distinctions, including *The weak Lefschetz property for standard graded Artinian Gorenstein algebras of embedding dimension four and socle degree three*: https://arxiv.org/abs/2404.08123
