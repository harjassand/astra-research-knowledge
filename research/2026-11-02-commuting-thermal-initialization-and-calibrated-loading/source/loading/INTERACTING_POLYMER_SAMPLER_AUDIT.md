# Independent receipt: interacting positive polymer sampler

2026-11-01. **PASS-CONDITIONAL of the sampler lemma.** The displayed mixed-rate and path-coupling calculations are correct under their explicit anchored-potential and activity assumptions. No assertion is made here that the actual inverse-noise preimage satisfies those assumptions. This is not a generic-noise loader, noncommuting Gibbs sampler or novelty claim.

## 1. Rates, detailed balance and upper envelope

For legal insertion of gamma, the ratio of target weights is exactly w_gamma exp(Delta_gamma Phi), so unit death rates and the stated birth rate satisfy detailed balance. A changed potential term must meet S_gamma. The anchored moment hypothesis implies the weaker sum_{C containing j} M_C<=epsilon_Phi because nonempty |S_C|>=1. Hence |Delta_gamma Phi|<=2epsilon_Phi |S_gamma|<=2epsilon_Phi m_gamma and b_gamma<=a_gamma.

All weights and rates used by this chain are nonnegative. Signed coefficients in an antecedent derivation of Phi do not become signed sampling weights. Absolute convergence and positive preimage are nevertheless necessary independent premises.

## 2. Mixed birth-rate calculation

Let the adjacent states be A and A+gamma0 and let eta be absent and insertable in both. Compatibility supplies disjoint top supports, and all four configurations needed for the mixed difference are legal. The mean value theorem gives

    |b_eta(A+gamma0)-b_eta(A)|
       <= max(b_eta(A+gamma0),b_eta(A))
          |Delta_gamma0 Delta_eta Phi|
       <= a_eta |Delta_gamma0 Delta_eta Phi|.

Each potential term cancels from the mixed difference unless its support meets BOTH S_eta and S_gamma0. Its four remaining evaluations have magnitude at most 4M_C. No differentiability of Phi as a function of the discrete syndrome is used.

Summing by C and then by a top site in S_gamma0 yields

    sum_eta m_eta |difference in birth rates|
      <=4B sum_{C:S_C meets S_gamma0} |S_C| M_C
      <=4B epsilon_Phi |S_gamma0|
      <=4B epsilon_Phi m_gamma0.

The overcounting only enlarges the bound. There is no omitted dependence on the number of top sites or the total bath/host volume in this step.

## 3. Hard-core conflicts and weighted metric

On legal configurations define d(A,B)=sum_{gamma in A symmetric-difference B} m_gamma. This is precisely the shortest path metric with one-polymer insertions/removals: remove A\B and insert B\A, keeping the common compatible subset throughout. Every path must pay for all exclusive polymers, so the path has minimum weight.

For the adjacent pair, synchronized deaths of common polymers leave d unchanged. Death of gamma0 reduces d by m_gamma0 at rate one. Any birth permitted on exactly one side, apart from the possible coalescing insertion of gamma0 itself, conflicts with gamma0. Its contribution is at most sum_{eta incompatible gamma0} m_eta a_eta. Coalescing insertion of gamma0 is helpful and may safely be discarded from an upper bound. Births permitted on both sides have disagreement rate equal to the absolute rate difference under shared uniform thinning.

Thus infinitesimal expected distance drift is at most

    -(1-theta_h-4B epsilon_Phi) m_gamma0.

Finite-state continuous-time path coupling therefore gives contraction rate kappa=1-theta_h-4B epsilon_Phi>0. This does not require a coupling restricted to adjacent configurations at later times; path-metric extension supplies the usual all-pairs contraction.

If m_gamma>=1 and D bounds the weighted diameter, the resulting total-variation mixing bound is at most D exp(-kappa t). A time kappa^(-1) log(D/delta) suffices. “Logarithmic mixing” therefore means logarithmic in weighted diameter and inverse requested error, with kappa uniformly bounded away from zero.

## 4. Truncation checks

Uniform potential error sup|Phi-Phi_L|<=u gives normalized density ratio between exp(-2u) and exp(2u), and hence O(u) total-variation error for small u. Restricting the potential sum preserves the absolute anchored moment bound.

For a polymer gamma, deletion/insertion pairing gives

    pi(gamma present)
      =sum_{A admitting gamma} pi(A) b_gamma(A)
      <=a_gamma.

Therefore pi(any omitted polymer present)<=sum_omitted a_gamma. The exact law conditioned on none being omitted is the corresponding truncated-dictionary interacting polymer law. Its total-variation distance to the original law is precisely the omitted-event probability. Interactions do not invalidate this truncation argument. Removing polymers also preserves all stated upper activity sums.

These bounds require a supplied constructive tail estimate, not merely convergence without a computable rate.

## 5. Precise finite-algorithm assumptions

The claimed polynomial implementation is valid IF the obligations are quantitative:

1. The size-O(log(n/delta)) truncated trace-polymer and potential-cluster dictionaries, with required coefficients and compatibility information, can be enumerated/evaluated in polynomial time in n/delta.
2. Weighted diameter D is polynomially bounded (as intended for a finite trace host with disjoint marked objects), and kappa has a size-independent positive lower bound.
3. The finite dominating event rate R=sum_gamma a_gamma+N_dict is polynomially bounded. With standard self-incompatibility, the hard-core inequality implies a_gamma<=theta_h, so R<= (1+theta_h)N_dict. If incompatibility is defined only between DISTINCT polymers, this implication is unavailable and a polynomial total-rate bound must instead be included explicitly.
4. Rates, logarithmic weights and acceptance probabilities can be approximated to the required polynomial-bit precision in polynomial time. Real-valued positive activities alone are not a computational oracle.

A clock at total rate R proposes births with rate a_gamma and death attempts with rate one per dictionary entry, using null events when disallowed/absent. Its expected number of events over the mixing time is R t. A high-probability Poisson event cutoff and per-event acceptance approximation budget give finite runtime and controlled additional variation error. No exponential-in-volume global rejection probability appears.

“Constructively enumerable and locally evaluable” should be understood as these quantitative conditions, rather than mere eventual computability. The root already labels these as algorithmic obligations; they are not consequences of the anchored moment inequality alone.

## Scope and decision

The conditional positive sampler works. The unproved application gate remains the actual calibrated inverse-noise cluster representation, positivity of its preimage, and uniform constructive bounds yielding epsilon_Phi, a_gamma, B and tails within the contraction regime. This receipt does not certify those premises, supplied-input encoding, generic coherent noise, unknown calibration or an interacting spin-bath target. No no-go or novelty inference follows.
