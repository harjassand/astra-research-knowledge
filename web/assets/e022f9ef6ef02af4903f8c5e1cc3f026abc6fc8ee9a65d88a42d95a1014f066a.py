"""Exact SymPy audit of a non-Weyl qutrit self-compatible positive channel.

The original cubic-phase channel is not positive as a Hilbert--Schmidt
operator. Its square is: applying the original channel to both outputs of its
explicit symmetric extension gives a legal extension of the square. This
script checks the exact transfer spectrum used by the MUB EB comparator.
"""
import sympy as s
from itertools import permutations

d = 3
w = (-1 + s.sqrt(-3)) / 2


def idx(i, a, b):
    return 9 * i + 3 * a + b


def cubic_vector(conjugate=False):
    v = s.zeros(27, 1)
    for i in range(d):
        for a in range(d):
            b = (-i - a) % d
            phase = w ** (i * a * b)
            v[idx(i, a, b)] = s.conjugate(phase) / 3 if conjugate else phase / 3
    return v


def partial_trace_one(rho, traced):
    """Partial trace of a 3-qutrit matrix; retain the other two in order."""
    keep = [j for j in range(3) if j != traced]
    out = s.zeros(9)
    for r in range(27):
        rr = [(r // 9) % 3, (r // 3) % 3, r % 3]
        for c in range(27):
            cc = [(c // 9) % 3, (c // 3) % 3, c % 3]
            if rr[traced] == cc[traced]:
                ir = 3 * rr[keep[0]] + rr[keep[1]]
                ic = 3 * cc[keep[0]] + cc[keep[1]]
                out[ir, ic] += rho[r, c]
    return out


def partial_trace_two(rho, keep):
    """Partial trace down to one qutrit."""
    traced = [j for j in range(3) if j != keep]
    out = s.zeros(3)
    for r in range(27):
        rr = [(r // 9) % 3, (r // 3) % 3, r % 3]
        for c in range(27):
            cc = [(c // 9) % 3, (c // 3) % 3, c % 3]
            if all(rr[j] == cc[j] for j in traced):
                out[rr[keep], cc[keep]] += rho[r, c]
    return out


def gell_mann_basis():
    out = []
    for i in range(d):
        for j in range(i + 1, d):
            A = s.zeros(d)
            A[i, j] = A[j, i] = 1
            B = s.zeros(d)
            B[i, j], B[j, i] = -s.I, s.I
            out.extend([A * s.sqrt(s.Rational(3, 2)), B * s.sqrt(s.Rational(3, 2))])
    for k in range(1, d):
        A = s.zeros(d)
        for i in range(k):
            A[i, i] = 1
        A[k, k] = -k
        out.append(A * s.sqrt(s.Rational(3, k * (k + 1))))
    return out


def main():
    p, q = cubic_vector(), cubic_vector(conjugate=True)
    assert s.simplify((p.conjugate().T * p)[0]) == 1
    assert s.simplify((q.conjugate().T * q)[0]) == 1
    for i in range(3):
        for a in range(3):
            for b in range(3):
                for perm in permutations((i, a, b)):
                    assert s.simplify(p[idx(i, a, b)] - p[idx(*perm)]) == 0
                    assert s.simplify(q[idx(i, a, b)] - q[idx(*perm)]) == 0
    Omega = ((p * p.conjugate().T + q * q.conjugate().T) / 2).applyfunc(s.simplify)
    assert s.trace(Omega) == 1

    # The tensor is fully permutation symmetric, so every one-system marginal
    # is I/3 and every pair marginal is the same Choi state J_Phi.
    marginals = [partial_trace_two(Omega, j) for j in range(3)]
    assert all(M == s.eye(3) / 3 for M in marginals)
    pairs = [partial_trace_one(Omega, j) for j in range(3)]
    assert pairs[0] == pairs[1] == pairs[2]

    J = pairs[2]  # retain reference and first receiver

    def Phi(A):
        out = s.zeros(3)
        for i in range(3):
            for j in range(3):
                for a in range(3):
                    for b in range(3):
                        out[a, b] += 3 * J[3 * i + a, 3 * j + b] * A[i, j]
        return out.applyfunc(s.simplify)

    basis = gell_mann_basis()
    T = s.Matrix([
        [s.simplify(s.trace(A.conjugate().T * Phi(B)) / 3) for B in basis]
        for A in basis
    ])
    expected = s.Matrix([
        [s.Rational(1, 3), 0, s.Rational(1, 3), 0, -s.Rational(1, 6), 0, 0, 0],
        [0, -s.Rational(1, 3), 0, s.Rational(1, 3), 0, s.Rational(1, 6), 0, 0],
        [s.Rational(1, 3), 0, s.Rational(1, 3), 0, -s.Rational(1, 6), 0, 0, 0],
        [0, s.Rational(1, 3), 0, -s.Rational(1, 3), 0, -s.Rational(1, 6), 0, 0],
        [-s.Rational(1, 6), 0, -s.Rational(1, 6), 0, s.Rational(1, 3), 0, 0, 0],
        [0, s.Rational(1, 6), 0, -s.Rational(1, 6), 0, -s.Rational(1, 3), 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert T == expected
    assert T == T.T
    assert T.eigenvals() == {
        s.Rational(1, 2) + s.sqrt(3) / 6: 1,
        s.Rational(1, 2) - s.sqrt(3) / 6: 1,
        -s.Rational(1, 2) - s.sqrt(3) / 6: 1,
        -s.Rational(1, 2) + s.sqrt(3) / 6: 1,
        s.Integer(0): 4,
    }
    T2 = T * T
    assert T2.eigenvals() == {
        s.Rational(1, 3) + s.sqrt(3) / 6: 2,
        s.Rational(1, 3) - s.sqrt(3) / 6: 2,
        s.Integer(0): 4,
    }

    # A complete set of four qutrit MUBs gives the canonical EB comparator
    # Psi=(1/4) sum_L Delta_L = (1/4)I on traceless Hermitians. The strict
    # inequality below is exactly 7 > 4*sqrt(3), i.e. 49 > 48.
    lambda_max = s.Rational(1, 3) + s.sqrt(3) / 6
    gap = s.simplify(s.Rational(1, 4) - (2 * lambda_max - 1))
    assert gap == (7 - 4 * s.sqrt(3)) / 12
    assert gap > 0

    print("exact cubic Choi trace", s.trace(J))
    print("exact transfer matrix", T)
    print("Phi eigenvalues", T.eigenvals())
    print("Phi^2 eigenvalues", T2.eigenvals())
    print("MUB-comparator margin", gap)


if __name__ == "__main__":
    main()
