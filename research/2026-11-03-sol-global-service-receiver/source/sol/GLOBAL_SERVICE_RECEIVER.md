# One common quadratic receiver pays all actual terminal/core switches

Author theorem for the live six-species raw list. This is a GLOBAL
terminal/core operation, not the complete reaction generator or recurrence.
It improves the routing identity by paying its actual source-profile
transport instead of requiring a false uniformly bounded two-sided law.

Use Q=eta1 A^2+eta2 D^2 and the exact routing reward v in
DYNAMIC_PACKET_ROUTING_AND_SWITCH_COST.md, with its continuous service
extension at zero anchors. Let J1=floor(min(B,C)/2), J2=floor(min(E,F)/2),
S=B+C+E+F. For a raw constant R chosen below define

    W=Q-J1 v1(A,D)-J2 v2(A,D)+R S^2.                 (1)

## 1. Acquired one-sided profile transport

There is a finite raw constant C such that increasing the I anchor by1
obeys, over ALL nonnegative anchors,

    (delta_A v1)_+<=C,
    (-delta_A v1)_+<=C(1+A),
    |delta_A v2|<=C.                                 (2)

The symmetric statements hold for increasing D. Negative off-diagonal
transport can occur in the positive routing domain only when the OTHER
terminal reward is larger. The large derivative at D~A^2 is negative
diagonal transport, which is compatible with (2).

Here is an elementary acquisition proof, including the relevant ratios.
For a,d>=3 put t=alpha3(a-1)(a-2), u=beta3(d-1)(d-2),
f=kf d,b=kb a. With p1=t(u+b)/Delta, p2=bt/Delta,

    v1=c2+p1(c1-c2), v2=c2+p2(c1-c2).

