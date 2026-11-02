# A global activation/repayment theorem for an ordered cycle family

Author-derived ordinary mathematical proof by the same principal. No independent review or historical-priority clearance is claimed. The unrestricted weak-reversibility conjecture remains open. The degree-seven k=3 member is an established complex-balanced baseline; the theorem below also covers arbitrary positive rates and generic non-complex-balanced members of unbounded deficiency.

## 1. Exact raw list and complete conclusion

Fix an integer k>=3. On three free count coordinates (A,B,C), let

    y0=(0,0,0), y1=(1,1,0), yj=(j,j−1,j−1) for 2<=j<=k.

The genuine channels are yi->yi+1, 0<=i<k, and yk->0. Their fixed constants kappa_0,...,kappa_k are all positive. Propensities are kappa_i (x)_(yi), with ordinary integer falling factorials and no hidden factorial divisors. Put

    M=A+B+C, q(x)=sum_i kappa_i (x)_(yi).

**Theorem.** This CTMC on N^3 is nonexplosive and irreducible positive recurrent. For its unique stationary law pi and every r>0,

    E_pi [(1+q(X)) exp(r M(X))] < infinity.                     (1)

Every positive physical return to zero has all finite polynomial moments. It has NO positive exponential moment; SLOW_CLOCK_CALIBRATION.md proves this compatible constraint.

The proof constructs one global physical return/occupation contract across all faces, including high A and low B/C. For positive rational rates and rational 1<u<t it acquires explicit finite chart constants and an integer finite-head radius for the reward F=(1+q)u^M. The receiving function off the slow section is constructed as a finite expected stopped occupation, with a proved bound, rather than supplied as an oracle. Exact enormous moment bounds can be retained as factored expressions; no practical performance or polynomial binary-input complexity is claimed.

The growth increments are

    u0=(1,1,0), u1=(1,0,1), ui=(1,1,1) for 2<=i<k;

the degradation decrement is v=yk=(k,k−1,k−1). Every growth increases A by one, increases total count by at most three, and never decreases B or C. Degradation decreases A by k and total count by 3k−2. Also q(x)>=kappa_0.

## 2. Actual class and strongest ordinary baseline

Every state communicates with zero. The following actual words decrement only the indicated coordinate:

* B>=1: [0,1,1,3,4,...,k].
* C>=1: [0,0,1,3,4,...,k].
* A>=1: [0,1], then channel 2 repeated 2k−3 times, then channel k twice.

For the first two words, 3,...,k−1 are the successive growth channels and k is degradation. Their intermediate sources are enabled under the stated conditions; their net changes are respectively -e_B,-e_C,-e_A. For the last word, after its growths the state is

    x+(2k−1,2k−2,2k−2),

so both degradations are enabled whenever A>=1. Its endpoint is x-e_A. Weak reversibility supplies enabled reverse paths for every step. Repetition proves that the actual class is all N^3. Maximum word length is 2k+1, and the total-count prefix overshoot is at most J_del=6k−5.

The stoichiometric span is R^3, since the first three growth increments have determinant -1. The deficiency is k−3. The network is complex balanced exactly when

    kappa_j=kappa_3^(j−2)/kappa_2^(j−3),   4<=j<=k.             (2)

Indeed the cycle flux equations force ab=kappa_0/kappa_1, ac=kappa_1/kappa_2 and abc=kappa_2/kappa_3, and every subsequent ratio must give that same abc. When (2) holds, the balance point is

    a=kappa_0 kappa_3/kappa_2^2,
    b=kappa_2^2/(kappa_1 kappa_3),
    c=kappa_1 kappa_2/(kappa_0 kappa_3).

Thus k=3 is deficiency zero and already has the ordinary product-Poisson theorem. For k=4, rates all one except kappa_4=2 violate (2). The new global construction is needed beyond that ordinary balance premise.

The accepted terminal-gap cone cannot admit this family: for divergent coordinates I={B,C}, outside coordinate A and weight w_B=w_C=1/2, s_A<=c_A forces source index<=terminal index, and hence w.(s−c)<=0. The full span makes I admissible. This is an exact refusal of that sufficient architecture, not instability.

