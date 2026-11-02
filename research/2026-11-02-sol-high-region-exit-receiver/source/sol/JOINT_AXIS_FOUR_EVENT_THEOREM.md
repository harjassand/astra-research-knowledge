# A complete four-event operation on every sufficiently high joint axis

Author theorem for the full two-port raw reaction list, all positive block
and core rates. This closes the simultaneous high-anchor axes at the SAME
proper receiver as PROPER_HIGH_ANCHOR_RECEIVER.md. It does not close states
with a bounded anchor, and therefore is not a full six-species recurrence
theorem.

Write the two block rate lists as alpha,beta, core rates as kf,kb, and

    B0=alpha0+beta0,
    r=(alpha0 kf beta3/(beta0 kb alpha3))^(1/3)>0.

In the proper receiver choose eta1=1, eta2=r. Its constants may be bounded
using finite rational upper/lower bounds on this algebraic number. Keep all
the same functions Psi,h_i,g_i,c0,C and U from that construction.

THEOREM. There are finite raw-list constants N and epsilon>0 such that from
every x=(a,0,0,d,0,0), a,d>=N, at the fourth actual NONCORE reaction time tau4,

    E_x[U(X_tau4)-U(x)]<=-epsilon,
    E_x tau4<=4/B0.                                    (A1)

All intervening core jumps, arbitrary transfers and every competing source
are retained. Multiplying U once by max{1,(4/B0+1)/epsilon} gives the ordinary
same-receiver physical Foster contract at these axes. The generator contract
on every high-anchor hidden state survives that same multiplication.

## 1. Why the actual operation is finite and acquired

Before the fourth noncore event, a ready pair can exist ONLY after three
reactions of one block in the order0,1,2. The alternative own words after
three growths are000,001,010,011; mixed-port words also have no ready pair.
Thus all core motion before tau4 is either absent or is the complete
two-state motion of ONE ready pair, after a clean three-step preparation.
There is no stationarity assumption and no truncation of core activity.

At all times up to tau4 hidden count is<=8, each anchor changes by at most12,
and the state space visited from a fixed input is finite. Thus no explosion
is possible within the operation. The noncore hazard is always>=B0, proving
the physical bound in (A1). Every actual endpoint is evaluated at U.

The complete kernel is acquired by four forward propagations and the exact
two-state Green calculation below. four_nc_axis_kernel.py returns the full
rational output law for requested inputs, actual physical mean, and exact
rational coefficients of the two algebraic receiver weights. It does not
replace an expectation by an assumed numerical interface.

## 2. The complete clean-I Green operator

The probability that the first three noncore events are I0,I1,I2 is

    pI=(alpha0/B0)
       alpha1(a+1)/[alpha1(a+1)+B0]
       alpha2(a+2)(a+1)/
          [alpha2(a+2)(a+1)+alpha1(a+2)+B0].             (A2)

At this point x0=(a+3,2,2,d,0,0). The only core successor is
x1=(a+3,0,0,d,2,2). Define

    lI2=4alpha2(a+3)(a+2),  lII2=4beta2 d(d-1),
    k0=4alpha3(a+3)(a+2)(a+1)+lI2+2alpha1(a+3)+B0,
    k1=4beta3 d(d-1)(d-2)+lII2+2beta1 d+B0,
    f=4kf(a+3)d,  b=4kb(a+3)d,
    D=k0 k1+k0 b+f k1,
    o0=(k1+b)/D, o1=f/D.                               (A3)

These are the actual occupation times before the fourth noncore event.
Their killing weights sum to1: o0 k0+o1 k1=1. The transferred-exit probability,
including every noncore channel at its ACTUAL landing, is

    TI=pI o1 k1=pI (f/k0)/[1+f/k0+b/k1].               (A4)

The clean-II quantities are obtained by (a,alpha,kf)<->(d,beta,kb).
Call its transferred-exit probability TII.

