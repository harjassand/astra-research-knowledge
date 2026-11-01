# A paid interior removal block for the actual rate-2 chain

**Author component theorem; not independently reviewed.** This component begins
with fixed-positive fractions of B,C,D,E, permits A=0, acquires a positive
relative-composition region, and removes a fixed fraction of the actual total.
It does not assume stochastic mixing, a product-Poisson law for the actual chain,
or favorable next-reaction choices. It is not an entrance theorem from arbitrary
boundary states and is not by itself a recurrence or stationary-tail theorem.

## 1. Exact statement

The actual CTMC has unit-rate 0<->A, 2A<->AC, 2A<->AD, 2A<->AE,
AE->CD, CD<->AB, and rate-2 CD->AE. Binary propensities use falling factorials,
so each 2A-source propensity is A(A-1), not A^2 or A(A-1)/2. Let S=A+B+C+D+E.

**Interior removal theorem.** Fix 0<epsilon<=1/4. There are finite
n0(epsilon) and c(epsilon)>0 such that, for every integer n>=n0(epsilon) and
every initial actual state satisfying

    S(0)=n,    B(0),C(0),D(0),E(0)>=epsilon n,    A(0)>=0,

    P[S(5)<=7n/8] >= 1-exp[-c(epsilon)n].                 (T)

Time 5 is physical time in the specified unit-rate convention. The constants are
uniform over the displayed initial states. Their existence construction is below;
no practical numerical bound on n0 is claimed. In particular, using epsilon=10^-100/4
is mathematically allowed, but the constants obtained here are not evaluated.

The stronger intermediate service statement is: except for the charged error,
either S has already reached 3n/4, or after a deterministic time tau_epsilon/n<=1
the actual composition stays in a fixed compact positive region until that hit
or time 5. Throughout the latter interval A>=n/8. The region and all tube margins
are explicit; the deterministic entrance time is an ordinary compactness/global-
attraction constant, not a stochastic equilibrium assumption.

All counts can be realized by independent unit-rate Poisson clocks with their
actual integrated intensities. Since S(t)=n+I(t)-D(t)<=n+I(t), where I is rate-one
immigration and D is the actual A-death counter, the chain is nonexplosive.

## 2. Internal deterministic field and its ordinary supplier

On the unit simplex, write p=(a,b,c,d,e). The homogeneous binary field is

    F_a = -3a^2+a(c+d-b)+3cd,
    F_b = cd-ab,
    F_c = a^2-ac+ae-3cd+ab,
    F_d = a^2-ad+ae-3cd+ab,
    F_e = a^2-2ae+2cd.                                    (1)

Its coordinates sum to zero. Put

    s=(sqrt(7)-1)/2,    q=(2/9)(1,s^2,s,s,2-s).

Here 1+s^2+2s+(2-s)=9/2, so q has total one, and F(q)=0.
The already constructed internal competitor reduces 2A->AC and 2A->AD to rate s
and adds 2A->CD with rate 1-s. Its deterministic field is identically (1).
It is complex balanced at q, has one strongly connected binary linkage class,
and its stoichiometric subspace is the full sum-zero hyperplane. For example,
the A-to-C, A-to-D, and A-to-E differences and the CD-to-AB difference have rank 4.
The actual stochastic generator is NOT replaced by the competitor's generator.

The only imported ordinary deterministic theorem is global attraction of the
positive complex-balanced equilibrium in a positive compatibility class for a
single-linkage complex-balanced mass-action system. The already-received source
is David F. Anderson, *A proof of the Global Attractor Conjecture in the single
linkage class case*, arXiv:1101.0761v6, Corollary 4.11, printed page 20. See
`../rate2_dyadic_continuation/DETERMINISTIC_SOURCE_RECEIPT.md` for the parent-authorized
source receipt. No further source was retrieved for this component. This supplier
is used on the INTERNAL competitor only; the full open network has a separate
port linkage and is not described as single-linkage.

Write

    H(p)=sum_i p_i log(p_i/q_i),
    D(p)=-grad H(p) dot F(p).

Complex balance gives D>=0 on the positive simplex. Equality forces every binary
complex monomial ratio p^y/q^y to coincide. Comparing 2A with AC, AD, AE, then CD
with AB, forces all five species ratios p_i/q_i equal; total one makes p=q.
Thus D>0 away from q in the positive simplex. This entropy identity and
homogeneity transfer to the actual deterministic field, not an actual stationary law.

