#!/usr/bin/env python3
"""Numerical algebra checks for the ordinary common-activity comparator.

This checks three independent representations of the limiting scalar law,
finite-N *clock-only* Feynman--Kac matrices, and an exact augmented finite
SSEP generator identity. It is not an acquired experiment, a finite-N
certificate for unknown native kinetics, or a numerical proof of the LDP.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigvals, expm
from scipy.optimize import minimize_scalar


def top_eigen(h, g0, g1, r, ell):
    q = np.array([[-r, r], [ell, -ell]], dtype=float)
    return float(np.max(eigvals(q + h * np.diag([g0, g1])).real))


def closed_eigen(h, g0, g1, r, ell):
    return 0.5 * (
        h * (g0 + g1) - r - ell
        + np.sqrt((h * (g0 - g1) - r + ell) ** 2 + 4 * r * ell)
    )


def occupation_cost(x, r, ell):
    return (np.sqrt(r * (1 - x)) - np.sqrt(ell * x)) ** 2


def circulation_rate(q, v, horizon, g0, g1, r, ell):
    def objective(x):
        speed = g0 + (g1 - g0) * x
        return q * q / (2 * v * horizon * speed) + horizon * occupation_cost(x, r, ell)

    fit = minimize_scalar(objective, bounds=(0, 1), method="bounded",
                          options={"xatol": 1e-13})
    candidates = [(objective(0), 0.0), (objective(1), 1.0), (fit.fun, fit.x)]
    value, occupancy = min(candidates)
    return float(value), float(occupancy)


def check_scalar_duality():
    rows = []
    largest_eigen_error = 0.0
    largest_dual_error = 0.0
    for g0, g1, r, ell in [(0.25, 1.75, 1, 1), (0.4, 1.9, 2, 3)]:
        v, horizon = 0.8, 1.3
        mean_speed = (ell * g0 + r * g1) / (r + ell)
        for lam in [-3.0, -0.7, 0.0, 0.4, 2.0]:
            h = v * lam * lam / 2
            largest_eigen_error = max(largest_eigen_error,
                                     abs(top_eigen(h, g0, g1, r, ell)
                                         - closed_eigen(h, g0, g1, r, ell)))
        for q in [0.0, 0.3, 1.0, 2.0, 5.0]:
            rate, occupancy = circulation_rate(q, v, horizon, g0, g1, r, ell)
            fit = minimize_scalar(
                lambda lam: horizon * closed_eigen(v * lam * lam / 2, g0, g1, r, ell) - lam * q,
                bounds=(-40, 40), method="bounded", options={"xatol": 1e-12})
            dual = -float(fit.fun)
            largest_dual_error = max(largest_dual_error, abs(rate - dual))
            deterministic_rate = q * q / (2 * v * horizon * mean_speed)
            assert rate <= deterministic_rate + 1e-10
            rows.append(dict(g0=g0, g1=g1, r=r, ell=ell, v=v, horizon=horizon,
                             circulation=q, random_gate_rate=rate,
                             deterministic_mean_rate=deterministic_rate,
                             minimizing_fast_occupation=occupancy))
    assert largest_eigen_error < 1e-12
    assert largest_dual_error < 1e-8
    return dict(largest_eigen_error=largest_eigen_error,
                largest_duality_error=largest_dual_error, rates=rows)


def finite_clock_mgf():
    g0, g1, r, ell, h, horizon = 0.25, 1.75, 1.0, 1.0, 1.4, 1.2
    matrix = np.array([[-r, r], [ell, -ell]]) + h * np.diag([g0, g1])
    top = closed_eigen(h, g0, g1, r, ell)
    rows = []
    for n in [4, 16, 64, 256, 1024]:
        # Subtract the exact leading eigenvalue to avoid artificial overflow.
        scaled = expm(n * horizon * (matrix - top * np.eye(2))) @ np.ones(2)
        values = top * horizon + np.log(scaled) / n
        rows.append(dict(n=n, initial_0=float(values[0]), initial_1=float(values[1]),
                         asymptotic=top * horizon))
    return rows


def tilted_ssep(n, particles, c, lam):
    masks = [sum(1 << i for i in sites) for sites in itertools.combinations(range(n), particles)]
    position = {mask: j for j, mask in enumerate(masks)}
    matrix = np.zeros((len(masks), len(masks)))
    for row, mask in enumerate(masks):
        for i in range(n):
            j = (i + 1) % n
            delta = ((mask >> i) & 1) - ((mask >> j) & 1)
            if delta:
                target = mask ^ (1 << i) ^ (1 << j)
                matrix[row, position[target]] += c * np.exp(lam * delta / n)
                matrix[row, row] -= c
    return matrix


def augmented_generator_identity():
    rows = []
    for n, particles in [(4, 2), (6, 3)]:
        native = tilted_ssep(n, particles, c=0.5, lam=1.1)
        native_top = float(np.max(eigvals(native).real))
        q = np.array([[-1.3, 1.3], [0.7, -0.7]])
        speeds = np.diag([0.4, 1.6])
        augmented = n * n * np.kron(speeds, native) + n * np.kron(q, np.eye(len(native)))
        full = float(np.max(eigvals(augmented).real)) / n
        reduced = float(np.max(eigvals(q + n * native_top * speeds).real))
        error = abs(full - reduced)
        assert error < 1e-10
        rows.append(dict(n=n, particles=particles, dimension=len(augmented),
                         full_augmented_eigenvalue_per_n=full,
                         exact_reduced_eigenvalue=reduced, error=error))
    return rows


def correlation_comparison():
    b, d, v1, v2, horizon = 1.0, 0.75, 0.8, 0.6, 1.3
    k = lambda h: h - b + np.sqrt(b * b + d * d * h * h)
    rows = []
    for lam1, lam2 in [(0.4, 0.7), (1, 1), (2, -1.3)]:
        h1, h2 = v1 * lam1 * lam1 / 2, v2 * lam2 * lam2 / 2
        shared = horizon * k(h1 + h2)
        independent = horizon * (k(h1) + k(h2))
        assert shared > independent
        rows.append(dict(lambda1=lam1, lambda2=lam2,
                         shared_log_mgf_rate=shared, independent_log_mgf_rate=independent))
    return dict(mixed_fourth_derivative_shared=horizon * d * d * v1 * v2 / b,
                mixed_fourth_derivative_independent=0.0, cases=rows)


def main():
    result = {
        "scope": "Population algebra and design calculations only. No physical trials, finite-N unknown-kinetic certificate, or proof by fixture.",
        "scalar_duality": check_scalar_duality(),
        "finite_clock_only_mgf": finite_clock_mgf(),
        "finite_augmented_ssep_generator_identity": augmented_generator_identity(),
        "matched_marginal_gate_correlations": correlation_comparison(),
    }
    output = Path(__file__).with_name("ACTIVITY_CLOCK_CHECKS.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
