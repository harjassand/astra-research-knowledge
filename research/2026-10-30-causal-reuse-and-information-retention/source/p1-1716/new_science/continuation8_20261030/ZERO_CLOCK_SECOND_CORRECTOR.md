# Native events suffice: a second corrector removes the external shared clock

30 October 2026. Root sustained follow-on construction. This is an addendum to
the reviewed positive-clock action files, which remain unchanged. Its consequence
is operational: the shared bit need not receive an externally timed reset.
It still must be updated atomically by every selected native event and coupled
to every selected port. Global interaction cost does not disappear.

## 1. The remaining zero-clock problem

Use fixed 0<=alpha<1 and the clean native ring rates r_i=c(1+alpha u delta_i),
where each native swap flips u. Set the external shared-clock rate to zero.
For F_H=A_H/A, the first corrector leaves u L_native F_H. The accepted quotient
estimate splits this into c u L_ex F_H+c alpha D F_H. The second term is bounded
by C_H/A and its time integral is superexponentially negligible. The unresolved
term was u g_H with

    g_H=L_ex F_H,  L_ex=sum_i(T_i-I).                       (1)

The inverse-activity theorem itself already holds with zero external clock.
The goal is to turn u g_H into an actual-generator coboundary plus an inverse-
activity remainder, without any hypothetical extra operation.

## 2. The missing finite-difference estimate

For every active exchange i,

    |g_H|<=8||H||_infinity,
    |Delta_i g_H|<=C ||H||_infinity/A.                    (2)

Here C is an absolute constant, independent of N, configuration and any minimum
activity fraction. A>=2 is enough. To prove the second inequality, expand

    Delta_i g_H=sum_j [Delta_j F_H(eta^i)-Delta_j F_H(eta)]. (3)

There are at most five j whose local exchange neighborhoods meet i. On these
terms the first-difference bound |Delta_j F_H|<=8||H||/A, together with
A(eta^i)>=A(eta)/2, bounds their total by C||H||/A.

For every other j, exchanges i,j commute and their local changes of A and A_H
are unaffected by the other exchange. Thus the corresponding term is a mixed
second difference of y/x, at x=A,y=A_H, in two directions (a,p),(b,q) with
|a|,|b|<=2 and |p|,|q|<=2||H||. If A>=8, every denominator in the interpolation
rectangle is at least A/2. Its second derivatives bound this difference by
C||H||/A^2. If 2<=A<8, all four actual configurations have activity at least
two; |F_H|<=||H|| bounds the difference by 4||H||, which is again at most
196||H||/A^2. Only originally active distant j contribute, at most A of them;
distant inactive j remain inactive after i. Summing proves (2).

This is precisely the extra locality information missing from a crude bounded
g_H estimate. It does not assert D(phi(A))=0 for nonlinear phi.

Put

    h_H=g_H/A.

Since |Delta_i A|<=2 and A(eta^i)>=A/2, (2) implies

    |h_H|<=C_H/A,  |Delta_i h_H|<=C_H/A^2,
    |L_native h_H|<=C_H/A.                               (4)

The last bound uses at most A active native events and bounded rates. None
of these estimates substitutes a typical activity of order N for a rare A.

## 3. Exact generator identity and superexponential control

Every native transition sends u to -u and the clean total native rate is cA.
Therefore

    L_native(u h_H)=-2c u A h_H-u L_native h_H,
    u g_H=-(1/(2c))L_native(u h_H)
                          -(1/(2c))u L_native h_H.       (5)

Apply the actual Dynkin martingale to u h_H. The endpoint divided by N^2 is
O(N^-2). Each native jump has size |h_H(eta^i)+h_H(eta)|<=C_H/A; its physical
bracket rate is at most C_H/A<=C_H/2. Hence the martingale divided by N^2 on
physical time N^2T is superexponentially negligible at speed N, by the bounded-
jump exponential inequality. The integral of the second term in (5) is bounded
by C_H int_0^T A^-1dt, already proved superexponentially negligible.

