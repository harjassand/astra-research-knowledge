#!/usr/bin/env python3
"""Finite exhaustive checks of the threshold-mask identities in v1.txt."""
from itertools import combinations, chain
from math import comb


def subsets(items):
    items = tuple(items)
    return chain.from_iterable(combinations(items, r) for r in range(len(items) + 1))


def coeff(s, k):
    if s < k:
        return 0
    return (-1) ** (s - k) * comb(s - 1, k - 1)


def local_expansion(f, k):
    return sum(comb(f, s) * coeff(s, k) for s in range(k, f + 1))


def union_expansion(F, rounds, k):
    # Evaluate the scalar coefficient of W_F in the inclusion-exclusion/cylinder sum.
    total = 0
    for J in subsets(range(rounds)):
        if not J:
            continue
        subtotal = 1
        for j in J:
            f_j = sum(x // 10 == j for x in F)
            subtotal *= local_expansion(f_j, k)
        total += (-1) ** (len(J) + 1) * subtotal
    return total


def main():
    for N in range(1, 8):
        for k in range(1, N + 1):
            for f in range(N + 1):
                assert local_expansion(f, k) == int(f >= k), (N, k, f)
            for eta in (0.01, 0.2, 1.0):
                beta = sum(comb(N, s) * comb(s - 1, k - 1) * eta**s
                           for s in range(k, N + 1))
                b = comb(N, k) * eta**k * (1 + eta) ** (N - k)
                assert beta <= b + 1e-12, (N, k, eta, beta, b)

    # Two and three disjoint rounds, each with N=3 locations, represented as
    # 10*j + local_index so every exact global mask can be enumerated.
    for rounds in (2, 3):
        N = 3
        locations = tuple(10 * j + i for j in range(rounds) for i in range(N))
        for k in range(1, N + 1):
            for F in subsets(locations):
                expected = int(any(sum(x // 10 == j for x in F) >= k
                                   for j in range(rounds)))
                actual = union_expansion(F, rounds, k)
                assert actual == expected, (rounds, k, F, actual, expected)
    print("PASS: local and multiround threshold-mask identities; beta <= b")


if __name__ == "__main__":
    main()
