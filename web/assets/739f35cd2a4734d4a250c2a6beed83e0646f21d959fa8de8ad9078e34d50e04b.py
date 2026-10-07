#!/usr/bin/env python3
"""Exact variance audit on dense rational perturbations of swap matchings.

The imported implementation is a local copy of c01_s03's phase-two program;
all output is written by the caller into this worker's revisions directory.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import importlib.util
import json
from math import comb, lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
COPIED_PROGRAM = HERE / "low_sector_sampler_copy.py"
spec = importlib.util.spec_from_file_location("copied_low_sector_sampler", COPIED_PROGRAM)
sampler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sampler)


def inversion_sign(perm):
    inv = sum(perm[i] > perm[j] for i in range(len(perm))
              for j in range(i + 1, len(perm)))
    return -1 if inv % 2 else 1


def det_int(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    return sum(inversion_sign(p) *
               __import__("math").prod(matrix[i][p[i]] for i in range(n))
               for p in permutations(range(n)))


def direct_disjoint_minor_sum(g, k):
    n = len(g)
    total = 0
    for rows in combinations(range(n), k):
        row_set = set(rows)
        for cols in combinations([j for j in range(n) if j not in row_set], k):
            total += det_int([[g[i][j] for j in cols] for i in rows]) ** 2
    return total


def phased_draw(problem, signs, k):
    """Evaluate c03_s01's alternating real/imaginary site-sign X_k exactly."""
    n = problem.n
    phases = [(s, 0) if i % 2 == 0 else (0, s)
              for i, s in enumerate(signs)]
    a = []
    for i in range(n):
        row = []
        for j in range(n):
            left = sampler.mul(phases[i], problem.g[i][j])
            right = sampler.mul(phases[j], problem.g[j][i])
            row.append(sampler.add(left, sampler.scale(right, -1)))
        a.append(row)
    return sampler.pfaffian_norm_coefficient(a, k)


def build_near_matching(n, delta):
    assert n % 2 == 0
    k = n // 2
    f = []
    for i in range(n):
        row = []
        for j in range(n):
            matching = int(j == (i ^ 1))
            row.append(Q(matching) + delta)
        f.append(row)
    return f, delta, k


def one_instance(n, delta, label):
    f, delta, k = build_near_matching(n, delta)
    problem = sampler.LowSector(f)
    m = 1 << n
    xs = []
    phased_xs = []
    for bits in product((-1, 1), repeat=n):
        xs.append(problem.prefix_draw_integer(k, bits))
        phased_xs.append(phased_draw(problem, bits, k))
    assert len(xs) == m
    g = [[entry[0] for entry in row] for row in problem.g]
    assert all(entry[1] == 0 for row in problem.g for entry in row)
    c_direct = direct_disjoint_minor_sum(g, k)
    expected_c = 2**k * (problem.denominator**k * (1 + k*delta))**2
    assert expected_c.denominator == 1
    assert c_direct == expected_c.numerator
    sum_x = sum(xs)
    sum_x2 = sum(x*x for x in xs)
    assert sum_x == m * c_direct, (n, sum_x, m*c_direct)
    relative_variance = Q(sum_x2, m*c_direct*c_direct) - 1
    phased_sum = sum(phased_xs)
    phased_sum2 = sum(x*x for x in phased_xs)
    assert phased_sum == m * c_direct, (n, phased_sum, m*c_direct)
    assert all(x == c_direct for x in phased_xs)
    raw_positive = [x for x in xs if x]
    expected_positive_value = 4**k * (problem.denominator**k * (1 + k*delta))**2
    assert len(raw_positive) == 2**k
    assert all(x == expected_positive_value for x in raw_positive)
    assert set(xs) <= {0, expected_positive_value}
    phased_relative_variance = Q(phased_sum2, m*c_direct*c_direct) - 1
    assert relative_variance == 2**k - 1
    assert phased_relative_variance == 0
    beta = [problem.g[i][i+1][0]**2 + problem.g[i+1][i][0]**2
            for i in range(0, n, 2)]
    baseline = __import__("math").prod(beta)
    assert all(3*baseline <= 4*x and 3*x <= 4*baseline for x in phased_xs)
    beta_min = 2 * (1 + delta) ** 2
    residual_frobenius_sq = n * (n - 2) * delta * delta
    certificate_threshold = beta_min / (256 * k * k)
    certificate_accepts = residual_frobenius_sq <= certificate_threshold
    certificate_ratio = residual_frobenius_sq / certificate_threshold
    if label == "inside_certified_near_matching":
        assert certificate_accepts
    else:
        assert not certificate_accepts
    bound = comb(2*k, k) - 1
    assert 0 <= relative_variance <= bound
    # Relative Frobenius perturbation squared: ||delta*J||_F^2 / ||M||_F^2.
    perturbation_ratio_sq = delta * delta * n
    return {
        "case": label,
        "n": n,
        "k": k,
        "delta": str(delta),
        "all_entries_nonzero": all(value != 0 for row in f for value in row),
        "near_matching_matrix": f"F=M+{delta}*J, M_(i,i xor 1)=1 and other entries 0",
        "relative_frobenius_perturbation_squared": str(perturbation_ratio_sq),
        "certificate_residual_frobenius_squared": str(residual_frobenius_sq),
        "certificate_threshold": str(certificate_threshold),
        "certificate_residual_over_threshold": str(certificate_ratio),
        "certificate_accepts": certificate_accepts,
        "scale_denominator": problem.denominator,
        "sign_words_exhausted": m,
        "direct_disjoint_minor_sum_for_scaled_matrix": str(c_direct),
        "closed_form_minor_sum_for_scaled_matrix": str(expected_c),
        "mean_pfaffian_estimator_for_scaled_matrix": str(Q(sum_x, m)),
        "mean_matches_direct_minor_sum": True,
        "relative_variance_exact": str(relative_variance),
        "relative_variance_decimal": float(relative_variance),
        "relative_variance_over_2powk_minus1": str(relative_variance / (2**k - 1)),
        "raw_nonzero_sample_count": len(raw_positive),
        "raw_nonzero_sample_value": str(expected_positive_value),
        "phased_mean_matches_direct_minor_sum": phased_sum == m*c_direct,
        "phased_relative_variance_exact": str(phased_relative_variance),
        "phased_relative_variance_decimal": float(phased_relative_variance),
        "phased_baseline_norm_for_scaled_matrix": str(baseline),
        "all_phased_draws_within_3over4_to_4over3_baseline": True,
        "universal_bound_Ck_minus1": bound,
    }


def main():
    results = [one_instance(n, Q(1, 64*n*n), "inside_certified_near_matching")
               for n in (4, 6, 8)]
    results.extend(one_instance(n, Q(1, 16*n), "outside_certificate_but_near_matching")
                   for n in (6, 8))
    output = {
        "status": "PASS_EXACT_FINITE_VARIANCE_AUDIT",
        "origin": "c03_l07 independent diagnostic; uses copied c01_s03 low-sector sampler for X_k",
        "matrix_family": "dense rational F=M+delta J, M a direct sum of 2x2 swaps",
        "results": results,
        "scope": "Exact small-n witnesses and a finite near-matching robustness test; not an asymptotic proof for every dense family.",
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
