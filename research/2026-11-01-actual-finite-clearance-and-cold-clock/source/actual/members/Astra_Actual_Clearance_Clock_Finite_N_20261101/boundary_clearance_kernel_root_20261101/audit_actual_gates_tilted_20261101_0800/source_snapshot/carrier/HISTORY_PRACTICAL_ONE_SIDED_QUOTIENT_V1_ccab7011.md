# A practical one-sided ratio quotient, with no mesoscopic entrance gate

**Author component, pending independent receipt.** This is a separate construction.
The complete cubic F2 construction, its two-sided counterexamples, and all earlier
freezes are unchanged. No stationary fast-A law, time change, or acquired entrance
is used here. All twelve actual rate-2 channels are included.

## Useful result first

Put `S=A+B+C+D+E`, `L=A+(C+D)/2`, `Z=C−D`, and let N be the fixed reference.
For

    R=E²/(NL),     V=R−4AE/(3NL),

consider actual states satisfying

    3/2 <= R <= 2,       L >= 100,       0 < E/N <= 1/100,
    0 <= A/L <= 1/100,   |Z|/L <= 1/100,
    |S−N| <= E/50.                                      (1)

The full finite-jump generator satisfies

    G V <= −R/(L+1) −4E/[3N(L+1)]
           −(4L²−Z²)/(6NL) −AE/(8L) < 0.                (2)

There is **no** `E^5>=32N³` assumption. In fact, the drift proof permits
`A/L<=1/5`; the sharper cap in (1) is used for the clean cost statement below.
The actual narrow count event `|S−N|<=12N^(1/5)` implies the count gate in (1)
on this upper-ratio region. That event itself is a separate, charged input.

The observable differs from R by at most `1/7500` before the stop and by less
than `3/10000` at a one-jump exit endpoint. Its complete actual bracket can be
paid by two positive source storages, **without a deterministic time horizon**.
For a local excursion with L bounded below by a received M>=100, the resulting
bracket is O(1/L_entry+1/E_entry), with explicit clock-exit charges below.

By contrast, the original `F1=R−RAE/(NL)` has an exact outward upper-face
witness even with S=N and the other requested practical gates. The quotient
change is substantive, not an appeal to closeness of corrected observables.

## 1. Literal chain and normalized exact generator

The twelve channels, in the order used by the scripts, are

| channel | rate | (ΔA, ΔL, ΔE, ΔZ, ΔS) |
|---|---:|---|
| 0→A | 1 | (1,1,0,0,1) |
| A→0 | A | (−1,−1,0,0,−1) |
| 2A→AC | A(A−1) | (−1,−1/2,0,1,0) |
| AC→2A | AC | (1,1/2,0,−1,0) |
| 2A→AD | A(A−1) | (−1,−1/2,0,−1,0) |
| AD→2A | AD | (1,1/2,0,1,0) |
| 2A→AE | A(A−1) | (−1,−1,1,0,0) |
| AE→2A | AE | (1,1,−1,0,0) |
| AE→CD | AE | (−1,0,−1,0,0) |
| CD→AE | 2CD | (1,0,1,0,0) |
| CD→AB | CD | (1,0,0,0,0) |
| AB→CD | AB | (−1,0,0,0,0) |

For a row with `(ΔA,ΔL,ΔE)=(b,v,w)`, the exact quotient increment is

    ΔV = [2Ew+w²−(4/3)(Aw+bE+bw)−v N V]/[N(L+v)].       (3)

Thus neither quotient covariance nor simultaneous A/E motion is omitted.
Set

    r=R, u=E/N, t=1/L, a=A/L, z=Z/L, δ=(S−N)/N,
    D=(4−t²)(1−t²).

The exact all-channel sum takes the form

    G V/(EL/N) = c0+c1 a+c2 a²+c3 a³,                    (4)

where all coefficient formulas are saved in `normalized_cubic_coefficients.txt`.
The convenient sign form is

    c0=−r t²/[u(1+t)]−4t²/[3(1+t)]−(4−z²)tu/(6r),
    c1=n1/(3r u²D),        c2=n2/(3r uD),
    c3=4{r(t²+8t−12)+u(−2t³+3t²+8t−12)}
          /[3r(t−2)(t−1)(t+2)].                         (5)

