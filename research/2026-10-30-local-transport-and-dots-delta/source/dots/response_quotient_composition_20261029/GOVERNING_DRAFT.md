# Recovery response equivalence is not compositional
2026-10-29. Root construction. Independent review pending. No novelty claim.

## Question
Can the input-sensitive response, which suffices for single-use maximally mixed recovery fidelity, serve as a reusable representation for coding across multiple channel uses? In general no. The obstruction occurs already with two qubit uses and an explicit encoder/decoder. This limits a representation, not the possibility of scalable learning.

## Exact collapse under tensor composition
Let N,M:L(A)->L(B) be CPTP maps agreeing on all traceless operators. Write omega_N=N(I/d), omega_M=M(I/d); then N(X)-M(X)=Tr(X)(omega_N-omega_M). If their tensor squares also agree on every traceless operator of A tensor A, choose traceless Hermitian H with N(H)=M(H)=Y nonzero. Applied to H tensor I/d, tensor-response equality implies Y tensor (omega_N-omega_M)=0. Consequently omega_N=omega_M and N=M.

The sole exception is when both maps are replacement channels (all Y=0): any tensor powers remain replacement channels and all traceless responses vanish. Thus response equivalence is a valid one-use objective quotient, but its tensor-compatible equivalence classes are singletons except for the replacement class. This is an algebraic statement, not a tomography lower bound or a claim that every operational task needs full reconstruction.

Quantitatively, define s=sup_{H=H*,Tr H=0,||H||_1=1} ||N(H)||_1. For N,M with identical single-use response, the induced trace-norm difference of their tensor squares restricted to traceless Hermitian inputs is at least s ||omega_N-omega_M||_1. Indeed H tensor I/d has trace norm one and its image difference factors. Supremum is attained in finite dimension. No diamond norm is needed; allowing a reference only strengthens this lower bound.

## Explicit two-use recovery separation
Consider qubit channels N_t with Bloch map r -> r/5 + t Z, for t=0 and t=4/5. Both are CPTP, as checked in the predecessor's exact Choi matrices. They have identical Pauli responses, and the same optimal single-use maximally mixed entanglement fidelity 2/5 after a TP recovery.

Use the known repetition isometry E|0>=|00>, E|1>=|11>. Put lambda=c=1/5, a=(1+t+lambda)/2, b=(1+t-lambda)/2. The two output basis states are products of diagonal states with zero-populations a,b. Their difference has diagonal
  (lambda(1+t), -lambda t, -lambda t, -lambda(1-t)).
The offdiagonal logical matrix unit maps to c^2 |00><11|.

For any TP recovery R, its adjoint maps each output Pauli into the operator interval [-I,I]. Therefore each term Tr[Pauli R(Delta)] is at most ||Delta||_1, and
  Fopt(N_t tensor N_t after E) <= 1/4 + lambda(1+t)/4 + c^2/2.
The recovery with Kraus operators
  K0=|0><00|+|1><11|,
  K1=|1><01|,
  K2=|1><10|
is TP and simultaneously attains all three bounds for 0<=t<=4/5. Thus the exact optimum is 8/25 for t=0 and 9/25 for t=4/5.

Both values are below the single-use 2/5: this example proves failure of compositional sufficiency, NOT a coding advantage or a capacity separation. Its encoder and decoder are explicit and identical for both channels. No unknown-environment access or learned inverse is assumed.

## Consequence for the current programme
Rank of the one-use input-sensitive support is an objective-specific acquisition parameter, not automatically an extensive complexity parameter for a code family. Tensoring introduces background-weighted responses. A scalable theory must either acquire the response of the actual encoded channel, control these new terms structurally, or prove that a weaker task-specific representation suffices. The accepted one-use information-support theorem is unchanged.
