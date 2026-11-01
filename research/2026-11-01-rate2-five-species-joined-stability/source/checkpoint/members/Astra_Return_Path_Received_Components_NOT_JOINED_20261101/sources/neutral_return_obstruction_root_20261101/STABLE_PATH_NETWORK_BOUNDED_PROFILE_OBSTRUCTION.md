# Root countermodel: connected return paths do not inherit the bounded-profile Foster representation

Status: NEW independent construction, not yet reviewed. This is a representation/service obstruction in an already stable ordinary model, NOT a counterexample to recurrence or exponential stationary moments.

## Actual five-species model

Species A,B,C,D,E. All rate constants are1, using falling-factorial mass-action conventions. The port is0<->A. The reversible internal pairs are

 2A <-> A+C,
 2A <-> A+D,
 2A <-> A+E,
 A+E <-> C+D,
 C+D <-> A+B.

The binary complex graph is a connected tree containing2A and EVERY A+satellite complex. Its sole square-free satellite hub C+D has NO direct2A connection. All internal transitions conserve total count Ntot. Start at

 x_N=(A=0,B=N,C=1,D=1,E=0).

Nonexplosion follows from Ntot(s)<=N+2+I(s), where I is the unit-rate immigration count. This model has the ordinary product of five Poisson(1) laws: every reversible pair individually satisfies detailed balance, including the port. Irreducibility follows by the two-particle complex paths and the port. It is positive recurrent and has E_pi r^Ntot=exp[5(r-1)] for EVERY finite r>1. None of those ordinary facts is claimed as an invention.

## A rigorous finite-horizon lack of A-service

Call every A-dependent reaction except A+B->C+D a BAD reaction. This includes every A death, all2A reactions, and all A+C,A+D,A+E reactions. The dominant chain suppresses bad channels and keeps immigration, A+B->C+D, and the two C+D exits to A+B and A+E. Couple actual and dominant chains until the first bad event.

For the dominant chain, pathwise

 C(s)+A(s)=D(s)+A(s)=1+I(s),
 E(s) counts C+D->A+E,
 B(s)=N-I(s)+A(s)-E(s).

Thus C,D<=1+I(T) throughout[0,T]. On the event I(T)<=m, E is bounded by a counting process of intensity(1+m)^2; stopping at the(m+1)st immigration justifies the usual conditional Poisson-tail domination without conditioning future intensities incorrectly. Hence, for integers m,ell,

 P(dominant I(T)>m or E(T)>ell)
 <=P(Pois(T)>m)+P(Pois(T(1+m)^2)>ell).

Let K=3+2m+ell and assume N>2K. On the complement, S=A+C+D+E<K and B>N/2. Before the actual process has a bad event or leaves these two bounds, its full generator satisfies

 L A <=1+2K^2-(N/2-K)A,
 bad intensity <=(1+5K)A.

The positive A terms from the2A reverse arms are at most AS; all negative terms may be discarded except -AB. Stopped Dynkin, A(0)=0 and A>=0 yield

 E integral_0^stop A(s)ds <=(1+2K^2)T/(N/2-K).

The compensator of the first bad event consequently gives the explicit bound

 P_xN(any bad event before T)
 <=P(Pois(T)>m)+P(Pois(T(1+m)^2)>ell)
   +(1+5K)(1+2K^2)T/(N/2-K).                         (1)

All stopped quantities are integrable by the Poisson total-count domination. First choose m,ell to make the two ordinary tails small, then send N to infinity. For EVERY fixed finite T,

 P_xN(any A death before T) ->0.                       (2)

This is a continuing actual process statement, not a frozen-bulk assumption or a chosen favorable path probability. Competing reactions and external immigrants have been paid. It shows why connectivity of the binary complex graph does not supply a population-uniform fixed-horizon A-occupation service.

## Exact exponential-total-count growth over each fixed horizon

Let D_A(T) be the actual death count. Then Ntot(T)=N+2+I(T)-D_A(T). For any r>1,

 E_xN r^[Ntot(T)-(N+2)] ->exp[T(r-1)]                 (3)

as N tends to infinity. The upper bound is the immigration mgf. The difference from that upper bound is at most

 (E r^(2I(T)))^(1/2) P(D_A(T)>0)^(1/2),

which vanishes by(2). No independence of the death count and immigration is used.

## Obstruction to the accepted bounded-multiplier representation

Suppose some r>1 and finite positive c,C,zeta,K0 admitted a function W on ALL states satisfying

 c r^Ntot <=W<=C r^Ntot,
 L W<=-zeta W+K0.

Poisson domination makes the required finite-time Dynkin/localization receiving legitimate. Its expectation inequality, divided by r^(N+2), and then(3), would imply for every fixed T

 c exp[T(r-1)] <=C exp[-zeta T].

Choosing T>log(C/c)/(r-1+zeta) contradicts this. Therefore NO geometric Foster function uniformly comparable to r^Ntot exists in this model. In particular, merely extending the accepted t^N times bounded positive face-profile architecture cannot solve the general connected-path problem.

This does not rule out an unbounded or anisotropic multiplier, another Lyapunov geometry, a multi-time drift argument, or a useful new theorem for the general path class. It certainly does not rule out recurrence or all stationary exponential moments: this countermodel has both by ordinary detailed balance. The earned lesson is that the missing return service requires a materially different construction, not an automatic graph-path substitution or a general instability claim.
