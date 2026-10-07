#!/usr/bin/env python3
"""Exact support-pattern check for the two-replica copy/exclusion tensor."""
from itertools import permutations, product

# E has entries 1 on 0000, 1010, 0101, and 0 elsewhere.
E = {"0000": 1, "1010": 1, "0101": 1}

def permuted_signature(order):
    out = {}
    for y in map("".join, product("01", repeat=4)):
        x = [None] * 4
        for new_pos, old_pos in enumerate(order):
            x[old_pos] = y[new_pos]
        out[y] = E.get("".join(x), 0)
    return out

def mgi(g):
    return (g["0000"] * g["1111"] - g["1100"] * g["0011"]
            + g["1010"] * g["0101"] - g["1001"] * g["0110"])

# Diagonal invertible gauges multiply each coordinate by a product of
# nonzero per-wire factors; test all signs on the two basis states per wire.
units = (1, -1)
for order in permutations(range(4)):
    g = permuted_signature(order)
    assert mgi(g) != 0
    for scales in product(units, repeat=8):
        a, b = scales[:4], scales[4:]
        transformed = {}
        for bits, value in g.items():
            factor = 1
            for i, bit in enumerate(bits):
                factor *= b[i] if bit == "1" else a[i]
            transformed[bits] = value * factor
        assert mgi(transformed) != 0
print("PASS: MGI remains nonzero under all 24 wire permutations and 2^8 diagonal sign gauges")
