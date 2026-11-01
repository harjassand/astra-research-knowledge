# Full corrected-clock jumps and bracket, including fast marks and startup

**Separate author component, pending independent receipt.** The main primitive
lemma is frozen independently in `MAIN_FREEZE.json`. This note receives the
remaining-clock derivative bounds, their startup extension, and the actual
regularized source budget. It does not supply the clock drift residual or acquire
any physical gate. Every enabled actual channel and complete exit jump is kept.

## Practical output for the actual endpoint receiver

Let N=T^5, T>=10000, and

    q(A,L,E)=b(L/T,E/T³)+AE b_l(L/T,E/T³)/(NT).

Receive the declared source/domain/segment conditions below. On the same actual
stop, including rawtime startup and the original horizon 4T, the two budget events

    Qψ=int ψ(L/T)q_LL/T² dt <=3/(2T),
    Qsrc=int[(19/20)AB+(17/101)CD](1+e)^−2 dt <=4T³

give the **full actual corrected-q martingale** the explicit costs

    <M_q> <=v=1449/(800T)+1285200/T³,
    |ΔM_q| <=j=27/(25T).                                (1)

The regularized source clock's received failure is `exp(−T³/2500)`; the
source-paid main primitive clock has additional failure at most `exp(−T/80)`.
Their sum removes the two auxiliary budget stops, but not physical/domain
failures. The source-paid primitive does not require A/L<=1/100, so it can cover
rawtime startup without that gate. It receives the same Qsrc event, not an
independent fresh source experiment.

At every admitted endpoint, including the complete failing jump,

    −2/T² < q−b <=0.                                     (2)

For T=10000 (N=10^20), (1) is `v=0.0001824102`, `j=0.000108`.
For T=100000 (N=10^25), it is `v=0.0000181137852`, `j=0.0000108`.
These are exact terminating decimals, not asymptotic estimates. No compact
cutoff K occurs. The root endpoint receiver may substitute (1) directly for
its v,j, once all dependencies and admission costs have been received.

## 1. Explicit received inputs and all-jump padding

The source component is the root's `REGULARIZED_WEIGHTED_SOURCE_BUDGET.md`.
It runs on the original horizon 4T with actual pre-stop gates

    B>=9N/10, L<=N/5000, E<=N/100, A/(E+T³)<=2,

and initial W0=(8/5)T³ at the actual raw corner. It gives the Qsrc ceiling above,

    int A/(1+e)² dt <=800/(171T²),
    q_A<=1+(21/20)AB+3CD,                                (3)

where q_A is the complete actual rate sum. An arbitrary later entrance cannot
inherit this initial charge; it must receive the actual remaining original
source budget, or a separately proved entrance charge.

The geometric input is that **every whole enabled jump segment**, including
the mark causing a physical/startup failure, lies in

    D={l>=0,e>=0,e²<=3l}
      union {0<=l<=1,0<=e<=1/1000}.                       (4)

It is enough to receive the explicit padding verified with the residual author:

* During startup, L'<=401 and E'<=8*400³+1 for every enabled endpoint. Thus
  l'<=.0401 and e'<.001 for T>=10000, including any endpoint L'=0.
* Post-startup, pre-stop L>=200, R<=2, E<=N/100. Every enabled endpoint has
  L'>=199 and

      e'^2<=2l+1/(50T)+T^-6<=3(l−1/T)<=3l'.

  Convexity of `e²/l` for l>0 covers the complete segment. The displayed scalar
  inequality follows from l>=200/T; no future successful exit is assumed.

The full note can also be used with any independently received equivalent
segment declaration. No enabled generator row may be deleted merely because
its endpoint fails a gate.

Actual nonnegative species imply A<=L on every segment, including startup.
The source cap L<=N/5000 and |ΔL|<=1 imply on every segment

    L'/N<=1/5000+1/N<=1/4000.                            (5)

No A/L cap is used in (5) or in the full-gradient estimates below.

