"""Exact finite-moment test of two-pulse loss-echo reconstruction.

H and Hshift use derivatives of one continuous loss pulse. K uses the
mixed derivatives of on(t1)-off(tau)-on(t2) survival at zero durations.
"""

import sympy as sp


def reconstruct(A, D, b, u=sp.Integer(1)):
    n = A.rows
    c = sp.ones(1, n)
    assert c * A == sp.zeros(1, n)
    M = A - u * D
    C = sp.Matrix.hstack(*[M**j * b for j in range(n)])
    O = sp.Matrix.vstack(*[c * M**i for i in range(n)])
    H = O * C
    Hshift = O * M * C
    K = O * A * C
    assert H.det() != 0

    Mh = H.inv() * Hshift
    Ah = H.inv() * K
    Dh = sp.simplify((Ah - Mh) / u)
    bh = H.inv() * (O * b)
    ch = c * C

    # Recover physical state axes using D's distinct eigenvalues and the
    # normalization that the measured survival is the sum of state masses.
    eigenpairs = sorted(Dh.eigenvects(), key=lambda item: item[0])
    assert len(eigenpairs) == n
    E0 = sp.Matrix.hstack(*[vecs[0] for _, _, vecs in eigenpairs])
    gains = list(ch * E0)
    assert all(gain != 0 for gain in gains)
    E = E0 * sp.diag(*[1 / gain for gain in gains])
    return (
        sp.simplify(E.inv() * Ah * E),
        sp.simplify(E.inv() * Dh * E),
        sp.simplify(E.inv() * bh),
        sp.simplify(ch * E),
        H.det(),
    )


def sharp_one_pulse_collision():
    s = sp.symbols("s", positive=True)
    c = sp.ones(1, 2)
    b = sp.Matrix([1, 0])
    pairs = [(2, 1, 2, 3), (1, 1, 2, 4)]
    outputs = []
    mixed = []
    for a, r, d1, d2 in pairs:
        A = sp.Matrix([[-a, r], [a, -r]])
        D = sp.diag(d1, d2)
        M = A - D
        outputs.append(sp.factor((c * (s * sp.eye(2) - M).inv() * b)[0]))
        mixed.append((c * M * A * M * b)[0])
    assert outputs == [(s + 6) / (s**2 + 8*s + 14)] * 2
    assert mixed == [10, 8]
    print("identical one-pulse Laplace transform:", outputs[0])
    print("two-pulse mixed third derivatives:", mixed)


def exact_three_state_replay():
    A = sp.Matrix([[-3, 1, 2], [2, -5, 1], [1, 4, -3]])
    D = sp.diag(2, 3, 5)
    b = sp.Matrix([1, 0, 0])
    Ar, Dr, br, cr, detH = reconstruct(A, D, b)
    assert (Ar, Dr, br, cr) == (A, D, b, sp.ones(1, 3))
    print("n=3 Hankel determinant:", detH)
    print("recovered A:", Ar.tolist())
    print("recovered D:", Dr.tolist())
    print("recovered b:", list(br))


if __name__ == "__main__":
    sharp_one_pulse_collision()
    exact_three_state_replay()
