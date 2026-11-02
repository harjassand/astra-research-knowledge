# Closing an unclean phase3 overlap by a twin-hazard operation

Author construction. This pays the actual phase3 overlap port which the star launch previously received without resolving. It does not infer high-anchor or arbitrary-face coverage.

## 1. Raw input and same receiver

Take x=rho+y3+z1, with rho's anchors zero, hidden coordinates nonnegative, total N large, and the same fixed small-relative-difference cone as the star theorem. Thus A=3,D=1, and Z=N+15. The peer case x=rho+y1+z3 has the same proof; because the conservative rates are2/1, its fixed terminal/adverse ratio is 2beta_3 instead of alpha_3. All rates are fixed positive.

Until the FIRST noncore event, A,D stay fixed. With physical hidden coordinates B,C,E,F, the core rates are

    f=6(B)_2(C)_2       for B,C decreasing by2,
    g=3(E)_2(F)_2       for B,C increasing by2.

The cold terminal channel has hazard

    h_T=6alpha_3(B)_2(C)_2=alpha_3 f.                     (T1)

All OTHER genuine noncore hazards sum to

    h_O=alpha_0+beta_0+3alpha_1 B+6alpha_2 BC+beta_1 E
          <=C(N+BC+1).                                   (T2)

These are exact raw identities, including every competing source. The first-noncore time has mean <=1/(alpha_0+beta_0), independent of the number of internal core jumps.

## 2. A terminal hazard pays every adverse transfer

Merge the events with rates f and h_T. At each such actual event, the conditional terminal probability is alpha_3/(1+alpha_3), independent of the current hidden counts. Hence the number J_down of downward core moves BEFORE the first noncore event has

    P(J_down>=j)<=(1+alpha_3)^(-j).                        (T3)

Other stopping channels only improve this bound. Arbitrarily many upward moves and pauses are included. This is an acquired raw hazard comparison, not a stationary fiber or a mixing statement.

## 3. The first noncore channel is terminal with probability 1-o(1)

Put l=ceil(N^(1/3)). If min(B,C)<l initially, the pair-difference cone implies max(B,C)<=l+eps N, while E,F>=cN for sufficiently small fixed eps. Until min(B,C) reaches l, the pure core has

    L min(B,C)=2(g-f)>=c N^4.

Stopping the bounded distance martingale gives mean pure-core hitting time <=C l/N^4. On this whole low region h_O<=C N l, so the probability of an OTHER noncore interruption before that hit or the desired terminal event is <=C l^2/N^3. A terminal before the guard is already a success.

After the guard, falling below l/2 requires at least l/4 downward moves, and (T3) bounds its probability exponentially in l. As long as min(B,C)>=l/2, exact factorial comparison gives

    h_O/h_T<=C[N/l^4+1/l^2].                             (T4)

The genuine channel compensator integrates this ratio against the actual terminal hazard; the latter integrates to a probability <=1. Combining the guard, (T3) and (T4) proves

    P(first noncore is not T)<=C N^(-1/3).                (T5)

uniformly in ALL nonnegative residual populations in the cone. For an input already above the guard, omit its first hitting segment. No instantaneous equilibration was used; the terminal can and generally does occur at a noncentral composition.

The desired terminal event has Delta Z=0. Every OTHER first-noncore event has Delta Z<=3 and bounded absolute increment. Thus every unsuccessful source contributes only O(N^-1/3) to the expected positive mass increment, and receives its actual endpoint.

## 4. A disappearing peer packet is also paid

After T, A=0,D=1. To apply the proved phase1 star episode its residual peer E-1 must be nonnegative. It was so initially. A violation E=0 requires a genuine core-up move from E=2 before the first noncore event.

At E=2, the difference cone gives F<=eps N+O(1), while B,C>=cN. Therefore the rate of that E=2->0 move satisfies

    g 1_(E=2)<=C N^-2 h_T.

The actual channel compensator bounds the probability of ever making it before the first noncore event by C N^-2. This includes every possible later return and recrossing. On that exceptional output stop and receive Z unchanged. On all other terminal outputs rho'=x_after-z1 is nonnegative, has total N and the SAME hidden-pair differences as rho. Thus it is an admitted ACTUAL phase1 input of STAR_PHASE_ONE_EXTENSION.md.

## 5. Complete physical repayment

On a terminal output with valid peer packet, execute that already constructed phase1 star episode, including its actual finite-rate activation and fixed delayed drainage. Its expected Delta Z is <=-d<0, its final increment is bounded, and its physical mean is <=C(N+15). On every other first-source outcome stop immediately at the same receiver.

By (T5) and the packet-loss bound, the whole operation has

    E Delta Z<=-d+o(1),
    E(Delta Z)^2<=C,
    E sigma<=C(N+15).

Since input Z=N+15, the same quadratic identity and a sufficiently large FIXED D give

    E[sigma+D Z(actual output)^2]<=D Z(input)^2.           (T6)

One common scale D can be chosen for the finite list of star, central and terminal-port operations. All failures, residence and actual source outputs have been paid. This closes the original star's unclean phase3 overlap port throughout its population cone, without demanding that it enter a central fiber first.

## 6. General operation and remaining boundary

The reusable principle is h_termination>=eta times the hazard of an adverse inventory move. It gives a geometric count of those adverse moves even while other inventories evolve and favorable motion is unbounded. A finite raw activation guard can then establish terminal dominance and the actual receiving class. This is stronger than merely possessing a deletion word or bounded rate distortion.

It is not a general raw-list theorem. Initial phase2/phase3 states with signed packet residuals, anchor>=4 outputs, and large pair-difference faces remain unclosed. Their receiving values exist at the physical function Z, but receiving a value is not yet proving a return operation there. The full recurrence synthesis still needs those compatible operations.
