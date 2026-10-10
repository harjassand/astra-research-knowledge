"""Numerical identity check for the nonreversible boundary/contour formulas.

This is deliberately not a certified implementation or a complexity test.
"""

import itertools
import numpy as np
from numpy.polynomial.legendre import leggauss
from mpmath import matrix, expm, mp


def directed_cycle(rates):
    d = len(rates)
    q = np.zeros((d, d), dtype=float)
    for j, rate in enumerate(rates):
        q[j, j] = -rate
        q[j, (j + 1) % d] = rate
    return q


q1 = directed_cycle([2.3, 0.7, 1.1])
q2 = directed_cycle([0.6, 1.5, 0.9])
local = [q1, q2]
q = np.kron(q1, np.eye(3)) + np.kron(np.eye(3), q2)
mu1 = np.array([0.15, 0.65, 0.20])
mu2 = np.array([0.40, 0.10, 0.50])
mu = np.kron(mu1, mu2)
states = list(itertools.product(range(3), repeat=2))
target_states = [(0, 0), (2, 1)]
target = [states.index(x) for x in target_states]
comp = [j for j in range(9) if j not in target]
eigs = [np.linalg.eig(qi.astype(complex)) for qi in local]


def local_exp(i, z):
    vals, vecs = eigs[i]
    return (vecs * np.exp(vals * z)[None, :]) @ np.linalg.inv(vecs)


def dyadic_gauss(fun, lower, upper, order=40):
    nodes, weights = leggauss(order)
    total = 0j
    left = lower
    while left < upper:
        right = min(2 * left, upper)
        mid = (left + right) / 2
        half = (right - left) / 2
        total += half * sum(w * fun(mid + half * x) for x, w in zip(nodes, weights))
        left = right
    return total


d = 3
c = 1 / (2 * d) + 1j
u = 1 + 1j / d


def inner_entry(rho, a, b):
    s = -c * rho

    def integrand(v):
        e0, e1 = local_exp(0, u * v), local_exp(1, u * v)
        return u * np.exp(-s * u * v) * e0[a[0], b[0]] * e1[a[1], b[1]]

    vmax = (2 * d / rho) * 32
    return dyadic_gauss(integrand, 1e-10, vmax, 48)


def boundary_h(rho):
    s = -c * rho
    r = np.linalg.solve(s * np.eye(9) - q, np.eye(9))
    k = r[np.ix_(target, target)]
    w = mu @ r[:, target]
    f = w @ np.linalg.solve(k, np.ones(len(target)))
    return (1 - f) / s


def direct_survival(t):
    mp.dps = 45
    qc = matrix(q[np.ix_(comp, comp)].tolist())
    trans = expm(t * qc)
    return float(sum(mu[comp[i]] * sum(trans[i, j] for j in range(len(comp)))
                     for i in range(len(comp))))


print('Nonreversible Q1 detailed-balance defect:',
      round(float(np.linalg.norm(q1 - q1.T)), 6))
for rho in [0.8, 3.0]:
    a, b = (0, 0), (2, 1)
    approximation = inner_entry(rho, a, b)
    s = -c * rho
    direct = np.linalg.solve(s * np.eye(9) - q, np.eye(9))[states.index(a), states.index(b)]
    print(f'rotated free resolvent rho={rho}: error={abs(approximation-direct):.3e}')

for t in [0.5, 2.0]:
    def outer_integrand(rho):
        return c * np.exp(-c * t * rho) * boundary_h(rho)

    survival = dyadic_gauss(outer_integrand, 1e-9, 600.0 / t, 48).imag / np.pi
    direct = direct_survival(t)
    print(f't={t}: boundary-contour={survival:.12f}, direct-killed={direct:.12f}, '
          f'error={abs(survival-direct):.3e}')