For any physical endpoint put f_i=A_i-h_i, as in the common receiver. At all
inputs a,d>=8 the endpoints have f_i>0, so Q=f_1^2+r f_2^2 without truncation.
Core transport in the clean-I cell changes f from(a,d) to(a+3,d-3).
Every raw terminal leaves those f coordinates unchanged. Source2 at a ready
pair changes its own f by-1; all the other killing channels in this cell
leave f unchanged. Consequently the EXACT clean-I contribution to E delta Q is

    TI [6(a-rd)+9(1+r)]
      +pI o0 lI2(-2a+1)
      +pI o1 lII2 r[-2(d-3)+1].                        (A5)

Clean-II contributes the analogous formula, with transfer increment
-6(a-rd)+9(1+r). In particular the source2 terms are all nonpositive for
a,d>=4. No favorable terminal-only path has been substituted for the full
exit law.

## 3. Every other branch and every unpaid loan

Outside the two clean prefixes, no core event occurs before tau4. Direct
enumeration of the feasible source words shows the ONLY positive changes
of either f coordinate are the four-own-event words0011,0101,0110; each
raises that coordinate by1. All other nonclean branches leave both f
coordinates unchanged. Their probabilities are products of the complete
actual race probabilities, including both input channels.

For block I their sum PplusI satisfies the explicit bound

    PplusI<=KplusI/a^2,
    KplusI=alpha0^2/(B0 alpha2)
              +3alpha0^2 alpha1/(2B0 alpha2^2).          (A6)

For0011, bound the second zero-source probability by alpha0/(alpha1 a)
and the last source1 probability by alpha1/[alpha2(a+2)]. For0101 and0110,
the middle/last zero source contributes an additional inverse anchor factor.
The exact three products are implemented and separately matched to the full
kernel in four_nc_axis_kernel.py. Thus the total positive nonclean Q cost is
at most3KplusI/a+3r KplusII/d.

The work part of U is also completely paid. After four noncore events,
Psi<=8a_work, where a_work is the weight named a in the workload theorem.
On a terminal fourth event Psi=0. Put

    KI=(alpha0/B0)[B0/alpha1+(alpha1+B0)/alpha2],
    KII=(beta0/B0)[B0/beta1+(beta1+B0)/beta2].

(A2) gives 1-pI-pII<=KI/a+KII/d. Put

    D_axis=D_frontier+B0/min(alpha3,beta3).

On a clean cell, the nonterminal killing hazard at each ready location is
<=D_axis/A_i times its terminal hazard. The own lower sources use the already
proved exact divisions. The peer empty input is also charged: its rate is
<=B0, while the ready terminal is at least(8/9)alpha_i3 A_i^3; its ratio is
therefore <=B0/(alpha_i3 A_i). Thus every competing input is included. Hence

    P(Psi(X_tau4)>0)<=(KI+D_axis)/a+(KII+D_axis)/d.

With Kwork=C[(c0+8a_work)^2-c0^2], the complete work receiving increment is
therefore bounded by

    Kwork[(KI+D_axis)/a+(KII+D_axis)/d].                 (A7)

This receives even a last-event outward excursion or an unfinished packet
at the same globally proper U. It neither drops that endpoint nor presumes
a continuation law for it.

## 4. Comparable anchors: one compatible quadratic geometry

Fix any finite R>1 and set n=min(a,d), with 1/R<=a/d<=R. The expressions
(A2)--(A5) are finite rational functions with strictly positive leading
denominators uniformly on this compact ratio interval. Expanding those
explicit expressions, uniformly as n tends to infinity, gives

    TI=(alpha0 kf/B0 alpha3)d/a^2+O_R(n^-2),
    TII=(beta0 kb/B0 beta3)a/d^2+O_R(n^-2),

and the untransferred source2 terms in (A5) and its mate give

    -delta0+O_R(n^-1),
    delta0=(2/B0)[alpha0 alpha2/alpha3
                              +r beta0 beta2/beta3]>0.

