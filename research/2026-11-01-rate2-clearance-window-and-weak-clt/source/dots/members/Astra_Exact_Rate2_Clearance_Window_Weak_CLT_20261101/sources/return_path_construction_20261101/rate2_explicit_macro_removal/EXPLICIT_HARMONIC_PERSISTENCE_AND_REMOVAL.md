# Explicit actual macro persistence and removal, without an interior ODE supplier

**Author theorem candidate, pending independent review.** This uses only the
actual count generator, rational phase geometry and paid count martingales.
It does not invoke deterministic global attraction or stochastic mixing.

## 1. Model, exact assumptions and service

Use the rate-2 tree: unit 0<->A, 2A<->AC, 2A<->AD, 2A<->AE,
AE<->CD and CD<->AB, except CD->AE has coefficient two. Binary propensities
are falling factorials. Write S=A+B+C+D+E and M=A+min(C,D).
Fix a reference integer N and a rational 0<m0<=10^-6. Set

    h=400/m0^2,             N>=32h.

For EVERY actual initial state satisfying

    3N/4<S(0)<=5N/4,        M(0)>=m0 N,                 (1)

one has

    P[S(h)>13N/16] <= B_pers+B_A+B_D+B_I,               (2)

where the fully explicit quantities are

    B_pers=32N^2 h exp(-m0 N/1000),
    B_A=exp[-200N^2/(32h+20/3)],
    B_D=exp(-N/2),          B_I=exp(-N/96).              (3)

A state already at S<=3N/4 can instead be received as immediate removal,
with its future immigration separately paid. The reference N is fixed, and all
actual channels are retained. No favorable path or attempt independence is used.

## 2. A smooth neutral coordinate and the falling-factorial phase

Define c=A+C, d=A+D, and

    H=2cd/(c+d) for c+d>0, H=0 otherwise,
    W=H-100A(A-1)/N,       Q=exp(-W/400).               (4)

Exactly M<=H<=2M and A<=M. Both AB<->CD and BOTH CD<->AE directions preserve
c,d. This removes their large neutral traffic from H. The falling factorial in
W is essential: when A=0, a CD exit creates A=1 and has ZERO phase increment.
Replacing it by A^2 would introduce an adverse CD/N startup cost.

We prove that in the actual source region

    3N/4<S<=2N, 1000<=H<=10^-6 N, N>=200000,             (5)

    GW>0, Gamma_W<=200 GW, |Delta W|<=3,
    GQ<=-Q GW/800<=0.                                   (6)

Here G is the full actual generator and Gamma is the full squared-mark intensity.
Every target, including exits, is evaluated by the SAME globally defined (4).

## 3. Exact drift and rational curvature costs

Let V=max(C,D), X=V+E, and s=c+d. Direct differentiation gives

    H_c=2d^2/s^2, H_d=2c^2/s^2,
    1<=H_c+H_d<=2,
    Hess H=-(4/s^3)[[d^2,-cd],[-cd,c^2]].

Its operator norm is <=4/s. Every nonzero (c,d) mark has entries in {-1,0,1}
and squared length <=2. Since s>=2H, Taylor's entire one-jump remainder is
bounded below by -4/(s-2)>=-4/H in (5). These are actual finite marks, not a
fluid-limit expansion with an unpriced remainder.

The exact c,d drifts and H-changing intensity are

    Gc=1+A+A(d+E)-3A^2,
    Gd=1+A+A(c+E)-3A^2,
    q_H=1+A+3A(A-1)+A(C+D+E).

The linearized harmonic drift is at least
`1+A+AV/2+AE-6A^2`: use 2(c^3+d^3)/s^2>=max(c,d)/2>=V/2.
Paying curvature with q_H gives

    GH>=1+A+AV/2+AE-6A^2
             -(4/H)[1+A+3A^2+A(C+D+E)].                (7)

The exact falling-factorial generator is

    G[A(A-1)]=-6A^3+10A^2-2A+2A^2(C+D)+2AE
                    +6ACD-2A(A-1)B.                   (8)

Use A<=H, CD<=H V, C+D<=2V, and C+D+E<=2V+E. Combining (7)-(8), with
H>=1000, H/N<=10^-6 and N>=200000, proves the uniform lower bound

    GW>=99/100 +(49/100)A X-6A^2-12A
                         +(200/N)A(A-1)B.             (9)

The margins are literal: the V coefficient is at least
`1/2-8/H-1000H/N>=.491`; the E coefficient is at least
`1-4/H-200/N>=.995`. The accumulated linear-A losses are less than 12A,
and the constant is at least .996. Nonnegative 600A^3/N and 200A/N were dropped.

If B>=N/4, (9) becomes

    GW>=.99+.49AX+44A^2-62A.

For integer A>=2, the last two terms are >=10A^2. For A=1, H<=2M implies
X>=min(C,D)>=H/2-1>=499; for A=0 the constant suffices. Therefore

    GW>= (1+AX+A^2)/4,            if B>=N/4.             (10)

If B<N/4, then X>=(S-A-B)/2>=(1/4-10^-6/2)N. In (5),
`6*10^-6 N+12<=.24(1/4-10^-6/2)N`. Thus (9) instead gives

    GW>=.99+AX/4,                if B<N/4.              (11)

