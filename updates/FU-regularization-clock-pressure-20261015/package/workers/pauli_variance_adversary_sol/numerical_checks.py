#!/usr/bin/env python3
"""Optional NON-CERTIFIED numerical checks; run via uv with numpy/scipy.

These checks do not prove positivity, the exact transform, or decimal
intervals for the delay-kernel variance. PROOF.md supplies analytic proofs.
The independent exact lower-bound checker is certificate.py.
"""
from pathlib import Path
from math import pi, sqrt
import json
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.special import spherical_jn

segments = []


def w(x):
    if x <= 2:
        return 1.0
    index = min(int((x - 2) // 2), len(segments) - 1)
    return float(segments[index].sol(x)[0])


y = 1.0
endpoints = {2: y}
for index in range(13):
    left, right = 2 + 2 * index, 4 + 2 * index
    sol = solve_ivp(lambda x, value:
                    [-(value[0] + w(x - 2)) / (2 * (x - 1))],
                    (left, right), [y], rtol=1e-12, atol=1e-16,
                    dense_output=True, max_step=.005)
    assert sol.success
    segments.append(sol)
    y = float(sol.y[0, -1])
    endpoints[right] = y


def integrate_piecewise(fun, boundaries):
    return sum(quad(fun, a, b, epsabs=1e-12, epsrel=1e-12)[0]
               for a, b in zip(boundaries[:-1], boundaries[1:]))


ws = []
for power in range(4):
    ws.append(2 ** (power + 1) / (power + 1)
              + integrate_piecewise(lambda x: x ** power * w(x),
                                    list(range(2, 21, 2))))
W0 = ws[0]
W1_identity = 2 * W0 - 1
normalization = 1 / (2 * W1_identity)
trace_sigma = 23 / 3 - 1 / (3 * W1_identity)
v = trace_sigma / 3


def radius_density(r):
    return (normalization * r * (w(r - 1) + w(r + 1))
            if r >= 1 else 0.)


identity_tests = []
for x in [2., 2.1, 2.5, 3., 4., 5., 8., 12., 18.]:
    cuts = sorted({x - 2, x, *[float(j) for j in range(2, 19, 2)
                             if x - 2 < j < x]})
    integral = integrate_piecewise(w, cuts)
    identity_tests.append({"x": x, "left": 2 * (x - 1) * w(x),
                           "right": integral,
                           "residual": 2 * (x - 1) * w(x) - integral})

transform_tests = []
for k in [.1, .7, pi / 2, 2.7, pi, 5.]:
    phi = integrate_piecewise(lambda s:
                               2 * normalization * s * w(s)
                               * np.sinc(k * s / pi),
                               list(range(0, 21, 2)))
    # Keep r+1<=20, before forward-integration cancellation dominates.
    aa = integrate_piecewise(lambda r:
                              radius_density(r) * np.sinc(k * r / pi),
                              list(range(1, 20, 2)))
    bb = integrate_piecewise(lambda r:
                              radius_density(r) * spherical_jn(1, k * r),
                              list(range(1, 20, 2)))
    transform_tests.append({"k": k, "phi": phi,
                            "trace_residual": aa - phi * np.cos(k),
                            "spin_residual": bb - phi * np.sin(k)})

assert max(abs(z["residual"]) for z in identity_tests) < 1e-10
assert max(abs(z["trace_residual"]) for z in transform_tests) < 1e-8
assert max(abs(z["spin_residual"]) for z in transform_tests) < 1e-8

# Probe and preserve the numerical failure instead of interpreting it as
# exact negativity. The analytic positive integral identity excludes it.
numerical_negative_endpoints = {k: value for k, value in endpoints.items()
                                if value < 0}

# Purely a display estimate: the bound is conditional on exact w(20).
# For each n, monotonicity and (21) prove the formula itself analytically.
conditional_tail_estimates = {
    str(n): 2 * 22 ** n * max(w(20), 0.) / (1 - (12 / 11) ** n / 21)
    for n in range(4)
}

s = sqrt(5)
a = (1 + s) / 2
y0 = a + 1
weights = [a / (2 * y0), (a + 2) / (2 * y0)]
radii = [a, a + 2]
relaxation_checks = {
    "radii": radii, "weights": weights,
    "mean": sum(p * r for p, r in zip(weights, radii)),
    "second_moment": sum(p * r * r for p, r in zip(weights, radii)),
    "third_moment_actual": sum(p * r ** 3 for p, r in zip(weights, radii)),
    "third_moment_required_by_positive_full_contract": 15 * y0,
    "maximum_first_32_zero_shell_residual": max(
        abs(sum(p * np.sinc((2 * n + 1) * r / 2)
                for p, r in zip(weights, radii))) for n in range(32)),
}

result = {
    "status": "PASS_NONCERTIFIED_NUMERICAL_DIAGNOSTICS",
    "scope": "Floating-point checks only; not interval-certified values or a replacement for PROOF.md.",
    "candidate_lipschitz_gap": 64 / (9 * pi ** 4),
    "candidate_taylor_gap": 16 / pi ** 3,
    "all_zero_relaxation_gap": (3 * sqrt(5) - 5) / 2,
    "certified_operator_gap": 25507 / 16000,
    "certified_isotropic_lower_bound": 121507 / 48000,
    "delay_kernel": {
        "W0_truncated_20": W0,
        "W1_from_exact_identity_using_numerical_W0": W1_identity,
        "direct_truncated_moments": ws,
        "moment_identity_residuals": [
            ws[1] - (2 * ws[0] - 1),
            ws[2] - (5 * ws[0] - 8 / 3),
            ws[3] - ((46 / 3) * ws[0] - 8)],
        "noise_covariance_trace_estimate": trace_sigma,
        "noise_isotropic_variance_estimate": v,
        "supplied_Dickman_variance": 23 / 9,
        "improvement_estimate": 23 / 9 - v,
        "w_at_even_endpoints": endpoints,
        "preserved_forward_ODE_negative_roundoff": numerical_negative_endpoints,
        "tail_formulas_evaluated_at_uncertified_w20": conditional_tail_estimates,
        "integral_identity_checks": identity_tests,
        "fourier_transform_checks": transform_tests,
    },
    "radius_only_relaxation": relaxation_checks,
}
Path(__file__).with_name("NUMERICAL_CHECKS.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
