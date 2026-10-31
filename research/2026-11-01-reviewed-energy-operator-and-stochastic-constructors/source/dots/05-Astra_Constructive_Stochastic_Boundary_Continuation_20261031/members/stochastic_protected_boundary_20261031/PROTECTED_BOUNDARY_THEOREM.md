# Protected-support activation and acquired finite-collar stability certificates

## Result first

A finite protected-token process can acquire the activation estimate that an infinite boundary fiber needs, without an independent-particle representation, a stationary fiber law, or coming down from infinity. Nonlinear reactions that cannot extinguish a positive service coordinate leave a protected token intact. Monomolecular conversion must coalesce tokens when its destination is already occupied; that detail is essential.

Combined with exact univariate tail bounds and a one-sided finite Dirichlet excess estimate, this yields a terminating raw-list certificate compiler for the architecture below. It allows arbitrary weakly reversible positive-count one-species subnetworks inside the service core, including non-pair cycles and jumps larger than one. Not every inactive phase needs nonlinear restoring reactions. The finite correction is checked on a whole finite-thickness collar, not just one boundary layer.

**Theorem.** For every network in Section1 and every rational T>1, the unbudgeted construction terminates with a positive normlike V and rational epsilon>0,C>=0 satisfying LV<=-epsilon V+C at every integer state. Every reachable class is nonexplosive and positive recurrent, and its invariant law has every finite exponential total-count moment. A single T certificate directly controls exponents below log T. The prototype has separate clock, polynomial-enumeration and finite-head budgets; a budget stop is UNKNOWN, not instability.

**Review status:** read the separately bound independent review. This proof does not inherit acceptance from earlier affine or cubic-only constructions. No general weak-reversibility theorem, historical novelty, efficient complete algorithm, stationary-product-form formula, or operational chemistry is claimed.

## 1. Raw architecture and what the finder actually acquires

Let the service species be Y_1,...,Y_m and the satellites Z_1,...,Z_s, with m,s>=1. The raw finder enumerates the service subset; the hub set H is derived from the nonzero star rows. Let I be its complement within the service subset. I may be empty.

The raw list is accepted only if:

1. The monomolecular service core on the complexes {0,Y_1,...,Y_m} is strongly connected on that entire vertex set. Write lambda_i,k_ij,d_i for immigration, conversion and death rates. Every hub h has d_h>0; inactive deaths may vanish.
2. The remaining service-changing reactions, apart from the stars below, have the form uY_i->vY_i for positive integers u,v, u!=v. For each service phase separately, the graph of these positive-count univariate reactions is weakly reversible. It may be empty and may have several linkage classes. A positive-count cycle such as Y_i->2Y_i->4Y_i->Y_i is allowed. These reactions may occur in hubs or inactive phases.
3. For every hub h and every satellite j, both 2Y_h->Y_h+Z_j and its reverse occur with positive rates alpha_hj,beta_hj. Every hub row is complete.
4. Every remaining reaction preserves each service count individually and total count. Such satellite rearrangements may have arbitrary finite molecularity. The complete raw reaction graph is weakly reversible.

All rates are positive exact rationals; null channels are discarded. No pivot, service partition, hub set, clock, tail cutoff, or head function is supplied as an oracle. The code is a trusted int/Fraction research constructor, not a hardened hostile-input parser. An independent verifier is a separate artifact with its own scope.

## 2. The protected-support comparison lemma

Here is the clock principle independently of the later tail construction.

Let X be a nonexplosive service count process containing a specified linear immigration/conversion/death subcore. Suppose every extra transition that decreases coordinate i leaves its resulting count at least1 whenever it fires. Equivalently for a mass-action reaction u->v, require v_i>=1 whenever u_i>v_i. Extra transitions can otherwise have arbitrary nonlinear rates and change several coordinates. This lemma does not assume those extra transitions have stationary laws.

Couple X to B in {0,1}^m with B<=X coordinatewise. For an immigration into i, set B_i=1. For a conversion i->j split its actual rate k_ij X_i into:

- protected rate k_ij B_i: perform the actual conversion and update B_i to0 and B_j to1;
- unprotected rate k_ij(X_i-B_i): perform the actual conversion and leave B unchanged.

If B_i=B_j=1, the protected event **erases the i-token and retains the j-token**. Suppressing that event would be wrong: if X_i=1, the actual conversion empties i. The stipulated update is coalescence, not exclusion.

