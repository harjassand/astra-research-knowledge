# A stopped killing/Green consequence of collective forcing

30 October 2026. New local theorem, not yet reviewed. It uses the exact collective forcing contract and does not import a whole chemical recurrence conclusion.

Run the n-label process of COLLECTIVE_BOUNDED_NOISE_FORCING.md, n fixed, with an additional independent hazard clock killing at rate

    kappa (A_t)_m,   kappa>0, integer m>=1,

where A counts target labels. More terminal kills may be included; the terminal-profile conclusion below refers only to marks from the displayed kill channel. The underlying label process can be continued after killing with the same admissible contract. Neither immigration nor label deletion is included in this theorem.

Choose any fixed

    0<delta<min{1/(2L-1), m/(Lm+1)}.

There are c,C,epsilon>0 such that uniformly in the initial rank configuration, for all sufficiently large n and t_n=n^-delta,

    P(tau>t_n)<=C exp(-c n^epsilon),
    E tau^j<=C_j n^(-j delta)  (each fixed j>=1).       (G)

## Proof of survival bound with actual stopping

At deterministic time t_n/2 in the un-killed extension, the collective theorem gives at least M=c n t_n^L target labels except with probability exp[-c n t_n^(2L-1)]. Choose a measurable cohort of floor(M) such labels.

During the remaining half block, progress and safe moves cannot remove these labels from the target. Let J count adverse touches of this cohort, with multiplicity. Each event touches <=k labels and the summed touch intensity is <=bM. Therefore, for xi>=0,

    E exp(xi J_u) <= exp[(bM/k)(exp(xi k)-1)u].

This follows from the exponential counting-process generator, conditionally on the state and chosen cohort at the midpoint; it is not an independence assertion. Set xi=1/k. For all sufficiently small u,

    P(J_u>=M/2)<=exp[-M/(4k)].

Outside this event, at least M/2 cohort labels remain target THROUGHOUT the second half block. For n large M>=4m, and its integrated killing hazard is at least c kappa t_n M^m. The independent killing-clock construction now gives

    P(tau>t_n)
      <= exp[-c n t_n^(2L-1)]
         +exp[-c n t_n^L]
         +exp[-c n^m t_n^(Lm+1)].

Every exponent is a positive power of n by the displayed choice of delta. This estimates the ACTUAL killed survival event using an unconditioned extension, never the law of a cohort conditioned on survival.

The same bound holds conditionally at each full block while alive. For n large its right side is <=1/2, hence tau/t_n is dominated in tail by a geometric number of blocks. This proves (G). Finite n can be bounded separately if the exact progress/no-adverse event and kill mark remain available; the large-n assertion does not need an unproved finite-shell extension.

## Terminal inverse profile via the actual kill compensator

For the displayed kill channel, at its pre-jump state, for any K>=m,

    P(A_(tau-)<=K, displayed kill)
      =E integral_0^tau kappa (A_t)_m 1{A_t<=K} dt
      <=C K^m n^-delta.

If the kill removes at most m target labels, its actual output inverse profile satisfies, for each fixed s>0,

    E[(1+A_out)^(-s); displayed kill]
      <= C_s n^[-delta s/(m+s)].                     (R)

Indeed split at K=n^[delta/(m+s)] (with fixed factors and K>=2m): low input uses the compensator estimate, high input has A_out>=K-m. Other terminal channels are NOT covered by (R) merely because they shorten tau. They require their own actual rate/profile compensators.

## Scope and costs

This earns a uniform polynomial time/occupation scale and an actual terminal-profile reset for a specified fast kill channel under collective bounded noise. It does not yet earn incoming-profile-preserving grades, signed activation credit, seed-source cost, repeated varying-population excursions, or a full section operator. The exponents are weaker than independent-label forcing and all downstream finite-grade ordering would need to be redone. The clock is the one in the theorem's exact generator; physical-time conversion remains a separate obligation.
