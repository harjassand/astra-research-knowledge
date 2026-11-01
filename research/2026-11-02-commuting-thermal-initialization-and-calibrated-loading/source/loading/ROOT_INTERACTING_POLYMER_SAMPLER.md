# Root conditional sampler for the calibrated-noise preimage

1 November2026. Supporting construction under explicit potential bounds. Not yet an actual noisy-loader theorem or a novelty claim.

## Positive target and assumptions
Let Gamma be compatible configurations of decoder-trace polymers on a finite host. For each polymer gamma let m_gamma be its marked-object size and S_gamma its nonzero TOP syndrome sites, with |S_gamma|<=m_gamma. Distinct compatible polymers have disjoint top support. Let w_gamma>0 be its original thermal activity. A positive pre-distorted target has form
 pi(Gamma) proportional to product_gamma w_gamma times exp[Phi(sigma_Gamma)].
Assume Phi(sigma)=sum_C phi_C(sigma restricted to S_C) and define M_C=sup_sigma |phi_C(sigma)|. Require the anchored moment bound
 sup_j sum_{C:j in S_C} |S_C| M_C <= epsilon_Phi.
This is an assumption to be EARNED from the signed error-cluster expansion, not a consequence of mere positivity of pi. Infinite cluster sums must converge absolutely and have a constructive truncation bound.

Set a_gamma=w_gamma exp(2 epsilon_Phi m_gamma). Assume
 sum_{eta incompatible gamma} m_eta a_eta <= theta_h m_gamma,
 B:=sup_j sum_{eta:j in S_eta} m_eta a_eta < infinity,
 theta_h+4B epsilon_Phi <1.
Low thermal activity is expected to give these rooted sums, but actual constants must be charged.

## State-dependent birth/death chain
Remove each present polymer at rate1. Insert each absent compatible gamma at rate
 b_gamma(Gamma)=w_gamma exp[Phi(sigma_Gamma+sigma_gamma)-Phi(sigma_Gamma)].
Detailed balance is exact for pi. Every potential changed by insertion meets S_gamma, so |Delta_gamma Phi|<=2epsilon_Phi |S_gamma| and b_gamma<=a_gamma. This samples only a positive distribution; no signed samples or global rejection factor exp(cn) are used.

## Explicit path coupling
Consider two legal configurations differing by one polymer gamma0. Couple deaths and common proposed births at dominating rate a_eta, using a shared uniform acceptance variable. Death of gamma0 removes weighted distance m_gamma0 at rate1.

A birth compatible on only one side must conflict with gamma0 and contributes at most sum_incompatible m_eta a_eta <=theta_h m_gamma0.

For eta compatible on BOTH sides, the differing birth rates obey
 |b_eta(Gamma+gamma0)-b_eta(Gamma)|
 <=a_eta |Delta_gamma0 Delta_eta Phi|
 <=4a_eta sum_{C:S_C meets S_eta and S_C meets S_gamma0} M_C.
The mean-value bound uses the common uniform upper bound a_eta for the two exponential rates. Sum the extra weighted disagreement over eta. For fixed C,
 sum_{eta:S_eta meets S_C} m_eta a_eta <=B |S_C|.
Then summing over C touching S_gamma0 gives at most4B epsilon_Phi |S_gamma0| <=4B epsilon_Phi m_gamma0.

Thus weighted distance contracts at rate at least1-theta_h-4B epsilon_Phi>0. The same legal remove-then-insert path metric and finite host diameter as in the noninteracting sampler yield logarithmic continuous-time mixing to fixed error. A dominating finite dictionary clock gives a polynomial implementation.

## Algorithmic obligations and finite errors
A potential tail bound sup_sigma |Phi-Phi_L|<=u implies bounded log density ratios and an O(u) total-variation perturbation after normalization for u small. Likewise an omitted-large-polymer bound can use the Papangelou upper activity a_gamma: the conditional inclusion probability is at most a_gamma, by removal/insertion pairing even with interactions. Thus sum_large a_gamma controls trace truncation.

If error clusters and trace polymers of size O(log(n/epsilon)) are constructively enumerable and locally evaluable, truncate both, allocate numerical/mixing/tail errors, and use the finite dominating chain. Runtime is polynomial in n/epsilon with fixed degree and convergence constants. The required absolute cluster coefficients, constructive truncation and positivity of the actual preimage remain separate proof obligations.

This lemma supplies a positive-sampling mechanism IF the calibrated inverse-noise Gibbs preimage has the stated weak local potential. It says nothing yet about unknown rates, coherent/non-Pauli gate noise, full noisy input encoding, or a noncommuting spin-bath Gibbs target.
