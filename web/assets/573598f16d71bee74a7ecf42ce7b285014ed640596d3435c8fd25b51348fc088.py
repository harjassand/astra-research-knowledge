"""Finite checks for the all-d weighted 2-design phase-retrieval construction.

For odd prime p >= d, take the Sidon subset S={(x,x^2):0<=x<d} of G=F_p^2.
The Bodmann--Haas construction has p^2+d points.  This script verifies the
weighted complex-projective 2-design moment numerically for small dimensions.
It is a finite diagnostic, not a proof or a statistical/exposure guarantee.
"""

from __future__ import annotations

import numpy as np


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % q for q in range(2, int(n**0.5) + 1))


def next_odd_prime_at_least(d: int) -> int:
    p = max(3, d)
    while not is_prime(p):
        p += 1
    return p


def swap_operator(d: int) -> np.ndarray:
    f = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            f[i * d + j, j * d + i] = 1
    return f


def check_dimension(d: int) -> tuple[int, float, float]:
    p = next_odd_prime_at_least(d)
    points = [(x, (x * x) % p) for x in range(d)]
    vecs: list[np.ndarray] = []
    probs: list[float] = []

    # Character vectors, one for each character of F_p^2.
    for a in range(p):
        for b in range(p):
            u = np.array(
                [np.exp(2j * np.pi * (a * x + b * y) / p) / np.sqrt(d)
                 for x, y in points],
                dtype=complex,
            )
            vecs.append(u)
            probs.append(d / (p * p * (d + 1)))

    # Coordinate vectors, one for each point of S.
    for j in range(d):
        u = np.zeros(d, dtype=complex)
        u[j] = 1
        vecs.append(u)
        probs.append(1 / (d * (d + 1)))

    moment = np.zeros((d * d, d * d), dtype=complex)
    for u, prob in zip(vecs, probs):
        pi = np.outer(u, u.conj())
        pi2 = np.kron(pi, pi)
        moment += prob * pi2

    target = (np.eye(d * d) + swap_operator(d)) / (d * (d + 1))
    # Row scaling ||a_j||^4 = prob makes these the phase-retrieval weights.
    row_weighted_moment = sum(
        prob * np.kron(np.outer(u, u.conj()), np.outer(u, u.conj()))
        for u, prob in zip(vecs, probs)
    )
    return len(vecs), float(np.max(np.abs(moment - target))), float(np.max(np.abs(row_weighted_moment - target)))


if __name__ == "__main__":
    for d in range(2, 11):
        m, moment_err, scaled_err = check_dimension(d)
        print(f"d={d:2d} m={m:4d} moment_error={moment_err:.3e} scaled_error={scaled_err:.3e}")
