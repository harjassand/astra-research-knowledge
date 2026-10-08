#!/usr/bin/env python3
"""Exact small-instance checks for the Gutzwiller stability obstruction.

Only the Python standard library is used. Determinants are expanded over
permutations, and all arithmetic is integer/Fraction arithmetic.
"""

from fractions import Fraction
from itertools import combinations, permutations
import json


def det_int(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    total = 0
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = -1 if inversions % 2 else 1
        for i, j in enumerate(p):
            term *= matrix[i][j]
        total += term
    return total


def submatrix(matrix, rows, cols):
    return [[matrix[i][j] for j in cols] for i in rows]


def sector_weight(matrix, k, disjoint):
    n = len(matrix)
    subsets = list(combinations(range(n), k))
    total = 0
    for rows in subsets:
        for cols in subsets:
            if disjoint and not set(rows).isdisjoint(cols):
                continue
            d = det_int(submatrix(matrix, rows, cols))
            total += d * d
    return total


def matmul_transpose(matrix):
    n = len(matrix)
    return [
        [sum(matrix[i][r] * matrix[j][r] for r in range(n)) + (i == j)
         for j in range(n)]
        for i in range(n)
    ]


def gadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def gmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gzero(a):
    return a == (Fraction(0), Fraction(0))


def q_matrix(matrix, k):
    """Return the row/column-marked fixed-k polynomial as (I,J,weight)."""
    n = len(matrix)
    terms = []
    for rows in combinations(range(n), k):
        for cols in combinations(range(n), k):
            if set(rows).isdisjoint(cols):
                d = det_int(submatrix(matrix, rows, cols))
                if d:
                    terms.append((rows, cols, d * d))
    return terms


def row_activity_weights(matrix, k):
    """Return w(S)=sum_{J disjoint S, |J|=k} det(A[S,J])^2."""
    n = len(matrix)
    out = {}
    for rows in combinations(range(n), k):
        weight = 0
        for cols in combinations(range(n), k):
            if set(rows).isdisjoint(cols):
                d = det_int(submatrix(matrix, rows, cols))
                weight += d * d
        if weight:
            out[rows] = weight
    return out


def evaluate_homogeneous_quadratic(terms, x):
    value = (Fraction(0), Fraction(0))
    for (i, j), weight in terms.items():
        value = gadd(value, tuple(weight * q for q in gmul(x[i], x[j])))
    return value


def rayleigh_data_quadratic(terms, i, j, x):
    p = (Fraction(0), Fraction(0))
    di = (Fraction(0), Fraction(0))
    dj = (Fraction(0), Fraction(0))
    dij = Fraction(0)
    for (a, b), weight in terms.items():
        monomial = tuple(weight * q for q in gmul(x[a], x[b]))
        p = gadd(p, monomial)
        if i in (a, b):
            other = x[b] if a == i else x[a]
            di = gadd(di, tuple(weight * q for q in other))
        if j in (a, b):
            other = x[b] if a == j else x[a]
            dj = gadd(dj, tuple(weight * q for q in other))
        if i in (a, b) and j in (a, b):
            dij += weight
    delta = gadd(gmul(di, dj), tuple(-q for q in tuple(dij * q for q in p)))
    return p, di, dj, dij, delta


def main():
    # Smallest nonzero row/column-marked example: Q=x1*y2+x2*y1.
    swap = [[0, 1], [1, 0]]
    q_terms = q_matrix(swap, 1)
    assert q_terms == [((0,), (1,), 1), ((1,), (0,), 1)]
    x1 = (Fraction(1), Fraction(1))
    x2 = (Fraction(1), Fraction(2))
    y1 = (Fraction(-4), Fraction(1))
    y2 = (Fraction(13, 2), Fraction(1, 2))
    q_witness = gadd(gmul(x1, y2), gmul(x2, y1))
    assert all(v[1] > 0 for v in (x1, x2, y1, y2))
    assert gzero(q_witness)
    q_rayleigh_at_ones = -1  # Delta_(x1,y2) = -x2*y1.

    # C4 endpoint-pair representation. B=I and C's columns are the next
    # endpoints on the oriented cycle 1->2->3->4->1.
    n = 4
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    B = [[int(i == j) for j in range(n)] for i in range(n)]
    C = [[int(i == edges[j][1]) for j in range(n)] for i in range(n)]
    V = [B[i] + C[i] for i in range(n)]
    pair_terms = {}
    for selected in combinations(range(n), 2):
        cols = list(selected) + [n + j for j in selected]
        d = det_int([[V[i][j] for j in cols] for i in range(n)])
        if d:
            pair_terms[selected] = d * d
    assert pair_terms == {(0, 2): 1, (1, 3): 1}

    # Here V=[I,A^T], hence A=C^T. Verify the same polynomial by the
    # fixed-filter full-sector minors det A[I,I^c].
    A4 = [list(row) for row in zip(*C)]
    full_sector_terms = {}
    for rows in combinations(range(n), 2):
        cols = tuple(i for i in range(n) if i not in rows)
        d = det_int(submatrix(A4, rows, cols))
        if d:
            full_sector_terms[rows] = d * d
    assert full_sector_terms == pair_terms

    plus_i = (Fraction(1), Fraction(1))
    minus_plus_i = (Fraction(-1), Fraction(1))
    f_witness = gadd(gmul(plus_i, plus_i), gmul(minus_plus_i, minus_plus_i))
    assert gzero(f_witness)
    assert plus_i[1] > 0 and minus_plus_i[1] > 0
    f_rayleigh_at_ones = -1  # Delta_(z1,z3) = -z2*z4.

    # The independently specified canonical non-full-sector example: A is
    # the 0/1 adjacency matrix of P5 and k=2.
    A5 = [
        [0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0],
    ]
    path_terms = row_activity_weights(A5, 2)
    expected_path_terms = {
        (0, 2): 1, (0, 3): 2, (0, 4): 1, (1, 2): 1,
        (1, 3): 3, (1, 4): 2, (2, 3): 1, (2, 4): 1,
    }
    assert path_terms == expected_path_terms
    path_x = [
        (Fraction(-3), Fraction(1, 100)),
        (Fraction(2), Fraction(29397, 20500)),
        (Fraction(0), Fraction(2)),
        (Fraction(-2), Fraction(1, 100)),
        (Fraction(3), Fraction(1, 100)),
    ]
    path_value = evaluate_homogeneous_quadratic(path_terms, path_x)
    assert all(q[1] > 0 for q in path_x)
    assert gzero(path_value)

    real_point = [
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1, 10), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(0)),
    ]
    p, d1, d4, d14, delta14 = rayleigh_data_quadratic(
        path_terms, 0, 3, real_point
    )
    assert p == (Fraction(42, 5), Fraction(0))
    assert d1 == (Fraction(31, 10), Fraction(0))
    assert d4 == (Fraction(51, 10), Fraction(0))
    assert d14 == 2
    assert delta14 == (Fraction(-99, 100), Fraction(0))

    # Physical normalizations for the C4 and P5 examples.
    z4 = sector_weight(A4, 2, True)
    w4 = sector_weight(A4, 2, False)
    norm4 = det_int(matmul_transpose(A4))
    assert (z4, w4, norm4) == (2, 6, 16)
    z5 = sector_weight(A5, 2, True)
    w5 = sector_weight(A5, 2, False)
    norm5 = det_int(matmul_transpose(A5))
    assert (z5, w5, norm5) == (12, 22, 64)

    # The 2x2 example has Z_1=W_1=2 and grand normalizer 4.
    assert sector_weight(swap, 1, True) == 2
    assert sector_weight(swap, 1, False) == 2
    assert det_int(matmul_transpose(swap)) == 4

    print(json.dumps({
        "Q_swap_terms_zero_based": q_terms,
        "Q_swap_upper_half_plane_witness_value": [str(v) for v in q_witness],
        "Q_swap_rayleigh_delta_at_real_ones": q_rayleigh_at_ones,
        "C4_pair_activity_coefficients_zero_based": {
            f"{i},{j}": c for (i, j), c in pair_terms.items()
        },
        "C4_full_sector_coefficients_zero_based": {
            f"{i},{j}": c for (i, j), c in full_sector_terms.items()
        },
        "C4_upper_half_plane_witness_value": [str(v) for v in f_witness],
        "C4_rayleigh_delta_at_real_ones": f_rayleigh_at_ones,
        "P5_k2_row_activity_coefficients_zero_based": {
            f"{i},{j}": c for (i, j), c in path_terms.items()
        },
        "P5_upper_half_plane_witness_value": [str(v) for v in path_value],
        "P5_rayleigh_data_at_positive_point": {
            "F": [str(v) for v in p], "d1": [str(v) for v in d1],
            "d4": [str(v) for v in d4], "d14": str(d14),
            "delta_1_4": [str(v) for v in delta14],
        },
        "C4_Z2_W2_grand_normalizer": [z4, w4, norm4],
        "P5_Z2_W2_grand_normalizer": [z5, w5, norm5],
        "checks": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