## 3. The common physical contract

Fix rational 1<u<t; arbitrary real desired exponential rewards are covered by choosing u>exp(r). Define

    W(x)=t^M, F(x)=(1+q(x))u^M,
    delta=1−1/t, s=u/t, zeta=1−s, rho=1−delta/2.

For any finite jump-based stopping episode, conditional expectation over its ACTUAL holding times gives

    E integral F dt = E sum_prejump u^M(1+1/q).

Thus the q term pays genuine jump activity and the 1 term pays physical residence. Since q>=kappa_0, an episode of at most l jumps with count overshoot at most 3l has expected F-cost at most

    l(1+1/kappa_0) u^(M+3l).                                  (3)

No nonexplosion, stationary fiber, mixing gap, neighboring-profile law or receiving function has been presumed. The embedded chain is constructed first; positive expected activity bounds below will rule out explosion.

Let the slow section be

    Z={A=0} union {B=C=0}.

For a finite nonnegative decreasing profile f_b, supported on b<B_*, prescribe section values

    V_Z(0,b,c)=t^(b+c)[1+f_b/(b+c+1)],
    V_Z(a,0,0)=t^a.

Values on a finite head H={M<=L}, including the origin, are set to zero. This profile and L will be acquired below. The common receiving function in the complement will be PROVED to satisfy V_off<=W.

## 4. A universal normalizer for the entire complement

From x outside Z stop at the first degradation or after k genuine jumps, whichever occurs first. Stop earlier upon hitting H. Every endpoint has count at most M+3k. We prove a uniform strict bound

    E_x W(X_sigma)<=rho W(x)                                  (4)

outside an explicit finite head; setting a head endpoint's assigned value to zero only improves the estimates.

Write

    R=max_(1<=j<=k) sum_(i<j) kappa_i/kappa_j,
    S=sum_(i<k) kappa_i/kappa_k.

Nested complexes give the exact ratio, when yj is enabled,

    q_i(x)/q_j(x)=(kappa_i/kappa_j)/[(x−yi)_(yj−yi)].            (5)

All nonzero falling-factorial factors in its denominator are positive integers. Let a,b,c denote the starting counts.

**High A.** If a>=2k, every lower-source/maximal-source ratio is at most 2(kappa_i/kappa_j)/a before the first degradation. With probability at least 1−2kR/a every chosen source is maximal. A maximal growth raises the maximal enabled index by at least one. The resulting growths form a subset of u0,...,u_(k−1), followed by degradation. If all indices were visited, the start would lie in Z: when A>0 and B>0, source 1 is already enabled; when A>0,B=0,C>0, one channel-0 jump already enables source 2. Thus outside Z at least one growth is omitted. Its endpoint is componentwise below x, with M reduced by at least two, in at most k jumps.

**High B, A>=1.** Before degradation, avoid channel 0; its probability relative to the enabled channel 1 is at most kappa_0/(kappa_1 b). All other growths increase both A and C by one. After at most k−1 such growths the degradation source is enabled. Once enabled its extra B degree makes the probability of choosing any growth at most S/(b−k+2)<=2S/b for b>=2k. Hence with probability at least

    1−k[kappa_0/kappa_1+2S]/b

degradation occurs after at most k−1 growths. Those add at most 3k−3 particles; degradation removes 3k−2. M falls by at least one. No assumption about C is used.

**High C, A>=1.** If necessary allow one initial growth to reach A>=2,B>=1. When B=0 only channel 0 is enabled; when A=1 the available channels 0 and 1 both accomplish this in one jump. Thereafter physical ABC growth dominates channels 0 and 1, since their total ratio to channel 2 is at most

    [kappa_0/(2kappa_2)+kappa_1/kappa_2]/c.

After at most k−2 additional ABC growths the degradation source is present. Its extra C degree then makes growth probability at most 2S/c for c>=2k. With probability at least

    1−k[kappa_0/(2kappa_2)+kappa_1/kappa_2+2S]/c

at most k−1 growths precede degradation, again decreasing M by at least one. No assumption about B is used.

