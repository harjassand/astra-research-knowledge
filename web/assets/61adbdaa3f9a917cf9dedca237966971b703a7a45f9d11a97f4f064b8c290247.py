#!/usr/bin/env python3
"""Exact rational audit for the two-mode mass-action witness in proof.md.

This checks the algebraic drift representation, rate envelope, collar lower
bounds, and the common-interval obstruction. It does not check the stochastic
martingale theorem or establish novelty.
"""

from fractions import Fraction as F
from math import comb
import json


def poly_from_roots(roots):
    """Low-to-high coefficients of -prod(x-r)."""
    coeffs = [F(1)]
    for root in roots:
        updated = [F(0)] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            updated[i] -= root * coeff
            updated[i + 1] += coeff
        coeffs = updated
    return [-coeff for coeff in coeffs]


def bernstein_coefficients(power, degree):
    """Return beta_i in p(x)=sum_i beta_i*C(n,i)x^i(1-x)^(n-i)."""
    return [
        sum(power[k] * F(comb(i, k), comb(degree, k)) for k in range(i + 1))
        for i in range(degree + 1)
    ]


def bernstein_to_power(beta, degree):
    power = [F(0)] * (degree + 1)
    for i, value in enumerate(beta):
        for offset in range(degree - i + 1):
            k = i + offset
            power[k] += (
                value
                * comb(degree, i)
                * comb(degree - i, offset)
                * ((-1) ** offset)
            )
    return power


roots = [
    (F(3, 10), F(13, 20), F(19, 20)),
    (F(1, 20), F(7, 20), F(4, 5)),
]
drifts = [poly_from_roots(r) for r in roots]
betas = [bernstein_coefficients(p, 3) for p in drifts]
assert all(bernstein_to_power(b, 3) == p for p, b in zip(drifts, betas))
assert all((b[0] > 0 and b[1] < 0 and b[2] > 0 and b[3] < 0) for b in betas)

rates = [[abs(bi) * comb(3, i) for i, bi in enumerate(b)] for b in betas]
assert max(max(row) for row in rates) == F(567, 1000)
assert max(max(row) for row in rates) < F(3, 5)

# Factorwise exact lower bounds for |f_j| on the four one-sided collars.
collar_lower_bounds = [
    F(9, 100) * F(44, 100) * F(74, 100),
    F(1, 5) * F(7, 50) * F(11, 25),
    F(11, 25) * F(7, 50) * F(3, 10),
    F(21, 25) * F(27, 50) * F(9, 100),
]
assert min(collar_lower_bounds) == F(1232, 100000)
assert min(collar_lower_bounds) > F(1, 100)

# Any common interval Q in [1/10,9/10] containing Q1 and Q2 has upper
# endpoint 9/10, where mode 1 points strictly outward.
def eval_poly(coeffs, x):
    return sum(coeff * x**i for i, coeff in enumerate(coeffs))


outward_drift_at_safe_upper = eval_poly(drifts[0], F(9, 10))
assert outward_drift_at_safe_upper == F(3, 400)
common_right_endpoint_intervals = [
    (F(501, 1000), F(13, 20), eval_poly(drifts[0], F(11, 20)), eval_poly(drifts[1], F(11, 20))),
    (F(13, 20), F(4, 5), eval_poly(drifts[0], F(3, 4)), eval_poly(drifts[1], F(3, 4))),
    (F(4, 5), F(9, 10), eval_poly(drifts[0], F(17, 20)), eval_poly(drifts[1], F(17, 20))),
]
assert common_right_endpoint_intervals[0][2] < 0 < common_right_endpoint_intervals[0][3]
assert common_right_endpoint_intervals[1][2] > 0 and common_right_endpoint_intervals[1][3] > 0
assert common_right_endpoint_intervals[2][2] > 0 > common_right_endpoint_intervals[2][3]

# Generic finite-volume theorem constants for both modes.
K = F(3, 5)
E_sum = F(8)
D = K * E_sum
B = K * 4
Lambda = K * 4
gamma = F(1, 100)
ell = F(1, 100)
mu = gamma / 2
theta = min(F(1), mu / (3 * B))
c = theta * ell
V0 = (2 * D / gamma).__ceil__()
d_guard = F(9, 1000)
initial_exponent = theta * d_guard
C = 2 * 2 * Lambda

# Large-volume first-jump exit probability when mode 2 starts exactly on its
# lower facet x=49/100. Here b and d are deterministic concentration hazards.
x_boundary = F(49, 100)
y_boundary = 1 - x_boundary
k0, k1, k2, k3 = rates[1]
birth_boundary = k0 * y_boundary**3 + k2 * x_boundary**2 * y_boundary
death_boundary = k1 * x_boundary * y_boundary**2 + k3 * x_boundary**3
zero_margin_first_exit_probability = death_boundary / (birth_boundary + death_boundary)
assert zero_margin_first_exit_probability == F(677803, 1603606)

result = {
    "drift_power_coefficients_low_to_high": [[str(c) for c in p] for p in drifts],
    "drift_bernstein_coefficients": [[str(c) for c in b] for b in betas],
    "mode_reaction_rates_in_order_up0_down1_up2_down3": [
        [str(c) for c in row] for row in rates
    ],
    "max_rate": str(max(max(row) for row in rates)),
    "collar_abs_drift_lower_bounds": [str(x) for x in collar_lower_bounds],
    "mode1_drift_at_safe_upper_9_10": str(outward_drift_at_safe_upper),
    "common_interval_right_endpoint_sign_partition": [
        {
            "interval": [str(lo), str(hi)],
            "mode1_sign_at_interior_witness": str(mode1_sign),
            "mode2_sign_at_interior_witness": str(mode2_sign),
        }
        for lo, hi, mode1_sign, mode2_sign in common_right_endpoint_intervals
    ],
    "zero_margin_mode2_first_jump_exit_probability_limit": str(
        zero_margin_first_exit_probability
    ),
    "generic_certificate_constants": {
        "D": str(D),
        "B": str(B),
        "Lambda": str(Lambda),
        "gamma": str(gamma),
        "ell": str(ell),
        "theta": str(theta),
        "c": str(c),
        "V0": V0,
        "guard_gap_d": str(d_guard),
        "theta_times_guard_gap": str(initial_exponent),
        "C_2mLambda": str(C),
    },
    "risk_bound_for_N_segments": (
        "2*N*exp(-V/160000) + (48/5)*V*T*exp(-V/144000)"
    ),
    "scope": "exact arithmetic only; no stochastic proof or novelty validation",
}
print(json.dumps(result, indent=2))
