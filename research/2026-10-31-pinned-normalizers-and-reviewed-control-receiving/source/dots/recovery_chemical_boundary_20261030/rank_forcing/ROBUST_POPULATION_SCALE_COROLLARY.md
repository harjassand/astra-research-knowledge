# Consequence for the abstract n-label arrival scale

This is a corollary of the proposed sharp robust exponent, not a chemical-network rate lower bound. Consider n labels under the same finite baseline/excess contract, with no deletion events, and let L be the acquired least-rank maximum. Extras may be correlated across labels but must obey the same support/rank restrictions. Let H_K be the first time at least K labels are simultaneously at a.

The independent potential-clock forcing events give a Binomial(n,p(t)) lower bound on the number of labels at a at time t, with p(t)>=c t^L for t<=1. Therefore, when t=C(K/n)^(1/L)<=1 and C is sufficiently large,

    P(H_K>t) <= P(Binomial(n,p(t))<K) <= exp(-c'K).

The containment is pathwise despite correlated actual label histories. If bounded deletions are restored, their paid count must be subtracted as in the original cohort argument; the displayed unqualified inequality assumes none.

Conversely start every label at a maximal-rank type and apply the sharp-exponent finite-R reset policy separately to each label. Its proof bounds FIRST hitting a as well as endpoint occupancy:

    P(label ever reaches a by t) <= (Qmax t)^L/L! + C(1+t)/R.

Reaching K simultaneous a labels requires at least K distinct labels to have visited a. Markov's inequality therefore gives, without requiring independence,

    P(H_K<=t) <= (n/K)[(Qmax t)^L/L! + C(1+t)/R].

For any sequence with n t_n^L/K_n tending to zero, choose finite reset speeds R_n so n(1+t_n)/(K_n R_n) tends to zero. The target-arrival probability then tends to zero. Thus the power (K/n)^(1/L) is optimal for a guarantee uniform over this abstract unbounded-excess class. The constants and achievable speeds of a FIXED raw network may improve the behavior or prevent this adverse policy; no necessity for chemical stability or optimality of the later Lyapunov decay exponents is inferred.
