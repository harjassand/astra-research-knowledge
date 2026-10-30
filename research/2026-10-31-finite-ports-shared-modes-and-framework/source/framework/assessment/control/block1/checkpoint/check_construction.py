#!/usr/bin/env python3
"""Exact word check and finite-dimensional channel diagnostics.

These diagnostics do not establish the uniform theorem; PROOF.md does.
No files outside this run and the frozen packet are used as scientific data.
"""
from fractions import Fraction as F
from math import factorial, pi, sqrt
import numpy as np


def hermitian_unitary(hamiltonian, time):
    values, vectors = np.linalg.eigh(hamiltonian)
    return (vectors*np.exp(-1j*time*values)) @ vectors.conj().T


# Gaussian rational arithmetic and an exact Pauli-polynomial certificate.
ZERO = (F(0), F(0))
ONE = (F(1), F(0))
IM = (F(0), F(1))


def gadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def gmul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def gpow(a, n):
    ans = ONE
    for _ in range(n):
        ans = gmul(ans, a)
    return ans


PAULI_PRODUCT = {
    ('X', 'Y'): (IM, 'Z'), ('Y', 'Z'): (IM, 'X'),
    ('Z', 'X'): (IM, 'Y'),
    ('Y', 'X'): ((F(0), F(-1)), 'Z'),
    ('Z', 'Y'): ((F(0), F(-1)), 'X'),
    ('X', 'Z'): ((F(0), F(-1)), 'Y'),
}


def pproduct(a, b):
    phase, word = ONE, ''
    for x, y in zip(a, b):
        if x == 'I':
            word += y
        elif y == 'I':
            word += x
        elif x == y:
            word += 'I'
        else:
            z, char = PAULI_PRODUCT[x, y]
            phase = gmul(phase, z)
            word += char
    return phase, word


def polyproduct(a, b, order=3):
    ans = [dict() for _ in range(order+1)]
    for j in range(order+1):
        for k in range(order+1-j):
            for x, cx in a[j].items():
                for y, cy in b[k].items():
                    ph, word = pproduct(x, y)
                    v = gmul(gmul(cx, cy), ph)
                    ans[j+k][word] = gadd(ans[j+k].get(word, ZERO), v)
    return [{k: v for k, v in d.items() if v != ZERO} for d in ans]


def pulsepoly(word, sign):
    ans = []
    for k in range(4):
        c = gpow((F(0), F(-sign)), k)
        c = c[0]/factorial(k), c[1]/factorial(k)
        ans.append({word if k % 2 else 'III': c})
    return ans


# Chronological list. Product of pulse unitaries is in reverse list order.
SCHEDULE = [('B', -1), ('C', -1), ('B', 1), ('C', 1),
            ('A', -1), ('C', -1), ('B', -1), ('C', 1),
            ('B', 1), ('A', 1)]
WORDS = {'A': 'XIX', 'B': 'IXY', 'C': 'YIZ'}


def exact_certificate():
    for sa in [-1, 1]:
        for sb in [-1, 1]:
            signs = {'A': sa, 'B': sb, 'C': sa*sb}
            ans = [{'III': ONE}, {}, {}, {}]
            for j, orient in SCHEDULE:
                ans = polyproduct(pulsepoly(WORDS[j], orient*signs[j]), ans)
            expected = [{'III': ONE}, {}, {}, {'ZXI': (F(0), F(-4))}]
            assert ans == expected, (signs, ans)
    print('EXACT: all four signed words = I - 4i delta^3 ZXI + O(delta^4).')
    print('EXACT: each native handle has balanced signed duration.')
    for j in WORDS:
        assert sum(o for k, o in SCHEDULE if k == j) == 0
    # Integral of |t-5 delta| over the support of each handle, in delta^2.
    weights = {j: F(0) for j in WORDS}
    for k, (j, _) in enumerate(SCHEDULE):
        weights[j] += abs(F(2*k+1, 2)-5)
    assert weights == {'A': F(5), 'B': F(12), 'C': F(8)}
    print('EXACT: midpoint motion weights:', weights)
    print('EXACT: sum squared weights / 2 =', sum(v*v for v in weights.values())/2)


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PM = dict(zip('IXYZ', [I, X, Y, Z]))


def kronword(word):
    ans = np.ones((1, 1), dtype=complex)
    for j in word:
        ans = np.kron(ans, PM[j])
    return ans


