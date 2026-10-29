# Near-pure source mass in computationally accessible Schur sectors

28 October2026. Root derivation candidate, independent review pending. This supplies a source-weight condition for the separately constructed low-defect decoder. It does not implement that decoder or claim finite noisy hardware performance.

Let rho be any finite-dimensional density operator with largest eigenvalue at least1-delta,0<=delta<=1. In k independent copies, measure the Schur-Weyl partition nu of the permutation action. For integer0<=j<=k, define the defect as k-nu_1. Then

 Pr[k-nu_1>j] <= Pr[Binomial(k,delta)>j].

No knowledge of the dominant eigenvector is required to execute the Schur label measurement. The eigenvalue premise is supplied here, not acquired by this lemma. A bound on rank alone does not imply it.

Proof. Write rho=(1-e)|0><0|+e sigma with sigma supported orthogonally to|0>, where e<=delta. This is a mathematical spectral decomposition, not an operation the protocol performs. Expand rho^tensor k as a convex sum over the positions occupied by sigma, with count t distributed as Binomial(k,e). Each vector in a term with t such positions is fixed by permutations of the k-t positions carrying|0>. Its span lies in the subrepresentations with a nonzero invariant vector for that subgroup S_(k-t). By the ordinary symmetric-group branching rule, V_nu has such an invariant exactly when one can remove t boxes leaving the single row(k-t), equivalently nu_1>=k-t. This remains true for arbitrary vectors/mixtures on the t remaining positions. If t<=j, there is no support in defect>j. The other terms contribute at most their entire mass. Binomial stochastic monotonicity then replaces e by delta. This proves the bound without an environmental dimension factor.

For an iid bipartite source rho_AB, any purification has environment marginal with the same nonzero spectrum. Thus the sum of discarded environmental Schur-sector weights in a universal distillation decomposition obeys this inequality if lambda_max(rho_AB)>=1-delta. Averaging over measured Alice/Bob labels preserves the total bad mass. It does NOT bound each individual conditional branch's bad mass.

A useful regime is delta=c/k. Fixed j can make the Poisson-like tail small while allowing a decoder whose complexity is polynomial in k at fixed defect. In contrast, simply replacing the entire source by its dominant pure state incurs k-copy trace distance exactly1-(1-delta)^k for the diagonal two-component example, approaching1-exp(-c). Active low-defect correction could therefore remove a real error term that a pure-state approximation does not control. The resulting overall operation still depends on the actual code-packing, control and source assumptions; no throughput follows from the tail lemma alone.

Fixed positive delta requires defect growing proportionally to k to keep this bound useful. A k^O(j) decoder is not thereby efficient in that regime. Nor does the bound survive arbitrary correlated copies merely because their one-copy marginals have large eigenvalues. For correlated sources, an actual bound on weight outside the low-defect subspace is a different supplied/acquired premise.

## Acquiring a sufficient premise without eigenvector tomography

For delta<1/2, a purity lower bound

 Tr(rho^2) >= (1-delta)^2+delta^2

implies lambda_max(rho)>=1-delta. To prove this, let r=lambda_max. Always purity<=r because sum eigenvalues=1. When purity>1/2, therefore r>1/2. Also purity<=r^2+(1-r)^2 by concentrating all remaining mass into one eigenvalue. The right side is increasing for r>=1/2, yielding the implication (with endpoint equality handled directly).

A trusted SWAP measurement on TWO independently generated copies returns an antisymmetric outcome with probability q=(1-Tr(rho^2))/2. Thus an upper confidence bound q<=delta(1-delta) suffices. For a distributed rho_AB, the global swap equals SWAP_A tensor SWAP_B. Each laboratory measures its own two-copy swap observable and communicates its sign; their product gives the required outcome. This uses two retained source copies, local joint operations and a classical link, not environment access or a known eigenbasis. The swap identity is a standard operation, not a new measurement proposal.

A concrete finite certificate: fix k,j,delta,beta and a test count n before sampling. Accept only zero antisymmetric outcomes. If

 (1-delta(1-delta))^n <= beta,

the probability of accepting an actual q>delta(1-delta) is at most beta. More powerful binomial acceptance regions are available but unnecessary to show finite acquisition. This is a frequentist false-acceptance statement, not a conditional posterior probability; it can have small acceptance probability for nonzero impurity. Test copies are consumed, and source stationarity/independence between this test and subsequent distillation remain assumptions. Calibrated swap-test bias must be subtracted from the margin; generic unknown control noise is not covered. The number of consumed source copies is2n, and the local gates/storage/readout are additional costs.

The qubit-product counterexample |0><0| tensor |1><1| has pure individual marginals but antisymmetric Schur weight1/2. Hence one-copy eigenvalues alone cannot substitute for the iid common-state premise. A different retained-memory theorem would need an actual common-direction excitation/low-defect bound rather than this binomial law.
