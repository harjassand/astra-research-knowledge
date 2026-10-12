#!/usr/bin/env python3
"""Exact finite checks for the accompanying research record.

Standard-library only. These checks are not substitutes for the general proofs.
Run: python verify.py --output VERIFICATION.json
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
import json
from math import comb, factorial, prod
from pathlib import Path
import time


def exact_rank(matrix: list[list[int | Fraction]]) -> int:
    """Gaussian elimination over the rational numbers, without tolerances."""
    if not matrix:
        return 0
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError('Ragged matrix')
    a = [[Fraction(x) for x in row] for row in matrix]
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pv = a[rank][col]
        for i in range(rank + 1, len(a)):
            if not a[i][col]:
                continue
            ratio = a[i][col] / pv
            for j in range(col, width):
                a[i][j] -= ratio * a[rank][j]
        rank += 1
        if rank == len(a):
            break
    return rank


def subsets(mask: int):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & mask


def kernel_checks() -> list[dict]:
    out = []
    for n in range(1, 6):
        for lam in (1, 2, 8):
            d = [Fraction((-1)**k * factorial(k) * lam**k,
                          prod(1 + lam*j for j in range(k + 1)))
                 for k in range(n + 1)]
            for k in range(n + 1):
                finite_difference = sum(
                    (Fraction((-1)**(k-j) * comb(k, j), 1 + lam*j)
                     for j in range(k + 1)), Fraction(0))
                assert finite_difference == d[k] and d[k] != 0
            kernel = [[Fraction(1, 1 + lam*(s & t).bit_count())
                       for t in range(1 << n)] for s in range(1 << n)]
            for s in range(1 << n):
                for t in range(1 << n):
                    assert kernel[s][t] == sum(
                        (d[u.bit_count()] for u in subsets(s & t)), Fraction(0))
            rank = exact_rank(kernel)
            assert rank == 1 << n
            if lam == 8:
                error = max(abs(kernel[s][t] - int((s & t) == 0))
                            for s in range(1 << n) for t in range(1 << n))
                assert error <= Fraction(1, 9)
            out.append({'n': n, 'lambda': lam, 'rank': rank,
                        'mobius_factorization': True})
    return out


def canonical_instance(n: int, lam: int):
    # Core rows, difference rows, equal-pair rows.
    pairs = [(i, a) for i in range(n) for a in range(lam)]
    rows = [('c', s) for s in range(1 << n)]
    rows += [('d', i, a) for i, a in pairs]
    rows += [('e', i, a) for i, a in pairs]
    basis = [('b0',)] + [('bp', i, a) for i, a in pairs]
    basis += [('bm', i, a) for i, a in pairs]
    cols = basis + [('t', t) for t in range(1 << n)]

    def v(row, label):
        if label[0] == 'b0':
            return int(row[0] == 'c')
        i, a = label[1:]
        if row[0] == 'c':
            return int(bool(row[1] & (1 << i)))
        if row[1:] != (i, a):
            return 0
        return int(row[0] == 'e' or label[0] == 'bp')

    def entry(row, col):
        if col[0] != 't':
            return v(row, col)
        t = col[1]
        return (v(row, ('b0',)) +
                sum(v(row, ('bp', i, a)) - v(row, ('bm', i, a))
                    for i, a in pairs if t & (1 << i)))

    positive, negative = [], []
    for b in basis:
        a_set = frozenset(i for i, row in enumerate(rows) if v(row, b))
        col_set = {cols.index(b)}
        if b[0] == 'b0':
            col_set.update(j for j, col in enumerate(cols) if col[0] == 't')
        elif b[0] == 'bp':
            col_set.update(j for j, col in enumerate(cols)
                           if col[0] == 't' and col[1] & (1 << b[1]))
        positive.append((a_set, frozenset(col_set)))
        if b[0] == 'bm':
            negative.append((a_set, frozenset(
                j for j, col in enumerate(cols)
                if col[0] == 't' and col[1] & (1 << b[1]))))
    matrix = [[entry(row, col) for col in cols] for row in rows]

    # A small, explicit disjoint positive partition.
    partition = [(frozenset(i for i, row in enumerate(rows) if row[0] == 'c'),
                  frozenset(j for j, col in enumerate(cols)
                            if col[0] in ('b0', 't')))]
    for b in basis[1:]:
        partition.append((frozenset(i for i, row in enumerate(rows) if v(row, b)),
                          frozenset({cols.index(b)})))
    for coordinate in range(n):
        partition.append((frozenset(i for i, row in enumerate(rows)
                                    if row[0] == 'd' and row[1] == coordinate),
                          frozenset(j for j, col in enumerate(cols)
                                    if col[0] == 't' and col[1] & (1 << coordinate))))
    return rows, cols, basis, matrix, positive, negative, partition


def incidence(rectangles, x, y):
    return sum(x in a and y in b for a, b in rectangles)


def canonical_checks() -> list[dict]:
    result = []
    for n, lam in ((1, 1), (2, 1), (3, 1), (4, 1), (2, 8), (3, 8)):
        rows, cols, basis, matrix, positive, negative, partition = canonical_instance(n, lam)
        assert len(set(positive + negative)) == len(positive) + len(negative)
        assert len(positive) + len(negative) == 1 + 3*n*lam
        assert len(partition) == 1 + 2*n*lam + n
        for x in range(len(rows)):
            for y in range(len(cols)):
                assert matrix[x][y] in (0, 1)
                assert incidence(positive, x, y) - incidence(negative, x, y) == matrix[x][y]
                assert incidence(partition, x, y) == matrix[x][y]
                if rows[x][0] == 'c' and cols[y][0] == 't':
                    expected = Fraction(1, 1 + lam*(rows[x][1] & cols[y][1]).bit_count())
                    assert Fraction(matrix[x][y], incidence(positive, x, y)) == expected
        expected_rank = 1 + 2*n*lam
        assert exact_rank(matrix) == expected_rank
        assert exact_rank([row[:len(basis)] for row in matrix]) == expected_rank
        result.append({'n': n, 'lambda': lam, 'rank': expected_rank,
                       'signed_length': len(positive) + len(negative),
                       'positive_partition_size': len(partition),
                       'actual_column_basis': True, 'no_duplicate_rectangles': True})
    return result


def compile_partition(positive, negative, nx: int, ny: int):
    p, q = len(positive), len(negative)
    rectangles = []
    for s in range(1 << q):
        active = [j for j in range(q) if s & (1 << j)]
        xs = {x for x in range(nx)
              if all((x in negative[j][0]) == bool(s & (1 << j)) for j in range(q))}
        for t in range(min(len(active), p - 1) + 1):
            ys = {y for y in range(ny) if sum(y in negative[j][1] for j in active) == t}
            for witness in combinations(range(p), t + 1):
                a = frozenset(x for x in xs if all(x in positive[i][0] for i in witness))
                b = frozenset(y for y in ys if all(y in positive[i][1] for i in witness))
                if a and b:
                    rectangles.append((a, b))
    return rectangles


def compiler_checks() -> dict:
    nonempty_subsets = [frozenset(i for i in range(2) if mask & (1 << i)) for mask in range(1, 4)]
    possible_rectangles = list(product(nonempty_subsets, repeat=2))
    examined = valid = 0
    max_output = 0
    for p in range(4):
        for q in range(3):
            for pi in combinations_with_replacement(range(9), p):
                positive = [possible_rectangles[i] for i in pi]
                for ni in combinations_with_replacement(range(9), q):
                    negative = [possible_rectangles[i] for i in ni]
                    examined += 1
                    matrix = [[incidence(positive, x, y) - incidence(negative, x, y)
                               for y in range(2)] for x in range(2)]
                    if any(z not in (0, 1) for row in matrix for z in row):
                        continue
                    valid += 1
                    out = compile_partition(positive, negative, 2, 2)
                    bound = 2**q * sum(comb(p, k) for k in range(1, min(q + 1, p) + 1))
                    assert len(out) <= bound
                    assert all(incidence(out, x, y) == matrix[x][y]
                               for x in range(2) for y in range(2))
                    max_output = max(max_output, len(out))
    return {'multisets_examined': examined, 'boolean_cases_verified': valid,
            'p_range': [0, 3], 'q_range': [0, 2], 'matrix_shape': [2, 2],
            'largest_nonempty_output': max_output}


def atomic_checks() -> list[dict]:
    result = []
    for m in range(1, 5):
        n = 2*m
        domain = [s for s in range(1 << n) if s.bit_count() in (m, m + 1)]
        max_pure = 0
        for pattern in product((-1, 0, 1), repeat=n):
            # -1 is an unspecified membership bit; 0 and 1 specify a literal.
            inside = [s for s in domain if all(v == -1 or bool(s & (1 << i)) == bool(v)
                                              for i, v in enumerate(pattern))]
            if inside and all(s.bit_count() == m + 1 for s in inside):
                max_pure = max(max_pure, len(inside))
        assert max_pure == 1
        result.append({'m': m, 'largest_pure_literal_atom': max_pure,
                       'necessary_atoms': comb(2*m, m + 1), 'unrestricted_partition_size': 1})
    return result


def priority_checks() -> list[dict]:
    result = []
    for n in range(1, 6):
        for bad in range(1 << n):
            matrix = [[int(not (s & t & bad)) for t in range(1 << n)]
                      for s in range(1 << n)]
            assert exact_rank(matrix) == 2**bad.bit_count()
        expected = Fraction(2**(n + 1) - 1, n + 1)
        result.append({'n': n, 'all_priority_subsets_verified': 1 << n,
                       'expected_residual_rank': str(expected)})
    return result


def cycle_check() -> dict:
    matrix = [[int((j - i) % 4 in (0, 1)) for j in range(4)] for i in range(4)]
    rank = exact_rank(matrix)
    assert rank == 3
    supports = [frozenset(i for i in range(4) if matrix[i][j]) for j in range(4)]
    assert all(not (a < b or b < a) for a, b in combinations(supports, 2))
    ranks_after = []
    for a in range(1, 16):
        for b in range(1, 16):
            cells = [(i, j) for i in range(4) for j in range(4)
                     if a & (1 << i) and b & (1 << j)]
            if not all(matrix[i][j] for i, j in cells):
                continue
            residue = [row[:] for row in matrix]
            for i, j in cells:
                residue[i][j] -= 1
            ranks_after.append(exact_rank(residue))
    assert min(ranks_after) == 3
    return {'input_rank': rank, 'no_nested_columns': True,
            'positive_rectangles_checked': len(ranks_after),
            'residual_ranks': sorted(set(ranks_after))}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('VERIFICATION.json'))
    args = parser.parse_args()
    started = time.monotonic()
    report = {'status': 'PASS', 'arithmetic': 'exact rational/integer; no floating rank tests',
              'kernel': kernel_checks(), 'canonical_basis': canonical_checks(),
              'small_negative_compiler': compiler_checks(), 'atomic_refinement': atomic_checks(),
              'priority': priority_checks(), 'cycle_obstruction': cycle_check()}
    report['elapsed_seconds'] = round(time.monotonic() - started, 3)
    report['scope'] = 'Finite diagnostics only. General proofs and external dependencies are in RESEARCH_RECORD.md.'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