Both p1,p2 increase with a. Since t'/t and b'/b are1+O(1/a), with raw
uniform constants even at a=3, their positive rational formulas give
0<=delta p_i<=C p_i/a<=C/a. Thus when c1>=c2, each delta v_i is positive
and bounded by a raw constant: c1-c2<=C a. When c2>c1, the positive
delta v1 is at most6eta1 and

 delta p1 = fu[delta t (u+b')+delta b t]/(Delta Delta'),
 p2 <= C a^3/[d^2(a^2+d)].

Use t comparable to a^2, u comparable to d^2 and Delta>=u(t+f).
The first formula times c2-c1<=C d bounds the negative delta v1 by
C a(d^2+a)/(a^2+d)^2<=C a. For v2 its negative part is at most
C(d/a)p2<=C a^2/[d(a^2+d)]<=C. The direct reward increment is bounded.
All constants are finite expressions of the fixed positive rates/weights.
At a=0,1,2 the displayed service extension and the 2x2 formulas give
the same bounds directly; a1->2 changes no profile when d>=3, and
a2->3 has p1'=O(1/d), p2'=O(1/d^3). At d=0,1,2 and a>=3 the two
profiles both equal c1 and increment by6eta1. Remaining cases are finite.
This proves (2), without a boundary oracle or a transported-profile premise.

For the unit blocks,kf2,kb1,eta1=eta2=1, C=100 is a concrete sufficient
choice. In fact for a,d>=3, delta p_i<=3p_i/(a-2). If a>=d this gives
delta v_i<=60. If a<d, the exact delta p1 formula bounds
(-delta v1)_+<=20a, and p2<=9a/(2d^2) bounds
(-delta v2)_+<=81. The a=0,1,2 cases are bounded by15, and the
zero/low peer cases by9 or6. This earns100, rather than fitting it to data.

## 2. The actual remaining inventory pays every terminal switch

A terminal on i changes its anchor by-3 and J to J'=J-e_i. Telescoping
the THREE one-unit upper bounds in (2) gives

    -sum_j J'_j [v_j(A-3e_i)-v_j(A)]
                         <=3C(J1+J2-1)<=3C S/4.       (3)

The actual J_i-1 is retained, including zero. Combining (3) with the exact
terminal/core cancellation identity gives

    L_service[Q-sum J_i v_i]<=3C S lambda_terminal,total/4.

Core conserves S; each terminal has delta S=-4. On an enabled terminal
S>=4, so delta(S^2)=-8S+16<=-4S. Choose

    R>=3C/8+1.                                      (4)

Then globally, at EVERY physical state,

    L_(all terminals+all core) W
           <=-(1+S) lambda_terminal,total.             (5)

At both-low anchors no terminal is enabled; v=0 and the core generator
of W is0. At a zero anchor core is disabled, and the active terminal's
reward/profile identity is checked directly. Thus (5) has no omitted
zero face, actual landing, or unbounded hidden-inventory restriction.
It pays actual terminal activity with an inventory-weighted margin.
It does not charge every core event or the residence while only growth
can activate service.

## 3. Properness and the actual common boundary values

Let eta_min=min eta_i, eta_max=max eta_i. The acquired profile is
nonnegative and v_i<=6eta_max(A+D). Also J1+J2<=S/4. Therefore

 Q-sum J_i v_i >=eta_min(A+D)^2/2
                              -3eta_max(A+D)S/2.

Taking in addition R>=1+9eta_max^2/(4eta_min), Young's inequality gives

    W>=eta_min(A+D)^2/4+S^2.

The reverse quadratic bound is immediate. Hence this is ONE explicit
proper globally quadratic receiver, with no fiber/transport oracle.
For the unit diagnostic R=100 satisfies both choices and proves (5).
On every bounded-anchor layer, W=R S^2+O(S), with a raw layer-dependent
coefficient; it has the same leading radial form as the banked low receiver.
An O(S) difference is not claimed automatically received by those episodes.

## 4. Newly created packets must be valued at the NEW source profile

For a growth on i, let delta J_i be0 or1 and v' the profile at its actual
new anchor. Its exact own packet/profile contribution groups as

    -delta J_i v_i -(J_i+delta J_i)(v_i'-v_i)
                  =J_i(v_i-v_i')-delta J_i v_i'.       (6)

Because v_i'>=0, the newly created packet has NO positive own switch debt.
The positive diagonal cost is at most C(1+A_i)J_i. When A_i>=3 and J_i>=1,
multiply by any actual own growth propensity. Exact factorial division
and J_i<=min(B_i,C_i)/2 imply

    sum_(own growth s) lambda_s
       [J_i(v_i-v_i')-delta J_i v_i']_+
                      <=C' lambda_terminal,i.         (7)

For instance source2/terminal equals
alpha2/[alpha3(A_i-2)(B_i-1)(C_i-1)], and
J_i/[(B_i-1)(C_i-1)]<=1. The source0/1 ratios are smaller. If J_i=0,
the positive own diagonal debt is EXACTLY zero, even on the packet-creating
growth. This is a source-sensitive raw payment, not a two-sided O(1)
transport assertion. General degree/diagonal-kernel similarity alone
would not give the new-packet cancellation (6).

## 5. What is still unclosed

The full generator adds all six genuine growth channels to (5). Their
radial S^2 contribution, anchor increment, and OFF-diagonal profile change
remain. An unready port J_i=0 can have arbitrarily fast source1 or source2
growth while its own terminal is exactly disabled. At A_i=2 an existing
ready inventory can activate a new terminal source; before that growth
its own terminal is again zero. These actual activation paths and all
competing peer paths must be paid at (1), or at a proved compatible
regularization of it. They are not covered by dividing by an unavailable
terminal propensity. Even on bounded-anchor layers an O(S) receiving
difference cannot simply be discarded.

Thus the false unbounded-profile obstruction has been replaced by an
earned GLOBAL service inequality and a paid ready-source transport rule.
The remaining leverage point is actual activation/ordinary-growth
repayment and its common receiving error, not another stationary-fiber
estimate or a uniform profile Lipschitz assumption. Full six-species
and arbitrary weak-reversibility recurrence are still unresolved.
