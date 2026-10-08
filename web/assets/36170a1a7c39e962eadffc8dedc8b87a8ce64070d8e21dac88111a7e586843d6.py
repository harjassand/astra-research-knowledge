#!/usr/bin/env python3
"""Exact finite checks for the r=s=t=2 scalar triangle obstruction over F_7."""

from itertools import product

P = 7
R = 2
COORDS = range(R)
US = (1, 2)
VS = (1, 2)


def inv(x):
    x %= P
    if not x:
        raise ZeroDivisionError
    return pow(x, P - 2, P)


# c[u,v] = u+r+v, with the displayed source labels u,v in {1,2}.
c = {(u, v): (u + R + v) % P for u in US for v in VS}
assert c == {(1, 1): 4, (1, 2): 5, (2, 1): 5, (2, 2): 6}
assert all(x != 0 for x in c.values())

# Rectangle word X_11 X_21^-1 X_22 X_12^-1 has factor -1.
w = c[1, 1] * inv(c[2, 1]) * c[2, 2] * inv(c[1, 2]) % P
assert w == P - 1
assert (1 - w) % P != 0  # normalized rank defect is exactly one in D=1.

# Bijection and shifts: for each u,v, (alpha,beta)->(alpha+v,beta+u)
# permutes all coordinate pairs modulo (s,t)=(2,2).
for u, v in product(US, VS):
    image = {
        ((alpha + v) % R, (beta + u) % R)
        for alpha, beta in product(COORDS, repeat=2)
    }
    assert image == set(product(COORDS, repeat=2))

# Triangle equations reduce, after coordinate constancy, to R_v=c_uv L_u.
# Exhaust all scalar invertibles for D=1 and verify none satisfy them.
units = range(1, P)
solutions = []
for L1, L2, R1, R2 in product(units, repeat=4):
    L = {1: L1, 2: L2}
    Rv = {1: R1, 2: R2}
    if all(Rv[v] == c[u, v] * L[u] % P for u, v in product(US, VS)):
        solutions.append((L1, L2, R1, R2))
assert not solutions

det = (c[1, 1] * c[2, 2] - c[1, 2] * c[2, 1]) % P
assert det == P - 1

print({
    "field": "F_7",
    "r_s_t": [R, R, R],
    "rectangle_cross_ratio": w,
    "rectangle_rank_defect_D1": 1,
    "triangle_coordinate_coverage": "all four (j,k) pairs for each (u,v)",
    "constant_scalar_solutions": len(solutions),
    "determinant": det,
    "status": "PASS",
})
