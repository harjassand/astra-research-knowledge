"""Finite sanity check for Cycle 3's completed Gaussian-block POVM.

This checks only the algebra of one finite-alphabet fixture. It is not a test
of Huang--Li--Needell's uniform statistical theorem, optical calibration, or
the unitary approximation lemma in the accompanying audit.
"""

from __future__ import annotations

import numpy as np


def unit_vector(rng: np.random.Generator, d: int) -> np.ndarray:
    x = rng.normal(size=d) + 1j * rng.normal(size=d)
    return x / np.linalg.norm(x)


def finite_alphabet_matrix(rng: np.random.Generator, m: int, d: int) -> np.ndarray:
    # P(phi=0)=3/4 and P(phi in {2,-2,2i,-2i})=1/16 each.
    alphabet = np.array([0, 2, -2, 2j, -2j], dtype=np.complex128)
    probabilities = np.array([12, 1, 1, 1, 1], dtype=float) / 16
    return rng.choice(alphabet, size=(m, d), p=probabilities)


def main() -> None:
    rng = np.random.default_rng(20261008)
    d, m = 4, 256
    eta, nbar = 0.73, 5000.0
    G = finite_alphabet_matrix(rng, m, d)
    gram = G.conj().T @ G
    ev, V = np.linalg.eigh(gram)
    if ev[0] < m / 4 or ev[-1] > 4 * m:
        raise RuntimeError("fixture did not land in the stated good-frame event")

    a = 1 / (4 * m)
    residual_evs, residual_V = np.linalg.eigh(np.eye(d) - a * gram)
    R = (residual_V * np.sqrt(np.maximum(residual_evs, 0))) @ residual_V.conj().T
    B = np.vstack((np.sqrt(a) * G, R))
    parseval_error = np.linalg.norm(B.conj().T @ B - np.eye(d), ord=2)

    x = unit_vector(rng, d)
    q_block = a * np.linalg.norm(G @ x) ** 2
    means_physical = nbar * eta * a * np.abs(G @ x) ** 2
    w = np.sqrt(nbar * eta * a) * x
    means_hln = np.abs(G @ w) ** 2
    mean_error = np.max(np.abs(means_physical - means_hln))

    # Complete B to a unitary U, then test the one-photon TV bound under a
    # small coherent unitary perturbation. The inequality itself is proved in
    # CYCLE3_AUDIT.md; this merely checks one numerical instance.
    complement = np.linalg.svd(B.conj().T, full_matrices=True)[2].conj().T[:, d:]
    U = np.column_stack((B, complement))
    M = U.shape[0]
    H0 = rng.normal(size=(M, M)) + 1j * rng.normal(size=(M, M))
    H = (H0 + H0.conj().T) / 2
    H /= np.linalg.norm(H, ord=2)
    delta_parameter = 1e-5
    rotation = np.linalg.eigh(H)
    expH = (rotation[1] * np.exp(1j * delta_parameter * rotation[0])) @ rotation[1].conj().T
    U_tilde = expH @ U
    operator_error = np.linalg.norm(U_tilde - U, ord=2)
    input_with_vacuum = np.zeros(M, dtype=np.complex128)
    input_with_vacuum[:d] = x
    p = np.abs(U @ input_with_vacuum) ** 2
    p_tilde = np.abs(U_tilde @ input_with_vacuum) ** 2
    tv = 0.5 * np.sum(np.abs(p - p_tilde))

    print(f"dimension={d}, Gaussian-block rows={m}, total POVM outputs={m+d}")
    print(f"good Gram eigenvalue range=[{ev[0]:.6g}, {ev[-1]:.6g}]")
    print(f"Gaussian-block one-photon probability={q_block:.9f} (target range [1/16,1])")
    print(f"Parseval operator-norm residual={parseval_error:.3e}")
    print(f"maximum Poisson-mean identity residual={mean_error:.3e}")
    print(f"unitary perturbation operator norm={operator_error:.3e}")
    print(f"one-photon outcome total variation={tv:.3e}")

    assert 1 / 16 <= q_block <= 1
    assert parseval_error < 1e-12
    assert mean_error < 1e-10
    assert tv <= operator_error + 1e-12


if __name__ == "__main__":
    main()
