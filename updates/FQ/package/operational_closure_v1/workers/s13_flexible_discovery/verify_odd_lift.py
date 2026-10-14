"""Exact-arithmetic checks for the six-state odd-parity lift of P_(1/20).

This script checks finitely many identities. The general all-dimension proof is
in REPORT.md and does not depend on numerical sampling or this script.
"""

from fractions import Fraction as F
from math import log
import json


def mv(a, v):
    return [sum(a[i][j] * v[j] for j in range(len(v)))
            for i in range(len(a))]


def dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))


def row_stationary(pi, q):
    return [sum(pi[i] * q[i][j] for i in range(len(pi)))
            for j in range(len(pi))]


q = F(1, 20)
eps = F(1, 7)
s = 1 + q
Q = [
    [-s, F(1), q],
    [q, -s, F(1)],
    [F(1), q, -s],
]
pi = [F(1, 3)] * 3
assert row_stationary(pi, Q) == [0] * 3

# Stationary time-reversed generator.
Qrev = [[pi[j] * Q[j][i] / pi[i] for j in range(3)]
        for i in range(3)]
assert all(Q[i][i] == Qrev[i][i] for i in range(3))
assert row_stationary(pi, Qrev) == [0] * 3

# The states are (A,+), (B1,+), (B2,+), (A,-), (B1,-), (B2,-).
L = [[F(0) for _ in range(6)] for _ in range(6)]
for i in range(3):
    for j in range(3):
        L[i][j] = Q[i][j]
        L[i + 3][j + 3] = Qrev[i][j]
L[0][0] -= eps
L[0][3] = eps
L[3][3] -= eps
L[3][0] = eps
rho = [p / 2 for p in pi] * 2
theta = [3, 4, 5, 0, 1, 2]

assert all(sum(row) == 0 for row in L)
assert row_stationary(rho, L) == [0] * 6
assert all(rho[i] == rho[theta[i]] for i in range(6))
assert all(L[i][i] == L[theta[i]][theta[i]] for i in range(6))
assert all(rho[i] * L[i][j] == rho[theta[j]] * L[theta[j]][theta[i]]
           for i in range(6) for j in range(6) if i != j)
assert all(L[i][j] >= 0 for i in range(6) for j in range(6) if i != j)

reached = {0}
while True:
    new = reached | {j for i in reached for j in range(6) if L[i][j] > 0}
    if new == reached:
        break
    reached = new
assert reached == set(range(6))

# Original and reversed B dwell derivatives: alpha S^k t.
alpha = [Q[0][1] / s, Q[0][2] / s]
S = [[Q[i][j] for j in (1, 2)] for i in (1, 2)]
t = [Q[i][0] for i in (1, 2)]
alphar = [Qrev[0][1] / s, Qrev[0][2] / s]
Sr = [[Qrev[i][j] for j in (1, 2)] for i in (1, 2)]
tr = [Qrev[i][0] for i in (1, 2)]
v, vr = t[:], tr[:]
derivatives = []
for _ in range(9):
    derivatives.append(dot(alpha, v))
    assert dot(alpha, v) == dot(alphar, vr)
    v, vr = mv(S, v), mv(Sr, vr)

b = 2 * q / s
c = 1 + q + q * q
assert derivatives[0] == b
assert derivatives[1] == F(341, 400) == 1 - 3 * q + q * q
assert s * c == 2 * q * s + 1 + q**3
assert sum(rho[i] * (-L[i][i]) for i in range(6)) == s + eps / 3
ordinary_ep = sum(
    float(rho[i] * L[i][j] - rho[j] * L[j][i])
    * log(float(rho[i] * L[i][j] / (rho[j] * L[j][i])))
    for i in range(6) for j in range(i + 1, 6) if L[i][j] > 0 and L[j][i] > 0
)
assert abs(ordinary_ep - float(1 - q) * log(1 / float(q))) < 1e-12

print(json.dumps({
    "q": str(q),
    "epsilon": str(eps),
    "stationary_mass_each_lift_state": str(rho[0]),
    "parity_detailed_balance": True,
    "A_dwell_rate": str(s),
    "B_dwell_transform": f"(({b}) z + ({c}))/(z^2 + ({2*s}) z + ({c}))",
    "B_density_at_zero": str(derivatives[0]),
    "B_density_derivative_at_zero": str(derivatives[1]),
    "matching_B_density_derivatives_0_to_8": [str(x) for x in derivatives],
    "ordinary_entropy_production_approx": ordinary_ep,
    "extra_stationary_jump_activity": str(eps / 3),
}, indent=2))
