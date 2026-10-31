# A terminating boundary/tail compatibility search from one-sided Dirichlet excess

## Result first, and the new obstruction actually crossed

The earlier phase-head construction assumed that inactive service phases could not die. Without that guard, the first finite killed-head correction can fix the extinction face and still create **positive drift on an unbounded inactive fringe**. The executed example below exhibits this failure exactly.

The new construction removes the guard by acquiring a uniform *positive excess* bound for every finite Dirichlet correction, independently of head size. A raw immigration/conversion path supplies a uniform first-activation clock; no stationary distribution, fiber mixing estimate, favorable pivot, or compatible head function is an input. The positive correction can grow the incoming fringe drift only linearly, while the explicitly acquired tail value grows exponentially. This proves termination of a search that solves an actual finite head and verifies every inactive fringe inequality before accepting it.

**Theorem.** For the raw network architecture in Section1, every reachable class is nonexplosive and positive recurrent, and its invariant law has all finite exponential total-count moments. For any exact rational T>1, the unbudgeted finite search below terminates and returns an exact rational global Foster certificate. This is completeness within the stated recognized architecture, not completeness for stable networks or for weak reversibility. The default implementation has an explicit finite-head budget and may return UNKNOWN before completion.

**Status at authorship:** mathematical derivation and exact executed construction; independent whole-review binding must be read separately. No acceptance is inherited from the previously reviewed, narrower no-inactive-death theorem. No novelty, general weak-reversibility solution, operational chemistry, or practical mixing speed is claimed.

## 1. Raw-list architecture

There is an acquired service subset S={Y_1,...,Y_m}, at least one satellite Z_j, and an acquired nonempty active hub subset H of S. Write I=S\H, service count r=sum_i y_i, satellite total Z=sum_j z_j, and total N=r+Z.

- The service core is monomolecular on {0,Y_1,...,Y_m}, with positive rates on its listed edges, and its graph is strongly connected on that whole vertex set. Let lambda_i, k_ij, and d_i be its immigration, conversion and death rates, with absent rates zero.
- Every hub h in H has a positive direct death d_h>0. **Inactive deaths d_i>=0 are now allowed.**
- For every hub h and every satellite j, both exact star channels 2Y_h->Y_h+Z_j and its reverse are present, with positive rates alpha_hj,beta_hj. All hub rows are complete.
- Any remaining reaction preserves each service coordinate individually and total N. It may have arbitrary finite molecularity and rate.
- The entire reaction graph is checked weakly reversible.

The program enumerates finite service subsets and checks every raw reaction. Neither S nor H is supplied. Rejection means no certificate from this architecture, not instability. The core's strong connectivity implies each single-particle service phase can reach a death, and at least one raw immigration/conversion path reaches H without passing through death.

## 2. Acquired exponential weights and rational tail

The first-hitting equations must be revised when inactive deaths are present. Set t_h=0 for h in H, and solve

    sum_j k_ij(t_j-t_i)-d_i t_i=-1,      i in I.                 (1)

This is the finite absorption-time system for a single inactive service particle killed on H **or death**. Its matrix is transient. It is not an assertion that every initial particle eventually reaches a hub.

Acquire

    L=max_h [1+sum_(i in I) k_hi t_i]/d_h,
    v_h=L,       v_i=L+t_i.

Then the full single-particle conversion/death matrix Q satisfies

    (Qv)_i=-1-d_i L<=-1,      i in I,
    (Qv)_h=sum_(i in I)k_hi t_i-d_h L<=-1.                     (2)

For rational T>1 set eta=(T-1)/L and q_i=1+eta v_i. All hub values are T and every q_i>=T. Each satellite receives weight T. Define

    delta=min_i eta/q_i>0,
    alpha=max_h sum_j alpha_hj,
    D=max_i d_i/q_i,
    B=sum_i lambda_i(q_i-1).

Choose rational 0<c<=1 with c alpha<=delta/2. The implementation takes min(1,delta/(4alpha)). Set g(1)=1 and

    g(r+1)/g(r)=r/(r+c),       r>=1.                            (3)