The deterministic input is `GLOBAL_L_WEIGHTED_CLOCK_DERIVATIVES.md`, with the
same-ceiling startup extension written in Section 2 of
`actual_clock_residual_receiver_20261101/ACTUAL_CLOCK_RESIDUAL_BUDGET.md`
under the root boundary directory (SHA256
`2ceb7e685692bfa2ae26e42b4080c074d009dad5320132c4a127b677898e8d07`).
That shared extension and the source budget remain explicit received inputs,
not independent acceptances conferred by this note. On D, write
ψ_p(l)=min(1,l^-p), ψ_p(0)=1. Receive

    |b_l|<=sqrt(ψ_5),      |b_e|<=6sqrt(ψ_4),
    |b_ll|<=9             for l<=1,
    |b_ll|<=(5/2)l^-7/2   for l>=1,
    |b_le|<=13            for l<=1,
    |b_le|<=l^-3          for l>=1.                      (6)

The smooth l=0 extension is a received deterministic fact, not division by a
zero inverse-flow coordinate. On the startup rectangle the proof of the small-l
bounds uses only e<=5/4, so the same ceilings apply. In particular
`J_inf<12l²` gives `|b_e|<=J_inf/(2l²)<6` before passing to the smooth boundary.
No b_ee bound is needed by this bracket component.

## 2. Exact full gradient, with no product/parameter motion missing

Set l=L/T,e=E/T³. Differentiate the literal corrected function, holding N fixed:

    q_Apartial = e b_l/T³,
    q_Lpartial = b_l/T +(A e/T⁴)b_ll,
    q_Epartial = b_e/T³ +(A/T⁶)(b_l+e b_le).              (7)

Here `q_Apartial` is a derivative, not the rate sum q_A in (3). For every actual
row `(ΔA,ΔL,ΔE)=(d,v,w)`, its exact finite jump is the integral of (7) along
the whole actual straight segment. Equivalently, if h=AE and g=b_l,

    Δq=Δb +(Δh)g/T⁶+h' Δg/T⁶,
    Δh=Ed+Aw+dw.                                        (8)

The h' term and the simultaneous product dw are retained. Equation (8) makes
explicit why the AB/CD fast marks, though having ΔL=0, do not disappear from
this corrected observable's bracket.

## 3. Continuous derivative envelopes, with fixed constants

The cone part of D has e<=sqrt(3l)<2sqrt(l). On the rectangle e<=1/1000.
Together with A<=Tl and (5), these give, for T>=10,

    |(A e/T⁴)b_ll| <=(1/5T)sqrt(ψ_5),
    |(A/T⁶)(b_l+e b_le)| <=(3/10T³)sqrt(ψ_4).           (9)

For the first inequality at l<=1, the squared ratio to ψ_5/T² is at most
`243/T⁴<1/25`; at l>=1 it is at most
`(75/4)l/T⁴<=75/16000<1/25`. For the second inequality at l<=1 the ratio to
sqrt(ψ_4)/T³ is at most `27/T²<3/10`; at l>=1 it is at most
`3sqrt(l)/T²<=3/sqrt(4000)<3/10`. The rectangle obeys the same small-l ceilings.
Thus

    |q_Lpartial| <=(6/5T)sqrt(ψ_5),
    |q_Epartial| <=(7/T³)sqrt(ψ_4),
    |q_Apartial| <=e sqrt(ψ_5)/T³.                       (10)

For the practical range T>=10000 the first correction in (9) instead obeys

    |(A e/T⁴)b_ll| <=(7/100T)sqrt(ψ_5),
    |q_Lpartial| <=(107/100T)sqrt(ψ_5),                  (11)

because `243/10000⁴<(7/100)²` and `75/16000<(7/100)²`.

Put φ=(1+e)^−2. On both pieces of D,

    e²ψ_5(l)<=24φ,          ψ_4(l)<=8φ.                  (12)

