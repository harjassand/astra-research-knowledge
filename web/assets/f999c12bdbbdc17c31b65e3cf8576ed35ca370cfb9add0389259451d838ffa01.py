#!/usr/bin/env python3
"""Exact Spin(5) spinor/ququart vector-bivector support checks."""

from __future__ import annotations

import sympy as sp


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)


def kron(*ops: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(*ops)


def main() -> None:
    gamma = [
        kron(X, I2),
        kron(Y, I2),
        kron(Z, X),
        kron(Z, Y),
        kron(Z, Z),
    ]
    ident4 = sp.eye(4)
    assert all(g.H == g and g**2 == ident4 for g in gamma)
    for i, gi in enumerate(gamma):
        for j, gj in enumerate(gamma):
            assert gi * gj + gj * gi == 2 * int(i == j) * ident4

    bivectors = [
        sp.simplify(sp.I * gamma[i] * gamma[j])
        for i in range(5)
        for j in range(i + 1, 5)
    ]
    frame = gamma + bivectors
    assert len(frame) == 15
    assert all(sp.trace(a) == 0 for a in frame)
    assert all(
        sp.simplify(sp.trace(a * b) / 4) == int(i == j)
        for i, a in enumerate(frame)
        for j, b in enumerate(frame)
    )

    # Fierz identity on Sym^2(C^4): sum_i Gamma_i tensor Gamma_i = I.
    swap = sp.zeros(16)
    for i in range(4):
        for j in range(4):
            swap[4 * i + j, 4 * j + i] = 1
    psym = (sp.eye(16) + swap) / 2
    fierz = sum((kron(g, g) for g in gamma), sp.zeros(16))
    assert fierz * psym == psym
    assert psym * fierz == psym

    def star(operators: list[sp.Matrix]) -> sp.Matrix:
        out = sp.zeros(64)
        for op in operators:
            out += kron(op.T, op, ident4) + kron(op.T, ident4, op)
        return out

    h_vector = star(gamma)
    h_bivector = star(bivectors)
    x = sp.symbols("x")
    vector_charpoly = sp.factor(h_vector.charpoly(x).as_expr())
    bivector_charpoly = sp.factor(h_bivector.charpoly(x).as_expr())
    assert vector_charpoly == x**16 * (x - 6)**4 * (x - 2)**20 * (x + 4)**16 * (x**2 - 20)**4
    assert bivector_charpoly == x**4 * (x - 12)**4 * (x - 8)**4 * (x - 2)**16 * (x + 2)**16 * (x + 4)**20
    vector_spec = h_vector.eigenvals()
    bivector_spec = h_bivector.eigenvals()
    assert max(vector_spec) == 6
    assert bivector_spec == {
        sp.Integer(12): 4,
        sp.Integer(8): 4,
        sp.Integer(2): 16,
        sp.Integer(-2): 16,
        sp.Integer(-4): 20,
        sp.Integer(0): 4,
    }
    print("Clifford vector+bivector frame is tau-HS orthonormal: PASS")
    print("Sym^2 spinor Fierz identity, sum Gamma_i⊗Gamma_i=I: PASS")
    print(f"vector star characteristic polynomial: {vector_charpoly}")
    print("vector star lambda_max=6: PASS")
    print(f"bivector star characteristic polynomial: {bivector_charpoly}")
    print(f"bivector star exact spectrum: {bivector_spec}")
    print("bivector star lambda_max=12: PASS")


if __name__ == "__main__":
    main()