## 3. A=0 is included: explicit deterministic positive entry

Let phi_t be the flow of (1), and let K_epsilon be the closed initial simplex
region with b,c,d,e>=epsilon. For every trajectory from this region,

    b(t)>=epsilon exp(-t),
    c(t),d(t)>=epsilon exp(-3t),
    e(t)>=epsilon exp(-2t),
    a(t)>=a(0)exp(-3t)+epsilon^2[exp(-3t)-exp(-6t)].        (2)

Indeed F_b>=-b, F_c>=-3c, F_d>=-3d, F_e>=-2e, and
F_a>=-3a+3cd on the unit simplex. Variation of constants gives the last inequality.
At time 1 every coordinate is therefore at least

    eta_epsilon=epsilon^2 exp(-3)[1-exp(-3)]>0.             (3)

Thus phi_1(K_epsilon) is a compact subset of the strictly positive simplex.
Every one of these trajectories converges to q by the stated deterministic
supplier. The following is the receiving argument which makes the entry time
uniform, rather than assuming that pointwise attraction is uniform.

## 4. Explicit entropy margins and a uniform entrance construction

Put

    q_* = min_i q_i = (2/9)s^2,
    h = q_*^2/64,
    L_H = 1+log(2/q_*),
    alpha = min{1/100, q_*/100, h/(100 L_H)}.               (4)

Pinsker's inequality gives ||p-q||_1<=sqrt(2H(p)). In particular,

    H(p)<=2h  ==>  p_i>=q_i-q_*/4>=3q_*/4,
                   p_A>=1/6.                             (5)

For each point of phi_1(K_epsilon), global attraction gives a time when H<h/8.
Continuous dependence gives an open neighborhood on which H<h/4 at that time.
Take a finite subcover. Entropy is nonincreasing, so at the largest of these
finitely many times every point has H<h/4. Consequently the following integer
exists and is finite:

    tau_epsilon = least integer t>=1 such that
                  sup_{p in K_epsilon} H(phi_t(p))<=h/4.  (6)

One may use any certified larger integer instead. This is an existence
construction, not a supplied numerical certificate for (6). For a computable
epsilon it can also be realized, without stochastic simulation, by enumerating
rational compact covers and validated finite-time integration of the polynomial
ODE, using the strict h/8-to-h/4 margin. The finite-cover argument proves that
such a search has a terminating certificate; it supplies no efficient cost bound.

For repeated local inward flow the entropy contraction constant can be explicit:

    kappa = (1-s)/486 = (1-s)q_A^2/24,
    D(p)>=kappa H(p) whenever H(p)<=h,
    Delta = 2/kappa.                                     (7)

Here is a direct proof, rather than an uncomputed local spectral premise. Put
r_i=p_i/q_i and u_y=p^y/q^y. On H<=h, Pinsker implies r_i in [1/2,3/2].
Complex balance rewrites the dissipation as

    D = sum_(y->z) k_yz q^y [u_y log(u_y/u_z)-u_y+u_z]
      >= sum_(y->z) k_yz q^y (sqrt(u_y)-sqrt(u_z))^2.

For the 2A->Ai edges i=C,D,E, their individual contributions are at least
s q_A^2 (r_A-r_i)^2/12 (the E edge has the larger rate 1).
This uses r_A/(sqrt(r_A)+sqrt(r_i))^2>=1/12. The two edges
2A->CD->AB have flux coefficients (1-s)q_A^2 and s^2 q_A^2;
s^2>(1-s). The sum of their contributions is at least

    [(1-s)q_A^2/2][r_A-sqrt(r_A r_B)]^2
       >= [(1-s)q_A^2/24](r_A-r_B)^2.

These selected edges are distinct. Since 2s>=1-s, their sum proves
D>=kappa sum_(i!=A)(r_i-r_A)^2. The q-weighted mean of r_i is 1, so

    H = sum q_i[r_i log r_i-r_i+1]
      <=sum q_i(r_i-1)^2
      <=sum q_i(r_i-r_A)^2
      <=sum_(i!=A)(r_i-r_A)^2.

The first inequality follows from the bound 1/r<=2 on [1/2,3/2]; the second is
the minimizing property of the weighted mean. This proves (7).