Consequently take integer thresholds

    A_hi>=max(2k,4kR t^(3k)/delta),
    B_hi>=max(2k,2k[kappa_0/kappa_1+2S]t^(3k)/delta),
    C_hi>=max(2k,2k[kappa_0/(2kappa_2)+kappa_1/kappa_2+2S]
                         t^(3k)/delta).

If an off-Z state has any coordinate above its threshold, its good endpoint has W ratio<=1/t and the bad probability times its maximum W ratio t^(3k) is at most delta/2. This proves (4). All off-Z exceptions lie in a finite box, hence in {M<=A_hi+B_hi+C_hi}.

**Actual Dirichlet receiver.** Put epsilon=delta/(8rho). Once f is fixed, choose L so f_max/(L+1)<=epsilon. Then V_Z<= (1+epsilon)W everywhere outside H and is zero on H. Also enlarge L so the expected cost (3), with l=k, is at most (delta/8)W. Since (1+epsilon)rho=1−3delta/8, one normalizer step with continuation value W off Z, boundary value V_Z on Z, and zero on H costs at most (1−delta/4)W.

Nonnegative value iteration therefore constructs

    V_off(x)=E_x[ integral_0^tau_(Z union H) F(X_s)ds
                   +V_Z(X_tau)1_(X_tau in Z\H)] <=W(x).        (6)

Every normalizer episode uses at least one jump. Its expected accumulated q reward is the expected genuine jump count, so (6) proves stopping in finite expected jump count and finite physical time. It is not an assumed hitting law. The first holding reward is at least u^M, so V_off is normlike. First-jump decomposition yields LV_off=−F at every off-Z state outside H. All actual outputs, including high A and both low inventories, are now received at this SAME earned function.

## 5. Interior plane excursion, including all unbounded overruns

Start (0,b,c), b,c>=K+k, where K>=2k. Stop at the next A=0, the first B<K or C<K, or H. Until a growth occurs out of A=k, exactly k growths precede degradation. The first two growths have B+C increment one; each later one has increment at most two. Hence every no-overrun return has Delta(B+C)<=0. Equality occurs only for the ordinary cycle or the branch with one extra channel 0 at A=1 and all later ABC increments; the latter gives (b+1,c−1). Thus equality never decreases B.

The actual B-deletion word from Section 2 has probability at least d/(c+1), where

    d=[kappa_1/(kappa_0+kappa_1)]
      [kappa_1/(kappa_0/2+kappa_1+kappa_2)]
      product_(j=3)^k [kappa_j/(sum_(i=0)^j kappa_i)] >0.        (7)

The first factors are the exact lower-source probability at A=1 and the repeated channel-1 probability at A=2. All later factors follow from (5). This word returns (0,b−1,c).

At its first A=k visit, the probability of any growth rather than degradation is at most U/(bc), U=4S. While A>=k,B,C>=K, the actual growth/degradation ratio is at most

    S/[(A−k+1)(B−k+2)(C−k+2)]
       <=rho_K:=S/(K−k+2)^2.                                  (8)

After a first overrun A=k+1. If T is the additional stopped jump count, U_A the upward steps taken at A>=k, D the degradations and L_A the upward steps below k, then L_A<=(k−1)D. Nonnegative terminal A implies D<=k+1+U_A, so

    T<=(k+1)U_A+J0,       J0=k(k+1).                           (9)

This holds also for protected-region exits and for every finite pre-stop prefix. Each collapsed A word with U_A=l has probability at most rho_K^l. Counting all words of length at most (k+1)l+J0 proves

    E L0^T <=2^(J0+1)L0^J0/[1−2^(k+1)rho_K L0^(k+1)].        (10)

It also proves almost-sure finite T. Choose L0=2t^3 and K so rho_K<=1/[2^(k+2)L0^(k+1)]. Then (10) is at most

    C_T=2^(J0+2)L0^J0.

The total count before the overrun is at most b+c+3(k+1), and thereafter increases by at most three per jump. The full output W budget is therefore at most

    C_out=t^(3(k+1)) C_T

times the starting W, conditionally on overrun. This includes the actual A landing at every protected exit. It includes EVERY competing path, not just the negative word. The full expected physical F-cost is at most C_int u^(b+c), with

    C_int=(1+1/kappa_0)(k+2)t^(3(k+1))(1+C_T).                 (11)

