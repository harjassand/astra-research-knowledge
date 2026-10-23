# Additional bounded check for the new opposite transport geometry

Written before executing this check, after the original Cycle7 reciprocal
diagnostic passed. The first contract, code and results remain unchanged.
The concrete new risk is confusing per-vertex acceptance or single-leaf
retention with a quotient holding probability in the fan-out construction.

Use n=2,m=16,b=1/4,K=3,alpha=1/2,eta=1/4. There is one root, 16 leaves
and one core. Native q=(1/4, sixteen copies of 1/1024,47/64),
pi=(1/8,sixteen copies of 1/32,3/8). Q chooses a uniform leaf from the
root, sends every leaf to the root, and holds the core. Use kappa=1/2
for the mismatch and kappa=1/4 for the matched control.

Compute individual-state screen factors and actual rejection diagonals,
then check stochasticity, detailed balance, strong lumpability, and the
same three-block G and L formulas used by the analytic proof. At horizons
2,4,8,16 verify native-law/quotient-law and TV equality and both finite
sandwiches. Explicitly check that leaf-block retention is larger than an
individual leaf's holding probability, and that the claimed escape formula
uses the entire block. Compare pure G with its finite sandwich.

All arithmetic is exact rational; the input KL bound is the same
5/2+17/47<3 after summing the leaves. These are eight hybrid and four
ordinary finite checks, not asymptotic-rate data. Record code/proof/contract
identities before running. No old suite, other-owner work, large graph or
numerical search is authorized by this added check. Stop after these checks
unless an actual discrepancy requires correction.
