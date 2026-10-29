# From a finite physical record to a prepared experiment

29 October 2026. Root construction, extending GENERAL_THERMAL_MEMORY_METRICS.md.
The forward warm-preparation theorem was independently derived by
physical_frontier/GENERAL_THERMAL_MEMORY_INDEPENDENT_REVIEW.md, Section 6.
The finite clock construction below supplies an additional implementation
step. Neither an equilibrium driver source nor an apparatus was operated.

## 1. Precisely what is prepared

Retain the autonomous equilibrium kinetic driver, one-way applied force
f_alpha(X)=sum_i alpha_i phi_i(X), receiver damping gamma, common bath
temperature tau and fixed physical reversal of the general record theorem.
The acquired record contains a simultaneous heat upper bound

    sigma_up(alpha)=max(0,[alpha^T Hhat alpha+eta_H ||alpha||^2]/tau).

The feature family is fixed before acquisition. Coefficients may subsequently
depend on that calibration data. SERVICE uses an actual fresh equilibrium
driver, independent of that data and previous service histories, and an
independent receiver with thermal momentum N(0,tau) and uniform circle phase.
Those preparations and calibrated actuation are paid source gates.

Apply the selected fixed force for a forward interval of length b. Write
rho_b^warm for the full resulting state and rho_f^stat for the stationary
coupled source. Then, in both KL directions,

    D(rho_b^warm || rho_f^stat),
    D(rho_f^stat || rho_b^warm)
                  <= exp(-2gamma b) sigma[f]/(2gamma).       (1)

For every future horizon, and every common causal experiment on that full
source with the same conditional apparatus dynamics and policy,

    TV(P_future,warm,P_future,stat)
                  <= exp(-gamma b) sqrt[sigma[f]/(4gamma)].  (2)

The horizon does not multiply this preparation error. The complete future
experiment is a Markov kernel of the prepared full state. This covers bounded
future decisions, not unbounded lifetime means without uniform integrability.
The apparatus must have the same conditional initialization in both comparisons.
Fresh common apparatus memory, with any warm-up reports discarded, is sufficient.
A retained warm-up transcript is extra correlated information and is not supplied
by the state-only bound (1).

### Ordinary proof

A stationary two-sided driver is a proof coupling. Set

    Y_t=int_0^infinity exp(-gamma s) f(X_(t-s)) ds,
    Y_t^0=int_0^t exp(-gamma(t-s)) f(X_s) ds
         =Y_t-exp(-gamma t)Y_0.

Conditional on the entire common driver history, the stationary and warm
receiver momenta at b are Gaussians of the SAME variance tau. Their means
differ by exp(-gamma b)Y_0. Both initial-state comparisons therefore have
conditional Gaussian KL exp(-2gamma b)Y_0^2/(2tau). The history marginal is
the same. Average, use E Y_0^2=tau sigma/gamma, and discard the history except
the current driver state. The receiver phase can be represented by a common
independent uniform terminal phase, since translating an independent uniform
phase by any realized past displacement leaves it uniform and independent.
This proves both directions of (1) for the full state. Data processing and
Pinsker give (2).

No stationary forcing-history oracle is used in execution. Only the actual
forward interval [0,b] is executed. No unobserved global mixing coefficient
is inserted: the already specified linear receiver damping supplies the
explicit lost-history factor. Equilibrium preparation of the DRIVER remains
a separate gate and is not obtained from visible mixing or this proof.

On the calibration confidence event, a target preparation TV epsilon is met by

    b=max(0, gamma^-1 log[sqrt(sigma_up/(4gamma))/epsilon]), (3)

with b=0 when sigma_up=0. The general signed-correlation work bound gives

    W_prepare <= tau sigma_up (4b+2/gamma).                (4)

This is work on the declared particles; field generation, sensors, clock,
controller and preparing the driver/receiver are additional real costs.
The estimate remains conservative at b=0, where actual preparation work is zero.

If the supplied initial product preparation is only within epsilon_init
in TV of the stipulated law, add epsilon_init to (2) by a triangle inequality
and propagation through the same dynamics. An initial error certificate must
be acquired separately; fitting a stationary visible record does not give one.

## 2. A finite clock, rather than a free exact real time

The exponential-lag acquisition in the general theorem can be implemented
with finite random bits and a finite grid, with an explicit bias charge.

Assume now the observable features are bounded and Lipschitz in driver position:

    |phi_i|<=B_i,  |phi_i(X)-phi_i(X')|<=L_i d(X,X').

These are physical calibration/structural bounds, not fitted conclusions.
The driver has d unit-mass momenta with equilibrium E|P|^2=d tau. Fix
T_c=M Delta. Use grid times t_k=k Delta for k=0,...,M-1 and a censor outcome *.
The ideal probabilities are

    p_k=exp(-gamma t_k)-exp(-gamma(t_k+Delta)),
    p_*=exp(-gamma T_c).                                 (5)

