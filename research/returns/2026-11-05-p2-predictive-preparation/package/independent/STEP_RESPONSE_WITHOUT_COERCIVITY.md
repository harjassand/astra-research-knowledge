# Finite-horizon response regularity from dissipation alone

## Lemma

Let a causal time-invariant linear plant have coordinate x, input force f,
nonnegative storage E, and a calibrated strict velocity-dissipation inequality

    E(t)-E(0) <= integral_0^t [f(s)xdot(s)-Gamma xdot(s)^2]ds,
    Gamma>0.

The zero state has E(0)=0 and x(0)=0. Let S be its response to the mathematical
unit step f=1. No quadratic storage lower bound on x is assumed.

For every finite L,

    Gamma integral_0^L |S'|^2 <= S(L)
       <= sqrt(L) ||S'||_L2(0,L).

Consequently

    ||S'||_L2(0,L) <= sqrt(L)/Gamma,                            (1)
    0<=S(t)<=t/Gamma for 0<=t<=L,
    |S(t)-S(s)| <= sqrt(L|t-s|)/Gamma, 0<=s,t<=L.              (2)

The same result follows from Young's inequality with nonnegative final storage.
The step is a mathematical response representation. An actual finite positive
ramp of duration h changes it by at most sqrt(Lh)/Gamma over the covered horizon,
with a modest enlarged L if the measurement schedule requires it. A positive
position average of width b gives the analogous sqrt(Lb)/Gamma allowance.

Thus a finite-horizon uniform step-response acquisition theorem does not require
a spectral gap, a hidden dimension, positivity of a memory kernel, or even
static coercivity. A grid spacing Delta=O(Gamma^2 eta_S^2/L) gives interpolation
error O(eta_S); the number of grid intervals is O(L^2/(Gamma^2 eta_S^2)). Actual
metrology, input accuracy, initialization and processing remain separately paid.

## What the added spring improves

If storage also obeys E>=mu x^2/2, the algebraically shifted functional
E-x+1/(2mu) is nonnegative and initially equals 1/(2mu). Under the unit step its
derivative is at most -Gamma xdot^2. Thus

    ||S'||_L2(0,infinity) <= 1/sqrt(2mu Gamma).

This yields the stronger, horizon-independent modulus
|S(t)-S(s)|<=sqrt(|t-s|/(2mu Gamma)). A known permanent spring supplies a physical
coercivity constant even if the bare passive plant's stiffness is unknown.

The same spring supplies a static coordinate range from a storage bound, which
in turn bounds its reaction force and the digitizer range. Without coercivity,
finite-time prediction is still possible mathematically, but the physical
architecture must obtain range and reaction bounds in another way. For example,
a known initial position and a finite motion-energy budget give the paid
horizon-dependent excursion |x(t)-x(0)|<=sqrt(t E0/Gamma) during a quiet phase.
Therefore the spring is a convenient earned hardware interface, not a necessary
mathematical premise of (1).

## Normalizations useful in the joined theorem

Quiet randomized initialization replaces E0 by E0/Gamma in its motion budget.
After an input program f,

    E_after <= E_before + ||f||_L2^2/(4Gamma).

With coercivity, a zero-state force error e produces displacement at most

    ||R e||_infinity <= ||e||_L2/sqrt(2mu Gamma).

Without coercivity, its finite-horizon substitute is

    ||R e||_infinity,[0,L] <= sqrt(L)||e||_L2(0,L)/Gamma.

These constants follow directly from the same physical energy inequality.
Linearity is used for the superposition and response-error statements, not for
the elementary quiet-window energy bound.

