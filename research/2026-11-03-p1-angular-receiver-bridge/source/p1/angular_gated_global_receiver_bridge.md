# A core-exact, terminal-monotone angular receiver for the six-species C3/core process

**Scope.** All ten stochastic mass-action rates are arbitrary fixed positives. Full-process nonexplosion is accepted as the programme prerequisite. This note proves an algebraic receiving geometry, an unrestricted-ready-inventory generator region, high-return and large-residual preservation after a finite head enlargement, a ratio-free hot-majority stopped surplus using Sol's U1675 v2, a compatible entire low-low corner, and physical-time switching without counted-event exits. It does **not** prove positive recurrence of the full chain, and does not assume the unearned intermediate activation law. Its key new step is the *global* angular correction, not another unconnected potential.

## 1. Exact radial-angular decomposition, invariant under core

Write M=A+B+C+D+E+F, S=B+C+E+F, T=A+D, and r1=B-C,r2=E-F, t1=min(B,C),t2=min(E,F). Define

    psi=3(r1)_+ + 3(r2)_+ + w(-r1)_+ + w(-r2)_+
        + floor(t1/2)+floor(t2/2)+2(t1 mod2)+2(t2 mod2),

where w=a_work from Sol's raw high-workload construction, an integer >=4. Let O=(t1 mod2)+(t2 mod2). Exact integer arithmetic gives

    psi = S/4 + (11/4)[(r1)_+ +(r2)_+]
              +(w-1/4)[(-r1)_++(-r2)_+] +(3/2)O.       (1)

Consequently psi>=S/4; if H=(S-psi)_+>0, then 0<H<=3S/4 and the total absolute difference is less than 3S/11. Therefore t1+t2>4S/11, so at least one port has minority >=2S/11. All these quantities, including S,T,psi and H, are preserved EXACTLY by either core reaction.

Use Sol's proper high potential U=eta1*g1^2+eta2*g2^2+C(psi+c0)^2, with h_i=|r_i|+(3t_i+(t_i mod2))/2 and g_i=(anchor_i-h_i)_+. Choose eta ratio and finite s>=1 as in the original high-axis theorem, and write V=sU, gamma=sC, P=psi+c0.

Define the **angular gauge**

    R(x) = S*(S-psi)_+/(1+S+T),
    V_ang(x) = V(x)+(gamma/3)*R(x)^2.                    (2)

This is globally proper and quadratically bounded: R<=3S/4<=3psi, so 0<=V_ang-V<=3gamma psi^2<=3V. Crucially R=0 whenever psi>=S, including Sol's ratio-free positive-unpaired hot-majority cone and ALL its guarded paths for sufficiently small cold fraction. Near large balanced inventories at bounded anchors, R=S-psi+O(1), and

    V_ang = eta*g^2 + gamma[P^2+(S-psi)^2/3]+O(S).

For the leading homogeneous expression, when S>=psi, the identity

    psi^2+(S-psi)^2/3 = S^2/4 + (4/3)(psi-S/4)^2          (3)

means that the angular derivative vanishes exactly at the realizable balanced boundary psi=S/4, rather than imposing an O(S) artificial mismatch on a bounded redistribution defect. The shift c0 contributes only an O(1) angular derivative. This is a bridge in receiving geometry, not a claim that it gives negative drift at all balanced low faces.

## 2. Raw terminal monotonicity (an exact result)

For a terminal event in either port, S'=S-4, T'=T-3, psi'=psi-1. Thus H'=(H-3)_+. If H<=3, R'=0<=R. If H>3, S>=5, T>=3, and with d=S+T+1, d'=d-7,

    R-R' = [d(3S+4H-12)-7SH]/[d(d-7)].                (4)

The numerator is nonnegative. Since d>=S+4, H<=3S/4 and 3S+4H-12>0, it is at least

    (S+4)(3S+4H-12)-7SH
      =3S^2-48+(16-3S)H.

For S=5 this is positive. For S>=6 it is >=(3/4)S^2+12S-48>0. Hence **every enabled terminal weakly reduces R and R^2, regardless of rates or other inventories**. Both core directions preserve R and R^2 exactly. Since the source terminal also leaves every g_i=(a_i-h_i)_+ unchanged, we obtain the **GLOBAL exact terminal decrement**

    Delta_terminal V_ang <= -gamma*(2*(psi+c0)-1).       (4a)

