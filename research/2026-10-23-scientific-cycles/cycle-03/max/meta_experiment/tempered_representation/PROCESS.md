# Process record

## Bounded protocol

The first clock read was **2026-10-21 17:16:21 UTC**. The hard twelve-minute deadline was **17:28:21 UTC**. Only the five authorized input files were read. No web, sibling outputs, unrelated filesystem material, agents, collaboration, or withheld solution was used. Output files are confined to the assigned directory.

## Representation search, completed within the first quarter of the budget

Two mathematically different representations were considered before committing to the proof.

1. **A normalized reference law proportional to \(q^\eta\).** Writing \(r(x)=q(x)^\eta/Z\) makes the local transition an ordinary full delayed-acceptance screen against \(r\). This exactly preserves the local kernel and its target reversibility. It does not replace the global proposal \(q\) by \(r\), and it does not preserve a uniform entropy or initial-density certificate. The boundary example \(q=(1/2,1/(2m),\ldots,1/(2m))\), \(\pi=q\), has \(D(\pi\|q)=0\) but \(q(1)/r(1)\) and \(D(q\|r)\) diverge for every fixed \(\eta<1\). In fact \(D(q\|r)=(1-\eta)\log m/2+O(1)\). Thus this representation did not give a valid direct application of the accepted theorem. Its failure was not treated as a lower theorem.

2. **A diagonal similarity transform of accepted local paths, with a rank-one bound for global resets.** With \(D=\operatorname{diag}(q^\eta)\), the positive envelope is \(M=D^{-1}QD\), and exactly \(M^k=D^{-1}Q^kD\). This preserves endpoint screen factors and the double-stochasticity of the underlying proposal powers. It loses exact rejection probabilities by overcounting them, which is harmless for an upper bound. Hölder gives \(qM^k(A)\le q(A)^\eta\) for every path length. The global term is handled through \(\mu J=q\), not by an uncontrolled matrix norm. This proves a setwise bound with a fixed exponent \(\eta\), rather than a time-degrading exponent.

The second representation was selected. Its similarity identity and Hölder bound were established by the 17:18:59 clock check, within the required first three minutes.

## Completion strategy

The fixed-exponent bound was combined with a first-entrance decomposition. A layer-cake/Jensen argument proved that a setwise bound relative to the stationary law is preserved under every subsequent invariant transition. This controls all returns after entrance.

A separate threshold argument converts the setwise initial-law bound into control of the middle-weight part of a smoothed indicator. Only the inherited spectral-anchor estimate is needed; the more delicate signed-tail maximum estimate from the accepted theorem is unnecessary once the low-weight mass is small. Taking an analysis split of order \(\sqrt{\log n}\), with cutoffs \(n\exp[-O(\sqrt{\log n})]\), leaves the leading entropy term equal to \(K/\log n\).

The matching identity-proposal lower bound and deterministic-time inversion were checked explicitly. A positive three-state counterfamily at \(\eta=0\) was also constructed, confirming that the proof's deterioration at zero corresponds to an actual endpoint obstruction.

## Concrete adversarial checks

The load-bearing claim is the fixed-exponent bound, not numerical convergence. It was checked analytically for arbitrary path length via exact similarity and both row and column sums. The rare-state swap family in the supplied starting lemmas has one-step mass of order \(q(A)^\eta\), so the exponent in this bound cannot simply be improved to one.

A separate numerical calculation tested 168 finite instances: dimensions 2, 3, and 6; exponents 0.001, 0.01, 0.1, 0.49, 0.5, 0.9, and 0.999; eight random symmetric stochastic proposals per pair; and probability scales spanning approximately 80 log units. It enumerated every nonempty subset at times zero through eight, for **36,792 subset/time checks**. It tested both \(qM^k(A)\le q(A)^\eta\) and \(qC^k(A)\le A_kq(A)^\eta\), as well as stationarity and the similarity identity.

The largest ratios were 1.0000000000000004 and 1.0000000000000002, respectively; the largest stationarity residual was 2.22e-16 and the largest relative similarity residual was 1.50e-15. These are floating-point consistency checks, not substitutes for the uniform proof. The numerical calculation did not impose the KL constraint because the matrix inequalities being tested do not require it.

After the complete proof was written, an additional adversarial check isolated preservation of nonlinear set bounds under invariant evolution. It used 100 seven-state reversible kernels, exponents from 0.001 to 0.99, and initial measures concentrated by increments of the concave cumulative function x^eta. Every nonempty subset was checked before and after seven transitions: **12,700 subset checks**. The largest initial and transported capacity ratios were 1.0000000000000002 and 1.0000000000000007. The analytical justification remains the layer-cake/Jensen proof, which covers every invariant kernel and every admissible submeasure.

No parameter optimization, simulated long trajectories, or empirical speed comparison was used. No unresolved mathematical gap remains in the stated obligation. Token costs are unknown; wall-clock and code measurements are reported separately in `COSTS.json`.
