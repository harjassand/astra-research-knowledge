# Corrected finite-level induction clock with a finite-N error budget

**Author candidate, pending independent review.** This is an actual finite-level
hitting-time window. It is not a point-mass approximation in CDF distance.
The all-start positive-recurrence theorem and its freezes are unchanged.

## 1. Model, scales and exact finite statement

Use the exact rate-2 tree: unit-rate 0<->A, 2A<->AC, 2A<->AD, 2A<->AE,
AE<->CD, CD<->AB, except CD->AE has coefficient two. Start at
x_N=(0,N,1,1,0). Write T=N^(1/5), and let K>=10^40 and 0<a<=1/4.
Define

    Mbar=2sqrt(K+1), p=K+1, q=Mbar+1, H=p+q+1.

Assume N>=10^200 and

    T^2>=16H,   T^3>=64p^2,   T^2>=4pq/a.               (1)

For the full actual process put L_full=A+(C+D)/2 and
F=L_full-3E^2/(4N)+AE/N. Let t_K be its first L_full>=KT hit.
The ordinary scalar system

    l'=1+3l^2 e, e'=2l^2, l(0)=e(0)=0

has exact identity l(s)=s+3e(s)^2/4. Let s_K denote its first l=K time.
Its finite blow-up time is s_*<=2; s_K<2.

With probability at least 1-B_clock-B_A, where

    B_clock=10^5 H^6/(a^6 T),
    B_A=36 H^3 T^3 exp(1-KT/64),                         (2)

the following simultaneous actual conclusions hold:

    (s_K-a)T <= t_K <= (s_K+a)T,
    no A death or other remaining bad channel occurs before t_K,
    KT<=L_full(t_K)<=KT+1,
    A(t_K)<=KT/32+1, C(t_K)-D(t_K)=0,
    |F(t_K)|<=KT/8,
    sqrt(NKT)<=E(t_K)<=(13/10)sqrt(NKT).                 (3)

A negative lower time endpoint can be replaced by zero. The probability lower
bound is understood as its maximum with zero. No headroom or total-band event
is included in (2); those are separately priced by the original immigration
counter when the accepted dyadic stage is consumed.

## 2. Retained process and all omitted-channel cost

Retain immigration, AB->CD, CD->AB, CD->AE, AE->CD and AE->2A. Let I count
immigration, R count AE->2A, and S count AE->CD. Up to coupling failure,

    L=A+C=A+D=1+I+R,
    B=N-I-2R+A-E.

The omitted channels are actual A death, all three 2A exits, AC->2A and AD->2A.
Stop the retained chain at 3T, first L>=KT, or first E>=Mbar T^3, giving an
L hit priority over a simultaneous E hit. Throughout the pre-stop region and
one-jump targets, A,C,D<=pT and E<=qT^3. Equation (1) implies B>=N/2.
The retained A generator and omitted intensity are exactly

    L_ret A=1+3C^2-AB,
    q_rem=A+3A(A-1)+A(C+D)<=(1+5pT)A.

For compact notation let S0=3. Stopped Dynkin and nonnegative terminal A give

    E int AB <=4S0 p^2 T^3,
    E int A <=8S0 p^2/T^2 =: h0,
    E int AE <=8S0 p^2 q T =: g0.                       (4)

A standard common-clock coupling until the first omitted mark therefore costs
at most

    E int q_rem <=48S0 p^3/T.                           (5)

The same actual path is used until that event. Its probability is paid rather
than assuming rare channels never fire. All expectations are stopped; no
unrestricted absolute-occupation or uniform-integrability claim is inferred.

## 3. Corrected F directly removes the fast A error

The exact retained generator, with the SAME F, is especially simple:

    L_ret F=1+E/N+CD/(2N)+2ACD/N
               +AE[1+(3E-2A-3/2-B)/N].                (6)

It follows by summing the six literal F marks; no stationary A fiber is used.
The retained identities imply

    |N-B+3E-2A-3/2| <=5H T^3.

Using (4), CD=C^2<=p^2T^2 and N=T^5, the entire accumulated absolute drift
error satisfies

    E [(1/T)int |L_ret F-1|]
      <= S0[q+p^2/2+16p^4+40H p^2q]/T^2
      <=100 S0 H^4/T^2.                                (7)

The initial F/T is 1/T, not zero, and is retained below.

The immigration and AE->2A F marks have absolute size <=2 by (1).
All other retained F marks have absolute size <=H/T^2. Expected compensators
for AB, the two CD exits, and AE->CD are bounded respectively by
4S0p^2T^3, 3S0p^2T^3 and g0. Thus the predictable F martingale bracket obeys

    E <M_F> <=4S0T+4g0
       +(H^2/T^4)[7S0p^2T^3+g0]
       <=64S0 H^5 T.                                   (8)

This is a genuine order-T bracket, not an order-T^3 fast-event estimate.
Stopped Doob, (7), and Markov's inequality, splitting the tolerance a/4 into
martingale a/8 and initial-plus-drift a/8, give

    P(sup |F(sT)/T-s|>a/4)
      <=[16384S0 H^5/(a^2T)]
          +8/(aT)+800S0 H^4/(aT^2).                    (9)

The supremum is taken only up to the retained stopping time divided by T.

