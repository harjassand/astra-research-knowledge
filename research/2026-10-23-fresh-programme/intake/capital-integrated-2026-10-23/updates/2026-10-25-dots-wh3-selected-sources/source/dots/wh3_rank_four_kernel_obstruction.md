# A general rank-four boundary obstruction from skew-matrix geometry

24 October 2026, root derivation; independent challenge requested. This is not the previously closed SU(2)-invariant example. Its proposed scope is every output support of dimension at most four.

For a subspace K of C3 tensor R define its WH Kraus span
 S(K)=span{(L_i tensor I)psi:psi in K,i=1,2,3},
where L_i span all complex antisymmetric3×3 matrices. Suppose dim S(K)<=4.
Then at least one of the following holds:
1. dim K<=1;
2. K has a common physical support of dimension at most two;
3. K is contained in C3 tensor a fixed reference line.

## Algebraic proof

Represent vectors by3×r matrices M. If M has rank at least two, the map A→AM from the3D space of skew matrices is injective. For two independent such vectors M,N, each Kraus span has dimension three, so the intersection has dimension at least two.

First suppose M has rank three. Replace an independent N by M+epsilon N if necessary so it too has rank three. Two independent skew matrices A1,A2 satisfy Ai N in S(M). In reference coordinates outside M's support, both Ai annihilate every column of N. Distinct nonzero skew3×3 matrices have distinct one-dimensional kernels, so those columns vanish. Restrict to the common3D reference support and multiply on the right by M inverse. This is a dimension-preserving algebraic change of coordinates, NOT an entropy-preserving physical filter. Now M=I and the two skew matrices satisfy
 A_i T=T^T A_i,  T=N M inverse.
Each A_i gives an invariant kernel line for T; on its two-dimensional quotient, the induced T is self-adjoint for a nondegenerate skew form and therefore scalar. Two distinct kernel lines force these scalars to agree and force T to be scalar on the whole3D space. This contradicts independence. Thus a K of dimension at least two cannot contain a Schmidt-rank-three vector.

If K contains a rank-two M, choose physical Schmidt coordinates and a right-invertible reference change so
 M=[[1,0],[0,1],[0,0]].
For any independent N, replace it by M+epsilon N so its rank is two. As above, two skew intersection matrices force N to have no reference columns outside this two-dimensional support. Write
 N=[[p,q],[r,s],[t,u]].
For A=[[0,−z,y],[z,0,−x],[−y,x,0]], the condition AN in S(M) is the homogeneous system with coefficient rows
 (0,t,−r), (−u,0,q), (−t,u,p−s).
Its nullspace must have dimension at least two, so its rank is at most one. But any nonzero t or u makes two displayed rows independent. Hence t=u=0. Reversing the right-coordinate change, every vector in K has the same two-dimensional physical support.

Finally, if all nonzero vectors in K are product, linearity forces a common physical factor or a common reference factor: otherwise the sum of two product vectors with independent factors has Schmidt rank two. This gives case2 or3.

## Entropic consequence once the algebra is accepted

Let P be an output support of rank at most four, and K=ker[2(W3 tensor id)(I−P)]. Then S(K) is contained in P, so the dichotomy applies.

- A one-dimensional K permits only a pure input. The previously proved Schmidt-weight inequality gives F<=−ln3.
- For any input supported on a physical plane, W3 has the exact direct-sum form .5 W2(rho) direct-sum .5 rho_R. W2 is a unitary channel. Therefore S(output)=ln2+.5S(input)+.5S(reference), and F is exactly−ln4, for EVERY state on that plane.
- On a fixed reference line the input is a product state, and the ordinary qutrit complement entropy inequality gives F<=−ln3.

The Gibbs-duality boundary argument then excludes all approaching output states of rank at most four, once its dimension-uniform tightness extension is applied with active reference dimension at most12 instead of9. Equality still requires the uniform product state or a locally unitary antisymmetric rank-three state; the physical-plane case has a strict gap.

This does not prove the faithful global inequality, or rule out rank-five and higher boundary mechanisms. The coordinate whitening above is used only to classify vector spaces. No relative entropy, energy, or physical state is claimed invariant under that nonunitary change of coordinates.