Indeed k+1+T<=(k+2)2^T, and (3) plus (10) pays both time and reaction activity.

Use the earned receiver V_off<=W on an exit with A>0. A protected first exit has B,C>=K−k+1>0, so it really is off Z. On an A=0 landing, V_Z<=2W once the finite head includes f_max/epsilon. Every no-overrun radial decrease absorbs the f/(M+1) term when epsilon<=(t−1)/2, which is already true for the chosen epsilon. Zero radial change cannot increase f because B does not decrease. Thus the negative contribution is at least d delta/[2(c+1)] while all positive overrun value is at most 2U C_out/(bc). Choose additionally

    K>=16 U C_out/(d delta).

Then the FULL output drift is at most

    E V(boundary)−W(start) <=−d delta W(start)/(8c).             (12)

Here V(boundary) includes the complete future normalization reward at any off-Z exit through (6). There is no omitted return cost. Set B_*=K+k; this is also the finite plane-chart cutoff.

## 6. Low-B plane chart, with an acquired feedback profile

Start (0,b,c), b<B_*, c large. Fire 0. At A=1 allow either 0 or 1. Then follow source j at phase A=j for 2<=j<=k, aborting on the first unexpected channel. Normal completion gives (0,b,c); the channel-0 choice at A=1 gives (0,b+1,c−1). Its exact probability before later phases is

    p_b=kappa_0/[kappa_0+kappa_1(b+1)].

For c>=2k every unexpected source probability along the later phases has total at most D_C/c, with D_C=2(k−1)R, by (5) and its extra C factor. Both first branches obey that same bound. For c>=2D_C the good conversion probability is at least p_b/2. Every abort lands off Z with total count at most b+c+3(k+1), hence receives the already proved V_off<=W. Put E=t^(3(k+1)).

Acquire the profile by

    f_b−f_(b+1)=G/p_b,   G=4(D_C E+1),
    f_b=0 for b>=B_*.

No B_*-state matrix need be enumerated: its exact closed form is

    f_b=G[(B_*−b)+(kappa_1/kappa_0)(B_*−b)(B_*+b+1)/2]

for b<B_*. This is a derived, nonconstant actual landing profile, not a supplied transport law. For c>=B_*+1, b+c+1<=2c. The good conversion decreases V_Z by at least p_b(f_b−f_(b+1))W/(4c), while every bad output costs at most D_C E W/c. Consequently

    E V(boundary)−V_Z(start) <=−W(start)/c.                    (13)

All feedback is included: the conversion can cross B_*, and f_(B_*)=0 is the actual neighboring value. Other aborts already pay their entire normalization through (6).

## 7. Low-C plane chart

Start (0,b,c), c<B_*, b large. Follow 0 then 1. At A=2 allow either 1 or 2, then sources 3,...,k; abort on any other channel. The channel-1 alternative returns (0,b−1,c), while the channel-2 alternative returns (0,b,c). Their physical clocks and all counts are actual.

The probability of the negative alternative, with all later designated channels, is at least

    d_C=(1/2)[kappa_1/(kappa_0+kappa_1)]
              [kappa_1/(kappa_0/2+kappa_1+kappa_2 B_*)]>0       (14)

for b>=4(k−2)R. The total bad probability is at most D_B/b, where

    D_B=2kappa_0/kappa_1+2(k−2)R.

At phases j>=3 every earlier source has a strictly smaller B exponent; at the first two phases the only excluded source is 0. This proves the stated bound directly from (5). The actual abort receives V_off<=W, with excess factor at most E. If b>=B_*+1 both good landings have f=0. For

    b>=max(2k,B_*+1,4(k−2)R,2D_B E/(delta d_C))

the full output drift is at most -delta d_C W/2. This is against the SAME V used in (12)–(13), without a receiving-law premise.

## 8. A-axis: continue until the borrowed inventory is repaid

Start (a,0,0), a large. Follow maximal sources along its normal translated cycle. Permit one first mismatch whose source-index gap is exactly one, then follow the actual maximal-source normalization until Z. Abort on a first gap >=2, a second mismatch, or after J=3k+3 jumps. Every abort is received at V_off; the successful paths below finish before the cap.

