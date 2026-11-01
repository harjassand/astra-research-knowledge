# Conditional adaptive ratio admission: complete drift, small endpoints, paid bracket

**Author theorem candidate, pending independent source-level receipt.** This
receives two additional path gates from the root. It does not establish those
gates, their entrance charge, or the ultimate inverse-cubic return consumer.
The outward witnesses against the earlier broader domain remain preserved.

## 1. Precisely what is received

N is fixed, T=N^(1/5), and S is the actual total count. Use the complete cubic
F2 from `COMPLETE_CUBIC_CONSTRUCTION_AND_OBSTRUCTIONS.md`, with the canonical
zero-at-A=0 algebraic inverse. Stop before leaving

    .99N<=S<=1.01N, E/N<=.01, A<=L/100, |Z|<=L/100,
    R=E²/(NL)∈[1/2,2], E^5>=32N³, L>=100,                 (D)

and **additionally receive**

    |S-N|<=E/100,
    theta_A=A²N/(L³E)<=1/100.                             (G)

The second gate is genuinely adaptive; A<=L/100 alone does not imply it. The
root owns its actual fast-A excursion/admission proof. Likewise (G)'s count
band is not silently substituted for a previously charged event. If the root
has earned |S-N|<=C T from the original immigration/death ledgers, then

    E>=2T³ and T²>=50C  imply  |S-N|<=E/100.

This is only a deterministic implication. Its stochastic entrance/count cost
must be received separately, including the actual source-storage entrance
charge. No equilibrium preparation is assumed.

Let r=R, u=E/N, t=1/L, a=A/L, z=Z/L and delta=S/N-1. The domain is equivalently
contained in the explicit rational constraints

    1/2<=r<=2, 0<u<=1/100, 0<t<=1/100,
    0<=a<=1/100, |z|<=1/100,
    |delta|<=u/100, t²/u<=r²/32, a²t/u<=1/100.             (9)

All exact jumps are those of the twelve-channel count model.

## 2. Uniform actual inward drift

On every physical state in (D),(G),

    | GF2/(EL/N) - [4-3R-RN/(EL²)] | <6/5.               (10)

This is a bound on the **full actual generator**, not only its algebraic
reference average. It retains the degree-four actual/reference discrepancy and
every parameter jump created by the complete cubic inverse.

Consequently the following two inward bands are certified:

    R∈[1/2,3/5]  =>  GF2 > (9/10) EL/N,
    R∈[9/5,2]    =>  GF2 < -(1/5) EL/N.                   (11)

For the lower band, t²/u<=r²/32 gives
4-3r-rt²/u>=11/5-27/4000; subtracting 6/5 leaves
3973/4000>9/10. For the upper band the last term is nonpositive, so
4-3r-rt²/u<=-7/5, and adding 6/5 leaves -1/5.

These are local generator statements on the received domain. They do not by
themselves say the chain remains there or that a terminal boundary is reached.

## 3. Ordinary proof of the uniform bound: exact factorizations and majorants

Write the complete correction from (4) of the construction note as

    chi=h1 a+h2 a²+h3 a³.

Its exact rational coefficients admit the useful polynomial splitting

    h1=u[delta H_d+t H_t+u H_u],
    h2=u²H_2, h3=u³H_3.                                 (12)

There is no asymptotic equality here. To acquire this splitting, expand the
numerator of h1 after s=1+delta and remove its common u factor. Assign every
monomial with a delta factor to delta H_d; of the remaining monomials assign
those with a u factor to u H_u; the remaining monomials all have a t factor and
are assigned to t H_t. Divide the h2 and h3 numerators by u² and u³. The code
asserts all required divisibilities. The denominators are the existing exact
rational denominators, not approximations.

For h1,h2,h3 these positive denominators have the respective forms

    C r²(2-t)²(1-t)²(1+t)^epsilon(2+t)² P^m,
    P=r(1+delta-u)+2u²(1-t),
    (C,m,epsilon)=(48,3,2),(8,2,2),(3,1,0).               (13)

The entire parameter segment of a single actual reaction is covered by

    49/100<=r<=21/10, u,t<=11/1000, |z|<=3/100,
    |delta|<=22/100000.                                  (14)

The A value held fixed after its jump corresponds to a segment a-value at most
(51/50)(a+t). In fact all required segment ratios for r,u,t and reciprocal r
are bounded by beta=51/50. This follows from L>=100 and E>=5000, which follow
from (D), and the actual unit/half-unit increments. Also

    |delta_segment|<= (11/1000) u_pre,

