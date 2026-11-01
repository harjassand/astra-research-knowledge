# Fully retained activated-to-macroscopic receiver

**Author theorem candidate, pending independent review.** All twelve actual
channels of the rate-2 tree are retained. This is a paid conditional interface,
not yet a global recurrence or stationary-tail theorem.

## 1. Exact assumptions and outputs

Use the actual count model in the uniform-growth source: unit-rate 0<->A,
2A<->AC, 2A<->AD, 2A<->AE, AE<->CD, CD<->AB, with CD->AE coefficient two.
Put S=A+B+C+D+E, R=C+D+E and M=A+min(C,D). Fix

    N>=10^40, r=1/1000, delta=10^-12,
    8<=k<=delta N,        S in (3N/4,2N],
    R>=4rN,              M>=k.

N is fixed reference mass; k is an integer. Define the main mass stop at either
S<=3N/4 (actual removal) or S>2N (adverse upper exit). Stop earlier on M>=delta N.
Starting with M>=delta N needs no dyadic construction. Otherwise the construction
below reaches macro M or a main mass stop, before time

    D_macro=256 N/k,

except on an event of probability at most

    8 exp(-k/3)+exp(-rN/100).                             (1)

The upper mass stop is explicitly adverse, not a service. A consumer must pay it.
At macro entry M lies in [delta N,delta N+1]; if no mass stop has occurred, S is
still in (3N/4,2N]. Section 5 supplies a further physical 1/N window which puts
all five counts above a fixed positive fraction of N, with error exp(-c_delta N).
Neither C-D balance nor a stationary A fiber is assumed.

## 2. Actual retention of the activated resource

Define J=R+2A+4M and Q=exp(-J/100). The exact J marks are:

- immigration +6, A death -6;
- each 2A channel -1 or -5;
- AC/AD->2A +1 or +5;
- AE->2A +5; AE->CD -1; CD->AE +1;
- both AB<->CD marks zero.

The last neutrality is essential. With theta=1/100, the elementary inequalities

    e^(6theta)-1<=7theta, e^(5theta)-1<=6theta,
    1-e^(-6theta)>=3theta, 1-e^(-theta)>=theta/2,
    e^(-5theta)+e^theta-2<=-3theta

hold. For the last, use e^(-5theta)<=1-5theta+(25/2)theta^2 and
e^theta<=1+theta+theta^2. Summing every actual source group gives

    LQ/Q <=theta[-3+7A+18A^2-A(C+D)/2-3AE-CD]
          <=theta[-3+7A+18A^2-AR/2-CD].                 (2)

On R>=2rN and M<delta N, A<=M, and
`7+18delta N<=rN/2<=R/4`. Thus LQ<=0 there.
Stop Q at macro M, a main mass stop, or the first R<=2rN, giving the macro/mass
outcomes priority at simultaneous jumps. At an R exit which is not such an
outcome, M<delta N and

    J<=2rN+6delta N<=3rN.

At initial entry J>=4rN. Optional stopping and positivity of Q therefore give

    P(R<=2rN before macro/mass stop)<=exp(-rN/100).        (3)

This covers the entire subsequent dyadic construction in one bound, including
all failed attempts and every adverse AE->CD jump. It is not a repeated fresh
probability cost at each stage.

## 3. A phase correction with negative CD startup cost

On all states define

    h_N=max(1/4,1-A/(4N)),       V_N=2^(-M) h_N.

While M<delta N and at its one-jump targets, clipping is inactive, h_N>=99/100,
and h_N<=1. Every positive M jump has A mark +1, every negative M jump has
A mark -1. If q_plus and q_minus denote their exact total intensities, then

    q_plus>=1+A(R-2M),       q_minus<=3A^2.

Indeed positive M jumps are immigration, AE->2A and the reverse arm belonging
to the strictly larger of C,D. If C=D only AE remains. These cases both imply
the displayed lower bound. The exact negative count is the previously verified
A+3A(A-1) at C=D and A+2A(A-1) otherwise.

Dividing by 2^(-M), a positive M jump contributes at most -49/100 times its
rate; a negative M jump contributes at most 101/100 times its rate.
For zero-M jumps, CD->AB and CD->AE together give EXACT phase reserve
`-3CD/(4N)`. The only adverse zero-M phase marks are AB->CD, AE->CD and at most
one of the 2A arm exits, of total intensity at most AB+AE+A(A-1).
All other zero-M marks are favorable. Consequently

    LV_N/2^(-M)
      <=-49/100 -(49/100)AR +(401/100)delta N A
           +(1/2+delta/4)A -(3/4)CD/N.                 (4)

Here S<=2N bounds B+E, and A,M<=delta N bound the remaining positive terms.
For R>=2rN, N>=10^40,

    (401/100)delta N+1/2+delta/4 <=(24/100)R.

Thus (4) is at most `-49/100-AR/4-3CD/(4N)`. Since R>=A and N>=1,
`AR>=A^2/N`, and `A^2+CD>=M^2/2`. Finally h_N<=1 gives

    LV_N<=-[M^2/(8N)]V_N.                               (5)

The CD startup cost now has the favorable sign. The small AB phase expense is
paid by actual M-increasing reverse arms/AE returns. This is why the initial
cutoff potential and this activated potential are different constructions.

## 4. Actual dyadic stages and their cost

