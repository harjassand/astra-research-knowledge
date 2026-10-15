# Preserved audit-harness corrections

The source packet was unchanged throughout. The copied source algebra program passed its 17 checks on every attempted run. Three early failures occurred only in newly written independent check expressions:

1. `trace(M).subs(delta**2,critical)` did not normalize rational expressions in delta before substitution. SymPy could not infer negativity of the unnormalized expression. The failed receipt and stderr are preserved with suffix `.attempt1`.
2. Factoring first still left denominator factors `(delta-1)(delta+1)` unaffected by substituting `delta**2`. The sign assertion remained inconclusive. The failed receipt and stderr are preserved with suffix `.attempt2`.
3. The periodic example used structural matrix equality before rational simplification. Algebraically equal entries had different expression trees. The failed receipt and stderr are preserved with suffix `.attempt3`.

The final checker verifies the trace identity first and then substitutes into its explicit rational formula. It compares periodic matrices by factoring each difference. No theorem statement or numerical source input changed. Final runs pass 17 copied-source and 13 independent exact checks. The 70-digit deadline evaluations are explicitly numerical illustrations. All runs had a hard 45-second limit, and no stochastic or FSP program was executed.
