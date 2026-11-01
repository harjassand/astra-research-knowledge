# Actual remaining-clock residual with literal global weighted constants

**Author construction; independent review pending.** This compiles received
clock derivatives and source budgets into the accepted exact full-chain
corrector identity. It is an ordinary finite-jump residual calculation, not a
novelty claim, mixing theorem, ODE-tracking argument, bracket theorem, or an
unconditional clearance statement. All rate-2 channels remain actual.

## 1. Result, same-stop hypotheses, and useful finite N

Set N=T^5, T>=10^4, L=A+(C+D)/2, Z=C-D, l=L/T, e=E/T^3, and

    q=b(l,e)+AE b_l(l,e)/(NT),   phi=(1+e)^-2,
    K=800/171,                  J=404/17.

Use the ORIGINAL physical horizon 4T and raw state (A,B,C,D,E)=(0,N,1,1,0).
Receive the actual startup/gate construction, with its separately charged
failures: before actual L=400 entrance it gives L>=1, A<=2, Z=0,
E<8*400^3, elapsed time<=800; afterwards it gives L>=200 and
|Z|/L<=1/100, until the first other failure. The advertised A/L<=1/100 is
available but is NOT needed by this residual bound: A<=L suffices throughout.
Receive on the same pre-stop domain

    B>=.9N, L<=N/5000, E<=N/100, E^2/(NL)<=2,
    |S-N|<=12T,
    integral A phi dt <= K/T^2,
    integral CD phi dt <= J T^3,
    integral A dt <=1.                                      (1)

All integrals start at raw time zero and stop together. Source-budget first hits,
count/gate failures, and deadline are actual stopping rules, not conditioning on
a future good event. If a supplied budget is initially phrased as a good-event
bound, include its continuous first-hit stop and charge its already supplied
failure bound. No new source preparation or restart is allowed. The regularized
source retains its raw initial storage even across startup.

The exact corrected observable has

    Gq=-1/T+R_b,

and the following deterministic bound holds through this common stop:

    integral |R_b| dt <= r(T)
      :=11/20000 +4380/(19T)+7254/T^2.                       (2)

It includes the entire Taylor segments, changed AE target in the product rule,
all source/error terms, and the imbalance defect. It is not a growing-compact
norm bound. Conservative outward evaluations are:

| N | integer lower bound for T | r(T) upper bound |
|---|---:|---:|
| 10^20 | 10000 | .023675171579 |
| 10^21 | 15848 | .015124964612 |
| 10^22 | 25118 | .009739231335 |
| 10^23 | 39810 | .006345240677 |
| 10^24 | 63095 | .004205460580 |
| 10^25 | 100000 | .002855988558 |

All actual stopping targets satisfy the additional bound

    |AE b_l/(NT)|<=2/T^2.                                   (3)

At the raw state the correction is zero and

    s_*-1/T <= q(X_0)=b(1/T,0) <=s_*.                        (4)

Thus a received bracket can be joined without the avoidable 800/T startup time
loss. The shared startup derivative extension used for that assertion is proved
next; it is not an assumption that the ratio cone covers a zero-L target.

## 2. Shared derivative domain, startup, and full jump padding

Write psi_p(l)=min(1,l^-p), with psi_p(0)=1. The already received derivative
ceilings extend to the union

    D={l,e>=0:e^2<=3l} UNION {0<=l<=1, 0<=e<=1/1000}.        (5)

On D the same constants apply:

    |b_l|<=1, |b_e|<=6, b_ll<=9, b_le<=13, |b_ee|<=148.

For l>=1 the existing stronger bounds are unchanged:

    |b_l|<=l^-5/2, |b_e|<=1/(2l^2),
    b_ll<=(5/2)l^-7/2, b_le<=l^-3, |b_ee|<=5l^-5/2.

Here and below b_ll,b_le are nonnegative. Also |b_e|<=1/(2l^2) holds for every
l>0,e>=0: it follows directly from b_l<=0,b_e<=0 and the transport identity.