For a death in i, similarly split d_i X_i into d_i B_i, which removes its token, and d_i(X_i-B_i), which does not. Every extra transition leaves B unchanged.

All split rates are nonnegative. An unprotected removal has X_i-B_i>=1, so it preserves B<=X. An extra removal leaves actual coordinate i at least1, so it also preserves dominance. Protected conversions and deaths preserve dominance directly. The X marginal has exactly its original rates, while the B marginal is an autonomous finite Markov chain with the listed linear token rates, independent of X. Nonexplosion of X makes the joint construction legitimate without accumulating unobserved events.

Start B at zero for any actual state. Let tau_H be first occupation of any hub by X and sigma_H first hub occupation by B. Pathwise tau_H<=sigma_H. Before sigma_H, B occupies only inactive coordinates, hence has exactly 2^|I| possible nonabsorbing states.

Construct its actual killed matrix Q_bin from the raw linear subcore, including coalescing conversions. Solve

    (-Q_bin)t=1.                                          (1)

The matrix is transient. From every token configuration, a finite positive-rate word from the strongly connected monomolecular graph reaches a hub, possibly using a death and then immigration through0. Other token events can be excluded during this finite word with positive probability. The finite chain therefore reaches the absorbing hub set almost surely with finite mean. In particular all entries of t are positive, as checked exactly.

The acquired uniform bound is

    sup_(x_H=0) E_x tau_H <= C_act:=t(0).                  (2)

It is t(0), not an assumed supremum over the infinite population fiber: for every initial X one restarts the coupling with B=0. The support-preserving condition holds for every extra positive-count univariate reaction in Section1. The standalone nonlinear core will be proved nonexplosive from its tail before (2) is used; there is no circular assumption about the full satellite process.

## 3. Exact exponential weights from the linear subcore

For i in I solve

    sum_j k_ij(tau_j-tau_i)-d_i tau_i=-1,     tau_h=0.

These are finite single-particle hitting equations for the linear subcore killed on H or death. They acquire weights, not a replacement model for the nonlinear core. Set

    L=max_h (1+sum_(i in I) k_hi tau_i)/d_h,
    v_i=L+tau_i, eta=(T-1)/L, q_i=1+eta v_i.

Then q_i>=T, q_h=T, and Qv<=-1 for the linear conversion/death matrix Q. Define

    delta=min_i eta/q_i,  alpha=max_h sum_j alpha_hj,
    D_death=max_i d_i/q_i, B_imm=sum_i lambda_i(q_i-1),
    c=min(1,delta/(4alpha)).

Define g(1)=1 and g(r+1)/g(r)=r/(r+c). For service total r>=1 put h0(y)=q^y g(r), and put h0(0)=1 as an auxiliary value. Since c<=1, g(r)>=1/r.

For r>=2, direct ratios give

    L_linear h0/h0 <=B_imm+2cD_death-delta r.              (3)

Conversions use q_j/q_i. Immigration uses q_i r/(r+c)<=q_i. Death uses q_i^(-1)(1+c/(r-1)), with extra contribution at most cD_death r/(r-1)<=2cD_death. The remaining weighted linear sum is sum_i eta y_i(Qv)_i/q_i<=-delta r.

## 4. Acquiring a bounded nonlinear contribution from raw univariate graphs

Let J=max(1,max|v-u|) over positive-count univariate reactions. Start with integer R_nl>=max(2,J+1). For each decreasing reaction uY_i->vY_i with d=u-v>0, increase R_nl until the exact inequality

    q_i^(-d) g(R_nl-d)/g(R_nl) <= (1+q_i^(-d))/2          (4)

holds. The left side is q_i^(-d) times a finite product of factors 1+c/k; it decreases with R_nl and tends to q_i^(-d)<1. Doubling therefore terminates. All ratio trials are recorded.

For every r>=R_nl, the quotient contribution of an increasing reaction is at most kappa(q_i^(v-u)-1)(y_i)_u. For a decreasing reaction, (4) bounds it above by kappa(q_i^(v-u)-1)(y_i)_u/2. Summing for phase i gives a fully acquired univariate polynomial

    P_i(n)=sum_(u<v) kappa(q_i^(v-u)-1)(n)_u
            +sum_(u>v) [kappa(q_i^(v-u)-1)/2](n)_u.       (5)

If the subnetwork is nonempty, P_i has negative leading coefficient. Indeed its largest complex M has an outgoing non-null edge by weak reversibility, every edge leaving M decreases, and no edge from a smaller source has degree M. The same argument applies when several positive linkage classes are present. This is the only graph fact needed here.

