# A raw-list global polynomial-cost episode with acquired transport

Author derivation from ordinary complex-balanced product-form theory, finite cycle circulation, finite differences and the Kac occupation identity. This is a GLOBAL episode/transport theorem for arbitrary finite weakly reversible mass-action lists. It is NOT a recurrence theorem: its receiving bound has no inward sign. Neither full recurrence of the six-species diagnostic nor unrestricted recurrence is claimed.

## 1. Precise output contract

Let a finite weakly reversible list on d species have positive fixed rates kappa_e, source s_e and product u_e. Use lambda_e(z)=kappa_e(z)_s_e. Let D=max_y |y| and M=number of distinct complexes. Null reactions can be omitted for physical return analysis; their genuine polynomial activity can be included in the reward. Physical singleton classes are elementary. For every other input x, the raw list constructs an actual randomized stopping episode sigma_x with:

* sigma_x includes at least one genuine reaction and ends after finitely many genuine reactions a.s.;
* for every fixed p>=0, with N=1+|x|,

      E_x integral_0^sigma (1+|X_t|)^p[1+q_actual(X_t)]dt
           <=C_p N^(p+K),                                (R1)

  where K=ceil(d/2)+2D(M+1) is a sufficient exponent;
* all source-indexed endpoint rewards have an explicitly acquired Poisson envelope (R8) below;
* both the actual endpoint AND the largest actual excursion obey

      P_x(sup_(t<=sigma) ||X_t-x||_1>=v)
        <=min(1,C N^K exp[-c(v-C0)_+^2/(N+v)]);            (R2)

  hence for fixed p>0,

      E_x sup_(t<=sigma)||X_t-x||_1^p
        <=C_p[N log(N+1)]^(p/2),                          (R3)
      E_x(1+|X_sigma|)^p<=C'_p N^p.                       (R4)

Constants depend on the finite raw list and p, not on x, its face, anchor sizes, lattice class or inventory ratios. This pays actual residence, every competing genuine reaction and every output; it does not presume nonexplosion of the full original process. The proof below constructs its finite pre-stop path by coupling to a proved nonexplosive reference.

The stopping rule uses independent ACCEPT/REJECT marks on genuine reactions; the ORIGINAL physical rates and path are unchanged. The reference parameters are chosen from x once and frozen throughout the episode. A numerical compiler for rational rates can acquire the finite data used here. It does not thereby solve the full kernel or recurrence problem efficiently.

## 2. Raw positive circulation and a nearby reference mean

For each raw edge choose a directed return path in its linkage, and let C_e be the resulting directed cycle. Weak reversibility supplies these paths by finite graph search, with length<=M. Let m_f>=1 count how often edge f occurs in the finite cycle cover. Then m is an exact positive circulation.

Choose one nontrivial reaction enabled at x and its strongly connected linkage L. For a complex y in L with a non-null outgoing edge, form its raw complex-balance defect polynomial

    b_y(c)=sum_(e:u_e=y) kappa_e c^(s_e)
                 -sum_(e:s_e=y) kappa_e c^y.

It is a NONZERO polynomial: the coefficient at its own monomial includes the strictly negative non-null outgoing sum, with no cancellation from distinct incoming source monomials. Pick its highest nonzero homogeneous part of degree h<=D. Precompute a positive integer direction v with that homogeneous polynomial nonzero at v. A finite grid {1,...,D+1}^d suffices to find one. Denote the nonzero leading value by a.

At input x evaluate only h+1 candidates

    c_t=x+1+t v, t=0,...,h.

The h-th finite difference of b_y(c_t) is h! a. Therefore some candidate has

    |b_y(c_t)|>=delta_0=h!|a|/2^h>0.                     (R5)

Choose any candidate c with |b_y(c)|>=delta_*=min(delta_0,1); a maximizing candidate is one option. The compiler uses the first candidate meeting this positive threshold. Every coordinate satisfies x_i+1<=c_i<=x_i+B, where the finite raw constant B can be taken <=1+D(D+1). All choices are finite exact comparisons for rational raw rates. This avoids an unevaluated equilibrium oracle and avoids arbitrarily small defects from a fortuitous near-balance point.

## 3. A complex-balanced SUBGENERATOR, not altered physical kinetics

Put f_e=kappa_e c^(s_e), epsilon=min_e f_e/m_e and

    g_e=epsilon m_e,
    kappa_bar,e=g_e/c^(s_e),
    kappa_rej,e=kappa_e-kappa_bar,e>=0.                    (R6)

The g flow is balanced at every complex, so the reference mass-action process with constants kappa_bar is complex balanced at c. All its constants are positive and no greater than the actual constants. Moreover, uniformly in x,

    kappa_bar,e>=c_raw N^-D.

Indeed c_i>=1 gives epsilon>=kappa_min/max m_e, and c^(s_e)<=C_raw N^D. The product-Poisson law

    pi_c(z)=product_i exp(-c_i)c_i^(z_i)/z_i!

is therefore a derived invariant law of the reference. The ordinary product-form theorem and finite Poisson activity prove its nonexplosion and classwise positive recurrence. All raw supports are unchanged by positive thinning, so reference and actual chains have the SAME communicating classes; weak reversibility makes them closed. We do not know or assume that the actual process is recurrent.

For clarity, this law belongs to a reference process personally constructed from the raw rates. It is not a stationary fiber assigned to the actual input. The actual episode consists of reference-rate events plus competing rejected-rate events, and stops at the FIRST rejected event. That is exactly ordinary independent Poisson splitting of the unchanged physical rates.

Stirling's elementary upper factorial bound gives the important input estimate

    pi_c(x)>=c_raw N^(-d/2).                              (R7)

