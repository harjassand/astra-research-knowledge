#!/usr/bin/env python3
"""Exact small-instance replay for the N68/N51 interface audit.

Uses only Python's standard library. This is finite evidence, not a proof of
the universal statements in RESULT.txt.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def zero_matrix(d: int):
    return [[0 for _ in range(d)] for _ in range(d)]


def identity(d: int):
    return [[int(i == j) for j in range(d)] for i in range(d)]


def matmul(x, y):
    d = len(x)
    return [
        [sum(x[i][q] * y[q][j] for q in range(d)) for j in range(d)]
        for i in range(d)
    ]


def add_scaled(dst, src, scalar):
    d = len(dst)
    for i in range(d):
        for j in range(d):
            dst[i][j] += scalar * src[i][j]


def affine_tuple(n: int, t: int):
    d = 2 * t
    base = n + 1
    matrices = []
    for letter in range(1, n + 1):
        matrix = zero_matrix(d)
        for a in range(d):
            for b in range(a, d):
                matrix[a][b] = math.comb(b, a) * base**a * letter ** (b - a)
        matrices.append(matrix)
    return matrices


def code_word(word, n: int) -> int:
    base = n + 1
    length = len(word)
    return base**length + sum(letter * base ** (length - q - 1) for q, letter in enumerate(word))


def word_matrix(word, matrices):
    d = len(matrices[0])
    result = identity(d)
    for letter in word:
        result = matmul(result, matrices[letter - 1])
    return result


def polynomial_matrix(terms, matrices):
    d = len(matrices[0])
    result = [[Fraction(0) for _ in range(d)] for _ in range(d)]
    for word, coefficient in terms.items():
        add_scaled(result, word_matrix(word, matrices), Fraction(coefficient))
    return result


def is_zero(matrix):
    return all(value == 0 for row in matrix for value in row)


def replay_sparse_class():
    n, t = 2, 3
    alphabet_words = [()]
    for length in (1, 2):
        alphabet_words.extend(itertools.product(range(1, n + 1), repeat=length))
    matrices = affine_tuple(n, t)
    # Check the affine action and injective code on every word of length <= 2.
    d = 2 * t
    row_ones = [1] * d
    codes = [code_word(word, n) for word in alphabet_words]
    assert len(set(codes)) == len(codes)
    for word in alphabet_words:
        row = row_ones[:]
        for letter in word:
            row = [
                sum(row[a] * matrices[letter - 1][a][b] for a in range(d))
                for b in range(d)
            ]
        expected = [code_word(word, n) ** q for q in range(d)]
        assert row == expected

    tested = 0
    for support_size in range(1, t + 1):
        for support in itertools.combinations(alphabet_words, support_size):
            for signs in itertools.product((-1, 1), repeat=support_size):
                terms = dict(zip(support, signs))
                assert not is_zero(polynomial_matrix(terms, matrices))
                tested += 1
    rational_terms = {
        (): Fraction(5, 11),
        (1,): Fraction(1, 2),
        (2, 1): Fraction(-3, 7),
    }
    assert not is_zero(polynomial_matrix(rational_terms, matrices))
    return {
        "n": n,
        "support_bound_t": t,
        "dimension": d,
        "words_tested_for_affine_code": len(alphabet_words),
        "nonzero_sparse_polynomials_tested": tested,
        "signed_rational_coefficient_fixture": "PASS",
        "all_exact_checks": "PASS",
    }


def replay_formula_blowup():
    cases = []
    for k in range(1, 9):
        words = {
            tuple(choice)
            for choice in itertools.product(*[(2 * j + 1, 2 * j + 2) for j in range(k)])
        }
        tree_size = 2 * k + k + (k - 1)
        assert tree_size == 4 * k - 1
        assert len(words) == 2**k
        cases.append(
            {
                "k": k,
                "formula_tree_vertices": tree_size,
                "degree": k,
                "distinct_words": len(words),
                "exact_check": "PASS",
            }
        )
    return cases


def replay_n68_response_mismatch():
    n, t = 1, 2
    matrix = affine_tuple(n, t)[0]
    d = 2 * t
    ident = identity(d)
    x_minus_one = [[matrix[i][j] - ident[i][j] for j in range(d)] for i in range(d)]
    x_minus_two = [[matrix[i][j] - 2 * ident[i][j] for j in range(d)] for i in range(d)]
    diagonal = [matrix[i][i] for i in range(d)]
    assert diagonal == [1, 2, 4, 8]
    assert not is_zero(x_minus_one) and x_minus_one[0][0] == 0
    assert not is_zero(x_minus_two) and x_minus_two[1][1] == 0
    scalar_inverse_at_zero = Fraction(1, 0 - 2)
    return {
        "n": n,
        "t": t,
        "diagonal_of_A1": diagonal,
        "x_minus_one_response_nonzero": not is_zero(x_minus_one),
        "x_minus_one_response_singular_witness_zero_diagonal": x_minus_one[0][0] == 0,
        "inverse_operand_A1_minus_2I_singular_witness_zero_diagonal": x_minus_two[1][1] == 0,
        "(x-2)^-1_at_scalar_0": str(scalar_inverse_at_zero),
        "exact_check": "PASS",
    }


def n51_large_branch_parameters():
    n = B = 1
    w = n + 1
    delta = 4 * w**3 * B
    M = 1
    while M <= B * delta:
        M *= 2
    d = M * (M // 2)
    E0 = 3 * M**2 * (w + M + 1)
    T0 = B * d * (d * E0 + 1)
    K = max(M, B * T0 + 2)
    grid = (K + 1) ** 5
    return {
        "n": n,
        "B": B,
        "w": w,
        "Delta": delta,
        "M": M,
        "d": d,
        "E0": E0,
        "T0": T0,
        "K": K,
        "five_grid_tuple_count": str(grid),
        "generator_executed": False,
        "interpretation": "parameter calculation only; no N51 list was generated",
    }


def replay_n51_domain_witness():
    # A small explicit two-point list. Choose one eigenvalue from each scalar
    # first-variable matrix; the inverse of their product is undefined at both.
    eigenvalues = (1, 2)
    def denominator(x):
        out = 1
        for lam in eigenvalues:
            out *= x - lam
        return out
    at_list = [denominator(lam) for lam in eigenvalues]
    at_zero = denominator(0)
    assert at_list == [0, 0]
    assert at_zero == 2
    return {
        "list_first_variable_eigenvalues": list(eigenvalues),
        "denominator_values_at_list": at_list,
        "denominator_at_scalar_0": at_zero,
        "inverse_defined_nonzero_at_scalar_0": Fraction(1, at_zero) != 0,
        "formula_size_for_h_2": 4 * len(eigenvalues),
        "exact_check": "PASS",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = {
        "status": "FINITE-EVIDENCE",
        "sparse_one_query_replay": replay_sparse_class(),
        "formula_size_vs_support": replay_formula_blowup(),
        "n68_invertibility_and_domain_mismatch": replay_n68_response_mismatch(),
        "n51_list_domain_adversary": replay_n51_domain_witness(),
        "n51_large_branch_parameters": n51_large_branch_parameters(),
        "scope": "These exact small checks do not validate universal source theorems or run the N51 generator.",
    }
    Path(args.output).write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
