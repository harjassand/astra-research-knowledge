#!/usr/bin/env python3
"""Exact finite checks supporting the period-nine bandwidth-two comparator.

The all-size argument is in PERIOD9_LEMMA.md.  This program checks its finite
period data and rational left inverses. It does not infer an all-size theorem
from numerical experiments, and does not test the whole treewidth-two class.
"""
from fractions import Fraction as F
from itertools import combinations
import json
import time

WORD = (0, 1, 2, 0, 3, 1, 0, 2, 3)


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)]
            for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def inverse(a):
    n = len(a)
    aug = [[F(v) for v in row] + [F(i == j) for j in range(n)]
           for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        v = aug[j][j]
        aug[j] = [x / v for x in aug[j]]
        for i in range(n):
            if i != j:
                v = aug[i][j]
                aug[i] = [x-v*y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def det(a):
    if not a:
        return F(1)
    if len(a) == 1:
        return F(a[0][0])
    return sum((-1)**j * F(a[0][j]) *
               det([row[:j] + row[j+1:] for row in a[1:]])
               for j in range(len(a)))


def main():
    started = time.perf_counter()
    p = len(WORD)
    assert all(WORD[i] != WORD[(i+d) % p]
               for i in range(p) for d in (1, 2))
    pairs = []
    for a, b in combinations(range(4), 2):
        positions = [i for i, c in enumerate(WORD) if c in (a, b)]
        gaps = [(positions[(i+1) % len(positions)] - positions[i]) % p
                for i in range(len(positions))]
        assert max(gaps) >= 3
        # Cut the cyclic list at a gap of >=3. Subsequent gaps of >=3
        # separate connected components in the infinite periodic support.
        start = (next(i for i, g in enumerate(gaps) if g >= 3) + 1) % len(gaps)
        lengths = []
        count = 1
        for step in range(len(gaps)):
            g = gaps[(start+step) % len(gaps)]
            if g >= 3:
                lengths.append(count)
                count = 1
            else:
                count += 1
        assert sum(lengths) == len(positions)
        assert max(lengths) <= 5
        pairs.append({"colors": [a, b], "positions": positions,
                      "cyclic_gaps": gaps, "component_vertex_counts": lengths})

    blocks = []
    for vertices in range(2, 6):
        edges = vertices-1
        incidence = [[F(i == j or i == j+1) for j in range(edges)]
                     for i in range(vertices)]
        gram = matmul(transpose(incidence), incidence)
        left = matmul(inverse(gram), transpose(incidence))
        assert matmul(left, incidence) == [[F(i == j) for j in range(edges)]
                                          for i in range(edges)]
        shifted = [[x - (F(3, 8) if i == j else 0)
                    for j, x in enumerate(row)]
                   for i, row in enumerate(gram)]
        minors = [det([row[:k] for row in shifted[:k]])
                  for k in range(1, edges+1)]
        assert all(x > 0 for x in minors)
        blocks.append({"vertices": vertices,
                       "left_inverse": [[str(x) for x in row] for row in left],
                       "gram_minus_3_over_8_identity_leading_minors":
                           [str(x) for x in minors]})

    result = {"status": "all exact finite checks passed", "period": list(WORD),
              "scope": "bandwidth at most two with supplied ordering, free diagonal",
              "query_count": 4, "row_norm": 1,
              "pairs": pairs, "blocks": blocks,
              "proved_constant_squared": "3+sqrt(5)",
              "rational_checker_constant_squared": "16/3",
              "measured_body_seconds": time.perf_counter() - started}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
