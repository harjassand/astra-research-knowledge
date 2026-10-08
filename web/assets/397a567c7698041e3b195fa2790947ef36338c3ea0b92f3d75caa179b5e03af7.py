#!/usr/bin/env python3
"""Replay two exact fixed-POVM failures recorded in PROOF_AND_GATE.md.

Python 3 + NumPy. These reject only the named fixed measurements, not the
channel-adaptive universal EB-comparison claim.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_stinespring_compression as fixtures  # noqa: E402


def cloner_product_haar_score(order: int = 256) -> float:
    """Fisher/canonical score on Z for independent Haar POVMs on both clones."""
    kraus = fixtures.cloner_kraus()
    b = lambda x: sum(k @ x @ k.conj().T for k in kraus)
    ident = np.eye(2, dtype=complex)
    z = np.diag([1.0, -1.0]).astype(complex)
    p_sym = np.zeros((4, 4), dtype=complex)
    p_sym[0, 0] = p_sym[3, 3] = 1.0
    p_sym[1, 1] = p_sym[2, 2] = 0.5
    p_sym[1, 2] = p_sym[2, 1] = 0.5
    target = np.diag([1.0, 0.0, 0.0, -1.0]).astype(complex) / 3
    assert np.allclose(b(ident / 2), p_sym / 3, atol=1e-12)
    assert np.allclose(b(z / 2), target, atol=1e-12)

    # Haar averaging over the common orientation at fixed u=n.m gives
    # E[(n_z+m_z)^2 | u] = 2(1+u)/3, hence the reduced integral below.
    nodes, weights = np.polynomial.legendre.leggauss(order)
    integral = np.dot(weights, (1.0 + nodes) / (3.0 + nodes))
    return (4.0 / 9.0) * float(integral)


def dephasing_symmetric_coherent_score(order: int = 256) -> float:
    """Score for 3|psi psi><psi psi| on a copying Z-dephasing broadcaster."""
    nodes, weights = np.polynomial.legendre.leggauss(order)
    x = (nodes + 1.0) / 2.0
    # |psi_0|^2 is uniform on [0,1] for a Haar-random qubit pure state.
    integrand = (2.0 * x - 1.0) ** 2 / (x**2 + (1.0 - x) ** 2)
    integral = 0.5 * float(np.dot(weights, integrand))
    return 1.5 * integral


def main() -> None:
    product_score = cloner_product_haar_score()
    product_exact = (4.0 / 9.0) * (2.0 - 2.0 * math.log(2.0))
    assert abs(product_score - product_exact) < 1e-12
    assert product_score < 1.0 / 3.0

    coherent_score = dephasing_symmetric_coherent_score()
    coherent_exact = 3.0 - 3.0 * math.pi / 4.0
    assert abs(coherent_score - coherent_exact) < 1e-12
    assert coherent_score < 1.0

    print(f"cloner + independent product-Haar score: {product_score:.12f}")
    print(f"cloner target eigenvalue:                {1.0 / 3.0:.12f}")
    print(f"dephasing + symmetric coherent score:    {coherent_score:.12f}")
    print(f"dephasing target eigenvalue:              {1.0:.12f}")
    print("Both failures are for the fixed POVMs only.")


if __name__ == "__main__":
    main()