On the cone, use `(1+e)²<=2+6l`; the small and large l cases are elementary
monomial bounds. The rectangle's constants are much smaller. Across any
actual segment,

    ψ_5(l')<=R_T ψ_5(l),    R_T=(1−1/T)^−5,
    φ(e')<=(1000/999)² φ(e)<(101/100)φ(e).               (13)

The weight on the right is always at the **actual pre-jump state**. The first
comparison remains valid across l=0 and l=1. The second uses T³>=1000 and
E'>=0, not a positive-E entrance assumption.

Combining (10)-(13), the squared derivatives everywhere on an enabled segment
are bounded in terms of its pre-state by

    |q_Lpartial|² <=(5/2)ψ_5(l)/T²,
    |q_Apartial|² <=25φ(e)/T⁶,
    |q_Epartial|² <=400φ(e)/T⁶.                         (14)

For T>=10000 the sharper first coefficient is `23/20`, since
`(107/100)²(10000/9999)^5<23/20`.

## 4. Full actual bracket, all twelve rows

Every enabled channel has |ΔA|=1, |ΔL|<=1, and |ΔE|<=1; therefore q_EE<=q_A.
The exact finite-segment integral and three-term Cauchy give from (14)

    Γ(q) <=(15/2) ψ_5 q_LL/T² +1275 φ q_A/T⁶.           (15)

This already yields the simple T>=10 bound

    <M_q> <=(15/2)Qψ+91800/T³,    |ΔM_q|<=13/(10T),      (16)

on the received source clock. With the source-paid Qψ<=8/T its leading cost
is 60/T. This is the conservative rawtime-0 variant originally requested.

For the practical constants, group the L-motion as x and the remaining two
motions as y. Apply

    (x+y)²<=(21/20)x²+21y²,
    y²<=2[(q_Apartial ΔA)²+(q_Epartial ΔE)²].

Using the sharper 23/20 L coefficient gives

    Γ(q) <=(483/400) ψ_5 q_LL/T² +17850 φ q_A/T⁶.        (17)

Every rate, including AB, CD→AB, and the E-changing CD/AE marks, is present.
In particular the fast rates are multiplied by their actual small corrected
jump weight φ/T⁶, not a unit-jump surrogate.

The complete source-rate integral follows from (3):

    int φ q_A <=4T+(303/17)Qsrc
               <=4T+(1212/17)T³ <72T³.                 (18)

The coefficient 303/17 is the maximum of 21/19 and 303/17. This uses the actual
source clock over the same original horizon; no independent-fast-law premise
or deterministic time change occurs. Combining (17), (18), and Qψ<=3/(2T)
gives exactly v in (1).

For jumps, the global supremum estimates in (10)-(11) give

    |Δq| <=107/(100T)+9/T³ <=27/(25T),                  (19)

because e²ψ_5<=3 on the cone and is smaller on the startup rectangle. Equation
(19) includes the enabled mark causing a startup/domain failure. Its martingale
compensator is continuous, so the same cap applies to ΔM_q.

Finally, the actual correction obeys

    |AE b_l/(NT)| <=l e sqrt(ψ_5(l))/T² <2/T²            (20)

on both pieces of D. Its sign is nonpositive by b_l<=0. This proves (2), with
no A/L cap and no lower-ratio gate.

## 5. How to receive the result honestly

Use the actual stopped chain, common source and primitive clocks, common
physical gate stop, and original horizon. Charge at least

    exp(−T³/2500)+exp(−T/80)

for the two auxiliary budget exits, plus all separately proved physical/startup
failures. If those source hypotheses have not been independently accepted,
(1) remains conditional on them. The derivative extension and all-segment
padding likewise must be received, not inferred from a successful future path.
The root residual author separately owns `D_t` in the Dynkin identity.

`check_full_corrected_bracket.py` checks the exact gradients and all twelve
product rows, rational continuous-envelope/padding constants, and the exact v,j
examples. It does not substitute numerical derivative samples for the received
analytic derivative bounds. No variance/UI claim, finite-N Gaussian error, or
clearance result follows from this bracket alone.
