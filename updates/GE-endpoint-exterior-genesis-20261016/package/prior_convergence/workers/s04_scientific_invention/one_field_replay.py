"""Exact checks for one unknown, nonselective state-dependent loss field.

The proof in REPORT.md is general; these are finite symbolic checks only.
"""

import sympy as sp


def two_state_check():
    a, b, d1, d2, s, u = sp.symbols("a b d1 d2 s u", positive=True)
    A = sp.Matrix([[-a, b], [a, -b]])
    D = sp.diag(d1, d2)
    y = sp.factor((sp.ones(1, 2) * (s * sp.eye(2) - A + u * D).inv()
                   * sp.Matrix([1, 0]))[0])
    expected = (s + a + b + u * d2) / (
        s**2 + s*(a+b+u*(d1+d2)) + u*(a*d2+b*d1) + u**2*d1*d2)
    assert sp.cancel(y - expected) == 0
    assert sp.cancel(y.subs(d2, d1) - 1/(s+u*d1)) == 0
    print("n=2 exact transfer:", y)
    print("n=2 uniform-loss degeneracy: 1/(s+u*d1)")


def three_state_constant_field_check():
    A = sp.Matrix([[-3, 1, 2], [2, -5, 1], [1, 4, -3]])
    D = sp.diag(2, 3, 5)
    n = 3
    b = sp.Matrix([1, 0, 0])
    c = sp.ones(1, n)
    I = sp.eye(n)
    points = [(s, u) for s in (1, 2, 3) for u in (1, 2, 4)]
    edges = [(i, j) for j in range(n) for i in range(n) if i != j]
    J = sp.zeros(len(points), 9)
    for row, (s, u) in enumerate(points):
        R = (s * I - A + u * D).inv()
        for col, (i, j) in enumerate(edges):
            # The physical rate a_ij changes A by (e_i-e_j)e_j^T.
            J[row, col] = (c * R * (I[:, i] - I[:, j]))[0] * (R * b)[j]
        for i in range(n):
            J[row, 6 + i] = -u * (c * R * I[:, i])[0] * (R * b)[i]
    det = J.det()
    assert det != 0
    print("n=3 exact finite-design Jacobian rank:", J.rank())
    print("n=3 exact finite-design Jacobian determinant:", det)

    # A and D can be simultaneously permuted without changing the data,
    # provided the known initial state is fixed.
    P = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    for s, u in points:
        original = (c * (s * I - A + u * D).inv() * b)[0]
        relabeled = (c * (s * I - P*A*P.T + u*P*D*P.T).inv() * b)[0]
        assert sp.cancel(original - relabeled) == 0
    print("permutation ambiguity: states 2 and 3 remain unlabelled")


if __name__ == "__main__":
    two_state_check()
    three_state_constant_field_check()
