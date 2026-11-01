# Independent receipt: bounded-primitive actual weighted bracket

Status: **PASS, no repair**, for the frozen conditional component
`MAIN_WEIGHTED_CLOCK.md`, SHA256
`7f1d8341f515a29e4b55880ac327949599238e39ec1bb2c5f3e8ef030538ef61`.
The reviewer did not author this component. The original files are preserved;
read-only copies and their author manifest are retained in `source_snapshot/main`.
This receipt does not by itself acquire the source/state gates or clearance.

## Continuous finite-jump proof, not sampled positivity

For psi(x)=min(1,x^-5), H(x)=integral_x^infinity psi, H is C1 and its
derivative is locally absolutely continuous on [0,infinity). Its weak second
derivative is nonnegative, zero below 1 and 5x^-6 above 1. There is no atom
at 1 because H' is continuous. Thus the integral Taylor formula remains exact
for every segment crossing 1.

For T>=10, h=1/T and R=(1-h)^-5, whenever x,y>=0 and |y-x|<=h,
psi(y)<=R psi(x). If x<=1 this is immediate. For x>1,y>=1 use
x/y<=x/(x-h)<=1/(1-h). For x>1,y<1, use
x<=1+h<=1/(1-h). Consequently H''(z)<=5R psi(x) almost everywhere on the
segment, since H''(z)<=5psi(z). This proves both signs and the precise factor
5R/2 in the Taylor remainder. Also |Delta H|<=|Delta L|/T and
(Delta H)^2<=R^2 psi(x)^2(Delta L)^2/T^2<=R^2 psi(x)(Delta L)^2/T^2.
These facts hold on the complete enabled jump, including terminal L=0. No
inverse L division or missing endpoint extension occurs.

Reconstructing the literal twelve reactions gives GL, q_LL and
GL-q_LL=A(3/2+L/2-4A) exactly as frozen. Hence the generator inequality is
GH<=-[T-(5/2)R]q_psi on q_LL<=GL. With no cap,
q_LL-GL<=4A^2 and A<=L imply the exact additional bound 4Al psi(l).
On e^2<=3l, (1+e)^2<=2+6l, and l psi(l)(2+6l)<=8 on BOTH l<=1 and l>=1.
On the startup rectangle, l psi(l)(1+e)^2<2. Therefore the source-paid defect
is indeed 32 A/(1+e)^2, whose received occupation budget gives
25600/(171T^2). This source input is separately charged; it is not silently
claimed from a future admitted trajectory.

## Source dependency and same-stop optional stopping

The received dependency is `REGULARIZED_WEIGHTED_SOURCE_BUDGET.md`, hash
`38973f8baacbadb5c8fdf63cac93e2aed49b7831883cd4c3943aff3e3ac10b2b`, under
root receipt `e1c1eb76b8592a098bdad9f6188b7f7f08e7d0e75ce153bc9a06aa53950dcae8`.
Its H_A<=800/(171T^2) applies only through its actual source clock and physical
admission stops over the original horizon 4T. The author's main lemma retains
those stops and separately requires their exit cost if removed, as necessary.

The weighted clock is a continuous compensator, so no budget overshoot is
lost. At its first hit, terminal H>=0 and H0<=5/4 imply the stated martingale
threshold x. All enabled exit jumps satisfy j_H<=1/T and bracket<=R^2 Qbar.
Freedman may be applied with a smaller certified positive threshold; it is not
necessary to substitute the larger actual x in its denominator. This validates
the constant simplifications below. A physical exit at the same time is never
silently accepted as successful service.

## Exact constants

The rational endpoint checks establish:

* T>=10: R<2, R^2<3, a_T=T-(5/2)R>=T/2.
* Qbar=5/T, no defect: x>=5/4, v<=15/T; the Freedman exponent is >=T/20.
* Qbar=8/T, source defect: x>=4-5/4-25600/17100>=5/4,
  v<=24/T; exponent >=T/32.
* T>=10000: R<1001/1000, R^2<1003/1000 and a_T>=9997T/10000.
  At Qbar=3/(2T), even the source-paid x exceeds 1/5,
  v<=3009/(2000T); exponent >=T/80.

Each endpoint inequality is exact rational arithmetic; monotonicity extends
it to all real T in the specified interval, not only integer test values.
The raw fixed corner has L0=1, so H0=5/4-1/T; using H0<=5/4 is conservative.
The author's additional statement about H0=5/4 at L0=0 is a valid general
boundary statement, not a premise that the specified corner has L0=0.

## Acceptance limits

Accepted: the conditional actual weighted clock, all finite-jump Taylor and
bracket coefficients, cap-only/source-paid alternatives, and all constants.
Not accepted by this receipt alone: source/state gate acquisition, full corrected
clock bracket, residual, raw-clock window, or clearance. These require their
own frozen sources and receive separate sections in this audit.
