# Acquired nonlinear boundary activation and terminating Dirichlet sewing

## Result and scope

The finite-head/tail compatibility mechanism does not require an independent-particle environment. This construction adds genuinely nonlinear service dynamics, acquires a uniform activation clock by a bounded return-time drift and an exact killed finite chain, and then proves that the actual Dirichlet patch/fringe search terminates. An ordinary finite killed-chain solution is not assumed globally compatible: the first executed patch fails exactly.

**Theorem.** For the raw architecture below, the unbudgeted algorithm, for each rational T>1, terminates with a positive normlike V and exact rational epsilon>0,C>=0 such that LV<=-epsilon V+C on every integer state. Every reachable class of the stochastic mass-action chain is nonexplosive and positive recurrent, and its invariant law has all finite exponential total-count moments. A fixed computed T directly certifies only exponents below log T. The implementation has separate finite activation-clock and finite patch budgets and can return UNKNOWN.

This is a restricted raw-network theorem, not a general weak-reversibility theorem. Historical novelty is not claimed. At authorship the independent review remains a separate required receipt. No acceptance is inherited from earlier affine-core packages. All reaction notation describes abstract Markov counts, not operational chemistry.

## 1. Raw recognized architecture

The finite raw list has positive exact rational rates. The finder enumerates a nonempty service subset S, a nonempty satellite complement, and derives the active hubs H from the listed star channels; let I=S\H. The following conditions are checked, not supplied as an oracle.

1. A monomolecular service core on {0,Y_1,...,Y_m} has a strongly connected graph on that whole set. Its rates are lambda_i for immigration, k_ij for conversion, and d_i for direct death. Every hub has d_h>0; inactive deaths may be zero or positive.
2. I is nonempty. For every inactive i, both nonlinear reactions 2Y_i->3Y_i and 3Y_i->2Y_i have positive rates kappa_i,mu_i. These are the only extra service reactions. No such pair is assigned to a hub in this version.
3. For every hub h and every satellite j, both channels 2Y_h->Y_h+Z_j and its reverse have positive rates alpha_hj,beta_hj. Hub rows are complete.
4. Every remaining reaction preserves each service count and total count individually; arbitrary finite-order satellite rearrangements are allowed. The complete reaction graph is weakly reversible.

Null channels are discarded. The constructor is a trusted int/Fraction research API, not a hardened hostile-input parser. Its output is not itself an independent verification receipt.

## 2. Acquiring the exponential weights

Let r=sum_i y_i and Z=sum_j z_j. For inactive phases solve the finite single-particle equations of the **linear subcore only**:

    sum_j k_ij(t_j-t_i)-d_i t_i=-1,  i in I;        t_h=0.

The linear subcore is transient when killed at a hub or death. Set

    L=max_h (1+sum_(i in I) k_hi t_i)/d_h,
    v_i=L+t_i, eta=(T-1)/L, q_i=1+eta v_i.

All q_i>=T and q_h=T. If Q is the linear conversion/death matrix, then Qv<=-1. Define

    delta=min_i eta/q_i,
    alpha=max_h sum_j alpha_hj,
    D=max_i d_i/q_i,
    B=sum_i lambda_i(q_i-1),
    c=min(1,delta/(4alpha)).

Define g(1)=1 and g(r+1)/g(r)=r/(r+c). Put h0(y)=q^y g(r) for r>=1 and h0(0)=1. This auxiliary zero value is replaced in the final finite head. Because c<=1, g(r)>=1/r.

For r>=2, the linear-core quotient satisfies

    L_linear h0/h0 <= B+2cD-delta r.                      (1)

Indeed conversions give q_j/q_i, immigration gives q_i r/(r+c)<=q_i, and death gives q_i^(-1)(1+c/(r-1)). The uncorrected linear sum is sum_i eta y_i(Qv)_i/q_i<=-delta r; the death-ratio correction is at most cD r/(r-1)<=2cD.

No stationary law of either the nonlinear or the linear core is used. The linear equations acquire weights, not a replacement dynamics for the actual core.

