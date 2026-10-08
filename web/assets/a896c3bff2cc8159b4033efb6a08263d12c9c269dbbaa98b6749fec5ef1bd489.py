#!/usr/bin/env python3
"""Exact physical-tensor check for an odd restricted subset (m=5, k=3).

Builds the irreducible 4-dimensional Clifford spinor and the ordinary
three-factor operators A_i=Gamma_i^T x Gamma_i x I,
B_i=Gamma_i^T x I x Gamma_i for i=1,2,3.  It checks the algebra, verifies
that both central signs C=prod B_i and both A-parity sectors occur, and
compares all four physical-sector characteristic polynomials exactly with
the matching canonical k=3 bit-model block.  Each physical block is four
copies of that canonical block.

This is a finite consistency check; the representation proof in REPORT.md is
the general argument.
"""

from __future__ import annotations

import sympy as sp


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)


def kron(*factors: sp.Matrix) -> sp.Matrix:
    out = factors[0]
    for factor in factors[1:]:
        out = sp.kronecker_product(out, factor)
    return out


def sector_charpoly(H: sp.Matrix, projector: sp.Matrix) -> sp.Poly:
    """Recover a block characteristic polynomial from exact power traces."""
    dim = int(sp.trace(projector))
    power_traces = [sp.Integer(dim)]
    power = sp.eye(H.rows)
    for _ in range(dim):
        power = power * H
        power_traces.append(sp.trace(projector * power))

    # Newton identities: e_0=1 and
    # k e_k = sum_{r=1}^k (-1)^(r-1) e_(k-r) Tr(H^r|block).
    elementary = [sp.Integer(1)]
    for k in range(1, dim + 1):
        value = sum(
            (-1) ** (r - 1) * elementary[k - r] * power_traces[r]
            for r in range(1, k + 1)
        ) / k
        elementary.append(sp.simplify(value))

    x = sp.Symbol("x")
    expr = sum(
        (-1) ** k * elementary[k] * x ** (dim - k)
        for k in range(dim + 1)
    )
    return sp.Poly(expr, x)


def main() -> None:
    # Jordan-Wigner irreducible Clifford frame for m=5, d=4.
    gamma = [
        kron(X, I2),
        kron(Y, I2),
        kron(Z, X),
        kron(Z, Y),
        kron(Z, Z),
    ]
    I4 = sp.eye(4)
    for i, Gi in enumerate(gamma):
        assert Gi.H == Gi and Gi * Gi == I4
        for j, Gj in enumerate(gamma):
            assert Gi * Gj + Gj * Gi == 2 * (i == j) * I4

    I64 = sp.eye(64)
    A = [kron(gamma[i].T, gamma[i], I4) for i in range(3)]
    B = [kron(gamma[i].T, I4, gamma[i]) for i in range(3)]
    for i in range(3):
        assert A[i].H == A[i] and A[i] ** 2 == I64
        assert B[i].H == B[i] and B[i] ** 2 == I64
        for j in range(3):
            if i < j:
                assert A[i] * A[j] == A[j] * A[i]
                assert B[i] * B[j] == B[j] * B[i]
            sign = -1 if i != j else 1
            assert A[i] * B[j] == sign * B[j] * A[i]

    C = B[0] * B[1] * B[2]
    D = A[0] * A[1] * A[2]
    for center in (C, D):
        assert center.H == center and center ** 2 == I64
        for op in A + B:
            assert center * op == op * center

    H = sum(A + B, sp.zeros(64))
    for eta in (-1, 1):
        for parity in (-1, 1):
            projector = (I64 + eta * C) * (I64 + parity * D) / 4
            assert projector.H == projector and projector ** 2 == projector
            assert sp.trace(projector) == 16

    # Canonical k=3 model: A_i=Z_i, B'_i=P X_i; original B_i=eta B'_i
    # on the central sector C=eta.  D=prod A_i is the parity label.
    I8 = sp.eye(8)
    xs = [kron(*(X if j == i else I2 for j in range(3))) for i in range(3)]
    zs = [kron(*(Z if j == i else I2 for j in range(3))) for i in range(3)]
    P = xs[0] * xs[1] * xs[2]
    D_bit = zs[0] * zs[1] * zs[2]

    x = sp.Symbol("x")
    full_charpoly = sp.factor(H.charpoly(x).as_expr())
    expected_full = x**24 * (x - 4)**4 * (x - 2)**8 * (x + 2)**8
    expected_full *= (x + 4)**4 * (x**2 - 12)**8
    assert sp.expand(full_charpoly - expected_full) == 0

    for eta in (-1, 1):
        H_bit = sum(zs, sp.zeros(8)) + eta * sum(
            (P * Xi for Xi in xs), sp.zeros(8)
        )
        for parity in (-1, 1):
            physical_projector = (I64 + eta * C) * (I64 + parity * D) / 4
            bit_projector = (I8 + parity * D_bit) / 2
            physical_poly = sector_charpoly(H, physical_projector)
            bit_poly = sector_charpoly(H_bit, bit_projector)
            assert sp.expand(physical_poly.as_expr() - bit_poly.as_expr() ** 4) == 0
            print(
                f"C={eta:+d}, A-parity={parity:+d}, rank=16: "
                f"physical={sp.factor(physical_poly.as_expr())}; "
                f"canonical rank-4 block={sp.factor(bit_poly.as_expr())}"
            )

    assert sp.sqrt(12) < 4
    print("m=5,k=3 physical ordinary-tensor audit: all exact checks PASS")
    print(f"full physical characteristic polynomial: {full_charpoly}")


if __name__ == "__main__":
    main()
