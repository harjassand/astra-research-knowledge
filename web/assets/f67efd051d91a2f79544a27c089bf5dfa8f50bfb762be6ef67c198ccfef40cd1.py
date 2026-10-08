#!/usr/bin/env python3
"""Exact checks of the selected complement-LCU seed block row, R=1,2,3."""
from fractions import Fraction as F
from itertools import product

N = 32
c, f = 0b00010, 0b10010
gs = (0b01110, 0b10110, 0b11010)
phi = {c: 1, f: -1}
psi = {c: 1, **{g: -1 for g in gs}}

def qrow(support, x):
    return [F(int(x == y)) - F(support.get(x, 0) * support.get(y, 0), len(support)) for y in range(N)]

Qp = [qrow(phi, x) for x in range(N)]
Qs = [qrow(psi, x) for x in range(N)]
G = [[sum(Qp[x][z] * Qs[z][y] for z in range(N)) for y in range(N)] for x in range(N)]
U = set(phi) | set(psi)
tau2 = F(1,  32)
coef = 4 * tau2

def product_at(row, y):
    value = F(1)
    for yi in y:
        value *= row[yi]
    return value

def c_entry(y):
    x = (c,) * len(y)
    gp = product_at([G[c][z] for z in range(N)], y)
    gpt = product_at([G[z][c] for z in range(N)], y)
    pp = product_at(Qp[c], y)
    ps = product_at(Qs[c], y)
    return F(int(y == x)) + coef * (gp + gpt - pp - ps)

for R in (1, 2, 3):
    count = 0
    outside_nonzero = []
    for y in product(range(N), repeat=R):
        value = c_entry(y)
        if value:
            count += 1
            if any(z not in U for z in y):
                outside_nonzero.append((y, value))
    assert count == 5**R, (R, count, 5**R)
    assert not outside_nonzero, (R, outside_nonzero[:3])
    print(f"R={R}: exact same-label block row support {count}; expected {5**R}; outside support 0")
