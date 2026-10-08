#!/usr/bin/env python3
"""Exact Fraction replay of the rational-rate common-denominator fixture."""

from collections import defaultdict
from fractions import Fraction as F


def add(a, b):
    out = defaultdict(F)
    for k, v in a.items():
        out[k] += v
    for k, v in b.items():
        out[k] += v
    return {k: v for k, v in out.items() if v}


def mul(a, b):
    out = defaultdict(F)
    for i, ai in a.items():
        for j, bj in b.items():
            out[i + j] += ai * bj
    return {k: v for k, v in out.items() if v}


def product(polys):
    out = {0: F(1)}
    for p in polys:
        out = mul(out, p)
    return out


def evaluate(p, x):
    x = F(x)
    return sum((c * x**k for k, c in p.items()), F(0))


def height(p):
    return max(p)


one_plus_x = {0: F(1), 1: F(1)}
one_plus_x2 = {0: F(1), 2: F(1)}
one_plus_x_sq = {0: F(1), 2: F(1)}
x3 = {3: F(1)}

edges = [
    {"p": one_plus_x_sq, "q": one_plus_x, "k": F(1), "nu_x": -1, "nu_y": 0},
    {"p": one_plus_x, "q": one_plus_x2, "k": F(1), "nu_x": 1, "nu_y": 0},
    {"p": x3, "q": one_plus_x, "k": F(1), "nu_x": 0, "nu_y": 1},
    {"p": one_plus_x_sq, "q": one_plus_x, "k": F(2), "nu_x": 1, "nu_y": 0},
]

denominator = product([edge["q"] for edge in edges])
lifted = []
for e, edge in enumerate(edges):
    other_q = [candidate["q"] for j, candidate in enumerate(edges) if j != e]
    lifted.append(mul(edge["p"], product(other_q)))

assert denominator == {0: F(1), 1: F(3), 2: F(4), 3: F(4), 4: F(3), 5: F(1)}
assert lifted[0] == lifted[3] == {
    0: F(1), 1: F(2), 2: F(3), 3: F(4), 4: F(3), 5: F(2), 6: F(1)
}
assert lifted[1] == {0: F(1), 1: F(4), 2: F(6), 3: F(4), 4: F(1)}
assert lifted[2] == {3: F(1), 4: F(2), 5: F(2), 6: F(2), 7: F(1)}

# For w=(1,0), all exponents only involve X, so source heights are polynomial degrees.
h_p = [height(edge["p"]) for edge in edges]
h_q = [height(edge["q"]) for edge in edges]
tau = [a - b for a, b in zip(h_p, h_q)]
h_d = height(denominator)
h_lift = [height(p) for p in lifted]
assert tau == [1, -1, 2, 1]
assert h_d == 5
assert h_lift == [6, 4, 7, 6]
assert h_lift == [h_d + order for order in tau]

nu_dot_w = [edge["nu_x"] for edge in edges]
essential = [i for i, value in enumerate(nu_dot_w) if value != 0]
essential_max = max(tau[i] for i in essential)
top_tied = [i for i in essential if tau[i] == essential_max]
assert essential == [0, 1, 3]
assert top_tied == [0, 3]
assert [nu_dot_w[i] for i in top_tied] == [-1, 1]
assert tau[2] > essential_max and nu_dot_w[2] == 0  # Neutral high-order channel is excluded.


def direct_flux_x(x):
    rates = [edge["k"] * evaluate(edge["p"], x) / evaluate(edge["q"], x) for edge in edges]
    return sum((edge["nu_x"] * rate for edge, rate in zip(edges, rates)), F(0))


def lifted_flux_x(x):
    return sum((edge["k"] * edge["nu_x"] * evaluate(p, x)
                for edge, p in zip(edges, lifted)), F(0))


measurements = {}
for x in (10, 100):
    d_value = evaluate(denominator, x)
    fx = direct_flux_x(x)
    gx = lifted_flux_x(x)
    assert gx == d_value * fx
    rates = [edge["k"] * evaluate(edge["p"], x) / evaluate(edge["q"], x) for edge in edges]
    fy = rates[2]
    gy = evaluate(lifted[2], x)
    assert gy == d_value * fy
    measurements[x] = {"D": d_value, "f_x": fx, "D_f_x": gx,
                       "f_y": fy, "D_f_y": gy, "rates": rates}

ratio_f = measurements[100]["f_x"] / measurements[10]["f_x"]
ratio_g = measurements[100]["D_f_x"] / measurements[10]["D_f_x"]
assert measurements[10]["D"] == 134431
assert measurements[10]["f_x"] == F(10322, 1111)
assert measurements[10]["D_f_x"] == 1248962
assert measurements[10]["f_y"] == F(1000, 11)
assert measurements[10]["D_f_y"] == 12221000
assert measurements[100]["D"] == 10304040301
assert measurements[100]["f_x"] == F(100030202, 1010101)
assert measurements[100]["D_f_x"] == 1020408090602
assert ratio_f == F(550166111, 51615161)
assert ratio_g == F(510204045301, 624481)

print("common denominator coefficients:", denominator)
print("lifted source polynomials:", lifted)
print("tropical orders tau:", tau)
print("common height and lifted heights:", h_d, h_lift)
print("essential indices / top tie indices:", essential, top_tied)
print("exact measurements:", measurements)
print("exact 10-to-100 net X-flux ratio:", ratio_f)
print("exact 10-to-100 lifted X-flux ratio:", ratio_g)
print("PASS: exact expansion, identity, active-tie, and neutral-exclusion checks")
