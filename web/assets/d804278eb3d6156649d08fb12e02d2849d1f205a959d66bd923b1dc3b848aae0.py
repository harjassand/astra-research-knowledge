"""Exact small-instance check of a row-norm-refined refresh bound."""

from fractions import Fraction
from itertools import combinations, permutations
from math import comb
import json


def det_int(matrix):
    n = len(matrix)
    total = 0
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = (-1 if inv % 2 else 1)
        for i in range(n):
            term *= matrix[i][p[i]]
        total += term
    return total


def main():
    F = [
        [0, 1, 2, 0],
        [1, 0, 1, 2],
        [2, 1, 0, 1],
        [0, 2, 1, 0],
    ]
    r = len(F)
    lambdas = [Fraction(1), Fraction(2), Fraction(1, 2), Fraction(3)]
    h = [sum(F[i][j] ** 2 for j in range(r)) for i in range(r)]
    alpha = [lambdas[i] * h[i] for i in range(r)]

    coordinate_lines = []
    for i in range(r):
        for j in range(i + 1, r):
            a = [0] * r
            b = [0] * r
            a[i], b[j] = 1, 1
            coordinate_lines.append(("coord", (a, b)))
    original_lines = []
    for i in range(r):
        e = [0] * r
        e[i] = 1
        row = list(F[i])
        original_lines.append(("orig", (e, row), lambdas[i]))

    M0 = len(coordinate_lines)
    lines = coordinate_lines + original_lines
    half = r // 2
    actual_contaminant_at_epsilon_one = Fraction(0)
    counted = 0
    for chosen in combinations(range(len(lines)), half):
        chosen_lines = [lines[j] for j in chosen]
        s = sum(line[0] == "orig" for line in chosen_lines)
        if s == 0:
            continue
        cols = []
        activity = Fraction(1)
        for line in chosen_lines:
            if line[0] == "coord":
                cols.extend(line[1])
            else:
                cols.extend(line[1])
                activity *= line[2]
        W = [[cols[j][i] for j in range(r)] for i in range(r)]
        d = det_int(W)
        actual_contaminant_at_epsilon_one += activity * d * d
        counted += 1

    # S = sum_s binom(M0, r/2-s) e_s(lambda_i * ||f_i||^2).
    S = Fraction(0)
    for s in range(1, half + 1):
        elementary = Fraction(0)
        for I in combinations(range(r), s):
            prod = Fraction(1)
            for i in I:
                prod *= alpha[i]
            elementary += prod
        S += comb(M0, half - s) * elementary
    assert actual_contaminant_at_epsilon_one <= S

    Z0 = 1
    for j in range(1, r, 2):
        Z0 *= j
    eta = Fraction(1, 32)
    K = 0
    while S / (1 << K) > eta * Z0:
        K += 1
    epsilon = Fraction(1, 1 << K)

    actual_contaminant = Fraction(0)
    for chosen in combinations(range(len(lines)), half):
        chosen_lines = [lines[j] for j in chosen]
        s = sum(line[0] == "orig" for line in chosen_lines)
        if s == 0:
            continue
        cols = []
        activity = epsilon ** s
        for line in chosen_lines:
            if line[0] == "coord":
                cols.extend(line[1])
            else:
                cols.extend(line[1])
                activity *= line[2]
        W = [[cols[j][i] for j in range(r)] for i in range(r)]
        d = det_int(W)
        actual_contaminant += activity * d * d
    assert actual_contaminant <= epsilon * S <= eta * Z0

    print(json.dumps({
        "dimension": r,
        "coordinate_lines": M0,
        "original_lines": len(original_lines),
        "enumerated_original_containing_line_sets": counted,
        "row_squared_norms": h,
        "exact_contaminant_at_epsilon_one": str(actual_contaminant_at_epsilon_one),
        "exact_row_norm_bound_S": str(S),
        "coordinate_partition_Z0": Z0,
        "refresh_budget_eta": str(eta),
        "chosen_epsilon": f"2^-{K}",
        "actual_contaminant_at_epsilon": str(actual_contaminant),
        "bound_epsilon_S": str(epsilon * S),
        "scope": "finite exact fixture; general Hadamard derivation is in path_and_ratios.txt",
    }, indent=2))


if __name__ == "__main__":
    main()
