#!/usr/bin/env python3
"""Exact and numerical checks for the paired-quadrature assay certificate.

The rational inequalities use only fractions. Floating-point values are
illustrative diagnostics for the exact formulas, not proof inputs.
"""

from fractions import Fraction as F
from math import atan2, ceil, cos, e, exp, factorial, log, sin, tan
import json


# x = tau * |U - 4| = (1/2)(1/100).
x = F(1, 200)
sin_lower = x - x**3 / 6
cos_upper = 1 - x**2 / 2 + x**4 / 24
tan_lower = sin_lower / cos_upper
tan_upper = x / (1 - x**2 / 2)  # sin(x) < x and cos(x) > 1-x^2/2
assert 0 < tan_lower < tan_upper < F(1, 100)

# e = sum 1/k!. For k >= 7, successive terms have ratio at most 1/8,
# so the tail after k=6 is at most (1/7!)/(1-1/8) = 1/4410.
e_partial = sum((F(1, factorial(k)) for k in range(7)), F(0))
e_upper = F(27183, 10000)
assert e_partial + F(1, 4410) < e_upper

# A separate geometric tail bound for exp(1/20) certifies the uniform
# two-quadrature Jacobian conditioning over d <= 2.1.
x05 = F(1, 20)
exp05_upper = 1 + x05 + x05**2 / 2 + (x05**3 / 6) / (1 - x05 / 4)
e105_upper = e_upper * exp05_upper
assert e105_upper < 1 / F(3498, 10000)  # exp(1.05) < 1/0.3498

# Delta = nu_+ - nu_- is increasing in tan(x) on the interval used here.
delta_lower = (
    F(10000, 27183)
    * F(32 * 132098, 257)
    * tan_lower
    / (F(1024) - F(65025) * tan_lower**2)
)
assert delta_lower > F(2959, 100000)  # Delta > 0.02959

# Each model's total Y-mean systematic bias is assumed <= 1e-4.
effective_gap_lower = F(2939, 100000)  # Delta - 2e-4 > 0.02939
assert delta_lower - F(1, 5000) > effective_gap_lower

# Hoeffding exponent for n=50,000 and outcomes in [-1,1].
n_shots = 50_000
exponent_lower = F(n_shots) * effective_gap_lower**2 / 8
assert exponent_lower > F(53, 10)

# A rational Taylor partial sum proves exp(5.3) > 200.
exp_53_lower = sum(
    (F(53, 10) ** k / factorial(k) for k in range(14)), F(0)
)
assert exp_53_lower > 200

# Numerical display only. The symbolic identities and rational lower bounds
# above establish the reported inequalities independently of these floats.
psi = atan2(-255, 32)
xf = float(x)
values = []
for a in (-0.01, 0.01):
    xx = a / 2
    g = cos(xx) + (255 / 32) * sin(xx)
    d = 2 + 2 * log(g)
    r = exp(-d / 2)
    phi = psi + xx
    q_mean = r * cos(phi)
    y_mean = r * sin(phi)
    values.append({"U": 4 + a, "d": d, "X_mean": q_mean, "Y_mean": y_mean})

delta_float = values[1]["Y_mean"] - values[0]["Y_mean"]
delta_formula_float = (
    e ** -1
    * 32
    * 132098
    * tan(xf)
    / (257 * (1024 - 65025 * tan(xf) ** 2))
)
assert abs(delta_float - delta_formula_float) < 1e-14
assert abs(values[0]["X_mean"] - values[1]["X_mean"]) < 1e-15

threshold = (values[0]["Y_mean"] + values[1]["Y_mean"]) / 2
hoeffding_upper = 2 * exp(-float(exponent_lower))
assert hoeffding_upper < 0.01

print(
    json.dumps(
        {
            "model_minus": values[0],
            "model_plus": values[1],
            "Y_threshold": threshold,
            "Y_gap_numeric": delta_float,
            "Y_gap_exact_lower_bound": str(delta_lower),
            "effective_gap_lower_bound_after_bias": str(effective_gap_lower),
            "shots": n_shots,
            "interrogation_time_tau": 0.5,
            "interrogation_native_time": n_shots / 2,
            "Hoeffding_exponent_lower_bound": str(exponent_lower),
            "Hoeffding_error_upper_diagnostic": hoeffding_upper,
            "qfi_at_nominal": {
                "F_UU": 0.25 * exp(-2),
                "F_dd": 0.25 * exp(-2) / (1 - exp(-2)),
                "F_Ud": 0.0,
            },
            "two_quadrature_sigma_min_lower_bound": "1749/10000",
            "two_quadrature_inverse_sensitivity_upper_bound": "20000/3498",
        },
        indent=2,
        sort_keys=True,
    )
)
