# Optional tighter conservative constant — reviewer-originated, separate from receipt
2026-10-29. New additive observation awaiting another reader; the accepted author's 32-bound is unchanged.

For real s and a Hamiltonian commutator L, exact integral Taylor expansion gives
 exp(sL)-I-sL = s^2 integral_0^1 (1-v) exp(vsL) L^2 dv.
Every exp(vsL) is a unitary-conjugation channel, of diamond norm one. Therefore the remainder norm is <=s^2 ||L||diamond^2/2<=2s^2, for all real s. Apply this separately to the physical controlled-SWAP generator (with the sample embedding/trace) and the effective controlled-tau generator. Zeroth and first terms agree, so local full-diamond error <=4s^2. Telescoping n fresh samples yields <=4t^2/n for every integer n>=1, with no n>=|t| restriction. As usual cap the stated distance by two.

Thus allocating n_j=max(1,ceil(4 |t_j| T/delta)) for each nonzero t_j gives total error <=delta and total samples <=4T^2/delta+number of nonzero operations. This is standard remainder analysis, not a new simulation method or optimality claim. It requires the same IID fresh-sample and ideal-control interface. It does not accept the separate filter construction.
