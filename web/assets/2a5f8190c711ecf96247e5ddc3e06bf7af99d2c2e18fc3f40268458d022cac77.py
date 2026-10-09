"""Finite diagnostics for A25 signed/shifted spectral initialization.

These computations illustrate exact algebraic bounds; they are not theorem proofs.
Requires NumPy.
"""
from __future__ import annotations

import json
import math
import numpy as np


def two_point_parameters(sigma: float, L: float):
    """Variance-sigma^2 mean-zero noise with rare atom A=2L."""
    A = 2.0 * L
    p = sigma**2 / (A**2 + sigma**2)
    b = sigma**2 / A
    return A, p, b


def clipping_bias_mc(*, n=2_000_000, d=4, q=1.0, sigma=1.0, L=20.0,
                     batch=50_000, seed=2501):
    rng = np.random.default_rng(seed)
    A, p, b = two_point_parameters(sigma, L)
    x = np.zeros(d)
    x[0] = q
    total = np.zeros((d, d), dtype=np.float64)
    rare_count = 0
    done = 0
    while done < n:
        k = min(batch, n - done)
        a = rng.standard_normal((k, d))
        signal = (a @ x) ** 2
        rare = rng.random(k) < p
        zeta = np.where(rare, A, -b)
        y = signal + zeta
        clipped = np.clip(y, -L, L)
        residual = y - clipped
        total += np.einsum("i,ij,ik->jk", residual, a, a, optimize=True)
        rare_count += int(rare.sum())
        done += k
    empirical = total / n
    predicted_rare_floor = p * L
    exact_rare_diagonal = np.array([p * (L + 3 * q**2)] +
                                   [p * (L + q**2)] * (d - 1))
    return {
        "n": n, "d": d, "q": q, "sigma": sigma, "L": L,
        "A": A, "p": p, "b": b,
        "mean_noise_exact": 0.0,
        "variance_noise_exact": p * A**2 + (1 - p) * b**2,
        "expected_rare_count": n * p,
        "observed_rare_count": rare_count,
        "sigma2_over_L": sigma**2 / L,
        "conditional_bias_floor_pL": predicted_rare_floor,
        "floor_ratio_to_sigma2_over_L": predicted_rare_floor / (sigma**2 / L),
        "rare_only_population_bias_diagonal": exact_rare_diagonal.tolist(),
        "empirical_bias_diagonal": np.diag(empirical).tolist(),
        "empirical_bias_eigenvalues": np.linalg.eigvalsh(empirical).tolist(),
    }


def contamination_modulus_mc(*, n=2_000_000, d=8, q=1.0, theta=0.3,
                             sigma=5.0, seed=2502):
    rng = np.random.default_rng(seed)
    x = np.zeros(d)
    x[0] = q
    xp = np.zeros(d)
    xp[0] = q * math.cos(theta)
    xp[1] = q * math.sin(theta)
    delta2_sum = 0.0
    p_sum = 0.0
    done = 0
    batch = 50_000
    while done < n:
        k = min(batch, n - done)
        a = rng.standard_normal((k, d))
        delta = (a @ x) ** 2 - (a @ xp) ** 2
        delta2_sum += float(delta @ delta)
        p_sum += float(np.sum(delta**2 / (delta**2 + 4 * sigma**2)))
        done += k
    empirical_delta2 = delta2_sum / n
    empirical_tv = p_sum / n
    theory_delta2 = 4 * q**4 * math.sin(theta)**2
    theory_tv_upper = theory_delta2 / (4 * sigma**2)
    return {
        "n": n, "d": d, "q": q, "theta": theta, "sigma": sigma,
        "empirical_E_delta2": empirical_delta2,
        "theory_E_delta2": theory_delta2,
        "empirical_pair_TV_for_constructed_noise": empirical_tv,
        "theory_TV_upper_bound": theory_tv_upper,
        "contamination_floor_scale_sin2_over_s2": math.sin(theta)**2 / (sigma / q**2)**2,
    }


def main():
    result = {
        "scope": "finite numerical diagnostics only; exact proof is in v6.txt",
        "clipping_skew_example": clipping_bias_mc(),
        "two_point_TV_example": contamination_modulus_mc(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
