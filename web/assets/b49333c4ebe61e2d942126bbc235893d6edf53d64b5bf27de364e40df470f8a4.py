#!/usr/bin/env python3
"""Exact small-dimensional checks for the symplectic EB-Dirichlet corollary.

The script checks rational linear-map identities only. It does not prove PPT,
non-entanglement-breaking, separability, or the imported EB-square theorem.
"""
import sympy as sp


def vec(A):
    return sp.Matrix(A).reshape(A.rows * A.cols, 1)


def superoperator(fn, d):
    cols = []
    for i in range(d):
        for j in range(d):
            E = sp.zeros(d)
            E[i, j] = 1
            cols.append(vec(fn(E)))
    return sp.Matrix.hstack(*cols)


def main():
    for d in (4, 6, 8):
        h = d // 2
        V = sp.zeros(d)
        for i in range(h):
            V[i, h + i] = 1
            V[h + i, i] = -1
        I = sp.eye(d)
        assert V.T == -V and V.T * V == I and V * V == -I

        def theta(X):
            return V * X.T * V.T

        def replacer(X):
            return sp.trace(X) * I

        S_theta = superoperator(theta, d)
        S_r = superoperator(replacer, d)
        S_id = sp.eye(d * d)
        S_phi = (S_r + S_id + S_theta) / (d + 2)
        S_square = S_phi * S_phi
        residual = 2 * (S_id - S_phi) - (S_id - S_square)

        assert S_theta * S_theta == S_id
        assert S_theta.T == S_theta
        assert S_r.T == S_r
        assert S_phi.T == S_phi
        assert residual == (S_id - S_phi).T * (S_id - S_phi)

        vI = vec(I)
        trace_row = vI.T
        assert S_phi * vI == vI
        assert trace_row * S_phi == trace_row

        eigenvalues = S_phi.eigenvals()
        expected = {sp.Integer(1), sp.Rational(2, d + 2), sp.Integer(0)}
        assert set(eigenvalues) == expected
        assert all(ev.is_nonnegative for ev in eigenvalues)
        print(f"d={d}: exact identities pass; spectrum={eigenvalues}")

    print("PASS: exact rational checks; imported EB/PPT claims remain unverified here.")


if __name__ == "__main__":
    main()
