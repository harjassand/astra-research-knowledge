# A terminating partial-row stability construction from tilted support coverage

## Result first

The finite partial-row LP finder need not be assumed to succeed. For its raw **linear-service-core** architecture, a different acquired construction proves termination: solve a finite protected-support hitting problem after an exponential change of weights, use monotonicity of its hitting-time table, and choose the exponential parameter sufficiently close to1. Uncovered satellite faces then have uniform negative drift, while covered faces retain negative drift in every satellite direction.

**Theorem.** Every raw network in Section1 has a nonexplosive, positive recurrent mass-action chain on each reachable class. The unbudgeted exact construction terminates and acquires a rational T>1, an explicitly defined positive normlike V, rational epsilon>0, and a finite factored rational constant C such that LV<=-epsilon V+C. The invariant law has finite exp(theta N) moment for every theta<log T. At least one positive exponential moment, hence all polynomial moments, is obtained. **All finite exponential moments are not claimed.**

The finite support and tilt-trial budgets in the prototype can return UNKNOWN. They are not mathematical counterexamples. Independent review, if accepted, is bound in a separate receipt. No acceptance is inherited from previous packages, and no general weak-reversibility theorem, historical novelty, practical mixing advantage, or operational chemistry is claimed.

## 1. Raw architecture

The raw finder enumerates a nonempty service subset Y_1,...,Y_m with nonempty satellite complement Z_1,...,Z_s. It recognizes:

1. A monomolecular service core strongly connected on {0,Y_1,...,Y_m}. Its immigration, conversion and death rates are lambda_i,k_ij,d_i.
2. An acquired nonempty hub set H. For each hub/satellite pair there is either no star or a reversible pair 2Y_h<->Y_h+Z_j with positive rates alpha_hj,beta_hj. Every satellite has at least one adjacent hub; **hub rows may be incomplete**. Every hub has d_h>0.
3. Every remaining reaction preserves each service coordinate and total count. Its degree may be arbitrary. The full raw graph is weakly reversible.

This version has no extra nonlinear service reactions. All rates are positive rationals; null channels are discarded. The constructor is a trusted int/Fraction research API. The service partition, hub set, support table, exponential parameter, radial correction and exception thresholds are all acquired from the raw list.

Let r=sum_i y_i, Z=sum_j z_j and N=r+Z. A support b in {0,1}^m is **covered** when for every satellite j some h with b_h=1 has beta_hj>0. Covered supports form an upward-closed set. Because every satellite has a neighbor, the all-occupied support is covered.

## 2. Acquired weights and their linear potential

Let I=S\H. Solve the finite linear-subcore absorption equations

    sum_j k_ij(t_j-t_i)-d_i t_i=-1, i in I;    t_h=0.

Define

    L=max_h (1+sum_(i in I)k_hi t_i)/d_h,
    v_i=L+t_i.

If Q is the single-particle conversion/death matrix, then Qv<=-1. For any rational T>1 put

    eta=(T-1)/L, q_i=1+eta v_i,
    delta=min_i eta/q_i,
    B=sum_i lambda_i(q_i-1), D=max_i d_i/q_i,
    alpha=max_h sum_j alpha_hj.

Then q_i>=T, q_h=T, delta>0 and D>0. These identities require direct hub deaths but do not require complete star rows.

For a positive service function f, exponential conjugation of the service generator gives

    L_core(q^y f(y))/(q^y f(y))
      = L_tilt f(y)/f(y)+B+sum_i eta y_i(Qv)_i/q_i
      <= L_tilt f(y)/f(y)+B-delta r.                      (1)

Here L_tilt is the actual linear service generator with positive rates

    tilted immigration lambda_i q_i,
    tilted conversion k_ij q_j/q_i,
    tilted death d_i/q_i.                                (2)

This is an exact generator identity, not an averaging or stationarity assumption.

## 3. The finite tilted protected-support chain

On {0,1}^m, use the same tilted immigration, conversion and death rates. Immigration into i sets b_i=1. Death from an occupied i removes its token. Conversion i->j from an occupied i sets b_i=0,b_j=1; if j is already occupied, the two tokens coalesce. It is incorrect to suppress that conversion when its destination is occupied.

Kill this chain on entering the covered supports. Its killed matrix A_T=-Q_bad is acquired by enumerating all binary supports and raw tilted transitions. Solve

    A_T tau=1,

and set tau=0 on covered supports. Put

    f_T(b)=1+tau(b), F_T=max_b f_T(b),
    K_T=max_(covered b) Q_bin f_T(b).                     (3)

### Why the killed matrix is transient

