# Spectral-floor reduction of a negative unfiltered reference score

Status: independently PASS as a dependency in `qutrit_reset_unfiltered_score_independent_audit.md`. This reduction alone is not whole score positivity.

Let A0=diag(a1,a2,a3)>=0, d>0, and Qi(b) be coordinate i of the reference-filter derivative at the unfiltered actual qutrit-reset seed with reset A0+bI. The exact acquired source formula, followed by t=s+b, gives

Qi(b)=d integral_b^infinity (t-b)/(ai+t)^2 g1(d/(a1+t),d/(a2+t),d/(a3+t)) dt.

Here i is the distinguished argument of g1. For b>0 differentiation is legitimate and

Qi'(b)=-d integral_b^infinity g1/(ai+t)^2 dt,
Qi''(b)=d g1(d/(a1+b),d/(a2+b),d/(a3+b))/(ai+b)^2.

The received zero-geometry theorem says the kernel along this path is either everywhere positive or has one strict negative-to-positive crossing theta. The kernel is positive eventually. Thus for b>=theta, Qi(b)>0 directly. On 0<b<theta, Qi is concave. Its continuous endpoint Qi(0) is finite: alternatively obtain this from the finite-dimensional derivative Tr_reference[(XlogX)-2(NX logNX)]+RlogR-log3 R; xlogx is continuous on positive semidefinite matrices. Continuity also follows from the source integral's endpoint bounds.

For 0<b<theta, concavity gives

Qi(b)>=(1-b/theta)Qi(0)+(b/theta)Qi(theta).

Therefore a negative Qi(b) forces Qi(0)<0. In fact Qi(0)<Qi(b) because Qi(theta)>0. Applied with b=lambda_min(A)>0 and A0=A-bI, every negative faithful-reset anchored coordinate score produces a strictly more negative score at a singular diagonal reset.

Equivalently, proving all infinitesimal anchored reference-score directions requires only the singular diagonal reset faces. Up to permutation the remaining faces have either distinguished noise ai=0 or one companion noise zero. There are two nonnegative bath parameters after scaling d=1. This does not prove finite anchored filter order, nor does it use or assert monotonicity under general reset processing.

The reduction is distinct from the whole-deficit spectral-floor theorem: the extra factor(t-b) yields a SECOND-derivative crossing and concavity, rather than direct tail-integral monotonicity. It is also distinct from the axisymmetric score receiving, which already pays the exceptional axis for A=diag(a,b,b).
