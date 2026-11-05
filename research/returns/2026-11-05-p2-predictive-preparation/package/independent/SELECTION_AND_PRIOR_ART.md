# Independent route: delayed passive echoes and randomized selection

## Initial construction before concentration

The independently chosen question was whether finite response memory implies
that an energy-bounded retained environment can be predictively initialized.
The first explicit construction used a conservative oscillator bath with

    K(t)=B(1-|t|/h)_+.

Its positive spectral density on omega>=0 is

    dnu/domega=2B(1-cos(omega h))/(pi h omega^2),

with the continuous value at zero. Initial phase coordinates proportional to
cos(omega L), sin(omega L) give a delayed triangular free-force pulse. Their
energy is independent of L. The force is exactly absent before L-h, although
the response kernel itself has compact support.

For visible potential mu x^2/2 and opposite pulses of peak A, the observed
trajectory separation at the peak is at least A h/e when h<=1/(mu+B). On the
rise, the positive Volterra integral gives

    d'+(mu+B)d >= 2A(t-(L-h))/h.

This lower bound concerns observed predictions, not merely different kernels.

The root then proposed strengthening the construction to the Lorentzian
conservative realization of an EXACT exponential kernel. Independent Fourier
and energy calculations verified the sharp radius in
CONSERVATIVE_INITIALIZATION_THEOREM.md.

## Quantifier obstacle and constructive change

An attempted extension of the obstruction to all randomized stopping revealed
a different operation. Finite total visible dissipation limits the number of
future windows with appreciable motion. A private uniform choice among disjoint
windows therefore supplies a probabilistically quiet continuation without
equilibrating the bath. RANDOMIZED_PREDICTIVE_INITIALIZATION.md contains the
finite-clock, metrology, backaction, and all-later-input statement.

The root joined this operation to a step-response acquisition method derived
from passivity and known visible storage coercivity. This avoids assuming an
ideal initialized bath and need not identify a microscopic memory kernel.

## Prior comparisons constraining the claim

1. Figotin--Schenker, Hamiltonian structure for dispersive and dissipative
   dynamical systems (2006/2007), construct conservative Hamiltonian extensions
   reproducing dissipative response. This is established machinery.
   https://arxiv.org/abs/math-ph/0608003

2. Mielke--Peletier--Zimmer, Deriving a GENERIC system from a Hamiltonian system,
   arXiv:2404.09284v2, analyze finite-dimensional compressions, deterministic
   prepared data, stochastic preparation, and well-preparedness in Section 5.3.
   The same-response distinction here is not the first recognition that bath
   preparation matters. https://arxiv.org/html/2404.09284v2

3. Ghadimi--Lan, Stochastic First- and Zeroth-Order Methods for Nonconvex
   Stochastic Programming, SIAM J. Optimization 2013, use random output iterates
   in a bounded-descent analysis. The energy averaging inequality has this
   familiar pattern. The physical counterfactual initialization interface is
   what the present construction must earn.
   https://arxiv.org/abs/1309.5549

4. Simchowitz--Mania--Tu--Jordan--Recht, Learning Without Mixing, COLT 2018, give
   nearly minimax OLS identification bounds from a single trajectory without
   standard mixing-time arguments. Avoid a first-learning-without-mixing claim.
   The proposed distinction is unknown-dimensional passive port response with
   arbitrary retained finite-energy state and all later admissible inputs.
   https://proceedings.mlr.press/v75/simchowitz18a.html

Targeted searches did not locate the exact finite-clock physical operation.
That is not a novelty or priority proof. No individual construction here is
declared civilisation-changing.

## Executed evidence

verify_initialization_laws.py and initialization_law_checks.json record
independent quadrature of the exact radius, an attaining energy-constrained
input, Fourier/time energy agreement for the same pulse delayed by 1000, and a
128-block example. The latter has sampled bad-block fraction 3/128 and analytic
energy probability bound 0.26578125.

These are floating mathematical diagnostics, not physical meter observations or
interval-certified ODE solutions. The proofs carry the general claims.