For r>=1 define h_0(y)=q^y g(r), and define the auxiliary value h_0(0)=1. This value at zero is used to measure the correction; the final function replaces it by the acquired finite-head solution.

The exact core quotient and star estimates from the finite product ratios yield, for r>=2,

    L_core h_0/h_0 <=B+2cD-delta r,                            (4)
    L V_0/V_0 <=B+2cD-(delta-c alpha)r
                -[c/(r+c)]sum_(h,j) beta_hj y_h z_j,           (5)

where V_0=T^Z h_0. These hold uniformly in all service compositions. Core conversion weights use Qq+d=eta Qv; deaths contribute at most2cD beyond that weighted drift. Forward stars contribute at most c alpha r, while reverse stars have the displayed exact negative coefficient. Neutral reactions contribute zero.

Pick epsilon_tail>0 and integer R_0>=2 such that

    B+2cD-(delta-c alpha)R_0<=-epsilon_tail.                    (6)

The code takes epsilon_tail=delta/4 and an exact ceiling. These computations contain no stationary law or asymptotic mixing premise.

## 3. Acquired uniform activation clock

Choose an actual directed simple core path

    0 -> Y_i0 -> Y_i1 -> ... -> Y_iell in H,

with no earlier hub. Its first edge is a positive immigration rate lambda_i0; its remaining edges are conversions between service phases. Such a path is found by finite graph search. For each pre-hub phase i, let a_i=sum_j k_ij+d_i be its total single-particle departure rate. The event that a newly immigrated particle follows each specified conversion as its next event, and that each holding time is at most1/a_i, has probability at least

    p=product_edges k_ij/(2a_i)>0,                             (7)

and reaches H within

    D_path=sum_pre-hub phases 1/a_i.                           (8)

Indeed each required event has probability (k_ij/a_i)(1-exp(-1))>=k_ij/(2a_i). A direct immigration into H has p=1,D_path=0.

For the autonomous monomolecular core, immigrant lineages are independent. Mark immigrants using the event just described. Their successful arrival process has intensity at least lambda_i0 p; the first successful immigrant activates a hub within D_path after its arrival. Extra initial particles can only make first activation earlier. Thus for every hub-empty initial service state,

    E_y tau_H <= C_act:=D_path+1/(lambda_i0 p).                  (9)

All terms are acquired rational bounds. This is ordinary Poisson thinning and finite path analysis, not a mixing theorem. It is applied to the standalone linear core (which is independently nonexplosive), so it does not assume nonexplosion of the full reaction network. Before hub activation, star channels are disabled and neutral channels do not affect service coordinates.

## 4. Finite Dirichlet heads and the one-sided excess lemma

For any R>=R_0 let

    F_R={y_H=0, r<R}.

This is finite, of size binomial(R+|I|-1,|I|), or1 if I is empty. The satellite population remains unbounded. Let Q_R be the actual core generator killed when leaving F_R, and let Q_RB be its exit rates. Exit states are active or have r=R. The finite killed chain is transient: a raw immigration/conversion word reaches H with positive probability, and finite irreducible-accessibility reasoning or (9) bounds its exit time.

Acquire the positive solution

    (-Q_R)u_R = 1+Q_RB h_0.                                   (10)

Define V_R=T^Z u_R(y) on F_R and V_R=V_0 elsewhere. The actual boundary values h_0 at exits are included in (10). On F_R,

    L V_R=-T^Z,       L V_R/V_R=-1/u_R(y).                     (11)

Now put w_R=u_R-h_0 on F_R and extend it by zero at exits. Finite generator algebra gives

    (-Q_R)w_R=f,      f(y)=1+L_core h_0(y).                    (12)

### One-sided Dirichlet-excess lemma

If f<=M throughout F_R, then

    w_R(y)<=M E_y tau_(F_R exit)<=M C_act.                     (13)