When outcome k occurs, read phi at 0 and t_k and record
sym(phi_0 phi_(t_k)^T)/gamma. At * record the zero matrix.
Always acquire the initial outer product for G. This is the left-grid
version of the exponentially sampled record.

Let q be a rational probability vector actually implemented by b fair random
bits, with an interval-certified TV(q,p)<=rho_clock. This can be constructed
by rounding each p_k DOWN to a multiple of 2^-b and assigning the remainder
to the censor outcome. Interval bounds on each exponential certify the total
rounding error. The clock draw then uses exactly b random bits and integer
comparisons; no exact irrational random draw is asserted.

Suppose each executed lag differs from t_k by at most delta_t, and this clock
error is independent of the physical driver path (or has the stated conditional
bound under independent clock choices). Bounds on timing alone do not control
arbitrary discontinuous features; that is why the L_i are explicit here.

For a stationary driver and deterministic s,t,

    E d(X_s,X_t) <= |s-t| E|P| <= |s-t| sqrt(d tau).

Consequently the symmetric lag correlation changes by at most

    [(B_i L_j+B_j L_i)/2] sqrt(d tau) |s-t|.               (6)

Comparing the grid time to every S in its interval, then charging the actual
timing error, gives the extra operator-norm bias

    eta_time <= sqrt(d tau) (Delta+delta_t)
                         ||B||_2 ||L||_2 / gamma.        (7)

Indeed the absolute quadratic form is bounded by the product
(sum |z_i|B_i)(sum |z_i|L_i), which is at most
||z||^2 ||B||_2 ||L||_2. Probability rounding contributes at most

    eta_bits <= 2 rho_clock ||B||_2^2/gamma,              (8)

because the recorded matrix norm is bounded by ||B||_2^2/gamma and the
total variation is half the probability L1 distance. The censored tail is

    eta_tail <= ||B||_2^2 exp(-gamma T_c)/gamma.           (9)

Thus the previous finite-confidence heat certificate remains valid with

    eta_H = eta_sampling + eta_time + eta_bits
                           + eta_tail + eta_sensor + eta_arithmetic. (10)

The bounded range used in Hoeffding is unchanged. The samples are independent
ACROSS actual preparations, irrespective of correlations between entries.
Calibrating gamma and tau is also required; uncertain parameters need their
own interval propagation, not substitution of a nominal value without error.

The corresponding extra execution resources are M stored clock thresholds
(or an exact equivalent sampler), b random bits per pair, a warranted timing
error delta_t and the actual lag evolution. Worst-case trajectory time is
T_c+delta_t. The ideal left-grid mean time is no greater than
(1-exp(-gamma T_c))/gamma, and changing its probability distribution adds
at most rho_clock T_c. Including actual timing error, the mean time is at most
(1-exp(-gamma T_c))/gamma+rho_clock T_c+delta_t.
The censor outcome may be decided before evolving
anything, which only reduces this upper bound. Computing tight exponential
bounds and thresholds has its ordinary bit cost.

This is one sufficient finite instrument construction. A smoother correlation
modulus or a different certified clock can reduce costs. The original ideal
clock theorem did not by itself acquire these resources.

## 3. Reuse across experiments, and the exact independence limit

For m fresh prepared services with conditional preparation errors epsilon_j
uniformly valid for their selected force coefficients, a sequential hybrid
coupling bounds the joint transcript TV by sum_j epsilon_j. Selection may be
adaptive in previous service reports if each next DRIVER really is fresh
and independent and the certificate is uniform over the selected family.
The single calibration failure probability is paid once; it is not multiplied
by the number of coefficient queries on the same simultaneous event.
Unconditionally, the joint transcript bound is at most
delta_calibration+sum_j epsilon_j, capped by one.

Turning a force off and waiting exponentially attenuates its residual shift.
That supplies an unconditional state-law approximation. It does NOT make the
driver independent of earlier reports, erase all hidden correlations, or
supply a fresh microscopic reset at finite time. Without the fresh-driver
gate or a separate operational regeneration theorem, an iid reuse claim is
not justified.

## 4. Consequence and comparison

The additional capability is a complete route from time-paired feature data
to bounded-confidence heat, a precise native equilibrium explanation cost,
a finite forward preparation and complete future-experiment error. The
record does not reconstruct the driver and does not execute it in software.
Its source-class assumptions remain substantive, and new driver interventions
generally require new information.

An equally informed conventional route uses the same pair correlations,
Gaussian conditional KL, linear filtering, dense matrix calculations and
finite-clock quadrature. This construction does not beat those operations.
Its contribution is their exact physical compatibility and the resulting
preparation and consequence guarantee with every interface stated.

