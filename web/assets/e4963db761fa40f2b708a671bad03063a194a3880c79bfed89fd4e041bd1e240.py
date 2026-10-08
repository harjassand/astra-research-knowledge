"""Finite arithmetic checks for the Parseval-frame photon-count model.

This script checks normalization/whitening and the exact product-Poisson
Bhattacharyya formula on one deterministic random fixture.  It does not test
the uniform Gaussian-frame theorem or phase-retrieval stability.
"""

from __future__ import annotations

import math
import numpy as np


def unit_complex(rng: np.random.Generator, d: int) -> np.ndarray:
    z = rng.normal(size=d) + 1j * rng.normal(size=d)
    return z / np.linalg.norm(z)


def poisson_affinity_truncated(lam: float, mu: float) -> float:
    cutoff = int(math.ceil(max(lam, mu) + 14 * math.sqrt(max(lam, mu, 1.0)) + 40))
    ks = np.arange(cutoff + 1, dtype=float)

    def root_prob(mean: float) -> np.ndarray:
        if mean == 0:
            out = np.zeros_like(ks)
            out[0] = 1.0
            return np.sqrt(out)
        logs = -mean + ks * math.log(mean) - np.array([math.lgamma(k + 1) for k in ks])
        return np.exp(0.5 * logs)

    return float(np.dot(root_prob(lam), root_prob(mu)))


def main() -> None:
    rng = np.random.default_rng(20261008)
    d, m, tau = 4, 24, 7.5
    A = (rng.normal(size=(m, d)) + 1j * rng.normal(size=(m, d))) / math.sqrt(2)
    C = A.conj().T @ A / m
    eigvals, eigvecs = np.linalg.eigh(C)
    C_inv_sqrt = (eigvecs * (eigvals ** -0.5)) @ eigvecs.conj().T
    B = A @ C_inv_sqrt / math.sqrt(m)

    parseval_error = float(np.linalg.norm(B.conj().T @ B - np.eye(d), ord=2))
    x, y = unit_complex(rng, d), unit_complex(rng, d)
    px, py = np.abs(B @ x) ** 2, np.abs(B @ y) ** 2
    if np.min(px) <= 0 or np.min(py) <= 0:
        raise RuntimeError("generic fixture unexpectedly has a zero outcome probability")
    mass_error = max(abs(float(px.sum()) - 1.0), abs(float(py.sum()) - 1.0))
    amplitude_h2 = float(np.sum((np.sqrt(px) - np.sqrt(py)) ** 2))
    predicted_bc = math.exp(-tau * amplitude_h2 / 2)
    marginal_bcs = [
        poisson_affinity_truncated(tau * float(p), tau * float(q))
        for p, q in zip(px, py)
    ]
    product_bc = float(np.prod(marginal_bcs))

    # Empirical check of E H^2(p_hat,p) <= (m-1)/N for a fixed categorical p.
    n_photons, trials = 80, 4000
    counts = rng.multinomial(n_photons, px, size=trials)
    phat = counts / n_photons
    h2 = np.sum((np.sqrt(phat) - np.sqrt(px)) ** 2, axis=1)
    empirical_mean_h2 = float(h2.mean())
    analytic_upper = (m - 1) / n_photons

    print(f"d={d}, channels={m}, expected Poisson photons={tau}")
    print(f"Parseval operator-norm residual: {parseval_error:.3e}")
    print(f"probability mass residual: {mass_error:.3e}")
    print(f"amplitude/Hellinger squared separation: {amplitude_h2:.9f}")
    print(f"Poisson product affinity (truncated marginal product): {product_bc:.12g}")
    print(f"Poisson product affinity (closed form): {predicted_bc:.12g}")
    print(f"absolute affinity discrepancy: {abs(product_bc - predicted_bc):.3e}")
    print(f"empirical E H^2(p_hat,p): {empirical_mean_h2:.6f}")
    print(f"proved upper (m-1)/N: {analytic_upper:.6f}")

    assert parseval_error < 1e-12
    assert mass_error < 1e-12
    assert abs(product_bc - predicted_bc) < 1e-10
    # Monte Carlo estimates can cross the expectation slightly; this generous
    # factor is only a sanity check, not a confidence statement.
    assert empirical_mean_h2 < 1.15 * analytic_upper


if __name__ == "__main__":
    main()
