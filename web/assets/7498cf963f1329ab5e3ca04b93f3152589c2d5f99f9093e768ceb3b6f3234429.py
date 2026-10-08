#!/usr/bin/env python3
"""Exact rational arithmetic for the sparse geometric-drift fixture.

This checks the finite threshold construction and the generator identity on a
small grid.  The all-state drift conclusion comes from the case proof in
REPORT.txt, not from the finite grid.
"""

from fractions import Fraction as F
from itertools import product


def ceil_q(x):
    return -((-x.numerator) // x.denominator)


def ceil_log2(x):
    assert x > 0
    n = 0
    while 2**n < x:
        n += 1
    return n


# E={(1,1),(2,1),(2,2)}; all intervals are singleton rational boxes.
J = (1, 2)
I = (1, 2)
E = ((1, 1), (2, 1), (2, 2))
KJI = {(j, i): 1 for j, i in E}
ALPHA_MINUS = ALPHA_PLUS = {j: F(1) for j in J}
DELTA_MINUS = DELTA_PLUS = {j: F(1) for j in J}
P_PLUS = {edge: F(1) for edge in E}
Q_MINUS = {edge: F(2) for edge in E}
U_PLUS = {edge: F(1) for edge in E}
V_MINUS = {edge: F(2) for edge in E}

neighbors_i = {i: tuple(j for j, ii in E if ii == i) for i in I}
neighbors_j = {j: tuple(i for jj, i in E if jj == j) for j in J}

M = max(
    [10]
    + [ceil_q(2 * sum((P_PLUS[j, i] for i in neighbors_j[j]), F(0)) / DELTA_MINUS[j]) for j in J]
    + [ceil_q(P_PLUS[e] / Q_MINUS[e]) for e in E]
)
R = F(M + 1, M)
DELTA_EXP = F(1, M + 1)  # 1 - R^(-1)
DELTA_STAR = min(DELTA_MINUS.values())
C_A = DELTA_STAR / 4
ALPHA_SUM_MINUS = sum(ALPHA_MINUS.values(), F(0))
H_PLUS = sum(ALPHA_PLUS.values(), F(0))

q_i = {
    i: min(Q_MINUS[j, i] for j in neighbors_i[i]) / (M + 1)
    for i in I
}
alpha_i_minus = {
    i: sum((ALPHA_MINUS[j] for j in neighbors_i[i]), F(0))
    for i in I
}
alpha_i_plus = {
    i: sum((ALPHA_PLUS[j] for j in neighbors_i[i]), F(0))
    for i in I
}
delta_i_plus = {
    i: max(DELTA_PLUS[j] for j in neighbors_i[i])
    for i in I
}
epsilon = {
    i: min(F(1), q_i[i] / (16 * max(delta_i_plus[i], alpha_i_plus[i])))
    for i in I
}
BETA_I = {i: epsilon[i] * alpha_i_minus[i] / 2 for i in I}
BETA = min(BETA_I.values())

edge_data = {}
for j, i in E:
    qedge = Q_MINUS[j, i] * DELTA_EXP
    cedge = P_PLUS[j, i] / M
    uedge = KJI[j, i] * U_PLUS[j, i]
    t4 = ceil_log2(max(F(1), 4 * uedge / qedge))
    t2 = ceil_log2(max(F(1), 2 * uedge / qedge))
    threshold_from_linear = ceil_q(
        F(8, 3) * (cedge / 2 + epsilon[i] * DELTA_PLUS[j] + BETA) / qedge
    )
    edge_data[j, i] = {
        "q": qedge,
        "c": cedge,
        "u": uedge,
        "t4": t4,
        "t2": t2,
        "b_linear": threshold_from_linear,
    }

B = {
    i: max(1, *(max(M * edge_data[j, i]["t4"], edge_data[j, i]["b_linear"]) for j in neighbors_i[i]))
    for i in I
}
T_I = {i: max(2, *(edge_data[j, i]["t4"] for j in neighbors_i[i])) for i in I}

G_EDGE = {}
for j, i in E:
    d = edge_data[j, i]
    z_exp = d["t2"]
    G_EDGE[j, i] = d["c"] * 3 ** (z_exp + 3) + d["u"] * M * (z_exp + 3)

G_J = {j: sum((G_EDGE[j, i] for i in neighbors_j[j]), F(0)) for j in J}
K_MAX_J = {j: max(KJI[j, i] for i in neighbors_j[j]) for j in J}
V_MIN_J = {j: min(V_MINUS[j, i] for i in neighbors_j[j]) for j in J}
A_THRESHOLD = {
    j: max(K_MAX_J[j] + 1, ceil_q(1 + (G_J[j] + C_A) / V_MIN_J[j]))
    for j in J
}
C_J = {j: A_THRESHOLD[j] * (G_J[j] + C_A) for j in J}

C_LOW = {
    i: (epsilon[i] * sum((DELTA_PLUS[j] for j in neighbors_i[i]), F(0)) + BETA) * 3 ** T_I[i]
    for i in I
}
C1 = H_PLUS + sum(DELTA_PLUS.values(), F(0)) + sum(C_J.values(), F(0)) + sum(C_LOW.values(), F(0))
C = max(H_PLUS, C1)
C = F(C)
C_DRIFT = min(C_A, BETA / 2, ALPHA_SUM_MINUS)


def fall(n, order):
    ans = 1
    for z in range(order):
        ans *= n - z
    return max(0, ans)


def h(i, a):
    return int(all(a[j - 1] == 0 for j in neighbors_i[i]))


def potential(state):
    a1, a2, b1, b2 = state
    a = (a1, a2)
    b = {1: b1, 2: b2}
    return (
        F(a1 + a2)
        + sum((R ** b[i] * (1 + epsilon[i] * h(i, a)) for i in I), F(0))
        + int(a1 + a2 == 0)
    )


def direct_generator(state):
    a1, a2, b1, b2 = state
    a = [a1, a2]
    b = [b1, b2]
    total = F(0)

    def add(rate, aa, bb):
        nonlocal total
        if rate:
            target = (aa[0], aa[1], bb[0], bb[1])
            total += rate * (potential(target) - potential(state))

    for j in J:
        aa = a.copy()
        aa[j - 1] += 1
        add(ALPHA_PLUS[j], aa, b.copy())
        if a[j - 1]:
            aa = a.copy()
            aa[j - 1] -= 1
            add(DELTA_PLUS[j] * a[j - 1], aa, b.copy())

    for j, i in E:
        aj = a[j - 1]
        bi = b[i - 1]
        if aj:
            bb = b.copy()
            bb[i - 1] += 1
            add(P_PLUS[j, i] * aj, a.copy(), bb)
        if aj and bi:
            bb = b.copy()
            bb[i - 1] -= 1
            add(Q_MINUS[j, i] * aj * bi, a.copy(), bb)
        if aj and bi:
            aa = a.copy()
            aa[j - 1] += KJI[j, i]
            add(U_PLUS[j, i] * aj * bi, aa, b.copy())
        rev_prop = V_MINUS[j, i] * fall(aj, KJI[j, i] + 1) * bi
        if rev_prop:
            aa = a.copy()
            aa[j - 1] -= KJI[j, i]
            add(rev_prop, aa, b.copy())
    return total


def formula_generator(state):
    a1, a2, b1, b2 = state
    a = (a1, a2)
    b = {1: b1, 2: b2}
    A = a1 + a2
    ans = H_PLUS - sum((DELTA_PLUS[j] * a[j - 1] for j in J), F(0))
    ans += -ALPHA_SUM_MINUS if A == 0 else F(0)
    ans += sum((DELTA_PLUS[j] for j in J if a[j - 1] == 1 and A == 1), F(0))
    for j, i in E:
        aj, bi = a[j - 1], b[i]
        d = DELTA_EXP
        c = R - 1
        ans += P_PLUS[j, i] * aj * c * R**bi
        ans -= Q_MINUS[j, i] * aj * bi * d * R**bi
        ans += KJI[j, i] * U_PLUS[j, i] * aj * bi
        ans -= KJI[j, i] * V_MINUS[j, i] * fall(aj, KJI[j, i] + 1) * bi
    for i in I:
        hs = h(i, a)
        ans -= epsilon[i] * R**b[i] * sum(
            (ALPHA_PLUS[j] for j in neighbors_i[i]), F(0)
        ) * hs
        for j in neighbors_i[i]:
            if a[j - 1] == 1 and all(a[z - 1] == 0 for z in neighbors_i[i] if z != j):
                ans += epsilon[i] * R**b[i] * DELTA_PLUS[j]
    return ans


def main():
    # Arithmetic checks for the finite threshold certificate.
    assert R**M >= 2 and R**M < 3
    assert all(epsilon[i] * max(delta_i_plus[i], alpha_i_plus[i]) <= q_i[i] / 16 for i in I)
    assert all(BETA <= q_i[i] / 32 for i in I)
    assert all(B[i] <= M * T_I[i] for i in I)
    for j, i in E:
        d = edge_data[j, i]
        assert M * d["t4"] >= 1
        assert R ** (M * d["t4"]) >= 2 ** d["t4"] >= 4 * d["u"] / d["q"]
        assert F(3, 1) ** (d["t2"] + 3) >= 1
    # Exact finite identity check, including catalyst and local support switches.
    states = 0
    for state in product(range(5), repeat=4):
        assert direct_generator(state) == formula_generator(state), (state, direct_generator(state), formula_generator(state))
        states += 1

    print({
        "status": "PASS",
        "scope": "exact threshold arithmetic and finite generator-identity fixture",
        "states_checked_for_identity": states,
        "E": E,
        "M": M,
        "R": str(R),
        "epsilon": {i: str(epsilon[i]) for i in I},
        "B": B,
        "G_edge": {e: str(G_EDGE[e]) for e in E},
        "A_threshold": A_THRESHOLD,
        "c": str(C_DRIFT),
        "C": str(C),
        "not_checked": [
            "all-state drift by finite enumeration",
            "recurrence for networks outside this paired family",
            "necessity of this certificate template",
        ],
    })


if __name__ == "__main__":
    main()