## 3. Acquiring a nonlinear core tail bound

Choose

    R_nl>=2,    R_nl>=1+2c/(min_i q_i-1).

For r>=R_nl, the i-th inactive nonlinear pair contributes at most

    A_i (y_i)_2 - B_i (y_i)_3,
    A_i=kappa_i(q_i-1),  B_i=mu_i(q_i-1)/(2q_i)>0.          (2)

The forward quotient is at most q_i-1. The reverse quotient is
q_i^(-1)(1+c/(r-1))-1<=-(q_i-1)/(2q_i). Here (n)_k is the falling factorial.

For integer n>=ceil(2+A_i/B_i), the polynomial A_i(n)_2-B_i(n)_3 is nonpositive. Enumerating the finitely many smaller nonnegative n acquires its global upper bound M_i>=0. Let B_eff=B+sum_i M_i. Thus the **actual nonlinear core** satisfies

    L_core h0/h0 <= B_eff+2cD-delta r,  r>=R_nl.           (3)

The standalone core is nonexplosive: h0 is normlike and positive, (3) bounds its drift above outside a finite set, and its generator on the remaining finite service states is finite. The usual stopped normlike-Lyapunov argument proves this independently of the satellite process and of the activation clock below.

For V0=T^Z h0, the stars have exactly the same useful ratios as before:

    forward_hj = alpha_hj y_h(y_h-1)c/(r-1),
    reverse_hj = -beta_hj y_h z_j c/(r+c).

Therefore, for r>=R_nl,

    LV0/V0 <= B_eff+2cD-(delta-c alpha)r
              -c/(r+c) sum_(h,j) beta_hj y_h z_j.         (4)

Acquire epsilon_tail=delta/4 and integer R0>=R_nl such that the constant/linear part of (4) is <=-epsilon_tail for r>=R0.

## 4. A nonlinear uniform activation clock, acquired from raw reactions

The previous fresh-immigrant lineage argument is **not valid here**: a cubic death can remove particles at a population-dependent rate. It is replaced as follows.

Let ell=|I|>=1, Lambda=sum_i lambda_i, kappa_max=max_(i in I) kappa_i, and mu_min=min_(i in I) mu_i>0. Consider the actual standalone service core until first hub activation. At a hub-empty state all service particles are inactive. Use the bounded function

    W(y)=r/(r+1),       0<=W<1.

Conversions do not change W; deaths give nonpositive contributions. For r>=6ell^2,

    sum_i(y_i)_3 >= r^3/ell^2-3r^2 >= r^3/(2ell^2).

This follows from sum y_i^3>=r^3/ell^2 and sum y_i^2<=r^2. The exact +1 and -1 differences of W are 1/[(r+1)(r+2)] and -1/[r(r+1)]. Consequently

    L_core W <= Lambda+kappa_max-mu_min r/(4ell^2).       (5)

Choose integer

    K_clock>=max(2,6ell^2,4ell^2(Lambda+kappa_max+1)/mu_min).

Then LW<=-1 at every hub-empty state with r>=K_clock. Stopping the already nonexplosive standalone core at either first hub activation or entry to

    F_clock={y_H=0, r<K_clock}

and localizing if necessary gives expected stopping time at most1, uniformly in its initial state outside F_clock. This uses bounded W and ordinary stopped Dynkin, not a stationary distribution or a hidden return-time estimate.

Acquire the actual finite generator Q_clock killed on leaving F_clock. For each y in F_clock solve

    (-Q_clock)t=1,
    (-Q_clock)p=b_H,                                     (6)

where b_H(y) is the actual total rate of exits that activate a hub. Thus t_y is the exit mean and p_y is the probability that this exit activates a hub, rather than merely reaching r=K_clock. Both systems are exact rational.

The matrix is transient and p_min=min_y p_y>0. To see this without assuming a favorable solution, use the strongly connected monomolecular raw graph. From any nonzero inactive state, an existing particle can follow a simple conversion/death path to zero, then a newly immigrated particle can follow a path to a hub. This prescribed finite event word never needs service total above its initial r (except from r=0, where it needs only1). It therefore stays inside F_clock until its final hub activation. Competing nonlinear events have finite rates at the finitely many states of this word, so its probability is positive. Finite-state reasoning gives transience and strictly positive activation probability for every starting state; the program nevertheless checks the solved inequalities exactly.