The strongly connected linear graph has a directed out-tree rooted at0 reaching every service phase. Its root edges are raw immigrations and its other edges are conversions. Fill service vertices in reverse tree-depth order. To fill vertex i, follow the root-to-i path with one token; intermediate ancestor tokens may coalesce, but previously filled deeper vertices are not on that path. Every prescribed transition has positive rate. Excluding other events over this finite word has positive probability. The resulting all-occupied support is covered.

This works from any initial support, including initially occupied ancestors: coalescence never prevents the path from retaining a token at its next vertex. Therefore every noncovered state of the finite chain reaches the killing set with positive probability. Its killed matrix is transient, all tau entries are finite and positive, and the rational linear system is nonsingular.

### Why the table is decreasing under inclusion

Every graphical map is monotone on subsets: immigration is union with {i}, death removes {i}, and coalescing conversion moves i to j when i is present. Apply the same finite-rate Poisson arrows to two initial supports b subset b'. Inclusion persists. Since the target set is upward-closed, its hitting time from b' is at most its hitting time from b, pathwise. Consequently tau and f_T are decreasing under inclusion.

The prototype independently checks every comparable pair of table entries, as well as the exact killed equations. The monotonicity is acquired and verified, not supplied by a caller.

## 4. Comparing actual supports to the finite chain

Apply the decreasing function f_T to b=supp(y), the positive/zero pattern of the actual service counts, under the tilted linear generator.

- Immigration has exactly the binary update and rate.
- If a death source has count1, its support update equals binary removal. If its count is at least2, actual support is unchanged, giving increment0, while binary removal has nonnegative increment because f_T is decreasing.
- If a conversion source i has count1, actual and binary updates coincide. If its count is n>=2, actual support becomes b union {j}; i remains occupied. Write a=f_T(b union {j})-f_T(b)<=0. The actual increment multiplied by n satisfies

      n a<=a<=f_T((b\{i}) union {j})-f_T(b),

  which is the binary increment. This also handles an already occupied destination.

Term by term, therefore,

    L_tilt[f_T(supp y)] <= Q_bin f_T(supp y).             (4)

On uncovered supports Q_bin f_T=-1, so the quotient is at most -1/F_T. On covered supports f_T=1 and the quotient is at most K_T. This finite comparison replaces the missing infinite-fiber estimate; no stationary law or mixing constant is assumed.

## 5. A terminating rational choice of exponential weight

Try T_n=1+2^(-n), n=0,1,2,... . For each trial compute the weights and the full finite tilted table exactly. Stop at the first trial with

    B(T_n) F_(T_n)<=1/4.                                 (5)

This unbudgeted search terminates. At T=1 all tilted rates are the original positive linear rates and the same finite killed matrix remains transient. Its entries are continuous rational functions of T near1, its determinant is nonzero at1, and its inverse is continuous there. Thus every hitting-time entry and F_T remains bounded near1, while B(T) tends to0. Eventually (5) holds.

This argument proves termination of an actual rational check loop. No favorable T, continuity modulus, clock bound or table is given as an oracle. It does not give a uniform efficient bound on the number of trials. The prototype explicitly charges every attempted finite linear system and may return UNKNOWN at its trial budget.

Fix the accepted T, write f=f_T,F=F_T,K=K_T, and choose

    c=min(1,delta/(4alpha),1/(4 D F^2))>0.                (6)

## 6. The shifted radial factor and all extinction layers

Use the radial factor

    g(0)=1,
    g(r+1)/g(r)=(r+1)/(r+1+c),   r>=0,

and define the single global function

    V(y,z)=q^y T^Z f(supp y) g(r).                        (7)

The shift is important: no separate arbitrary value or finite patch at r=0 is needed. For r>=1,

    g(r-1)/g(r)=1+c/r.

The g-factor can only decrease immigration's contribution relative to (1), and it does not affect conversions. Its extra death contribution is at most

    (c/r) sum_i d_i y_i q_i^(-1)
                    f(supp(y-e_i))/f(supp y) <= c D F,   (8)

because f>=1. At r=0 there are no deaths, so the same upper bound remains valid.

Every star preserves the positive/zero support of its hub. Since q_h=T, its f and exponential factors cancel. Forward stars contribute at most c alpha r, and reverse stars contribute exactly

    -c/(r+1+c) sum_(h,j) beta_hj y_h z_j.                 (9)

Consequently, with a=delta-c alpha>0, the universal master bound is

    LV/V <= B+c D F-a r
               + { -1/F on uncovered supports;
                    K    on covered supports }
               -c/(r+1+c)sum_(h,j)beta_hj y_h z_j.        (10)

By (5) and (6), every uncovered support satisfies

    LV/V<=-1/(2F)-a r.                                   (11)

This is uniform over all unbounded populations on every uncovered satellite face, including total service count0 and1. No finite LP compatibility assumption remains.

## 7. Covered faces, compact exception bounds and full recurrence

Define

    A=B+K+c D F,
    epsilon=min(delta/4,1/(4F)),
    R=max(1,ceil((A+epsilon)/a)).

