# Fresh exact-math audit: average-output thermal basin

2026-11-02. **PASS** for the conditional channel/hold interface and ideal Petz benchmark. Neither establishes a physical writer.

## Reference-safe hold bound

Let C_j=i[H,Q_j]. It is Hermitian; C_j(I-P)=0 therefore implies C_j=P C_j P. For any joint written state sigma_LGR and any Hermitian reference contraction M,

`-c_j P tensor I_R <= C_j tensor M <= c_j P tensor I_R`.

Consequently `|Tr[(C_j tensor M)sigma]|<=c_j Tr(P sigma_LG)`. The coefficient `Tr_LG[(C_j tensor I_R)sigma]` is Hermitian by partial-trace cyclicity on LG, so trace-norm duality yields the claimed coefficient bound. No reference factorization is needed.

For every input density matrix xi_A, xi_A<=I_A, so positivity of W gives `W(xi_A)<=2W(I/2)<=2kappa rho`. Stationarity preserves this operator domination under the actual hold evolution. Hence the instantaneous bad weight is at most2kappa p. In the decoded Pauli expansion, the identity/reference coefficient is conserved and each nonidentity coefficient has trace prefactor Q_j/2 of norm1. Integrating therefore proves

`||storage_T-id||_diamond <=min(2,epsilon_write+2kappa p T sum_j c_j)`.

The factor12 when all c_j<=2v_dyn n is correct. This stronger linear-p bound uses a genuinely stronger write-state domination assumption than the stationary-overwrite theorem; it does not follow from small write error alone.

## Petz channel and Stinespring constants

The proposed Kraus operators `K_g=sqrt(rho)(r^-1/2 tensor |g>)` give complete positivity and `sum_g K_g^dagger K_g=I`, hence trace preservation. Direct substitution gives W_rho(r)=rho. Operator monotonicity under congruence proves

`W_rho(I/2)<=rho/[2 lambda_min(r)]`.

For delta=||rho-I/2 tensor tau||_1<1, partial trace gives ||r-I/2||_1<=delta. Since r is a QUBIT state, its deviation eigenvalues are +/-u/2 with u<=delta; therefore lambda_min(r)>=(1-delta)/2. This qubit fact is necessary for the displayed constant.

Use the same environment label g for the ideal product-write Kraus operators `K0_g=I tensor sqrt(tau)|g>`. Splitting their stacked-isometry difference gives

`||V-V0|| <= ||r^-1/2|| ||sqrt(rho)-sqrt(rho0)||_2 + ||r^-1/2/sqrt(2)-I||`.

The first term is at most sqrt(2delta/(1-delta)) by the square-root trace inequality. The second is at most (1-delta)^(-1/2)-1: among the qubit eigenvalues the small-eigenvalue deviation is the larger one. The common-environment channel inequality `||W-W0||_diamond<=2||V-V0||` proves the stated conservative bound. Partial trace only improves it, so it bounds the decoded write error as required. This remains an ideal global channel, with no implementation theorem implicit in the Kraus formula.

## Explicit local-stochastic counterexample to automatic domination

Take n independent thermal gauge bits with rho_G=[diag(1-p,p)]^tensor n, 0<p<1/2, and an otherwise idle maximally mixed logical qubit. Apply independent bit flips of probability epsilon>0 to the gauge bits. This is ordinary local stochastic noise. Their excitation probability becomes

`p'=p+epsilon(1-2p)>p`.

The all-excited diagonal matrix element forces every bound `N(rho)<=kappa_N rho` to satisfy

`kappa_N >= (p'/p)^n`.

Thus kappa_N is exponentially large in volume even for small fixed local noise, and the logical channel can remain EXACTLY the identity in this example. This separates logical accuracy from average-output thermal domination. Exact Gibbs-preserving channels do have kappa_N=1, but preservation alone supplies no logical fidelity.

## Scope

The note correctly identifies an explicit strong service contract, not a consequence of generic local stochastic faults, small energy error, or accurate decoding. A physical writer still must earn both logical fidelity and operator domination while charging thermal resources, controller coherence, switching/reset operations, environment access, and imperfections. Strong low-temperature logical polarization can worsen both Petz kappa and the stated fidelity estimate. No novelty, physical WRITE, or all-temperature guarantee is certified.
