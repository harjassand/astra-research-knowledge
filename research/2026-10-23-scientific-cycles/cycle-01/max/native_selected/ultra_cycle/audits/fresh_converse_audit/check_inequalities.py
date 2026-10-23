"""Independent finite checks of the coarse-grained converse normalizations.

These are deterministic arithmetic checks, not a proof of the imported LSI.
Run with python3 check_inequalities.py. Only writes its JSON receipt locally.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


def norm2(x):
    return float(np.vdot(x, x).real / x.shape[0])


def reset(x, sites, D, n):
    """Normalized conditional expectation onto identity on selected sites."""
    sites = tuple(sites)
    rest = tuple(i for i in range(n) if i not in sites)
    permutation = sites + rest + tuple(n + i for i in sites + rest)
    s, r = D ** len(sites), D ** len(rest)
    y = x.reshape((D,) * (2 * n)).transpose(permutation).reshape(s, r, s, r)
    reduced = np.trace(y, axis1=0, axis2=2)
    grouped = np.kron(np.eye(s) / s, reduced)
    return grouped.reshape((D,) * (2 * n)).transpose(np.argsort(permutation)).reshape(x.shape)


def bell_probability_direct(x, sites, D, n):
    """Direct contraction of vec(x)/sqrt(d) with Bell bras on selected pairs."""
    sites = tuple(sites)
    rest = tuple(i for i in range(n) if i not in sites)
    r = D ** len(rest)
    amplitude = np.zeros((r, r), dtype=complex)
    for u, aa in enumerate(itertools.product(range(D), repeat=len(rest))):
        for v, bb in enumerate(itertools.product(range(D), repeat=len(rest))):
            for ss in itertools.product(range(D), repeat=len(sites)):
                row, col = [0] * n, [0] * n
                for j, value in zip(sites, ss):
                    row[j] = col[j] = value
                for j, value in zip(rest, aa):
                    row[j] = value
                for j, value in zip(rest, bb):
                    col[j] = value
                amplitude[u, v] += x[np.ravel_multi_index(row, (D,) * n), np.ravel_multi_index(col, (D,) * n)]
    return float(np.vdot(amplitude, amplitude).real / (D ** (n + len(sites))))


def entropy_deficit(x):
    eigenvalues = np.linalg.svd(x, compute_uv=False) ** 2
    nonzero = eigenvalues[eigenvalues > 1e-14]
    return float(np.dot(nonzero, np.log(nonzero)) / len(eigenvalues))


def local_A(Q):
    ratio = 2.0 if Q == 2 else math.log(Q - 1) / (1 - 2 / Q)
    return 1.5 * math.log(2) * ratio


def main():
    rng = np.random.default_rng(20261021)
    receipt = {"purpose": "normalization and coefficient checks; not external LSI proof"}
    count, min_gap = 0, math.inf
    for N in range(1, 17):
        for b in range(1, N + 1):
            if N % b:
                continue
            for bits in itertools.product((0, 1), repeat=N):
                active = [i for i, bit in enumerate(bits) if bit]
                hierarchy = N - min(active) if active else 0
                chunks = sum(any(bits[j:j + b]) for j in range(0, N, b))
                gap = hierarchy - (b * chunks - (b - 1))
                assert gap >= 0
                min_gap = min(min_gap, gap)
                count += 1
    receipt["coarse_basis"] = {"binary_supports_checked": count, "N_max": 16, "minimum_gap": min_gap}

    coefficient_error, minimum_lsi_slack, minimum_coarse_slack = 0.0, math.inf, math.inf
    cases = []
    for D, N, t, b in [(2, 4, 1, 2), (2, 2, 2, 1), (3, 2, 1, 2), (2, 3, 1, 3)]:
        n, d, m = N * t, D ** (N * t), math.log(D)
        matrices = [np.eye(d, dtype=complex)]
        for _ in range(6):
            z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
            matrices.extend([z, z.conj().T @ z])
        matrices.append(np.diag([math.sqrt(d)] + [0] * (d - 1)).astype(complex))
        for x in matrices:
            x = x / math.sqrt(norm2(x))
            hierarchy = 0.0
            for a in range(t):
                for i in range(1, N + 1):
                    sites = list(range(a * N, a * N + i))
                    p = norm2(reset(x, sites, D, n))
                    coefficient_error = max(coefficient_error, abs(p - bell_probability_direct(x, sites, D, n)))
                    hierarchy += m * (1 - p)
            chunks = sum(1 - norm2(reset(x, range(a * N + j, a * N + j + b), D, n))
                         for a in range(t) for j in range(0, N, b))
            ent = entropy_deficit(x)
            coarse_slack = hierarchy - b * m * chunks + t * (b - 1) * m
            lsi_slack = local_A(D ** b) * chunks - ent
            minimum_coarse_slack = min(minimum_coarse_slack, coarse_slack)
            minimum_lsi_slack = min(minimum_lsi_slack, lsi_slack)
            assert coarse_slack > -1e-10
            assert lsi_slack > -1e-10
        cases.append({"D": D, "N": N, "t": t, "b": b, "matrices": len(matrices)})
    receipt["matrix_checks"] = {"cases": cases, "max_Bell_coefficient_error": coefficient_error,
                                "minimum_coarse_slack": minimum_coarse_slack,
                                "minimum_LSI_slack": minimum_lsi_slack}
    extremizers = []
    for Q in range(3, 21):
        x = np.diag([Q - 1] + [1] * (Q - 1)).astype(complex)
        x /= math.sqrt(norm2(x))
        ent = entropy_deficit(x)
        energy = 1 - abs(np.trace(x) / Q) ** 2
        expected = math.log(Q - 1) / (1 - 2 / Q)
        assert abs(ent / energy - expected) < 1e-10
        extremizers.append({"Q": Q, "Ent_over_energy": ent / energy, "exact_local_inverse_alpha": expected})
    receipt["local_constant_extremizers"] = extremizers

    # A symbolic positive-increment expansion used by the stronger stopping bound.
    moment_checks = []
    for D, N, L in [(2, 1, 2), (2, 7, 4), (3, 5, 3), (17, 3, 6)]:
        g = [math.exp(-L)] + [D ** k for k in range(1, N + 1)]
        expanded = g[0] + sum((g[i] - g[i - 1]) * D ** (-i) for i in range(1, N + 1))
        closed = 1 + (N - 1 + math.exp(-L)) * (1 - 1 / D)
        assert abs(expanded - closed) < 1e-10
        moment_checks.append({"D": D, "N": N, "L": L, "expanded": expanded, "closed": closed})
    receipt["stopping_moment_constants"] = moment_checks
    receipt["asymptotic_coarse_coefficient"] = 1 / (3 * math.log(2))
    receipt["stronger_stopping_coefficient"] = 0.5
    receipt["status"] = "PASS"
    (HERE / "CHECK_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "local_constant_extremizers"}, indent=2))


if __name__ == "__main__":
    main()
