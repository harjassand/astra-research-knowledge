#!/usr/bin/env python3
"""Exact small-instance checks for localized weighted hole-sector inequalities.

This checks coefficient support and Newton inequalities for the theorem in
INITIAL.txt. It does not certify real-rootedness in general.
"""
from fractions import Fraction
from itertools import permutations, product
from math import comb
from random import Random
import json
from pathlib import Path


def gadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def determinant_gaussian(matrix):
    n = len(matrix)
    if n == 0:
        return (1, 0)
    total = (0, 0)
    for perm in permutations(range(n)):
        inv = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = (1, 0)
        for i, j in enumerate(perm):
            term = gmul(term, matrix[i][j])
        total = gadd(total, (-term[0], -term[1]) if inv % 2 else term)
    return total


def hole_partition(F, U):
    n = len(F)
    R = [i for i in range(n) if not (U >> i) & 1]
    if len(R) % 2:
        return 0
    k = len(R) // 2
    total = 0
    for I_mask in range(1 << len(R)):
        if I_mask.bit_count() != k:
            continue
        I = [R[a] for a in range(len(R)) if (I_mask >> a) & 1]
        J = [R[a] for a in range(len(R)) if not ((I_mask >> a) & 1)]
        det = determinant_gaussian([[F[i][j] for j in J] for i in I])
        total += det[0] * det[0] + det[1] * det[1]
    return total


def all_hole_partitions(F):
    n = len(F)
    return [hole_partition(F, U) if U.bit_count() % 2 == 0 else 0
            for U in range(1 << n)]


def add_coordinate_pair_auxiliary(f, n, i, j, activity):
    out = []
    ib, jb = 1 << i, 1 << j
    for U, value in enumerate(f):
        if U.bit_count() % 2 or (U & ib) or (U & jb):
            out.append(value)
        else:
            out.append(value + activity * f[U | ib | jb])
    return out


def check_localizations(f, n, activities, tag):
    checked = 0
    zero_fibres = 0
    max_degree = 0
    for status in product((0, 1, 2), repeat=n):
        forced = sum(1 << i for i, s in enumerate(status) if s == 0)
        forbidden = sum(1 << i for i, s in enumerate(status) if s == 1)
        free = [i for i, s in enumerate(status) if s == 2]
        coeff = [Fraction(0) for _ in range(n // 2 + 1)]
        for W_sub in range(1 << len(free)):
            W = 0
            wt = Fraction(1)
            for a, i in enumerate(free):
                if (W_sub >> a) & 1:
                    W |= 1 << i
                    wt *= activities[i]
            U = forced | W
            if U.bit_count() % 2 == 0:
                coeff[U.bit_count() // 2] += f[U] * wt
        nz = [k for k, c in enumerate(coeff) if c]
        if not nz:
            zero_fibres += 1
            continue
        lo, hi = nz[0], nz[-1]
        assert nz == list(range(lo, hi + 1)), (tag, status, coeff)
        seq = coeff[lo:hi + 1]
        d = len(seq) - 1
        for k in range(1, d):
            lhs = (seq[k] / comb(d, k)) ** 2
            rhs = (seq[k - 1] / comb(d, k - 1)) * (seq[k + 1] / comb(d, k + 1))
            assert lhs >= rhs, (tag, status, coeff, k)
        checked += 1
        max_degree = max(max_degree, d)
    return {"tag": tag, "checked_nonzero_fibres": checked,
            "zero_fibres": zero_fibres, "max_reduced_degree": max_degree}


def random_matrix(n, rng, sparse=False):
    F = []
    for _ in range(n):
        row = []
        for _ in range(n):
            if sparse and rng.random() < 0.62:
                row.append((0, 0))
            else:
                row.append((rng.randint(-2, 2), rng.randint(-2, 2)))
        F.append(row)
    return F


def paired_matrix(n, pairs):
    F = [[(0, 0) for _ in range(n)] for _ in range(n)]
    for i, j in pairs:
        F[i][j] = (1, 0)
    return F


def main():
    rng = Random(20261007)
    n = 6
    matrices = {
        "dense_gaussian_integer": random_matrix(n, rng),
        "sparse_gaussian_integer": random_matrix(n, rng, sparse=True),
        "three_disjoint_directed_pairs": paired_matrix(n, [(0, 1), (2, 3), (4, 5)]),
        "diagonal_boundary_case": [[(int(i == j), 0) for j in range(n)] for i in range(n)],
    }
    activity_vectors = {
        "positive": [Fraction(i + 1, 2) for i in range(n)],
        "boundary_zeros": [Fraction(0 if i % 3 == 0 else i + 1, 2) for i in range(n)],
    }
    results = []
    for name, F in matrices.items():
        f = all_hole_partitions(F)
        for activity_name, x in activity_vectors.items():
            results.append(check_localizations(f, n, x, f"{name}:{activity_name}"))
        if name in {"dense_gaussian_integer", "three_disjoint_directed_pairs"}:
            f_aux = add_coordinate_pair_auxiliary(f, n, 0, 3, Fraction(1, 3))
            results.append(check_localizations(f_aux, n, activity_vectors["boundary_zeros"],
                                               f"{name}:aux_0_3_activity_1_3"))
    summary = {
        "scope": "finite exact diagnostics only; proof is in INITIAL.txt",
        "dimension": n,
        "localization_fixtures": results,
        "total_nonzero_fibres": sum(r["checked_nonzero_fibres"] for r in results),
        "total_zero_fibres": sum(r["zero_fibres"] for r in results),
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
