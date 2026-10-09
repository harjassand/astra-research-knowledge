"""Finite diagnostic for the anisotropic shifted-initializer counterexample."""
from __future__ import annotations
import json
import math
import numpy as np


def run(n=2_000_000, d=3, sigma=100.0, q=1.0, seed=2503, batch=50_000):
    rng = np.random.default_rng(seed)
    kappa = 1.0 / (8.0 * math.pi)
    L = kappa * sigma**2 / q**2
    A = 2.0 * L
    p = sigma**2 / (A**2 + sigma**2)
    b = sigma**2 / A
    x = np.zeros(d)
    x[2] = q
    accum = np.zeros((d, d), dtype=np.float64)
    rare_count = 0
    done = 0
    while done < n:
        k = min(batch, n - done)
        a = rng.standard_normal((k, d))
        signal = (a @ x) ** 2
        sign = np.where(a[:, 0] ** 2 >= a[:, 1] ** 2, 1.0, -1.0)
        rare = rng.random(k) < p
        zeta = np.where(rare, sign * A, -sign * b)
        y = signal + zeta
        cy = np.clip(y, -L, L)
        accum += np.einsum("i,ij,ik->jk", cy, a, a, optimize=True)
        rare_count += int(rare.sum())
        done += k
    qhat = L * np.eye(d) + accum / n
    vals, vecs = np.linalg.eigh(qhat)
    top = vecs[:, -1]
    target = (L + q**2) * np.eye(d) + 2 * np.outer(x, x)
    target_vals = np.linalg.eigvalsh(target)
    c = p * L
    ideal_bias = -c * np.diag([2 / math.pi, -2 / math.pi] + [0.0] * (d - 2))
    ideal_q = target + ideal_bias
    ideal_vals, ideal_vecs = np.linalg.eigh(ideal_q)
    return {
        "n": n, "d": d, "q": q, "sigma": sigma, "s": sigma / q**2,
        "kappa": kappa, "L": L, "A": A, "p": p, "b": b,
        "expected_rare_count": n * p, "observed_rare_count": rare_count,
        "pL": c, "asymptotic_pL_over_q2": c / q**2,
        "target_eigenvalues": target_vals.tolist(),
        "anisotropic_approx_eigenvalues": ideal_vals.tolist(),
        "empirical_shifted_eigenvalues": vals.tolist(),
        "top_overlap_e2_squared": float(top[1] ** 2),
        "top_overlap_signal_e3_squared": float(top[2] ** 2),
        "approx_top_overlap_e2_squared": float(ideal_vecs[1, -1] ** 2),
        "approx_top_overlap_signal_e3_squared": float(ideal_vecs[2, -1] ** 2),
    }

if __name__ == "__main__":
    print(json.dumps({"scope": "finite diagnostic only; exact remainder proof is in v7.txt", "result": run()}, indent=2, sort_keys=True))