def partial_trace_superoperator(data_dim, bath_dim):
    dim = data_dim*bath_dim
    ans = np.zeros((data_dim**2, dim**2), dtype=complex)
    for a in range(dim):
        for b in range(dim):
            if a % bath_dim == b % bath_dim:
                ans[(a//bath_dim)+data_dim*(b//bath_dim), a+dim*b] = 1
    return ans


def channel_bounds(diff, in_dim, out_dim):
    # General upper bound from Hilbert-Schmidt norm on a reference of in_dim.
    upper = sqrt(in_dim*out_dim)*np.linalg.svd(diff, compute_uv=False)[0]
    # Maximally entangled input gives a valid diamond lower bound.
    choi = np.zeros((out_dim*in_dim, out_dim*in_dim), dtype=complex)
    for a in range(in_dim):
        for b in range(in_dim):
            image = diff[:, a+in_dim*b].reshape((out_dim, out_dim), order='F')
            choi[a*out_dim:(a+1)*out_dim, b*out_dim:(b+1)*out_dim] = image
    lower = np.linalg.eigvalsh((choi+choi.conj().T)/2)
    lower = np.sum(np.abs(lower))/in_dim
    return lower, min(2., upper)


def qubit_static_diagnostic():
    handles = {j: kronword(w) for j, w in WORDS.items()}
    Fgate = kronword('ZX')
    target = hermitian_unitary(Fgate, pi/4)
    tr = partial_trace_superoperator(4, 2)
    target_channel = np.kron(target.conj(), target) @ tr
    # All these baths satisfy every local-motion bound with constant <=1.
    for label, bath in [('zero', np.zeros((2, 2))),
                        ('z_half', .5*Z),
                        ('oblique', (X+2*Y+3*Z)/(2*sqrt(14)))]:
        drift = np.kron(np.eye(4), bath)
        print('\nSTATIC BATH:', label)
        print('N delta total_duration lower_diamond upper_diamond upper/delta')
        last_upper = None
        for n in [200, 1600, 12800, 102400, 819200, 6553600, 52428800]:
            delta = (pi/(16*n))**(1/3)
            channel = np.zeros((64, 64), dtype=complex)
            for sa in [-1, 1]:
                for sb in [-1, 1]:
                    signs = dict(A=sa, B=sb, C=sa*sb)
                    u = np.eye(8, dtype=complex)
                    for j, orient in SCHEDULE:
                        u = hermitian_unitary(drift+orient*signs[j]*handles[j], delta) @ u
                    channel += np.kron(u.conj(), u)/4
            final_channel = tr @ np.linalg.matrix_power(channel, n)
            low, up = channel_bounds(final_channel-target_channel, 8, 4)
            print(f'{n:7d} {delta:.8g} {10*n*delta:.8g} '
                  f'{low:.8g} {up:.8g} {up/delta:.8g}')
            if n >= 819200 and last_upper is not None:
                assert up < .7*last_upper, (label, up, last_upper)
            last_upper = up


def moving_spectator_diagnostic():
    """A discontinuous coin-independent bath, with a large spectator term.

    Fifty known-policy-aligned pieces per cycle; their bandwidth increases
    as delta shrinks. This deliberately does not fit a frozen-bath model.
    The analytic local-commutator bound is 2*(.25+.15)=.8 for every Pauli.
    """
    memory_sigma = {'A': np.kron(X, I), 'B': np.kron(Y, I),
                    'C': np.kron(Z, I)}
    data_sigma = {'A': np.kron(X, I), 'B': np.kron(I, X),
                  'C': np.kron(Y, I)}
    handles = {j: np.kron(data_sigma[j], memory_sigma[j]) for j in WORDS}
    tr = partial_trace_superoperator(4, 4)
    print('\nMOVING SPECTATOR: 50 bath pieces per cycle; max local bound <= .8')
    print('omega delta one_cycle_upper upper/delta^4 computed_max_local')
    for omega in [0., 2000.]:
        for delta in [.1, .05, .025, .0125, .00625]:
            baths = []
            max_local = 0.
            for r in range(50):
                n = np.array([np.sin(37*r+.3), np.cos(53*r+.1), np.sin(17*r+.7)])
                n /= np.linalg.norm(n)
                v = np.array([np.cos(19*r+.2), np.sin(29*r+.4), np.cos(11*r+.8)])
                v /= np.linalg.norm(v)
                n_sigma = n[0]*X+n[1]*Y+n[2]*Z
                v_sigma = v[0]*X+v[1]*Y+v[2]*Z
                bath = omega*np.kron(I, Z)+.25*np.kron(n_sigma, I)+.15*np.kron(v_sigma, X)
                baths.append(np.kron(np.eye(4), bath))
                for sigma in memory_sigma.values():
                    max_local = max(max_local, np.linalg.norm(bath@sigma-sigma@bath, 2))
            channel = np.zeros((256, 256), dtype=complex)
            for sa in [-1, 1]:
                for sb in [-1, 1]:
                    signs = dict(A=sa, B=sb, C=sa*sb)
                    u = np.eye(16, dtype=complex)
                    for k, (j, orient) in enumerate(SCHEDULE):
                        for sub in range(5):
                            h = baths[5*k+sub]+orient*signs[j]*handles[j]
                            u = hermitian_unitary(h, delta/5) @ u
                    channel += np.kron(u.conj(), u)/4
            gate = hermitian_unitary(kronword('ZX'), 4*delta**3)
            diff = tr@channel-np.kron(gate.conj(), gate)@tr
            _, upper = channel_bounds(diff, 16, 4)
            print(f'{omega:6g} {delta:.6g} {upper:.8g} {upper/delta**4:.8g} {max_local:.8g}')
            assert max_local <= 1+1e-10
            assert upper <= 10000*delta**4+1e-9


if __name__ == '__main__':
    exact_certificate()
    qubit_static_diagnostic()
    moving_spectator_diagnostic()
