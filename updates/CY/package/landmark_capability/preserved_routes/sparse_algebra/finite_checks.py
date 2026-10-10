"""Finite checks for sparse_transfer.py (stdlib only)."""

from __future__ import annotations

import json
import random

from sparse_transfer import SparseMatrix, direct_term, transfer_term


def dense_power_term(A: SparseMatrix, u, v, exponent: int) -> int:
    """Independent O(N^3 log exponent) reference for small matrices."""
    n, p = A.n, A.p
    dense = [[0] * n for _ in range(n)]
    for i, row in enumerate(A.rows):
        for j, value in row:
            dense[i][j] = value

    def multiply(X, Y):
        return [
            [sum(X[i][k] * Y[k][j] for k in range(n)) % p for j in range(n)]
            for i in range(n)
        ]

    result = [[int(i == j) for j in range(n)] for i in range(n)]
    base = dense
    e = exponent
    while e:
        if e & 1:
            result = multiply(result, base)
        e >>= 1
        if e:
            base = multiply(base, base)
    Av = [sum(result[i][j] * v[j] for j in range(n)) % p for i in range(n)]
    return sum(u[i] * Av[i] for i in range(n)) % p


def all_vectors(p, n):
    if n == 0:
        yield ()
        return
    for prefix in all_vectors(p, n - 1):
        for a in range(p):
            yield prefix + (a,)


def main():
    p = 3
    vectors = list(all_vectors(p, 2))
    exhaustive = 0
    order_hist = {}
    for flat in all_vectors(p, 4):
        entries = [(i // 2, i % 2, value) for i, value in enumerate(flat) if value]
        A = SparseMatrix.from_entries(2, p, entries)
        for u in vectors:
            for v in vectors:
                exhaustive += 1
                # Cover the initial segment by repeated direct multiplication.
                for exponent in range(10):
                    actual, C = transfer_term(A, u, v, exponent)
                    expected = direct_term(A, u, v, exponent)
                    assert actual == expected, (A, u, v, exponent, actual, expected, C)
                order = len(C) - 1
                order_hist[order] = order_hist.get(order, 0) + 1

    # Random sparse and dense cases, including enormous binary-encoded indices.
    rng = random.Random(20261010)
    random_cases = 0
    for n, density, count in ((3, 0.25, 80), (5, 0.45, 80), (7, 0.15, 40)):
        for _ in range(count):
            entries = []
            for i in range(n):
                for j in range(n):
                    if rng.random() < density:
                        entries.append((i, j, rng.randrange(p)))
            A = SparseMatrix.from_entries(n, p, entries)
            u = [rng.randrange(p) for _ in range(n)]
            v = [rng.randrange(p) for _ in range(n)]
            exponent = 10**75 + rng.randrange(10**6)
            actual, C = transfer_term(A, u, v, exponent)
            expected = dense_power_term(A, u, v, exponent)
            assert actual == expected, (n, A, u, v, exponent, actual, expected, C)
            random_cases += 1

    # Hand-picked cancellation checks: same-eigenvalue annihilation and a
    # nonzero sequence whose first scalar term vanishes.
    equal_diag = SparseMatrix.from_entries(2, 101, [(0, 0, 1), (1, 1, 1)])
    assert transfer_term(equal_diag, [1, -1], [1, 1], 10**100)[0] == 0
    unequal_diag = SparseMatrix.from_entries(2, 101, [(0, 0, 1), (1, 1, 2)])
    assert transfer_term(unequal_diag, [1, -1], [1, 1], 10**100)[0] == dense_power_term(
        unequal_diag, [1, -1], [1, 1], 10**100
    )
    assert transfer_term(unequal_diag, [1, -1], [1, 1], 0)[0] == 0
    assert transfer_term(unequal_diag, [1, -1], [1, 1], 1)[0] == 100

    print(
        json.dumps(
            {
                "field": "F_3 exhaustive; F_3/F_101 hand cases",
                "exhaustive_2x2_A_u_v_cases": exhaustive,
                "direct_exponents_per_exhaustive_case": 10,
                "random_large_index_cases": random_cases,
                "random_index_bits": 250,
                "scalar_recurrence_order_histogram_exhaustive": order_hist,
                "cancellation_checks": 4,
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