Transferred source2 contributions are nonpositive and of order n^-1.
The transfer curvature, (A6) and (A7) are O_R(n^-1). Therefore

    E delta U = (6/B0)(a-rd)
        [alpha0 kf d/(alpha3 a^2)-beta0 kb a/(beta3 d^2)]
        -delta0+O_R(n^-1).                              (A8)

The bracket has the sign of r^3-(a/d)^3. Its product with a-rd is
nonpositive EXACTLY. This choice of receiving geometry comes from the raw
transfer and terminal coefficients; equal weights are not assumed suitable
for arbitrary rates. Thus the drift is <=-delta0/2 for all sufficiently large
comparable anchors. Every error in (A8) has been bounded above by finite
rational formulas, not by an asserted effective process.

## 5. Extreme anchor ratios: do not extrapolate (A8)

For all a,d>=8, k0 and k1 in (A3) lie between fixed positive raw multiples
of a^3 and d^3. The probability pI is bounded below by a fixed raw constant.
Consequently, when d>=R a with R>=1, there are fixed raw constants c,C such that

    c min(1,d/a^2)<=TI<=C min(1,d/a^2),
    TII<=C a/d^2.                                      (A9)

For example f/k0 is between raw multiples of d/a^2 and b/k1 between raw
multiples of a/d^2. Their exact common denominator in (A4) gives (A9).
The ratio (a/d^2)/min(1,d/a^2) is at most R^-3 if d<=a^2, and at most
1/(8R^2) otherwise. Thus choose a finite R large enough that TII<=TI/2,
and also a-rd<=-rd/2. The two transfer terms are then bounded above by

    -c' d min(1,d/a^2)+C' min(1,d/a^2).                 (A10)

All source2 terms are favorable. The remaining positive terms (A6),(A7)
are <=K(1/a+1/d), with fixed finite K. Enlarge the anchor threshold to absorb
the curvature term in (A10). If a>=N>=R, then

    d min(1,d/a^2)>=R^2.

Choose R first so this negative margin exceeds1, then N so the remaining
inverse-anchor errors are small. This proves a uniform negative margin on
the whole region d>=Ra, including d>>a^2 and arbitrarily larger scales.
The opposite extreme a>=Rd is identical with the ports interchanged. These
two extremes and the comparable band prove (A1) for ALL sufficiently high
joint axes, without freezing an inventory or anchor.

## 6. Actual consequence and remaining frontier

With this choice of eta and one common scale, every state with both anchors
sufficiently high now has an earned operation at the SAME proper U:
the actual generator handles every nonempty-hidden state; tau4 handles the
joint axes. All low-anchor landings are paid at U. Constants are finite and
have explicit inequalities; the final all-axis threshold N has not been
numerically materialized, and no practical-size head is claimed.

Exact finite diagnostics include comparable, equilibrium-ratio and extreme
axis inputs. The conservative constants make the receiver drift positive at
moderate anchors, and negative at the displayed sufficiently large inputs.
Those fixtures check the formulas; the all-axis result is the argument above.

The unresolved global region has at least one bounded anchor. It includes
unbounded interacting inventories and the outgoing operation at THIS U.
Prior central-face/star results do not supply that operation merely because
their receiver is also quadratic. Therefore full six-species recurrence and
arbitrary weak-reversibility recurrence remain unproved.

Multistep embedded-chain arguments are established methodology: Anderson,
Cappelletti and Kim, arXiv:1904.08967v2, Sections3.3 and6, Theorems3.1,4.1,6.1
and Lemma6.4. Their theorem requires one linkage class and its stated tier
condition (the main structural corollary is binary), which this diagnostic
does not satisfy. Here four counts genuine noncore reactions; every intervening
core path and its physical residence are solved rather than counted as four
raw jumps. No global novelty or priority claim is inferred from that distinction.