This holds even on zero-anchor faces of the *other* port, at all population ratios, and without an auxiliary routing profile. (The full core contribution to V_ang need not vanish because core can change g_i; only the new angular term is core invariant.)

For every growth source 0,1,2 of either block, Delta S belongs to {1,2}, Delta T=1 and |Delta psi|<=b=w+1. The function S/(1+S+T) changes by at most 3/(1+S+T), while H_+ changes by at most b+2. Using H<=3S/4 gives

    |Delta R|<=L:=b+5,
    (Delta R^2)_+<=2LR+L^2
                      <=(3L/2)*S^2/(1+S+T)+L^2.       (5)

Thus for the complete actual generator, **angular core increments vanish, terminal increments are nonpositive, and only genuine growth channels can increase this correction**, with an explicit bounded-jump estimate. This is the reusable terminal-monotone, core-invariant mechanism.

## 3. High-anchor operation remains available for the new V_ang

Sol's original all-high proof gives, on each nonempty-hidden state with A,D above a finite original threshold,

    L V <= -(s/B0) P q_nc,  B0=alpha0+beta0,           (6)

where q_nc=G+Tserv is the sum of all eight block propensities, G comprises the six growth sources and Tserv the two terminal sources. On the joint axes, the fourth actual noncore-event stop has a fixed strictly negative original V margin after increasing the anchor head.

We prove that an enlarged finite high head N_ang suffices for (6) with half its margin for V_ang. Let S0 be large, K large, and split the raw states:

* **S<=S0.** Since A+D>=2N_ang, every one-step growth destination has S'<=S0+2 and R'^2<=C(S0)/(2N_ang)^2. Terminal/core angular increments are nonpositive. Therefore the added positive generator is <=gamma*C(S0)*G/(3N_ang^2); choose N_ang to absorb half the fixed old (s/B0)c0*q_nc margin.
* **S>S0, A+D>K S.** From (5), R<=3S/(4K), so angular growth contribution is at most (gamma/3)[(3L/2)S/K+L^2]G. First select K large and then S0 large, comparing P>=S/4, to absorb half the old (s/B0)P*q_nc margin, since G<=q_nc.
* **S>S0, A+D<=K S, H<=0.** R=0 and the one-step angular increase is at most (gamma/3)L^2G. Enlarge S0 to absorb it against the old -sP q_nc/B0.
* **S>S0, A+D<=K S, H>0.** By (1), some port has minority at least 2S/11. For both anchors>=N_ang, its genuine terminal intensity is >=c (N_ang)_3 S^4. Every terminal-ready port's complete growth/terminal ratio is <=C/(N_ang-2) by the exact factorial divisions, and an unready port (minority<=1) has total growth at most C_K S^3. Hence

        G/Tserv <= C/(N_ang-2)+C_K/[(N_ang)_3 S].       (7)

    Choose N_ang and S0 so the right-hand side is arbitrarily small; the angular positive part is at most (gamma/3)[(3L/2)S+L^2]G, paid by half the old negative margin.

These choices are nested but finite, depend only on the fixed raw rates and chosen w,C,c0, and do not impose a state-dependent external assumption. Thus for all nonempty-hidden all-high inputs with A,D>=N_ang,

    L V_ang <= -(s/(2B0)) P q_nc.                       (8)

On a joint axis, R(input)=0. Up to the fourth genuine noncore event, the total hidden inventory is at most eight, and A+D>=2N_ang-3. Every actual landing therefore adds at most O(gamma/N_ang^2) to the old output. Enlarge N_ang once more to preserve half the existing strictly negative four-event drift. Scaling V_ang by a further fixed positive constant if necessary pays both physical time and q_nc count on the full simultaneous-high return, in this ONE V_ang. No high boundary value was assumed. The proved exit remains at its actual low-anchor landing.

## 4. Full generator in balanced/ready states, with all physical endpoints

At a state with both h_i>=a_i+3 (here a_i=A,D), every one-jump neighbor, including every possible core donor, has g_i=0: growth raises h_i by >=0 while raising its anchor by1; a terminal lowers both by3; outgoing core lowers h_i by3 and incoming raises it by3. These identities are exact.