After an unsuccessful finite-head exit, (5) bounds the expected time until return to F_clock or activation by1. Repeated strong Markov cycles therefore give the acquired uniform bound

    sup_(y_H=0) E_y tau_H <= C_act=(1+t_max)/p_min.        (7)

One rigorous derivation truncates the number of cycles: every cycle has conditional success probability at least p_min and mean internal time at most t_max, with intervening expected return time at most1. Summing the geometric tail gives (7), without presupposing that the full activation expectation is finite.

The clock is computed before the compatibility search. A separate clock-state budget may return UNKNOWN; it is not suppressed because the later patch happens to be small.

## 5. Exact heads and a uniform one-sided excess bound

For any R>=R0 let F_R={y_H=0,r<R}. Solve the actual nonlinear finite Dirichlet problem

    (-Q_R)u_R=1+Q_RB h0.                                 (8)

The killed matrix is transient by (7), and u_R>0. Define V_R=T^Z u_R on F_R and V_R=V0 elsewhere. On the head all stars vanish, all neutral reactions preserve V, and the exact generator satisfies LV_R=-T^Z.

Let w_R=u_R-h0 inside the head and zero at its exits. Then

    (-Q_R)w_R=f,     f=1+L_core h0.

Acquire a finite forcing radius K_force>=R_nl satisfying

    delta K_force>=B_eff+2cD+1,
    T K_force/(K_force+c)>=1,
    T^K_force g(K_force)>=1.

Beyond it, (3) gives f<=0. Enumerate every inactive state below it and acquire M=max(0,max f). Positivity of the finite killed resolvent and (7) imply the bound

    w_R(y)<= E_plus:=M C_act                              (9)

simultaneously for every head size. Negative correction values require no control: only positive incoming leakage can spoil the tail. All quantities, including the finite forcing enumeration, are paid for and recorded.

## 6. Polynomial fringe leakage and terminating compatibility search

Only inactive states at r=R can enter F_R from its inactive complement. The relevant entrances are linear deaths and cubic 3Y_i->2Y_i channels. At such a state the additional generator caused by the patch is bounded above by

    T^Z E_plus [d_I R+mu_max R^3]
       <= T^Z E_plus L_leak R^3,                         (10)

where d_I=max_(i in I)d_i, mu_max=max_(i in I)mu_i and L_leak=d_I+mu_max. Hence

    LV_R/V_R <= -epsilon_tail
                  +E_plus L_leak R^3/[T^R g(R)].         (11)

The added term tends to zero. The actual search starts at R0, solves (8), and checks the exact quotient on **every** inactive composition with r=R. It accepts only if all are <=-epsilon_tail/2; otherwise it doubles R and repeats. This terminates unbudgeted by (11). A declared finite head-state budget can stop the search with UNKNOWN and must retain the failed prior trials.

The recorded conservative scalar witness checks

    T^R g(R)>=2L_leak E_plus R^3/epsilon_tail,
    T R^4 >=(R+c)(R+1)^3.                                (12)

The second inequality makes T^r g(r)/r^3 nondecreasing for all r>=R: its successive ratio is T[r/(r+c)][r/(r+1)]^3, whose factors increase with r. Both inequalities eventually hold. This scalar witness is not substituted for the actual finite-head search and does not hide its costs.

## 7. Remaining states and probabilistic conclusion

Stars never change whether a given hub is absent: their forward reaction needs two hub particles and leaves at least one, and the reverse needs one. Thus no star enters the hub-empty head. Added nonlinear inactive reactions do not change any hub count. Every core reaction changes total service count by at most one.

The only remaining patch-affected states are the finitely many active service configurations with 1<=r<=R. For each such y, exact algebra gives

    LV_R/V_R=H_y-sum_j a_yj z_j,
    a_yj=c/(r+c) sum_h beta_hj y_h>0.                     (13)

