#!/usr/bin/env python3
"""Finite 8x8 check of the quartic coefficient in PROOF Section 4.

Requires pre-existing NumPy. The analytic proof, not these floating-point
residuals, establishes the mathematical claims.
"""
from fractions import Fraction as F
import numpy as np
from checks import comm, primitive_area

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def kron(*matrices):
    answer = np.ones((1, 1), dtype=complex)
    for matrix in matrices:
        answer = np.kron(answer, matrix)
    return answer


def unitary(h, t):
    values, vectors = np.linalg.eigh(h)
    return (vectors*np.exp(-1j*t*values))@vectors.conj().T


def run(word, coefficient):
    current_a, current_b = F(0), F(0)
    bath_signs, cb = [], F(0)
    for handle, sign in word:
        slope_a = F(sign if handle == 'A' else 0)
        mid_a = current_a+slope_a/2
        r = int(mid_a > 0)-int(mid_a < 0)
        assert current_a*(current_a+slope_a) >= 0
        bath_signs.append(r)
        slope_b = F(sign if handle == 'B' else 0)
        cb += r*(current_b+slope_b/2)
        current_a += slope_a
        current_b += slope_b
    ca = primitive_area(word, 'A')
    predicted = ca*ca+cb*cb
    print('segments:', len(word), 'c_A:', ca, 'c_B:', cb,
          'predicted infidelity/delta^4:', predicted)
    handles = {'A': kron(X, I, X), 'B': kron(I, X, Y),
               'C': kron(Y, I, Z)}
    bath = kron(I, I, Z)/2
    f = kron(Z, X, I)
    for delta in [.01, .005, .0025, .00125]:
        fidelity = 0.
        degree = 3 if len(word) == 10 else 5
        remove_target = unitary(f, coefficient*delta**degree)
        for sa in (-1, 1):
            for sb in (-1, 1):
                signs = {'A': sa, 'B': sb, 'C': sa*sb}
                u = np.eye(8, dtype=complex)
                for (j, orient), r in zip(word, bath_signs):
                    u = unitary(r*bath+orient*signs[j]*handles[j], delta)@u
                u = remove_target@u
                tr_data = np.trace(u.reshape(4, 2, 4, 2), axis1=0, axis2=2)
                fidelity += np.vdot(tr_data, tr_data).real/(4*16*2)
        ratio = (1-fidelity)/delta**4
        print(f'delta={delta:.6g} infidelity/delta^4={ratio:.10g} '
              f'ratio/prediction={ratio/float(predicted):.8g}')
        if delta == .00125:
            assert abs(ratio/float(predicted)-1) < .01


if __name__ == '__main__':
    a, b, c = [('A', 1)], [('B', 1)], [('C', 1)]
    cubic = comm(a, comm(b, c))
    fifth = comm(a, comm(a, cubic))
    run(cubic, -4)
    run(fifth, 16)