Expand P_i(n)=sum_(k=0)^M a_k n^k with a_M<0. Set A_plus=sum_(k<M)max(a_k,0). For n>=1,

    P_i(n)<=a_M n^M+A_plus n^(M-1).

Hence P_i(n)<=0 whenever n>=N_i:=max(1,ceil(A_plus/(-a_M))). Enumerate n=0,...,N_i-1 exactly and set M_i=max(0,max P_i(n)). No polynomial optimizer is assumed; this finite, possibly expensive enumeration is explicit. The implementation may decline it at its stated budget.

Let B_eff=B_imm+sum_i M_i. The actual nonlinear service core now satisfies

    L_core h0/h0 <=B_eff+2cD_death-delta r, r>=R_nl.       (6)

Since h0 is positive and normlike and the remaining service states are finite, (6) proves nonexplosion of the standalone core by the ordinary stopped Lyapunov argument. We can therefore apply the protected-token lemma and use the exact clock (2).

For V0=T^Z h0, stars have exact forward quotient alpha_hj y_h(y_h-1)c/(r-1) and reverse quotient -beta_hj y_h z_j c/(r+c). Consequently

    LV0/V0 <=B_eff+2cD_death-(delta-c alpha)r
              -c/(r+c)sum_(h,j) beta_hj y_h z_j.          (7)

Acquire epsilon_tail=delta/4 and R0>=R_nl so the constant/linear part is <=-epsilon_tail for all r>=R0.

## 5. Finite Dirichlet corrections and one-sided excess

For each R>=R0 define the finite service head F_R={y_H=0,r<R}. It has binomial(R+|I|-1,|I|) states, or one state if I is empty. Its satellite fiber remains unbounded.

Use the actual nonlinear core killed at exit from F_R, not a truncated reflecting surrogate. Solve

    (-Q_R)u_R=1+Q_RB h0.                                 (8)

This includes h0 at every actual exit, including exits that jump beyond r=R. The killed matrix is transient by (2) and u_R>0. Define V_R=T^Z u_R on F_R, V_R=V0 elsewhere. Stars vanish on the head, and neutral reactions preserve V; thus LV_R=-T^Z there exactly.

Put w_R=u_R-h0 on F_R and zero at exits. Then

    (-Q_R)w_R=f,       f=1+L_core h0.

Acquire K_force>=R_nl with

    delta K_force>=B_eff+2cD_death+1,
    T K_force/(K_force+c)>=1,
    T^K_force g(K_force)>=1.

For every r>=K_force, (6) gives f<=0. Enumerate every inactive service composition below K_force and set M=max(0,max f). The positive finite killed resolvent and (2) give

    w_R(y)<=E_plus:=M C_act                               (9)

uniformly over every head size and state. Only positive excess matters for leakage. A large negative correction is harmless and does not need an absolute-value estimate.

## 6. A finite-thickness collar and proof that its search terminates

Let p be the maximum of1 and the source molecularities of decreasing positive-count reactions in inactive phases. Let

    K_leak=max_(i in I)d_i
              +sum_(inactive decreasing reactions) kappa,

with absent terms zero. At any inactive state of total r>=1, the combined rate of core jumps entering a lower-total head is at most K_leak r^p. Each such entrance adds at most T^Z E_plus to the patched generator. Therefore

    LV_R/V_R <=-epsilon_tail
                   +K_leak E_plus r^p/[T^r g(r)]          (10)

throughout the inactive collar R<=r<R+J. Outside this collar, an inactive state cannot enter F_R in one jump. This is why merely checking r=R would be insufficient for jumps larger than one.

The actual search solves (8) at R0, evaluates the exact quotient for **every inactive composition at every integer level R,...,R+J-1**, and accepts only if all values are <=-epsilon_tail/2. On failure it doubles R and repeats, retaining the failed trial. The conservative sufficient witness is acquired by checking

    T^R g(R)>=2K_leak E_plus R^p/epsilon_tail,
    T R^(p+1)>=(R+c)(R+1)^p.                              (11)

The successive ratio of T^r g(r)/r^p is T[r/(r+c)][r/(r+1)]^p, an increasing product tending to T>1. Thus (11) eventually holds and then holds for all larger radii. Equation (10) proves that the unbudgeted exact-collar search terminates. The finite polynomial, clock and patch budgets remain separate implementation limitations, not omitted costs.

## 7. Active layers, full Foster bound, and moments