**Rectangle extension.** The only extra domain in (5) is the small-e rectangle.
For l<=1/2, the existing mixed-derivative proof splits the inverse flow at
L=1/2 and uses only e<=5/4, not e^2<=3l. Its logarithmic estimate gives
J_inf<12l^2. Consequently |b_e|<=J_inf/(2l^2)<6. Its integral estimate gives
b_le<13 and b_le<=150l^2. The identity

    b_ee=-(3/2)b_l-[3e/2+1/(2l^2)]b_le

gives |b_ee|<2349/16<148, even using the weaker e<=5/4. The global estimate
b_ll<=5sqrt(1+e) is <9 on this rectangle. For 1/2<=l<=1 use
b_le<=l^-3<=8, |b_e|<=1/(2l^2)<=2, and the same exact identity; its b_ee bound
is below18 when e<=1/1000. All assertions extend to l=0 by the already received
smooth forward-flow boundary extension, not singular substitution into inverse
formulas. In particular b_l(0,e)=-1. This establishes (5) with no new oracle.

**Actual startup segments.** Before the first startup failure, every enabled
endpoint has

    0<=l'<=401/T<=.0401,
    0<=e'<=(8*400^3+1)/T^3<1/1000.

The whole segment is therefore in the rectangle. This includes an adverse
endpoint with L'=0, and the actual stopping jump is retained. Startup sources
also have E^2/(NL)<64*400^6/N<2 by L>=1 and N>=10^20.

