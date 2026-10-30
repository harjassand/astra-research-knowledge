# Receiving one-component backward certificates in a collectively disturbed population
30 October 2026. Root generalization of the product-forcing construction. Local mathematical candidate; no global network claim or historical novelty assertion.

## Actual generator allocation is part of the certificate
Let n persistent coordinates x_i carry target sets A_i. The actual conditional generator has a positive, NO-DOUBLE-COUNTED allocation into coordinate subgenerators L_i, extra safe transitions, and adverse transitions. For each L_i event the marginal transition of coordinate i has a specified generator Q_i (or a history-dependent generator against which the inequality below holds uniformly). Any collateral coordinate changes are safe for the backward tests. The sum of these allocated event intensities must not exceed the actual generator's event intensities.

This is stronger than merely observing a progress rate at each coordinate. One common clock moving all n coordinates cannot be counted as n different rate-q clocks. The synchronized-progress counterexample in ROOT_PRODUCT_FORCING_REVIEW.md is retained. If each genuine progress event benefits at most r coordinates and is otherwise safe, uniform allocation across its beneficiaries can often supply a valid per-coordinate subrate reduced by at most r; it must actually be checked.

Adverse events touch at most k coordinates, and their total conditional participation intensity at coordinate i is at most b_i. Realized coordinate paths, adverse choices, and the environment may be arbitrarily correlated. The process must be nonexplosive or admit the standard bounded-test localization/Dynkin argument.

## Acquired one-coordinate input
For a declared horizon T, supply differentiable functions v_i(u,x) in [0,1], 0<=u<=T, satisfying

 v_i(0,x)=1_(x in A_i),
 partial_u v_i(u,x)<=Q_i v_i(u,x).

The second inequality is required for every allowed retained history if Q_i varies. An exact finite-chain backward probability is one example; a certified subsolution is equally valid. Every extra safe transition, and all collateral changes in an allocated L_i event, must increase or preserve the relevant v_j(u,x_j) for ALL u in this interval. These conditions are not inferred from a marginal probability estimate at one horizon.

## Product receiving law
Fix a in (0,1), C_k=(1-a)^(-(k-1)), beta_i=C_k b_i, and

 p_i(u,x)=e^(-beta_i u)v_i(u,x),
 f_i(u,x)=1-a p_i(u,x),
 F(t,x)=product_i f_i(T-t,x_i).

Because other factors can only decrease under an allocated coordinate event,

 (partial_t+sum_i L_i)F
 <=-F sum_i beta_i a p_i/f_i.

For an adverse event touching J, each new factor is at most1, so

 F_after/F_before-1 <=product_(i in J)f_i^(-1)-1
 <=C_k sum_(i in J) a p_i/f_i.

Actual participation bounds cancel the negative term. Extra safe events only help. Therefore

 E[(1-a)^(sum_i 1_(x_i(T) in A_i))]
 <=product_i[1-a e^(-beta_i T)v_i(T,x_i(0))].          (GBP)

GBP is a joint concentration certificate constructed from the actual generator and acquired one-coordinate backward tests. It does NOT say the endpoint indicators are independent, negatively associated, or Bernoulli variables with those parameters. Only the displayed transform and its valid Chernoff consequences are claimed.

For homogeneous rank-lowering progress, v_r(u)=Pr(Pois(q u)>=r) is the exact pure-death backward solution and safe collateral rank decreases meet the condition. GBP recovers ROOT_PRODUCT_FORCING.md and its exp(-c n T^L) lower-tail scale. Finite-state phase/clock models can instead contribute their actual matrix-exponential backward functions, if the uniform collateral and adverse participation interfaces are verified.

The result preserves source acquisition costs: solving/verifying each backward inequality, rate allocation and all participation bounds is required. It does not derive these from observed low-order correlations, assumed labels, a mean holding time, or a bounded generator norm without localization. Variable population, terminal output rewards, seed extinction, physical-clock conversion and whole chemical recurrence remain separate.
