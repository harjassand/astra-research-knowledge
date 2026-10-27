# Fresh continuation result

The full all-copy qutrit Werner inequality remains **unresolved**. No admissible negative complex rank-two endpoint witness was constructed. The frozen first-stage Cauchy growth invariant has not acquired the subexponential upper bound it needs.

The strongest new object is the Cartan-power completion in CARTAN.md. For H=(C^3)^{tensor n}, let C_k(H) be the span of kth tensor powers of decomposable bivectors. The explicit compressed-operator minimum alpha_(n,k) retains every rank-two projection and satisfies

\[
0\le g_n/4-\alpha_{n,k}
\le16\,3^n(3/2)^n/k.
\]

This follows from a primary coherent-state approximation theorem with its norm convention checked, not from an assumed Werner positivity statement. With k(n)=ceil(16*9^n), the error is at most 2^{-n}. The prior N525 projection-completeness and persistent-gap theorem therefore identifies the same full scientific target with alpha_(n,k(n)) tending to zero. That convergence is **not proved**. The explicit representation dimension remains doubly exponential in n; no efficient algorithm or practical advantage is claimed.

The decisive result is a rigorous **obstruction to every finite Cartan degree**. On three binary physical sites, rank-two projections onto span(u,Theta u), where Theta is the odd-qubit spin flip, have q=0. Their quaternionic planes are Zariski dense in the complex Grassmannian, by an explicit graph-chart polynomial argument. Their coherent powers span every finite Cartan representation. Consequently no nonzero PSD compressed operator can have the required coherent symbol: it would annihilate a spanning family of zero vectors but must have a positive expectation on the plane span(000,011). Thus alpha_(n,k)<0 for every finite k>=2 and every qutrit n>=3, by binary embedding and pure-site padding. These are negative **relaxed states**, not distillation witnesses. The degree-two control is explicit and rational: -3/8, with exact Cartan membership verified.

A second complete auxiliary construction, in PROOF.md, fixes all whole-replica permutation moments of a flat rank-two projection and uses finite de Finetti plus a proved spectral-rigidity lemma to obtain convergence. Its strongest opposition is an exact PSD four-replica state with all 24 permutation moments correct and objective -13/32. It is binary-supported, where q is always nonnegative. Therefore whole-permutation corrections alone cannot make that finite replica operator positive at any n>=3. This extends beyond the prior N525 two-replica shadow-LP diagnostic; it does not claim that diagnostic as new work.

All displayed finite identities are checked by verify.py and saved in verification.json, including physical Gram metrics, invariant subspaces, all S4 characters, projection normalization, -13/32, and -3/8. Checks also pass under python -O. Numerical probes were only discovery aids; the retained statements have exact algebraic proofs. No exhaustive priority clearance, proof-assistant certification, or external review is claimed.

The hardest remaining obligation is precise: obtain alpha_(n,k(n)) >= -o(1) on an unbounded sequence of copy counts, using valid physical/representation structure. The finite-degree obstruction shows that replacing this with finite-degree nonnegativity would be false. The all-copy mission is not completed by this checkpoint.
