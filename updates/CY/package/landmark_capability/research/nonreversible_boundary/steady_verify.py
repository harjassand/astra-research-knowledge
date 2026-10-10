"""Finite-example check for unbalanced recurring gate steady-state response.

Full eight-state algebra is an independent oracle, not the proposed scalable
implementation. One base-resolvent entry is separately evaluated as a
product of local heat kernels.
"""

import itertools
import numpy as np
from numpy.polynomial.legendre import leggauss


def integrate(fun, lo, hi, order=36):
    x, w = leggauss(order)
    result = 0.0
    while lo < hi:
        right = min(2 * lo, hi)
        mid, half = (lo + right) / 2, (right - lo) / 2
        result += half * sum(weight * fun(mid + half * node)
                             for node, weight in zip(x, w))
        lo = right
    return result


n = 3
a_rate, b_rate = 0.1, 1.2
ql = np.array([[-a_rate, a_rate], [b_rate, -b_rate]])
q0 = sum(np.kron(np.kron(np.eye(2**j), ql), np.eye(2**(n-j-1)))
         for j in range(n))
pl = np.array([b_rate, a_rate]) / (a_rate + b_rate)
pi0 = pl
for _ in range(n-1):
    pi0 = np.kron(pi0, pl)
states = list(itertools.product(range(2), repeat=n))
gates = [states.index((0, 0, 0)), states.index((1, 1, 1))]
e = np.eye(2**n)[:, gates]
gamma = np.array([[-0.7, 0.7], [0.0, 0.0]])
q = q0 + e @ gamma @ e.T
observable = np.array([sum(x) for x in states], dtype=float)


def stationary(generator):
    linear = generator.T.copy()
    linear[-1, :] = 1
    rhs = np.zeros(len(generator))
    rhs[-1] = 1
    return np.linalg.solve(linear, rhs)


pi = stationary(q)
base_value = float(pi0 @ observable)
actual_value = float(pi @ observable)
print('base expected active coordinates', base_value)
print('coupled expected active coordinates', actual_value)
print('unbalanced gate residual', np.linalg.norm(pi0 @ e @ gamma @ e.T, ord=np.inf))


def abel_woodbury(s):
    r0 = np.linalg.solve(s * np.eye(2**n) - q0, np.eye(2**n))
    m = e.T @ r0 @ e
    v = e.T @ r0 @ observable
    small = np.linalg.solve(np.eye(2) - gamma @ m, gamma @ v)
    return base_value + pi0[gates] @ small


for s in [0.1, 0.001, 0.00001]:
    woodbury = abel_woodbury(s)
    direct = s * pi0 @ np.linalg.solve(s * np.eye(2**n) - q, observable)
    print(f's={s}: Abel Woodbury={woodbury:.12f}, full-resolvent={direct:.12f}, '
          f'identity error={abs(woodbury-direct):.3e}, '
          f'stationary error={abs(woodbury-actual_value):.3e}')

# Check one selected base-resolvent entry by the factorized local heat.
eigvals, eigvecs = np.linalg.eig(ql)
invvecs = np.linalg.inv(eigvecs)


def local_heat(t):
    return (eigvecs * np.exp(eigvals * t)[None, :]) @ invvecs


s = 0.3
factorized = integrate(
    lambda t: np.exp(-s*t) * local_heat(t)[0, 1]**n,
    1e-10, 150.0, 40)
direct_entry = np.linalg.solve(s * np.eye(2**n) - q0,
                               np.eye(2**n))[gates[0], gates[1]]
print(f'product free-resolvent entry error={abs(factorized-direct_entry):.3e}')
