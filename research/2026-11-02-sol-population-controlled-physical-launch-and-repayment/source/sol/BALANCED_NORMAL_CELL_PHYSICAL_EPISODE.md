# A complete slow physical episode from a derived normal-cell reference measure

Author construction, same principal. This proves an infinite-face operation for the six-species diagnostic. It does not prove global recurrence or the unrestricted weak-reversibility principle. Finite killed inverses, time reversal and stopped Foster arguments are ordinary machinery; the useful addition is the acquired normal-cell measure, its actual occupation bound and the phase-crossing repayment comparison.

## 1. One physical receiver, including every exit

The disjoint ordered blocks have complexes

    y0=0, y1=A+B, y2=2A+B+C, y3=3A+2B+2C,
    z0=0, z1=D+E, z2=2D+E+F, z3=3D+2E+2F.

Their cyclic rates are positive alpha_i and beta_j. The conservative pair is

    A+D+2B+2C -> A+D+2E+2F (rate 2),
    A+D+2E+2F -> A+D+2B+2C (rate 1).

The rate convention is ordinary falling factorial without factorial divisors. Put m(0)=0,m(1)=2,m(2)=4 and m(a)=7 for a>=3. For EVERY physical state define

    Z(x)=15+|x|-m(A)-m(D),   U_D(x)=D Z(x)^2.              (N1)

Z>=1 and its sublevels are finite, because both corrections are bounded by7. No auxiliary inventory is being hidden in an unbounded tag. In particular (N1) receives a cold landing, an anchor4 overrun, and every other actual output without a prescribed receiving law.

When A=i,D=j belong to {0,1,2,3}, call the two block channels from sources y_i,z_j NORMAL. Call BOTH conservative channels normal. Every other genuine channel is unexpected. A normal block jump follows the actual physical phase i->i+1 modulo4. It preserves Z exactly, including 3->0; conservative jumps also preserve Z exactly.

At the first unexpected event only the following possibilities exist:

* phase1, source0: Delta Z=0;
* phase2, source0 or source1: Delta Z=-1;
* phase3, source0/source1/source2: Delta Z=2/2/3.

These follow directly from the physical count changes and m. They do not require that a retagged raw source be enabled afterwards.

## 2. The entire normal cell and its ACQUIRED measure

Start at A=D=0 with hidden base rho=(0,b,c,0,e,f), total N=b+c+e+f. Let

    w=(0,-2,-2,0,2,2),
    x(i,j,k)=rho+k w+y_i+z_j.

Include every (i,j,k) with i,j in {0,1,2,3}, k integer and x>=0. This is a finite cell: physical total is N+m(i)+m(j)<=N+14. Signed residual coordinates down to -2 are INCLUDED when the physical state is nonnegative. Every actual normal jump stays in this cell. In particular one must not truncate it to nonnegative rho+k w.

Its genuine normal generator Q has the explicit positive invariant weight

    mu(i,j,k)=2^k/[alpha_i beta_j product_l x_l(i,j,k)!].     (N2)

Proof: for fixed j,k the flux on a normal I-cycle edge is

    2^k/[beta_j product_l (rho+k w+z_j)_l!],

independent of i. If the common residual is not nonnegative, ALL those I-cycle edges are absent, so incoming and outgoing I-flux are both zero. The same argument applies to II. The two conservative edges satisfy exact pair balance in (N2), since their raw rate ratio has the compensating factor2. This proves mu Q=0 on the FULL finite cell, without assuming irreducibility or an input distribution.

Let h be the sum of ALL unexpected hazards. It is zero at phase00 and at least h0=min(alpha_0,beta_0)>0 elsewhere. Put

    G=(-Q+diag h)^(-1).

This is the ACTUAL occupation kernel before the first unexpected source sigma. No physical trajectory is replaced by mu. In particular starting at a cold point is not declared equilibrated.

## 3. Actual clocks and adjoint occupation, without a mixing gap

From any off-00 point, the physical time until killing or phase00 has mean <=1/h0. At phase00 the mean wait is 1/(alpha_0+beta_0). Its first normal jump enters phase10 or01. There the conservative pair is disabled and the genuine total rate is <=C(N+15); an unexpected own zero-source event has hazard >=h0. Thus the conditional probability of killing immediately at this first off-00 point is >=c/(N+15). Restarting at successive actual phase00 returns gives

    max_i sum_j G(i,j) <= C_T(N+15).                        (N3)

This proof counts physical holding times and every intervening path. Finite cell size and bounded rates imply a.s. finite genuine jump count before sigma; no uniform expected-activity requirement is imposed on a future global theorem.

Define the time-reversed normal generator by Q*(j,i)=mu(i)Q(i,j)/mu(j). A reverse I-cycle jumps from phase i to i-1 at the SAME rate alpha_i(x)_y_i as the forward normal channel from phase i; the conservative pair is unchanged. At reverse phase00 its first jump enters30 or03. Its total rate there is <=C(N+15)^4, since both anchors are <=3. The same actual renewal argument proves

    max_j sum_i G*(j,i) <= C_*(N+15)^4,                    (N4)
    mu(i)G(i,j)=mu(j)G*(j,i),
    G(i,j)<=C_*(N+15)^4 mu(j)/mu(i).                       (N5)

The reverse process is a mathematical adjoint used to bound the actual forward kernel. Neither a mixing rate nor stationary entrance has been inserted.

## 4. A reference barrier controls ALL cold occupation

