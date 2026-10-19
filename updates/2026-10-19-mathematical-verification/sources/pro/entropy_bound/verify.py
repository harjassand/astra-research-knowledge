"""Targeted numerical audits. They supplement, and do not replace, the proofs."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm, null_space


RNG = np.random.default_rng(20261019)


def symmetric_power(x: np.ndarray, power: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((x + x.T) / 2)
    assert values.min() > 0
    return (vectors * values**power) @ vectors.T


def entropy_audits() -> dict:
    min_ratio = np.inf
    checks = 0
    for n in [3, 4, 5, 8, 12]:
        for _ in range(160):
            p = np.exp(RNG.uniform(-4, 1, n))
            p /= p.sum()
            f = RNG.uniform(0.01, 1, (n, n))
            f = (f + f.T) / 2
            np.fill_diagonal(f, 0)
            for _ in range(n):
                length = int(RNG.integers(3, n + 1))
                cycle = RNG.choice(n, length, replace=False)
                amount = RNG.uniform(0.01, 1)
                for u, v in zip(cycle, np.roll(cycle, -1)):
                    f[u, v] += amount
            q = f / p[:, None]
            q[np.diag_indices(n)] = -q.sum(axis=1)
            assert np.max(np.abs(p @ q)) < 2e-12
            a = np.sqrt(p)[:, None] * q / np.sqrt(p)[None, :]
            k = (a - a.T) / 2
            skew2 = float(np.sum(k * k))
            sigma = sum(
                (f[i, j] - f[j, i]) * np.log(f[i, j] / f[j, i])
                for i in range(n) for j in range(i + 1, n)
            )
            total = -np.trace(q)
            s = sum(np.sort(p)[:2])
            coefficient = max(12 * p.min(), 2 * s)
            bound = coefficient * skew2 / total
            assert sigma + 1e-10 >= bound, (n, p, sigma, bound)
            min_ratio = min(min_ratio, sigma / bound)
            checks += 1
    # Sharpness of the uniform stationary constant for the skew-only bound.
    triangle_ratios = []
    n = 5
    for epsilon in [1e-1, 1e-2, 1e-3]:
        f = np.zeros((n, n))
        for i in range(3):
            j = (i + 1) % 3
            f[i, j] = 1 + epsilon
            f[j, i] = 1 - epsilon
        p = np.full(n, 1 / n)
        q = f / p[:, None]
        q[np.diag_indices(n)] = -q.sum(axis=1)
        k = (q - q.T) / 2
        sigma = 3 * (2 * epsilon) * np.log((1 + epsilon)/(1-epsilon))
        bound = 12 / n / (-np.trace(q)) * np.sum(k*k)
        triangle_ratios.append(float(sigma / bound))
    assert triangle_ratios[-1] < 1.000001
    return {"checks": checks, "min_random_sigma_over_bound": min_ratio,
            "sharp_triangle_ratios": triangle_ratios}


def branch_audits() -> dict:
    errors = []
    entropy_ratios = []
    for n in [3, 4, 6]:
        for _ in range(15):
            p = RNG.uniform(0.2, 1, n)
            p /= p.sum()
            u = np.sqrt(p)
            w = null_space(u[None, :])
            # A nonnormal logarithm with one conjugate branch pair +/-2 pi i.
            similarity = np.diag([RNG.uniform(0.7, 1.4), 1.0])
            rotation = 2 * np.pi * np.array([[0., -1.], [1., 0.]])
            block = similarity @ rotation @ np.linalg.inv(similarity)
            b = w[:, :2] @ block @ w[:, :2].T
            # An equilibrium complete-graph baseline guarantees generator signs.
            c = max(1.0, max(
                -b[i, j] / (u[i]*u[j])
                for i in range(n) for j in range(n) if i != j
            )) + 2
            h = -c * (np.eye(n) - np.outer(u, u))
            a = h + b
            q = a * u[None, :] / u[:, None]
            assert np.max(np.abs(q.sum(axis=1))) < 5e-12
            assert np.min(q[~np.eye(n, dtype=bool)]) > 0
            k = (a - a.T) / 2
            uu = (a + a.T) / 2 - h
            residual = np.sum(k*k) - np.sum(uu*uu) - 8*np.pi**2
            errors.append(abs(float(residual)))
            # Stable direct exponential equality; no numerical log of tiny modes.
            assert np.linalg.norm(expm(a) - expm(h)) < 1e-11
            f = p[:, None] * q
            sigma = sum((f[i,j]-f[j,i])*np.log(f[i,j]/f[j,i])
                        for i in range(n) for j in range(i+1,n))
            bound = max(12*p.min(), 2*sum(np.sort(p)[:2])) / (-np.trace(q)) \
                    * (np.sum(uu*uu) + 8*np.pi**2)
            entropy_ratios.append(float(sigma/bound))
    return {"checks": len(errors), "max_branch_identity_residual": max(errors),
            "min_sigma_over_nonprincipal_bound": min(entropy_ratios)}


def compression_audits() -> dict:
    ratios = []
    smallest_psd_eigenvalue = 0.0
    for n, m in [(4, 2), (6, 3), (10, 4), (16, 5)]:
        for _ in range(80):
            orth, _ = np.linalg.qr(RNG.normal(size=(n, n)))
            eigenvalues = np.exp(RNG.uniform(-10, 0, n))
            matrix = (orth * eigenvalues) @ orth.T
            r = matrix[:m, :m]
            delta = (matrix @ matrix)[:m, :m] - r @ r
            a = np.linalg.eigvalsh(r).min()
            for alpha in [0.15, 0.5, 0.85]:
                gap = symmetric_power(r, alpha) - symmetric_power(matrix, alpha)[:m,:m]
                smallest_psd_eigenvalue = min(smallest_psd_eigenvalue,
                                              float(np.linalg.eigvalsh(gap).min()))
                bound = (1-alpha)*a**(alpha-2)*np.linalg.norm(delta, 2)
                ratio = np.linalg.norm(gap, 2) / bound
                assert np.linalg.eigvalsh(gap).min() > -1e-11
                assert ratio <= 1 + 1e-9
                ratios.append(float(ratio))
    # Approach the sharp constant for general positive compression matrices.
    sharp_ratios = []
    a, alpha = 0.4, 0.5
    for b in [0.03, 0.01, 0.003]:
        matrix = np.array([[a,b],[b,b*b/a+1e-14]])
        gap = a**alpha - symmetric_power(matrix, alpha)[0,0]
        bound = (1-alpha)*a**(alpha-2)*b*b
        sharp_ratios.append(float(gap/bound))
    return {"checks": len(ratios), "max_gap_over_bound": max(ratios),
            "minimum_gap_eigenvalue": smallest_psd_eigenvalue,
            "general_positive_operator_sharpness_ratios": sharp_ratios}


if __name__ == "__main__":
    result = {"seed": 20261019, "entropy": entropy_audits(),
              "branch": branch_audits(), "compression": compression_audits()}
    path = Path(__file__).with_name("verification.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
