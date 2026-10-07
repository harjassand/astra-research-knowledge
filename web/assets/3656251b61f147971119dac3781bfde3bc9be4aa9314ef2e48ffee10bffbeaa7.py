"""Finite-difference diagnostic for the spin-1 local kernel identities.

This checks only small matrix fixtures. It is not evidence for the all-N
stopped-diffusion theorem or its tail bounds.
"""
from __future__ import annotations

import numpy as np


SQRT2 = np.sqrt(2.0)
S_PLUS = np.array([[0, SQRT2, 0], [0, 0, SQRT2], [0, 0, 0]], complex)
S_MINUS = S_PLUS.conj().T
SX = (S_PLUS + S_MINUS) / 2
SY = (S_PLUS - S_MINUS) / (2j)
SZ = np.diag([1.0, 0.0, -1.0]).astype(complex)
SPIN = np.array([SX, SY, SZ])
ID3 = np.eye(3, dtype=complex)
EPS = 2.0e-4


def exp_hermitian(a: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh(a)
    return (vecs * np.exp(vals)) @ vecs.conj().T


def tau(y: np.ndarray) -> np.ndarray:
    a = np.tensordot(y, SPIN, axes=1)
    e = exp_hermitian(a)
    return e / np.trace(e)


def kernel(y: np.ndarray, nsites: int) -> np.ndarray:
    result = tau(y)
    for _ in range(nsites - 1):
        result = np.kron(result, tau(y))
    return result


def generators(n: np.ndarray, nsites: int) -> tuple[np.ndarray, np.ndarray]:
    sn = np.tensordot(n, SPIN, axes=1)
    dim = 3**nsites
    total = np.zeros((dim, dim), complex)
    for site in range(nsites):
        factors = [ID3] * nsites
        factors[site] = sn
        term = factors[0]
        for factor in factors[1:]:
            term = np.kron(term, factor)
        total += term
    return total, total @ total


def radial_m(y: np.ndarray) -> tuple[float, float]:
    r = float(np.linalg.norm(y))
    if r < 1.0e-10:
        return 2.0 / 3.0, 4.0 / 3.0
    m = 2.0 * np.sinh(r) / (1.0 + 2.0 * np.cosh(r))
    return m, 2.0 * m / r


def vfield(n: np.ndarray, y: np.ndarray) -> np.ndarray:
    r = float(np.linalg.norm(y))
    if r < 1.0e-7:
        return 2.0 * n
    u = float(np.dot(n, y))
    return (2.0 * u / (r * r)) * y + r / np.tanh(r / 2.0) * (n - (u / (r * r)) * y)


def directional(fun, y: np.ndarray, direction: np.ndarray) -> np.ndarray:
    return (fun(y + EPS * direction) - fun(y - EPS * direction)) / (2 * EPS)


def check(nsites: int, n: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    kfun = lambda z: kernel(z, nsites)
    jn, jn2 = generators(n, nsites)
    k = kfun(y)
    r = float(np.linalg.norm(y))
    u = float(np.dot(n, y))
    _, g = radial_m(y)
    beta = nsites * g * u

    def bop(fun, z):
        return nsites * radial_m(z)[1] * float(np.dot(n, z)) * fun(z) + directional(fun, z, vfield(n, z))

    def rop(fun, z):
        return directional(fun, z, np.cross(n, z))

    b_k = bop(kfun, y)
    r_k = rop(kfun, y)
    first_b = np.linalg.norm((jn @ k + k @ jn) - b_k) / max(1.0, np.linalg.norm(b_k))
    first_r = np.linalg.norm((jn @ k - k @ jn) - 1j * r_k) / max(1.0, np.linalg.norm(r_k))

    b2_k = bop(lambda z: bop(kfun, z), y)
    r2_k = rop(lambda z: rop(kfun, z), y)
    lhs = (jn2 @ k + k @ jn2) / 2.0
    rhs = (b2_k - r2_k) / 4.0
    second = np.linalg.norm(lhs - rhs) / max(1.0, np.linalg.norm(lhs))
    return float(max(first_b, first_r)), float(second)


def main() -> None:
    n = np.array([0.31, -0.47, 0.825], float)
    n /= np.linalg.norm(n)
    points = [np.array([0.23, -0.31, 0.17]), np.array([-0.41, 0.12, 0.29])]
    for nsites in (1, 2):
        for y in points:
            first, second = check(nsites, n, y)
            print(f"spin1 N={nsites} y={y.tolist()} first={first:.3e} second={second:.3e}")
            assert first < 2.0e-7
            assert second < 2.0e-6


if __name__ == "__main__":
    main()