Exclude only the direct corner-receiving seam: define anchor-safe states as those with both anchors>=3, or one anchor<=2 and the other>=6. Then no enabled one-jump destination can enter the double-low corner {A,D<=2}.

Let P=psi+c0, b=w+1, L=b+5, gamma=sC and

    Cgrow=2b+2L+(b^2+L^2/3)/c0.                        (9)

On such a state, using the EXACT source list, Delta psi=-1 at each terminal, |Delta psi|<=b at growth, and the angular bound (5),

    L V_ang <=gamma*[Cgrow*P*G -(2P-1)*Tserv].        (10)

Consequently every anchor-safe state satisfying

    h_i>=a_i+3 for both ports,
    Tserv>=2*Cgrow*G,
    gamma*P>=3*(1+1/B0),                              (11)

has

    L V_ang <= -1-q_nc.                               (12)

This includes (A,D)=(3,3), B=C=E=F=n for every sufficiently large n, and a broad family of one-low/one-high configurations. No core jump was discarded: its increment in V_ang is exactly zero at the input because g_i are zero both before and after the jump and R is core invariant. The sector itself need NOT be invariant under core events; its first exit can be through a genuine core jump.

## 4a. A complete bounded-head balanced region with no individual g-margin premise

The algebra above permits a stronger uniform result. **Fix any finite head H>=3**. There is an actual finite S_H such that for all states

    3<=A,D<=H, S>=S_H, psi<S,

one has L V_ang<=-1-q_nc (and hence the same inequality for Vhat_ang, since no one-step landing can enter the double-low corner). There is no condition on individual h_i-a_i, no pair-ratio bound and no restriction on which port carries the balanced inventory.

Proof: psi<S implies a port j has minority t_j>=2S/11, so its genuine terminal T_j>=c_H S^4 for S large, while every growth propensity is at most C_H(1+S^2) since both anchors are bounded. Both anchors are >=3, hence **every core donor is also a genuine terminal donor**, and the exact raw ratio

    core_out_i / terminal_i
      <= kappa_ij*H/[kappa_i3*(a_i-1)*(a_i-2)] <=C_H

bounds total core activity by C_H*Tserv. The anchor term Q=sum eta_i g_i^2 has all one-jump increments bounded by C_H because g_i<=H; its terminal increments are exactly zero. The angular term has zero core contribution, nonpositive terminal contribution and growth contribution <=gamma*C_b(S+1)G. The psi-square term has terminal decrement -gamma(2P-1). Thus

    L V_ang <= -gamma(2P-1)*Tserv
                 +C_H*Tserv+C'_H(1+S)*G.

Using P>=S/4, Tserv>=c_H S^4 and G<=C_H(1+S^2), the right-hand side is eventually <=-1-q_nc uniformly in this entire bounded-head balanced region. This gives a kinetic **whole-phase** result, not a state catalogue, and it includes states with one port completely unready (g_i positive) so long as the other port carries sufficient balanced inventory and both anchors are terminal-capable. The zero-anchor interface is genuinely different because core can be disabled and no receiving drift is implied there.

## 5. The prior mixed-sign result is preserved after threshold enlargement

Preserve the original exact raw mixed-sign source-table theorem

    A,D>=3; |B-C|>=max(A+2,R1),
    |E-F|>=max(D+2,R2),  L psi<=-q_nc/4.

Both g_i vanish at the input and all one-jump neighbors, including core. Thus for P sufficiently large the original V part obeys L V<=-(gamma P/4)q_nc. Here the mixed-region hypothesis itself implies A+D<=|r1|+|r2|<=S, so no large-anchor split is needed. If H>0, one port has minority >=2S/11. With anchors>=3, its terminal is >=c S^4. For any other ready port with minority>=sqrt(S), exact factorial ratios make its own growth/terminal ratio O(S^-1/2). If the other port has minority<sqrt(S), its growth is O_K(S^(7/2)), dominated by that large terminal. Hence G/Tserv=O_K(S^-1/2). If H<=0, R=0 and the first growth correction is O(gamma G), absorbed by P>>1. Increasing R1,R2 makes S large enough for these inequalities and proves the same physical/count Foster inequality with V_ang on the entire enlarged mixed-sign region. Since both anchors>=3, no one-step neighbor enters the corner corrector.

