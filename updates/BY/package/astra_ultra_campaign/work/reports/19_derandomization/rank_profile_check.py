"""Exact rank-profile counterexample for a coefficient-cut invariant.

For each variable subset S, form the coefficient matrix whose rows index
monomials on S and columns index monomials on its complement. The script
computes its rank over Q for two distinct multilinear polynomials.
"""

from fractions import Fraction
from itertools import combinations


N = 4
POLYNOMIALS = {
    "f=x1*x2+x3*x4": {
        (1, 1, 0, 0): 1,
        (0, 0, 1, 1): 1,
    },
    "g=x1*x3+x2*x4": {
        (1, 0, 1, 0): 1,
        (0, 1, 0, 1): 1,
    },
}


def exact_rank(matrix):
    matrix = [[Fraction(entry) for entry in row] for row in matrix]
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][col]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row != pivot_row and matrix[row][col]:
                factor = matrix[row][col]
                matrix[row] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def coefficient_matrix(polynomial, subset):
    subset = tuple(subset)
    complement = tuple(i for i in range(N) if i not in subset)
    row_monomials = sorted({tuple(m[i] for i in subset) for m in polynomial})
    col_monomials = sorted({tuple(m[i] for i in complement) for m in polynomial})
    matrix = []
    for row_monomial in row_monomials:
        row = []
        for col_monomial in col_monomials:
            exponent = [0] * N
            for i, power in zip(subset, row_monomial):
                exponent[i] = power
            for i, power in zip(complement, col_monomial):
                exponent[i] = power
            row.append(polynomial.get(tuple(exponent), 0))
        matrix.append(row)
    return matrix


for size in range(N + 1):
    for subset in combinations(range(N), size):
        label = "".join(str(i + 1) for i in subset) or "empty"
        ranks = [
            exact_rank(coefficient_matrix(polynomial, subset))
            for polynomial in POLYNOMIALS.values()
        ]
        print(f"{label:>5}: {ranks[0]} {ranks[1]}")
