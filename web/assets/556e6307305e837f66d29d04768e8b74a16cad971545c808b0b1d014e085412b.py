#!/usr/bin/env python3
"""Exact-rational check of the seven-triangle FEM embedding in v1.txt."""
from fractions import Fraction as F

I = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
c = (F(1, 3), F(1, 3))
O = [(c[0] + 4 * (p[0] - c[0]), c[1] + 4 * (p[1] - c[1])) for p in I]
coords = I + O
triangles = [(0, 1, 2)]
for i in range(3):
    j = (i + 1) % 3
    triangles.extend([(3 + i, 3 + j, j), (3 + i, j, i)])


def local_stiffness(ids, tensor):
    p0, p1, p2 = [coords[i] for i in ids]
    det = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
    area = abs(det) / 2
    grads = [
        ((p1[1] - p2[1]) / det, (p2[0] - p1[0]) / det),
        ((p2[1] - p0[1]) / det, (p0[0] - p2[0]) / det),
        ((p0[1] - p1[1]) / det, (p1[0] - p0[0]) / det),
    ]
    return [[area * sum(grads[a][r] * tensor[r][s] * grads[b][s]
                        for r in range(2) for s in range(2))
             for b in range(3)] for a in range(3)]


def assemble(kappa):
    k = F(kappa)
    half = F(1, 2)
    central_tensor = [[(k + 1) * half, (k - 1) * half],
                      [(k - 1) * half, (k + 1) * half]]
    eye = [[F(1), F(0)], [F(0), F(1)]]
    full = [[F(0) for _ in range(6)] for _ in range(6)]
    for ids in triangles:
        tensor = central_tensor if ids == (0, 1, 2) else eye
        loc = local_stiffness(ids, tensor)
        for a, ia in enumerate(ids):
            for b, ib in enumerate(ids):
                full[ia][ib] += loc[a][b]
    return [row[:3] for row in full[:3]]


def mat_add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mat_scale(s, a):
    return [[s * x for x in row] for row in a]


def mat_outer(x, y):
    return [[a * b for b in y] for a in x]


def det3(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))

w = [F(1), F(-1, 2), F(-1, 2)]
v = [F(0), F(1, 2), F(-1, 2)]
ww = mat_outer(w, w)
vv = mat_outer(v, v)
S = [[F(0) for _ in range(3)] for _ in range(3)]
# S is the coefficient-one ring contribution, computed by subtracting the central face.
for i in range(3):
    for j in range(3):
        S[i][j] = assemble(1)[i][j] - (vv[i][j] + ww[i][j])
C = mat_add(vv, S)

# Sylvester's criterion verifies S and C are SPD (all leading principal minors > 0).
for M in (S, C):
    assert M[0][0] > 0
    assert M[0][0] * M[1][1] - M[0][1] * M[1][0] > 0
    assert det3(M) > 0

for kappa in (100, 1000):
    A = assemble(kappa)
    expected = mat_add(mat_scale(F(kappa), ww), C)
    assert A == expected, (kappa, A, expected)
    assert A[0][1] < 0 and A[0][2] < 0 and A[1][2] > 0
    assert A[0][1] * A[0][2] * A[1][2] > 0
    # Absolute diagonal-dominance deficits at free rows 1 and 2.
    deficits = [sum(abs(A[i][j]) for j in range(3) if j != i) - A[i][i] for i in (1, 2)]
    assert all(d > 0 for d in deficits)
    print(f"kappa={kappa}: signs=(-,-,+), abs-DD deficits={deficits}")

print("S =", S)
print("C =", C)
print("exact assembly and SPD checks passed")
