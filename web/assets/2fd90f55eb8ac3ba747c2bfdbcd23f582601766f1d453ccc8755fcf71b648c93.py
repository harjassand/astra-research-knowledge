#!/usr/bin/env python3
"""Scoped finite algebra for the ground-energy candidate; no limit oracle."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import math
import random
import numpy as np

HERE = Path(__file__).resolve().parent


def occupation(x, i):
    return (x >> i) & 1


def edges(s):
    out = []
    for x in range(1 << s):
        for i in range(s - 1):
            if occupation(x, i) and not occupation(x, i + 1):
                out.append((x, x ^ (3 << i), i))
    return out


def kinetic(v, s):
    return 2 * sum((v[x] - v[y]) ** 2 for x, y, _ in edges(s)) + 2 * sum(
        (occupation(x, 0) + occupation(x, s - 1)) * v[x] ** 2
        for x in range(1 << s)
    )


def project(v, s, u):
    mask = sum(1 << i for i in u)
    groups = {}
    for x in range(1 << s):
        key = (x & ~mask, (x & mask).bit_count())
        groups.setdefault(key, []).append(x)
    p = [F(0)] * len(v)
    for xs in groups.values():
        val = sum(v[x] for x in xs) / len(xs)
        for x in xs:
            p[x] = val
    return p


def swap(x, i, j):
    return x ^ ((1 << i) | (1 << j)) if occupation(x, i) != occupation(x, j) else x


def swap_form(v, i, j):
    return sum(v[x] * (v[x] - v[swap(x, i, j)]) for x in range(len(v)))


def forward(x, s, a):
    # Cells start at physical i=0,...,S. Array bits encode physical1,...,S;
    # the first window therefore starts at bit index -1, a zero ghost.
    return [F(sum(occupation(x, j) for j in range(max(i, 0), min(i + a, s))), a)
            for i in range(-1, s)]


counts = {
    "one_block_compression": 0,
    "two_block_hypergeometric": 0,
    "complete_graph_form_fixtures": 0,
    "moving_particle_form_fixtures": 0,
    "ground_quotient_configurations": 0,
    "ground_form_identities": 0,
    "IMS_identities": 0,
    "forward_hop_L1": 0,
    "softmax_entropy": 0,
    "weak_law_raw_L1_controls": 0,
    "continuum_diagnostic": 0,
}
max_residual = 0.0

# Exact block compression on arbitrary rational vectors, including outside sites.
for s in range(2, 9):
    v = [F(((x * 13 + s * 7) % 23) - 9, 7) for x in range(1 << s)]
    for ell in range(2, s + 1):
        for start in range(s - ell + 1):
            u = tuple(range(start, start + ell))
            p = project(v, s, u)
            left = sum(p[x] ** 2 * occupation(x, start) * occupation(x, start + 1)
                       for x in range(1 << s))
            right = sum(p[x] ** 2 * F(k * (k - 1), ell * (ell - 1))
                        for x in range(1 << s)
                        for k in [sum(occupation(x, i) for i in u)])
            assert left == right
            qnorm = sum((v[x] - p[x]) ** 2 for x in range(1 << s))
            complete = sum(swap_form(v, i, j) for i, j in combinations(u, 2))
            assert complete >= ell * qnorm
            counts["one_block_compression"] += 1
            counts["complete_graph_form_fixtures"] += 1
    for i, j in combinations(range(s), 2):
        lhs = swap_form(v, i, j)
        rhs = 4 * (j - i) * sum(swap_form(v, k, k + 1) for k in range(i, j))
        assert lhs <= rhs
        counts["moving_particle_form_fixtures"] += 1

# Hypergeometric identity for all total counts in two equal-sized blocks.
for ell in range(1, 9):
    for k in range(2 * ell + 1):
        total = math.comb(2 * ell, k)
        variance = sum(F(math.comb(ell, h) * math.comb(ell, k - h), total)
                       * F((2 * h - k) ** 2, ell ** 2)
                       for h in range(max(0, k - ell), min(ell, k) + 1))
        p = F(k, 2 * ell)
        assert variance == 4 * p * (1 - p) / (2 * ell - 1)
        assert variance <= F(1, 2 * ell - 1)
        counts["two_block_hypergeometric"] += 1

# Exact positive ground quotient and form identity for J=1, all number sectors.
for s in range(1, 9):
    z = [F(3 * i + 5, i + 3) for i in range(s)]
    f = [math.prod(z[i] for i in range(s) if occupation(x, i))
         for x in range(1 << s)]
    v = [F((x * 7 + 3) % 19 + 1, 11) for x in range(1 << s)]
    adj = [[] for _ in f]
    for x, y, _ in edges(s):
        adj[x].append(y)
        adj[y].append(x)
    quotient = []
    for x in range(1 << s):
        b = occupation(x, 0) + occupation(x, s - 1)
        graph = 2 * sum(1 - f[y] / f[x] for y in adj[x]) + 2 * b
        local = 2 * b
        for i in range(s - 1):
            ni, nj = occupation(x, i), occupation(x, i + 1)
            local += 2 * (ni * (1 - nj) * (1 - z[i + 1] / z[i])
                          + nj * (1 - ni) * (1 - z[i] / z[i + 1]))
        assert graph == local
        quotient.append(local)
        counts["ground_quotient_configurations"] += 1
    potential = sum(v[x] ** 2 * quotient[x] for x in range(1 << s))
    residual = 2 * sum(f[x] * f[y] * (v[x] / f[x] - v[y] / f[y]) ** 2
                       for x, y, _ in edges(s))
    assert kinetic(v, s) == potential + residual
    assert residual >= 0
    counts["ground_form_identities"] += 1

    # A rational stereographic two-component diagonal partition of unity.
    a = max(1, s // 2)
    t = [sum(r ** 2 for r in forward(x, s, a)) / (s + 1) for x in range(1 << s)]
    c0 = [(1 - q ** 2) / (1 + q ** 2) for q in t]
    c1 = [2 * q / (1 + q ** 2) for q in t]
    assert all(c0[x] ** 2 + c1[x] ** 2 == 1 for x in range(1 << s))
    u0, u1 = ([v[x] * c[x] for x in range(1 << s)] for c in (c0, c1))
    defect = 2 * sum(v[x] * v[y] * ((c0[x] - c0[y]) ** 2
                                    + (c1[x] - c1[y]) ** 2)
                     for x, y, _ in edges(s))
    assert kinetic(u0, s) + kinetic(u1, s) == kinetic(v, s) + defect
    assert defect >= 0
    counts["IMS_identities"] += 1

    for a in range(1, s + 1):
        for x, y, _ in edges(s):
            rx, ry = forward(x, s, a), forward(y, s, a)
            changed = sum(rx[i] != ry[i] for i in range(s + 1))
            l1 = sum(abs(rx[i] - ry[i]) for i in range(s + 1)) / (s + 1)
            assert changed <= 2
            assert l1 <= F(2, a * (s + 1))
            counts["forward_hop_L1"] += 1

rng = random.Random(29417)
for k in (1, 2, 3, 7, 19):
    for m in (0.1, 1.0, 7.0, 30.0):
        for _ in range(25):
            values = [rng.uniform(-9, 12) for _ in range(k)]
            top = max(values)
            q = [math.exp(m * (v - top)) for v in values]
            p = [z / sum(q) for z in q]
            mean = sum(z * v for z, v in zip(p, values))
            assert mean + math.log(k) / m >= top - 2e-12
            counts["softmax_entropy"] += 1

# Weak empirical convergence does not imply raw step-density L1 convergence.
for p in (F(1, 4), F(1, 2), F(3, 4)):
    exact_expected_l1 = p * (1 - p) + (1 - p) * p
    assert exact_expected_l1 == 2 * p * (1 - p) > 0
    for l in (10, 100, 1000):
        empirical_variance = p * (1 - p) / l
        assert empirical_variance < exact_expected_l1
        counts["weak_law_raw_L1_controls"] += 1

# Finite continuum diagnostics for product recovery and positive test fields.
grid = np.linspace(0.0, 1.0, 40001)
diagnostics = []
for amp in (0.8, 1.9, 2.9):
    theta = amp * np.sin(math.pi * grid)
    rho = np.sin(theta / 2) ** 2
    for kappa, lam in ((0.0, 0.0), (7.0, 12.0), (13.0, -3.0)):
        target = amp ** 2 * math.pi ** 2 / 4 - kappa * np.trapezoid(rho ** 2, grid) - lam * np.trapezoid(rho, grid)
        errs = []
        for l in (32, 64, 128, 256, 512, 1024):
            th = amp * np.sin(math.pi * np.arange(l + 1) / l)
            pr = np.sin(th[1:l] / 2) ** 2
            d = l * np.sum(1 - np.cos(np.diff(th)))
            energy = d - kappa * np.sum(pr[:-1] * pr[1:]) / l - lam * np.sum(pr) / l
            errs.append(abs(float(energy) - target))
            counts["continuum_diagnostic"] += 1
        assert errs[-1] < 2e-4
        diagnostics.append({"amplitude": amp, "kappa": kappa, "lambda": lam,
                            "L": [32, 64, 128, 256, 512, 1024], "errors": errs})
    ph = np.sin(2 * math.pi * grid)
    php = 2 * math.pi * np.cos(2 * math.pi * grid)
    dual = 2 * (-np.trapezoid(rho * php, grid) - np.trapezoid(rho * (1 - rho) * ph ** 2, grid))
    target_kinetic = amp ** 2 * math.pi ** 2 / 4
    assert dual <= target_kinetic + 1e-10
    dual_errs = []
    for l in (32, 64, 128, 256, 512, 1024):
        x = np.arange(1, l) / l
        pr = np.sin(amp * np.sin(math.pi * x) / 2) ** 2
        h = (1 - np.cos(2 * math.pi * x)) / (2 * math.pi)
        dh = np.diff(h)
        q = 2 * np.sum(pr[:-1] * (1 - pr[1:]) * (-np.expm1(dh))
                       + pr[1:] * (1 - pr[:-1]) * (-np.expm1(-dh)))
        q += 2 * (pr[0] + pr[-1])
        dual_errs.append(abs(float(l * q) - dual))
        counts["continuum_diagnostic"] += 1
    assert dual_errs[-1] < 0.09
    diagnostics.append({"amplitude": amp, "test_field": "sin(2pi x)",
                        "dual": float(dual), "kinetic": target_kinetic,
                        "errors": dual_errs})

result = {"status": "PASS", "date": "2026-10-08", "J": 1,
          "counts": counts, "largest_Hilbert_dimension": 256,
          "exact_tests": "Fraction arithmetic; all asserted identities exactly equal",
          "numerical_tests": "NumPy continuum diagnostics and stable softmax inequality",
          "numpy_version": np.__version__, "diagnostics": diagnostics,
          "limits_not_tested": ["all-size static replacement", "random-profile Fisher liminf",
                                "ground-energy asymptotic theorem", "external validation", "novelty"]}
(HERE / "CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "counts": counts,
                  "largest_Hilbert_dimension": result["largest_Hilbert_dimension"]}, indent=2))