The exact numerator n1 is

    4δr²D + r²(16−12r)
    −3r³t³+3r³t²+12r³t
    +4r²t⁴−4r²t³u+46r²t²u−20r²t²+34r²tu−76r²u
    +3rt⁵u²+17rt⁴u²+4rt³u²+20rt²u²−16rtu²−64ru²
    +11t⁵u³+2t⁴u³z²−t⁴u³−48t³u³−10t²u³z²
      +12t²u³+16tu³+8u³z²−32u³.

The exact numerator n2 is

    r²t³−31r²t²−4r²t+52r²
    −14rt³u−126rt²u+32rtu+168ru
    −2t⁵u²+5t⁴u²−t³u²−36t²u²+36tu²+64u².              (6)

## 2. Continuous-domain inward proof

Throughout the box

    r in [3/2,2], t,u in (0,1/100], |z|<=1/100,
    |δ|<=u/50,

one has `3<D<=4`. The coefficient of δ in n1 is exactly `4r²D>0`.
After retaining `r²(16−12r)<=−2r²`, the sum of the positive remaining
monomials divided by r², together with the maximum mass term, is strictly less
than 1/4. This is a continuous rational monomial bound, not a grid sign test:

    n1 <= −(7/4)r²,       c1 <= −7r/(48u²).             (7)

Likewise the sum of the positive monomials in n2/r² is less than 54. Hence

    c2 <= 6r/u.                                          (8)

The exact rational upper sums are in `practical_upper_certificate.json`.
For c3, its denominator is positive and both bracketed numerators in (5) are
negative for `0<t<=1/100`. Thus c3<0. Finally, for `0<=a<=1/5`,

    c1 a+c2 a²+c3 a³
      <= −(ar/u²)[7/48−6au]
      <= −ar/(8u²),                                      (9)

since `7/48−6/(500)>1/8`. Multiplying c0 and (9) by `EL/N=u/t`
gives exactly (2). No absolute bound on the large negative AE contribution was
paid; that sign is the reason the quotient is useful.

This also explains the proposed polynomial numerator

    F=L−3E²/(4N)+AE/N,     Q=F/L,     V=(4/3)(1−Q).

The proof is of the **full quotient generator**, not merely of GF or the small
size of `V−R`.

## 3. Original narrow mass event and the absent E^5 gate

From `r>=3/2`, `L>=100`, and `u<=1/100`,

    E=rL/u >=15000,          N=rL/u² >=1500000.

Moreover

    E^5/N=(rL)^4/u³ >=150^4*100³ >=600^5.

Taking fifth roots proves

    12N^(1/5) <= E/50.                                    (10)

Thus the charged original-ledger event `|S−N|<=12T` is enough for (1),
with no acquired mesoscopic inequality involving `E^5/N³`.

A concrete exact F1 counterexample is

    N=S=5,000,000,000;  L=100;  E=1,000,000;
    A=1; C=D=99; B=4,998,999,801; Z=0.

Here R=2, E/N=1/5000, A/L=1/100, and the mass discrepancy is zero.
The complete actual sums, recorded as exact fractions in the certificate, obey

    184 < G F1 <185,          −6482 < G V <−6481.          (11)

Here `E^5/N³=8`, so this witness directly addresses removing the inherited gate.
It refutes F1 as the requested pointwise upper barrier; it does not refute the
actual chain's capability. Every channel contribution is saved separately.

## 4. One-step endpoints, jumps, and full actual bracket

For this section use the sharper cap A/L<=1/100 in (1). A pre-stop physical
state has E>=15000, L>=100. Every active jump has `|ΔL|,|ΔE|,|ΔA|<=1` and
preserves nonnegative species. Along its complete straight segment,

    |V_L| <= (21/10)/L,
    |V_A| <= (7/5)u/L,
    |V_E| <= (21/10)u/L,                                  (12)

