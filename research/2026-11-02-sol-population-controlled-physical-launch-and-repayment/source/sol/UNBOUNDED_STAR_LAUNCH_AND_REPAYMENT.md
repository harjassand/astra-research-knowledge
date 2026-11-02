# Population-controlled launch without a clean-zero event

Author construction. This replaces the nonuniform forced-zero minorization in COLD_LAUNCH_AND_DELAYED_PHYSICAL_REPAYMENT.md. It earns a common physical episode with BOTH cold and hot inventories unbounded. It is not global recurrence: high anchors, arbitrary initial active phases and large pair-difference faces still require their own compatible operations.

## 1. Complete destination of this operation

For the same two ordered blocks plus rate2/rate1 conservative pair, start at

    x=(0,b,c,0,e,f), b,c,e,f>=0, N=b+c+e+f.

There are fixed eps>0,D,N0 depending only on the positive raw rates, such that for every input with N>=N0 and

    |b-c|,|e-f| <= eps N,                                  (S1)

an actual episode has

    E[sigma+D Z(actual output)^2]<=D Z(input)^2,
    Z(x)=15+|x|-m(A)-m(D),                                (S2)

with the SAME m=(0,2,4,7,7,...) as before. All interruptions and endpoints are included. No bound on b+c or e+f is assumed. One pair may be bounded, may grow as any sublinear power of N, or may be comparable to the other. The episode has E sigma<=C(N+15) and bounded total Delta Z, with constants independent of all four input inventories.

## 2. Change the launch stop: a seven-state ACTUAL controller

Run only until the FIRST unexpected source OR the first overlap A>0,D>0. Before that stop the conservative pair is disabled. A normal I-cycle preserves its residual (b,c), a normal II-cycle preserves (e,f), and at most one anchor is positive. Therefore the complete genuine normal process is the seven-state star

    00, 10,20,30, 01,02,03.

This is not a truncated inventory controller: the four unbounded inventories are exact fixed residual parameters until the stop. Every actual competing raw source is either a transition of this star or an explicitly retained exit. Every normal transition preserves Z exactly. Thus there is NO unbounded launch-population loan to estimate; the stop was chosen before such a loan can accumulate.

At active I phase i, define genuine normal rates

    r1=alpha_1(b+1),
    r2=2alpha_2(b+1)(c+1),
    r3=6alpha_3(b+2)(b+1)(c+2)(c+1).

The I normal path is 00->10->20->30->00. At each positive I phase the peer zero-source input has rate beta_0 and is an overlap exit. The own unexpected sources are:

* phase1: alpha_0, Delta Z=0;
* phase2: alpha_0+2alpha_1(b+1), Delta Z=-1;
* phase3: alpha_0+3alpha_1(b+2)+6alpha_2(b+2)(c+2), Delta Z=2/2/3 channelwise.

The II arm has the swapped formula. An overlap exit itself is Z-neutral. Call overlaps from phase1 or2 CLEAN, and overlaps from phase3 UNCLEAN. The latter are received immediately at (S2), before any conservative jump; no claim about their later composition is needed for this episode.

All absorption probabilities and the physical mean are acquired by a seven-state rational killed inverse for rational raw inputs. The following analytic identities make the population-uniform control explicit.

## 3. Exact occupation identities pay every exit type

Let T_i^I be actual occupation time at I phase i before the launch stop. Write P_c,I for its neutral own phase1 exit, P_g,I for its repaying phase2 exit, P_b,I for its harmful phase3 exit, and P_o,i,I for overlap at that phase. Then EXACTLY

    P_c,I=(alpha_0/beta_0) P_o,1,I,
    P_b,I=h3 E T_3^I,
    P_o,1,I=beta_0 E T_1^I.

Before the stop each complete phase3 crossing requires a phase1 crossing. The genuine compensator therefore gives

    r3 E T_3^I <= r1 E T_1^I.

Consequently

    P_b,I <= [h3 r1/(beta_0 r3)] P_o,1,I
            <=C_b,I/(c+1) P_o,1,I <=C_b,I P_o,1,I,        (S3)
    P_o,3,I <=(r1/r3)P_o,1,I<=C_u,I P_o,1,I.             (S4)

These constants are acquired directly from the displayed finite rates. For example C_b,I=alpha_1(alpha_0+alpha_1+alpha_2)/(alpha_3 beta_0) is a conservative sufficient constant; all falling-factorial divisors omitted from it are >=1. Also C_u,I=alpha_1/(6alpha_3) suffices. The peer arm gives the corresponding constants.

Sum the two arms. With P_g repaying, P_c neutral, P_b harmful, P_a clean overlap and P_u unclean overlap,

    P_c<=C_c P_a, P_b<=C_b P_a, P_u<=C_u P_a,
    P_g+P_c+P_b+P_a+P_u=1.

Hence

    P_g+P_a>=p_*>0                                      (S5)

