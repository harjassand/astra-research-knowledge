#!/usr/bin/env python3
"""Independent finite checks of hidden-block coordinate stability.

This is an exact algebra validator, not the asymptotic phase-count engine.
Only Python's standard library is used; the established local ANF utility
module is imported from the previous construction.
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'work_dense_cont'))
from cubic_structure_compiler import (substitute, brute, independent, apply,
                                      indices, xor_all)


def transpose(a):
    n = len(a)
    return [sum(((a[j] >> i) & 1) << j for j in range(n)) for i in range(n)]


def mul(a, b):
    return [apply(a, c) for c in b]


def congruence(a, t):
    return mul(mul(transpose(t), a), t)


def off(a):
    return [x & ~(1 << i) for i, x in enumerate(a)]


def rank(a):
    return len(independent(a))


def qpoly(a):
    return {(1 << i) | (1 << j) for i in range(len(a))
            for j in range(i + 1, len(a)) if (a[j] >> i) & 1}


def polar(p, n):
    a = [0] * n
    for s in p:
        if s.bit_count() == 2:
            i, j = indices(s)
            a[i] ^= 1 << j
            a[j] ^= 1 << i
    return a


def random_invertible(n, rng, blocks=None):
    a = [1 << i for i in range(n)]
    if blocks is None:
        blocks = [list(range(n))]
    for block in blocks:
        for _ in range(12 * len(block)):
            i, j = rng.sample(block, 2)
            if rng.randrange(3):
                a[i] ^= a[j]
            else:
                a[i], a[j] = a[j], a[i]
    assert rank(a) == n
    return a


def invert(a):
    n = len(a)
    rows = [transpose(a)[i] | (1 << (n + i)) for i in range(n)]
    for i in range(n):
        j = next(j for j in range(i, n) if (rows[j] >> i) & 1)
        rows[i], rows[j] = rows[j], rows[i]
        for j in range(n):
            if j != i and (rows[j] >> i) & 1:
                rows[j] ^= rows[i]
    return transpose([row >> n for row in rows])


def main():
    rng = random.Random(20261027)
    stability = []
    dense_disguises = []
    count_checks = 0
    diagonal_correction_nonzero = 0
    row_type_blowups = []
    for c in (4, 8, 16):
        labels = []
        transformed_labels = []
        for i in range(c):
            for j in range(i + 1, c):
                labels.extend((1 << i, 1 << j, 0))
                transformed_labels.extend(((1 << i) ^ (1 << j), 1 << j, 0))
        n = len(labels)
        old = [sum(((a & b).bit_count() & 1) << j
                   for j, b in enumerate(labels)) for a in labels]
        new = [sum(((a & b).bit_count() & 1) << j
                   for j, b in enumerate(transformed_labels))
               for a in transformed_labels]
        assert rank(old) == rank(new) == c
        assert len(set(old)) == c + 1
        assert len(set(new)) == c * (c - 1) // 2 + c
        row_type_blowups.append(dict(n=n, rank=c, old_row_types=len(set(old)),
                                    new_row_types=len(set(new)), block_width=3))
    for n in (6, 9, 12):
        blocks = [list(range(i, i + 3)) for i in range(0, n, 3)]
        cubics = {sum(1 << j for j in block) for block in blocks}
        for trial in range(12):
            r = 1 + trial % 3
            u = [rng.randrange(1 << n) for _ in range(r)]
            # D = U U^T permits a genuinely unknown nonzero diagonal.
            d = [xor_all(v for v in u if (v >> i) & 1) for i in range(n)]
            s = [0] * n
            edges = rng.sample([(i, j) for i in range(n)
                                for j in range(i + 1, n)], n // 2)
            for i, j in edges:
                s[i] ^= 1 << j
                s[j] ^= 1 << i
            t = random_invertible(n, rng, blocks)
            dt = congruence(d, t)
            diagonal = [d[i] & (1 << i) for i in range(n)]
            correction = off(congruence(diagonal, t))
            st = congruence(s, t)
            transformed = substitute(qpoly(off(d)) ^ qpoly(s), n, t)
            observed = polar(transformed, n)
            expected = [x ^ y ^ z for x, y, z in zip(off(dt), correction, st)]
            assert observed == expected
            assert rank(dt) == rank(d) <= r
            extra = len(qpoly(correction))
            assert extra <= n
            for i in range(n):
                assert all(i // 3 == j // 3 for j in indices(correction[i]))
            edge_count = len(qpoly(st))
            assert edge_count <= 9 * len(edges)
            diagonal_correction_nonzero += bool(extra)
            stability.append(dict(n=n, trial=trial, rank=rank(d),
                                  initial_edges=len(edges),
                                  transformed_edges=edge_count,
                                  diagonal_local_edges=extra))

            # Scramble the FULL ANF. Its cubic terms generate quadratic
            # leakage on Boolean reduction, so transforming only the old
            # quadratic matrix is invalid.
            a = random_invertible(n, rng)
            shift = rng.randrange(1 << n)
            hidden = substitute(cubics, n, a, shift)
            ai = invert(a)
            inverse_shift = apply(ai, shift)
            recovered = substitute(hidden, n, ai, inverse_shift)
            assert recovered == cubics
            old_quad = {s for s in hidden if s.bit_count() == 2}
            wrong_recovered_quad = polar(substitute(old_quad, n, ai,
                                                    inverse_shift), n)
            assert polar(recovered, n) == [0] * n
            raw_rank = rank(polar(hidden, n))
            wrong_rank = rank(wrong_recovered_quad)
            dense_disguises.append(dict(n=n, trial=trial,
                                       raw_cubic_terms=sum(s.bit_count() == 3 for s in hidden),
                                       raw_quadratic_rank=raw_rank,
                                       shortcut_wrong_rank=wrong_rank,
                                       constant=0 in hidden))
            if trial < 3:
                assert brute(hidden, n) == brute(cubics, n)
                count_checks += 1
    result = dict(stability_checks=len(stability),
                  nonzero_diagonal_corrections=diagonal_correction_nonzero,
                  dense_affine_roundtrips=len(dense_disguises),
                  shortcut_failures=sum(bool(x['shortcut_wrong_rank'])
                                        for x in dense_disguises),
                  full_rank_raw_quadratics=sum(x['raw_quadratic_rank'] == x['n']
                                              for x in dense_disguises),
                  exact_count_checks=count_checks,
                  row_type_blowups=row_type_blowups,
                  stability=stability, dense_disguises=dense_disguises)
    path = Path(__file__).with_name('hidden_cubic_coordinate_results.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('stability', 'dense_disguises')}, indent=2))


if __name__ == '__main__':
    main()
