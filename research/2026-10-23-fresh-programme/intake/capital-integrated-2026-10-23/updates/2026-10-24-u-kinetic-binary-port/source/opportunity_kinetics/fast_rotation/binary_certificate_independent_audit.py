#!/usr/bin/env python3
"""Independent interval audit of the binary-port finite-cycle certificate.

The source's RK4 routine is used only to reconstruct its candidate nodes; the
residual, contraction, and work-integral bounds below are recomputed here.
No target file is edited.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

from mpmath import iv


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "work/opportunity_kinetics/lead/binary_port_finite_cycle.py"
CERTIFICATE = ROOT / "work/opportunity_kinetics/lead/binary_cycle_certified.json"

spec = importlib.util.spec_from_file_location("binary_model", SOURCE)
model = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.dont_write_bytecode = True
spec.loader.exec_module(model)

cert_doc = json.loads(CERTIFICATE.read_text())
cert = cert_doc["interval_certificate"]
assert cert_doc["model"] == "geometric"
assert cert["amplitude_exact"] == "0.3"
assert cert["frequency_exact"] == "0.01"
n = int(cert["proposed_profile_intervals"])
a_text, nu_text = cert["amplitude_exact"], cert["frequency_exact"]

# Reconstruct the candidate only. The proof below uses independent interval
# formulas and treats the first two binary64 node coordinates as exact dyadics.
profile, _numeric = model.numeric_profile(n, float(a_text), float(nu_text), False)
assert len(profile) == n + 1
assert profile[-1, 0] == profile[0, 0] and profile[-1, 1] == profile[0, 1]

iv.dps = 45
a, nu = iv.mpf(a_text), iv.mpf(nu_text)
pi_iv = iv.pi
dt = 2 * pi_iv / (nu * n)
half_time = dt / 2
half_angle = nu * half_time
exp_max = iv.exp(a / 2)
d0 = iv.mpf(26) / 25
d_max = d0 * exp_max
q1_bound = d_max * a * nu
q2_bound = d_max * nu**2 * (a + a**2 / 2)
q_min = iv.mpf(1) / 1000 / exp_max
gamma = 3 * q_min

f = [1, 0, 0]
q0 = [
    [Fraction(-3120, 3000), Fraction(480, 3000), Fraction(3, 3000)],
    [Fraction(3000, 3000), Fraction(-483, 3000), Fraction(10, 3000)],
    [Fraction(120, 3000), Fraction(3, 3000), Fraction(-13, 3000)],
]


def from_dyadic(x: float):
    f = Fraction.from_float(float(x))
    return iv.mpf(f.numerator) / f.denominator


def upper(x) -> float:
    return math.nextafter(float(x.b), math.inf)


def matvec(matrix, vector):
    return [sum((matrix[i][j] * vector[j] for j in range(3)), iv.mpf(0))
            for i in range(3)]


def l1(vector):
    return sum((abs(x) for x in vector), iv.mpf(0))


def q_and_time_derivative(theta):
    h = a * iv.cos(theta)
    hdot = -a * nu * iv.sin(theta)
    q = [[iv.mpf(0) for _ in range(3)] for _ in range(3)]
    qdot = [[iv.mpf(0) for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            if row == col:
                continue
            delta = f[row] - f[col]
            base = iv.mpf(q0[row][col].numerator) / q0[row][col].denominator
            q[row][col] = base * iv.exp(h * delta / 2)
            qdot[row][col] = q[row][col] * delta * hdot / 2
    for col in range(3):
        q[col][col] = -sum(q[row][col] for row in range(3) if row != col)
        qdot[col][col] = -sum(qdot[row][col] for row in range(3) if row != col)
    return q, qdot


max_r0 = max_r1 = max_slope = max_residual = 0.0
w_profile = iv.mpf(0)
for k in range(n):
    # Define the exact node as two exact dyadic coordinates and their exact
    # affine complement, so the whole interpolant is normalized by definition.
    left = [from_dyadic(profile[k, 0]), from_dyadic(profile[k, 1])]
    right = [from_dyadic(profile[k + 1, 0]), from_dyadic(profile[k + 1, 1])]
    left.append(1 - left[0] - left[1])
    right.append(1 - right[0] - right[1])
    assert all(float(x.a) > 0 for x in left + right)
    assert left[0] + left[1] + left[2] == 1
    assert right[0] + right[1] + right[2] == 1

    pmid = [(x + y) / 2 for x, y in zip(left, right)]
    slope = [(y - x) / dt for x, y in zip(left, right)]
    theta = 2 * pi_iv * (2 * k + 1) / (2 * n)
    q, qdot = q_and_time_derivative(theta)
    rmid = l1([slope[i] - matvec(q, pmid)[i] for i in range(3)])
    rdot_mid = l1([-matvec(qdot, pmid)[i] - matvec(q, slope)[i]
                   for i in range(3)])
    slope_norm = l1(slope)
    # r'' = -Q'' p - 2 Q' p'; the induced 1-norm bounds use the maximum
    # exit rate and |f_i-f_j| <= 1 for this binary port.
    r_bound = rmid + half_time * rdot_mid + half_time**2 / 2 * (
        q2_bound + 2 * q1_bound * slope_norm
    )
    max_r0 = max(max_r0, upper(rmid))
    max_r1 = max(max_r1, upper(rdot_mid))
    max_slope = max(max_slope, upper(slope_norm))
    max_residual = max(max_residual, upper(r_bound))

    # Exact integral on one line segment. Here half_time is dt/2, while
    # half_angle = nu*half_time; this distinction is essential.
    w_profile += 2 * a * (
        pmid[0] * iv.sin(theta) * iv.sin(half_angle)
        + slope[0] * iv.cos(theta) *
        (iv.sin(half_angle) / nu - half_time * iv.cos(half_angle))
    )

state_error = iv.mpf(max_residual) / gamma
work_error = 4 * a * state_error  # ||f||_infty=1; int |hdot| dt = 4a.
work_enclosure = w_profile + iv.mpf([-1, 1]) * work_error

# Independent consistency checks against the saved certificate's displayed
# upper bounds and enclosure. Its decimal intervals are compared numerically;
# all recomputed proof quantities above remain interval enclosures.
assert max_r0 <= cert["max_midpoint_residual_l1_upper"] * (1 + 2e-12)
assert max_r1 <= cert["max_midpoint_residual_derivative_l1_upper"] * (1 + 2e-12)
assert max_slope <= cert["max_profile_slope_l1_upper"] * (1 + 2e-12)
assert max_residual <= cert["global_residual_l1_upper"] * (1 + 2e-12)
assert upper(state_error) <= float(cert["exact_periodic_probability_error_l1_upper"].split(",")[-1].rstrip("]")) * (1 + 2e-12)
assert upper(work_error) <= float(cert["work_error_upper"].split(",")[-1].rstrip("]")) * (1 + 2e-12)
assert float(work_enclosure.b) < 0

print(json.dumps({
    "candidate_nodes_reconstructed": n + 1,
    "exact_dyadic_complement_normalization": True,
    "dt_time_units": str(dt),
    "half_time": str(half_time),
    "half_phase": str(half_angle),
    "base_max_exit": str(d0),
    "uniform_min_offdiagonal_lower": str(q_min),
    "uniform_TV_contraction_rate_lower": str(gamma),
    "qdot_operator_norm_upper": str(q1_bound),
    "qddot_operator_norm_upper": str(q2_bound),
    "midpoint_residual_l1_upper": max_r0,
    "midpoint_residual_derivative_l1_upper": max_r1,
    "profile_slope_l1_upper": max_slope,
    "global_residual_l1_upper": max_residual,
    "periodic_probability_l1_error_upper": str(state_error),
    "piecewise_linear_work_on": str(w_profile),
    "work_error_upper": str(work_error),
    "exact_periodic_work_on_enclosure": str(work_enclosure),
    "certified_negative_work_on": float(work_enclosure.b) < 0,
}, indent=2))