Take integer stage level j and an entrance with M>=j (if already M>=2j, skip
this stage). Stop on M>=min(2j,delta N), M<=floor(j/2), any main mass stop,
R<=2rN, or the deadline

    T_j=128N/j.

While this stage continues, M>j/2, hence (5) implies
`LV_N<=-[j^2/(32N)]V_N`. Initial V_N<=2^(-j). At a lower-M exit V_N is at least
`(99/100)2^(-floor(j/2))`. Ordinary optional stopping therefore bounds that
exit before any other outcome by

    (100/99)2^(-j/2)<=2exp(-j/3),                        (6)

using log2>=2/3. If no exit occurs by T_j, then M<2j and V_N>=(99/100)2^(-2j).
The integrating-factor inequality gives

    P(no exit by T_j)<=(100/99)exp[j log2-4j]
                       <=2exp(-3j).                    (7)

Here log2<=1. Combine these as a conservative `4exp(-j/3)` stage failure.
There is no restriction on the stage entrance beyond the stated actual region
and M>=j; in particular no E/F matching or C-D balance is needed.

Use j_i=2^i k, skipping any already-crossed levels, and stop at the first actual
M>=delta N. Mass outcomes have first priority, macro M second, then resource
exit and auxiliary lower boundary. Terminal M overshoot is at most one.
Conditional stage estimates apply to the continuing actual state; only analysis
clocks restart. The deadlines sum to at most 256N/k. Since k>=8, the failures
sum to at most 8exp(-k/3). Add the single resource failure (3) to obtain (1).
No immigration estimate is hidden in this conditional disjunction.

## 5. Macro M gives compact positive fractions, with an actual paid window

Set

    eta=delta^4/(1000*3^40),  rho=eta exp(-100)/4.

At a macro entry with S in [3N/4,2N], normalize counts by N. The internal
polynomial field F is

    a'=-3a^2+a(c+d-b)+3cd,  b'=cd-ab,
    c'=a^2-ac+ae+ab-3cd,   d'=a^2-ad+ae+ab-3cd,
    e'=a^2-2ae+2cd.

Its mass is constant in [3/4,2]. On this set

    a'>=-6a+3cd, b'>=-2b+cd,
    c'>=-6c+a^2, d'>=-6d+a^2, e'>=-4e+a^2+2cd.

At entrance a+min(c,d)>=delta. If a>=delta/2, then for 0<=t<=1,
`a(t)>=delta exp(-6)/2`. For 1/2<=t<=1 the c,d,e coordinates are at least
`beta=delta^2 exp(-18)/8`; hence
`b(1)>=beta^2 exp(-2)/2=delta^4 exp(-38)/128`.
All five coordinates at time 1 exceed eta, using exp(1)<3.
If min(c,d)>=delta/2 instead, then c,d>=delta exp(-6)/2 throughout;
variation of constants gives

    a(1)>=3delta^2 exp(-18)/4,
    b(1)>=delta^2 exp(-14)/4,
    e(1)>=delta^2 exp(-16)/2,

and c,d retain their displayed bounds. Again all five coordinates exceed eta.
This proof uses only differential inequalities, not a global-attractor theorem.

For completeness the actual short-window concentration is paid directly. Put
Y(u)=X(u/N)/N and stop at actual total >3N. The sum of physical intensities is
at most 32N^2 before that stop; every coordinate mark is at most 1/N. Each
coordinate martingale has squared-mark compensator at most 32/N over u in [0,1].
The exact scaled drift is

    F(Y)+(a/N)(2,0,-1,-1,-1)+(1/N^2)(1,0,0,0,0).

The correction has infinity norm at most 7/N. On the cube [0,3]^5 the infinity-
norm Lipschitz constant of F is at most 100 (row sums of its exact Jacobian).
Stopped Freedman and Gronwall therefore give, for N>=28exp(100)/eta,

    P(sup_[0,1] ||Y(u)-phi_u(Y(0))||_infinity>eta/2)
      <=10 exp[-N rho^2/(2(32+rho/3))].                 (8)

Indeed each martingale is kept within rho, and 7/N<=rho. Its Gronwall envelope
is at most eta/2. Such closeness also rules out the 3N upper stop, including its
terminal jump: the deterministic total is <=2 and the coordinate error is much
less than 1/5. Thus (8) is an actual full-chain window, not a stopped claim with
an unpriced escape. At physical time 1/N, all five actual counts are at least
eta N/2 on its good event. A consumer may treat a prior hit S<=3N/4 as removal
instead; otherwise the compact-positive entrance is received. If S<=2N there,
B,C,D,E are at least epsilon S for epsilon=eta/4.

## 6. Scope and construction costs

All potential formulas use the actual state and fixed reference N. The dyadic
sum is finite, with no independence or restarted process assumption. Exponential
supermartingales are justified by finite mass localization and nonexplosion from
S(t)<=S(0)+I(t). All constants are explicit; practical magnitude is not claimed.
The exponent eta in the positivity receiver is extremely small, so its threshold
may far exceed 10^40. This is an honest existence cost, not a numerical claim.

This component still assumes an activated R entry and a seed M>=k. It explicitly
returns a mass-exit disjunction and does not identify upper exit with success.
An arbitrary-state consumer must earn those entrances, price immigration and
receive the interior theorem before claiming actual fixed fractional removal.