If a deterministic state z has mass m in [3/4,9/8] and normalized entropy <=h,
its mass remains m, and its normalized flow obeys p'=mF(p). Hence
H(phi_u(z)/m)<=H(z/m)exp[-(3/4)kappa u]. At fast time Delta this is at most
h exp(-3/2)<h/4, while throughout it is <=h. This is the needed inward margin
on every repeated window; merely staying in the same compact set would not
suffice for concatenation. All local constants are explicit algebraic/logarithmic
expressions; only the initial global entrance time (6) remains an existence constant.

If z,w have masses at least 3/4 and ||z-w||_infinity<=alpha, then

    ||z/|z|_1-w/|w|_1||_1 <= (40/3)alpha.                 (8)

When the normalized deterministic w has H<=h, Pinsker and (4),(8) imply that the
whole line segment between normalized z and w has every coordinate >=q_*/2.
On that region H is L_H-Lipschitz in l1. Hence

    |H(z/|z|_1)-H(w/|w|_1)| <= 2h/15.                    (9)

Consequently:
* deterministic H<=h along a window gives actual H<=17h/15<2h;
* deterministic endpoint H<=h/4 gives actual endpoint H<=23h/60<h/2<h.

The same endpoint implication applies to the entrance window at tau_epsilon.
The derivative estimate is needed only at its endpoint, not along its possibly
non-interior initial portion. A discrete crossing of the lower mass threshold
is a removal success and needs no normalization estimate after the crossing.

## 5. Short-window concentration for the FULL actual chain

Keep n fixed as the reference initial total. Put Z(u)=X(u/n)/n, with fast time u.
Until the total reaches 2n, the exact scaled drift is

    b_n(z) = F(z)+(a/n)(2,0,-1,-1,-1)+(1/n^2)(1,0,0,0,0). (10)

This includes all three falling-factorial corrections, every binary channel,
actual A deaths, and immigration. It follows directly by summing their actual
stoichiometric vectors. In particular ||b_n-F||_infinity<=5/n for n>=1.

Every actual channel changes each coordinate by at most one. The sum of all
actual intensities at total S is bounded by

    3A(A-1)+A(B+C+D+2E)+3CD+A+1 <=6S^2+S+1.

Before S reaches 2n this is at most 27n^2. Thus each coordinate of the stopped
scaled martingale has jump bound 1/n and predictable bracket at most 27R/n on
a fast-time interval of length R. Exponential martingale/Freedman bounds and a
union over five coordinates give, conditionally on any initial history,

 P[sup_{u<=R}||M(u)||_infinity>r]
    <=10 exp[-n r^2/(54R+2r/3)].                          (11)

Stopping additionally at S<=3n/4 is permitted. Formula (11) includes the
stopping jump. No conditional equilibrium or mixing statement is being used.

On [0,2]^5 the l-infinity Lipschitz constant of F is at most 40, by its Jacobian
row sums. Comparing with the internal ODE of the same initial state, Gronwall gives

    sup||Z(u)-phi_u(Z(0))||_infinity
       <=exp(40R)[sup||M||_infinity+5R/n]                 (12)

up to the stated stops. Define

    r_R = (alpha/2)exp(-40R),
    c_R = r_R^2/(54R+2r_R/3),
    n_R = ceil(10R exp(40R)/alpha).                       (13)

For n>=n_R, a window of length at most R has tracking error <=alpha except
with probability 10 exp(-c_R n). This bound is uniform over all starting states
of mass <=9/8. A concentration-good path starting in that mass range cannot hit
2n before the low-total success, since the deterministic mass is constant and
the available mass gap is greater than 5alpha. For an interval shorter than R,
the same R-based constants bound its martingale and perturbation costs.

## 6. Concatenation on a finite PHYSICAL interval

Let

    sigma = inf{t:S(t)<=3n/4},    t_0=tau_epsilon/n,
    n >= max{512,tau_epsilon,n_tau_epsilon,n_Delta}.       (14)

The first concentration window has fast length tau_epsilon. Unless sigma has
already occurred, (6),(9),(12) give H(X(t_0)/S(t_0))<h/2.
After t_0 partition physical time up to 5 into windows of length Delta/n, with
a possible shorter final window. At each full endpoint, (7),(9),(12) restore
H<h/2; the next window is therefore allowed to start in H<=h. Throughout a good
window before sigma, H<2h. There are at most 5n/Delta+1<=5n+1 such windows.

The immigration event

    G_I={I(5)<=n/8}