Every star preserves whether a hub is present. Every positive-count univariate reaction also preserves that phase's presence. Only a linear core reaction can remove the last hub; every core total jump has magnitude at most J. Thus the remaining potentially affected active states have total 1<=r<R+J, a finite set of service compositions.

For every such y the exact generator quotient is

    LV_R/V_R=H_y-sum_j a_yj z_j,
    a_yj=c/(r+c)sum_h beta_hj y_h>0.                       (12)

The computation of H_y uses the complete nonlinear core and its true head values. Complete hub rows guarantee each satellite slope is strictly positive. Exact integer satellite thresholds give a finite rational Foster C. With

    epsilon=min(epsilon_tail/2,min_(head)1/u_R),

the head, inactive collar, finite active layers and analytic tail exhaust all states and give LV_R<=-epsilon V_R+C.

V_R is positive and normlike: outside its finite service head it dominates T^(r+Z)/r; inside the head it is a positive coefficient times T^Z. Stopped Dynkin and finite sublevels prove full-process nonexplosion, including arbitrary-degree neutral satellite transitions. Weak reversibility supplies feasible return paths for every enabled reaction, so communicating classes are closed. The Foster bound yields classwise positive recurrence.

For stationary integration, stopped exponential Dynkin first gives P_tV<=aV+b, a=exp(-epsilon t)<1, b=C(1-a)/epsilon. Invariance and concavity of min(V,n) imply pi[min(V,n)-min(aV+b,n)]<=0. This integrand is bounded below by -b. Fatou therefore proves pi(V)<=C/epsilon without assuming that integral in advance. Repeating the terminating construction for rational T>exp(theta) gives every finite exponential total-count moment. The same classwise invariant law is used; neither costs nor constants are uniform in T.

## 8. Executed wider example

There are five species A,E,B,D,C. The linear core has 0->A at1/10; A->E, A->0, E->A, B->0 and D->0 at1; E->B and E->D at2. The nonlinear positive-count subnetwork is the cycle

    A->2A at1/100,  2A->4A at1/100,  4A->A at10.

There is no nonlinear restoring reaction on E. The satellite stars are 2B<->B+C at rates1,1 and 2D<->D+C at rates2,1. The raw scan finds S={A,E,B,D}, H={B,D}, I={A,E} after26 service-subset trials.

At T=2, the binary clock has four states 0,E,A,A+E, with exact hitting means24,3,14,3. Hence C_act=24, uniformly over arbitrary initial A,E populations. This does not depend on the nonlinear-cycle rates. A cubic-only coming-down theorem requiring restoring pairs on every inactive phase would not accept this network.

The acquired nonlinear-ratio radius is4 and J=3. The univariate polynomial has negative leading coefficient -2425/512 and exact global upper bound5/12 after12 integer checks. The finite head has R=4 and10 service states. All18 inactive collar states at levels4,5,6 pass; the largest quotient is -12049/7770. There are182 exact active service layers and1050 original full-generator challenges. The forcing support enumeration has15 states. These finite costs, exact rational coefficient sizes, epsilon and C are present in results.json.

A separate exact generator-coupling challenge checks1875 joint count/token states and20750 split event terms. It verifies the original-count marginal, autonomous binary marginal, and coordinatewise dominance. This is computational evidence in addition to the ordinary coupling proof, not a replacement for it.

The full network is not complex balanced: the linear linkage forces b=d=1/45>0, but the two star linkages demand c=b and c=2d. In a direction supported equally on B,C, their star linkage is maximal and has no descending edge, so the network is not strongly endotactic. These checks rule out particular easy explanations; they are not a historical priority search.

## 9. What was generalized, and what remains open

The clock comparison lemma applies to any already nonexplosive service process whose extra transitions cannot extinguish a positive coordinate. It is broader than the full stability theorem. This compiler acquires that standalone nonexplosion and the required exponential tail only for the explicitly recognized univariate-WR architecture. It does not assume an arbitrary useful tail, uniform return estimate, or compatible finite patch.

The coupling, finite killed resolvents, univariate polynomial bounds, and Foster tools are conventional stochastic-process machinery. Their exact acquisition and compatibility composition are the delivered mathematical construction. Direct hub deaths and complete satellite rows are still substantive restrictions; multiple partially covered satellite faces and general nonlinear cross-species service reactions remain unresolved. No general weak-reversibility conclusion, completeness over stable graphs, polynomial-time claim, mixing-rate advantage, historical novelty, or physical enabling claim is made.