**Post-startup segments.** Every enabled jump has Delta L>=-1 and Delta E<=1.
At a source L>=200, l'>=(199/200)l>0. Since e^2<=2l and
E<=N/100, hence e<=T^2/100,

    (e')^2 <=2l+1/(50T)+T^-6 <=3(l-1/T)<=3l'.

The middle comparison follows from L>=200 and T>=10^4. The epigraph
l>=e^2/3 is convex, so its endpoint checks cover the ENTIRE straight segment,
including adverse exits. No ratio bound is assumed at a target without proof.

For the source-relative line suprema in the exact corrector identity this yields

    F20,r <=10 psi_(7/2)(l),
    F11,r <=14 psi_3(l),
    F02,r <=150 psi_(5/2)(l).                              (6)

For example 9(200/199)^(7/2)<10,
13(200/199)^3<14, and 148(200/199)^(5/2)<150. Startup has l<1 and the
un-inflated rectangle ceilings suffice. These three comparisons are checked
by exact rational arithmetic after squaring the half-integer cases. The first
and second derivatives therefore share the same declared padded domain as the
separate corrected-clock bracket construction; no third derivative is used.

## 3. The elementary weighted moment receiver

At every pre-stop source e^2<=2l. Independently,

    e<= (3/2)sqrt(l),
    (1+e)^2 <=2+4l <=6 max(1,l).

For nonnegative r,s and p>=1+r+s/2 this implies

    (1+e)^2 l^r e^s psi_p(l) <=6(3/2)^s.                  (7)

For p>=r+s/2 the unweighted version is

    l^r e^s psi_p(l)<=(3/2)^s.                            (8)

Both are proved by splitting l<=1 and l>=1. No relationship to the single
deterministic origin orbit is assumed. Combining (7) with (1) gives explicit
A-weighted and CD-weighted integral bounds. Combining (8) with integral A<=1
or the original horizon<=4T gives the two remaining types of charge.

For higher A powers use only

    A^a<=A L^(a-1) for a>=1,
    A^a CD<=L^a CD.

Consequently all monomials below have a literal integral charge. Two terms use
the unweighted A budget: the 3AL^2 term in r_h and A^2LE in the product-le
term. This avoids introducing a growing-l cutoff when the weighted exponent
would otherwise be too small. All other monomials use the weighted source
budgets or the fixed horizon.

## 4. Exact residual groups and their pre-integration bounds

The received exact corrector has

    R_b=b_l(A+AL-3A^2)/T
       +b_e[A(A-1)-2AE-2Q]/T^3
       +b_l r_h/T^6 +R2_b+P_b,
    Q=2AL-A^2+Z^2/4,
    r_h=E-3EQ+2ACD+A(A-1)^2+2CD
        +AE(N-B+2L+2-7A).

The coefficient of AE satisfies

    |N-B+2L+2-7A|<=12T+E+4L+2.

The exact ordinary jump/product formulas include h'_r=(A+Delta A)(E+Delta E),
not merely h=AE. On every enabled row h'_r<=(A+1)(E+1). The AB<->CD rows
have Delta l=Delta e=0, hence contribute ZERO to both R2_b and P_b; their fast
rates have not been assigned fictitious slow increments.

The actual slow-rate sums simplify to

    q_LL=1-A/2+A^2+AL/2+AE <=1+(3/2)AL+AE,
    w_LE=A(A-1)+AE <=AL+AE,
    q_EE=A(A-1)+2AE+2CD <=AL+2AE+2CD,
    s_L=1-A+A^2+AL+AE <=1+2AL+AE.                         (9)

All identities in (9) are reconstructed from the twelve literal rows by the
checker. Below a notation c psi_p P/T^k means its pointwise nonnegative
contribution to |R_b|. After separating the two Z^2 terms, the remaining groups
are bounded by:

| group | numerator polynomial including its coefficient | p | k |
|---|---|---:|---:|
| first l | A+2AL | 5/2 | 1 |
| first e, without Z | 6(5AL+2AE) | 2 | 3 |
| r_h, without Z or 12T term | E+10AEL+3AL^2+2CD+AE^2+2AE | 5/2 | 6 |
| r_h, 12T term | 12AE | 5/2 | 5 |
| Taylor ll | 5[1+(3/2)AL+AE] | 7/2 | 2 |
| Taylor le | 14(AL+AE) | 3 | 4 |
| Taylor ee | 75(AL+2AE+2CD) | 5/2 | 6 |
| product ll | 10(A+1)(E+1)(1+2AL+AE) | 7/2 | 7 |
| product le | 14(A+1)(E+1)(AL+2AE+2CD) | 3 | 9 |

This uses |b_l|<=psi_(5/2), |b_e|<=6psi_2 and (6). The Taylor coefficients
5 and75 retain the integral factor1/2; the mixed coefficient14 includes both
symmetric Hessian entries correctly. The product groups retain the FULL target
h'_r and exact first-order segment integrals; no third derivative, dropped
covariation, or small-mark approximation occurs.

For r_h we kept the actual 2CD term instead of unnecessarily replacing it by
2L^2, so its source budget can be used. We bounded
2ACD+A(A-1)^2<=3AL^2, and 3EQ<=6AEL+(3/4)EZ^2.
These are valid on all integer A, including A=0 and1.

**Imbalance terms.** Put epsilon=1/100. On startup Z=0; afterwards the received
cap gives Z^2<=epsilon^2L^2, so this holds at every source. The b_e contribution
is bounded using the sharper global |b_e|<=1/(2l^2):

    integral |b_e| Z^2/(2T^3) dt <=epsilon^2.

The r_h contribution uses e l^2 psi_(5/2)<=3/2:

    integral 3 E Z^2 |b_l|/(4T^6) dt <=(9/2)epsilon^2.

Their sum is exactly 11/20000. This constant is an admitted imbalance tolerance,
not an unpriced asymptotic term. A tighter actual imbalance budget would improve
it; no such improvement is assumed here.

## 5. Exact integrated polynomial and the simple bound

Apply (7)-(8) monomial by monomial to the preceding table. The complete result
is r_full(T)=sum_(n=0)^10 c_n/T^n, where

| n | c_n |
|---:|---|
| 0 | 11/20000 |
| 1 | 20+45K =4380/19 |
| 2 | 6+(537/2)K+252J |
| 3 | 60+312K+1164J |
| 4 | 24+936K |
| 5 | 2100K+168J |
| 6 | 40+180K+168J |
| 7 | 948K |
| 8 | 372K |
| 9 | 144K |
| 10 | 84K |

Every coefficient is nonnegative. For T>=10^4, exact fractions give

    c_2+sum_(n=3)^10 c_n/(10^4)^(n-2)
       <7253.765<7254.

This proves (2). The leading 4380/(19T) comes from the fully paid ll Taylor
term, not an ignored Ito/curvature correction. The entire positive product
contribution is included in the displayed coefficients. No signed cancellation
has been relied upon to advertise a small bound.

`check_residual_budget.py` expands each polynomial itself and assigns each
monomial to its weighted-A, weighted-CD, unweighted-A or original-horizon
receiver. Its report saves every such monomial receipt, the exact full
coefficients, the rational simplification, source hashes, and outward numerical
examples. It imports no derivative solver and performs no simulation. These
checks support the construction; an ordinary independent receiving review of
this document remains required.

## 6. Initial/terminal correction and a conditional timing interface

The sign b_l<=0 gives q<=b. At a post-startup stopping target, the padded cone
provides e<=sqrt(3l)<2sqrt(l). Since A<=L and |b_l|<=psi_(5/2),

    |AE b_l/(NT)| <=l e psi_(5/2)(l)/T^2 <=2/T^2.

At a startup target, l<=.0401,e<.001 gives a much smaller bound; the same
2/T^2 ceiling applies, including L=0 where A=0. Thus q>=-2/T^2 on the entire
stopped domain and every target. Formula (4) follows by integrating |b_l|<=1
along e=0 from l=0 to1/T. It does not require simulating a deterministic flow.

For an actual macro target `L>=N/5000 or E>=ceil(N/100)` while all preceding
admissions survive, a convenient terminal ceiling is

    q_target<=b_target<=3*10^6/T^6.                       (10)

Indeed b(l,e)<=l^-3/2 globally by the inverse-flow bound
L(w)>=l+3w^2/4 and its elementary integral. Thus an L-cap target costs at most
5000^(3/2)/T^6<355000/T^6. At an E-cap target the padded cone l>=e^2/3 gives
L(v)>=v^2/3 and b<=3/(2e^3)<=1.5*10^6/T^6. The larger displayed constant is
safe for both; actual successor geometry, not only source geometry, was used.

Let a separate received theorem supply a radius m for the martingale of THIS
q, on the SAME stopping rules, with failure delta_M. Add all separately supplied
admission/budget failures; do not condition the bracket inequality on their
good event. If

    s_*+2/T^2+r(T)+m<4,

then the usual stopped-clock contradiction proves that the macro target is
reached before original4T on the joint good event. Its physical hitting time
obeys

    s_*-1/T-3*10^6/T^6-r(T)-m
       <= tau_macro/T <=s_*+2/T^2+r(T)+m.                 (11)

The lower endpoint can be clipped at zero. This is a conditional macro timing
receiver. A separately received actual continuation (for example physical h=5)
may extend only the upper endpoint, using the actual exit state, and must add
its own failure. Earlier clearance must be excluded or paid separately. This
document does not acquire those gates, that bracket, or that continuation.

## 7. Exact limitations and source bindings

The derivative and regularized-storage sources were independently received
while this construction was in progress. Their source hashes are:

* GLOBAL_L_WEIGHTED_CLOCK_DERIVATIVES.md:
  20dff0a1775870b93aa81a12bb88125892f242a0986438b3ce9e63e0c4d83ccb.
* REGULARIZED_WEIGHTED_SOURCE_BUDGET.md:
  38973f8baacbadb5c8fdf63cac93e2aed49b7831883cd4c3943aff3e3ac10b2b.
* Accepted exact TASK_OBSERVABLE_CORRECTOR.md:
  02e55555d845f7f3060e23500cb36934fbfd4709eb8755c9b1ebf2cfa7002a94.

The checker binds these and the raw entrance/remaining-clock sources. It does
not turn an unreceived stochastic gate into an accepted one. In particular
upper-R survival and the regularized source's A/(E+T^3)<=2 gate remain supplied
admission obligations. The unweighted occupation clock must be stopped/paid,
not merely asserted typical. All estimates stop at FIRST failures.

No growing-K derivative norm, ODE trajectory tracking, fast-state equilibrium,
mixing, larger persistence strip, external source, installation, publication,
hardware experiment, or helper was used. No useful-bound obstruction was found
once the stated weighted source budgets are received. The remaining limitations
are explicit admission/bracket/continuation obligations and the fixed 1% imbalance
charge, rather than hidden residual constants.