ensures S(t)<=9n/8 for all t<=5. The local estimates are NOT conditioned on this
future event. At each actual window start, apply (11) conditionally on its past
when that start lies in the allowed mass/entropy region, and union-bound these
past-measurable local bad events. On G_I all needed mass hypotheses then hold.
This prevents an illicit future-event conditioning of martingale estimates.

The total concentration cost is at most

    10 exp(-c_tau_epsilon n)+(50n+10)exp(-c_Delta n).       (15)

On the complement of these errors and on G_I, either sigma<=5, or throughout
[t_0,5] the actual state has S>3n/4 and H<2h. Equations (5),(14) yield

    A(t)>=S(t)/6>=n/8,
    integral_0^5 A(t)dt >=(5-t_0)n/8>=n/2.                (16)

The physical service here is actual A occupation. It has not been inferred from
a deterministic stationary ratio on a single long window, which would incur
an exp(O(n)) Gronwall factor. The O(n) short windows each have a fresh inward
margin and a uniform exp(-c n) cost; only the explicit union factor accumulates.

## 7. Actual death and immigration clocks finish the removal

Let D(5)=Y_D(Lambda_D(5)) with Lambda_D(5)=integral_0^5 A(t)dt and Y_D a unit-rate
Poisson process. This exact time-change identity does not require independence
between Lambda_D and Y_D. On the event sigma>5 and G_I,

    D(5)=n+I(5)-S(5)<3n/8.

If (16) holds, this implies Y_D(n/2)<3n/8. The ordinary Poisson lower tail gives

    P[Y_D(n/2)<3n/8] <=exp(-n/64).                        (17)

For n>=512 the rate-one immigration upper tail gives

    P[G_I^c]=P[Poisson(5)>n/8]<=exp(-n/64).                (18)

If sigma<=5, then irrespective of subsequent binary dynamics or deaths,

    S(5)<=3n/4+[I(5)-I(sigma)]<=7n/8 on G_I.              (19)

Combining (15)--(19), with

    c_0=min{c_tau_epsilon,c_Delta,1/64}>0,

proves the explicit pre-absorption bound

    P[S(5)>7n/8] <=100(n+1)exp(-c_0 n).                   (20)

For an explicit existence recipe, choose the first integer N_abs>=2/c_0 with
log(100(N_abs+1))<=c_0 N_abs/2. It exists, and the inequality persists for every
n>=N_abs because c_0 n/2-log(100(n+1)) is then increasing. Take n0(epsilon)
to be the maximum of N_abs and the thresholds in (14), and c(epsilon)=c_0/2.
This proves (T). The dependence on epsilon is only through the uniform entrance
constant tau_epsilon and its concentration cost; the local tube is universal.

## 8. What has been acquired and what is still external

Supplied/received:
1. An actual initial state with B,C,D,E each at least epsilon times its actual total.
2. The exact deterministic drift-equivalent competitor and the stated ordinary
   single-linkage global-attraction theorem, with its hypotheses checked above.

Acquired here:
1. A=0 allowed; explicit strictly positive deterministic entry at fast time 1.
2. A uniform finite deterministic entropy-entry time for the entire input compactum.
3. A paid actual-chain entropy-tube entry, all channels retained.
4. O(n) paid local inward windows, giving actual occupation service on O(1)
   physical time with total error O(n exp(-c n)).
5. Actual death and immigration accounting yielding fixed-fraction total removal.

Not acquired here:
* A uniform entrance to the input region from arbitrary chain states.
* An exponential-probability entrance from the earlier boundary/mesoscopic phase.
* A computable practical numerical value of tau_epsilon or the very large n0.
* Recurrence, stationary exponential moments, or a geometric Foster function.
* Any changed dynamics, operational controller, new hardware, or publication.

For the neighboring dyadic component's stated output, B>=N/2,
C,D>=delta N/2, E>=sqrt(delta)N/2 and actual total <=(1+delta)N imply this input
with epsilon=delta/4 (delta=10^-100). That is a conditional composition statement;
the dyadic lemma and its entrance errors retain their own review burdens.

## 9. Verification scope

`check_interior_algebra.py` checks the actual drift (including port and falling
factorials), exact competitor drift equivalence, complex balances, stoichiometric
rank, exact equilibrium, total mass drift, and analytic numerical margins.
`check_results.json` records its output. Optional ordinary ODE samples are explicitly
illustrations only; they do not certify the uniform global entry constant (6) or
replace the proof. No stochastic simulation is needed or used in the theorem.
