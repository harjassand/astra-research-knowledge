# A bounded-primitive budget for the global L-weighted actual bracket

**Author freeze, pending independent receipt.** This lemma is independent of any
remaining-clock derivative claim. It uses the literal twelve-channel chain. The
optional source-paid version explicitly receives the separately charged source
budget; it does not assert that budget's gates are acquired. No prior file or
practical/tilted-carrier construction is modified.

## Result

Let N=T^5, T>=10, l=L/T, e=E/T³, and

    ψ(l)=min(1,l^-5),     ψ(0)=1,
    Qψ(t)=int_0^(t∧τ) ψ(L/T) q_LL/T² ds.

The original physical horizon is 4T. Any other declared gate/first-failure stop
may be included in τ. All endpoint statements include the complete enabled
exit jump. If actual pre-stop states satisfy `q_LL<=G L`, then

    P(Qψ reaches 5/T before τ) <= exp(−T/20).              (1)

The actual gate `A<=L/100` suffices; writing it this way avoids division at L=0.

There is also a source-paid version **without any A/L gate**. Suppose pre-stop
states lie in the union

    e²<=3l,   or   [0<=l<=1 and 0<=e<=1/1000],             (2)

and receive the actual regularized source occupation

    H_A=int A/(1+e)² ds <=800/(171T²).                    (3)

Then, before the source-clock/gate stops,

    P(Qψ reaches 8/T) <=exp(−T/32).                       (4)

The source-clock exit probability must be added separately if that stop is
removed. For the practical range T>=10000, both versions admit the sharper
budget

    Qψ<=3/(2T),       failure <=exp(−T/80),               (5)

again adding the received source-clock failure in the source-paid version.
These bounds use the actual initial bounded storage, not a fresh equilibrium
or a future successful trajectory. No constant grows with a compact cutoff.

## 1. Explicit primitive and finite steps

Take the bounded nonnegative decreasing primitive

    H(l)=int_l^infinity ψ(y)dy
        =5/4−l           for 0<=l<=1,
         1/(4l^4)        for l>=1.                       (6)

It is C¹, its derivative is absolutely continuous locally, and its a.e. second
derivative is `−ψ'(l)>=0`. Thus its kink in the second derivative at 1 causes
no remainder omission. Its initial value is always at most 5/4, even at L=0.

Write `R_T=(1−1/T)^−5`. For nonnegative x,y with |y−x|<=1/T,

    ψ(y)<=R_T ψ(x),
    0<=H(y)−H(x)+ψ(x)(y−x)
       <=(5/2)R_T ψ(x)(y−x)².                            (7)

For the first inequality: if x<=1 it is immediate; if x>1, use y>=x−1/T
when y>=1, or x<=1+1/T when y<1. For the second, integrate the exact a.e.
second derivative and use `|ψ'(y)|<=5ψ(y)`. This is an exact finite-jump bound,
not a diffusion approximation. Every enabled actual segment has L>=0 because
both endpoints are nonnegative count states.

Also

    |ΔH|<=|ΔL|/T<=1/T,
    (ΔH)²<=R_T² ψ(l)(ΔL)²/T².                            (8)

The first bound uses ψ<=1 directly, rather than a large ratio near the origin.
For T>=10, exact rational endpoint comparisons give `R_T<2`, `R_T²<3`.

## 2. Full actual generator and the optional source defect

The twelve-channel identities are

    G L=1+A+AL+AE−3A²,
    q_LL=1−A/2+A²+AL/2+AE,
    G L−q_LL=A(3/2+L/2−4A).                             (9)

All channels remain present; the AB/CD rows simply have ΔL=0 for this test
function. By (7), with `qψ=ψ(l)q_LL/T²`,

    G H <=−ψ(l)G L/T +(5/2)R_T qψ.                      (10)

If q_LL<=GL, this gives

    G H <=−a_T qψ,      a_T=T−(5/2)R_T >=T/2.            (11)

No expectation of A is used. On A<=L/100 the final expression in (9) is
nonnegative.

Without this cap, the exact defect is controlled by

    q_LL−G L <=4A²,       A<=L,

so

    G H <=−a_T qψ+4A lψ(l).                              (12)

On the cone in (2), `(1+e)²<=2+6l` implies

    lψ(l)(1+e)²<=8.

On the startup rectangle in (2), the same expression is below 2. Thus

    G H <=−a_T qψ+32 A/(1+e)².                           (13)

The received source budget (3) bounds its total positive drift by

    d_T=25600/(171T²).                                   (14)

This optional variant allows startup A spikes in this bracket calculation.
It does not remove any A gate needed elsewhere, and it does not establish the
cone/startup rectangle or source admission.

## 3. Actual martingale and exact budget formula

Let M_H be the actual stopped Dynkin martingale. Equations (8) and the complete
rate sum give

    |ΔM_H|<=j_H=1/T,
    <M_H> <=R_T² Qψ.                                    (15)

Stop additionally when Qψ reaches Qbar. The compensator clock is continuous,
so it has no overshoot. Terminal H is nonnegative at the actual exit endpoint.
If the initial value is H0 and an admitted positive-drift ceiling is d (zero
for (11), d_T for (13)), a clock hit forces

    M_H >=x=a_T Qbar−H0−d.

Whenever x>0, bounded-jump Freedman gives the literal conditional cost

    P(clock hit before the other stops)
      <= exp{−x²/[2(R_T² Qbar+x/(3T))]}.                 (16)

One may replace x by any certified smaller positive threshold. Equation (16)
retains actual entrance storage and any charged drift defect. The universal
ceilings below use only H0<=5/4; they do not reset the chain at an entrance.

For Qbar=5/T and d=0, use x>=5/4 and bracket<=15/T. The exponent is at least
T/20. For Qbar=8/T and d=d_T, use

    4−5/4−25600/(171*100)>=5/4,

and bracket<=24/T; the exponent is at least T/32. These prove (1) and (4).

For T>=10000, exact rational comparisons yield

    R_T<1001/1000, R_T²<1003/1000,
    a_T >=(9997/10000)T.

With Qbar=3/(2T), even the source-paid threshold obeys

    x >=(9997/10000)(3/2)−5/4−25600/(171*10000²)>1/5.

The bracket is at most `3009/(2000T)`. Using x=1/5 in (16) gives exponent
at least T/80, proving (5). The rawtime-0 case has exactly H0=5/4 when L0=0.

## 4. Scope and exact checks

The source-paid result is stopped at the original horizon 4T because its
received source budget has that horizon. The cap-only result itself needs no
time bound, but does not enlarge the original declared experiment. If a source
clock, physical gate, or startup failure occurs on an enabled mark, that mark
is included in the bracket/jump bounds and the failure is charged separately.
The weight and primitive stay well-defined at L_exit=0.

`check_main_weighted_clock.py` verifies (9), the rational constants in all three
budgets, and exact finite-jump regressions on both sides of the kink, at L=0,
and across very large l. The uniform proof is (7)-(16), not positivity inferred
from the regressions. `MAIN_FREEZE.json` freezes this component independently of
the subsequent corrected-clock bracket.
