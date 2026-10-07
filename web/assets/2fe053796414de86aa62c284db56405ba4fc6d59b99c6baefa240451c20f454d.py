#!/usr/bin/env python3
"""Exact finite diagnostics for coordinate/total-count covariance bounds.

This does not prove the general theorem in revisions/total_covariance_extension.txt.
It checks localized fibers of bounded signed-hole examples using exact
Fraction arithmetic, including zero coordinate activities and empty fibers.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
from random import Random
import json

from weighted_hole_localization_checks import (
    add_coordinate_pair_auxiliary,
    all_hole_partitions,
    paired_matrix,
    random_matrix,
)


def diagnostics(f, n, activities, taus, tag):
    checked = 0
    empty_coefficient = 0
    empty_weighted_tau = 0
    min_cov = None
    max_cov_minus_var = None
    min_cov_minus_var = None
    for status in product((0, 1, 2), repeat=n):
        forced = sum(1 << i for i, s in enumerate(status) if s == 0)
        forbidden = sum(1 << i for i, s in enumerate(status) if s == 1)
        free = [i for i, s in enumerate(status) if s == 2]
        support = []
        for choice in range(1 << len(free)):
            U = forced
            activity = Fraction(1)
            for k, i in enumerate(free):
                if (choice >> k) & 1:
                    U |= 1 << i
                    activity *= activities[i]
            if U & forbidden or U.bit_count() % 2 or f[U] == 0:
                continue
            K = U.bit_count() // 2
            support.append((U, K, f[U] * activity))

        if not support:
            empty_coefficient += 1
            continue

        for tau in taus:
            masses = [(U, K, a * tau**K) for U, K, a in support]
            Z = sum(a for _, _, a in masses)
            if Z == 0:
                # A boundary activity can annihilate a fiber that was
                # coefficient-nonempty before activities were applied.
                empty_weighted_tau += 1
                continue
            EK = sum(a * K for _, K, a in masses) / Z
            for i in free:
                EI = sum(a for U, _, a in masses if (U >> i) & 1) / Z
                EIK = sum(a * K for U, K, a in masses if (U >> i) & 1) / Z
                cov = EIK - EI * EK
                var_i = EI * (1 - EI)
                assert cov >= 0, (tag, status, tau, i, cov)
                assert cov <= var_i, (tag, status, tau, i, cov, var_i)
                min_cov = cov if min_cov is None else min(min_cov, cov)
                gap = cov - var_i
                max_cov_minus_var = gap if max_cov_minus_var is None else max(max_cov_minus_var, gap)
                min_cov_minus_var = gap if min_cov_minus_var is None else min(min_cov_minus_var, gap)
                checked += 1
    return {"tag": tag, "coordinate_tau_checks": checked,
            "empty_coefficient_fibres": empty_coefficient,
            "annihilated_weighted_fibre_tau_checks": empty_weighted_tau,
            "minimum_covariance": str(min_cov) if min_cov is not None else None,
            "maximum_covariance_minus_indicator_variance": str(max_cov_minus_var)
            if max_cov_minus_var is not None else None,
            "minimum_covariance_minus_indicator_variance": str(min_cov_minus_var)
            if min_cov_minus_var is not None else None}


def pair_covariance(f, n, i, j, activities):
    masses = []
    for U, coeff in enumerate(f):
        if coeff == 0:
            continue
        a = Fraction(coeff)
        for k in range(n):
            if (U >> k) & 1:
                a *= activities[k]
        masses.append((U, a))
    Z = sum(a for _, a in masses)
    Ei = sum(a for U, a in masses if (U >> i) & 1) / Z
    Ej = sum(a for U, a in masses if (U >> j) & 1) / Z
    Eij = sum(a for U, a in masses if ((U >> i) & 1) and ((U >> j) & 1)) / Z
    return Eij - Ei * Ej


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
    taus = [Fraction(1, 3), Fraction(1), Fraction(3)]
    results = []
    for name, F in matrices.items():
        f = all_hole_partitions(F)
        for activity_name, activities in activity_vectors.items():
            results.append(diagnostics(f, n, activities, taus,
                                       f"{name}:{activity_name}"))
        if name in {"dense_gaussian_integer", "three_disjoint_directed_pairs"}:
            f_aux = add_coordinate_pair_auxiliary(f, n, 0, 3, Fraction(1, 3))
            results.append(diagnostics(f_aux, n, activity_vectors["boundary_zeros"], taus,
                                       f"{name}:aux_0_3_activity_1_3"))

    F4 = [[(1, -1), (0, 0), (2, 1), (0, 0)],
          [(2, -2), (0, 0), (0, 0), (0, 0)],
          [(0, 0), (0, 0), (1, -2), (0, 0)],
          [(0, 0), (0, 1), (0, 0), (0, 0)]]
    f4 = all_hole_partitions(F4)
    pair_cov = pair_covariance(f4, 4, 0, 3, [Fraction(1)] * 4)
    assert pair_cov == Fraction(-1, 50)

    summary = {
        "scope": "finite exact diagnostics only; proof is in revisions/total_covariance_extension.txt",
        "dimension": n,
        "global_fugacities": [str(t) for t in taus],
        "localization_fixtures": results,
        "total_coordinate_tau_checks": sum(r["coordinate_tau_checks"] for r in results),
        "negative_pair_covariance_control": {
            "dimension": 4,
            "hole_coefficients": f4,
            "pair": [0, 3],
            "activities": [1, 1, 1, 1],
            "covariance": str(pair_cov),
            "purpose": "The total-count covariance theorem is not pairwise positive association.",
        },
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