The exact H_y includes the full nonlinear core, not merely its affine subcore. Every satellite slope is positive by complete hub rows. Finite integer satellite thresholds and a rational Foster C are therefore acquired directly. Set epsilon=min(epsilon_tail/2,min_(head)1/u_R). This proves the global inequality LV_R<=-epsilon V_R+C by four exhaustive regions: head, inactive fringe, finite active service layers, and analytic tail.

V_R is positive and normlike. In the tail it dominates T^N/r, and the finite service head has positive coefficients times T^Z. Stopped Dynkin plus finite sublevels yields nonexplosion of the **full** process, even with arbitrary-degree neutral satellite reactions. Finite-set hitting plus weak-reversibility return paths gives classwise positive recurrence.

The stationary moment argument does not assume integrability of V. Stopped exponential Dynkin gives P_t V<=aV+b, with a=exp(-epsilon t)<1 and b=C(1-a)/epsilon. Invariance and concavity of min(V,n), followed by Fatou with the integrand bounded below by -b, give pi(V)<=C/epsilon. For each desired theta, repeat the terminating construction with rational T>exp(theta); since V dominates exp(theta N) up to a finite factor, the invariant law has that moment. There is no uniform computational cost or uniform moment constant in theta.

## 8. Executed nonlinear example and a real failed first patch

Species are A,B,D,C. The monomolecular core is

    0->A at1/10; A->B, A->D, A->0, B->0, D->0 at1.

The inactive restoring pair is 2A->3A at1/10 and 3A->2A at10. Complete satellite rows are

    2B <-> B+C at rates1,1;
    2D <-> D+C at rates2,1.

The raw scan, without supplied service/hub roles, finds S={A,B,D}, H={B,D}, I={A} after11 partition trials. At T=2 the acquired values include q=(7/3,2,2), c=3/56. The nonlinear tail maximum for the A pair is4/15. The activation clock solves two actual6-state systems, obtaining

    p_min=13324287823300/13370018636953,
    t_max=204966018318800/13370018636953,
    C_act=218336036955753/13324287823300.

The first compatibility head has R=2 and2 service states. Its exactly solved correction has positive inactive-fringe quotient

    2775046/4141725 >0

at service state2A, for **every** satellite population. A valid finite Dirichlet solve therefore is not yet a global stability certificate. Doubling to R=4 yields a4-state patch; its inactive fringe quotient is

    -58285045547056322143/311733653035701120.

There are30 active service layers and420 original exact state challenges. epsilon=3/56. Both the failed2-state and successful4-state systems are charged (20 matrix entries), separately from the6-state clock and finite forcing enumeration.

This example is not complex balanced: the monomolecular linkage forces a=b=d=1/30, whereas its restoring pair forces a=1/100; the two star linkages also require c=b and c=2d. A Poisson-product decomposition cannot simply be assumed. It is four-species and does not follow from the announced two-species result. In direction supported on {B,C} with equal positive weights, the B-star linkage lies entirely at the maximal source tier and has no descending edge, so the network is not strongly endotactic. No general novelty inference follows from these comparisons.

## 9. Scope of the mechanism and conventional comparators

Bounded Lyapunov return estimates, finite killed resolvents, geometric trial arguments, and Foster theory are conventional tools. Their acquired composition is the present mechanism: a nonlinear raw core yields its own uniform activation bound; finite positive forcing yields a uniform one-sided correction bound; polynomial incoming rates are then beaten by the exact exponential tail, proving termination of the compatibility search. A useful activation clock or compatible patch is not a premise.

The construction is not complete for arbitrary nonlinear cores, arbitrary missing-hub geometries, or stable reaction networks. It retains direct hub deaths and complete hub rows. The special independent-particle assumption is removed, but the chosen inactive restoring pairs are a substantive structural restriction. The coarse clock radius can be very expensive in several inactive dimensions, rational bit growth is charged, and default budgets can decline perfectly stable examples. No polynomial-time claim, general WR resolution, operational capability, or historical priority claim is made.
