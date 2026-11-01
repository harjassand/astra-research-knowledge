# Independent review of the rate 2 task observable corrector

## Decision and exact scope

**PASS for the finite N stopped compact transport certificate, with the explicit
receiver conventions below.** No coefficient, sign, product-jump, or asymptotic
power repair is required. This decision rests on the ordinary mathematical audit
in this document, not on symbolic success. The source is an author construction;
this separate receipt supplies its independent receiving review.

The received operation is: for a supplied real C² function f of
z=(L/T,E/T³), compile F=f+AE f_l/(NT), with T=N^(1/5), into an actual full-chain
transport identity, state/channel-weighted residual, full bracket/jump bound,
and stopped compact-window probability certificate. Its occupation, imbalance,
and total-count-band costs are explicitly charged. The proof does not average
against any stationary fast-state law.

The following conventions make the receiving statement unambiguous:

1. The initial state is an admitted nonnegative integer state: L(0)<KT,
   E(0)<MT³, and |n(0)-N|<=d, or the analogous consistently chosen closed-boundary
   version. The initial state and all one-jump endpoints used at a crossing lie
   in the stated enlarged rectangle. Starting outside it is not covered merely
   by nonnegative counts.
2. The C² function is defined on an open neighborhood of the entire compact
   union of the relevant jump segments. All derivative bounds in a common
   finite-N certificate cover that union. For the asymptotic claims, K,M,S and
   the five derivative norms F_10,F_01,F_20,F_11,F_02 are uniformly bounded as
   T grows. A T-dependent f with growing norms is not covered by the unqualified
   O(T^-1) shorthand; the literal formulas still apply.
3. D_A in the count-band lower-tail estimate is evaluated at the **same bounded
   stopping time** sigma as H=integral_0^sigma A. Equivalently, one bounds a
   lower-band exit before the other stops and before the H budget. One cannot
   combine D_A(ST) after a physical stop with a pre-stop H budget.
4. If a Chernoff threshold is nonpositive or not above its compensator bound,
   use the trivial bound 1. When Hbar=0 and k_->0, the stopped death-count event
   has probability zero; interpret the displayed entropy formula by its limit.
   Count-band failure is not claimed small without initial distance from the
   relevant edge.

These are scope clarifications, not changes to the displayed algebra. The
original source files were not modified. At initial inspection there was no
author freeze in the target directory. `SOURCE_SNAPSHOT_FREEZE.json` therefore
records an independent receiver snapshot, not a fictitious author freeze.

## Source identity

The reviewed source bytes have these SHA-256 hashes:

- TASK_OBSERVABLE_CORRECTOR.md:
  `02e55555d845f7f3060e23500cb36934fbfd4709eb8755c9b1ebf2cfa7002a94`
- check_task_observable_corrector.py:
  `819df4b96c9dc691ef575e261bad14b5411021532c4ced318bd0892709395fcd`
- exact_checks.json:
  `ab4c024b29ab5f918ec6ef9d0e55a0d7e5ec061cd7df15f0e1aecba12c405f73`

Exact copies are retained in `source_snapshot/`. The author checker was replayed
on that copy, and its output and rewritten JSON are byte-identical to the input
JSON. No source retrieval, installation, hardware work, or publication was used.

## Generator and finite jump algebra

The model consists of the twelve source/product-complex reactions in the source
table, with falling-factorial rate A(A-1) for each 2A source, and specifically
rate 2CD for CD to AE. Each active transition has a nonnegative endpoint. Direct
addition gives

    GL = 1+A+AL+AE-3A²,
    GE = A(A-1)-2AE+2CD.

To check the less transparent correction drift without hiding the fast rows,
write h=AE. Immigration and A death contribute E-AE. The two 2A-to-arm channels
contribute -2A(A-1)E; their reverses contribute A(C+D)E. The 2A-to-AE channel
contributes A(A-1)(A-E-1). The two outgoing AE channels together contribute
-2A²E. The CD-to-AE channel contributes 2CD(A+E+1). Finally CD-to-AB and
AB-to-CD contribute E(CD-AB). Thus

    Gh = E+2ACD+A(A-1)²+2CD+3ECD
         +h(2+2L-7A-B).

Using CD=L²-Q and inserting -Nh+Nh proves exactly source equation (1).
Moreover Q=2AL-A²+Z²/4>=0, and

    N-B+2L+2-7A = N-n+E+4L+2-8A.

