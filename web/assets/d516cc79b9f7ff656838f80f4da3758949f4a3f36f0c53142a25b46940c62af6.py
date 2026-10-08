#!/usr/bin/env python3
"""Exact finite falsifier for extending the N68 s=2 tuple to dense degree 2.

Uses only Python integers. It constructs the prescribed N68 affine matrices for
n=5, s=2, evaluates a nonzero 5-term commutative polynomial through its
canonical ordered lift, and verifies the complete 4x4 response is zero.
It also computes the rank/nullity of the full degree<=2 monomial-image map.
"""

from itertools import product
import json
from pathlib import Path


def zero(d):
    return [[0] * d for _ in range(d)]


def eye(d):
    a = zero(d)
    for i in range(d):
        a[i][i] = 1
    return a


def mmul(a, b):
    d = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(d)) for j in range(d)]
            for i in range(d)]


def mpow(a, k):
    out = eye(len(a))
    base = a
    while k:
        if k & 1:
            out = mmul(out, base)
        base = mmul(base, base)
        k >>= 1
    return out


def n68_tuple(n, s):
    d = 2 * s
    bbase = n + 1
    out = []
    for letter in range(1, n + 1):
        a = zero(d)
        for row in range(d):
            for col in range(row, d):
                # binom(col,row) * B^row * letter^(col-row)
                from math import comb
                a[row][col] = comb(col, row) * bbase**row * letter**(col-row)
        out.append(a)
    return out


def eval_monomial(mats, alpha):
    out = eye(len(mats[0]))
    for a, exponent in zip(mats, alpha):
        out = mmul(out, mpow(a, exponent))
    return out


def mat_add_scaled(acc, a, scale):
    return [[acc[i][j] + scale * a[i][j] for j in range(len(acc))]
            for i in range(len(acc))]


def rref_rank(matrix):
    # Exact fraction-free Gauss elimination is unnecessary at this tiny size;
    # use Python Fraction to make the rank computation auditable.
    from fractions import Fraction
    a = [[Fraction(x) for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        q = a[rank][col]
        a[rank] = [x / q for x in a[rank]]
        for r in range(rows):
            if r != rank and a[r][col]:
                q = a[r][col]
                a[r] = [a[r][j] - q * a[rank][j] for j in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def main():
    n, s, degree = 5, 2, 2
    d = 2 * s
    mats = n68_tuple(n, s)

    # Polynomial:
    #   60 x3*x4 - 91 x3*x5 + 156 x4^2 - 130 x4*x5 + 5 x5^2
    # Coefficients use zero-based exponent vectors in x1,...,x5.
    witness = {
        (0, 0, 1, 1, 0): 60,
        (0, 0, 1, 0, 1): -91,
        (0, 0, 0, 2, 0): 156,
        (0, 0, 0, 1, 1): -130,
        (0, 0, 0, 0, 2): 5,
    }
    assert len(witness) == 5
    assert any(witness.values())
    assert max(sum(alpha) for alpha in witness) == degree

    response = zero(d)
    for alpha, coeff in witness.items():
        response = mat_add_scaled(response, eval_monomial(mats, alpha), coeff)
    assert response == zero(d)

    # Build vectorized images of every commutative monomial of degree <=2.
    monomials = [alpha for alpha in product(range(degree + 1), repeat=n)
                 if sum(alpha) <= degree]
    assert len(monomials) == 21
    images = [eval_monomial(mats, alpha) for alpha in monomials]
    # 16 rows (matrix entries), 21 columns (monomials).
    linear_map = [[images[j][i][k]
                   for j in range(len(images))]
                  for i in range(d) for k in range(d)]
    rank = rref_rank(linear_map)
    nullity = len(monomials) - rank
    assert rank == 8
    assert nullity == 13

    # The free commutator has zero abelianization but a nonzero invertible
    # 2x2 evaluation, so free PIT is not a commutative-quotient test.
    x = [[0, 1], [0, 0]]
    y = [[0, 0], [1, 0]]
    xy = mmul(x, y)
    yx = mmul(y, x)
    commutator = [[xy[i][j] - yx[i][j] for j in range(2)] for i in range(2)]
    assert commutator == [[1, 0], [0, -1]]

    receipt = {
        "claim_scope": "one finite exact N68 tuple; not a theorem-level PIT lower bound",
        "n": n,
        "s_parameter": s,
        "matrix_dimension": d,
        "response_entries": d * d,
        "total_degree_bound": degree,
        "commutative_polynomial_space_dimension": len(monomials),
        "monomial_image_map_rows": d * d,
        "monomial_image_map_rank_over_Q": rank,
        "kernel_dimension_over_Q": nullity,
        "witness_coefficients": [
            {"exponent_vector": list(alpha), "coefficient": coeff}
            for alpha, coeff in sorted(witness.items())
        ],
        "witness_support": len(witness),
        "witness_is_nonzero": True,
        "witness_exceeds_promised_support": len(witness) > s,
        "full_matrix_response": response,
        "response_is_zero": True,
        "commutator_abelianization_is_zero": True,
        "commutator_matrix_response": commutator,
        "commutator_response_is_invertible": True,
        "arithmetic": "exact integers and rational row reduction",
    }
    out = Path(__file__).with_name("receipt.json")
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
