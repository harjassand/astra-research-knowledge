"""Finite exact-diagonalization benchmark for CYCLE2_REPORT.md."""

import json
import numpy as np


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
N = 4


def one_site(site, matrix):
    factors = [I] * N
    factors[site] = matrix
    result = factors[0]
    for factor in factors[1:]:
        result = np.kron(result, factor)
    return result


def two_site(site1, site2, matrix1, matrix2):
    factors = [I] * N
    factors[site1] = matrix1
    factors[site2] = matrix2
    result = factors[0]
    for factor in factors[1:]:
        result = np.kron(result, factor)
    return result


H_plus = np.zeros((2**N, 2**N), dtype=complex)
for u, v in ((0, 1), (1, 2), (2, 3)):
    H_plus += (
        two_site(u, v, X, X)
        + two_site(u, v, Y, Y)
        + 0.5 * two_site(u, v, Z, Z)
    )

b = [0.25] * N
c = [0.1, -0.15, 0.2, -0.1]
for site in range(N):
    H_plus += b[site] * one_site(site, X) + c[site] * one_site(site, Z)

beta = 0.7
eigenvalues, eigenvectors = np.linalg.eigh(H_plus)
weights = np.exp(beta * eigenvalues)
rho = (eigenvectors * weights) @ eigenvectors.conj().T / weights.sum()

# Trace out sites 3 and 2; tensor axes are row-0..row-3, col-0..col-3.
tensor = rho.reshape((2,) * 8)
tensor = np.trace(tensor, axis1=3, axis2=7)
tensor = np.trace(tensor, axis1=2, axis2=5)
rho_12 = tensor.reshape((4, 4))

xx_12 = np.kron(X, X)
purity_12 = float(np.trace(rho_12 @ rho_12).real)
expectation_xx_12 = float(np.trace(xx_12 @ rho_12).real)
C = 3 * 3 + sum(bi + abs(ci) for bi, ci in zip(b, c))

print(
    json.dumps(
        {
            "system": "four-site path",
            "alpha_edges": [1, 1, 1],
            "gamma_edges": [0.5, 0.5, 0.5],
            "b": b,
            "c": c,
            "beta": beta,
            "C": C,
            "trace_rho_12": float(np.trace(rho_12).real),
            "expectation_X1X2": expectation_xx_12,
            "purity_q2": purity_12,
            "rho_12_eigenvalues": np.linalg.eigvalsh(rho_12).tolist(),
        },
        indent=2,
    )
)
