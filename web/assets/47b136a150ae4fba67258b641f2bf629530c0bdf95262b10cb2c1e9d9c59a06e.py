"""Exact counterexample to density-proportional rank-leaf pruning.

Uses only the Python standard library. No numerical tolerances or random tests.
All 64 coefficients of the 2x2 matrix multiplication tensor are checked.
"""

from fractions import Fraction as F
from itertools import product


def mat(v):
    return [v[:2], v[2:]]


def flatten(a):
    return a[0] + a[1]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def inv(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert d
    return [[F(a[1][1], d), F(-a[0][1], d)],
            [F(-a[1][0], d), F(a[0][0], d)]]


def transformed_form(a, left, right):
    result = []
    for j in range(4):
        basis = [0] * 4
        basis[j] = 1
        z = flatten(mm(mm(left, mat(basis)), right))
        result.append(sum(x * y for x, y in zip(a, z)))
    return result


# Strassen's standard rank-seven decomposition, row-major coordinates.
A = [[1, 0, 0, 1], [0, 0, 1, 1], [1, 0, 0, 0],
     [0, 0, 0, 1], [1, 1, 0, 0], [-1, 0, 1, 0], [0, 1, 0, -1]]
B = [[1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, -1],
     [-1, 0, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [0, 0, 1, 1]]
C = [[1, 0, 0, 1], [0, 0, 1, -1], [0, 1, 0, 1],
     [1, 0, 1, 0], [-1, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0]]

P = [[7, 5], [1, 2]]
Q = [[6, 6], [5, 1]]
R = [[5, 5], [4, 1]]

# X' = P X Q^{-1}; Y' = Q Y R^{-1}; XY = P^{-1}(X'Y')R.
AA = [transformed_form(a, P, inv(Q)) for a in A]
BB = [transformed_form(b, Q, inv(R)) for b in B]
CC = [flatten(mm(mm(inv(P), mat(c)), R)) for c in C]

assert all(value != 0 for leg in (AA, BB, CC)
           for row in leg for value in row)

for i, j, h in product(range(4), repeat=3):
    x, y = [0] * 4, [0] * 4
    x[i], y[j] = 1, 1
    expected = flatten(mm(mat(x), mat(y)))[h]
    actual = sum(AA[l][i] * BB[l][j] * CC[l][h] for l in range(7))
    assert actual == expected, (i, j, h, actual, expected)

print("PASS: all 64 exact tensor coefficients")
print("PASS: all 84 leg coefficients are nonzero")
print("P =", P, "Q =", Q, "R =", R)
for name, leg in (("A", AA), ("B", BB), ("C", CC)):
    print(name, [[str(value) for value in row] for row in leg])

for k in range(1, 5):
    # Every tensor-product coefficient is a product of k nonzero rationals.
    full_input_coordinates = 4 ** k
    full_rank_leaves = 7 ** k
    sparse_support = 1
    active_leaves = full_rank_leaves
    density_prediction = F(sparse_support * full_rank_leaves,
                           full_input_coordinates)
    assert active_leaves > density_prediction
    print(f"k={k}: one supported input touches {active_leaves} leaves; "
          f"density-proportional prediction {density_prediction}")