Since 0<=A<=L, |4L-8A|<=4L. This proves equation (2) with its stated constant.
Summing squared and absolute L,E increments gives every rate sum in (3),
including the negative mixed covariance q_LE=-(A(A-1)+h).

For a single transition, with h'=h+Delta h and g=f_l,

    Delta(hg) = g Delta h + h' Delta g
              = g Delta h + h Delta g + Delta h Delta g.

The last product is indispensable. Summing this equality gives the source
product rule with **post-jump h'**, not h. Taylor's fundamental theorem along
one segment, valid for C² f, gives the exact integral R2 and the exact first
integral of Delta g in (5). Inserting the two slow drifts and Gh into GF cancels
h f_l/T with -Nh f_l/(NT). The remaining leading terms are

    f_l/T + 3EL² f_l/(NT) + 2L² f_e/T³ = (V dot Df)/T,

because N=T⁵. This proves the complete identity (4), with no omitted drift,
product, or covariance remainder and no third derivative.

On AB to CD and CD to AB, Delta L=Delta E=0. Hence Delta f=Delta g=0 exactly,
and both R2 and P vanish row by row. This is an exact slow-coordinate invariance,
not a small-jump approximation or cancellation of two large absolute bounds.
The fast contribution to Gh above remains present and is part of the exact
correcting drift. There is no frozen-generator substitution.

## Per segment derivative weights and deterministic residual

Taylor's integral has total weight integral_0^1(1-theta)dtheta=1/2; the two mixed
Hessian entries produce coefficient 1 on |uv|/T⁴. The first integral for Delta g
has weight one. Consequently the last two lines of (6) have precisely the stated
coefficients and retain their individual segment norms. Bounding derivatives
only at endpoints would not suffice in general. C² is enough even for functions
such as |l-l_star|^(5/2)+e², whose third derivative fails at l_star.

The remaining absolute bounds follow from

    |A+AL-3A²| <= A+2AL,
    |A(A-1)-2h-2Q| <= A(A-1)+2h+2Q,
    CD<=L²,
    |r_h| <= H_h.

The first inequality uses |1-3A/L|<=2 when L>0; L=0 forces A=0.
Every active row has 0<=A'<=A+1, 0<=E'<=E+1, so h'<=h+=(A+1)(E+1).
Replacing the individual norms by uniform segment norms and summing the exact
absolute jump intensities proves (7). No sign cancellation is assumed in this
bound. The exact signed representation (5) remains separately available.

Before the common stop, L<KT, E<MT³, |n-N|<=d. Also a2<=A² and
Q<=2AL+Z²/4. Integrating q_LL,w_LE,q_EE,s_L yields respectively U,W,V_E,V_L
from (13). For the six groups in H_h, the integrated charges are respectively

    MST⁴,
    6MKT⁴ Hbar + (3/4)MT³ Zbar,
    2K²T² Hbar,
    KT Jbar,
    2K²ST³,
    MT³(d+MT³+4KT+2)Hbar.

The A(A-1)² charge uses integer A: (A-1)²<=A² for A>=1, and then A³<=KT A²;
at A=0 its value is zero. These charges sum to the displayed R_h^int. Substitution
in (6)-(7) gives every term and constant of rho_f in (14). All occupations are
pre-stop integrals, so the crossing jump contributes no extra occupation mass.

## Actual corrected martingale and neighbors

Equation (8) is exactly the one-transition product equality above, plus Delta f.
Applying the segment first-derivative bounds to Delta f and the segment second-
derivative bounds to Delta g proves d_r and (9). In particular each fast row
has jump Delta F=+/- E f_l/(NT), giving the nonzero combined bracket

    (AB+CD) E² f_l²/(N²T²).

The source q_hh in (10) is the sum of all twelve squared h jumps. For the two AE
outgoing rows, the identity

    (E-A-1)²+(-A-E+1)² = 2[(E-1)²+A²]

accounts exactly for its middle term. The coarse bound uses |u|,|v|<=1 and
|w|<=A+E+1, then

    (a|u|+b|v|+c|w|)²
      <= 2(a|u|+b|v|)²+2c²w².

Its integrated version is (15). For Phi, use A(C+D)<=2AL, CD<=L²,
AB<=A(N+d), and bound the three remaining square groups in q_hh by
(A+E+1)²(A²+2h+2L²). This reproduces precisely Phi, with no uncharged fast rate.
Thus v_f bounds the actual predictable quadratic variation, and j_f bounds each
actual stopped jump, not merely jumps of f.