## 4. The E integral residual is priced separately

Let e_N(s)=E(sT)/T^3, l_N(s)=L(sT)/T. Write J for the CD->AE count.
Exactly E=J-R-S, with J compensator 2int C^2. Its stopped martingale satisfies
`E sup |M_J/T^3|^2<=8S0 p^2/T^3`.
Replacing C^2=(L-A)^2 by L^2 costs expected at most 32S0p^3/T^4 after the
scaled integration; (R+S)/T^3 has expectation at most 16S0p^2q/T^2.
Therefore, for

    eta_N(s)=e_N(s)-2int_0^s l_N(u)^2 du,
    epsilon=a^3/12,

Doob and Markov, each at tolerance epsilon/2, yield

    P(sup |eta_N|>epsilon)
       <=4608S0 p^2/(a^6T^3)+1152S0 H^3/(a^3T^2).      (10)

These are actual stopped counter errors, not a deterministic replacement of the
E death channels. Together (5), (9), (10), S0=3, H>=1, a<=1 and T>=1 are
bounded by B_clock in (2).

## 5. Scalar time-shift comparison, without exp(CK^2) Gronwall

On the two residual good events, (1) implies deterministically

    AE/(NT)<=pq/T^2<=a/4.

Consequently the exact corrected-variable identity gives

    l_N(s)=s+3e_N(s)^2/4+xi_N(s),  |xi_N|<=d=a/2,
    e_N(s)=2int_0^s l_N(u)^2du+eta_N(s), |eta_N|<=epsilon.

Both coordinates are nonnegative. Put w(s)=2int_0^s l_N(u)^2du, so w is
absolutely continuous even though e_N need not be monotone.
For the upper comparison z=w+epsilon>=e_N,

    z'<=2[s+d+3z^2/4]^2, z(0)=epsilon.

Since a>=d and e(a)>=2a^3/3>=epsilon, ordinary scalar comparison gives
`e_N(s)<=e(s+a)` whenever the latter is finite.
For the lower comparison,

    w'>=2[(s-d)+3(max(w-epsilon,0))^2/4]_+^2.

Hence w(a)>=(2/3)(a-d)^3=epsilon. For s>=a, z=w-epsilon is nonnegative and

    z'>=2[s-d+3z^2/4]^2>=2[(s-a)+3z^2/4]^2.

Thus `e_N(s)>=e(s-a)` for s>=a; the lower bound is zero before a.
Returning to the exact l identity gives the corresponding comparison

    l((s-a)_+) <= l_N(s) <= l(s+a),                       (11)

where each side is used only while its deterministic argument exists. This is
a pathwise time window, not a comparison of probability distribution functions.
No global Lipschitz exponential in K is paid: the actual scalar structure is used.

An E-boundary cannot occur before an L hit on these good events. At such an E
exit, 3e_N^2/4>=3(K+1), whereas before an L hit the F identity and its errors
bound that quantity by K+a/2. Thus the E exit is contradictory. The upper part
of (11) excludes an L hit before (s_K-a)T; the lower part forces an L hit by
(s_K+a)T<3T. For this last conclusion only e(s-a), not e(s+a) beyond blow-up,
is used. This avoids extending a compact fluid argument through its explosion.

## 6. Paid fast-A cap at the actual hitting time

The retained A upward intensity is 1+3C^2+AE; the downward intensity is AB+AE.
The elementary bounds exp(1)-1<2 and 1-exp(-1)>1/2 give

    L_ret exp(A)/exp(A)<=2+6p^2T^2+A(2qT^3-N/4)
                         <=2+6p^2T^2-NA/8.

Equation (1), and N>=10^200, make this nonpositive for every integer A>=1.
Each excursion starting at an actual 0->1 A crossing therefore reaches
ceil(KT/64) with conditional probability at most exp(1-KT/64), by stopping
exp(A) at zero, that cap or any other common stop. The expected number of these
excursions is at most the expected total upward count, bounded by

    S0T+3S0p^2T^3+g0<=12S0H^3T^3.

Sum conditional probabilities over the actual entry stopping times. No excursion
independence is assumed. This proves the B_A term in (2). It pays the supremum
of A up to the level hit, not only a deterministic-time sample of A.

On the joint good event the full and retained paths coincide, so C-D=0 and no
A death has occurred. The hit has KT<=L<=KT+1. The F estimate gives |F|<=4T,
which is <=KT/8 since K>=10^40. Also

    (4/3)(1-4/K)<=E(t_K)^2/(NKT)<=(4/3)(1+2/K).

This interval lies inside [1,(13/10)^2]. The A cap is stronger than KT/32+1.
Thus every non-mass entrance condition of the accepted full-chain dyadic stage
is actually earned at t_K, proving (3).

## 7. Costs and scope

All constants in this finite-level bound are explicit algebraic expressions.
The error prefactor is deliberately conservative and polynomial in K and a^-1;
it is not asserted small unless its displayed value is small. The enormous
accepted dyadic floor K>=10^40 remains honest. Conditions (1) and every error
term must be checked before consuming the bound at a finite N.
This proof supplies no macro clearance conclusion by itself. The accepted stage
requires a mass band and the actual interior theorem requires positive fractions
and its own size threshold. Both are received, with their full clock and count
costs, in a separate continuation source.
