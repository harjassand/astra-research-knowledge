#!/usr/bin/env python3
"""Exact four-state check for the slow-fast observable certificate.

Usage: python3 work/applied/a11_certified_simulation/example.py [epsilon]
All generator, stationary-vector, residual, and quadratic-variation checks use
fractions.Fraction. The reported concentration radius is a numerical display of
the exact Freedman inputs; this script does not generate a random trajectory.
"""

from fractions import Fraction as F
import math
import sys


def solve(A, b):
    """Exact Gauss-Jordan solve for a nonsingular square system."""
    n = len(A)
    M = [list(map(F, A[i])) + [F(b[i])] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if M[i][j])
        M[j], M[pivot] = M[pivot], M[j]
        d = M[j][j]
        M[j] = [v / d for v in M[j]]
        for i in range(n):
            if i != j and M[i][j]:
                a = M[i][j]
                M[i] = [x - a * y for x, y in zip(M[i], M[j])]
    return [M[i][-1] for i in range(n)]


eps = F(sys.argv[1]) if len(sys.argv) > 1 else F(1, 10**8)
assert eps > 0
# State order: (z,y) = (0,0),(0,1),(1,0),(1,1).
n = 4
Q0 = [[F(0) for _ in range(n)] for _ in range(n)]
Q1 = [[F(0) for _ in range(n)] for _ in range(n)]

def add_rate(Q, i, j, rate):
    Q[i][j] += F(rate)
    Q[i][i] -= F(rate)


# Fast y-flips: kappa_0=1, kappa_1=2 and p=1/2.
add_rate(Q0, 0, 1, F(1, 2))
add_rate(Q0, 1, 0, F(1, 2))
add_rate(Q0, 2, 3, 1)
add_rate(Q0, 3, 2, 1)
# Slow z-flips: rates 1+y from z=0 and 2-y from z=1.
add_rate(Q1, 0, 2, 1)
add_rate(Q1, 1, 3, 2)
add_rate(Q1, 2, 0, 2)
add_rate(Q1, 3, 1, 1)
Q = [[Q0[i][j] + eps * Q1[i][j] for j in range(n)] for i in range(n)]

# Solve pi Q=0 plus sum pi=1 exactly.
A = [[Q[j][i] for j in range(n)] for i in range(n)]
b = [F(0)] * n
A[-1] = [F(1)] * n
b[-1] = F(1)
pi = solve(A, b)
assert all(sum(pi[i] * Q[i][j] for i in range(n)) == 0 for j in range(n))
assert sum(pi) == 1 and all(x > 0 for x in pi)

f = [F(0), F(1), F(0), F(1)]
u = [F(0), F(1), F(0), F(1, 2)]
c = F(1, 2)
residual = [f[i] - c + sum(Q0[i][j] * u[j] for j in range(n)) for i in range(n)]
q1u = [sum(Q1[i][j] * u[j] for j in range(n)) for i in range(n)]
assert residual == [0] * n
assert max(abs(x) for x in q1u) == 1

# Carré du champ Gamma_Q(u)(x) = sum_y q_xy (u_y-u_x)^2.
gamma = [sum(Q[i][j] * (u[j] - u[i]) ** 2 for j in range(n) if j != i)
         for i in range(n)]
V = max(gamma)
assert V == F(1, 2) + eps / 2
R = max(u) - min(u)
assert R == 1

stationary_mean = pi[1] + pi[3]
closed_form = 2 * (2 * eps + 1) / (9 * eps + 4)
assert stationary_mean == closed_form
assert abs(stationary_mean - c) == eps / (2 * (9 * eps + 4))
assert abs(stationary_mean - c) <= eps

alpha = 0.05
T = 10000.0
x = math.log(2 / alpha)
radius = float(eps) + float(R) / T + (
    math.sqrt(2 * float(V) * T * x) + float(R) * x / 3
) / T

print("epsilon:", eps)
print("stationary distribution:", pi)
print("stationary mean y:", stationary_mean)
print("exact mean deviation from 1/2:", abs(stationary_mean - c))
print("verified max residual:", max(map(abs, residual)))
print("verified ||Q1 u||_infinity:", max(map(abs, q1u)))
print("verified carré-du-champ bound V:", V)
print("oscillation of u:", R)
print("global slow eigenvalue: -3 epsilon (mixing scale ~ 1/(3 epsilon))")
print("Freedman radius for T=10000, alpha=0.05:", f"{radius:.10g}")
print("EXACT_FINITE_STATE_CERTIFICATE_CHECKS_PASSED")
