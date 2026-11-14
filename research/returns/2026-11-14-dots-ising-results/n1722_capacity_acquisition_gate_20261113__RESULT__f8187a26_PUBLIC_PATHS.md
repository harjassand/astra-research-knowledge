# Independent capacity-acquisition gate after occupation closure

This is a scope/reduction result, not a new capacity algorithm. It uses the authorized original source `n1722_transport_attack_20261113/ordered_current_source_return.txt`, lines 20–41, 283–334 and 480–533. No held source was opened.

Keep the ORIGINAL A, physical generator, kappa, target B and decreasing voltage. Suppose a completed occupation proof establishes

0 <= N_(A^c)/ZA <= eta.

Then, with lambda=C_kappa/ZA,

 1/lambda - 1/kappa <= Q=N/C <= (1+eta)/lambda - 1/kappa.

This follows exactly from N_A=ZA-C/kappa, including A intersect B. Combined with the original allminus source join, alpha=1+kappa D0,

 1/lambda - 1/kappa <= T_h <= alpha[(1+eta)/lambda-1/kappa]+D0.

If an acquired joint confidence interval gives 0<lambda_- <= lambda <= lambda_ < kappa, the fully evaluable enclosure is

 T_lower=1/lambda_ -1/kappa,
 T_upper=alpha[(1+eta)/lambda_- -1/kappa]+D0.

Use these actual endpoints to test the requested ratio; do not hide cancellation in an asymptotic error statement. If lambda_<=kappa/2, the relative error amplification from the reciprocal and occupation correction is bounded by a constant. Neither occupation closure nor this algebra acquires lambda.

## Exactly what remains for the retained capacity estimator

The original source only supplies a CONDITIONAL estimator. A constructed trial voltage f with energy W must come with:
1. a polynomial-time acquired energy-weighted edge law, including its normalizer W;
2. a certified polynomial bound on W/C_kappa, not merely finite upper/lower capacity inequalities;
3. polynomial expected cost of the coupled ORIGINAL-PHYSICAL decision trajectory, for example a nonnegative V with -L_kill V >= Gamma_f and an acquired bound on sum w V/W;
4. charged proposal approximation, truncation and arithmetic errors, with confidence allocation.

Its second moment is <=(n+1) W C. Thus independent samples needed for fixed relative precision scale at least with the certified ratio (n+1)W/C in the available guarantee. The supplied truncation uses inverse-polynomial TV only AFTER W/C has been bounded polynomially. Occupation bounds on sum w v, even for every exterior sector, do not give a representation of f, an edge sampler, or the decision-time supersolution.

## Why the current capacity interval does not already close the gate

Our thermal-core lower is C/ZA >= 1/D_kappa, where
 D_kappa=kappa^-1+2n exp(8 theta R/a0+8 theta), a0=49999/50000.
At theta4 its exponential term has slope 32/a0>32 in R. The current optimized cut upper has leading slope about21.76. Using that upper as a candidate W bound and this lower to certify W/C therefore leaves an exponential certified gap about exp(10.24 R), before polynomial factors. This does NOT prove the actual ratio W/C is exponential: it proves the presently available bounds do not certify a polynomial ratio. A sharper constructed flow or a near-optimal acquired trial potential may close it; winding occupation certificates alone cannot.

Similarly, a direct simulation from the acquired core samples success probability p=C/(kappa ZA). It does not remove rarity: Bernoulli relative estimation requires order1/p successful-decision opportunities in the naive scheme. The retained importance-sampling estimator exists specifically to avoid that cost, conditional on the four gates above.

## Research consequence

Zero-essential occupation closure is an important independent theorem. It would reduce full mean prediction to acquiring lambda with the exact endpoint contract above, but would not itself prove the original polynomial-work North Star. Capacity acquisition should remain a separately tracked obligation, not silently inferred from source coverage or from an exponential native-time proof. No new breakthrough or package is claimed here.