Proof: the finite killed resolvent represents w_R as the expected integral of f until exit. Alternatively, positivity of (-Q_R)^(-1) gives w_R<=M(-Q_R)^(-1)1. Its row sums are the finite exit means, bounded by (9). Only an upper bound on w_R is required. Negative correction values are harmless for incoming leakage; an absolute-value bound would add an unnecessary obligation.

The remaining task is to acquire M **independently of R**. Equation (4) provides this rather than assuming it.

## 5. Finite support of positive forcing

Since T>1 and g loses only a polynomial factor, h_0(y) grows exponentially uniformly with r. More explicitly, acquire integer K>=2 such that

    delta K>=B+2cD+1,
    T K/(K+c)>=1,
    T^K g(K)>=1.                                              (14)

The first two are rational ceilings; the last is checked using exact products/powers and increased if necessary. The ratio condition ensures T^r g(r) is nondecreasing for r>=K. For every service composition with r>=K, (4) now gives

    L_core h_0<=-h_0<=-1,
    f=1+L_core h_0<=0.                                        (15)

Thus the positive forcing is confined to finitely many inactive configurations r<K. Enumerate those exact configurations and set

    M=max(0, max_(y_H=0,r<K) [1+L_core h_0(y)]).                (16)

This is a genuinely finite acquisition. The uniform positive excess bound

    w_R(y)<=E_+:=M C_act                                      (17)

therefore holds simultaneously for every head size R. The code records K, every finite forcing row, M, the activation path and its probability/time bounds, and E_+.

The inequality g(r)>=1/r also follows because c<=1, giving a simpler optional support bound. The implemented conditions (14) are exact and sufficient without replacing them by an unproved asymptotic radius.

## 6. New inactive fringe leakage and termination

The only new uncontrolled entrances into F_R are deaths from an inactive service state with r=R. Let d_I=max_(i in I)d_i (zero if I is empty). At such a state, star rates vanish, and the additional generator term caused by the patch is

    T^Z sum_(i in I) d_i y_i w_R(y-e_i)
       <=T^Z d_I R E_+.                                      (18)

By (6), the unmodified tail quotient there is at most -epsilon_tail. Since h_0(y)>=T^R g(R), the entire inactive fringe satisfies

    L V_R/V_R <= -epsilon_tail+d_I R E_+/[T^R g(R)].            (19)

The last term tends to zero. Consequently every sufficiently large R has inactive fringe quotient <=-epsilon_tail/2. A scalar sufficient condition is

    T^R g(R)>=2d_I R E_+/epsilon_tail.                         (20)

To make a recorded scalar radius also a bound for all larger radii, the code additionally checks

    T R^2 >=(R+c)(R+1).                                       (21)

Then T^r g(r)/r is nondecreasing for r>=R, because its successive ratio is T r^2/[(r+c)(r+1)], an increasing product of two positive factors. Both (20) and (21) eventually hold, and they are checked exactly.

The **actual search** does not need to pay for the largest conservative head implied by (20). It starts at R_0, solves (10), and evaluates the exact quotient on every inactive composition with r=R. It accepts that head only if all those finitely many inequalities are <=-epsilon_tail/2. Otherwise it doubles R and repeats. Equations (17)–(21) prove termination of the unbudgeted search. This is a constructive compatibility proof; an arbitrary finite killed-chain correction alone is not declared sufficient.

The default finite-head work budget can stop this search and return UNKNOWN. Such a budget stop is not a mathematical counterexample and not completion of an arbitrary-exponent computation.

## 7. Remaining leakage and the global certificate

Outside F_R and its fringe, the earlier tail is unchanged. Inactive states with r>R cannot enter F_R in one core jump; active states with r>=R+1 also cannot. All stars preserve the presence of a hub and therefore never enter F_R.

For every active service configuration with 1<=r<=R, compute the exact patched core quotient and forward-star quotient H_y. Its dependence on satellites is exactly

    L V_R/V_R =H_y-sum_j a_yj z_j,
    a_yj=[c/(r+c)]sum_h beta_hj y_h>0.                         (22)

