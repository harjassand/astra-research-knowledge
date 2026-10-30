# Exact failure certificate at the non-A-birth boundary

30 October 2026. Mathematical stress test of the acquired local interface, not a new recurrence theorem or counterexample to weakly reversible recurrence.

The reviewed graph compiler restricts linear D-consuming births to a+D->2a. The following exact calculation shows that this restriction cannot simply be removed while keeping its scalar small-return and uniform reset outputs.

Take an irreducible conversion cycle C->E->a->C in the common D-clock, with C->E rate lambda>0 and E->a rate mu>0. Add a non-a birth C+D->2C of rate beta>0. Keep any of the previous seed/clear/2D channels; they are disabled before the first a at initial state

    a=E=0, C=n, D=1.

The optional 2D channel is disabled at D=1. The a-born linear birth is also disabled until a appears. Let tau_a be the first a arrival and tau_0 the non-a birth that exhausts D. First ignore connector stopping.

## Exact killed-particle representation

Until tau_a or tau_0, no new particle has been born. The n initial C particles are independent chains with transitions C->E at lambda, E->a at mu (absorbing success), and killing from C at beta (the first such kill anywhere is the actual D-consuming birth). This is an exact pre-stop representation, not an independence assertion after conditioning on survival.

Put d=lambda+beta-mu. For d!=0, single-particle transient probabilities are

    p_C(t)=exp(-(lambda+beta)t),
    p_E(t)=lambda [exp(-mu t)-exp(-(lambda+beta)t)]/d,
    g(t)=p_C(t)+p_E(t).

When d=0, p_E(t)=lambda t exp(-mu t). Thus

    P(tau_a<tau_0)=n integral_0^infinity mu p_E(t) g(t)^(n-1) dt.

Since p_E(t)=lambda t+O(t^2) and g(t)=1-beta t+O(t^2), rescale t=u/n to obtain

    n P(tau_a<tau_0) -> lambda mu integral_0^infinity u exp(-beta u)du
                       = lambda mu / beta^2.

The limit is justified directly: for t<=epsilon, g(t)<=exp(-beta t/2), p_E(t)<=Ct, giving an integrable C u exp(-beta u/4) bound after rescaling; for t>=epsilon, g(t)<=rho<1 and integral p_E(t)dt<infinity, so the remaining n^2 rho^(n-1) contribution vanishes. Likewise

    E min(tau_a,tau_0)=integral_0^infinity g(t)^n dt ~ 1/(beta n).

## Actual physical first-stage consequence

Physical A=a+a0 equals a0 until the first a. Its fast multiplier is the fixed positive constant F0=(a0)_a0(B)_q. The two connector birth intensities before that first a are also fixed, i+t a0 B. Adding that actual connector stop changes the probability of reaching tau_0 first by at most O(1/n), using the preceding mean and its competing-hazard compensator. Therefore

    P(actual D=0 stop before first a or connector)=1-O(1/n).

On that event A_out=A_in=a0. For every fixed s>0,

    E[f_s(A_out); actual dormant stop]/f_s(A_in) -> 1.

In particular the scalar positive-D-to-dormant profile operator is NOT small, and no uniform terminal f_s reset to zero is possible on this sequence. The earlier acquired local certificate therefore genuinely fails outside its birth restriction.

## What must change, and what does not follow

The calculation does not show transience or null recurrence of the full connector process. It only rejects a proposed extension of the local compiler. A broader construction would have to retain this order-one dormant return inside a coupled face Green, with its actual A loss and hidden-type composition, instead of treating it as an error kernel. Conventional finite-chain killing already exposes the obstruction; another added-species recurrence example would not address it.
