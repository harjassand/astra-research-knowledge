# Strong inventory tails coexist with arbitrarily slow physical return

Same principal, ordinary proof; no independent audit or historical-priority claim. This is a constraint on the destination and on the chosen global contract, not a counterexample to weak-reversibility recurrence.

## 1. A matched ordinary calibration comes first

For the family in GLOBAL_ORDERED_CYCLE_THEOREM.md, the k=3 member has deficiency zero. Its positive recurrence and product-Poisson law are established by Anderson, Craciun and Kurtz, *Product-Form Stationary Distributions for Deficiency Zero Chemical Reaction Networks* (2010), Theorems 4.1–4.2. [Primary author copy](https://people.math.wisc.edu/~craciun/PAPERS_NEW/Anderson_Craciun_Kurtz_ProdFormFinal_2010.pdf).

For every k, whenever the exact complex-balance rate identities in the global proof hold, let c=(a,b,c) be that proof's positive balance point. The stationary exponential/activity reward has the explicit ordinary value

    E_pi [(1+q(X))u^M]
      =exp((u−1)(a+b+c)) [1+kappa_0 sum_(j=0)^k u^|yj|].       (C1)

Indeed independent Poisson factorial tilting gives E[(X)_y u^M]=c^y u^|y| exp((u−1)sum c), and every cycle flux kappa_j c^yj equals kappa_0. At k=3 and all unit rates this becomes

    exp(3(u−1)) [2+u^2+u^4+u^7].                             (C2)

The new global compiler's huge bound is substantially worse on this ordinary admitted locus; it supplies no computational or scientific advantage there. Generic k>=4 rates violate complex balance, and only there is the comparison premise different. Historical novelty beyond these governing baselines has not been established.

## 2. Every member has no positive exponential physical return-time moment

Let k>=3 and let every fixed kappa_i>0. For n>=1 put

    z_n=(0,n,n), S_n={z_n+yj:0<=j<=k}.

Each of the k+1 designated cycle jumps sends z_n+yj to the next member of S_n, cyclically. The set avoids zero. At its phase j, denote the designated propensity by r_j(n), the actual TOTAL propensity by Q_j(n). Higher sources than j are disabled by the A count. At j>=1 the designated source dominates every lower source as n tends to infinity: the exact factorial ratio has at least one divergent B or C factor. Hence

    r_j(n)/Q_j(n) ->1, Q_j(n)->infinity  for j>=1.

At phase zero, however, Q_0=r_0=kappa_0 exactly. For any 0<s<kappa_0 and n sufficiently large all Q_j>s. Conditional on its next raw jump being the designated one, retaining the actual holding clock gives the UNNORMALIZED transform

    E[e^(s holding) 1_(designated jump)]=r_j(n)/(Q_j(n)−s).

The transform of one full designated neutral cycle is therefore

    H_n(s)=product_(j=0)^k r_j(n)/(Q_j(n)−s)
          -> kappa_0/(kappa_0−s)>1.                           (C3)

Choose one n with H_n(s)>1. Irreducibility supplies a finite positive-probability path from zero to z_n that avoids returning to zero after its departure (erase any earlier loop at zero). Repeating N designated neutral cycles afterwards still avoids zero. If T_0^+ is the original positive PHYSICAL return time, the strong Markov property and nonnegative elapsed prefix imply

    E_0 exp(s T_0^+) >= p_prefix H_n(s)^N   for every N.

Let N tend to infinity. The expectation is infinite. For s>=kappa_0 the initial Exp(kappa_0) holding time already has infinite transform. Consequently

    E_0 exp(s T_0^+)=infinity for EVERY s>0.                   (C4)

The same argument works for return to any fixed state: choose n so S_n avoids that state and use an irreducible prefix avoiding its positive return. Thus even a single fixed-state exponential-return theorem cannot be transferred to this family. This does not contradict the finite physical occupation of (1+q)u^M proved in the global construction. In fact that construction's hierarchy of statewise occupation bounds proves every finite polynomial moment of the positive zero-return time; see its equation (20). The tail is faster than every polynomial in this precise moment sense, while every exponential moment is infinite.

This is why the global contract chosen before local analysis pays integrated time and genuine activity, and why it deliberately does not demand an exponential moment of global physical return. The earlier accepted-scope multiplicative theorem remains intact within its own terminal-gap premises; this family's exact terminal-gap refusal and (C4) show why those premises matter.

## 3. An exact zero-Poincare-gap calibration on the ordinary Poisson case

At k=3 and unit rates, pi=e^(−3)/(A!B!C!). For z=z_n write p_n=pi(z). The four stationary weights divided by p_n are

    1,
    1/(n+1),
    1/[2(n+1)^2],
    1/[6(n+1)^2(n+2)^2].

Only nondiagonal designated jumps stay in S_n. All earlier raw-source jumps leave it, so its outward stationary flux divided by p_n is exactly

    J_n=1/(n+1)
      +[1+2(n+1)]/[2(n+1)^2]
      +[1+3(n+2)+6(n+2)^2]/[6(n+1)^2(n+2)^2].              (C5)

Thus Q(S_n,S_n^c)/pi(S_n)~2/n, while pi(S_n)->0. The stationary Dirichlet energy of 1_(S_n) is its outward flux, even for this nonreversible chain: stationarity equates inward and outward flux. Its variance is pi(S_n)(1−pi(S_n)). These exact test functions force the Poincare constant's spectral-gap infimum to zero.

No statement about every possible nonreversible spectral or hypocoercive notion is inferred. The precise conclusion is the failure of a positive uniform Poincare/Dirichlet gap. The global construction never inserted such a gap as a premise.

## 4. What the fixed translated source list does supply

Here slow neutral cycling costs O(1) physical time per cycle but eventual rare deviations have a globally paid activation/repayment law. The raw nested list supplies exact factorial ratios; one finite maximal-source normalizer receives all nonsection landings; a decreasing f_b/(M+1) correction pays actual low-B conversions; and on the A-axis the entire first-order borrowed inventory is repaid before the remaining O(A^−2) risk is charged. These are compatible with (C4).

The state-selected explosive corridor from the preceding stage lacks this fixed translation-complete source structure. Deletion words and finite-cell inward odds alone did not pay its global clock. Conversely, (C4) shows that even the correct finite mass-action list cannot be required to supply a uniform exponential-return clock or mixing gap. The unrestricted destination needs finite global return reward with its actual state dependence, not either of those stronger properties.
