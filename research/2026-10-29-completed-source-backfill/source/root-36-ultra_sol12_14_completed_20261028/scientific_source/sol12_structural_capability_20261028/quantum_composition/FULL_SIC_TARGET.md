# Full SIC dual receiver and the remaining quantum-memory operation

The acquired five-support theorem alone does not establish all nine
weights. The peer subsequently paid the following alternative receiver
by nine-vector majorization; independent reconstruction is in
`PEER_MAJORISATION_CHALLENGE.md`:
`sum_(i=1)^9 exp(2 Tr S_i K) <= (Tr exp K)^2`
for every Hermitian three-by-three K. This equivalence is a standard
Gibbs-variational transformation of the acquired channel identity; no
priority is claimed for Fenchel/Gibbs duality.

Indeed `S(M)=inf_K[log Tr exp K-Tr MK]`. Thus
`inf_p [2S(sum p_i S_i)-H(p)]`
`=inf_K [2log Tr exp K-log sum_i exp(2Tr S_i K)]`.
The infima commute because they are infima over a product domain; no
minimax interchange is used. The inner minimization over p is classical
Gibbs and yields weights proportional to `exp(2Tr S_i K)`. Singular M
requires the usual faithful approximation. A scalar shift of K cancels
on both sides, so traceless Hermitian K suffices (eight real parameters).

A certified strict failure at K would construct an actual negative
Bell-mixture deficit: choose those Gibbs weights and use
`2S(M_p)-H(p)<=2log Tr exp K-log sum_i exp(2Tr S_i K)<0`.
Conversely a negative deficit gives a violating K, directly for faithful
M and by a sufficiently small faithful regularization otherwise. No
violating K is acquired in this work; majorization excludes it.

The ordinary SIC two-design identity followed by scalar Jensen gives
only a factor 3/2 on the right side, so it does not pay the desired bound.
Likewise the sharp purity envelope already fails for support six. Those
are failures of relaxations, not negative quantum sources or hardness
results. The full scalar SIC inequality is now paid by the peer
construction. It covers Bell-diagonal sources, not every qutrit/reference
state.

An exact composition test is already available. Compose the
acquired five-branch channel with the received two-branch channel having
weights 3/4 at label00 and1/4 at label20. Weyl phases cancel under
conjugation, so composition convolves label probabilities modulo three.
In order `(00,01,02,10,11,12,20,21,22)` the resulting vector is
`(194,25,12,6,3,0,64,8,4)/316`.
It has eight positive weights, so the sparse rule alone cannot receive
it. The peer's full scalar result now receives the target and arbitrary
finite Weyl convolution. This is an actual composition closure, with no
negative quantum source inferred from earlier relaxation failures.

## Narrow quantum-memory operation still unpaid

Let independent PSD matrices C_i act on a logical memory L and set
`X=sum_i P_Phi_i tensor C_i`, `C=sum_i C_i`,
`M=sum_i S_i tensor C_i`. The SAME exact AB permutation proves
`NX=I3/3 tensor M` and `EX=I9/9 tensor C`. Orthogonality of the Bell
projectors and cancellation of trace-log3 terms give the exact identity
`Delta(X)=sum_i Tr C_i log C_i+Tr C log C-2Tr M log M`.
Thus the next receiver is a conditional SIC preparation inequality,
`2S(M)>=S(sum_i |i><i| tensor C_i)+S(C)`, when TrC1.

Commuting C_i are already paid by simultaneous diagonalization and the
full scalar theorem. The common affine form `C_i=p_i U+V` is paid by the
inherited common-bath lift. Arbitrary independent noncommuting C_i are
not received by scalar eigenvalue majorization alone. Their PSD/memory
interface must be acquired; scalar-to-quantum-side-information transfer
is not free. This is a specific unpaid operation, not a global hardness
claim. It is NOT_ESTABLISHED in this work.