## 6. Ratio-free U1675 v2 supplies arbitrarily large V_ang-native surplus

The governing v2 source is HOT_MAJORITY_COMMON_CLEANUP.md, referenced by knowledge unit U1675 v0002. Its progress f(a,c), failure-hazard comparison and p^F subsolution earn a success probability delta_H>0 independent of the ratio of positive unpaired populations. The cleanup count is at most N_H+1, the initial anchors A,D<=H stay under a fixed head during cleanup, and all failure outputs are genuine. Conditional on success, the guarded delayed drain yields at least cK/2 mean good deletions by executing O(K(q+1)) physical trials, as long as q=C+F<=eps*n and n=min(B-C,E-F) is large. The unconditional mean satisfies E[D]>=delta_H*cK/2.

For EVERY prescribed Gamma>0 and fixed finite initial head H, first choose K sufficiently large. Then choose eps sufficiently small, and finally n0 sufficiently large. Along the full actual cleanup and drain, the positive residuals remain >=n/2, cold count remains <=eps*n+O_H(1), and the anchors are bounded by a fixed head. Consequently g1=g2=0 and psi>=S on EVERY visited physical state; R=0 identically. Thus V_ang=V along the entire path and every output, with no angular receiving error whatsoever.

Each guarded good deletion lowers psi by exactly3, every neutral completed activation leaves psi unchanged, and the cleanup and last interruption create a pathwise bounded psi error |xi|<=b_H. Writing P=psi_in+c0,

    psi_out+c0=P+xi-3D,
    E[D]>=delta_H*cK/2,
    E[time+J_nc]<=C_H+C K(q+1),
    D<=n/4+1.

Since P>=3(r1+r2), and M=r1+r2+2q+A+D<=r1+r2+2eps*n+2H, P is uniformly comparable **from below** to M without any upper ratio restriction. The negative term -6P*E D in the exact squared expansion can be made at least Gamma*(1+M), with the fixed cleanup errors and actual time/count cost absorbed by the K,eps,n0 sequence. Shrinking eps additionally ensures

    E[time+J_nc+V_ang(out)] <= V_ang(in)-Gamma*(1+M_in),
    M_out<=2(1+M_in) pathwise,                            (13)

for ALL ratio-free U1675 v2 inputs. This is not inferred from Z^2 by comparability; the good deletion's exact -3 psi is used.

## 7. Exact double-low corner and corrected receiving constant

On C0={A,D<=2}, stop at first anchor 3. Terminals are impossible before it, at most five noncore reactions occur and mean physical duration <=5/B0. Define

    F0_ang(x)=E_x[time+J_nc+V_ang(X_exit)], x in C0.

Every core step preserves S,T,psi,R, and g_i^2 remains bounded by a constant while anchors<=3. Hence the five noncore events give an acquired finite K0 such that

    |F0_ang(x)-V_ang(x)|<=K0(1+M(x)).                  (14)

F0_ang is proper and finite and L F0_ang=-1-q_nc on all C0. Define Vhat_ang=F0_ang on C0 and V_ang elsewhere. High-region first exit from anchors>=N_ang>=6 cannot land in C0, so its exact law is unaffected; the mixed-sign and anchor-safe sectors also have no corner one-jump endpoint.

For each ratio-free positive-unpaired input, choose the Gamma from (13) with Gamma>=4K0+1. The pathwise M_out<=2(1+M_in) yields

    K0(1+M_out)+K0(1+M_in)<=4K0(1+M_in).

Thus (13) receives the TRUE Vhat_ang values at input and output with coefficient one. This corrects the old Gamma>=3K0 constant and removes L entirely.

## 8. Time-charged switching lemma: core exits do not require noncore count

Let a nonexplosive CTMC on a countable state space admit a nonnegative proper receiver F and a countable menu of actual stopping operations on domains D_i with

    E_x[tau_i + N_nc(tau_i)-N_nc(0)+F(X_tau_i)]<=F(x).

