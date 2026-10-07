"""Scoped numerical diagnostics for the analytic scout derivations.

These verify normalization/orientation and expected scaling for specified codes.
They do not prove asymptotic optimality or historical novelty.
"""
import json
import math
from pathlib import Path

import numpy as np


def density(theta, x, beta):
    theta = np.asarray(theta)
    x = np.asarray(x)
    distance = np.maximum(theta - x, 0.0)
    if beta == 0:
        power = (x <= theta).astype(float)
    else:
        power = distance ** beta
    return (beta + 1) * power / theta ** (beta + 1) * (x >= 0)


nodes, weights = np.polynomial.legendre.leggauss(256)


def quad(fn, lo, hi):
    if hi <= lo:
        return 0.0
    return float((hi - lo) / 2 * np.dot(weights, fn((lo + hi) / 2 + (hi - lo) / 2 * nodes)))


def predictive(x, beta):
    return 0.5 * quad(lambda theta: density(theta, x, beta), max(1.0, x), 2.0) + 0.5 * float(density(2.0, x, beta))


def posterior(theta, x, beta):
    if x >= 2:
        return 2.0 * (np.asarray(theta) == 2.0)
    return density(theta, max(0.0, x), beta) / predictive(max(0.0, x), beta)


def hinge_regret(x, y, h, beta):
    threshold = 2 ** (-(2 * beta + 2)) * h ** beta

    def divergence(theta):
        u = posterior(theta, x, beta)
        v = posterior(theta, y, beta)
        return np.maximum(u - threshold, 0) - np.maximum(v - threshold, 0) - (v > threshold) * (u - v)

    points = sorted(set([1.0, 2.0] + [value for value in (x, y) if 1 < value < 2]))
    regret = 0.5 * sum(quad(divergence, lo, hi) for lo, hi in zip(points[:-1], points[1:])) + 0.5 * float(divergence(2.0))
    required = threshold * h / 8
    return {"beta": beta, "h": h, "direction": "up" if y > x else "down", "regret": regret, "analytic_strip_lower": required, "ratio": regret / required}


def hats_error(theta, beta, n):
    # The same regular trapezoidal rule computes hat masses and reconstructed TV.
    x = np.linspace(0, 2, 64 * n + 1)
    dx = x[1] - x[0]
    quadrature_weights = np.full_like(x, dx)
    quadrature_weights[[0, -1]] *= 0.5
    h = 2 / n
    left = np.minimum((x / h).astype(int), n - 1)
    frac = (x - left * h) / h
    q = density(theta, x, beta)
    encoded = np.bincount(left, weights=(1 - frac) * q * quadrature_weights, minlength=n + 1)
    encoded += np.bincount(left + 1, weights=frac * q * quadrature_weights, minlength=n + 1)
    hat_masses = np.full(n + 1, h)
    hat_masses[[0, -1]] /= 2
    coefficients = encoded / hat_masses
    decoded = coefficients[left] * (1 - frac) + coefficients[left + 1] * frac
    return {"N": n, "D": n + 1, "tv": float(0.5 * np.dot(np.abs(decoded - q), quadrature_weights)), "source_mass": float(np.dot(q, quadrature_weights)), "decoded_mass": float(np.dot(decoded, quadrature_weights))}


result = {"status": "NUMERICAL_DIAGNOSTICS_ONLY", "hinge_regrets": [], "hat_codes": {}}
for beta in (0.0, 0.25, 0.75, 1.0, 2.0):
    for h in (0.125, 0.0625, 0.03125):
        for direction in (-1, 1):
            result["hinge_regrets"].append(hinge_regret(1.5, 1.5 + direction * h, h, beta))
    rows = [hats_error(1.421, beta, n) for n in (16, 32, 64, 128, 256)]
    for before, after in zip(rows[:-1], rows[1:]):
        after["observed_doubling_exponent"] = math.log(before["tv"] / after["tv"], 2)
    result["hat_codes"][str(beta)] = rows

assert min(row["ratio"] for row in result["hinge_regrets"]) > 1
assert max(abs(row["source_mass"] - row["decoded_mass"]) for rows in result["hat_codes"].values() for row in rows) < 1e-10
target = Path(__file__).with_name("statistical_geometry_checks.json")
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "minimum_hinge_ratio": min(row["ratio"] for row in result["hinge_regrets"]), "last_doubling_exponents": {beta: rows[-1]["observed_doubling_exponent"] for beta, rows in result["hat_codes"].items()}, "saved": str(target)}, indent=2))
