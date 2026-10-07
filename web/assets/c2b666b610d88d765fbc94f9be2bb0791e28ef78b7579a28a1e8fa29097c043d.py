#!/usr/bin/env python3
"""Bounded numerical diagnostics for the c09_l04 log-concave pair.

The proof is in INITIAL.txt.  This script checks the explicit analytic
constant bounds and a finite midpoint-grid instance of the positive periodic
hat codec; it does not certify the asymptotic theorem.
"""

import json
import math


A = 1e-3
D = 24
SQRT2 = math.sqrt(2.0)
NORMALIZER = math.sqrt(2.0 * math.pi)


def normal_pdf(x):
    return math.exp(-0.5 * x * x) / NORMALIZER


def normal_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def m2_midpoint(n=40000, radius=8.0):
    step = 2.0 * radius / n
    total = 0.0
    for k in range(n):
        x = -radius + (k + 0.5) * step
        total += math.tanh(x) ** 2 * normal_pdf(x)
    return total * step


def h_terms(x, v, m2_value):
    h = h1 = h2 = 0.0
    for j, vj in enumerate(v, start=1):
        r = A * math.exp(-j) * math.sqrt(m2_value)
        k = 2.0 * math.pi * j
        phase = k * normal_cdf(x)
        co = math.cos(phase)
        si = math.sin(phase)
        h += r * vj * SQRT2 * co
        h1 += r * vj * (-SQRT2 * k * si * normal_pdf(x))
        h2 += r * vj * SQRT2 * (
            -(k * k) * co * normal_pdf(x) ** 2
            + k * x * si * normal_pdf(x)
        )
    return h, h1, h2


def c_log_curvature(x, v, m2_value):
    h, h1, h2 = h_terms(x, v, m2_value)
    return -1.0 + h2 / (1.0 + h) - (h1 / (1.0 + h)) ** 2


def product_log_curvature(x, s, v):
    g = math.tanh(x)
    gp = 1.0 - g * g
    gpp = -2.0 * g * gp
    z = s * v
    den = 1.0 + z * g
    return -1.0 + z * gpp / den - (z * gp / den) ** 2


def shared_density(t, v, m2_value):
    val = 1.0
    for j, vj in enumerate(v, start=1):
        r = A * math.exp(-j) * math.sqrt(m2_value)
        val += SQRT2 * r * vj * math.cos(2.0 * math.pi * j * t)
    return val


def periodic_hat_codec_tv(j_count, v, m2_value, grid_n=32768):
    """Midpoint-grid TV diagnostic for the positive hat/Durrmeyer kernel."""
    masses = [0.0] * j_count
    f_values = []
    hats = []
    for n in range(grid_n):
        t = (n + 0.5) / grid_n
        z = j_count * t
        left = int(z) % j_count
        alpha = z - math.floor(z)
        right = (left + 1) % j_count
        f = shared_density(t, v, m2_value)
        f_values.append(f)
        hats.append((left, right, alpha))
        weight = 1.0 / grid_n
        masses[left] += (1.0 - alpha) * f * weight
        masses[right] += alpha * f * weight

    absolute_error = 0.0
    for f, (left, right, alpha) in zip(f_values, hats):
        out_density = j_count * (
            (1.0 - alpha) * masses[left] + alpha * masses[right]
        )
        absolute_error += abs(out_density - f) / grid_n
    return absolute_error / 2.0


def main():
    # Sum i^4 q^i = q(1+11q+11q^2+q^3)/(1-q)^5, q=e^-2.
    q = math.exp(-2.0)
    s4 = q * (1.0 + 11.0 * q + 11.0 * q * q + q**3) / (1.0 - q) ** 5
    assert s4 < 1.0
    m2 = m2_midpoint()
    assert 0.0 < m2 < 1.0

    # Analytic uniform bounds: e^2>7 gives sum e^-2i<1/6 and s4<1.
    delta_bound = A / math.sqrt(3.0)
    h2_bound = 9.0 * math.sqrt(2.0) * A
    c_curvature_bound = -1.0 + h2_bound / (1.0 - delta_bound)
    tanh_second_bound = 4.0 / (3.0 * math.sqrt(3.0))
    p_curvature_bound = -1.0 + A * tanh_second_bound / (1.0 - A)
    assert c_curvature_bound < -0.98
    assert p_curvature_bound < -0.99

    v = [(-1.0) ** j / math.sqrt(D) for j in range(1, D + 1)]
    c_grid_max = max(
        c_log_curvature(-8.0 + 16.0 * k / 16000.0, v, m2)
        for k in range(16001)
    )
    p_grid_max = max(
        product_log_curvature(-8.0 + 16.0 * k / 16000.0, A * math.exp(-1), 1.0)
        for k in range(16001)
    )

    # M2 is a uniform bound on ||f_v''||_infinity; the kernel proof gives
    # TV <= M2/J^2 for every J>=5.  Midpoint output is numerical evidence only.
    m2_bound = SQRT2 * (2.0 * math.pi) ** 2 * A * math.sqrt(s4)
    codec = []
    for j_count in (8, 16, 32):
        tv = periodic_hat_codec_tv(j_count, v, m2)
        bound = m2_bound / (j_count * j_count)
        assert tv <= bound + 2e-7
        codec.append({"J": j_count, "midpoint_TV": tv, "analytic_TV_bound": bound})

    print(json.dumps({
        "scope": "finite numerical diagnostics; analytic proof is in INITIAL.txt",
        "a": A,
        "dimensions_checked": D,
        "m2_midpoint": m2,
        "sum_i4_exp_minus_2i": s4,
        "uniform_delta_bound": delta_bound,
        "uniform_abs_h_second_bound": h2_bound,
        "C_log_curvature_upper_bound": c_curvature_bound,
        "P_log_curvature_upper_bound": p_curvature_bound,
        "C_grid_log_curvature_max": c_grid_max,
        "P_grid_log_curvature_max_for_v1": p_grid_max,
        "periodic_hat_codec": codec,
        "fisher_gram_identity": "both equal m2 * diag((a*exp(-i))^2) exactly",
    }, indent=2))


if __name__ == "__main__":
    main()
