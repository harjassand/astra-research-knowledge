# Root elementary support bound for commuting Gibbs syndromes

2026-11-02. Independently checked by the explicit-family constructor. This is an elementary coding/Fourier lemma, not a historical novelty claim and not a proof of the ell=8 decoder.

Let C be any binary linear subspace of F_2^M. Give s in C probability proportional to product_i q_i^(s_i), with 0<=q_i<=1. Then for EVERY coordinate set T, whether or not its indicator is a valid syndrome,

 Pr[T subset supp(s)] <= product_(i in T) q_i.

## Proof
If the fiber s_T=1 is empty the result is immediate. Otherwise restrict the zero fiber s_T=0 to the complementary coordinates to obtain a linear code C0. The one fiber's complementary coordinates form a coset v+C0. Its unnormalized weight is q_T Z_(v+C0)(q_rest), while the full denominator is at least Z_C0(q_rest).

The product weight f(x)=product_j q_j^(x_j) has nonnegative Walsh transform:

 fhat(u)=product_j[1+(-1)^(u_j)q_j]>=0.

The character formula gives

 Z_(v+C0)=|C0|/2^m sum_(u in C0perp) (-1)^(u dot v) fhat(u)
 <=|C0|/2^m sum_(u in C0perp) fhat(u)=Z_C0.

Combining the two statements proves the claim, including q_i=0 or1 by continuity/direct evaluation.

## Actual application and exact limit
For a commuting Pauli stabilizer Hamiltonian sum_i J_i(I-S_i)/2 with J_i>=0, the allowed syndrome strings form a linear subspace, and every allowed sector has the same dimension. Consequently its Gibbs syndrome law satisfies the lemma with q_i=exp(-beta J_i). Redundant checks cause no exception. This is an odds-parameter bound, not stochastic domination by the independent Bernoulli law of probability q_i/(1+q_i).

Thus a commuting-model Peierls argument can bound ANY fixed occupied witness T by exp(-beta sum_T J_i), without first proving T itself is a removable valid syndrome. Bounded witness enumeration and a sufficiently large occupied-witness implication remain necessary. In particular the ell=8 construction still needs the actual coarse map, correction identity, contraction/local computability and protected decoder. This lemma does not manufacture those properties.

It changes the interpretation of the central-cube singleton test: that test refutes naive component REMOVABILITY, but it does not obstruct this alternative commuting Gibbs probability bound. For generic weak perturbations or the native clock effective free energy, weights are not a pure product on C; nonnegative Walsh positivity is not automatically available. The previously reviewed removable-witness route for those models remains intact and separate.