Admitted one-jump endpoints satisfy 0<=L'<=KT+1 and 0<=E'<=MT³+1. Line segments
between such endpoints stay in the nonnegative enlarged rectangle. At a crossing,
A'<=L'<=KT+1, so the endpoint h' bound is Hplus, even when the pre-stop bound
KT times MT³ would fail. The stopped identity reads

    f(z_tstop)-f(z_0)-integral_0^tstop V dot Df ds/T
      = M_F(tstop)+integral_0^tstop R_f ds
        -h_tstop f_l(z_tstop)/(NT)+h_0 f_l(z_0)/(NT).

Taking absolute values proves (17) once (16) is established.

There is no integrability/explosion gap: n changes only by immigration and A
death, so n(t)<=n(0)+I(t), with rate-one Poisson I. On every finite horizon the
right side is finite almost surely; the finite collection of states below that
bound has bounded total jump rates. Localization then proves nonexplosion. Before
the compact/count stop the state space and the one-jump enlargement are already
finite, so Dynkin martingales and optional stopping here are legitimate.

## Exponential martingale estimates

For |y|<=j and 0<theta<3/j, expanding the exponential and using
k!>=2*3^(k-2) for k>=2 gives

    exp(theta y)-1-theta y <= theta² y²/[2(1-theta j/3)].

The compensated jump exponential is a positive local martingale and hence a
supermartingale. Stopping at the first positive crossing x and using the
deterministic predictable-bracket bound v gives exp[-theta x+theta²v/
(2(1-theta j/3))]. For v>0, theta=x/(v+jx/3) gives the exponent in (16).
Apply the same argument to -M and add the two bounds. The zero-bracket cases
are obtained directly because the martingale is identically zero. This proves
the two-sided maximal probability claim without invoking an unverified outside
result.

## Paid occupation and imbalance stops

Under (18),

    B=n-2L+A-E >= N-d-2KT-MT³ >= N/2.

Also C+D<=2KT<=N/4. The exact A drift therefore obeys

    GA=1-A-3a2+A(C+D)+3CD-AB
       <=1+3K²T²-(N/4)A.

Stopped Dynkin with nonnegative terminal A proves (20). For the stronger tail,
the exact A bracket is

    q_A=1+A+3a2+A(C+D)+2h+3CD+AB.

Use a2<=KT A, C+D<=2KT, E<=MT³, B<=N+d, and CD<=K²T²
to obtain q_A<=r+C_A A with exactly the printed C_A. All A jumps have size one.
At a continuous H-budget hit before the physical stop,

    M_A=A_terminal-A(0)-integral GA
       >=NHbar/4-A(0)-rST=x_A.

Its bracket is at most v_A. The one-sided exponential argument just proved gives
(21). Since A<=KT before stopping, J<=KT H pathwise; Jbar>=KT Hbar needs no
separate failure probability.

Only the four arm-exchange channels move Z. Direct addition gives GZ=-AZ and
q_Z=2a2+A(C+D)=2A(L-1)<=2KT A. For the stopped damping coefficient
alpha_s=A_s*1_{s<tau}, variation of constants and integration by parts yield

    Z_tstop=Z(0)exp(-integral_0^t alpha)
      +M_Z(tstop)
      -integral_0^t exp(-integral_s^t alpha) alpha_s M_Z(sstop) ds.

The nonnegative integral kernel has total mass at most one. Hence
sup|Z_tstop|<=|Z(0)|+2sup|M_Z(tstop)|. Before the H stop its bracket is at most
2KT Hbar, and its jumps have size one. This proves (23), including its factor
of two. A supremum cap zmax gives the pre-exit integral budget ST zmax²; the
terminal crossing overshoot does not alter that integral.

Alternatively G(Z²)=-2AZ²+q_Z yields E[Z(tstop)²]<=Z(0)²+2KT Hbar.
Integrating this nonnegative stopped bound for t<=ST dominates the occupation
up to the stop and proves (24). Markov charging of any proposed Z2 budget follows.
The supremum and occupation routes are alternatives, not a claim of independent
failure events.

## Count band and composition of failures

Let sigma be a bounded common stopping time no later than ST, including all
other relevant stops. Write delta=n(0)-N. Since n=n(0)+I-D_A, an upper-band
crossing by sigma requires I(ST)>=d-delta. A lower-band crossing before the
other stops requires D_A(sigma)>=d+delta. Rounding these weaker necessary
thresholds upward is safe even for a strict crossing convention; floor plus one
can give the sharper strict threshold.