where L and u on the right are the **pre-jump** values. For example, the common
ratio bound is `(1+1/15000)/(1−1/100)`, and
`2[(1+1/15000)/(1−1/100)]²<21/10`. On these segments `0<V<=E²/(NL)` and
`2E−(4/3)A>0`, justifying the signed derivative simplifications. No S or Z
derivative exists for V.

At pre-stop states,

    0<=R−V<=1/7500.

At every one-jump exit endpoint,

    0<=R−V<3/10000.                                       (13)

Let `q_LL=sum λ(ΔL)²` and `q_A=sum λ(ΔA)²=sum λ`; every one of the twelve
channels changes A by ±1. Equation (12), including the AB/CD rows, gives

    Γ(V) <=9 q_LL/L² +25 (E/N)² q_A/L²,
    |ΔV| <=11/(5M)                                       (14)

when the pre-stop L is at least a received `M>=100`. Indeed the two grouped
jump terms have coefficients at most `21/10` and `7/2`; their squared
Cauchy bound is below 9 and 25. The huge AB rate is multiplied by its actual
small quotient jump, not by a unit-jump surrogate.

## 5. Reciprocal-L storage pays the dangerous L-motion bracket

The exact identities are

    G L=1+A+AL+AE−3A²,
    q_LL=1−A/2+A²+AL/2+AE,
    G L−q_LL=A(3/2+L/2−4A)>=0.                           (15)

The last inequality uses A/L<=1/100 and also holds for A/L<=1/8. The exact
finite-jump reciprocal identity is

    G(1/L)=−G L/L²+sum λ(ΔL)²/[L²(L+ΔL)].                (16)

For L>=M>=100, put `κ=(M−2)/(M−1)`. Then

    G(1/L) <=−κ q_LL/L².                                 (17)

Define the actual occupation `Q_L(t)=int_0^(t∧τ) q_LL/L² ds`, where τ is the
first exit from the local upper-band/gate domain. There need be no deterministic
time horizon. The positive terminal storage remains defined at the exit because
L_exit>=M−1. Its martingale satisfies

    |ΔM_L|<=j_L=1/[M(M−1)],
    <M_L> <=Q_L/(M−1)².

Condition on an admitted entrance state `(L_0,E_0,A_0,...)`, choose any
`Qbar_L>1/(κL_0)`, and put `x_L=κQbar_L−1/L_0`. A first clock hit forces the
martingale to exceed x_L. Thus

    P(Q_L reaches Qbar_L before τ)
      <= exp{−x_L²/[2(Qbar_L/(M−1)²+j_L x_L/3)]}.        (18)

This statement is conditional on that actual entrance, not a reset or a mean
initialization. A convenient choice is

    Qbar_L=2/(κL_0).

Its exponent is exactly

    3M(M−1)(M−2)/[2L_0(7M−2)].                           (19)

If the received entrance also satisfies `L_0<=2M`, this is at least M/10.
Thus the L-motion bracket is paid at scale `1/L_0`, including AE spikes,
without assuming their mean occupation and without a time cutoff.

## 6. A raw E-weighted source clock, with immigration paid by Q_L

Put

    W_E=A/E²+3/E,
    q_E=[AB/2+CD]/E²,        Q_E=int q_E ds.

The finite-jump source identity is the earlier weighted storage with its
literal raw-E units. To display every parameter-motion contribution, set
`φ=E^-2`, `d_±φ=(E±1)^-2−φ`, and `α_±=1/[E(E±1)]`. Then

    G W_E=φ G A +[A(A−1)²+2CD(A+1)]d_+φ+2A²E d_-φ
             −3[A(A−1)+2CD]α_+ +6AEα_-.                (20)

For E>=8 the exact one-step inequalities in the frozen weighted-source proof,
combined with the literal gate

    C+D+8A+12E <= B/2,

give

    G W_E <= E^-2−q_E.                                   (21)

That gate is automatic on (1). In fact

    B>=cN, c=2969/3000,
    C+D+8A+12E <=[(103/50)/15000+12/100]N <cN/2.

Hence the stopped occupation also pays

    int A/E² <=2Q_E/(cN),       int CD/E² <=Q_E.           (22)

