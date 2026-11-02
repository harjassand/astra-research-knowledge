# The selected finite-flag channel is not antidegradable

This is a diagnostic theorem fixing the scope of the negative search. It is NOT a positive-capacity theorem. The channel is the explicitly specified ideal rectangular-GKP logical channel with three receiver flags, obtained by the 64×64 lookup partition at v=0.38, aspect r=3 in `certified_repetition_quantizers.json`. A mathematical modular-syndrome instrument is specified; no physical finite-energy GKP preparation or efficient receiver is asserted.

Let t[f,i] be the joint mass of flag f and Pauli i, in order I,X,Y,Z. Define

    H = (1/2) [[1,1,1,1], [1,1,-1,-1],
               [1,-1,1,-1], [1,-1,-1,1]].

## Exact self-compatibility reduction

A channel is antidegradable iff it has a joint extension to two output copies with the same channel as each marginal. One direction applies the antidegrading map to a Stinespring environment. Conversely, in a dilation of a joint-output channel, the second output is contained in the first marginal's environment.

Dephase both output flags and twirl such an extension under the simultaneous Pauli action. Neither operation changes the required Pauli-channel marginals. For each pair of flags f,g, its three-qubit Choi block has the form

    W (R[f,g] tensor I_2/2) W†,    R[f,g] >= 0.

Here W maps |i,s> to |Bell_i>_AB tensor P_i|s>_C, with |Bell_i>=(I tensor P_i)|Phi+>. The corresponding basis using pair AC instead of AB differs by H tensor I_2; direct exact Pauli algebra verifies this identity. Therefore necessary (indeed sufficient) compatibility constraints are

    sum_g diag R[f,g] = t[f,:],
    sum_f diag(H R[f,g] H) = t[g,:].

A separating dual consists of four-component real vectors u[f],v[g] such that every

    D[f,g] = diag u[f] + H diag v[g] H

is positive semidefinite but

    C = sum_f (u[f]+v[f]) dot t[f,:] < 0.

For any compatible channel, C=sum_fg Tr(D[f,g]R[f,g]) >= 0, a contradiction.

## Verified certificate

`non_antidegradable_rational_dual.json` stores u,v as exact rational numbers with denominator 10^10. `certify_non_antidegradable.py` verifies all nine D matrices are positive definite by exact rational LDL elimination (all pivots positive; the smallest pivot is approximately 3.8460e-6). It then evaluates the linear target functional using the exact dyadic probability enclosure endpoints from the independent Gaussian integration certificate. The result is

    -0.000017215448554546446 <= C <= -0.00001721544581367059 < 0.

The precise rational endpoints, not these display decimals, are saved. The lookup table SHA256 is

    9e7cf502c6c734cc1fed4d63245f14fd86669c72829c75d90db424880a58e199.

Thus this specifically defined flagged channel is not antidegradable, despite the separate all-length obstruction to equal-mixture Clifford-axis repetition codes. Its quantum capacity remains undetermined here; neither zero capacity nor positive capacity follows. No novelty claim is made for the compatibility reduction, and the unsuccessful least-squares feasibility search is not being mistaken for a certificate: the rational dual and interval target bound provide the proof.