Every a_yj is positive because the hub rows are complete and y is active. Finite integer satellite thresholds and a finite rational Foster constant are therefore acquired just as in the earlier phase construction. With

    epsilon=min(epsilon_tail/2, min_(y in F_R)1/u_R(y)),

the exact certificate is LV_R<=-epsilon V_R+C on every integer state. It combines four independently verified regions: the true head, the inactive fringe, active leaking layers, and the analytic tail. No region is replaced by simulation.

## 8. Probabilistic conclusion and moment scope

V_R is positive and normlike: outside the finite service-head it is an exponential of all counts divided by at most a polynomial, and on each of finitely many service-head states its positive coefficient multiplies T^Z. Stopped Dynkin and finite sublevels establish nonexplosion, including high-degree neutral motion. Outside a finite set the drift is <=-1, so finite-set hitting and weak-reversibility return paths establish classwise positive recurrence.

Stationary moment integration is justified without assuming its conclusion. Stopped exponential Dynkin gives P_t V_R<=aV_R+b, a=exp(-epsilon t)<1, b=C(1-a)/epsilon. Apply invariance and concavity to min(V_R,n); the difference from min(aV_R+b,n) is bounded below by -b. Fatou gives pi(V_R)<=C/epsilon. Choosing any rational T>exp(theta), with its separately acquired head, yields pi(exp(theta N))<infinity. The same unique invariant law is used across requests; constants and computation sizes are not uniform.

The executed certificate for a particular T only directly controls exponents below log T. The all-exponent statement rests on the terminating mathematical construction for arbitrary T, not on extrapolating one numerical run or ignoring the implementation budget.

## 9. Exact failed patch and successful acquired repair

Take the five-species accepted phase example and add A->0 at rate1, making A an inactive phase with a death. The earlier theorem/finder intentionally rejects this extra channel. The relaxed raw finder acquires the same service/hub split, now with

    q=(8/3,7/3,2,2),      c=3/64,
    initial R_0=2.

The first head has3 service states. Although its Dirichlet equations are exactly solved, its inactive fringe at2A has **positive** quotient

    2159109577/927605760 >0.

Therefore that local correction is NOT a global Foster certificate. This failed attempt is preserved in the search receipt.

Doubling to R=4 gives a10-state head. All5 inactive fringe configurations then pass; the largest quotient is -12049/7770. The active fringe has55 configurations, each retaining the exact negative satellite slope. The program records all coefficients, thresholds, and the final rational epsilon,C. There are1050 additional exact rational state challenges.

The independent activation path is 0->A->E->B. Its acquired constants are

    p>=1/20,       D_path=7/10,
    C_act=2007/10.

Finite forcing acquisition gives K=4, M=7/6 and E_+=4683/20. The conservative scalar termination radius is32; the exact compatibility search actually stopped at4. Neither radius was assumed as an oracle.

The example is still not complex balanced. Core balance gives b=d=1/45>0, while the two star components demand satellite concentration simultaneously b and2d. Its stable behavior is proved by the constructed correction, not inferred from the incompatible Poisson factors.

## 10. Costs, comparator, and failure boundary

The raw recognizer scans finite service subsets; exact linear-system dimensions and every failed/successful head solve are reported. This run paid for3x3 and10x10 head systems (109 total matrix entries), not only the successful solve. A separate finite forcing enumeration and scalar radius computation pay for the termination witness. Rational bit growth and large Foster constants remain real costs. No polynomial complexity or practical speedup is claimed.

The fresh-immigrant clock is standard independent-particle/Poisson-thinning machinery applied only where its assumptions are actually true. Finite killed resolvents, positive inverse matrices and Foster theory are conventional. The important compatibility step is the *one-sided* uniform excess estimate: it permits a finite exact patch search to terminate even when local correction creates positive fringe drift. No fast stationary law or mixing oracle is supplied.

This remains a restricted shared-hub/monomolecular-core architecture. Missing hub rows, hubs without direct death, nonlinear service cores, or several independent absent-hub geometries are not covered. No general weak-reversibility theorem or historical novelty is claimed. All chemical symbols denote abstract Markov counts only.
