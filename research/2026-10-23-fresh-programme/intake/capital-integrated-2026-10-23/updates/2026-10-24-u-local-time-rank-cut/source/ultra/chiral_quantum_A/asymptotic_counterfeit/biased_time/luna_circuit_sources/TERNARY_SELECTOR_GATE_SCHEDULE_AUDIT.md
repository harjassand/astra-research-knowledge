# Ternary reversible-selector gate and schedule audit

Scope: exact identities and the explicit layout in
`../REVERSIBLE_BIAS_AMPLIFICATION_OPENING.txt`. Gate lists are chronological.

## Three-bit map and nearest-neighbor cost

For input `(x,y,z)`, the first three gates give
`x1=x xor y=s1`, `y1=y xor z=s2`, and `z1=z xor y1=y`. The final
`Toffoli(x1,y1;z1)` gives
`q=y xor (s1 AND s2)=Maj(x,y,z)`: when either neighbor equals `y` the
product is zero, and when both differ they are both `1-y`, so the product
flips `y`. Thus the outputs are exactly `(s1,s2,q)` with no phases; all
operations are controlled/permutation unitaries. The two parity bits and
majority identify the input uniquely.

For Toffoli with physical order `[x,y,z]` (controls `x,y`, target `z`),
the chronological fixed-alphabet word is
`CV(y,z)`, `CNOT(x,y)`, `CV†(y,z)`, `CNOT(x,y)`, `CV(x,z)`.
The first four gates are adjacent. Route the last outer gate by
`SWAP(y,z)`, `CV(x,z)`, `SWAP(y,z)`; the passenger is restored exactly,
with no phase because SWAP is the exact permutation unitary. This costs
`4+3=7` nearest-neighbor two-qubit gates. Adding the three adjacent CNOTs
for P3 gives 10 total. This is an explicit fixed-alphabet compilation,
not a universal-control assertion.

## Ternary routing and schedule counts

Set `L=3n`. Before the parent P3, child-root payloads are at zero-based
positions `n-1`, `2n-1`, `3n-1=L-1`. Move the middle payload right to
`L-2`, costing `n-1` swaps. Then move the first payload right to
`L-3`, costing `2n-2` swaps. The second path stops before the third payload;
it does not cross either selected payload. Apply P3 to `[L-3,L-2,L-1]`
and reverse the routing in reverse order. Every nonselected wire is
restored, while the two parent syndromes and parent payload return to the
first, second, and third child-root positions, respectively.

The parent overhead is `2[(n-1)+(2n-2)]+10 = 2L+4` gates/layers. Children
run in parallel, so for `L=3^k`, `D_P(1)=G_P(1)=0` and
`D_P(L)=D_P(L/3)+2L+4`, while
`G_P(L)=3G_P(L/3)+2L+4`. Summing gives the stated explicit-schedule
counts
`D_P(L)=3(L-1)+4k` and `G_P(L)=2Lk+2(L-1)`.

Given the stated `L-1` adjacent-SWAP implementation of `Pi_block`,
`Omega=P_shifted^{-1} Pi_block P` uses two P schedules plus that block
permutation. Therefore
`D_Omega=2D_P+(L-1)=7(L-1)+8k` and
`G_Omega=2G_P+(L-1)=4Lk+5(L-1)`.
These are schedule costs for this construction, not optimality claims.
