"""Finite checks for the row-rescaled Sidon design as a POVM.

The proof is algebraic in the report. This numerical check exercises the
normalization, POVM completeness, and weighted linear inverse in small d.
It is diagnostic, not a proof or a hardware benchmark.
"""

from __future__ import annotations

import numpy as np


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % q for q in range(2, int(n**0.5) + 1))


def next_odd_prime(d: int) -> int:
    q = max(3, d)
    while not is_prime(q):
        q += 1
    return q


def check(d: int) -> tuple[int, float, float, float, float]:
    q = next_odd_prime(d)
    S = [(x, x * x % q) for x in range(d)]
    nu_char = d / (q * q * (d + 1))
    nu_basis = 1 / (d * (d + 1))
    # The coordinate projectors sum to I (not d I); the character
    # projectors sum to q^2/d I. The two square-root-weighted layers
    # therefore contribute (q+1)/sqrt(d(d+1)) I.
    gamma = np.sqrt(d * (d + 1)) / (q + 1)

    vectors: list[np.ndarray] = []
    weights: list[float] = []
    for a in range(q):
        for b in range(q):
            vectors.append(np.array([
                np.exp(2j * np.pi * (a * x + b * y) / q) / np.sqrt(d)
                for x, y in S
            ], dtype=complex))
            weights.append(nu_char)
    for j in range(d):
        e = np.zeros(d, dtype=complex)
        e[j] = 1
        vectors.append(e)
        weights.append(nu_basis)

    projectors = [np.outer(u, u.conj()) for u in vectors]
    effects = [gamma * np.sqrt(w) * P for w, P in zip(weights, projectors)]
    completeness = sum(effects, start=np.zeros((d, d), dtype=complex))

    rng = np.random.default_rng(20261008 + d)
    x = rng.normal(size=d) + 1j * rng.normal(size=d)
    x /= np.linalg.norm(x)
    X = np.outer(x, x.conj())
    outcome_probs = np.array([np.trace(E @ X).real for E in effects])
    # Weighted design inverse: T = sum_j sqrt(nu_j) q_j Pi_j.
    T = sum((np.sqrt(w) * prob * P
             for w, prob, P in zip(weights, outcome_probs, projectors)),
            start=np.zeros((d, d), dtype=complex))
    Xhat = (d * (d + 1) / gamma) * T - (d / gamma) * np.trace(T) * np.eye(d)

    # Wrong but tempting: use the usual design POVM effects d*nu_j*Pi_j.
    # Its phase-retrieval fourth-power weights are proportional to nu_j^2.
    z = sum(w * w for w in weights)
    wrong_moment = sum(
        [((w * w / z) * np.kron(P, P))
         for w, P in zip(weights, projectors)],
        start=np.zeros((d * d, d * d), dtype=complex),
    )
    swap = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            swap[i * d + j, j * d + i] = 1
    target = (np.eye(d * d) + swap) / (d * (d + 1))
    wrong_design_error = float(np.max(np.abs(wrong_moment - target)))
    design_moment = sum(
        [(w * np.kron(P, P)) for w, P in zip(weights, projectors)],
        start=np.zeros((d * d, d * d), dtype=complex),
    )
    design_error = float(np.max(np.abs(design_moment - target)))

    # Coordinate states have identical character-layer distributions and
    # differ only on two basis outcomes, each of probability 1/(q+1).
    e0 = np.eye(d, dtype=complex)[:, 0]
    e1 = np.eye(d, dtype=complex)[:, 1]
    probs0 = np.array([np.vdot(e0, E @ e0).real for E in effects])
    probs1 = np.array([np.vdot(e1, E @ e1).real for E in effects])
    h2 = float(np.sum((np.sqrt(probs0) - np.sqrt(probs1)) ** 2))
    h2_error = abs(h2 - 2 / (q + 1))
    return (q * q + d,
            float(np.max(np.abs(completeness - np.eye(d)))),
            float(np.max(np.abs(Xhat - X))),
            design_error, wrong_design_error, h2_error)


if __name__ == "__main__":
    for dim in range(2, 11):
        m, povm_err, inverse_err, design_err, wrong_err, h2_err = check(dim)
        print(f"d={dim:2d} m={m:4d} povm_error={povm_err:.3e} "
              f"inverse_error={inverse_err:.3e} "
              f"design_error={design_err:.3e} "
              f"usual_design_povm_fourth_moment_error={wrong_err:.3e}")
        print(f"           coordinate_pair_H2_error={h2_err:.3e} "
              f"target_H2={2 / (next_odd_prime(dim) + 1):.6f}")