Both cases include A=0 and arbitrarily unbalanced C,D.

## 4. Full variance and exponential lower barrier

Every actual H mark has absolute size <=2 (one coordinate changes by one, or
both change together and H_c+H_d<=2). Every falling-factorial mark has absolute
size <=2A, including its zero mark at A=0. Thus |Delta W|<=2+200*10^-6<3.
The full intensity is

    q_all=1+A+3A(A-1)+A(C+D)+2AE+3CD+AB.

In (5), q_all/N^2<=13*10^-6: use S<=2N, A<=10^-6N and CD<=2NH.
Consequently, using (u+v)^2<=2u^2+2v^2,

    Gamma_W<=8q_H+(8*100^2 A^2/N^2)q_all
            <=8+34A^2+16AX.                            (12)

Equation (10) pays this with factor 200. In case (11),
`A^2<=5*10^-6 AX`, so the same factor is more than sufficient. Hence
Gamma_W<=200GW everywhere in (5).
For theta=1/400 and |z|<=3, Taylor's integral remainder and exp(3/400)<2 give
`exp(-theta z)-1<=-theta z+theta^2 z^2`.
Summing every channel yields (6). No phase averaging or omitted rare event occurs.

## 5. Actual persistence over a fixed physical horizon

Stop globally at S<=3N/4, S>2N, H<=m0 N/2 or h, with main mass
outcomes taking priority at simultaneous marks. Start with H>=M>=m0N.
Every lower hit must occur in an excursion entering H<m0N from above. Since
H jumps by at most two, that entrance has H>=m0N-2. Until return to H>=m0N
or any global stop, its source region lies in (5): N>=32h and m0<=10^-6 ensure
m0N/2>=1000 and N>=200000.
At the excursion entrance,

    W>=m0N-2-100m0^2N.

At a lower H exit, W<=H<=m0N/2 because A(A-1)>=0 on integer states.
The difference is at least (2/5)m0N, by the same size assumptions. Optional
stopping of Q therefore gives a conditional lower-hit probability at most

    exp(-m0N/1000).                                     (13)

Before the global upper mass stop, q_all<=32N^2. Hence the expected number of
actual downward entry crossings during h is <=32N^2h. Sum (13) at those entry
stopping times: no independence is assumed. The probability of a lower H hit
before a main mass stop and before h is at most B_pers.
On persistence, H>m0N/2 implies M>=H/2>m0N/4.

## 6. From persistence to actual A occupation

The exact A generator implies, on every count state,

    GA>=3M^2-A(1+6M+B).                                 (14)

To verify, write x=min(C,D), y=max(C,D)>=x and M=A+x. Substituting y>=x in
the positive term A(C+D)+3CD leaves the difference from (14) equal to
`1+3A+2Ax>=0`. Since M+B<=S<=2N, (14) gives

    GA>=(3m0^2/16)N^2-13NA                              (15)

before the persistence/main stops. Stop additionally at int A dt=4N.
If no stop occurs before h and this clock has not hit 4N, the actual A martingale
satisfies

    M_A(h)=A(h)-A(0)-int GA
           <=2N-75N^2+52N^2<=-20N^2.                  (16)

Every A mark has absolute size one, and its stopped bracket is <=32N^2h.
The bounded-mark exponential-martingale inequality therefore bounds (16) by
exactly B_A in (3). This earns the occupation clock rather than assuming it.

## 7. Actual deaths, original immigration and the endpoint

Use the actual unit-rate immigrant count over the WHOLE fixed interval [0,h].
Since N>=32h, Chernoff at log2 and log2>=2/3 give

    P[I(h)>N/16]<=exp(-N/96)=B_I.                        (17)

On its complement, S(t)<=S(0)+I(h)<=21N/16<2N, so every adverse upper mass
exit is excluded. If S has hit 3N/4 at any earlier time, its continuing total at
h is <=3N/4+N/16=13N/16, paying all unused time.

If no such lower hit occurs, and persistence and (16)'s good event hold, the
actual clock int A dt must hit 4N by h. At that time the death count is a unit
Poisson clock evaluated at 4N. Survival S>3N/4 and (17)'s good event require
fewer than 2N deaths, since the initial total is <=5N/4. This event is contained
in {Pois(4N)<2N}, regardless of correlations with the occupation clock. Chernoff
bounds it by exp[-2N(1-log2)]<=exp(-N/2)=B_D.
Thus one of the four explicitly priced errors is necessary for S(h)>13N/16.
This proves (2). All upper exits, failed lower excursions, port deaths and waiting
time are charged on the continuing actual process.

## 8. Exact costs and intended interfaces

The entire receiver is explicit rational arithmetic, exponentials and ordinary
Poisson/martingale inequalities. Its very conservative h=400/m0^2 is enormous
for the tiny macro fractions used by earlier stages. It is not a practical bound.
For the N^(1/5) stage endpoint one may use m0=delta/2, yielding h=1600delta^-2;
then the size condition is N>=51200delta^-2. All previously unevaluated interior
attraction constants disappear from this receiver. Joining it to a first-passage
or all-start theorem still requires a separate exact composition check, including
its upper entrance S<=5N/4 and the original episode's immigration headroom.
No arbitrary connected-network or changing-rate result is claimed.
