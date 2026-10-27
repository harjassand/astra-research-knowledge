#!/usr/bin/env python3
"""Finite check of the independent-space barrier for disjoint cubic triples.

The proof uses Gowers's direct-sum slice-rank theorem. This validator
enumerates all subspaces at the first forbidden dimension, not just
coordinate subspaces or a sample of disguises.
"""
import itertools
import json
import random
from pathlib import Path


def spaces(n, d):
    # Unique reduced-row-echelon bases, with pivots in increasing order.
    for pivots in itertools.combinations(range(n), d):
        free = [j for j in range(n) if j not in pivots]
        entries = [(i, j) for i, pivot in enumerate(pivots)
                   for j in free if j > pivot]
        for mask in range(1 << len(entries)):
            rows = [1 << pivot for pivot in pivots]
            for k, (i, j) in enumerate(entries):
                if (mask >> k) & 1:
                    rows[i] |= 1 << j
            yield rows


def volume(a, b, c):
    return sum(((a >> i) & 1) * ((b >> j) & 1) * ((c >> k) & 1)
               for i, j, k in itertools.permutations(range(3))) & 1


VOL = [[[volume(a, b, c) for c in range(8)] for b in range(8)]
       for a in range(8)]


def evaluate(a, b, c, blocks):
    out = 0
    for _ in range(blocks):
        out ^= VOL[a & 7][b & 7][c & 7]
        a >>= 3
        b >>= 3
        c >>= 3
    return out


def is_independent(basis, blocks):
    return not any(evaluate(a, b, c, blocks)
                   for a, b, c in itertools.combinations(basis, 3))


def gaussian_binomial(n, d):
    num = den = 1
    for i in range(d):
        num *= (1 << (n - i)) - 1
        den *= (1 << (d - i)) - 1
    assert num % den == 0
    return num // den


def main():
    results = []
    rng = random.Random(20261027)
    for blocks in (1, 2, 3):
        n = 3 * blocks
        forbidden = 2 * blocks + 1
        checked = independent = 0
        for basis in spaces(n, forbidden):
            checked += 1
            independent += is_independent(basis, blocks)
        assert checked == gaussian_binomial(n, forbidden)
        assert independent == 0
        witness = [1 << (3 * j + k) for j in range(blocks) for k in (0, 1)]
        assert len(witness) == 2 * blocks
        assert is_independent(witness, blocks)
        # Exhaust all X-shifts; if its derivative is affine then there is
        # exactly one Z-mask that could yield a Pauli stabilizer.
        pauli = []
        for trial in range(3):
            edges = [(i, j) for i in range(n) for j in range(i + 1, n)
                     if trial and rng.randrange(2)]
            unary = rng.randrange(1 << n) if trial else 0
            values = []
            for x in range(1 << n):
                value = sum(((x >> (3 * j)) & 7) == 7 for j in range(blocks))
                value += sum(((x >> i) & 1) * ((x >> j) & 1) for i, j in edges)
                value += (x & unary).bit_count()
                values.append(value & 1)
            stabilizing_shifts = []
            for a in range(1 << n):
                constant = values[a] ^ values[0]
                b = sum((values[(1 << i) ^ a] ^ values[1 << i] ^ constant) << i
                        for i in range(n))
                if all((values[x ^ a] ^ values[x]) ==
                       (constant ^ ((x & b).bit_count() & 1))
                       for x in range(1 << n)):
                    stabilizing_shifts.append([a, b])
            assert stabilizing_shifts == [[0, 0]]
            pauli.append(dict(quadratic_edges=len(edges), x_shifts_exhausted=1 << n,
                              stabilizing_masks=stabilizing_shifts, nullity=n))
        results.append(dict(n=n, forbidden_dimension=forbidden,
                            subspaces_exhausted=checked, independent=independent,
                            optimal_dimension=2 * blocks, witness_basis=witness,
                            pauli_checks=pauli))
    path = Path(__file__).with_name('independent_space_barrier_results.json')
    path.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
