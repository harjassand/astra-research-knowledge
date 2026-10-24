# A positive Gibbs-dual route to the antisymmetric entropy frontier

24 October 2026, root construction. The central inequality below is UNPROVED.

Let W3(A)=(Tr(A)I−A^T)/2. The uniform antisymmetric-qutrit squashing bound is equivalent, by the Weyl-flag argument in su3_phase_cycle_and_entropy_target.md, to

 2 S((W3 tensor id)rho) >= S(rho)+S(rho_R)+ln3

for arbitrary finite references and input states. This is NOT the stronger arbitrary-marginal mutual-information half-contraction statement.

A sufficient explicit noncommutative Maclaurin inequality is, for every positive X on C3 tensor R,

 Tr exp[I3 tensor (Tr_A log X−log X_R)−(log X)^(T_A)] <= Tr(X)/3.  (G)

Sufficiency needs no minimax interchange. Set X=(W3 tensor id)rho, so X_R=rho_R, and G=2(W3* tensor id)(log X)−I tensor log X_R. The Gibbs variational inequality gives

 S(rho)−2S(X)+S(X_R) <= log Tr exp(G).

For normalized X, (G) bounds the right side by −ln3. Faithful approximation handles boundary states if the universal inequality is established.

Physical representation: use the antisymmetric Stinespring isometry from C3 into wedge² C3. The matrix G is exactly the restriction to wedge² C3 tensor R of

 K=log X_BR+log X_ER−I_BE tensor log X_R.

K commutes with Swap_BE. Thus (G) is equivalent to Tr[P_- exp(K)]<=Tr X/3. Ordinary three-matrix Golden–Thompson/strong-subadditivity bounds Tr exp(K)<=Tr X, but this alone does not establish the sharper antisymmetric-sector weight.

For product X=A tensor C the proposed inequality reduces to the ordinary elementary-symmetric inequality e2(A)<=[Tr A]^2/3. It also holds blockwise for classical reference X. Neither proves the noncommuting-reference case.

## A tempting shortcut fails exactly

It would suffice to combine the ordinary full-trace bound with Tr[Swap_BE exp K]>=Tr[exp K]/3. This reflection-positivity guess is FALSE.

Take R=C3 and X=exp(−t Swap_BR), t>0. Write s=e^t+2e^(−t), so X_R=s I. In the three-qutrit permutation decomposition, the fully symmetric subspace has dimension10, the fully antisymmetric subspace dimension1, and the mixed representation has multiplicity8. Consequently

 Tr exp K=[10e^(−2t)+e^(2t)+8e^(−t)+8e^t]/s,
 Tr[P_- exp K]=[e^(2t)+8e^(−t)]/s.

The normalized swap expectation tends to −1 as t grows, the opposite of the proposed lower bound. But (G) itself STILL HOLDS: Tr X/3=s and its slack is

 s−Tr[P_- exp K] = 4(1−e^(−t))²/s >=0.

This exact family shows why bounding the antisymmetric fraction and the total mass separately loses the needed compensation. It is a rejected proof mechanism, not a rejection of (G). The asymptotic antisymmetric state also explains why rank-one-only diagnostics miss a load-bearing boundary.

## Executed finite diagnostic and boundary

wh3_explicit_gibbs_candidate.py/json sampled240 positive states across reference dimensions1..4, including Wishart and near-rank-one families. The largest observed normalized ratio was .8187525773561737. This is only arithmetic/candidate exploration, not evidence sufficient to certify (G). Discovery cost is unknown. No hardware, purchases, publication or physical control operation occurred.

Next obligation: prove or produce a finite counterexample to (G), retaining the exact same input/output/reference interface. A failure of this sufficient explicit trial marginal need not disprove the optimized entropy inequality.

## Closest ordinary frameworks checked

Berta, Sutter and Walter, Quantum Brascamp–Lieb Dualities, CMP401 (2023),1807–1830, DOI10.1007/s00220-023-04678-w, explicitly relates quantum relative-entropy and matrix-exponential inequalities, including its Corollary3.10 for strong data processing. The use of Gibbs duality here is ordinary capital, not a new general duality theorem. Its stated fixed-reference theorem does not by itself prove the conditional antisymmetric bound above.

Carlen, Lieb and Reuvers, Entropy and entanglement bounds for reduced density matrices of fermionic states, arXiv:1403.3816v3, is a relevant primary fermionic entropy antecedent. The abstract and source were retrieved; no claim that its results establish this arbitrary-reference inequality has been made.

A focused isospectral boundary perturbation diagnostic is saved in wh3_rotated_antisymmetric_diagnostic.py/json. It tests450 rotations of faithful approximations to the tight antisymmetric projector and found no violation; the largest ratio .9999999866682111 was the UNROTATED epsilon1e−8 input. Execution .08646s, peakRSS49196KiB. This does not establish local or global extremality. A separate75-case diagonal-reference-filter calculation also found no violation (largest .9999986682067068 at the unfiltered epsilon1e−6 input); this was an exploratory inline calculation, not a certified source-complete experiment.

## Correction, 16:50 UTC

The exponential inequality is not merely a potentially stronger sufficient condition. reference_adapted_gibbs_duality.md proves its EXACT equivalence to the entropy target by Gibbs variational duality and relative-entropy data processing, with explicit witness transfer in both directions and a monotone search update. The earlier weaker wording above is preserved as construction history. Independent verification confirmed the identity and stationary-point equation. Global maximality remains unproved.

## Source-resolved significance, 17:09 UTC

Reading the governing primary text, not only its abstract, identifies the exact historical target: Carlen–Lieb–Reuvers arXiv:1403.3816v3, Section4, Theorem4.4 gives the Christandl–Schuch–Winter upper bound for Slater two-particle states. Conjecture4.5 asserts equality and minimality. For N=3 its value is (1/2)ln3, exactly the antisymmetric-qutrit squashing target here. The present restricted proofs and equivalent Gibbs representation do NOT resolve that conjecture. Its explicit primary provenance is https://arxiv.org/html/1403.3816v3#S4 .

This connects the current construction to unavoidable correlations from fermionic statistics, rather than treating it as an arbitrary optimization benchmark. It does not establish an engineering advantage, a device, or historical originality for Gibbs duality.
