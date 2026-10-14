#!/usr/bin/env python3
"""Exact rational checks for the simple binary-control identifiability review."""

from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json
from pathlib import Path


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def bernoulli_sum_pmf(probabilities):
    pmf = [F(1)]
    for p in probabilities:
        pmf = poly_mul(pmf, [1 - p, p])
    return pmf


def conditional_count_pmf(n, j, p_low, p_high):
    return bernoulli_sum_pmf([p_low] * (n - j) + [p_high] * j)


def mixture_count_pmf(n, law_j, p_low, p_high):
    out = [F(0)] * (n + 1)
    for j, weight in enumerate(law_j):
        if weight:
            pmf = conditional_count_pmf(n, j, p_low, p_high)
            out = [x + weight * y for x, y in zip(out, pmf)]
    return out


def mixture_matrix(n, p_low, p_high):
    return [[conditional_count_pmf(n, j, p_low, p_high)[k]
             for j in range(n + 1)] for k in range(n + 1)]


def determinant(matrix):
    a = [row[:] for row in matrix]
    det = F(1)
    for col in range(len(a)):
        pivot = next((r for r in range(col, len(a)) if a[r][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        p = a[col][col]
        det *= p
        for r in range(col + 1, len(a)):
            factor = a[r][col] / p
            for c in range(col + 1, len(a)):
                a[r][c] -= factor * a[col][c]
    return det


def support_law_to_voids(q, support_law):
    # support_law maps an occupied-cell bit mask to an exact probability.
    voids = {}
    for mask in range(1 << q):
        voids[mask] = sum((w for support, w in support_law.items()
                           if support & mask == 0), F(0))
    return voids


def invert_voids(q, voids):
    # voids[mask] = P(no occupied cell in mask).
    # P(O=T) = sum_{U subset T} (-1)^(|T|-|U|) P(O subset T?)
    # Here F(U)=P(O subset U)=void(complement(U)).
    law = {}
    full = (1 << q) - 1
    for target in range(1 << q):
        total = F(0)
        sub = target
        while True:
            f = voids[full ^ sub]
            sign = -1 if (target.bit_count() - sub.bit_count()) % 2 else 1
            total += sign * f
            if sub == 0:
                break
            sub = (sub - 1) & target
        law[target] = total
    return law


def finite_partition_mobius_check():
    q = 5
    support_law = {
        0b00011: F(1, 7),
        0b10101: F(2, 7),
        0b11000: F(1, 7),
        0b11101: F(3, 7),
    }
    assert sum(support_law.values()) == 1
    voids = support_law_to_voids(q, support_law)
    recovered = invert_voids(q, voids)
    assert {m: p for m, p in recovered.items() if p} == support_law
    return {
        "q": q,
        "nonzero_support_patterns": len(support_law),
        "void_queries": len(voids),
        "exact_mobius_recovery": True,
        "support_law": {str(m): str(p) for m, p in support_law.items()},
    }


def finite_bin_simple_countermodel():
    n = 6
    p_low, p_high = F(1, 100), F(99, 100)
    even = [(0, 1, 5), (1, 5, 0), (5, 0, 1)]
    odd = [(0, 5, 1), (1, 0, 5), (5, 1, 0)]
    masks_checked = []
    for mask in range(1 << 3):
        law_even = [F(0)] * (n + 1)
        law_odd = [F(0)] * (n + 1)
        for occ in even:
            j = sum(occ[i] for i in range(3) if mask & (1 << i))
            law_even[j] += F(1, 3)
        for occ in odd:
            j = sum(occ[i] for i in range(3) if mask & (1 << i))
            law_odd[j] += F(1, 3)
        assert law_even == law_odd, (mask, law_even, law_odd)
        assert mixture_count_pmf(n, law_even, p_low, p_high) == \
            mixture_count_pmf(n, law_odd, p_low, p_high)
        masks_checked.append(mask)
    return {
        "n": n,
        "coarse_cells": 3,
        "p_low": str(p_low),
        "p_high": str(p_high),
        "binary_masks_checked": masks_checked,
        "even_occupancies": even,
        "odd_occupancies": odd,
        "all_subset_sum_laws_equal": True,
        "all_full_count_histograms_equal": True,
        "simple_point_realization": {
            "rule": "Within each disjoint cell choose k distinct interior ages for occupancy k; never reuse an age.",
            "maximum_occupancy_per_cell": 5,
            "all_histories_are_simple": True,
        },
    }


def parity_channel_check():
    n = 6
    p_low, p_high = F(1, 100), F(99, 100)
    delta = p_high - p_low
    plus = [F(comb(n, j), 2 ** (n - 1)) if j % 2 == 0 else F(0)
            for j in range(n + 1)]
    minus = [F(comb(n, j), 2 ** (n - 1)) if j % 2 else F(0)
             for j in range(n + 1)]
    q_plus = mixture_count_pmf(n, plus, p_low, p_high)
    q_minus = mixture_count_pmf(n, minus, p_low, p_high)
    diff = [a - b for a, b in zip(q_plus, q_minus)]
    expected = [F((-1) ** (n - k) * comb(n, k), 2 ** (n - 1)) * delta ** n
                for k in range(n + 1)]
    assert diff == expected
    assert sum(abs(x) for x in diff) == 2 * delta ** n
    assert sum(abs(a - b) for a, b in zip(plus, minus)) == 2
    assert plus[0] - minus[0] == F(1, 2 ** (n - 1))
    mat = mixture_matrix(n, p_low, p_high)
    det = determinant(mat)
    assert det == delta ** (n * (n + 1) // 2)
    return {
        "n": n,
        "p_low": str(p_low),
        "p_high": str(p_high),
        "delta": str(delta),
        "pi_plus": [str(x) for x in plus],
        "pi_minus": [str(x) for x in minus],
        "void_probability_gap": str(plus[0] - minus[0]),
        "output_histogram_l1_gap": str(sum(abs(x) for x in diff)),
        "output_histogram_total_variation": str(delta ** n),
        "channel_determinant": str(det),
        "determinant_formula_verified": True,
        "inverse_l1_norm_lower_bound": str(delta ** (-n)),
    }


def kl_conditioning_check():
    n = 6
    p_low, p_high = F(1, 4), F(7, 20)  # 0.25 and 0.35
    eta = min(p_low, p_high, 1 - p_low, 1 - p_high)
    delta = p_high - p_low
    chi2_upper = (delta ** (2 * n) * comb(2 * n, n) /
                  (2 ** (2 * n - 2) * eta ** n))
    alpha = F(1, 20)
    n_lower = 2 * (1 - 2 * alpha) ** 2 / chi2_upper
    return {
        "n": n,
        "p_low": str(p_low),
        "p_high": str(p_high),
        "eta": str(eta),
        "delta": str(delta),
        "chi_square_and_kl_upper_bound": str(chi2_upper),
        "chi_square_and_kl_upper_bound_decimal": float(chi2_upper),
        "alpha": str(alpha),
        "necessary_iid_products_for_max_error_at_most_alpha_lower_bound": str(n_lower),
        "lower_bound_decimal": float(n_lower),
        "scope": "One binary-set count-histogram assay for the explicit parity-mixture pair; not a global adaptive-tomography bound.",
    }


def near_pair_check():
    n = 4
    eta = F(1, 4)
    slope = F(1)
    separation = F(1, 1000)
    alpha = F(1, 20)
    one_sample_kl = n * (slope * separation) ** 2 / (eta * (1 - eta))
    products_lower = 2 * (1 - 2 * alpha) ** 2 / one_sample_kl
    return {
        "n": n,
        "eta": str(eta),
        "Lipschitz_slope_bound": str(slope),
        "matched_age_displacement": str(separation),
        "one_product_KL_upper_bound": str(one_sample_kl),
        "alpha": str(alpha),
        "necessary_products_lower_bound": str(products_lower),
        "scope": "Two deterministic simple histories with atomwise matched age displacement at most epsilon, for any calibrated M-Lipschitz per-atom probability control; raw labels are more informative than the product count.",
    }


def finite_control_affine_witness():
    # Two arbitrary-shaped (here polynomial) per-age response profiles on four
    # candidate ages. The signed relation [1,-3,3,-1] annihilates 1,t,t^2.
    t_values = [F(0), F(1, 3), F(2, 3), F(1)]
    p_profiles = [
        [F(1, 4) + t / 2 for t in t_values],
        [F(1, 4) + t * t / 2 for t in t_values],
    ]
    mu_plus = [F(1, 4), F(0), F(3, 4), F(0)]
    mu_minus = [F(0), F(3, 4), F(0), F(1, 4)]
    assert sum(mu_plus) == sum(mu_minus) == 1
    means = []
    for profile in p_profiles:
        plus_mean = sum((w * p for w, p in zip(mu_plus, profile)), F(0))
        minus_mean = sum((w * p for w, p in zip(mu_minus, profile)), F(0))
        assert plus_mean == minus_mean
        means.append(str(plus_mean))

    # Embed the random candidate atom in n=3 simple histories by adding two
    # common ages. Their response probabilities are arbitrary calibrated values.
    n = 3
    common_probabilities = [F(2, 5), F(3, 5)]
    for profile in p_profiles:
        plus_variable = sum((w * p for w, p in zip(mu_plus, profile)), F(0))
        minus_variable = sum((w * p for w, p in zip(mu_minus, profile)), F(0))
        plus_hist = bernoulli_sum_pmf(common_probabilities + [plus_variable])
        minus_hist = bernoulli_sum_pmf(common_probabilities + [minus_variable])
        assert plus_hist == minus_hist
    return {
        "n": n,
        "finite_controls": 2,
        "candidate_age_parameters": [str(t) for t in t_values],
        "profile_1_probabilities": [str(p) for p in p_profiles[0]],
        "profile_2_probabilities": [str(p) for p in p_profiles[1]],
        "law_plus_weights": [str(w) for w in mu_plus],
        "law_minus_weights": [str(w) for w in mu_minus],
        "equal_variable_atom_means": means,
        "common_atom_probabilities": [str(x) for x in common_probabilities],
        "both_laws_are_simple": True,
        "all_full_count_histograms_equal": True,
        "scope": "Exact witness for this finite profile pair; the general affine-dependence proof covers any finite list of per-age probability profiles.",
    }


def main():
    results = {
        "finite_partition_mobius": finite_partition_mobius_check(),
        "simple_finite_bin_countermodel": finite_bin_simple_countermodel(),
        "parity_channel": parity_channel_check(),
        "purity_conditioning": kl_conditioning_check(),
        "near_pair_resolution": near_pair_check(),
        "finite_control_affine_witness": finite_control_affine_witness(),
    }
    out_path = Path(__file__).with_name("results.json")
    out_path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