For Poisson I(ST), E exp(theta I)=exp(ST(exp(theta)-1)). Markov with
theta=log(k_+/(ST)) proves the first entropy bound in (25) when k_+>ST.
For the stopped death count, exp(theta D_A(sigma)-(exp(theta)-1)H_sigma)
is a positive supermartingale. On D_A(sigma)>=k_- and H_sigma<=Hbar it is at
least exp(theta k_--(exp(theta)-1)Hbar). Markov and
theta=log(k_-/Hbar) prove the second bound. This is valid for the stopped
count; no independence of D_A and H is required or asserted.

A consumer removing auxiliary budgets may add the H failure cost, one chosen
imbalance/occupation failure cost, and the applicable upper/lower band costs by
a union bound. The J failure cost is zero when Jbar>=KT Hbar. This does **not**
remove L or E exits: those are physical-window exits whose relevance to a clock
or clearance claim remains for the consumer to establish. Initial count margin
matters. For example an initial state at the upper band edge need not have a
small upper-band exit probability; the source does not claim otherwise.

## Compact power audit

Take the source choice Hbar=h0 T^-2, Jbar=K h0 T^-1,
Zbar=S T², d=d0 T³, and uniformly bounded C² norms. The maximum powers of T in
the eight successive summands of (14) are

    -2, -1, -1, -1, -3, -3, -2, -2.

Thus rho_f=O(T^-1). The maximum powers in the four expanded summands of v_f are

    -1, -3, -3, -3.

The endpoint correction is O(T^-2) and j_f=O(T^-1). These powers use the actual
Phi, including its fast AB term; that term is not silently discarded.

For the H tail, A(0)<=KT implies

    x_A >= (h0/4-3K²S)T³-(K+S)T.

Choosing h0>12K²S gives a positive order-T³ margin for sufficiently large T;
v_A=O(T³), so (21) is exp[-Omega(T³)]. Conditions (18) also hold eventually for
fixed positive K,M,d0. With Z(0)=0 and zmax=sqrt(T), m_Z=sqrt(T)/2 and
2KT Hbar=2Kh0/T. The exponent in (23) is asymptotic to (3/4)sqrt(T), giving
the printed imbalance rate. Choosing zmax=epsilon*T instead contributes
O(epsilon²) through the Zbar terms of rho and has an order-T exponent; the other
terms must still be retained. Constants need not be uniform as K,M or derivative
norms vary.

These statements do not make the full stochastic transport error O(T^-1): its
martingale bracket is O(T^-1), typically corresponding to O(T^-1/2) fluctuations.
For fixed precision x>0, (16) gives exp[-Omega(T)] under these fixed parameters;
this is a stopped probability statement, not a global CLT. No count-band decay
rate is inferred without inserting n(0) into its explicit thresholds.

## Adversarial checks and reproducibility

`independent_exact_audit.py` reconstructs propensities from source/product
complexes and falling factorials without importing the author checker. It passed
55 exact symbolic assertions, 4,608 rational-state cases, and 37,248 active-channel
checks. Checks include mixed degree-five observables, all product jumps, active
endpoint nonnegativity, segment derivative jump bounds, full brackets, and the
compact exponent ledger. The original author's 33 checks and 3,500-state result
also replayed exactly. These finite checks are supplementary, not universal
proof substitutes.

Two concrete adversarial witnesses show why tempting simplifications fail:

- For A=C=D=E=1, B=7, T=2, N=32 and f=l, the two fast rows contribute exactly
  1/512 to q_F even though both slow coordinates are fixed. Dropping the fast
  corrected bracket is false.
- For f=l², E=3, T=2, N=32, an immigration jump has Delta h=3 and Delta g=1.
  Omitting Delta h Delta g/(NT) misses exactly 3/64. Replacing h' by h in P is
  false even in this simplest channel.

The receiver also checked the proof-only attacks not settled by polynomial tests:
C² versus C³, derivatives peaking inside a segment, threshold-crossing endpoint
corrections, last-jump inclusion, zero occupation budgets, common-stop compensator
consistency, and initially thin count margins. The received formulas survive
with the stated conventions. No source algebra repair was necessary.

## Not received

This review does not acquire f, prove V dot Df=-1 for a useful clock, interpret
its boundary values, prove actual clearance, pay physical-window exits, extend
to growing K or M, establish near-blow-up/global transport, prove a global CLT,
or establish recurrence/mixing. A special clock's decreasing derivative weights
may be inserted into (5)-(9), but this review supplies no such derivative theorem.