because its only new total-count increment is at most 1/N, and
1/E=ut/r<=1/5000. This proves that (14) is an actual one-step padding, not an
assumed future state.

### 3.1 Explicit continuous-domain coefficient bounds

The checker covers the full r interval in (14) with 65 rational subintervals
of width at most 1/40. On each interval [r_-,r_+], every numerator is bounded
by the sum of the absolute values of its monomials, with r replaced by r_+
and the small variables by their stated absolute bounds. For derivatives,
multiply each monomial by its relevant exponent and decrease that exponent
when taking an unweighted derivative. Denominators are bounded below by (13),
using

    P>=r_-[1-(22/100000)-(11/1000)]>0.

Quotient derivatives use the explicit logarithmic derivatives of (13). For
example r-weighted differentiation contributes at most

    2 + m r_+[1+(22/100000)+(11/1000)]/P_min.

The t,u,delta derivatives are bounded by the equally explicit individual
factor derivatives. All constants and comparisons use Fraction arithmetic.
The boxes cover continua; this is **not** inference from a positive finite grid.
Full per-box rational bounds are saved in
`adaptive_uniform_drift_certificate.json`.

For the mean, expand the numerator of Dbar-[4-3r-rt²/u] after s=1+delta.
Its denominator is 64 times the common r²/four-factor denominator times uP³.
Use |delta|^j<=100^-j u^j. A monomial with one remaining negative u power
necessarily has at least t²; substitute t²/u<=r²/32. The checker asserts this
property for every monomial. The remaining factors are ordinary nonnegative
powers bounded on each of 60 rational r intervals covering [1/2,2].

### 3.2 All three actual drift pieces are charged

The reference-average error is bounded as just described. The frozen mismatch
in normalized power coefficients is exactly

    E_fast/(EL/N)=
      -3a² h1/u
      +[-6a³+5a²t-8at] h2/u
      +[-9a^4+15a³t-24a²t-3a²t²] h3/u.                  (15)

For parameter motion with A+Delta A held fixed, the physical differential
operators are

    partial_L=-t(r partial_r+t partial_t+a partial_a+z partial_z),
    partial_E=(ut/r)(2r partial_r+u partial_u),
    partial_Z=t partial_z,
    partial_S=(u²t/r) partial_delta.                     (16)

Use (12), the certified coefficient bounds, and integrate these derivatives
along each actual parameter segment. No parameter jump is replaced by an
unbounded formal derivative at a single point.

The actual normalized absolute parameter rates obey

    s_L/L² <= t²+at+2a²+a+ar/u,
    q_EE/L²<=a²+2+2ar/u,
    q_Z/L²<=2a,
    q_S/L²=t²+at.

The only potentially singular product in this bound is the AE contribution
through H_t. Its precise factor is a(a+t)t/u, and it is paid by

    a(a+t)t/u <= 1/100 + (1/100)(2²/32)=9/800.            (17)

Here the first term is the received adaptive gate and the second is the
received lower-scale gate. Count-displacement terms instead use
|delta|/u<=1/100. This is the step that was invalid on the earlier domain.

The exact rational majorants from the complete calculation have the following
conservative ceilings:

| normalized contribution | rigorous upper bound |
|---|---:|
| algebraic mean minus 4-3r-rt²/u | 8/25 |
| full frozen mismatch (15) | 1/10000 |
| all L parameter motion | 813/1000 |
| all E parameter motion | 17/5000 |
| all Z parameter motion | 1/100000000 |
| all S parameter motion | 1/100000000 |

Their sum is less than 6/5. The computed (non-rounded) rational total is about
1.135945645, but that decimal is not used for acceptance. This proves (10).
The entire arithmetic is replayed by `certify_adaptive_drift.py`.

## 4. Small endpoints and actual jump/bracket costs on the broader domain

A separate continuous rational majorant, using the same exact coefficient
formulas but the larger one-step box

    r∈[.49,2.1], u,t<=.011, a<=.03, |z|<=.03,
    |S/N-1|<=.011,

proves

    |F2-R|<1/1000                                        (18)

at every pre-stop state in (D) and at every one-jump exit endpoint. It also
proves the following physical-coordinate derivative bounds on that box:

    |partial_A F2|<=3ut,  |partial_L F2|<=3t,
    |partial_E F2|<=3ut,  |partial_Z F2|<=ut,
    |partial_S F2|<=ut.                                 (19)

In (19), A,L,E,Z,S are independent smooth coordinates, with N fixed. The proof
uses exact polynomial majorants and denominator lower bounds, not samples.
Its full record is `uniform_derivative_and_endpoint_certificate.json` and its
replay is `bound_derivatives_and_bracket.py`.

