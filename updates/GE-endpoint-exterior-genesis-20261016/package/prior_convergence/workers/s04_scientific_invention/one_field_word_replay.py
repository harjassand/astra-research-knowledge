"""Exact finite-word realization from one switched, unknown loss field.

This is a symbolic structural-identification check, not a noisy assay.
"""

import sympy as sp


def main():
    A = sp.Matrix([[-3, 1, 2], [2, -5, 1], [1, 4, -3]])
    D = sp.diag(2, 3, 5)
    b = sp.Matrix([1, 0, 0])
    c = sp.ones(1, 3)
    assert c * A == sp.zeros(1, 3)

    # Accessible by mixed derivatives of on/off pulse durations. The on
    # generator is A-uD, so linear combinations yield words in A and D.
    O = sp.Matrix.vstack(c, c * D, c * D**2)
    B = sp.Matrix.hstack(b, A * b, D * A * b)
    assert O.det() != 0 and B.det() != 0
    H = O * B
    HA = O * A * B
    HD = O * D * B
    # H entries have word length at most 4, HA/HD at most 5 (=2n-1).
    Ah = H.inv() * HA
    Dh = H.inv() * HD
    bh = H.inv() * (O * b)
    ch = c * B

    # Distinct eigenvalues of D give canonical physical state axes.
    eigenpairs = sorted(Dh.eigenvects(), key=lambda item: item[0])
    E0 = sp.Matrix.hstack(*[vecs[0] for _, mult, vecs in eigenpairs])
    gains = list(ch * E0)
    assert all(gain != 0 for gain in gains)
    E = E0 * sp.diag(*[1 / gain for gain in gains])
    Ar = sp.simplify(E.inv() * Ah * E)
    Dr = sp.simplify(E.inv() * Dh * E)
    br = sp.simplify(E.inv() * bh)
    cr = sp.simplify(ch * E)
    assert (Ar, Dr, br, cr) == (A, D, b, c)

    print("rank(H):", H.rank(), "det(H):", H.det())
    print("maximum word length: 5")
    print("recovered A:", Ar.tolist())
    print("recovered D:", Dr.tolist())
    print("recovered b:", list(br))
    print("recovered c:", list(cr))


if __name__ == "__main__":
    main()
