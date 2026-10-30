# Exact coupled-face Green and a pooled catalyst coordinate

30 October 2026. New working construction, NOT independently reviewed. It preserves the previously reviewed compiler and the exact non-small-return obstruction. The purpose is to remove that bottleneck with an actual stopped operator, not assert its old norm small.

## Primary comparator and choice of representation

Laurence–Robert, [Scaling Methods for Stochastic Chemical Reaction Networks, §2.4](https://arxiv.org/html/2310.01949v3#S2.SS4), states a Filonov criterion: a normlike energy with an integrable state-dependent stopping time, bounded below by the first jump truncated at a fixed constant, and expected energy loss dominating expected elapsed time yields positive recurrence. This supplies a stopping-time method, not automatic coverage of this network. It motivates grouping a complete coupled-face excursion before estimating drift. Publisher access returned403; the author preprint was accessible. No denied Wisconsin source was accessed.

## 1. Exact deficiency-two module

Residual species a,C,E,D, with physical A=a+a0, a0>=2, m=a0+2. Fixed positive rates for

    a+D -> C+D       nu a D,
    C+D -> E+D       lambda C D,
    E+D -> a+D       mu E D,
    a+D -> 2a        kappa a D,
    2D -> a+D        rho (D)_2,
    2a -> a+D        k1 (a)_2,
    2a -> 2D         k2 (a)_2,
    C+D -> C+E       beta C D,
    C+E -> C+D       gamma C E,

plus clearing k0(a)_2. All fast rates are multiplied by (A)_a0(B)_q, with q>m and the same connector. Total n=a+C+E+D is conserved before clearing. The local module is considered on n>=2 and nonnegative residual a (so A>=a0); any smaller inactive exceptions belong to the finite connector head, not this local stage. Both seed channels are positive for the proposed global weakly reversible model.

The old D=0 interface is indeed non-small: from a=E=0,C=n-1,D=1, the first fast jump enters D=0 with probability beta/(beta+lambda). Nothing below removes or misprices that event.

Instead define the TRUE dormant set

    F={D=0, C E=0},

with two components (C-axis and E-axis, their overlap included once). The mixed face M0={D=0,C E>0} is active and is included inside the active module M={D>0} union M0. Stop an M-stage at the first true-F entrance, clearing, or connector event. A seed inside M is not a stop for the full stage, though it is a restart for local estimates.

## 2. Exact mixed-face first-event kernel

At a mixed-face input (a,c,e,0), the only fast events are:

* reverse C+E->C+D, rate gamma c e;
* the two seeds, total rate (k1+k2)(a)_2;
* clearing, rate k0(a)_2.

Connector immigration/activation add their actual physical rates, or their normalized rates after dividing by (A)_a0(b)_q. Thus the next event has the exact exponential holding law with total rate equal to their sum, and its output is one of the actual reverse/seed/connector/clear outputs. Reverse and seed outputs have positive D; connector/clear outputs terminate this stage. This is the coupled-face Green: a one-holding-time resolvent, not a small transition probability.

Positive-D entries into M0 can only be:

* beta C D at D=1, sending (a,c,e,1)->(a,c,e+1,0), c>0;
* kappa aD at D=1 with c e>0, sending (a,c,e,1)->(a+1,c,e,0).

For the first entry type, its operational rate beta c times the mean mixed holding is <=beta/gamma, since outgoing mixed e is at least1. For the second, the outgoing a is a+1, so the seed/clear denominator is at least (k0+k1+k2)a(a+1); its rate kappa a times the mean is bounded uniformly. This remains true when connector stopping shortens the hold.

Applying the entrance compensator up to a finite localization and then the strong Markov property at each actual entrance gives

    E total operational time in M0 <= C E total operational time with D>0.

The same inequality holds for any fixed power or inverse power of 1+A in the running cost: A is fixed during each mixed hold and changes by at most1 at entrance, so its actual input/output cost ratio is uniformly bounded. Physical restoration divides by (A)_a0(b)_q and retains that bounded ratio. Initial mixed-face waiting is handled separately in Section7 below.

This estimate pays arbitrarily many order-one mixed returns. No bound on their count and no assumption that their transition operator has norm<1 is used.

## 3. Pooled dynamics in the D-clock

On M, before true-F entry, use the clock

    u=integral 1_{D>0} D dt_op.

Mixed-face holding is deleted from this clock and has just been paid by its exact Green. Put

    z=E+D-1.

On positive-D states, a+C+z=n-1 and z>=0. The beta/gamma pair only switches E and D and preserves (a,C,z). Between nonlinear seed/clear marks, the pooled transitions in u-time are

    a -> C       rate nu a,
    C -> z       rate lambda C,
    z -> a       rate mu E + rho(D-1) + kappa a.

The first two terms in the last rate satisfy

    c z <= mu E + rho(D-1) <= C z,
    c=min(mu,rho)>0.

The kappa a transition consumes a z particle when z>=1. If z=0, that event instead enters the true dormant set and stops the stage. At mixed-face returns the reverse switch preserves the pooled state; a seed is retained as its actual a-to-z change. Thus the pooled process has a baseline linear cycle a->C->z->a plus adapted extra z->a transitions, stopped at true-F entry. Its total pooled population n-1 is fixed before seeds/clearing too; seeds merely convert one or two a particles into z.

One may choose a protected particle in the E+D pool and reassign its label at E/D switches. This is only a labeling of indistinguishable particles, not a change to the chain. Every pooled z->a event consumes one unprotected pool particle; the z=0 exception is the actual true-F stop.

## 4. Minimal-clock tagged particles, not a fictitious independent chain

The pooled z->a rate contains adapted extra terms, so claiming an exactly independent Q-cohort would be wrong. Instead attach independent per-label Poisson clocks of rates nu, lambda, c for the baseline moves a->C, C->z, z->a. Extra z->a moves are assigned adaptively to z labels; they can only advance a label toward a.

For any interval of length t<=1, the following event for a label guarantees it is at a at the endpoint, REGARDLESS of its starting pooled type and any extra z->a moves:

* no nu-clock ring throughout the interval;
* at least one lambda-clock ring in its first third;
* at least one c-clock ring in its second third.

Its probability is at least c1 t^2. These forcing events are independent across labels, conditional on the history before the interval. A label initially at a also stays there if its nu clock does not ring.

Before the next seed, this gives a binomial lower domination for a-occupancy at any deterministic D-clock horizon. Nonlinear seeds restart the low-a argument at their actual output. For an initial-a cohort, delete at most two labels per seed and continue deleted labels fictitiously. Surviving labels still have the forcing-event bound. Seed counts before clearing have a fixed geometric tail because all seed/clear marks share (a)_2, in positive D and on M0 alike.

The same deterministic-horizon/crossing argument as the reviewed tagged construction therefore gives

    P(inf_{t<sigma} a_t<c a_in) <= C n^M exp(-c a_in).

Here sigma is the ACTUAL M-stage stop and includes all mixed holds. A crossing in the D-clock can only be caused by an a->C move (cohort rate <=nu a_in) or a counted seed; mixed reverse switches do not reduce a. The claim uses independent forcing events at deterministic times, never survival-conditioned independence of the pooled particles.

## 5. Independent polynomial clock cost

All active states in M have a prescribed path of at most a fixed H (H=9 suffices for this cycle) to clearing or true F. A mixed state first takes its reverse C+E edge. With D>0, convert type particles along C->E->a, use the a-born birth if only one type remains, or the 2D source if all mass is D. Reaching true F is an allowed terminal event. Every required operational rate is bounded below away from zero and every total rate is at most C n^2.

Requiring each prescribed holding time to be <=1 gives success probability >=c n^(-2H) in H-unit blocks. Conditional block iteration yields all fixed polynomial absorption-time moments, independently of recurrence of the full connector. This pays the bad-cohort event and justifies localization in Section2. Connector stopping only shortens the episode.

## 6. Low-a clock, resets, and genuine dormant rarity

Below a cutoff K, use the independent forcing events of Section4 on n-1 labels. A D-clock horizon

    t_*=C sqrt(K/n)

has expected forced a-count at least4K and failure probability exp(-cK). Stop/restart at the actual seed, high-a entrance, terminal event, or horizon. The total seed count has bounded mean; the number of horizon failures satisfies the same conditional geometric counting inequality as in the reviewed graph proof. Thus E u_low<=C t_*.

Positive-D operational time is at most u_low, and Section2 pays the mixed-face time by the same quantity. Consequently low clearing probability is <=C K^2 t_*, and low connector probability is <=C t_* after physical normalization. A true-F entry can ONLY be an a+D birth at D=1 with C E=0, so its low-stage probability is <=C K t_*.

After a reaches K, the tagged-cohort estimate keeps it above cK except on probability C n^M exp(-cK). Clearing's physical hazard then pays time K^(-m)/(b)_q and A-occupation K^(1-m)/(b)_q. The actual terminal inverse profile is at most C K^(-s) outside that exceptional event. Hence, for every fixed s>0,

    E f_s(A_out) <= C_s [K^(-s)+K^2 sqrt(K/n)+n^M exp(-cK)].

Choosing K=n^(1/(2s+5)) yields a reset exponent s/(2s+5). Positive power decays for physical T and U follow from

    (b)_q T <= C[sqrt(K/n)+K^(-m)+n^M exp(-cK)],
    (b)_q U <= C[K sqrt(K/n)+K^(1-m)+n^M exp(-cK)].

For TRUE dormant return, the high-stage terminal compensator only sees a-born D=1 exits and costs C/K, while the low stage costs C K sqrt(K/n). With K=n^(1/5),

    P(enter F before connector/clear) <= C n^(-1/5).

This is a statement about F, not the old non-small D=0 kernel.

## 7. Initial mixed face and the acquired local certificate

For initial D=0,c e>0, the exact first hold has operational denominator at least c[ce+(a)_2]. If a<K and n is large, ce>=c+e-1=n-a-1>=n-K-1, so low-A terminal clear/connector probability is <=C K^2/n and its waiting time is small. Reverse and seed outputs are actual positive-D inputs of unchanged n; apply the preceding uniform kernels there. At high a, direct holding/outputs preserve each fixed profile and inverse-power grade. In particular all uniform resets survive, possibly reducing positive exponents.

The logarithmic-input split from the reviewed compiler now reacquires all fixed grades and profile preservation for the complete M-stage. The high-input proof uses Section4's forcing cohort instead of falsely asserting independent Q-chains. The terminal true-F compensator is unchanged, so for p>=a0 and x>=C log^2(2+n),

    T/U <= C/x,
    V_p/[(b)_q U] <= C_p x^(a0-p),

up to the already paid exponentially small error. All costs and rewards concern the SAME M-stage, including its mixed-face holds and actual true-F stopping event.

## Scope

This constructs a coupled active-face Green and reacquires the local interface for the stated deficiency-two module. It is not yet a whole-network recurrence receipt. The two true dormant components have identical A,B seed/clear kernels but their face labels and actual seed outputs must be retained in any full signed-cycle continuation. That remaining transfer is not licensed by merely renaming D=0 as F.
