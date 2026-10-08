#!/usr/bin/env python3
"""Exact rational independent check of the sparse support-switch generator.

This is finite evidence only.  It checks the displayed identity on a second,
three-catalyst path graph and evaluates selected mixed-escape sequences.
"""
from fractions import Fraction as F
from itertools import product

J = range(3)
I = range(3)
E = ((0, 0), (1, 0), (1, 1), (2, 1), (2, 2))
N_I = {i: tuple(j for j, ii in E if ii == i) for i in I}
N_J = {j: tuple(i for jj, i in E if jj == j) for j in J}
R = F(6, 5)
K = F(2)
lam = [F(1)] * 3
alpha = [F(1)] * 3
delta = [F(1)] * 3
eps = [F(1)] * 3
p = {(j, i): F(1) for j, i in E}
q = {(j, i): F(2) for j, i in E}
u = {(j, i): F(1) for j, i in E}
v = {(j, i): F(1) for j, i in E}
k = {(j, i): 1 for j, i in E}


def fall(a, order):
    out = 1
    for r in range(order):
        out *= a - r
    return max(out, 0)


def h(a, i):
    return int(sum(a[j] for j in N_I[i]) == 0)


def V(x):
    a, b = x[:3], x[3:]
    return (sum(lam[j] * a[j] for j in J)
            + sum(R ** b[i] * (1 + eps[i] * h(a, i)) for i in I)
            + K * int(all(a[j] == 0 for j in J)))


def direct_LV(x):
    a, b = x[:3], x[3:]
    out = F(0)

    def jump(change, rate):
        nonlocal out
        if rate:
            y = tuple(x[t] + change[t] for t in range(6))
            assert all(z >= 0 for z in y), (x, y, rate)
            out += rate * (V(y) - V(x))

    for j in J:
        d = [0] * 6
        d[j] = 1
        jump(d, alpha[j])
        d = [0] * 6
        d[j] = -1
        jump(d, delta[j] * a[j])
    for j, i in E:
        d = [0] * 6
        d[3 + i] = 1
        jump(d, p[j, i] * a[j])
        d = [0] * 6
        d[3 + i] = -1
        jump(d, q[j, i] * a[j] * b[i])
        d = [0] * 6
        d[j] = k[j, i]
        jump(d, u[j, i] * a[j] * b[i])
        d = [0] * 6
        d[j] = -k[j, i]
        jump(d, v[j, i] * fall(a[j], k[j, i] + 1) * b[i])
    return out


def formula_LV(x):
    a, b = x[:3], x[3:]
    H = sum(alpha[j] * lam[j] for j in J)
    out = H - sum(lam[j] * delta[j] * a[j] for j in J)
    for j, i in E:
        c, d = R - 1, 1 - 1 / R
        out += (p[j, i] * c * a[j] * R ** b[i]
                - q[j, i] * d * a[j] * b[i] * R ** b[i]
                + lam[j] * k[j, i] * u[j, i] * a[j] * b[i]
                - lam[j] * k[j, i] * v[j, i]
                    * fall(a[j], k[j, i] + 1) * b[i])
    out -= K * sum(alpha) * int(all(a[j] == 0 for j in J))
    for j in J:
        out += K * delta[j] * int(a[j] == 1 and all(a[l] == 0 for l in J if l != j))
    for i in I:
        local = [a[j] for j in N_I[i]]
        switch = -sum(alpha[j] for j in N_I[i]) * int(all(z == 0 for z in local))
        switch += sum(delta[j] * int(a[j] == 1 and all(a[l] == 0 for l in N_I[i] if l != j))
                      for j in N_I[i])
        out += eps[i] * R ** b[i] * switch
    return out


checked = 0
for x in product(range(4), repeat=6):
    direct = direct_LV(x)
    formula = formula_LV(x)
    if direct != formula:
        raise AssertionError((x, direct, formula))
    checked += 1


def seq_states(n):
    return {
        "inactive B1 high; unrelated A3 high": (0, 0, n, n, 0, 0),
        "active B2 high; sole-neighbor switch": (0, 1, 0, 0, n, 0),
        "active B2 high; two neighbors high": (0, n, n, 0, n, 0),
        "A2 high; bounded positive neighbor B1": (0, n, 0, 1, 0, 0),
        "A2 high; all neighbor substrates zero": (0, n, 0, 0, 0, 0),
        "A2 and adjacent B2 both high": (0, n, 0, 0, n, 0),
        "all catalysts zero; all substrates high": (0, 0, 0, n, n, n),
    }


print(f"identity_grid_states={checked}; exact_rational=YES; graph_edges={len(E)}")
for name, state in seq_states(32).items():
    value = direct_LV(state)
    assert value == formula_LV(state)
    print(f"mixed_sequence_endpoint={name}; n=32; LV={value}; sign={'negative' if value < 0 else 'nonnegative'}")
for n in (4, 8, 16, 32):
    vals = [direct_LV(state) for state in seq_states(n).values()]
    print(f"sequence_scale=n:{n}; all_seven_negative={all(z < 0 for z in vals)}")
