#!/usr/bin/env python3
"""Exact drift-profile construction and finite channel barrier diagnostics.

Uses the retained first-tranche exact Gaussian-rational Pauli arithmetic.
The analytic theorem is in PROOF.md; numerical outputs are diagnostics.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial, pi, exp, sqrt
from pathlib import Path
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import check_construction as native
import numpy as np


def inverse(word):
    return [(j, -s) for j, s in reversed(word)]


def commword(u, v):
    return inverse(v)+inverse(u)+v+u


def degree_five_word():
    a, b, c = [('A', 1)], [('B', 1)], [('C', 1)]
    ell = commword(a, commword(b, c))
    word = commword(a, commword(a, ell))
    # Set the leading coefficient to -16 i F, matching the target sign.
    return [(j, -s if j == 'C' else s) for j, s in word]


def exact_word_certificate(word):
    for sa, sb, sc in product([-1, 1], repeat=3):
        signs = dict(A=sa, B=sb, C=sc)
        ans = [{'III': native.ONE}]+[{} for _ in range(5)]
        for j, orient in word:
            pulse = []
            for k in range(6):
                z = native.gpow((F(0), F(-orient*signs[j])), k)
                z = z[0]/factorial(k), z[1]/factorial(k)
                pulse.append({native.WORDS[j] if k % 2 else 'III': z})
            ans = native.polyproduct(pulse, ans, order=5)
        expected = [{'III': native.ONE}]+[{} for _ in range(4)]
        expected += [{'ZXI': (F(0), F(-16*sa*sb*sc))}]
        assert ans == expected, ans
    print('EXACT: 46-segment native word has leading -16 i sA*sB*sC delta^5 F.')
    print('EXACT: degrees 1,2,3,4 vanish for all eight global native sign variants.')


# target handle, bath rotation axis, other affected handle, resulting Q
SPEC = [('A', 'Y', 'C', 'XIZ'), ('A', 'Z', 'B', 'XIY'),
        ('B', 'X', 'C', 'IXZ'), ('B', 'Z', 'A', 'IXX'),
        ('C', 'X', 'B', 'YIY'), ('C', 'Y', 'A', 'YIX')]


def profiles(word):
    # Average primitive on each half-segment. Half-cell width = 1/2.
    primitives = {j: [] for j in 'ABC'}
    current = {j: F(0) for j in 'ABC'}
    for handle, orient in word:
        for _ in range(2):
            for j in 'ABC':
                slope = orient if j == handle else 0
                primitives[j].append(current[j]+F(slope, 4))
                current[j] += F(slope, 2)
    assert all(value == 0 for value in current.values())
    size = 2*len(word)
    out = []
    for target, axis, other, qword in SPEC:
        x, y = primitives[target], primitives[other]
        sy, syy, sx, sxy = sum(y), sum(z*z for z in y), sum(x), sum(a*b for a, b in zip(x, y))
        determinant = size*syy-sy*sy
        intercept = (sx*syy-sxy*sy)/determinant
        slope = (size*sxy-sy*sx)/determinant
        residual = [a-intercept-slope*b for a, b in zip(x, y)]
        maxr = max(abs(r) for r in residual)
        assert maxr > 0
        h = [r/(2*maxr) for r in residual]
        mu = sum(a*b for a, b in zip(h, x))/2
        assert sum(h) == 0
        assert sum(a*b for a, b in zip(h, y)) == 0
        assert max(abs(a) for a in h) == F(1, 2)
        assert mu == sum(r*r for r in residual)/(4*maxr) > 0
        out.append((target, axis, qword, h, mu))
        print('EXACT profile:', target, 'bath axis', axis, 'noise', qword, 'mu=', mu)
    return out


def exact_noise_commutant():
    common = []
    qwords = [row[3] for row in SPEC]
    for letters in product('IXYZ', repeat=3):
        label = ''.join(letters)
        if all(native.pproduct(q, label) == native.pproduct(label, q) for q in qwords):
            common.append(label)
    assert common == ['III', 'IXI'], common
    print('EXACT: common Pauli commutant of the six noise operators:', common)


def diagnostic(word, prof):
    handles = {j: native.kronword(w) for j, w in native.WORDS.items()}
    f = native.kronword('ZXI')
    # Exact invariant space is span{I,X2}; use its Pauli orthocomplement.
    basis = []
    for letters in product('IXYZ', repeat=3):
        label = ''.join(letters)
        if label not in ('III', 'IXI'):
            basis.append(native.kronword(label).reshape(-1, order='F')/sqrt(8))
    basis = np.stack(basis, axis=1)
    vf = basis.conj().T @ f.reshape(-1, order='F')
    print('\nNUMERIC: gain triple (1,1,1); independent fresh bath labels each cycle')
    print('delta N norm_on_complement (1-norm)/delta^4 F_expectation trace_error_lower')
    for delta in [.1, .05, .025, .0125, .00625]:
        channel = np.zeros((64, 64), dtype=complex)
        for sa, sb in product([-1, 1], repeat=2):
            signs = dict(A=sa, B=sb, C=sa*sb)
            for _, axis, _, h, _ in prof:
                bath_axis = np.kron(np.eye(4), native.PM[axis])
                for bath_sign in [-1, 1]:
                    u = np.eye(8, dtype=complex)
                    for k, (j, orient) in enumerate(word):
                        for half in range(2):
                            ham = orient*signs[j]*handles[j]+bath_sign*float(h[2*k+half])*bath_axis
                            u = native.hermitian_unitary(ham, delta/2) @ u
                    channel += np.kron(u.conj(), u)/48
        restricted = basis.conj().T @ channel @ basis
        norm = np.linalg.svd(restricted, compute_uv=False)[0]
        n = max(1, round(pi/(64*delta**5)))
        expectation = (vf.conj() @ np.linalg.matrix_power(restricted, n) @ vf/8).real
        print(f'{delta:.7g} {n:d} {norm:.12g} {(1-norm)/delta**4:.8g} '
              f'{expectation:.8g} {1-expectation:.8g}')
        assert norm < 1
        assert 1-expectation > .1


if __name__ == '__main__':
    word = degree_five_word()
    assert len(word) == 46
    exact_word_certificate(word)
    prof = profiles(word)
    exact_noise_commutant()
    min_mu = min(row[-1] for row in prof)
    beta = F(8, 3)*min_mu**2
    gamma = min_mu**2/3
    d = len(word)
    c3 = exp(1)*(5*d)**3/6
    delta0 = min(1/(5*d), sqrt(float(beta))/(4*c3), (4/float(beta))**.25)
    print('minimum mu:', min_mu)
    print('rigorous contraction gamma = min_mu^2/3:', gamma)
    print('conservative sufficient delta_0:', delta0)
    diagnostic(word, prof)
