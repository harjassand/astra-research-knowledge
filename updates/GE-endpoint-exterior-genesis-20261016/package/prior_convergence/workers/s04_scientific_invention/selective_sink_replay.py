"""Exact rational replay of the selective-sink reconstruction theorem.

This verifies finite symbolic identities only. It is not an experiment.
"""

import sympy as sp


def moments_at_infinity(f, s, count):
    z = sp.symbols("z")
    series = sp.series(f.subs(s, 1 / z), z, 0, count + 1).removeO()
    return [sp.expand(series).coeff(z, k + 1) for k in range(count)]


def reconstruct(A, b, efficiencies=None, u1=sp.Rational(1), u2=sp.Rational(2)):
    n = A.rows
    if efficiencies is None:
        efficiencies = [sp.Rational(1)] * n
    s = sp.symbols("s")
    e = sp.eye(n)
    one = sp.ones(1, n)
    scaled_alpha = []
    survival = {}
    for i in range(n):
        qs = []
        for u in (u1, u2):
            M = A - u * efficiencies[i] * e[:, i] * e[i, :]
            Y = (one * (s * e - M).inv() * b)[0]
            survival[(i, u)] = sp.factor(Y)
            q = sp.factor((1 - s * Y) / u)
            qs.append(q)
        q1, q2 = qs
        F_i = sp.factor((u2 - u1) * q1 * q2 / (u2 * q2 - u1 * q1))
        target = efficiencies[i] * ((s * e - A).inv() * b)[i]
        assert sp.cancel(F_i - target) == 0
        scaled_alpha.append(F_i)

    scaled_cols = [sp.Matrix([moments_at_infinity(f, s, n + 1)[k]
                              for f in scaled_alpha]) for k in range(n + 1)]
    scaled_V = sp.Matrix.hstack(*scaled_cols[:-1])
    if scaled_V.det() == 0:
        return sp.Integer(0), None, None, survival
    e0 = sp.Matrix([[1] + [0] * (n - 1)])
    inverse_efficiencies = list(e0 * scaled_V.inv())
    recovered_efficiencies = [sp.factor(1 / x) for x in inverse_efficiencies]
    assert recovered_efficiencies == efficiencies
    alpha = [sp.factor(inverse_efficiencies[i] * scaled_alpha[i]) for i in range(n)]

    cols = [sp.Matrix([moments_at_infinity(f, s, n + 1)[k] for f in alpha])
            for k in range(n + 1)]
    V = sp.Matrix.hstack(*cols[:-1])
    W = sp.Matrix.hstack(*cols[1:])
    return V.det(), sp.simplify(W * V.inv()), recovered_efficiencies, survival


def reconstruct_finite_frequencies(A, b, efficiencies, frequencies=(1, 2, 3), u1=1, u2=2):
    """Reconstruct from only 2n*n exact Laplace moments of absorption times."""
    n = A.rows
    assert len(frequencies) == n and len(set(frequencies)) == n
    I = sp.eye(n)
    one = sp.ones(1, n)
    F = sp.zeros(n, n)
    for i in range(n):
        E_i = I[:, i] * I[i, :]
        for j, s in enumerate(frequencies):
            phis = []
            for u in (u1, u2):
                Y = (one * (s * I - A + u * efficiencies[i] * E_i).inv() * b)[0]
                phis.append(sp.factor(1 - s * Y))
            phi1, phi2 = phis
            F[i, j] = sp.factor((u2 - u1) * phi1 * phi2 /
                                  (u1 * u2 * (phi2 - phi1)))

    w = F.T.inv() * sp.Matrix([sp.Rational(1, s) for s in frequencies])
    U = sp.diag(*list(w)) * F
    right = sp.Matrix.hstack(*[s * U[:, j] - b for j, s in enumerate(frequencies)])
    A_hat = sp.simplify(right * U.inv())
    return A_hat, [sp.factor(1 / x) for x in w], F.det(), U.det()


def main():
    A = sp.Matrix([[-3, 3, 1], [2, -4, 4], [1, 1, -5]])
    b = sp.Matrix([1, 0, 0])
    assert sp.ones(1, 3) * A == sp.zeros(1, 3)
    efficiencies = [sp.Rational(2), sp.Rational(3), sp.Rational(5)]
    det, recovered, recovered_efficiencies, _ = reconstruct(A, b, efficiencies)
    print("fixture A:", A.tolist())
    print("Krylov determinant:", det)
    print("recovered A:", recovered.tolist())
    print("recovered sink efficiencies:", recovered_efficiencies)
    assert recovered == A

    finite_A, finite_eff, det_F, det_U = reconstruct_finite_frequencies(
        A, b, efficiencies)
    assert finite_A == A and finite_eff == efficiencies
    print("finite-frequency recovered A:", finite_A.tolist())
    print("finite-frequency recovered efficiencies:", finite_eff)
    print("finite-frequency det F:", det_F)

    # Symmetric branches have an unexcited antisymmetric mode: no theorem.
    B = sp.Matrix([[-2, 1, 1], [1, -1, 0], [1, 0, -1]])
    det_b, rec_b, rec_eff_b, _ = reconstruct(B, b, efficiencies)
    assert det_b == 0 and rec_b is None
    print("symmetric-branch Krylov determinant:", det_b)

    # A spatially uniform removal rate adds -h I and keeps global survival
    # independent of A: Y_h(s)=1/(s+h) for *every* conservative A.
    s, h = sp.symbols("s h", positive=True)
    e = sp.eye(3)
    Y_uniform = sp.factor((sp.ones(1, 3) * (s * e - (A - h * e)).inv() * b)[0])
    assert sp.cancel(Y_uniform - 1 / (s + h)) == 0
    print("uniform-sink survival transform:", Y_uniform)


if __name__ == "__main__":
    main()
