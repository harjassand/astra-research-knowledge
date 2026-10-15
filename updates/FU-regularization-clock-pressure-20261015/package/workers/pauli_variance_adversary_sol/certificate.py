#!/usr/bin/env python3
"""Exact continuum certificate for tr Sigma >= 121507/16000.

No third-party packages. All decision arithmetic is fractions.Fraction.
The finite grid is upgraded to the whole interval by a rigorous curvature
bound, and the infinite tail is handled by a quadratic lower bound.
See PROOF.md for the reduction from an arbitrary, nonradial POVM.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from pathlib import Path
import hashlib
import json


def atan_bracket(x, terms=30):
    total = sum(((-1) ** j * x ** (2 * j + 1) / (2 * j + 1)
                 for j in range(terms)), F(0))
    following = x ** (2 * terms + 1) / (2 * terms + 1)
    return ((total, total + following) if terms % 2 == 0
            else (total - following, total))


lo5, hi5 = atan_bracket(F(1, 5))
lo239, hi239 = atan_bracket(F(1, 239))
machin_lo, machin_hi = 16 * lo5 - 4 * hi239, 16 * hi5 - 4 * lo239
pi_lo = F(3141592653589793238462643383279, 10 ** 30)
pi_hi = pi_lo + F(1, 10 ** 30)
assert pi_lo < machin_lo < machin_hi < pi_hi
pi_mid = (pi_lo + pi_hi) / 2
pi_error = (pi_hi - pi_lo) / 2

# Degree 33 for sine, degree 32 for cosine, after exact period reduction.
ORDER = 16
sin_remainder = pi_hi ** 35 / factorial(35)
cos_remainder = pi_hi ** 34 / factorial(34)
eta = max(sin_remainder, cos_remainder) + pi_error
assert eta < F(1, 10 ** 20)


@lru_cache(None)
def trig(phase):
    """Rational approximations to sin(pi*phase), cos(pi*phase)."""
    phase -= 2 * ((phase + 1) // 2)  # [-1,1), exact at the true pi.
    x = pi_mid * phase
    square = x * x
    sine_poly, cosine_poly = F(0), F(0)
    for j in range(ORDER, -1, -1):
        sine_poly = sine_poly * square + F((-1) ** j, factorial(2 * j + 1))
        cosine_poly = cosine_poly * square + F((-1) ** j, factorial(2 * j))
    return x * sine_poly, cosine_poly


LAMBDA = F(14587, 1000)
C0 = -F(33171, 1000)
D_TEXT = [
    "66.376948", "0.456434", "2.654797", "0.128355",
    "0.708823", "0.035971", "0.346882", "0.006797",
    "0.210109", "0.014304", "0.121343", "0.040421",
    "0.053209", "0.071045", "-0.005282", "0.107522",
    "-0.062231", "0.145519", "-0.107277", "0.163311",
    "-0.118344", "0.136878", "-0.074047", "0.055310",
]
D = list(map(F, D_TEXT))
assert C0 + 3 * LAMBDA == F(1059, 100)
SUM_D = sum(map(abs, D))

K_DATA = []
for n, d in enumerate(D, 1):
    sn, cn = trig(F(n, 8))
    # Absolute constants use Taylor enclosure, never rounded floats.
    abs_sin, abs_cos = abs(sn) + eta, abs(cn) + eta
    k_hi = pi_hi * n / 8
    K_DATA.append((n, d, sn, cn, abs_sin, abs_cos, k_hi))

curvature = F(2) + sum(
    abs(d) * k_hi ** 2 * (abs_sin / 3 + abs_cos / 4)
    for n, d, sn, cn, abs_sin, abs_cos, k_hi in K_DATA)
spin_slope = sum(abs(d) * abs_cos * k_hi / 3
                 for n, d, sn, cn, abs_sin, abs_cos, k_hi in K_DATA)
assert curvature < 36
assert spin_slope < 11 < LAMBDA
assert F(3, 2) * SUM_D < 110

# Error in one grid summand. For r>=1/40, k>=pi/8, x>=3/320.
# Also r<=20 and n<=24 imply phase=n*r/8<=60.
RECIP_MIN_X = F(320, 3)
delta_x = 60 * pi_error
sinc_error = (eta * RECIP_MIN_X
              + (1 + eta) * delta_x * RECIP_MIN_X ** 2)
j1_error = (eta * (RECIP_MIN_X ** 2 + RECIP_MIN_X)
            + (1 + eta) * delta_x
            * (2 * RECIP_MIN_X ** 3 + RECIP_MIN_X ** 2))
summand_error = (sinc_error + j1_error
                + eta * (F(3, 2) + sinc_error + j1_error))
EVAL_ERROR = F(1, 10 ** 12)
assert SUM_D * summand_error < EVAL_ERROR
assert SUM_D * eta < EVAL_ERROR  # the r=0 endpoint.


def h_plus_approx(r):
    value = r * r - C0 - LAMBDA * r
    for n, d, sn, cn, abs_sin, abs_cos, k_hi in K_DATA:
        if r == 0:
            f = sn
        else:
            phase = F(n, 8) * r
            sx, cx = trig(phase)
            x = pi_mid * phase
            sinc = sx / x
            j1 = sx / (x * x) - cx / x
            f = sn * sinc - cn * j1
        value -= d * f
    return value


STEP = F(1, 40)
GRID_THRESHOLD = F(7, 1000)
minimum, minimum_index = None, None
for index in range(801):
    r = index * STEP
    lower = h_plus_approx(r) - EVAL_ERROR
    assert lower > GRID_THRESHOLD, (index, float(lower))
    if minimum is None or lower < minimum:
        minimum, minimum_index = lower, index

# Linear interpolation and |h''|<36 give this lower bound between nodes.
interval_margin = GRID_THRESHOLD - 36 * STEP * STEP / 8
assert interval_margin > 0

# For r>=20: h_+(r)>=r^2-lambda*r-c-110. This quadratic is increasing.
tail_margin = F(20) ** 2 - 20 * LAMBDA - C0 - 110
assert tail_margin > 0
assert 40 > LAMBDA

receipt = {
    "status": "PASS_EXACT_RATIONAL_CONTINUUM_CERTIFICATE",
    "arithmetic": "fractions.Fraction; no floating-point decision arithmetic",
    "frequency_n_over_8": list(range(1, 25)),
    "lambda": str(LAMBDA), "c": str(C0), "d_decimal_exact": D_TEXT,
    "rounded_operator_output_second_moment_lower_bound": "1059/100",
    "rounded_noise_covariance_trace_lower_bound": "759/100",
    "rounded_isotropic_noise_variance_lower_bound": "253/100",
    "operator_output_second_moment_lower_bound": str(C0 + 3 * LAMBDA + interval_margin),
    "noise_covariance_trace_lower_bound": str(C0 + 3 * LAMBDA + interval_margin - 3),
    "isotropic_noise_variance_lower_bound": str((C0 + 3 * LAMBDA + interval_margin - 3) / 3),
    "grid": {"start": "0", "stop": "20", "step": "1/40", "nodes": 801,
             "enclosed_values_all_exceed": "7/1000",
             "minimum_lower_approx_for_display_only": float(minimum),
             "minimum_node": str(minimum_index * STEP)},
    "curvature_bound": "36",
    "curvature_upper_approx_for_display_only": float(curvature),
    "between_nodes_margin": str(interval_margin),
    "spin_slope_upper_bound": "11",
    "spin_slope_approx_for_display_only": float(spin_slope),
    "tail_start": "20", "tail_margin": str(tail_margin),
    "taylor_order": ORDER, "grid_evaluation_error_bound": str(EVAL_ERROR),
    "cached_trig_arguments": trig.cache_info().currsize,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope": "Exact global scalar inequalities plus analytic POVM reduction; not a formal proof-assistant certificate or proof of the optimal constant.",
}
output = Path(__file__).with_name("CERTIFICATE.json")
output.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
