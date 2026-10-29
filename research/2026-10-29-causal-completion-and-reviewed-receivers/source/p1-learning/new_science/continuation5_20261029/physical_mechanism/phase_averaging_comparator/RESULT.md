# Completed ordinary comparison: phase kicks and deterministic mirror cycling

29 October 2026. This unit is separate from the completed transport alternative.
The governing proof is `PI_KICK_AND_MIRROR_COMPARATORS.md`; primary predecessors
and their actual read scopes are in `PRIMARY_PHASE_AVERAGING_COMPARISON.md`.

## What the constructive comparison establishes

Actual independent Poisson pi kicks match the general uniform-time,
volume-independent phase-diffusion estimate. If each phase can actually be
flipped by pi at rate gamma, with all other physical coordinates unchanged,
the unknown phase offset becomes a frozen parameter and the orientation is an
independent telegraph sign. Its gap is 2 gamma. For the same reversible visible
projections and arbitrary outside-configuration-dependent amplitudes,

    M_tel = max_i ess sup(s_i beta_i^2),
    r_tel = M_tel/(2 gamma) < 1,
    sup_t ||P exp(-t A_gamma)P - exp(-ta)||
        <= r_tel/[2 sqrt(1-r_tel)].

Here P averages the independent stationary signs, not the untouched original
phase offsets. Since M_tel <= s_max alpha^2, the worst-case ratio equals the
circle-diffusion ratio at gamma=kappa. The proof uses the same relative-form
energy argument, with an actual random-telegraph supplier. This is an ordinary
motional-narrowing alternative; it is not a new physical principle or a claim
that a noise-only interface already supplies pi actuation.

The strongest deterministic comparison is better on a more restricted consumer.
On a common native-invariant sector with

    ||a|| <= L,  -alpha a <= B <= alpha a,

an actual global pi pulse interchanges a+B and a-B. The symmetric cycle

    + for h/2, pi, - for h, pi, + for h/2

has a positive self-adjoint endpoint operator T_h. Its effective generator
-log(T_h)/(2h) differs from a by at most epsilon_h a in relative form, where
epsilon_h is explicit in the governing proof and is O(L^2 h^2). Consequently

    sup_n ||T_h^n - exp(-2nh a)||
        <= epsilon_h/[2 sqrt(1-epsilon_h)].

This controls arbitrarily many cycles without a positive visible spectral-gap
assumption. It holds for each fixed unknown phase and each retained pulse
schedule. After actual conditional mean-zero phase averaging, the all-physical-
time bound adds only 2 alpha^2 L^2 h^2. If the initial orientation is retained
and conditioned on, the general partial-cycle term is instead 2 alpha L h.
A finite-speed forward full rotation followed by exact retracing supplies the
same palindrome proof when uncontrolled drift/noise is absent during it.

For SSEP with configuration-independent unknown bond amplitudes, the linear
density sector is native invariant and L <= Delta s_max. The deterministic
estimate is therefore uniform in volume and includes diffusive times N^2 tau.
This is a real stronger ordinary comparator for that receiver. The symmetric
product itself is conventional Strang splitting; the note proves its actual
operation, relative-log and record scope explicitly.

## Why this does not subsume the broader noise receiver

For amplitudes alpha_i(Y_outside_i,Z), native evolution generally leaves the
linear density sector even when the phase-averaged generator remains SSEP.
Its small one-particle norm cannot then be used as the norm of the native
evolution. The independent-noise and telegraph proofs retain this larger
family; the deterministic bounded-sector theorem does not.

There is also an exact full-space obstruction to an all-time, volume-uniform
quadratic mirror bound. For independent fair spins with independent uniform
phases and commuting heat-bath modes, the parity observable has initial-segment
multiplier

    exp(-Nt) I_0(alpha t)^N.

At t=h/2=1/N its error is asymptotic to alpha^2 h/(8e), although completed
mirror cycles are exact. Synchronous rotation has an analogous inverse-
frequency lower bound. These are matched independent-phase examples, not a
different prior. They refute a quadratic full-space extension, but do not
refute a possible general inverse-frequency deterministic upper bound. That
broader problem remains unresolved in this unit.

An actual absolute phase setter plus hold is stronger still: theta_i=pi/2
sets all modulation terms to zero exactly. Its existence cannot be inferred
from translations, pi kicks, or a diffusion kernel.

## Real preparation, records and control costs

Exact sign averaging requires fresh independent signs conditional on the
complete deployment record and frozen parameters. Retaining their outcomes
removes that premise. Fresh unrecorded telegraph burn-in gives a direct
TV <= min(1,N exp(-2 gamma u)/2) preparation bound only when the phase actuator
can run alone while the visible specimen is actually held fixed. Marginal
sign mixing during concurrent native evolution does not remove visible-sign
correlations. The alternative is an independently warranted joint preparation
contract, not an omitted apparatus record.

All the estimates compare fixed-time endpoint operators. They are not complete
native-path, adaptive-record, or exposed-bath-key guarantees. Converting their
L2 bounds to observable expectations retains the real incoming density norm.
Independent kicks cost N gamma expected local events per unit time. Broadcast
mirror pulses do not establish volume-independent physical action or energy.
Controlled rotation has its own waveform, torque and dissipation requirements.
No common-energy or apparatus comparison has been established.

## Verification and disposition

`check_mirror_density.py` was executed successfully and produced
`PHASE_COMPARATOR_CHECKS.json`. Five declared density-sector cases include
128 sites, gap 0.0012045437948274248, and physical times through N^2. The largest
sampled density error was 0.0000073594363544124895. The checker also evaluates
the relative-log bound, the independent-spin asymptotic floors, a full two-site
outside-dependent telegraph model, and an explicit retained-key counterexample.
These are population numerical checks, not interval certificates or physical
experiments. The proofs, not a finite time grid, supply the uniform guarantees.

The unit is complete. Its positive result is an explicit strong ordinary
supplier and a sharper bounded-sector comparator; its failure result prevents
overextending deterministic cycling to the full many-body quadratic claim.
Motional narrowing, random decoupling and symmetric splitting have close
primary predecessors, whose scope is preserved. No priority, apparatus or
practical speedup claim is made. The general full-space deterministic
inverse-frequency question is left open without further expansion here.
