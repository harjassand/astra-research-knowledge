#!/usr/bin/env python3
"""Finite diagnostics for the two root derivations; no experimental evidence."""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import platform
import sys
import numpy as np


def g(x):
    if x < -1e-10:
        raise ValueError(x)
    if x <= 0:
        return 0.0
    return math.log1p(x) + x * math.log1p(1.0 / x)


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def main():
    exact_checks = 0
    hadamard = [[F(x, 2) for x in row] for row in
                [[1, 1, 1, 1], [1, -1, 1, -1],
                 [1, 1, -1, -1], [1, -1, -1, 1]]]
    for r in (1, 2, 3):
        p = [[sum(hadamard[i][l] * hadamard[j][l] for l in range(r))
              for j in range(4)] for i in range(4)]
        assert mm(p, p) == p
        assert all(p[i][i] == F(r, 4) for i in range(4))
        for n in (F(1), F(100)):
            for nu in (F(0), F(1, 10), n / 2):
                b = (4 * n - r * nu) / (4 - r)
                cov = [[nu * p[i][j] + b * (F(i == j) - p[i][j])
                        for j in range(4)] for i in range(4)]
                assert all(cov[i][i] == n for i in range(4))
                assert mm(mm(p, cov), p) == [[nu * x for x in row] for row in p]
                exact_checks += 1

    rng = np.random.default_rng(7122026)
    feasible_checks = 0
    max_excess = -math.inf
    for k, r in ((2, 1), (4, 1), (4, 2), (8, 3)):
        v = np.exp(2j * np.pi * np.outer(np.arange(k), np.arange(k)) / k) / np.sqrt(k)
        p = v[:, :r] @ v[:, :r].conj().T
        for n in (1.0, 100.0, 1000.0):
            for nu in (0.1, n / 2):
                b = (k * n - r * nu) / (k - r)
                bound = r * g(nu) + (k - r) * g(b)
                base_nu = nu / 2
                base_b = (k * n - r * base_nu) / (k - r)
                base = base_nu * p + base_b * (np.eye(k) - p)
                for _ in range(10):
                    phase = np.exp(1j * rng.uniform(-np.pi, np.pi, k))
                    rotated = phase[:, None] * base * phase.conj()[None, :]
                    mix = nu / (4 * base_b)
                    cov = (1 - mix) * base + mix * rotated
                    assert np.max(np.abs(np.diag(cov) - n)) < 1e-8
                    ev = np.linalg.eigvalsh(cov)
                    assert min(ev) >= -1e-8
                    selected = v[:, :r].conj().T @ cov @ v[:, :r]
                    assert max(np.linalg.eigvalsh(selected)) <= nu + 1e-8
                    excess = sum(g(float(x)) for x in ev) - bound
                    assert excess < 1e-8
                    max_excess = max(max_excess, excess)
                    feasible_checks += 1

    hidden_checks = 0
    for m in (1, 2, 3, 7, 32, 127):
        for gamma in (F(1), F(1, 1000000)):
            for eps in (F(1, 100), F(1, 5)):
                for hidden in (None, 0, m - 1):
                    w = [gamma / m] * m
                    if hidden is not None:
                        w[hidden] += 2 * eps * gamma
                    capacity = sum(w) / 2
                    expected = gamma / 2 if hidden is None else (1 + 2 * eps) * gamma / 2
                    assert capacity == expected
                    for i, wi in enumerate(w):
                        ui = F(i % 3, 2)
                        energy = wi * (ui * ui + (1 - ui) ** 2)
                        assert energy - wi / 2 == 2 * wi * (ui - F(1, 2)) ** 2
                    hidden_checks += 1

    examples = []
    for k in (2, 4, 8, 64):
        n, r, nu = 100.0, 1, 0.1
        b = (k * n - r * nu) / (k - r)
        w_bal = k * g(n) - r * g(nu) - (k-r) * g(b)
        w_cold = r * (g(n)-g(nu)+(nu-n)*math.log1p(1/n))
        excess_work = (k-r)*((b-n)*math.log1p(1/n)+g(n)-g(b))
        assert excess_work >= 0
        assert abs(w_bal-w_cold-excess_work) < 1e-10
        examples.append({"ports": k, "protected_modes": r, "local_occupation": n,
                         "selected_occupation": nu,
                         "free_energy_over_kBT": w_bal,
                         "direct_cooling_work_over_kBT": w_cold,
                         "balanced_extra_work_over_kBT": excess_work,
                         "with_one_percent_warm_loss": .99 * nu + .01 * n})
    result = {"status": "FINITE_DIAGNOSTICS_PASS", "python": sys.version,
              "numpy": np.__version__, "platform": platform.platform(),
              "exact_thermal_cases": exact_checks,
              "feasible_entropy_cases": feasible_checks,
              "maximum_entropy_excess": max_excess,
              "exact_hidden_channel_cases": hidden_checks,
              "examples": examples,
              "scope": "Exact rational identities plus floating finite covariance cases; no novelty or physical validation."}
    dest = Path(__file__).with_name("results.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
