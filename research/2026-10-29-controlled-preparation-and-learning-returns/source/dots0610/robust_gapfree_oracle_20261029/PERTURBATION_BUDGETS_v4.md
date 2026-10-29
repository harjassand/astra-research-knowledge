# Concrete sufficient approximate-symmetry budgets
2026-10-29. Companion to ROBUST_ORACLE_v4.md; author derivation, review pending. These are conditional source-interface examples, not a general physical noise model inferred from probe data.

## State-independent contamination of a collective process
At each actual history let the complete joint CPTP source map be
 N_t=(1−lambda_t)N_t^0+lambda_t B_t,
where every Kraus operator of N_t^0 commutes with the SAME fixed hidden star swaps, B_t is an arbitrary joint CPTP map, and0<=lambda_t<=1 is fixed before the current private controls. B_t can be nonunital and may retain/update source memory. Linearity of the loss in the channel and0<=E_i<=2I give
 E_{i,t}(C_i*)<=2lambda_t I_M.
Thus Gamma_T<=2(n−1) E sum_t lambda_t, with no reset assumption. A pathwise upper bound on the cumulative lambda budget also suffices. This includes arbitrary small-fraction contamination rather than a reconstructed complete environment.

## Coherent joint perturbations, quadratic budget
Suppose a joint unitary U_t differs in operator norm by at most nu_t from a joint unitary U_t^0 commuting with the same fixed hidden star swaps. Then
 ||[U_t,S_i* tensor I]||op<=2nu_t,
 E_{i,t}(C_i*)<=2nu_t² I_M,
 Gamma_T<=2(n−1) E sum_t nu_t².
For U_t=exp(−i epsilon_t H_t)U_t^0 with Hermitian H_t, one may take nu_t<=min(2,|epsilon_t| ||H_t||op). This is a quadratic coherent perturbation bound at the complete joint operation interface; it does not assume the reduced channel is unitary or the source memory initially independent of the outer payload. A deterministic hidden environment can retain all previous information.

For a common finite Kraus/Stinespring representation, a similar sufficient condition follows by bounding the squared weighted commutator vector directly. No general conversion from a reduced-channel norm to a complete joint memory norm is presumed here.

## Fixed-n tolerance interpretation
For the finite operation use the threshold Gamma_max in equation(3) of ROBUST_ORACLE_v4.md. Either
 E average lambda_t <=Gamma_max/[2(n−1)T],
or
 E average nu_t² <=Gamma_max/[2(n−1)T]
is sufficient under the corresponding decomposition. These are conservative sufficient conditions, not estimated quantities or necessity statements.

With an available code and b≈nu_budget B,T=cB, the asymptotic Markov failure term for constant contamination lambda is at most2a(D/d)c(n−1)lambda/nu_budget, plus vanishing learner terms. Constant coherent perturbation amplitude uses lambda replaced by nu². Small constant contamination can therefore retain a nonzero readiness bound at fixed n, whereas readiness tending to one requires a vanishing defect budget in this proof. An arbitrary-length fixed-n coding family is not supplied by this calculation.

## Statistical caution
The comparator remains fixed independently of the observed dataset. Small selected empirical loss does not by itself certify Gamma_T for a retrospectively chosen frame. The protocol's matching guard certifies its accepted operation; the approximate-symmetry budget is a sufficient readiness hypothesis. Future noise and counterfactual controller histories are outside the statement.
