#!/usr/bin/env python3
"""Exact small-k checks for the Clifford-vector star SOS and qubit control."""

from __future__ import annotations

import sympy as sp


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
PAULI = (X, Y, Z)


def kron_all(*factors: sp.Matrix) -> sp.Matrix:
    out = factors[0]
    for factor in factors[1:]:
        out = sp.kronecker_product(out, factor)
    return out


def embedded(k: int, site: int, op: sp.Matrix) -> sp.Matrix:
    return kron_all(*(op if j == site else I2 for j in range(k)))


def check_canonical_sos(k: int, eps: int) -> None:
    xs = [embedded(k, j, X) for j in range(k)]
    ys = [embedded(k, j, Y) for j in range(k)]
    zs = [embedded(k, j, Z) for j in range(k)]
    ident = sp.eye(2**k)
    parity = sp.eye(2**k)
    for x in xs:
        parity = parity * x
    jx = sum(xs, sp.zeros(2**k))
    jy = sum(ys, sp.zeros(2**k))
    jz = sum(zs, sp.zeros(2**k))
    jx, jy, jz = jx / 2, jy / 2, jz / 2

    direct = sum(zs, sp.zeros(2**k))
    for i in range(k):
        string = sp.eye(2**k)
        for j, x in enumerate(xs):
            if i != j:
                string = string * x
        direct += eps * string
    compact = 2 * (jz + eps * parity * jx)
    assert direct == compact

    casimir = jx**2 + jy**2 + jz**2
    c = jy + eps * sp.I * parity / 2
    lhs = compact**2 / 4
    rhs = casimir + ident / 4 - c * c.conjugate().T
    assert lhs == rhs
    assert (parity * jx - jx * parity) == sp.zeros(2**k)
    assert (parity * jy + jy * parity) == sp.zeros(2**k)
    assert (parity * jz + jz * parity) == sp.zeros(2**k)


def check_qubit_characteristic() -> None:
    a, b, c = sp.symbols("a b c", real=True)
    x = sp.Symbol("x")
    weights = (a, b, c)
    ident = sp.eye(2)
    star = sp.zeros(8)
    for weight, op in zip(weights, PAULI):
        star += weight * (
            kron_all(op.T, op, ident) + kron_all(op.T, ident, op)
        )
    observed = sp.factor(star.charpoly(x).as_expr())
    expected = x**2 * (x**3 - 4 * (a**2 + b**2 + c**2) * x - 16 * a * b * c) ** 2
    assert sp.expand(observed - expected) == 0


def main() -> None:
    for k in range(1, 6):
        for eps in (-1, 1):
            check_canonical_sos(k, eps)
        print(f"k={k}: both twist signs and SOS identity PASS")
    check_qubit_characteristic()
    print("qubit anisotropic 8x8 characteristic polynomial PASS")


if __name__ == "__main__":
    main()