There are four exact finite classifications of a gap-one first mismatch:

1. At phase 1, repeating channel 0 adds AB. Maximal completion makes two degradations and returns to the SAME axis point.
2. At phase 2, repeating channel 1 adds AC. Maximal completion also returns to the SAME axis point.
3. At phases 3,...,k−1, the preceding source has the SAME ABC physical increment as the maximal source, so the physical completion is unchanged.
4. At phase k, channel k−1 causes an ABC overrun. One degradation leaves (a+1,1,1), then sources 2,...,k return (a−1,0,0).

These statements are exact coordinate identities. Cases 1 and 2 are the borrowed-inventory repayment that a first-switch stopping rule loses. Every successful completion uses at most 2k+2 jumps. All prefixes have A>=a−kJ, so if a>=2k(J+1), (5) bounds a gap-one-or-larger mismatch probability by 2R/a and a gap>=2 probability by 4R/a^2. Therefore

    P(abort)<=C_bad/a^2,
    C_bad=4kR+4kJ R^2.                                        (15)

The first term pays every gap>=2 first event; the second pays a first gap-one event followed by any second event. This includes raw source mismatches having identical physical increments.

The negative terminal-overrun event has probability at least d_A/a, where

    d_A=kappa_(k−1)/(8kappa_k),                                (16)

for a>=max(2R,4(k+J)R). Indeed at the terminal phase its exact growth/degradation ratio is kappa_(k−1)/[kappa_k(a+1)], and the normal prefix and maximal completion together have probability at least one half. Every other good branch returns the identical axis value. An abort has M<=a+3J and is genuinely off Z, so (6) pays it by at most t^(a+3J). Hence for

    a>=max(2k(J+1),2R,4(k+J)R,
                  2 C_bad t^(3J)/(delta d_A))

the full output drift is at most

    E V(boundary)−t^a <=−delta d_A t^a/(2a).                   (17)

Every outward prefix and every abort is charged. There is no protected-region exit omitted: the whole pre-abort construction has bounded length J, and the normalizer handles the actual future after an abort. Its own prefix F-cost is at most J(1+1/kappa_0)u^(a+3J).

## 9. One finite head closes all operations without circular choices

All constants above are acquired in this order: k,kappa,u,t; the normalizer thresholds; the interior K and B_*; the explicit finite profile f; the low-C and axis constants. Only then select a single integer L. There is no dependence of K on f or on an unproved receiver: V_Z<=2W is obtained by enlarging L after f is known, and the complement's strict contraction absorbs that profile.

Choose L to include the normalizer box, the low-B/low-C/axis thresholds, and f_max/epsilon. Also choose L so each body's expected F-cost is at most half its output margin in (12), (13), (17) or the low-C inequality. Those comparisons are explicit: all body costs are C u^M, while the smallest margins have form c t^M/M. They hold beyond a finite threshold since u<t. They can be acquired without evaluating enormous powers: with zeta=1−u/t,

    M(u/t)^M <= exp(−zeta M/2)

for M>=4/zeta^2, because log M<=sqrt M. Thus M(u/t)^M<=h is guaranteed additionally by M>=2/[zeta min(h,1)]. The simpler comparison C(u/t)^M<=h follows for M>=C/(zeta h). All are rational sufficient thresholds for rational input. Finally enlarge L, if desired, so the residual output margin after cost is at least one; t^M>=exp(delta M)>=(delta M)^2/2 provides an explicit rational condition.

The compiler records one conservative L satisfying all these inequalities. It does not infer it from finite samples. On every section state outside H, its chosen actual episode, followed by the earned normalizer on an abort, ends in Z or H and satisfies

    E[ integral_0^sigma F ds+V_Z(X_sigma)1_(X_sigma in Z\H)]
       <=V_Z(x)−1.                                          (18)

Off the section, (6) supplies the SAME contract. The body choices are exhaustive: b<B_* uses (13); b>=B_*,c<B_* uses Section 7; both inventories large use (12); the A-axis uses (17). High-A and low-inventory exits from every body have already been received by (6). Stopping earlier on H only removes nonnegative future reward.