Fix R and assume |b-c|,|e-f|<=R. Fix delta=1/128. Let COLD be the cell states with at least one of B,C,E,F below delta N. There are constants c_R>0,C_R,p_R and an acquired finite threshold such that

    sum_(j in COLD) mu(j) <= C_R(N+15)^p_R exp(-c_R N) mu_max. (N6)

Here mu_max is the maximum weight on the finite cell, acquired by exact factorial-ratio comparisons (or finite enumeration). A direct factorial-ratio proof of the exponential barrier is enough: along a phase00 fiber with B increasing by2 and E decreasing by2,

    mu(B+2)/mu(B)
      =(E)_2(F)_2/[2(B+1)(B+2)(C+1)(C+2)].                 (N7)

For N sufficiently large compared with R, when the smaller pair is below N/16 and the other pair is above N/3, the ratio towards the interior is at least2. From a state with a hidden coordinate below N/128 there are at least floor(N/256)-O_R(1) such inward steps before that coordinate reaches N/64. The reverse comparison when E,F are small is even stronger because of the factor2. Hence its weight is exponentially below some interior weight. Phase buffers change hidden counts by at most2 and add anchor factorials <=6. The finitely many signed residual end points can be compared with a nonnegative residual point within two fiber steps. These changes cost only a fixed power of N; summing O(N) states gives (N6). This also proves that a maximizer lies away from all cold ends. All constants can be enlarged using these finite explicit factorial comparisons; no equilibrium computation is a premise.

Suppose the ACTUAL input has any phase i,j in {0,1,2,3} and satisfies the checkable reference-band condition

    mu(input)>=mu_max exp(-c_R N/2).                       (N8)

Combining (N5)-(N8), every polynomially bounded genuine hazard a_j obeys

    E_input integral_0^sigma a(X_t)1_COLD dt
       <=poly_R(N) exp(-c_R N/2)=:epsilon_N.               (N9)

This bounds not just a chosen exit law but actual cold occupation, unexpected cold exits, and normal phase crossings occurring there. Intermediate core excursions are included. It is NOT a bound for arbitrary cold input; earning passage from cold input into (N8) remains a separate global obligation.

## 5. Phase crossings compare bad exits with actual repayment

Let P_g,P_c,P_b denote the probabilities of the three exit types in section1. They sum to1. Let J_l^I be the number of genuine normal I phase-l transitions BEFORE killing, and similarly for II. Starting at phase00, the pathwise counting identities give

    J_3^I<=J_2^I,   J_1^I<=J_2^I+1,                      (N10)

and the same for II. These hold with arbitrary interleaved core movement and peer block evolution. For an arbitrary initial phase, use J_3^I<=J_2^I+1 instead; its additional O(N^-2) error below is harmless. The second inequality already holds from every initial phase.

At phase2 the repaying hazard is alpha_0+2 alpha_1 B, while the normal phase2 hazard is 2 alpha_2 B C. Since C<=N+14, EVERY cell state satisfies

    alpha_0+2 alpha_1 B >= c/(N+15) *2 alpha_2 B C.

Consequently P_g>=c/(N+15) E[J_2^I+J_2^II]. This comparison does not discard cold points. On warm points, a phase1 conversion hazard is at most C/(N+15) times its normal phase1 hazard, and a phase3 overrun hazard is at most C/(N+15)^2 times its normal phase3 hazard. Formula (N9) pays the entire cold remainder. The genuine channel compensator and (N10) therefore yield

    P_b <=C_b/(N+15) P_g+epsilon_N,
    P_c <=C_c P_g+C'_c/(N+15)+epsilon_N.                  (N11)

All constants depend only on the fixed positive raw rates, R and delta. In particular P_g>=p0>0 for all sufficiently large N. Since a bad exit raises Z by at most3,

    E Delta Z <=-P_g+3P_b<=-p0/2,
    E(Delta Z)^2<=9.                                      (N12)

Thus a first unexpected source has a uniformly negative MASS increment despite the physical waiting time growing with N. No demand for a bounded number of ordinary normal cycles or exponential physical return was used.

## 6. Complete physical contract on this infinite face

Every point of the normal cell has Z=N+15. By (N3),(N12),

    E[Z_out^2-Z_in^2] <=-p0 Z_in+9,
    E sigma<=C_T Z_in.

Choose D>=2C_T/p0 and enlarge the acquired finite threshold. Then the SAME physical receiver (N1), including cold exits and anchor4 outputs, satisfies

    E_input[sigma+U_D(actual output)]<=U_D(input).         (N13)

This is a complete actual-time episode for every input in the infinite family (N8). It pays all physical residence and every output. It does not separately claim q occupation or exponential return. The finite adjoint occupation bound was acquired from the raw normal list, not supplied as a favorable transport interface.

## 7. Frontier

The operation avoids a stationary fiber and does not improve the already banked uniform multiplicative neutral criterion. It deliberately observes until a genuinely rare source occurs, with mean physical time O(N), then uses phase-crossing flow identities to compare bad and repaying exits. The normal cell can grow with N and have a vanishing gap.

A full theorem must still acquire passage into the reference band from every cold input, control the launch population and its later repayment at (N1), and cover unbounded anchors and unbounded hidden-pair differences. The present two ordered blocks retain an aggregate +1/-3 anchor structure; this result is evidence for a new integrated operation, not a resolution of arbitrary coupled activation layers. A reusable extension would derive an appropriate finite normal policy, its raw reference flow and crossing/debt inequalities for networks without that ordered phase structure. None of those decisions is assumed earned for a general list.
