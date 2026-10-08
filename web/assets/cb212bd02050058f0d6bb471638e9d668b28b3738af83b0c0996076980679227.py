#!/usr/bin/env python3
"""Finite diagnostic for an interpolating SU(3) wall-fiber eigenvalue bound.

This instantiates the CPV tridiagonal X,Y matrices and the exact affine
L_S map in MISSING_LABEL_MAPPING.txt. It tests, on bounded carriers and all
low-output labels in the requested region, the candidate sorted-spectrum
bound kappa_l >= c [j_l + eta*j_l^2], eta=(a-b)/(a+b),
j_l=|p-q|/3+l-1. This is finite numerical evidence only.
"""

from __future__ import annotations

import numpy as np


def ls_eigenvalues(a: int, b: int, p: int, q: int) -> tuple[np.ndarray, int]:
    """Build the exact CPV source block, then symmetrize by diagonal similarity."""
    N = a + b
    ell = N + 1 - (p + 2 * q) / 3
    n = N + 1 - (2 * p + q) / 3
    # p <= q, so ell <= n and the source's omega_m basis applies.
    xi = np.array(
        [ell, b + 1, b + 1 + ell - n, ell - a - 1, n - a - 1, 0.0],
        dtype=float,
    )
    xi_b = max(xi[3:])
    dim = int(round(min(xi[:3]) - xi_b))
    Lambda = float(sum(xi[:3]) - sum(xi[3:]) + 2 * abs(ell - n))
    lambda_minus = -Lambda / 2 + float(sum(xi)) / 6
    lambda_plus = Lambda / 2 + float(sum(xi)) / 6

    X = np.zeros((dim, dim), dtype=float)
    Y = np.zeros((dim, dim), dtype=float)
    for i in range(1, dim + 1):
        x = xi - i - xi_b + 0.5
        E = {k: float(np.sum(x**k)) for k in range(1, 5)}
        X[i - 1, i - 1] = (
            -(3.5 * E[1] ** 3 - 18 * E[1] * E[2] + 18 * E[3]) / 108
            - E[1] * (Lambda**2 + 2) / 24
        )
        Y[i - 1, i - 1] = (
            2.5 * E[1] ** 4
            + 32 * E[1] * E[3]
            + 6 * (E[2] ** 2 - 3 * E[1] ** 2 * E[2] - 4 * E[4])
            + 6 * E[2] * (Lambda**2 + 2)
            - 3 * E[1] ** 2 * (Lambda**2 - 2)
            - 1.5 * Lambda**4
            + 6 * Lambda**2
            - 36
        ) / 288

    for j in range(1, dim):
        x_upper = float(np.prod([j + xi_b - z for z in xi[:3]]))
        x_lower = float(np.prod([j + xi_b - z for z in xi[3:]]))
        X[j - 1, j] = x_upper
        X[j, j - 1] = x_lower
        Y[j - 1, j] = x_upper * (j + xi_b - lambda_minus)
        Y[j, j - 1] = x_lower * (j + xi_b - lambda_plus)

    C2 = (a * a + a * b + b * b + 3 * a + 3 * b) / 3
    C3 = (a - b) * (2 * a + b + 3) * (a + 2 * b + 3) / 18
    alpha = C3 / C2
    c = (p * p + p * q + q * q + 3 * p + 3 * q) / 3
    scalar = -c * c / 12 + (C2 / 3 + 0.25 + alpha**2) * c - 4 * alpha * C3 / 3
    K = (-Y - 2 * alpha * X + scalar * np.eye(dim)) / N**2

    # A real irreducible tridiagonal self-adjoint operator in its physical
    # multiplicity metric is similar to a symmetric Jacobi matrix. Preserve
    # the common sign of each off-diagonal pair under this diagonal similarity.
    J = np.diag(np.diag(K).copy())
    for i in range(dim - 1):
        product = K[i, i + 1] * K[i + 1, i]
        if product <= 0:
            raise ArithmeticError(
                f"nonpositive off-diagonal product at {(a, b, p, q, i)}: {product}"
            )
        entry = np.sign(K[i, i + 1]) * np.sqrt(product)
        J[i, i + 1] = entry
        J[i + 1, i] = entry
    return np.linalg.eigvalsh(J), dim


def main() -> None:
    worst = (float("inf"), None)
    blocks = 0
    tested = 0
    for b in range(1, 21):
        for a in range(b, 61):
            eta = (a - b) / (a + b)
            for p in range(a + 1):
                for q in range(p, a - p + 1):
                    if (p + 2 * q) % 3:
                        continue
                    delta = (q - p) // 3
                    j_max = min((2 * p + q) // 3, b)
                    if delta > j_max:
                        continue
                    eigenvalues, dim = ls_eigenvalues(a, b, p, q)
                    blocks += 1
                    if dim != j_max - delta + 1:
                        raise AssertionError(
                            f"CPV/GT dimension mismatch {(a,b,p,q,dim,delta,j_max)}"
                        )
                    js = np.arange(delta, delta + dim)
                    for eig, j in zip(eigenvalues, js):
                        if j == 0:
                            continue  # the only unconstrained slot in the candidate
                        ratio = eig / (j + eta * j * j)
                        tested += 1
                        if ratio < worst[0]:
                            worst = (float(ratio), (a, b, p, q, int(j), float(eig)))

    print(f"CPV blocks checked: {blocks:,} carrier/output blocks (a<=60,b<=20)")
    print(f"nonzero-index eigenvalue tests: {tested}")
    print(f"minimum kappa/[j+eta*j^2]: {worst[0]:.12g}")
    print(f"attained at (a,b,p,q,j,kappa): {worst[1]}")
    print("Status: finite numerical diagnostic only; no uniform theorem inferred.")


if __name__ == "__main__":
    main()