uniformly in ALL b,c,e,f. This is the sought joint rule: an apparent neutral debt either exposes actual repayment, or carries a clean activation probability that pays its harmful companions. No separate favorable receiving law is assumed. The finite graph crossing identity was applied before inventories could move, so no unearned neighboring-profile transport is inserted.

The launch's mean physical time is <=C(N+15). At00 its holding mean is 1/(alpha_0+beta_0). Away from00 the total own-zero plus peer-zero stopping hazard is at least alpha_0+beta_0. After a departure from00 the first phase1 point has total rate <=C(N+15), and stopping hazard at least that fixed positive sum. Thus each actual 00 excursion has probability >=c/(N+15) of stopping immediately there, and has bounded physical mean. Geometric renewal proves the claim, with every intervening path retained. The star is finite at each input, so the launch has finitely many genuine jumps a.s.

## 4. Every clean exit can activate the actual reference band

A clean exit has phases (1,1),(2,1) or(1,2). Both anchors are below3, so neither terminal source is enabled. Run the actual conservative pair until a chosen deep reference band or the first noncore reaction. Under (S1), for a sufficiently small fixed eps, the conservative reference maximum stays uniformly inside the hidden simplex. The quartic core drift points towards it from either cold end.

Choose a relative band width eta>0. On either side outside that band, the genuine core drift of B has the appropriate sign and magnitude >=c_eta N^4. Stopping the distance-to-band martingale gives pure-core mean hitting time <=C_eta/N^3. The full genuine noncore hazard with anchors<=2 is <=C N^2. Therefore the ACTUAL interruption probability is <=C_eta/N, and actual mean time is <=C_eta/N^3. At any interrupting reaction here Delta Z<=0: phase1 growth is neutral; phase2 lower-source growth repays one; its normal source is neutral. Every such interruption is a paid actual endpoint.

On successful entry Z is unchanged. For any prescribed FIXED L, choose eta so the reference deficit is <=cN/(8L). This is acquired from the explicit one-dimensional factorial-ratio maximum and its uniform strictly convex interior limit. No stationary entrance law or infinite-rate limit is used.

The reference barrier and deficit transport extend uniformly from fixed pair-difference bounds to (S1). For example choose eps initially <=1/8192, then leave a factor-two margin for the finitely many later raw buffers. If a hidden coordinate is below N/128, its paired coordinate differs by at most eps N+O(1); both are below N/64 for large N. The opposite pair is above N/3. The same exact inward ratio >=2 therefore holds for at least cN steps. Signed packet end points cost only a fixed power of N. Thus the actual killed-adjoint occupation bound remains polynomial times exp(-cN), with constants and thresholds independent of b,c,e,f satisfying (S1). This is the uniform version of the already proved barrier, not an assumed profile.

## 5. A FIXED amount of drainage pays every launch outcome

After successful clean activation execute at most L of the earned normal-cell episodes. As in the bounded-head construction, stop on an anchor4 or a failed next-band test; pay that actual endpoint at (S2). The fixed band budget, the proved bounded-buffer deficit transport and the actual occupation bound give

    E Delta Z_drain<=-d L+o(1),
    |Delta Z_drain|<=3L,
    E drain_time<=C L(N+15).                              (S6)

The constant d>0 depends only on the raw rates and a fixed warm fraction. The probability of premature overrun is O(L/N), and the other band failure probabilities are exponentially small. Pair differences change by O(L), absorbed by the initial factor-two cone margin after enlarging N0. All outputs and interruptions are included.

Choose L so dL>=3C_b+1. The number L depends ONLY on fixed raw rates. A failed clean activation has nonpositive Delta Z, so combining (S3),(S5),(S6) gives

    E Delta Z_total
       <=-P_g+3P_b-(dL-o(1))P_a
       <=-P_g-P_a+o(1) <=-p_*/2                           (S7)

for large N. The total increment has a fixed bound 3+3L. Mean physical time is <=C_L(N+15). Since input Z=N+15, the exact quadratic identity gives

    E[Z_out^2-Z_in^2]<=-p_* Z_in+(3+3L)^2.

Choose a fixed D large enough to pay C_L Z_in, then enlarge the finite threshold. This proves the complete common physical contract (S2).

## 6. Scientific scope

The population-controlled operation replaces the failed route through zero. It does not use a head whose size or success probability grows with the cold population. Both cold inventories can evolve unboundedly; the actual stop exposes their source debt BEFORE a population loan accumulates. Competing paths are paid through exact star occupation and actual finite-rate activation, followed by a fixed amount of delayed drainage at the same physical quadratic receiver.

It covers the entire A=D=0 section inside a fixed small-relative-difference cone, including all cold/hot ratios. High anchors, arbitrary initial active phases outside the admitted reference bands, and large pair-difference faces are STILL separate obligations. In particular an unclean phase3 overlap is paid as an endpoint, not asserted to be globally resolved. A full recurrence theorem needs a compatible policy for those outputs and every remaining infinite face. The seven-state crossing construction is a reusable missing operation; it is not an unrestricted weak-reversibility theorem or an acquired general numerical solver.
