"""Finite-example check of persistent gate/reset Woodbury and hit contour.

Uses full nine-state matrices as an independent oracle. Succinct product
evaluation of the shifted base resolvent is checked separately in verify.py.
"""

import itertools
import numpy as np
from numpy.polynomial.legendre import leggauss
from mpmath import matrix, expm, mp


def cycle(rates):
    out = np.zeros((len(rates), len(rates)))
    for i, r in enumerate(rates):
        out[i, i] = -r
        out[i, (i + 1) % len(rates)] = r
    return out


def integrate(fun, lo, hi, order=48):
    x, w = leggauss(order)
    total = 0j
    while lo < hi:
        right = min(2 * lo, hi)
        center, half = (lo + right) / 2, (right - lo) / 2
        total += half * sum(weight * fun(center + half * node)
                            for node, weight in zip(x, w))
        lo = right
    return total


q1 = cycle([2.3, 0.7, 1.1])
q2 = cycle([0.6, 1.5, 0.9])
q0 = np.kron(q1, np.eye(3)) + np.kron(np.eye(3), q2)
p1 = (1 / np.array([2.3, 0.7, 1.1]))
p1 /= sum(p1)
p2 = (1 / np.array([0.6, 1.5, 0.9]))
p2 /= sum(p2)
pi = np.kron(p1, p2)
mu = np.kron([0.15, 0.65, 0.20], [0.40, 0.10, 0.50])
states = list(itertools.product(range(3), repeat=2))
gates = [states.index(x) for x in [(0, 0), (1, 2), (2, 1)]]
target = [states.index(x) for x in [(2, 1), (0, 2)]]
comp = [j for j in range(9) if j not in target]
e = np.eye(9)[:, gates]
gamma = np.zeros((3, 3))
flow = 0.20 * min(pi[gates])
for j in range(3):
    rate = flow / pi[gates[j]]
    gamma[j, j] = -rate
    gamma[j, (j + 1) % 3] = rate
reset = 0.4
q = q0 + e @ gamma @ e.T + reset * (np.outer(np.ones(9), pi) - np.eye(9))

droot = np.diag(np.sqrt(pi))
dinverse = np.diag(1 / np.sqrt(pi))
a0 = -droot @ q0 @ dinverse
a = -droot @ q @ dinverse
b = np.sqrt(pi)
source = mu / np.sqrt(pi)
dg = np.diag(np.sqrt(pi[gates]))
tg = -dg @ gamma @ np.linalg.inv(dg)
w = np.column_stack([b, e])
jmat = np.zeros((4, 4))
jmat[0, 0] = -reset
jmat[1:, 1:] = tg
c = 1 / 6 + 1j


def woodbury(rho):
    s = -c * rho
    k0 = np.linalg.solve((s + reset) * np.eye(9) + a0, np.eye(9))
    inner = np.eye(4) + jmat @ w.T @ k0 @ w
    k = k0 - k0 @ w @ np.linalg.solve(inner, jmat @ w.T @ k0)
    return s, k


def survival_contour(t):
    def integrand(rho):
        s, k = woodbury(rho)
        kb = k[np.ix_(target, target)]
        v = source @ k[:, target]
        f = v @ np.linalg.solve(kb, b[target])
        return c * np.exp(-c * t * rho) * (1 - f) / s

    return integrate(integrand, 1e-9, 600.0 / t).imag / np.pi


def survival_direct(t):
    mp.dps = 40
    qc = matrix(q[np.ix_(comp, comp)].tolist())
    p = expm(t * qc)
    return float(sum(mu[comp[i]] * sum(p[i, j] for j in range(len(comp)))
                     for i in range(len(comp))))


print('stationarity error', np.linalg.norm(pi @ q, ord=np.inf))
print('row-sum error', np.linalg.norm(q @ np.ones(9), ord=np.inf))
for rho in [0.8, 3.0]:
    s, kw = woodbury(rho)
    kd = np.linalg.solve(s * np.eye(9) + a, np.eye(9))
    print(f'Woodbury rho={rho}: error={np.linalg.norm(kw-kd,ord=np.inf):.3e}')
for t in [0.5, 2.0]:
    contour = survival_contour(t)
    direct = survival_direct(t)
    print(f't={t}: coupled contour={contour:.12f}, direct killed={direct:.12f}, '
          f'error={abs(contour-direct):.3e}')
