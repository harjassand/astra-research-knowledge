# Why the new occupation mechanism is not a rephrased strict-power bound
Status: elementary personal observations, separate from the four frozen proof files.

## Uniform strict-power clearing is impossible on the new active family
Take an active initial state A=1 and put N-1 copies into one reservoir species X_i. Its A+(m-1)X_i source is enabled for large N. Every source has A multiplicity at least1. At A=1, only A-multiplicity1 sources can fire, and their total rate is at most C N^(m-1). Clearing is disabled since m>=2. Therefore the expected waiting time to the FIRST fast event is at least cN^{-(m-1)}. Clearing cannot occur earlier. It follows that

    E tau_clear >=cN^{-(m-1)}

at these active starts. The same lower bound holds for time to the first clearing/competing connector event at fixed B=q, because competitor rates at A=1 are bounded and the total event intensity remains at most CN^(m-1).

Consequently NO uniform estimate E tau_clear<=C N^{-(m-1+epsilon)} with epsilon>0 can hold for this family. This is an analytic obstruction, not a failure to optimize the previous proof. The relative ratio T/U can still tend to zero by a power, as the new local occupation lemma derives.

## Small concrete non-complex-balanced member
Take two composition species A,C, m=3, q=4, and fast edges (all carry 4B):

    A+2C <-> 2A+C <-> 3A,

with forward/backward coefficients (2,1) on the first pair and (1,3) on the second. Add0->A+B->3A+4B->0 with arbitrary positive coefficients.

All fast complexes contain A, and the source A+2C has an A-producing edge, so the new source contract is satisfied. The state A=0 is a genuine fast siphon, including arbitrarily large C. Physical immigration seeds it.

There are five distinct complexes in the full network, one linkage class, and stoichiometric rank3: use fast vector (1,-1,0), immigration vector (1,0,1), and activation vector (2,0,3), which are linearly independent. Thus deficiency=5-1-3=1, not0.

A positive complex-balanced equilibrium would force zero flux on the first fast edge, since A+2C is an endpoint with only that pair. It then forces zero flux on the next edge at the middle fast complex. Hence it would require simultaneously A/C=2 and A/C=1/3, an impossibility. The shared B^4 factor cancels. The connector meets the fast graph only at3A+4B and cannot repair these endpoint/interior balance equations. Thus this concrete member is not complex balanced for any choice of positive connector coefficients.

This is not a novelty claim or an assertion that all conventional recurrence results fail. It merely proves the new contract has non-product-form members and an actual obstruction to the old uniform strict-power clearing premise.