Assume each stopped episode is a.s. finite and contains **at least one genuine physical reaction**, possibly a core reaction with zero counted noncore increment. Choose a deterministic priority among all eligible policies. Reapply a policy at each actual endpoint in the union G=union D_i; stop at the first episode endpoint outside G. Telescoping gives E[total time+total noncore count+F(final)]<=F(start). Indeed the partial accumulated physical times have uniformly bounded expectations. If there were infinitely many episodes with infinite total time, Fatou contradicts that bound. If their total time were finite, each has at least one genuine reaction, contradicting the accepted nonexplosion. Hence only finitely many episodes occur a.s.; no expected bound on **core event count** is necessary. The original count-charged fusion lemma remains true but is unnecessarily restrictive for core-exit boundaries.

Apply this lemma with F=Vhat_ang and the high-region exit, C0 exit, enlarged mixed-sign first exit, ratio-free v2 cleanup/drain stops with Gamma chosen to pay (14), the anchor-safe dominance region (11) first exit, and each fixed-head whole-balanced region in section 4a. This gives a genuine **one-receiver, coefficient-one, expected-physical-time return to the complement** of their union. It is not the first physical exit: a stopped episode may temporarily leave that union and continue until its actual prescribed endpoint. The complement is still unbounded, so this does not establish a finite-set return or full positive recurrence.

## 9. Live gap and a falsifiable next operation

The new receiver is radially substantial on balanced cold states, exactly unchanged on the ratio-free hot cone, and compatible with every all-high anchor ratio. The old U-versus-W leading quadratic mismatch is avoided by using the same angularly gated function across all covered operations. Its core and terminal contributions obey exact sign identities, not favorable presumed rate constants.

The remaining unbounded complement contains bounded-anchor balanced normal cells and unsafe (one anchor<=2, other 3..5) terminal-to-corner landings, plus mixed activation traces without the source0/source1/2 repayment law.

An **exact low-axis countercheck** fixes the scope. At x_n=(0,n,n,0,n,n) with n positive and even, S=4n, psi=n and T=0. Only source0 of either block is enabled, at aggregate rate B0. After either source0, S=4n+1, psi=n+3,T=1 and all g_i remain zero. With gamma=sC, the single-source V_ang increment divided by gamma is

    (n+3+c0)^2-(n+c0)^2
       + (1/3){[(4n+1)(3n-2)/(4n+3)]^2 - [12n^2/(4n+1)]^2}.

Its exact asymptotic expansion is n/2+6*c0+805/48+O(1/n), so

    L V_ang(x_n)=B0*gamma*(n/2+O(1))>0.

The corner Green corrector, not a fictitious pointwise source0 sign, receives this state. This positive drift is consistent with recurrence and proves that the angular gauge itself does not replace the necessary multi-step neutral-word completion. It also shows precisely why the remaining problem is an actual stopped-law sign, not mere algebraic regularization. At A=D=0 with B=C=E=F=n, a clean block word returns S,psi unchanged; completed abnormal words can change the angular variable. A *first-unexpected-source* stop still has unpaid phase loans and cannot be declared inward from an output-moment bound. The next required actual operation is a **source-completed, multi-defect renewal** that pays full residence and the new angular receiver at its genuinely returned phase, including overlap/core transfers. Its missing sign is not assumed here.

There is no theorem yet that arbitrary weakly reversible networks have this angular geometry; the reusable result is the precise combination of a terminal-monotone core-invariant angular ratio and time-charged actual-policy fusion. Full six-species positive recurrence is not claimed.

## 10. Exact sources

- Sol: PROPER_HIGH_ANCHOR_RECEIVER.md, JOINT_AXIS_FOUR_EVENT_THEOREM.md, HIGH_REGION_ELIMINATION.md, commit 487bfb76526a4218c71990cd32dda8e0a52478c7.
- Sol: HOT_MAJORITY_COMMON_CLEANUP.md, knowledge unit U1675 v0002, commit 0b4666b8278ea5bf7e36253f68006d32dbcaa5ea. Earlier comparable-population service proof is preserved only in its original scope.
- Sol: GLOBAL_SERVICE_RECEIVER.md, commit 23d0ada35f0340d1460403d23503620e3686c2d0; retained as an independent service comparator, not imported into Vhat_ang by an unjustified quadratic ratio.
- Original previous complete common-V receiver fusion: global_receiver_fusion_positive_cone.md; previous successful high/mixed positive-cone operations preserved.
- Reproducible finite checks: verify_angular_receiver.py. Finite checks validate identities on tested physical states; they do not certify the uniform all-rate quantifiers.