The additive shift B is fixed. No global mixing rate is used.

## 4. A rejected event is reached with polynomial raw probability

Because g is a circulation, the residual flux d_e=f_e-g_e has the SAME complex defect b_y(c). By the acquired positive defect threshold, some rejected coefficient in L satisfies

    kappa_rej,e>=c_raw N^-D.

The initially enabled source y0 in L can reach its source s_e by a simple directed complex path of length H<=M-1. Every step is genuinely enabled: its physical states are x-y0+y_j>=0. They are distinct before the target, so this prescribed path does not return to x first. All its physical counts are <=|x|+D.

Each accepted reference event on that path has probability at least c_raw N^-2D in the FULL actual race, and the final specified rejection has the same lower bound. This uses the lower reference/rejected coefficient just proved, enabled falling factorials>=1, and total actual rate<=C_raw N^D along this finite collar. Thus during one reference return cycle to x, the probability of an actual rejection before that return is at least

    p_x>=c_raw N^(-2DM).

The rejection may happen sooner on another channel, which only helps the stopping claim. No deletion word, receiving law, or stationary entrance probability is supplied.

## 5. Kac occupation acquires the COMPLETE killed reward

Write q_bar for the genuine reference rate. Since x is active, q_bar(x)>=c_raw N^-D. Let Gamma be its reference/actual communication class. The ordinary reference return-cycle identity is

    E_x^bar integral_0^(T_x^+) F(Y_t)dt
       =pi_c(F 1_Gamma)/[pi_c(x)q_bar(x)]
       <=pi_c(F)/[pi_c(x)q_bar(x)]

for every nonnegative F with finite Poisson mean. It follows by applying the discrete embedded-chain Kac identity to its invariant measure pi_c q_bar and restoring holding times. The unknown class normalizer cancels exactly.

Couple the actual pre-rejection path to that reference path with competing killing. A killed trial costs no more than a complete reference return cycle. At every actual return to x the same trial restarts, with success probability at least p_x. A geometric renewal bound therefore gives the ACQUIRED global resolvent inequality

    E_x integral_0^sigma F(X_t)dt
       <=L_x pi_c(F),
    L_x=[pi_c(x)q_bar(x)p_x]^-1
       <=C_raw N^(d/2+D+2DM).

This is a bound on the actual killed process, from its actual input, covering every competing path. It is not use of an equilibrium fiber or a favorable transport expectation. Reference Kac recurrence is legitimate because its product-form stationary law and finite activity have already been proved independently of the unknown original recurrence.

Taking F=(1+|z|)^p(1+q_actual(z)) proves (R1), using exact Poisson factorial moments and ordinary polynomial Poisson moment bounds. In particular finite expected genuine pre-stop activity implies finitely many genuine events before sigma a.s. The raw positive rejection probability and renewal argument also prove sigma<infinity a.s.

## 6. Source-specific output AND full-excursion receiving envelopes

For any nonnegative receiving reward V and any actual rejected channel e, the genuine compensator and Poisson factorial identity give

    E_x[ V(X_sigma)1_(rejected channel=e)]
       <=L_x kappa_rej,e c^(s_e) E[V(Zeta+u_e)],           (R8)

where Zeta has the derived independent Poisson(c) law. The identity used is

    sum_z pi_c(z)(z)_s V(z-s+u)=c^s E[V(Zeta+u)].

Thus every actual source and product is retained, with a concrete common receiving envelope. It is not an asserted equality of the actual output law with Poisson.

For the maximum excursion, count EVERY genuine jump into a set A before and including rejection. The same argument, now with the FULL actual coefficients kappa_e, proves

    E_x[number of genuine entries into A before/at sigma]
       <=L_x sum_e kappa_e c^(s_e) P(Zeta+u_e in A).       (R9)

If x is outside A, visiting A requires such an entry. This pays the cost of leaving a protected region rather than discarding it. Since c=x+O_raw(1), all products u_e are bounded, and the prefactor in (R9) is <=C N^K, the standard elementary Poisson Chernoff bound yields (R2). Integrating its minimum with1 gives (R3). Taking |X_sigma|<=|x|+||X_sigma-x||_1 gives the moment-preserving receiving law (R4). Integer Poisson moments suffice first; fixed real powers follow by Holder.

## 7. What the theorem does and does not complete

This constructs one globally available actual-time operation for EVERY weakly reversible raw list, including high anchors, signed finite-tag representations and arbitrary inventory ratios. It replaces a furnished global clock/output oracle by a finite raw construction and explicit polynomial bounds. The nearby reference is chosen algorithmically and frozen; no paid resource, external controller, rate change or physical hardware action occurs.

It DOES NOT prove the needed inward inequality E[sigma+U_out]<=U_in. Moment-preserving transport has a constant and no sign. Repeating these episodes need not yield return or prevent accumulation of episode endpoints at infinity. Neither full original nonexplosion nor positive recurrence follows merely from (R1)-(R4). The remaining leverage point is a signed receiving/repayment rule for these globally acquired episodes, or a different global synthesis. A finite reference cycle or a finite computation is not that rule.

## 8. Ordinary provenance

The Poisson reference and its actual nonexplosion/recurrence are ordinary Anderson-Craciun-Kurtz2010 Theorem4.1 and Anderson-Cappelletti-Koyama-Kurtz2017/2018 Theorem2/Corollary2. Finite positive cycle circulation, finite differences, Kac regeneration and Poisson factorial tilting are also established ingredients. The author-derived operation here is their raw input-adaptive construction, polynomial actual rejection/reward bound, and source-indexed/full-excursion transport contract. No historical-priority claim is made.