For every covered support with r>=R, (10) gives LV/V<=-epsilon. For covered states with r<R, every satellite coefficient is at least

    a_sat=c beta_min/(R+c)>0,

where beta_min is the smallest positive reverse-star rate. Acquire

    Z_star=max(0,ceil((A+epsilon)(R+c)/(c beta_min))).       (12)

If total satellite count exceeds Z_star, the covered-state drift is also at most -epsilon V. Thus the only possible exceptions lie in the explicit finite set r<R,Z<=Z_star.

A sufficient finite Foster constant is the factored rational expression

    C=F(A+epsilon) q_max^R T^Z_star.                      (13)

Indeed g<=1 and f<=F, so within the finite exception set V<=F q_max^R T^Z_star, while LV+epsilon V<=(A+epsilon)V. Together with (11) this proves LV<=-epsilon V+C everywhere.

The expression (13) is an exact positive rational arithmetic expression. The prototype deliberately does **not** expand gigantic numerator/denominator powers: their exponents and conservative unreduced bit bounds are reported. This is not a claim that writing all bits of C is cheap. The algebraic proof and a verifier of the factored expression do not need that expansion.

Because c<=1, g(r)>=1/(r+1), hence V>=T^N/(r+1) is normlike. Also (10) gives the global bound LV<=A V, which proves nonexplosion by stopped Dynkin and finite sublevels without needing to expand C. The finite-set Foster inequality then gives positive recurrence on every closed communicating class. Full weak reversibility supplies feasible return paths, so reachable communicating classes are closed.

Stationary integration is justified rather than assumed: stopped exponential Dynkin applied to the finite constant (13) gives P_tV<=a_tV+b_t. Invariance and concavity of min(V,n), followed by Fatou with a constant lower bound, give pi(V)<=C/epsilon. For theta<log T, exp(theta N) is bounded by a finite multiple of V. The construction proves at least one such T, not arbitrary prescribed T, so it does not establish all exponential moments.

## 8. Exact same-input construction and honest costs

The raw example is the same non-complex-balanced partial-row network used in the separately reviewed LP finder: service core0->B at1/10,0->D at1/5; B->0,D->0,B->D,D->B at1; stars2B<->B+C and2D<->D+F at rates1,1; neutral C<->F at rates1,1.

The service and hub roles are acquired after5 partition trials. The covered support is {B,D}; the other three supports form the killed system. The rational halving loop tries seven T values and accepts

    T=65/64,
    F=20665756991/619103615,
    K=4622853684288/40241734975.

Each trial solves a3x3 exact system:63 total matrix entries. The final table monotonicity check has9 comparable pairs and its largest fraction has35-bit numerator/denominator size. The resulting conservative bounds are

    c=24913803596894434625/109330819074832735764736,
    R=7581,
    Z_star=3822285280.

The Foster constant is retained in factored form. Its conservative unreduced numerator/denominator bit upper bounds are approximately26.8 billion bits each. No such expansion was attempted. This construction is a termination/existence result, not a useful numerical mixing estimate.

The original program checks the exact full raw generator quotient against (10) at720 ordinary states and48 targeted states near R and Z_star. Bounded-jump ratios make these checks exact without evaluating enormous values T^N. These are master-bound checks, not claimed bitwise evaluations of the fully expanded C.

The earlier LP construction on the same raw example acquired T=2 and a much smaller explicit finite correction/constant. It can be quantitatively preferable, but it has no completeness theorem and can return UNKNOWN. The present route gives a structural termination guarantee at a possibly much smaller T and substantially looser constants. Neither is declared universally superior.

## 9. Conventional machinery, scope and unresolved frontiers

Monotone graphical couplings, exponential generator conjugation, killed finite matrices, and Foster theory are conventional. The acquired support-coverage table is the missing finite object here: its monotonicity turns a finite binary calculation into a uniform bound on every infinite uncovered fiber. The shifted radial ratio then makes all extinction layers compatible without an assumed stationary fiber law, good pivot, or good LP solution.

The result remains restricted by a strongly connected monomolecular service core, direct hub deaths, reversible star shapes and service-preserving neutral extras. It does not establish the theorem for general nonlinear service interactions, arbitrary cross-species autocatalysis, or all weakly reversible networks. The support-clock comparison itself may extend beyond the accepted architecture, but no such stability extension is asserted here.

A single logical protected token can suffice for first-hub activation and can reduce that different clock's state count. It cannot by itself record simultaneous multi-hub coverage; the finite support table here has a different target and purpose.

No general-WR solution, historical novelty, physical capability, polynomial-time guarantee, or practical tail/mixing quality is claimed. Budget UNKNOWN outcomes and the very large compact constant are substantive limitations, not editorial omissions.
