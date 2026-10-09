"""Exact rational checks of the continuum proof's displayed constant bounds.

This uses no spatial grid, time simulation, or sampled spectrum.  It checks
closed analytic bounds, not the validity or novelty of the whole theorem.
Pi is enclosed by the alternating series in Machin's identity
pi=16*atan(1/5)-4*atan(1/239).  The identity follows from the tangent addition
formula with the angles in the principal quadrant.
"""

from fractions import Fraction as F
import json


def atan_interval(x, terms):
    partial = sum(((-1) ** j) * x ** (2 * j + 1) / (2 * j + 1)
                  for j in range(terms))
    other = partial + ((-1) ** terms) * x ** (2 * terms + 1) / (2 * terms + 1)
    return min(partial, other), max(partial, other)


lo5, hi5 = atan_interval(F(1, 5), 18)
lo239, hi239 = atan_interval(F(1, 239), 5)
pi_lo, pi_hi = 16 * lo5 - 4 * hi239, 16 * hi5 - 4 * lo239
assert 0 < pi_hi - pi_lo < F(1, 10**25)

R, beta, nu = F(1001, 1000), F(151, 100), F(1, 1000)
P, delta = 2 * R, R - 1
base_d = beta * F(32, 35) - 3 * pi_hi / 8
d_plus = pi_lo / R - beta
assert d_plus > beta
base_s = base_d - 1152 * delta**2 / beta
base_eta = beta * d_plus * base_s / (P * F(46, 10)**2)
assert base_eta > F(11708, 10**6)
assert base_eta > F(1, 100)

hetero_s = base_d - nu * F(32, 35) - 1152 * delta**2 / (beta - nu)
hetero_eta = (beta - nu) * (d_plus - nu) * hetero_s / (P * (F(46, 10) + nu)**2)
assert hetero_s > F(200796, 10**6)
assert hetero_eta > F(116, 10**4)
assert hetero_eta > F(1, 100)

sqrt2_lo, sqrt2_hi = F(1414, 1000), F(1415, 1000)
assert sqrt2_lo**2 < 2 < sqrt2_hi**2
assert 3 * pi_hi / sqrt2_lo < 8
holder_K_bound = 8 * (2 * sqrt2_hi / (F(3, 4) * pi_lo) + 4 / pi_lo)
assert holder_K_bound < 20

# Use zeta(2)<2 and zeta(3)<4/3, which follow by integral comparison.
tip_image_upper = 8 / pi_lo + F(3, 8)
assert tip_image_upper < 3
sqrt_delta_upper = F(32, 1000)
assert sqrt_delta_upper**2 > delta
arch_height_upper = F(25, 8) * delta + F(3, 4) * sqrt_delta_upper
assert F(9, 2) + arch_height_upper < F(46, 10)
assert 20 + F(3, 4) + F(25, 8) * sqrt_delta_upper < 24

# At epsilon=.01 this entire heterogeneous b family is rate weakening.
assert F(1, 100) * (F(46, 10) + nu) < beta - nu

# Symbolic exponents behind the critical clock and contact-volume mechanism.
r_contact = F(1, 2)
p_memory = (r_contact + 2) / (r_contact + 1)
assert p_memory == F(5, 3)
assert 1 - 1 / p_memory == F(2, 5)

report = {
    "type": "rational_arithmetic_for_closed_continuum_bounds",
    "spatial_grid": False,
    "time_simulation": False,
    "whole_theorem_verification": False,
    "pi_interval": [float(pi_lo), float(pi_hi)],
    "pi_interval_width_upper": str(pi_hi - pi_lo),
    "base_coercivity_eta_over_kappa_lower": float(base_eta),
    "heterogeneous_b_eta_over_kappa_lower": float(hetero_eta),
    "heterogeneous_b_lorentz_negative_margin_lower": float(hetero_s),
    "K_holder_coefficient_upper": float(holder_K_bound),
    "tip_image_upper_over_kappa": float(tip_image_upper),
    "arch_height_upper_over_epsilon_kappa": float(arch_height_upper),
    "critical_memory_power": str(p_memory),
    "all_assertions_passed": True,
}
print(json.dumps(report, indent=2))
