"""Finite output-channel diagnostics for the exact high-degree-word barrier.

Distances below come from two orthogonal data inputs with maximally mixed
memory. The asymptotic bound in DERIVATION.md is analytic, not fitted here.
"""

from itertools import product
from math import pi
import numpy as np
from high_order_barrier import high_word, adversary

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1., -1.]).astype(complex)
PAULIS = {'A': np.kron(np.kron(X, I), X),
          'B': np.kron(np.kron(I, X), Y),
          'C': np.kron(np.kron(Y, I), Z)}
ZM = np.kron(np.eye(4), Z)
QDATA = np.kron(Z, Z)
DELTA_INPUT = np.kron(QDATA, I)/4  # rho_plus-rho_minus; trace norm exactly two


def unitary(h, t):
    values, vectors = np.linalg.eigh(h)
    return (vectors*np.exp(-1j*t*values)) @ vectors.conj().T


def trace_memory(matrix):
    a = matrix.reshape(4, 2, 4, 2)
    return np.trace(a, axis1=1, axis2=3)


def channel(tau, randomized_bath):
    word = high_word()
    hs, _, _ = adversary(word)
    us = []
    for a, b in product((-1, 1), repeat=2):
        signs = {'A': a, 'B': b, 'C': a*b}
        for eta in ((-1, 1) if randomized_bath else (1,)):
            u = np.eye(8, dtype=complex)
            for (handle, orientation), h in zip(word, hs):
                hamiltonian = orientation*signs[handle]*PAULIS[handle] + eta*float(h)*ZM
                u = unitary(hamiltonian, tau) @ u
            us.append(u)
    return sum(np.kron(u.conj(), u) for u in us)/len(us)


def main():
    print('46-pulse degree-five word; 16*N*tau^5=pi/4.')
    print('rho_+/-=(I +/- Z1Z2)/4, tensor I_M/2; target outputs are orthogonal.')
    print('Reported 1-distance/2 is a lower bound on at least one output trace-norm error.')
    print('N tau private+bath average lower bound fixed_eta=+1 lower bound')
    for n in (1000, 100000, 10000000, 1000000000):
        tau = (pi/(64*n))**(1/5)
        lower_bounds = []
        for randomized in (True, False):
            cycle = channel(tau, randomized)
            evolved = np.linalg.matrix_power(cycle, n) @ DELTA_INPUT.reshape(-1, order='F')
            output = trace_memory(evolved.reshape(8, 8, order='F'))
            output = (output+output.conj().T)/2
            distance = np.sum(np.abs(np.linalg.eigvalsh(output)))
            lower_bounds.append(1-distance/2)
        print(n, f'{tau:.10g}', *(f'{value:.10g}' for value in lower_bounds))
    print('Floating-point diagnostics only. Matrix-power rounding grows with N.')
    print('The randomized-bath bound implies existence of a fixed admitted bath trajectory;')
    print('the fixed_eta=+1 column additionally tests one deterministic periodic trajectory.')


if __name__ == '__main__':
    main()
