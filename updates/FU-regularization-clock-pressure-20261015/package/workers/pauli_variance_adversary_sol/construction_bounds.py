#!/usr/bin/env python3
"""Exact elementary enclosures for the feasible delay-kernel variance.

The analytic proof supplies W0 < 4*sqrt(3)-4+(37/3)*w(6).
This script proves W0<3069/1000 and v<19529/7707<2.534.
No ODE solver, quadrature, float decision, or third-party package is used.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib
import json


def root_bracket(number, denominator=10 ** 12):
    numerator = isqrt(number * denominator ** 2)
    lo, hi = F(numerator, denominator), F(numerator + 1, denominator)
    assert lo * lo <= number < hi * hi
    return lo, hi


def log_point_bracket(z, terms=80):
    assert z > 1
    y = (z - 1) / (z + 1)
    total = 2 * sum((y ** (2 * j + 1) / (2 * j + 1)
                     for j in range(terms)), F(0))
    tail = 2 * y ** (2 * terms + 1) / ((2 * terms + 1) * (1 - y * y))
    return total, total + tail


def log_interval(lo, hi):
    return log_point_bracket(lo)[0], log_point_bracket(hi)[1]


lo3, hi3 = root_bracket(3)
lo5, hi5 = root_bracket(5)
lo15, hi15 = root_bracket(15)
lo_acosh2, hi_acosh2 = log_interval(2 + lo3, 2 + hi3)
lo_acosh4, hi_acosh4 = log_interval(4 + lo15, 4 + hi15)

# w(6) = 1 + [2 - 2 sqrt(3) + acosh(2) - acosh(4)] / sqrt(5).
lo_a = 2 - 2 * hi3 + lo_acosh2 - hi_acosh4
hi_a = 2 - 2 * lo3 + hi_acosh2 - lo_acosh4
ratios = [a / root for a in (lo_a, hi_a) for root in (lo5, hi5)]
lo_w6, hi_w6 = 1 + min(ratios), 1 + max(ratios)
assert 0 < lo_w6 < hi_w6 < F(57, 5000)

W0_UPPER = F(3069, 1000)
assert 4 * hi3 - 4 + F(37, 3) * hi_w6 < W0_UPPER
W1_UPPER = 2 * W0_UPPER - 1
V_UPPER = F(23, 9) - 1 / (9 * W1_UPPER)
assert V_UPPER == F(19529, 7707)
assert V_UPPER < F(1267, 500)

receipt = {
    "status": "PASS_EXACT_RATIONAL_FEASIBLE_UPPER_BOUND",
    "arithmetic": "fractions.Fraction; no floating-point decision arithmetic",
    "sqrt_denominator": "1000000000000", "log_series_terms": 80,
    "w6_proved_upper_bound": "57/5000",
    "W0_proved_strict_upper_bound": str(W0_UPPER),
    "W1_proved_strict_upper_bound": str(W1_UPPER),
    "feasible_isotropic_variance_proved_strict_upper_bound": str(V_UPPER),
    "feasible_isotropic_variance_rounded_strict_upper_bound": "1267/500",
    "w6_bracket_for_display_only": [float(lo_w6), float(hi_w6)],
    "upper_bound_for_display_only": float(V_UPPER),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope": "Elementary constant enclosure combined with the analytic delay-kernel proof; not certification of the tighter quadrature decimal or of optimality.",
}
Path(__file__).with_name("CONSTRUCTION_BOUND.json").write_text(
    json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