The immigration remainder in (21) does not require a time horizon. On the
upper band,

    E^-2 <=L^-2/22500 <=q_LL/(22500 L²),                 (23)

because `L/E=u/r<=1/150` and `q_LL>=1` for actual integer states. Thus
`I_E=int E^-2<=Q_L/22500`.

Let m>=15000 be a received lower bound for E before τ; one may take
`m=sqrt(3NM/2)`. This choice is at least 15000 because the domain also
implies N>=15000M. For every actual row,

    |ΔW_E| <=[7+4(A+1)/E]E^-2 <=8E^-2,
    Γ(W_E)<=64 E^-4(1+3AB+3CD).                          (24)

In particular, with the process additionally stopped on Q_L<=Qbar_L and
Q_E<=Qbar_E,

    j_E=8/m²,
    v_E=64/m² [Qbar_L/22500+6Qbar_E].                    (25)

Set

    D_E=W_E(0)+Qbar_L/22500,
    Qbar_E>D_E,          x_E=Qbar_E−D_E.

Then the further clock-exit probability, before τ and the L-clock exit, is

    P(Q_E reaches Qbar_E first)
       <=exp{−x_E²/[2(v_E+j_E x_E/3)]}.                  (26)

The convenient choice `Qbar_E=2D_E` gives a bound no larger than
`exp(−D_E m²/1670)`. Keeping (26) is sharper and retains the actual entrance
charge. No assertion that `W_E(0)` is uniformly comparable to a chosen scale
is needed.

## 7. Paid quotient fluctuation and a single-excursion consumer

The full rate sum obeys `q_A<=1+3AB+3CD` under the source gate. Therefore

    int (E/N)² q_A/L²
      =int R² q_A/E²
      <=4 I_E+24Q_E.

Combining (14), (18), and (26), until both clocks and the physical gates stop,

    <M_V> <=v_V=(9+1/225)Qbar_L+600Qbar_E,
    |ΔM_V| <=j_V=11/(5M).                               (27)

For any x>0 the actual stopped upward martingale has the time-uniform bound

    P(sup M_V>=x) <=exp{−x²/[2(v_V+j_V x/3)]}.           (28)

Both clock-exit probabilities must be added if the auxiliary clock stops are
removed. For the convenient budgets above,

    v_V=(2038/225)Qbar_L+1200 A_0/E_0²+3600/E_0,

so no power of the maximum E range or deterministic time horizon occurs.
When `L_0` is comparable to the received floor M, this is O(1/M), with all
constants and entrance storage visible.

For example, an admitted excursion entering with `R_0<=9/5`, stopped on
leaving the lower side R>=3/2 or any other physical gate, can reach R>=2 only
if its V martingale rises by at least

    x=1/5−3/10000=1997/10000.

This follows from the exact negative drift (2) and endpoint bound (13). Its
single-excursion upper-hit probability is bounded by (18)+(26)+(28) with this
x. It is not a global claim: the existence of the entrance, persistence of
A/Z/count/other gates, localization of earlier time below the upper band, and
any joining/counting of repeated excursions remain receiving obligations.

All no-horizon statements follow first at a finite localized time and then by
monotone convergence/Fatou. The chain is nonexplosive on finite intervals because
its total count is bounded above by the initial total plus rate-one immigration.

## 8. Exact evidence and scope

`derive_practical.py` constructs both quotient generators from the twelve rows.
`check_practical_upper.py` checks the finite-jump identities, exact polynomial
sign numerators, rational continuous-domain majorants, one-step derivative and
endpoint constants, source-storage identity, and the exact F1 outward witness.
Its certificate and the explicit coefficient file are ordinary local artifacts.
`check_stopped_clocks.py` independently replays the actual Fraction-valued rows
and checks the exact stopped-cost simplifications; these regressions are checks,
not the continuous sign proof.
There is no sampled-positivity acceptance and no imported stationary reference.

This component supplies a simpler one-sided observable and literal paid local
costs. It does not claim that the practical gates are acquired, that all upper
excursions have been joined, or that the macro-time/clearance consumer has been
proved. The parent owns those operations.
