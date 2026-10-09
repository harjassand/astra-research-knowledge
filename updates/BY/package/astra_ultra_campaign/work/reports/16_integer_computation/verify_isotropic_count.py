#!/usr/bin/env python3
"""Small exact checks for the symplectic-span independent-set identity.

All arithmetic is integer arithmetic.  This is a finite sanity check, not a
proof of the general identity.
"""

from collections import defaultdict
from math import comb
from random import Random


def symplectic_dot(x, y, m):
    low = (1 << m) - 1
    xa, xb = x & low, (x >> m) & low
    ya, yb = y & low, (y >> m) & low
    return ((xa & yb).bit_count() + (xb & ya).bit_count()) & 1


def rref_basis(vectors, r):
    rows = list(vectors)
    pivots = []
    for col in reversed(range(r)):
        pivot = next((i for i in range(len(pivots), len(rows))
                      if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        i = len(pivots)
        rows[i], rows[pivot] = rows[pivot], rows[i]
        p = rows[i]
        for j in range(len(rows)):
            if j != i and ((rows[j] >> col) & 1):
                rows[j] ^= p
        pivots.append(col)
    rows = rows[:len(pivots)]
    order = sorted(range(len(pivots)), key=lambda i: -pivots[i])
    return tuple(rows[i] for i in order)


def span(basis):
    out = [0]
    for b in basis:
        out += [x ^ b for x in out]
    return frozenset(out)


def isotropic_spaces(r):
    assert r % 2 == 0
    m = r // 2
    by_dim = {0: [()]}
    for k in range(m):
        next_spaces = {}
        for basis in by_dim[k]:
            members = span(basis)
            for x in range(1 << r):
                if x in members:
                    continue
                if any(symplectic_dot(x, b, m) for b in basis):
                    continue
                child = rref_basis((*basis, x), r)
                next_spaces[child] = None
        by_dim[k + 1] = list(next_spaces)
    return by_dim


def independence_poly(labels, m):
    n = len(labels)
    out = [0] * (n + 1)
    for mask in range(1 << n):
        chosen = [i for i in range(n) if (mask >> i) & 1]
        if all(not symplectic_dot(labels[i], labels[j], m)
               for p, i in enumerate(chosen) for j in chosen[p + 1:]):
            out[len(chosen)] += 1
    return out


def compressed_poly(labels, by_dim, m):
    n = len(labels)
    out = [0] * (n + 1)
    for d, spaces in by_dim.items():
        for basis in spaces:
            members = span(basis)
            count = sum(x in members for x in labels)
            t = m - d
            coefficient = (-1 if t & 1 else 1) * (1 << (t * t))
            for j in range(count + 1):
                out[j] += coefficient * comb(count, j)
    return out


def compressed_max_weight(labels, weights, by_dim, m):
    best = 0
    for basis in by_dim[m]:
        members = span(basis)
        best = max(best, sum(max(w, 0) for x, w in zip(labels, weights)
                             if x in members))
    return best


def direct_max_weight(labels, weights, m):
    best = 0
    n = len(labels)
    for mask in range(1 << n):
        chosen = [i for i in range(n) if (mask >> i) & 1]
        if all(not symplectic_dot(labels[i], labels[j], m)
               for p, i in enumerate(chosen) for j in chosen[p + 1:]):
            best = max(best, sum(weights[i] for i in chosen))
    return best


def isotropic_count(t, q=2):
    # Number of d-spaces in a 2t-dimensional symplectic space.
    gaussian = [[0] * (t + 1) for _ in range(t + 1)]
    gaussian[0][0] = 1
    for a in range(1, t + 1):
        gaussian[a][0] = 1
        for d in range(1, a + 1):
            gaussian[a][d] = q ** d * gaussian[a - 1][d] + gaussian[a - 1][d - 1]
    result = []
    for d in range(t + 1):
        product = 1
        for i in range(d):
            product *= q ** (t - i) + 1
        result.append(gaussian[t][d] * product)
    return result


def main():
    rng = Random(20261010)
    for t in range(9):
        nums = isotropic_count(t)
        mobius_sum = sum(((-1) ** d) * (2 ** (d * (d - 1) // 2)) * nums[d]
                         for d in range(t + 1))
        assert mobius_sum == ((-1) ** t) * (2 ** (t * t)), (t, nums, mobius_sum)

    cases = 0
    for m in range(1, 4):
        r = 2 * m
        by_dim = isotropic_spaces(r)
        for n in range(0, 9):
            for _ in range(40):
                labels = [rng.randrange(1 << r) for _ in range(n)]
                direct = independence_poly(labels, m)
                compressed = compressed_poly(labels, by_dim, m)
                assert direct == compressed, (m, labels, direct, compressed)
                weights = [rng.randrange(-4, 8) for _ in range(n)]
                direct_max = direct_max_weight(labels, weights, m)
                compressed_max = compressed_max_weight(labels, weights, by_dim, m)
                assert direct_max == compressed_max, (m, labels, weights,
                                                       direct_max, compressed_max)
                cases += 1
    all_vectors_rank4 = list(range(1 << 4))
    rank4_spaces = isotropic_spaces(4)
    assert independence_poly(all_vectors_rank4, 2) == compressed_poly(
        all_vectors_rank4, rank4_spaces, 2)
    print(f"mobius identity: t=0..8 passed")
    print(f"polynomial and max-weight identities: {cases} random instances passed for symplectic ranks 2,4,6")
    print("full 16-vertex rank-4 symplectic instance: passed")
    print("isotropic subspace counts:", {r: sum(map(len, isotropic_spaces(r).values())) for r in (2, 4, 6)})


if __name__ == "__main__":
    main()