## 10. Global physical recurrence, moments and an explicit factored bound

Repeat section episodes, absorbing at H. The nonnegative potential plus accumulated F reward is a supermartingale. Finite-stage expectations are legitimate by bounded-prefix or proved exponential-tail estimates; localization and monotone convergence give finite expected total F reward until H. Since F pays genuine jump count, H is reached in finitely many jumps almost surely. Off-section starts first use (6). Thus the whole process reaches H with finite physical time, activity and exponential count occupation.

From h in finite H take one ordinary jump. There are finitely many successors, and their proved hitting reward is bounded by V<=2t^M. Thus the original chain's positive head-return excursions have finite F reward. The original trace on H is finite irreducible, because the raw chain is irreducible. Its return count has a geometric block bound. Closing those actual excursions yields a physical return to zero with finite expected F reward and positive finite mean time. Infinitely many returns include independent positive holding times at zero; their sum diverges, proving nonexplosion. The regenerative occupation formula proves (1).

An explicit, deliberately enormous bound avoids enumerating H. Let

    D=3k−2, J_del=6k−5, N_path=(2k+1)L,
    Q_col=(sum_i kappa_i)(L+J_del)^D,
    p_min=min_i kappa_i/Q_col,
    e_head=p_min^N_path.

The acquired deletion words give, from every head state, a path to zero of at most N_path jumps within the collar M<=L+J_del. Its actual probability is at least e_head. Hence the finite head trace hits zero within N_path trace steps with probability at least e_head. A head excursion has expected F reward at most

    B_H=(1+1/kappa_0)u^L+2t^(L+3).

A full positive return has expected F reward at most B_H[1+N_path/e_head]. Its mean physical length is at least 1/kappa_0, the initial holding mean at zero. Consequently

    E_pi F <= kappa_0 B_H[1+N_path/e_head].                    (19)

For rational inputs this is an acquired exact FACTORED expression. Fully expanding its powers can require enormous bit work, which is not performed or hidden. It is not a practical mixing estimate. No exponential moment of GLOBAL physical return time is claimed: the large zero-cells have arbitrarily slow exits, as the separate calibration proves.

**Physical return-tail consequence.** For each 1<u<t the same proof also bounds the ordinary zero-hitting reward by

    G_u(x)=E_x integral_0^tau_0 (1+q)u^M ds
           <=C_u+2t^M,                                      (20)

where C_u is the maximum of the finitely many zero-hitting rewards on H, bounded by the acquired trace estimate. Starting at zero, ordinary tau_0 is zero here. In particular E_x tau_0<=C_u+2t^M. Inductively suppose E_x tau_0^(p−1)<=C v^M for every nonzero state, for some v>1. Choose a new occupation contract with u>v. The strong Markov property, the identity T^p=p integral_0^T (T−s)^(p−1)ds and Tonelli's theorem give

    E_x tau_0^p <=pC E_x integral_0^tau_0 v^M ds
                 <=pC G_u(x)<=C' (t')^M.

Localization removes any initial integrability presumption. From zero, its initial Exp(kappa_0) holding followed by the fixed successor y1 proves that the POSITIVE return has every finite polynomial moment as well. Therefore its tail is bounded by C_p T^(−p) for every fixed p. The separate neutral-cell proof rules out every exponential physical return moment. Constants for this hierarchy have not been materialized by the stationary-reward compiler.

## 11. Structural content and actual frontier

The additional property used beyond coarse deletion geometry is the fixed nested raw source list: exact factorial divisibility, bounded source-index gaps, a finite maximal-source normalizer, and the anchor's +1/−k accounting. These identities pay the full physical clock and every outward repayment path. They are absent in the state-selected explosive corridor.

This is a complete global construction for the stated raw family, not just another face estimate. It goes beyond the admitted terminal-gap condition and beyond complex balance, with arbitrary deficiency and positive rates. A recognizer may certify this grammar and emit its proved data; all other lists remain UNKNOWN. General weak reversibility still requires acquiring an analogous global section/repayment mechanism without this ordered anchor pattern.
