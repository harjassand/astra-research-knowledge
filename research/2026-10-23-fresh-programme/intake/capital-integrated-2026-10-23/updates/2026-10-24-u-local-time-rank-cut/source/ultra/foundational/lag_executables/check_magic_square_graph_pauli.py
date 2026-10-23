#!/usr/bin/env python3
"""Exact finite replay of magic-square graph and two-qubit Pauli grid."""

from itertools import product

SIGNS = (-1, 1)
BETA = (1, 1, -1)

left = []
for x in range(3):
    for a in product(SIGNS, repeat=3):
        if a[0] * a[1] * a[2] == 1:
            left.append((x, a))

right = []
for y, beta in enumerate(BETA):
    for b in product(SIGNS, repeat=3):
        if b[0] * b[1] * b[2] == beta:
            right.append((y, b))

assert len(left) == len(right) == 12

# Bitset of neighbors for each left vertex.
adj = []
for x, a in left:
    mask = 0
    for j, (y, b) in enumerate(right):
        if a[y] == b[x]:
            mask |= 1 << j
    adj.append(mask)

degrees_left = [mask.bit_count() for mask in adj]
degrees_right = [sum((adj[i] >> j) & 1 for i in range(12)) for j in range(12)]
assert degrees_left == [6] * 12
assert degrees_right == [6] * 12

# Exhaust every S subset of left vertices and count complete common neighbors.
all_right = (1 << 12) - 1
max_area = -1
maximizer_counts = {}
maximizers = []
for S in range(1 << 12):
    common = all_right
    size_left = S.bit_count()
    bits = S
    while bits:
        one = bits & -bits
        i = one.bit_length() - 1
        bits -= one
        common &= adj[i]
    size_right = common.bit_count()
    area = size_left * size_right
    if area > max_area:
        max_area = area
        maximizer_counts.clear()
        maximizers.clear()
    if area == max_area:
        maximizer_counts[(size_left, size_right)] = \
            maximizer_counts.get((size_left, size_right), 0) + 1
        maximizers.append((S, common))

assert max_area == 6
assert maximizer_counts == {(1, 6): 12, (2, 3): 48, (3, 2): 48, (6, 1): 12}
assert len(maximizers) == 120

# Every maximizing shape has the expected row/column support pattern.
def count_by_axis(mask, vertices, axis_value):
    return sum(1 for j, vertex in enumerate(vertices)
               if ((mask >> j) & 1) and vertex[0] == axis_value)

for S, common in maximizers:
    k, ell = S.bit_count(), common.bit_count()
    lrows = tuple(count_by_axis(S, left, x) for x in range(3))
    rcols = tuple(count_by_axis(common, right, y) for y in range(3))
    if (k, ell) == (1, 6):
        assert sorted(rcols) == [2, 2, 2]
    elif (k, ell) == (6, 1):
        assert sorted(lrows) == [2, 2, 2]
    elif (k, ell) == (2, 3):
        assert sorted(lrows) == [0, 1, 1]
        assert sorted(rcols) == [1, 1, 1]
    elif (k, ell) == (3, 2):
        assert sorted(lrows) == [1, 1, 1]
        assert sorted(rcols) == [0, 1, 1]
    else:
        raise AssertionError((k, ell))

# Pauli strings with a Gaussian-integer phase. Single-qubit multiplication:
# P Q = phase * R. This avoids numerical matrix tolerances.
mul1 = {
    ("I", "I"): (1, "I"), ("I", "X"): (1, "X"),
    ("I", "Y"): (1, "Y"), ("I", "Z"): (1, "Z"),
    ("X", "I"): (1, "X"), ("Y", "I"): (1, "Y"),
    ("Z", "I"): (1, "Z"),
    ("X", "X"): (1, "I"), ("Y", "Y"): (1, "I"),
    ("Z", "Z"): (1, "I"),
    ("X", "Y"): (1j, "Z"), ("Y", "X"): (-1j, "Z"),
    ("Y", "Z"): (1j, "X"), ("Z", "Y"): (-1j, "X"),
    ("Z", "X"): (1j, "Y"), ("X", "Z"): (-1j, "Y"),
}


def multiply(p, q):
    phase1, out1 = mul1[p[0], q[0]]
    phase2, out2 = mul1[p[1], q[1]]
    return phase1 * phase2, out1 + out2


def commute(p, q):
    phase_pq, out_pq = multiply(p, q)
    phase_qp, out_qp = multiply(q, p)
    return out_pq == out_qp and phase_pq == phase_qp


def product3(row):
    phase, current = 1, "II"
    for p in row:
        phase2, current = multiply(current, p)
        phase *= phase2
    return phase, current


grid = [
    ["ZI", "IZ", "ZZ"],
    ["IX", "XI", "XX"],
    ["ZX", "XZ", "YY"],
]
for row in grid:
    assert all(commute(row[i], row[j]) for i in range(3) for j in range(i + 1, 3))
    assert product3(row) == (1, "II")

column_products = []
for y in range(3):
    col = [grid[x][y] for x in range(3)]
    assert all(commute(col[i], col[j]) for i in range(3) for j in range(i + 1, 3))
    column_products.append(product3(col))
assert column_products == [(1, "II"), (1, "II"), (-1, "II")]

# Every grid string is symmetric under transpose (it has zero or two Y's), so
# measuring the transposed column on Bob's half of two Bell pairs gives the
# same cell outcome as Alice's row measurement.
for row in grid:
    for p in row:
        assert p.count("Y") in (0, 2)

print("magic-square graph: |L|=|R|=12; degrees are all 6")
print("maximum complete biclique area:", max_area)
print("maximizing (left_size,right_size) counts:", maximizer_counts)
print("shapes: 1x6 stars (12), 2x3 rectangles (48), 3x2 rectangles (48), 6x1 stars (12)")
print("2x3: left vertices in two distinct rows; one common right vertex per column")
print("3x2: right vertices in two distinct columns; one common left vertex per row")
print("Pauli rows: +I,+I,+I; columns: +I,+I,-I; all within-line pairs commute")
print("PASS: exact graph enumeration and exact Pauli phase checks")
