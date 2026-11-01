# Buffered actual progress removes the unnecessary lower-ratio gate

Status: root construction awaiting independent review. This is a conditional actual macro-exit clock, not a proof of its A/imbalance/upper-ratio admission or a practical clearance algorithm.

Use the exact rate2 count process and fixed reference N. Let L=A+(C+D)/2, Z=C-D, R=E²/(NL), and

 U0=E-A/2, V=U0+L/100.

Assume the actual pre-stop gates

 B>=100, E/B<=1/5, L/B<=1/10,
 A<=L/100, |Z|<=L/100, CD>=4,
 L<=N/5000, R<=2, V>=100.

There is NO lower bound on R. Every actual outgoing jump is retained.

## Same-source progress and variance

The earlier exact U0 identities and looser A/Z gates give

 G U0>=AB/10+CD/4, q_U0<=9 G U0, |Delta U0|<=3/2.

The actual L identities are

 G L=1+A+AL-3A²+AE,
 q_LL=1-A/2+A²+AL/2+AE.

On A<=L/100, G L>=0 and q_LL<=G L, since their difference is
A(4A-L/2-3/2)<=0. Thus

 G V>=CD/4>=L²/5.

The markwise inequality (u+beta l)^2<=(1+beta)u²+(beta+beta²)l²,
with beta=1/100, implies

 q_V<=(101/100)q_U0+(101/10000)q_LL<=10 G V.

All V jumps have magnitude<=151/100. Also A<=L/100 gives

 E+L/200<=V<=E+L/100.

This is why a lower R gate is no longer needed to keep the progress coordinate positive.

## Explicit physical-time potential

For V>=100, finite-jump Taylor and the bracket comparison give

 G(V^-3)<=G V/V^4[-3+60 V^4/(V-151/100)^5]<=-2 G V/V^4.

The final scalar inequality follows from3*10000^5<5*9849^5. Because
E²<=2NL and L<=N/5000,

 V<=sqrt(2NL)+L/100<(3/2)sqrt(NL).

Consequently

 G(V^-3)<=-32/(405N²).

The globally positive bounded extension

 Psi=16N²/[max(V,50)]³

has G Psi<=-1 on every admitted pre-stop state; all actual successor V values exceed98.49, so the extension changes no relevant jump. Actual stopped Dynkin yields E sigma<=Psi(initial), where sigma is the first declared macro cap OR another admitted-domain failure. If the true entrance has E>=e0 T³, T=N^(1/5), then V>=E and

 E sigma<=16T/e0³,
 P(sigma>d)<=16T/(e0³d).

The other-domain exit probability must still be charged before replacing sigma by a macro-target time. No state reset or assumption that E is monotone is used.

## The E floor is also an actual source barrier

Under the same source/A/imbalance gates (without needing V>=100),
exp(-U0/20) is a nonnegative supermartingale: finite-jump Taylor, q_U0<=9G U0 and |Delta U0|<=3/2 give its generator<=0. In particular, before other failures and a declared horizon,

 P(E hits a lower E_floor)<=exp[-(U0(initial)-E_floor)/20].

At such a hit U0<=E_floor, so this statement follows without pretending U0 or E is globally nonnegative/monotone. If E_floor>=100, V>=E then prevents V=100 from being an uncharged earlier exit. Finite-horizon integrability follows from the original population/Poisson bound.

## Actual macro handoff, when all gates are supplied

Take cap tau_cap=first{E>=ceil(N/100) OR L>=N/5000}. Under R<=2 and |Z|<=L/100 at its actual target, M=A+min(C,D)=L-|Z|/2>=199L/200. An L cap gives M>=199N/10^6; an E cap gives M>=199N/(4*10^6). Thus either target supplies far more than the accepted harmonic receiver's m0=10^-6 seed, provided the required one-jump target gates are received. The original narrow count event supplies its mass entrance and cost only when the actual macro cap occurs by ORIGINAL time4T. A later entrance/progress clock must fit within that same remaining horizon, or a separate horizon extension must be proved and paid. Large N alone does not extend the event. If the subsequent harmonic service is invoked at the actual cap, its own future immigration/death estimates must be received conditionally from that past-measurable state; the pre-cap narrow band is not asserted through physical removal.

This handoff would still pay the harmonic receiver's current fixed h=4*10^14 and its explicit errors. It is not a practical short-clearance claim. Improving that actual continuation cost remains a separate capability question. The new point is narrower: upper-ratio protection plus positive buffered progress can suffice; proving an unnecessary lower-ratio barrier should not choose the scientific destination.
