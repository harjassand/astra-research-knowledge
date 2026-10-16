# Two-symbol analytic qubit-reference estimation family

Status: internally derived and independently reconstructed. External review and historical priority remain open. This is a lower-dimensional construction, not an optimality theorem over all encodings.

Use the two prepared qubit states sigma_+=(I+aX)/2 and sigma_-=(I+aY)/2, 0<a<1. A common output unitary rotates them to (I+bZ±bX)/2 where b²=a²/2. Put c=b².

For each classical input sign, take reference baseline B_i=diag(1,delta)/2 and tangent H_+=X/2, H_-=-X/2. The balanced label states have conditional blocks (B_i±tH_i)/(1+delta). They are normalized, have identical reference marginal, and are faithful on these two classical inputs whenever delta>0 and t²<delta. A third input, if retained in the alphabet, has zero weight; a sufficiently small common positive block can regularize it while preserving any strict gap.

The raw input SLD cost is 4/(1+delta). The target baseline has flag blocks A and delta A, A=(I+bZ)/2; the offdiagonal tangent block is bX/2. Solving the two scalar Sylvester equations gives

g_target=4c(1+delta)/[(1+delta)²-c(1-delta)²].

The target/input ratio is R=c/[1-c((1-delta)/(1+delta))²]. Since the total reference tangent is zero, the erasure SLD cost is q times the input cost. Hence the exact normalized binary MMSE gap is

Delta=4t²/(1+delta)² * [R-q].

This yields a positive gap whenever q<c/(1-c) and delta is sufficiently small. Ordinary reference-free SLD threshold is c, while the two-output complete threshold is c/(1-c). Thus c<q<c/(1-c) gives the intended ordering reversal.

At the rank-deficient limiting choice t²=delta, write x=((1-delta)/(1+delta))². The gap is (1-x)[c/(1-cx)-q]. For c<=q<c/(1-c), its maximum within this family is

[1-sqrt(q(1-c)/c)]²,

attained at 1-cx=sqrt(c(1-c)/q). This is only the supremum in this restricted family, and faithful choices approach it. No global two-level-memory optimum is asserted.

At a=3/5, c=9/50, q=1/5, delta=1/16, t=6/25, the exact gap is positive. The comparison is the same physical output pair and erasure channel, with an explicit two-level quantum reference. It is not an implemented experiment.
