# A fixed pure qubit witness for every serial iterate

9 October 2026. Elementary supplement to Section 6 of FINITE_CRITERION.md. The reviewed criterion is preserved unchanged. This pure-input refinement was derived after that review and is not represented as separately externally certified or priority checked.

## Statement

If a completely positive map Phi on M_d has no entanglement-breaking power, then there are orthogonal unit vectors u,v in C^d such that the single pure input

 psi = (|0> tensor u + |1> tensor v)/sqrt(2)

has an NPT output under id_2 tensor Phi^n for every positive integer n. For a non-trace-preserving map every such output is nonzero; normalizing its trace preserves this assertion.

The amount of entanglement may tend to zero arbitrarily rapidly. This gives no robust storage, positive quantum capacity, finite-precision experimental certificate, or tensor-power distillability conclusion.

## Proof

Use the finite criterion with L=lcm(1,...,d), Psi=Phi^L and m=d^2. Its negative certificate gives an invariant projection P, Q=I-P, and cross transfer

 T: P M_d Q -> P M_d Q,   T(X)=P Psi(X) Q,

such that T^m is nonzero. The cross space has dimension k=rank(P)rank(Q)<=m. For a linear map on a k-dimensional space, the increasing kernels ker(T^j) have stabilized by j=k. Hence ker(T^m) contains every vector killed by any positive power of T.

Rank-one matrices u v*, with u in PH and v in QH, span the cross space. Since ker(T^m) is a proper subspace, some such rank-one X lies outside it. Normalize u and v to unit length, which does not change membership in the kernel. Then T^n(X)!=0 for every n>=1: if T^n(X)=0 for n<=m, then T^m(X)=0, while n>m is excluded by kernel stabilization.

For rho=|psi><psi|, the output under id_2 tensor Psi^n has qubit-block form

 (1/2) [[A_n,B_n],[B_n*,D_n]],

where A_n=Psi^n(u u*) is supported on P and P B_n Q=T^n(X)!=0. Its partial transpose on the qubit is

 (1/2) [[A_n,B_n*],[B_n,D_n]].

For every q in QH, the vector |0> tensor q has zero diagonal quadratic form. For suitable q in QH and p in PH, its matrix entry against |1> tensor p equals q* B_n* p /2 and is nonzero. A positive semidefinite matrix with a zero diagonal quadratic form must annihilate that vector, so the partial transpose is not positive. Thus the same rho has NPT output at every positive multiple of L.

Suppose the output under an intermediate Phi^j were PPT. For any n with Ln>=j, the later output follows by the local CP map id_2 tensor Phi^(Ln-j). Partial transpose on the unchanged qubit commutes with that evolution, so positivity of the partial transpose would persist. This contradicts the result at Ln. Therefore every positive iterate has NPT output on the same pure input.

## An exact qutrit illustration

For the rational CPTP family in NONFAITHFUL_BOUNDARY_EXAMPLE.md and t!=0, choose u=|0> and v=|1>. Then

 Phi_t^n(|0><1|)=(epsilon t)^n |0><1|,
 epsilon=1/8,   r=1/2.

After qubit partial transpose, the principal submatrix on |0,1>, |1,0> is

 [[0, (epsilon t)^n/2],[(epsilon t)^n/2, (1-r^n)/2]].

Its determinant is -(epsilon t)^(2n)/4<0. Its negative eigenvalue tends to zero even though no finite iterate becomes PPT. The local script verify_fixed_pure_witness.py checks this expression in exact rational arithmetic on bounded examples; the general assertion follows from the proof above, not from those tests.