In particular (u_segment t_segment)/(ut) is at most
(1+1/5000)/(1-1/100)<51/50. Accounting for these segment ratios, the actual row jumps satisfy

    |Delta F2|<=(51/50)[3ut|Delta A|+3t|Delta L|
                        +3ut|Delta E|+ut|Delta Z|+ut|Delta S|].

Since every A jump has magnitude one, and q_EE,q_Z,q_S<=q_A, Cauchy gives

    Gamma(F2)<=50t² q_LL+110u²t² q_A.                    (20)

No fast-channel jump was treated as order one: AB↔CD have only the A term,
weighted by ut. Immigration and all competing reactions remain in (20).
Also E>=2T³ and r<=2 imply t<=1/(2T), hence every jump satisfies

    |Delta F2|<=2/T.                                    (21)

The exact pointwise full rates used below are

    q_LL<=1+A+2AL+AE,
    q_A<=1+AB+3CD+A(3L+2E).

## 5. Paying (20) by actual weighted occupations

Let e=E/T³ and take physical horizon h=s0 T. Before the physical-domain exit,
define the actual stopped integrals

    H2=integral A e^-2 ds,
    J2=integral CD e^-2 ds.

On e>=2, R∈[1/2,2], E/N<=nu=1/100, S/N<=1.01, direct polynomial inequalities
give

    U_L:=integral t²q_LL ds
       <=s0/(4T)+(T^-2+16T^-1+2T)H2,

    U_A:=integral u²t²q_A ds
       <=s0/T^5+[5153/(1250T)]H2+12J2/T^6.              (22)

For the second inequality use A's unweighted occupation only through
integral A<=nu²T^4 H2, an immediate consequence of e<=nuT². In particular
no stochastic time change was introduced. Therefore a deterministic pair of
received stopped bounds H2<=Hbar, J2<=Jbar yields

    bracket(M_F2)<=v2=50 U_L(Hbar)+110 U_A(Hbar,Jbar).      (23)

With Hbar=O(T^-2), Jbar=O(T³), this is O(T^-1). The finite formulas, not the
asymptotic notation, are the certificate.

For completeness the weighted storage in the preserved component pays these
budgets on this very domain. Indeed B>=cN with c=2449/2500, while

    C+D+8A+12E <.121N <B/2.

Thus W2=A/e²+3T³/e satisfies the full generator inequality

    G W2<=e^-2-[(AB/2)+CD]e^-2.

Let Q2 be the integral of the bracketed quantity times e^-2. For any admitted
entrance inside (D), its actual deterministic cost is

    D_entry=W2(0)+h/4
            <=D*=T/50+(3/2)T³+h/4.

Choose the explicit clock ceiling Qbar=2D*. The actual W2 jumps are at most 2,
and before this clock hits its ceiling its bracket is at most
4h+96Qbar. At a clock exit its martingale must be at least D*. The usual
bounded-jump exponential inequality therefore gives the literal bound

    P(Q2 exits before another physical stop)<=exp[-D*/418].

On the complement,

    H2<=4D*/(cN),       J2<=2D*.                          (24)

This conservative choice of a known ceiling does not pretend the actual
entrance cost is always Theta(T³); it remains valid if that cost is smaller.
For sharper costs keep D_entry explicitly. The probability in (24) concerns
only the weighted occupation clock, not the adaptive A/count/ratio exits.

Combining (21)-(24), the actual stopped F2 martingale satisfies

    P(sup |M_F2|>=x)
      <=2 exp[-x²/(2(v2+2x/(3T)))],                       (25)

with the weighted-clock exit charged separately. This is a complete actual
bracket/jump payment, not a frozen-A variance formula.

## 6. What is now usable, and what is still owed

The same fully acquired cubic F2 now has:

* uniform inward full drift near both R faces, **conditional on (G)**;
* uniformly small one-jump endpoint correction;
* an actual all-channel bracket paid by explicit weighted clocks;
* exact negative witnesses showing why the earlier weaker hypotheses failed.

It still does not pay the probability of entering or retaining (G), the fast-A
adaptive excursion bound, the original count event, or the final boundary/
return consumer. The root must join those operations with the actual entrance
charge. An uncharged assertion that the path remains in the adaptive region
would invalidate the proposed admission theorem.

`test_adaptive_envelope.py` also replays all earlier mechanisms after imposing
the added cap and S=N or N±100 floor(T): all twelve rational replays have inward
sign. Those tests are supplementary falsification checks. The **uniform** proof
is the continuous-domain coefficient and polynomial-gate argument above.
