#!/usr/bin/env python3
"""Exact rational checks for the non-DSBS XOR instance in v2.txt."""

from fractions import Fraction as F
from itertools import permutations
from math import log2


JOINT = ((F(6, 25), F(7, 50)), (F(3, 50), F(14, 25)))


def entropy(probabilities):
    return -sum(float(p) * log2(float(p)) for p in probabilities if p)


def main():
    px = tuple(sum(row) for row in JOINT)
    py = tuple(sum(JOINT[x][y] for x in range(2)) for y in range(2))
    pz = (JOINT[0][0] + JOINT[1][1], JOINT[0][1] + JOINT[1][0])

    # For XOR, z=0 at (0,0),(1,1); z=1 at (0,1),(1,0).
    pyz = [[F(0), F(0)] for _ in range(2)]
    pxz = [[F(0), F(0)] for _ in range(2)]
    for x in range(2):
        for y in range(2):
            z = x ^ y
            pyz[y][z] += JOINT[x][y]
            pxz[x][z] += JOINT[x][y]
    assert all(pyz[y][z] == py[y] * pz[z] for y in range(2) for z in range(2))

    wy = tuple(tuple(JOINT[x][y] / px[x] for y in range(2)) for x in range(2))
    wz = tuple(tuple(pxz[x][z] / px[x] for z in range(2)) for x in range(2))
    # No single output permutation turns the Y channel into the Z channel.
    equivalent = any(
        all(wz[x][z] == wy[x][perm[z]] for x in range(2) for z in range(2))
        for perm in permutations(range(2))
    )
    assert not equivalent

    # Verify the exact linear coefficient governing concavity in v2.
    a, s, r = F(7, 19), F(315, 589), F(160, 589)
    f0 = s * s * a * (1 - a) - r * r * a * (1 - a)
    f1 = s * s * (-r) * (1 - 2 * a) - r * r * s * (1 - 2 * a)
    assert f0 == F(10500, 212629)
    assert f1 == -F(6300000, 204336469)
    assert f0 + f1 == F(10500, 566029) > 0

    h_y, h_z = entropy(py), entropy(pz)
    h_xy = entropy(p for row in JOINT for p in row)
    print("P_X:", px)
    print("P_Y:", py)
    print("P_Z:", pz)
    print("Y independent of Z:", True)
    print("W_Y:", wy)
    print("W_Z:", wz)
    print("output-permutation equivalent:", equivalent)
    print(f"H(Y)={h_y:.12f}")
    print(f"H(Z)={h_z:.12f}")
    print(f"H(X,Y)={h_xy:.12f}")
    print(f"2H(Z)={2*h_z:.12f}")
    print(f"SW gap H(X,Y)-2H(Z)={h_xy-2*h_z:.12f}")
    print("concavity F(0), F(1):", f0, f0 + f1)


if __name__ == "__main__":
    main()
