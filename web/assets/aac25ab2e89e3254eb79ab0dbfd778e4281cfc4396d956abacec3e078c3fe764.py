#!/usr/bin/env python3
"""Exact finite Ising checks and numerical SK spectral checks.

The exact checks use couplings (log 2)/2 times integers, giving rational
Gibbs laws and heat-bath rates. They do not test the thermodynamic theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import itertools
import json
import math
import time
import numpy as np


def matvec(q, f):
    return [sum(a * b for a, b in zip(row, f)) for row in q]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def exact_model(n, field_site=None, field_power=0):
    spins = list(itertools.product((-1, 1), repeat=n))
    lookup = {s: i for i, s in enumerate(spins)}
    coupling = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            coupling[i][j] = coupling[j][i] = ((i + 2) * (j + 3) % 5) - 2
    energy = [sum(coupling[i][j] * s[i] * s[j]
                  for i in range(n) for j in range(i + 1, n))
              + (field_power * s[field_site] if field_site is not None else 0)
              for s in spins]
    # All energies have a common parity, so relative Gibbs weights are rational.
    base = min(energy)
    assert all((e - base) % 2 == 0 for e in energy)
    weights = [F(2) ** ((e - base) // 2) for e in energy]
    normalizer = sum(weights)
    pi = [w / normalizer for w in weights]
    q = [[F(0) for _ in spins] for _ in spins]
    for a, s in enumerate(spins):
        for i in range(n):
            molecular_power = sum(coupling[i][j] * s[j] for j in range(n))
            if field_site == i:
                molecular_power += field_power
            flip_rate = 1 / (1 + F(2) ** (s[i] * molecular_power))
            target = list(s)
            target[i] *= -1
            b = lookup[tuple(target)]
            q[a][b] += flip_rate
            q[a][a] -= flip_rate
    return spins, pi, q, coupling


def exact_checks():
    assertions = 0
    cases = []
    for n in (2, 3, 4, 5):
        spins, pi, q, coupling = exact_model(n)
        assert all(sum(row) == 0 for row in q)
        assertions += len(q)
        for b in range(len(spins)):
            assert sum(pi[a] * q[a][b] for a in range(len(spins))) == 0
            assertions += 1
        for i in range(n):
            fi = [F(s[i]) for s in spins]
            assert dot(pi, fi) == 0
            assertions += 1
            # Local-field derivative of the generator, with field in exponent units.
            dq = [[F(0) for _ in spins] for _ in spins]
            lookup = {s: a for a, s in enumerate(spins)}
            for a, s in enumerate(spins):
                power = sum(coupling[i][j] * s[j] for j in range(n))
                p = 1 / (1 + F(2) ** (s[i] * power))
                target = list(s)
                target[i] *= -1
                b = lookup[tuple(target)]
                rate_derivative = -2 * s[i] * p * (1 - p)
                dq[a][b] = rate_derivative
                dq[a][a] = -rate_derivative
            for b in range(len(spins)):
                lhs = sum(pi[a] * dq[a][b] for a in range(len(spins)))
                rhs = -sum(pi[a] * fi[a] * q[a][b] for a in range(len(spins)))
                assert lhs == rhs
                assertions += 1
            for field_power in (-4, -1, 1, 3, 6):
                _, pi_h, q_h, _ = exact_model(n, i, field_power)
                th = (F(2) ** field_power - 1) / (F(2) ** field_power + 1)
                assert all(pi_h[a] == pi[a] * (1 + th * fi[a])
                           for a in range(len(spins)))
                assertions += len(spins)
                for b in range(len(spins)):
                    assert sum(pi_h[a] * q_h[a][b] for a in range(len(spins))) == 0
                    assertions += 1
                v = fi
                for order in range(6):
                    assert dot(pi_h, v) == th * dot(pi, [x * y for x, y in zip(fi, v)])
                    assertions += 1
                    v = matvec(q, v)
                alpha = (1 + F(2) ** (-abs(field_power))) / 2
                assert F(1, 2) <= alpha <= 1
                assertions += 1
        cases.append({"n": n, "states": 2 ** n, "coupling_integer_matrix": coupling})
    return {"assertions": assertions, "cases": cases,
            "scope": "Exact finite checks of tilt, stationarity, FDT generator identity, and semigroup derivatives through order 5. No large-n source theorem test."}


def numeric_sk_checks():
    rng = np.random.default_rng(227229)
    cases = []
    for law in ("Gaussian", "Rademacher"):
        for n in (4, 6, 8):
            s = np.array(list(itertools.product((-1., 1.), repeat=n)))
            j = np.zeros((n, n))
            upper = np.triu_indices(n, 1)
            j[upper] = rng.normal(size=len(upper[0])) if law == "Gaussian" else rng.choice((-1., 1.), size=len(upper[0]))
            j += j.T
            w = j / math.sqrt(n)
            energy = 0.5 * np.einsum("ai,ij,aj->a", s, w, s)
            pi = np.exp(energy - energy.max())
            pi /= pi.sum()
            q = np.zeros((len(s), len(s)))
            lookup = {tuple(x): a for a, x in enumerate(s)}
            molecular = s @ w
            for a, x in enumerate(s):
                for i in range(n):
                    target = x.copy()
                    target[i] *= -1
                    b = lookup[tuple(target)]
                    rate = (1 - x[i] * math.tanh(molecular[a, i])) / 2
                    q[a, b] += rate
                    q[a, a] -= rate
            root = np.sqrt(pi)
            h = -root[:, None] * q / root[None, :]
            symmetry_error = np.max(np.abs(h - h.T))
            eigenvalue, eigenvector = np.linalg.eigh(h)
            assert symmetry_error < 2e-13
            assert eigenvalue.min() > -2e-13
            eigenvalue = np.maximum(eigenvalue, 0)
            transformed_spins = root[:, None] * s
            coefficients = eigenvector.T @ transformed_spins
            weight = np.sum(coefficients ** 2, axis=1) / n
            assert abs(weight.sum() - 1) < 2e-13
            max_error = 0.
            for time_value in (0., 0.2, 1., 3., 8.):
                decay = np.exp(-time_value * eigenvalue)
                correlation = float(weight @ decay)
                p_spins = (eigenvector @ (decay[:, None] * coefficients)) / root[:, None]
                for local_field in (-2., -.3, .7, 3.):
                    th = math.tanh(local_field)
                    remanence = sum(np.dot(pi * (1 + th * s[:, i]), p_spins[:, i])
                                   for i in range(n)) / n
                    max_error = max(max_error, abs(remanence - th * correlation))
                assert correlation >= -1e-13
                # All signs of complete monotonicity from the spectral representation.
                for order in range(1, 7):
                    signed_derivative = weight @ (eigenvalue ** order * decay)
                    assert signed_derivative >= -1e-13
            assert max_error < 2e-12
            cases.append({"law": law, "n": n, "states": len(s),
                          "symmetry_error": float(symmetry_error),
                          "max_remanence_identity_error": float(max_error),
                          "weight_sum": float(weight.sum())})
    return {"cases": cases,
            "scope": "Finite SK spectral sanity checks. No extrapolation of critical asymptotics or release correctness."}


if __name__ == "__main__":
    start = time.perf_counter()
    result = {"exact": exact_checks(), "numerical": numeric_sk_checks()}
    result["wall_seconds"] = time.perf_counter() - start
    path = Path(__file__).with_name("check_response.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"exact_assertions": result["exact"]["assertions"],
                      "numerical_cases": len(result["numerical"]["cases"]),
                      "wall_seconds": result["wall_seconds"],
                      "output": str(path)}, indent=2))
