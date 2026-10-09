#!/usr/bin/env python3
"""Finite search over local group-sum plus residual-label representations.

For each candidate decomposition, the operational code sends the residual-label
pair by Slepian-Wolf coding, then sends a common linear syndrome of each local
group label. The decoder combines the syndromes and decodes their group sum
using the residual labels as side information. This search is only over the
stated representation class; it is not a converse for arbitrary codes.
"""

from collections import defaultdict
from itertools import product
from math import log2

from latin_intercalate_hybrid import EPSILON, LATIN, Q, entropy

BASE = {
    (0, 1): 0.45,
    (0, 3): 0.05,
    (1, 1): 0.05,
    (1, 3): 0.45,
}
WEIGHTS = {
    (x, y): (1.0 - EPSILON) * BASE.get((x, y), 0.0) + EPSILON / (Q * Q)
    for x in range(Q)
    for y in range(Q)
}


def partitions(n):
    """Return all set partitions as canonical restricted-growth strings."""
    out = []

    def extend(prefix, maximum):
        if len(prefix) == n:
            out.append(tuple(prefix))
            return
        for value in range(maximum + 2):
            extend(prefix + [value], max(maximum, value))

    extend([0], 0)
    return out


def partitions_containing(n, pair):
    return [p for p in partitions(n) if p[pair[0]] == p[pair[1]]]


def valid_decomposition(a, b, tx, ty, modulus):
    outputs = {}
    for x in range(Q):
        for y in range(Q):
            group_sum = (a[x] + b[y]) % modulus
            key = (tx[x], ty[y], group_sum)
            z = LATIN[x][y]
            if key in outputs and outputs[key] != z:
                return False
            outputs[key] = z
    return True


def rate(a, b, tx, ty, modulus):
    p_t = defaultdict(float)
    p_gt = defaultdict(float)
    for (x, y), mass in WEIGHTS.items():
        group_sum = (a[x] + b[y]) % modulus
        t = (tx[x], ty[y])
        p_t[t] += mass
        p_gt[group_sum, tx[x], ty[y]] += mass
    h_t = entropy(p_t.values())
    h_gt = entropy(p_gt.values())
    return h_t + 2.0 * (h_gt - h_t), h_t, h_gt - h_t


def search_binary():
    all_partitions = partitions(Q)
    best = (float("inf"), None)
    valid = 0
    for a in product(range(2), repeat=Q):
        for b in product(range(2), repeat=Q):
            for tx in all_partitions:
                for ty in all_partitions:
                    if not valid_decomposition(a, b, tx, ty, 2):
                        continue
                    valid += 1
                    candidate = rate(a, b, tx, ty, 2)
                    if candidate[0] < best[0] - 1e-12:
                        best = (candidate[0], (a, b, tx, ty, candidate[1:]))
    return valid, best


def search_z4_intercalate():
    # The selected 2x2 output table is [[0,1],[1,0]]. Its Z4 image must
    # differ by the order-two element 2 in both local labels.
    tx_parts = partitions_containing(Q, (0, 1))
    ty_parts = partitions_containing(Q, (1, 3))
    best = (float("inf"), None)
    valid = 0
    for other_a in product(range(4), repeat=3):
        a = (0, 2, *other_a)
        for other_b in product(range(4), repeat=3):
            it = iter(other_b)
            b = tuple(0 if y == 1 else 2 if y == 3 else next(it) for y in range(Q))
            for tx in tx_parts:
                for ty in ty_parts:
                    if not valid_decomposition(a, b, tx, ty, 4):
                        continue
                    valid += 1
                    candidate = rate(a, b, tx, ty, 4)
                    if candidate[0] < best[0] - 1e-12:
                        best = (candidate[0], (a, b, tx, ty, candidate[1:]))
    return valid, best


def main():
    binary_valid, binary_best = search_binary()
    z4_valid, z4_best = search_z4_intercalate()
    print(f"binary valid decompositions: {binary_valid}")
    print(f"binary best sum rate: {binary_best[0]:.12f}")
    print(f"binary best labels/partitions: {binary_best[1]}")
    print(f"Z4 intercalate valid decompositions: {z4_valid}")
    print(f"Z4 intercalate best sum rate: {z4_best[0]:.12f}")
    print(f"Z4 best labels/partitions: {z4_best[1]}")


if __name__ == "__main__":
    main()