It follows that

    int_0^T u L_ex F_H(eta_(N^2t))dt
          is speed-N superexponentially negligible.       (6)

For smooth time-dependent H, h_H is linear in H at each configuration, with
the same bounds for its time derivative. Dynkin's added derivative term is
O(N^-2) after the current normalization. Uniform-in-terminal-time estimates
follow from maximal martingale bounds and inverse-activity domination.

The first weighted-current correction consequently holds at zero clock. All
these base-law superexponential statements transfer to bounded weak comparison
tilts by the same exact second-moment likelihood identity. The previously
reviewed spatial-tilt receiver, action topology, lower approximation and proof
of goodness therefore apply unchanged. The complete nonlocal action is (3) of
`NONLOCAL_ACTION_FROM_EVENT_MEMORY.md`, now also for gamma_N=0.

## 4. Compatibility with hidden phase amplitudes

Use the actual combined supplier
r_i=bar r_i[1+zeta_i cos(theta_i)] from
`HIDDEN_KINETICS_AND_DESIGNED_MEMORY.md`, with |zeta_i|<=b<1 and independent
phase diffusion kappa_N->infinity, but with NO external shared-bit clock.
Write R_tot=sum_i bar r_i zeta_i cos(theta_i). The actual total native rate is
cA+R_tot, and the exact replacement for (5) is

    u g_H=-(1/(2c))L_actual(u h_H)
           -(1/(2c))u L_actual h_H-(1/c)u R_tot h_H.      (7)

The phase generator acts trivially on u h_H and h_H. Bounded actual native
rates and (4) still give |L_actual h_H|<=C_H/A and a martingale bracket rate
at most C_H/A. The final term in (7) is phase-linear, with coefficients
u bar r_i zeta_i h_H bounded uniformly and independent of all actuated phases.
The established independent-phase Feynman--Kac estimate removes its accumulated
contribution at speed N. Use the valid bound sum_i||coefficient_i||_infinity^2
<=C_H N; no supremum/sum interchange is assumed.

Thus the same full programmed nonlocal action remains valid uniformly over
the stated arbitrary bounded hidden amplitudes, with only the supplied native
event updates and independent phase actuators. Initial arbitrary phases use
the same active warmup; actual initial association and full future laws remain
required. Hidden memory is neither copied nor reset.

## 5. Optional external resets and the complete slow-clock range

If 0<=gamma_N<=1, the generator identity (5) adds a remainder proportional to
gamma_N u h_H, which is bounded by C_H/A. Clock jumps of u h_H have bounded
bracket rate. The first corrector's clock occupation and martingale terms
remain negligible; for its bounded odd occupation term at very small gamma,
one can instead apply the same native identity to u F_H using h=F_H/A.
Its native remainder is O(1/A), while its amplitude and bracket remain bounded.
More explicitly, Delta_i(F_H/A)=O(A^-2), so this second application is identical
to (4)--(7), with gamma_N bounded. Therefore bounded nonnegative external rates,
including zero, require no inverse-gamma estimate.

For gamma_N>1 and gamma_N/N->0 the already reviewed positive-clock proof applies.
Splitting a sequence into these two regimes proves the same action for every
nonnegative gamma_N=o(N). This enlargement is an optional byproduct; zero clock
is the operationally useful new case.

## 6. What changed and what remains open

The mechanism no longer needs a continuous external shared-bit clock to recover
the desired full law. The bit is driven by the native events themselves. Its
update count remains order N^3 over the diffusive horizon in the warranted
interior regime; global coupling and atomic updates remain real resources.
The independent phase ports are still needed for the displayed unknown-kinetics
class, rather than inferred from the event bit alone.

Uniform ellipticity still uses fixed alpha<1 and b<1. The full spatial action
at alpha=1, or with unknown closed gates b=1, is not proved here. Exact bounded
current at alpha=1 remains valid under its separate transition-support premise.
The second-corrector argument does not imply a finite-N acquired confidence
bound, a joint apparatus-record LDP, or historical novelty of corrector methods.
