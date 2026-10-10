#!/usr/bin/env python3
"""Finite sanity checks for the block-join Rips witness (not a proof).

For m blocks of three vertices, at scale c the Rips complex consists of
subsets using at most one vertex from each block.  This script enumerates that
complex, computes its mod-2 Betti numbers by bitset Gaussian elimination, and
checks the predicted simplex count and top Betti number 2**m.
"""

from itertools import product
import argparse


def gf2_rank(columns):
    """Rank of a binary matrix given by integer bitset columns."""
    pivots = {}
    for col in columns:
        x = col
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return len(pivots)


def join_discrete_triples(m):
    """Return simplices by dimension for the join of m 3-point sets."""
    by_dim = [[] for _ in range(m + 1)]
    for choice in product(range(4), repeat=m):
        simplex = tuple(3 * block + (v - 1)
                        for block, v in enumerate(choice) if v)
        if simplex:
            by_dim[len(simplex) - 1].append(simplex)
    return by_dim


def boundary_rank(simplices_k, simplices_km1):
    if not simplices_k:
        return 0
    index = {s: i for i, s in enumerate(simplices_km1)}
    columns = []
    for simplex in simplices_k:
        col = 0
        for j in range(len(simplex)):
            face = simplex[:j] + simplex[j + 1:]
            col ^= 1 << index[face]
        columns.append(col)
    return gf2_rank(columns)


def betti_numbers(by_dim):
    betti = []
    for k, simplices in enumerate(by_dim):
        rank_dk = (boundary_rank(simplices, by_dim[k - 1]) if k else 0)
        rank_dkp1 = (boundary_rank(by_dim[k + 1], simplices)
                     if k + 1 < len(by_dim) else 0)
        betti.append(len(simplices) - rank_dk - rank_dkp1)
    while betti and betti[-1] == 0:
        betti.pop()
    return betti


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=4)
    args = parser.parse_args()
    if args.max_m < 1 or args.max_m > 5:
        raise SystemExit("Use 1 <= --max-m <= 5; enumeration is exponential.")

    for m in range(1, args.max_m + 1):
        by_dim = join_discrete_triples(m)
        count = sum(map(len, by_dim))
        betti = betti_numbers(by_dim)
        # Convert ordinary H_0 to reduced H_0 for the join formula.
        betti[0] -= 1
        expected = [0] * m
        expected[m - 1] = 2 ** m
        assert count == 4 ** m - 1, (m, count)
        assert betti == expected, (m, betti, expected)
        print(f"m={m}: simplices={count}; Betti={betti}; PASS")


if __name__ == "__main__":
    main()
