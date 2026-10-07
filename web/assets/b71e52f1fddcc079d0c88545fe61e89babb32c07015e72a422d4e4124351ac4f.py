#!/usr/bin/env python3
"""Exact small-instance check of the mismatch-retaining Plucker exchange."""

from itertools import combinations
import json
from pathlib import Path


def det_bareiss(matrix):
    a = [list(row) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k] != 0), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[n - 1][n - 1]


def column_matrix(columns, n, f):
    out = [[0] * len(columns) for _ in range(n)]
    for j, (kind, index) in enumerate(columns):
        if kind == "I":
            out[index][j] = 1
        else:
            for i in range(n):
                out[i][j] = f[i][index]
    return out


def paired_basis(i_set, j_set, n):
    # Columns of [I_n | F] for det([I_{I^c}, F_J]) = +/- det F[I,J].
    return ([('I', i) for i in range(n) if i not in i_set]
            + [('F', j) for j in j_set])


def is_target_basis(columns, n, k):
    identity_indices = {i for kind, i in columns if kind == "I"}
    f_indices = {i for kind, i in columns if kind == "F"}
    holes = set(range(n)) - identity_indices
    return (len(f_indices) == k and len(holes) == k
            and holes.isdisjoint(f_indices))


def main():
    # F is the directed 4-cycle permutation: each column j is e_(j+1 mod 4).
    n, k = 4, 2
    f = [[int(i == (j + 1) % n) for j in range(n)] for i in range(n)]
    target = []
    for i_set in combinations(range(n), k):
        for j_set in combinations(range(n), k):
            if set(i_set).isdisjoint(j_set):
                cols = paired_basis(set(i_set), set(j_set), n)
                d = det_bareiss(column_matrix(cols, n, f))
                if d:
                    target.append((tuple(i_set), tuple(j_set), cols, d))
    assert len(target) == 2
    assert sorted(abs(row[3]) for row in target) == [1, 1]

    # No nontrivial one-column exchange between the two target paired bases.
    direct_target_edges = 0
    for _, _, a, _ in target:
        for _, _, b, _ in target:
            if a == b:
                continue
            for pos, e in enumerate(a):
                for fcol in b:
                    if fcol in a:
                        continue
                    a2 = list(a)
                    a2[pos] = fcol
                    d2 = det_bareiss(column_matrix(a2, n, f))
                    if d2 and is_target_basis(a2, n, k):
                        direct_target_edges += 1
    assert direct_target_edges == 0

    identity_checks = 0
    max_terms = 0
    mismatched_nonzero_terms = 0
    for _, _, a, da in target:
        for _, _, b, db in target:
            for pos, e in enumerate(a):
                if e in b:
                    continue
                b_only = [x for x in b if x not in a]
                signed_sum = 0
                square_sum = 0
                nonzero_terms = 0
                for fcol in b_only:
                    bpos = b.index(fcol)
                    a2 = list(a)
                    b2 = list(b)
                    a2[pos] = fcol
                    b2[bpos] = e
                    da2 = det_bareiss(column_matrix(a2, n, f))
                    db2 = det_bareiss(column_matrix(b2, n, f))
                    signed_sum += da2 * db2
                    square_sum += (da2 * db2) ** 2
                    if da2 and db2:
                        nonzero_terms += 1
                        if not (is_target_basis(a2, n, k)
                                and is_target_basis(b2, n, k)):
                            mismatched_nonzero_terms += 1
                assert signed_sum == da * db
                assert (da * db) ** 2 <= len(b_only) * square_sum
                assert nonzero_terms > 0
                max_terms = max(max_terms, len(b_only))
                identity_checks += 1

    result = {
        "matrix": "4-cycle permutation",
        "n": n,
        "sector_k": k,
        "target_microstates": [
            {"I": list(i_set), "J": list(j_set), "det_basis": d}
            for i_set, j_set, _, d in target
        ],
        "target_support_size": len(target),
        "direct_target_one_column_exchange_edges": direct_target_edges,
        "signed_plucker_identity_checks": identity_checks,
        "maximum_exchange_terms": max_terms,
        "nonzero_terms_outside_target_fiber": mismatched_nonzero_terms,
        "result": "PASS",
        "scope": "exact integer fixtures only; universal identity is proved in INITIAL.txt",
    }
    out = Path(__file__).with_name("basis_exchange_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
