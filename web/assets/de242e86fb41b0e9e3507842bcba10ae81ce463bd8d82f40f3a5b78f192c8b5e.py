"""Exact rational replay of a legal nonmodular KMS qubit obstruction to J >= 4 E.

No numerical optimizer; all channel and quadratic coefficients use Fraction.
Logs appear only as formal coefficients.  Their sign proves the obstruction.
"""
from fractions import Fraction as F
import json


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def scale(c, a):
    return [[c * a[i][j] for j in range(2)] for i in range(2)]


def trprod(a, b):
    return sum(a[i][j] * b[j][i] for i in range(2) for j in range(2))


sigma = [[F(1, 17), F(0)], [F(0), F(16, 17)]]
P = [
    [[F(9, 25), F(12, 25)], [F(12, 25), F(16, 25)]],
    [[F(16, 25), F(-12, 25)], [F(-12, 25), F(9, 25)]],
]
pi = [
    [[F(9, 265), F(48, 265)], [F(48, 265), F(256, 265)]],
    [[F(1, 10), F(-3, 10)], [F(-3, 10), F(9, 10)]],
]
r = [trprod(sigma, p) for p in P]
assert r == [F(53, 85), F(32, 85)]
assert add(*P) == [[F(1), F(0)], [F(0), F(1)]]
for p in P + pi:
    assert p[0][0] + p[1][1] == 1
    assert p[0][0] * p[1][1] - p[0][1] * p[1][0] == 0


def phi(x):
    return add(*(scale(trprod(p, x), y) for p, y in zip(P, pi)))


assert phi(sigma) == sigma
# Sigma^(1/4) = diag(1,2) / 17^(1/4).  The common scalar cancels.
D = [F(1), F(2)]


def weighted_t(x):
    gx = [[D[i] * x[i][j] * D[j] for j in range(2)] for i in range(2)]
    y = phi(gx)
    return [[y[i][j] / (D[i] * D[j]) for j in range(2)] for i in range(2)]


basis = []
for i in range(2):
    for j in range(2):
        e = [[F(0) for _ in range(2)] for _ in range(2)]
        e[i][j] = F(1)
        basis.append(e)
columns = [sum(weighted_t(e), []) for e in basis]
T = [[columns[j][i] for j in range(4)] for i in range(4)]
assert all(T[i][j] == T[j][i] for i in range(4) for j in range(4))


def mv(a, x):
    return [sum(a[i][j] * x[j] for j in range(4)) for i in range(4)]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


fixed = [F(1), F(0), F(0), F(4)]
assert mv(T, fixed) == fixed
eta = sum(T[i][i] for i in range(4)) - 1
assert eta == F(1273, 2650)
# Rank at most two by the explicit outer-product representation; characteristic
# identity then verifies the two nonzero eigenvalues without floating point.
T2 = [[sum(T[i][k] * T[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
T3 = [[sum(T2[i][k] * T[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
assert all(T3[i][j] - (1 + eta) * T2[i][j] + eta * T[i][j] == 0
           for i in range(4) for j in range(4))

L = [[F(i == j) - T[i][j] for j in range(4)] for i in range(4)]
# Physical density perturbation H = [[-4,1],[1,4]]/17.
# h = Gamma^(-1/2)(H) = [-4,1/2,1/2,1] / sqrt(17).
h = [F(-4), F(1, 2), F(1, 2), F(1)]
R = [F(1, 2), F(2, 5), F(2, 5), F(1, 2)]
Rh = [R[i] * h[i] for i in range(4)]
E2 = dot(Rh, mv(L, Rh)) / 17
Lh = mv(L, h)
J2_constant = (h[0] * Lh[0] + h[3] * Lh[3]) / 17
# B_off = (16/15) log(2).
J2_log2 = F(16, 15) * (h[1] * Lh[1] + h[2] * Lh[2]) / 17
defect_constant = J2_constant - 4 * E2
assert E2 == F(1088273, 4505000)
assert J2_constant == F(2559, 2650)
assert J2_log2 == F(-8, 337875)
assert defect_constant == F(-349, 563125)
assert defect_constant < 0 and J2_log2 < 0
# Nonmodular control: diagonal input produces nonzero off-diagonal output.
nonmodular_entry = phi(basis[0])[0][1]
assert nonmodular_entry == F(-168, 1325)

# A separate classical KMS channel with the same sigma has negative spectrum.
# Its Heisenberg quantum extension first pinches in the sigma basis.
Tc = [[F(0), F(0), F(0), F(1, 4)],
      [F(0), F(0), F(0), F(0)],
      [F(0), F(0), F(0), F(0)],
      [F(1, 4), F(0), F(0), F(15, 16)]]
assert mv(Tc, fixed) == fixed
assert mv(Tc, [F(4), F(0), F(0), F(-1)]) == [F(-1, 4), F(0), F(0), F(1, 16)]

result = {
    "arithmetic": "exact fractions, formal ln(2)",
    "weighted_T_rows": [[str(x) for x in row] for row in T],
    "nonzero_spectrum": ["1", str(eta)],
    "rho_epsilon": "[[1-4 epsilon,epsilon],[epsilon,16+4 epsilon]]/17",
    "epsilon_squared_E": str(E2),
    "epsilon_squared_J": f"{J2_constant} + ({J2_log2}) ln(2)",
    "epsilon_squared_J_minus_4E": f"{defect_constant} + ({J2_log2}) ln(2)",
    "nonmodular_phi_E00_offdiagonal": str(nonmodular_entry),
    "classical_control_spectrum": ["1", "-1/16", "0", "0"],
    "all_assertions": "PASS",
}
print(json.dumps(result, indent=2))
