# Independent exposure-moment power-boundary review

30 October 2026. Frozen source SHA256 636e6a5b5b4470eaef64c454a6bb2cff46088b3e45fc38e11c016e8f8af45bbf, copied to `product_sources/EXPOSURE_MOMENT_POWER_BOUNDARY.md`. Dependency: the reviewed cumulative-budget product and priced exhaustion construction.

**Verdict: accept (M), its eta>1 polynomial consequence, and the order-one adversarial obstruction, with the initial-state/moment interpretation below.** No fixed-raw-rate necessity or global/stopped result is established.

For fixed a, the product transform bounds the virtual lower tail at a constant multiple of n exp(-CB)g_L(T), with exponential rate a constant times the same quantity. Each exhausted label has H_i>=B, so E J_T<=n M exp(-eta B), without any cross-label independence. Markov at a constant fraction of the virtual threshold gives a failure term bounded by C'M exp(-(eta-C)B)/g_L(T). The Poisson mass lower bound on 0<T<=1 gives exactly (M). Constants may depend on the fixed a; they need not remain uniform as a tends to zero.

For k>=1, C=(1-a)^(-(k-1)) can be chosen below any eta>1 (and is exactly one when k=1). Substituting T=n^-delta and B=gamma log n gives the displayed zeta and beta. The open gamma interval exists exactly when L eta delta<eta-C, as stated. This proves a positive polynomial count with a polynomial exceptional-probability term, not the former exponential-only concentration or sharp stopped scale.

In the obstruction, initialize all labels at rank1. Before t0 there is no adverse action, so marking probability p=1-exp(-q t0)<=qT. Conditional on being marked, the first reset has exponential integrated intensity E and exposure is min(E,B). Direct integration gives

    E exp(min(E,B)) = integral_0^B 1 dx + 1 = B+1.

Hence the unconditional exposure moment is 1+pB<=1+q. A marked label can end at target only if no reset occurs, probability exp(-B), or if a progress ring occurs during the final epsilon interval after a reset. A union bound pays all final-interval progress, marked or unmarked, by q epsilon. Thus endpoint target probability is at most qT exp(-1/T)+q exp(-2/T), and multiplication by n with T=n^-delta still tends to zero faster than every inverse power. Every actual rate is finite for a fixed horizon, event batch size is one, and the progress generator remains genuinely allocated.

Binding initial-state precision: if uniformity is intended over all initial rank configurations, record each label's initial rank and make only initially rank1 labels eligible for the final attack. Initially rank0 labels receive no adverse clock. Then the moment bound holds for every initial configuration, while the all-rank1 configuration retains the obstruction. This is an admissible retained-history rule, not anticipation.

The moment assumption and counterexample are UNCONDITIONAL exposure bounds from the declared start. They are not uniform conditional bounds at every subsequently selected history or stopping time. In particular, conditioning on a successful marked label makes its remaining exposure moment large. No restartable conditional certificate is disproved here. Likewise the family of admissible controls depends on the tested horizon; it disproves a uniform polynomial theorem over that family, not a result for one fixed physical rate law. One may disable pulses for non-small horizons if a class definition requires those too.

The example also satisfies any weaker positive exposure moment order below one, by monotonicity, but no claim of optimal non-polynomial estimates at order one is made. Raw exposure acquisition, incoming Green estimates, births/deletions, physical-clock conversion and full recurrence remain separate obligations.
