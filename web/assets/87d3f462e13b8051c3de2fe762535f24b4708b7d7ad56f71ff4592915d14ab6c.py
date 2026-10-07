#!/usr/bin/env python3
"""Finite diagnostics for the uniform-score R1 refinement; see R1.txt."""

import json
import math

A = 1e-3
D = 24
SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
NORM = math.sqrt(2.0 * math.pi)


def phi(x):
    return math.exp(-0.5 * x * x) / NORM


def Phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def h_terms(x, v):
    h = h1 = h2 = 0.0
    for i, vi in enumerate(v, start=1):
        r = A * math.exp(-i) / SQRT3
        k = 2.0 * math.pi * i
        phase = k * Phi(x)
        co, si = math.cos(phase), math.sin(phase)
        h += r * vi * SQRT2 * co
        h1 += r * vi * (-SQRT2 * k * si * phi(x))
        h2 += r * vi * SQRT2 * (
            -k * k * co * phi(x) ** 2 + k * x * si * phi(x)
        )
    return h, h1, h2


def c_curvature(x, v):
    h, h1, h2 = h_terms(x, v)
    return -1.0 + h2 / (1.0 + h) - (h1 / (1.0 + h)) ** 2


def p_curvature(x, s, v):
    g = 2.0 * Phi(x) - 1.0
    gp = 2.0 * phi(x)
    gpp = -2.0 * x * phi(x)
    z = s * v
    den = 1.0 + z * g
    return -1.0 + z * gpp / den - (z * gp / den) ** 2


def f_density(t, v):
    val = 1.0
    for i, vi in enumerate(v, start=1):
        r = A * math.exp(-i) / SQRT3
        val += SQRT2 * r * vi * math.cos(2.0 * math.pi * i * t)
    return val


def codec_tv(j_count, v, n=32768):
    masses = [0.0] * j_count
    values = []
    labels = []
    for k in range(n):
        t = (k + 0.5) / n
        z = j_count * t
        left = int(z) % j_count
        alpha = z - math.floor(z)
        right = (left + 1) % j_count
        val = f_density(t, v)
        values.append(val)
        labels.append((left, right, alpha))
        masses[left] += (1.0 - alpha) * val / n
        masses[right] += alpha * val / n
    l1 = 0.0
    for val, (left, right, alpha) in zip(values, labels):
        decoded = j_count * ((1.0 - alpha) * masses[left] + alpha * masses[right])
        l1 += abs(decoded - val) / n
    return l1 / 2.0


def main():
    q = math.exp(-2.0)
    s2 = q / (1.0 - q)
    s4 = q * (1 + 11*q + 11*q*q + q**3) / (1.0-q)**5
    assert s2 < 1.0 / 6.0
    assert s4 < 1.0

    delta_bound = A / 3.0
    h2_bound = 3.0 * math.sqrt(6.0) * A
    c_bound = -1.0 + h2_bound / (1.0 - delta_bound)
    g2_bound = 2.0 / math.sqrt(2.0 * math.pi * math.e)
    p_bound = -1.0 + A * g2_bound / (1.0 - A)
    assert c_bound < -0.99
    assert p_bound < -0.999

    v = [(-1.0) ** i / math.sqrt(D) for i in range(1, D + 1)]
    c_grid = max(c_curvature(-8 + 16*k/16000, v) for k in range(16001))
    p_grid = max(p_curvature(-8 + 16*k/16000, A*math.exp(-1), 1.0)
                 for k in range(16001))

    m2_bound = SQRT2 * (2.0 * math.pi) ** 2 * A / SQRT3
    codec = []
    for j in (8, 16, 32):
        tv = codec_tv(j, v)
        bound = m2_bound / (j*j)
        assert tv <= bound + 2e-7
        codec.append({"J": j, "midpoint_TV": tv, "analytic_TV_bound": bound})

    print(json.dumps({
        "scope": "finite numerical diagnostics only; R1.txt contains the proof",
        "a": A,
        "dimension": D,
        "sum_exp_minus_2i": s2,
        "sum_i4_exp_minus_2i": s4,
        "delta_bound": delta_bound,
        "h_second_bound": h2_bound,
        "P_curvature_upper_bound": p_bound,
        "C_curvature_upper_bound": c_bound,
        "P_grid_curvature_max": p_grid,
        "C_grid_curvature_max": c_grid,
        "M2_upper_bound": m2_bound,
        "codec": codec,
        "P_score_law": "2*Phi(Z)-1 is exactly Uniform[-1,1]",
        "Fisher_gram": "both are diag(s_i^2/3) exactly",
    }, indent=2))


if __name__ == "__main__":
    main()
