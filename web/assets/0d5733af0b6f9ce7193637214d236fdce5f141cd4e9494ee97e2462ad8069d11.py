#!/usr/bin/env python3
"""Exact low-rank checks for the root-data formulas in RESULT.txt.

This script checks, for A1, A2, B2, C2 and G2:
  (a) positive coroot counts and exact Weyl dimension-ratio moment bounds;
  (b) the local fundamental-flag Hessian minimum.

It is a reproducible finite arithmetic check, not a proof for all root
systems or a numerical evaluation of the global constant gamma_G.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


# Cartan convention A_ij = <alpha_j, alpha_i^vee>.
CARTAN = {
    "A1": [[2]],
    "A2": [[2, -1], [-1, 2]],
    "B2": [[2, -1], [-2, 2]],
    "C2": [[2, -2], [-1, 2]],
    "G2": [[2, -3], [-1, 2]],
}

# Simple-root squared lengths and positive-root coefficients, with long
# roots normalized to squared length 2.
GEOMETRY = {
    "A1": ([Fraction(2)], [(1,)]),
    "A2": ([Fraction(2), Fraction(2)], [(1, 0), (0, 1), (1, 1)]),
    "B2": ([Fraction(2), Fraction(1)],
           [(1, 0), (0, 1), (1, 1), (1, 2)]),
    "C2": ([Fraction(1), Fraction(2)],
           [(1, 0), (0, 1), (1, 1), (2, 1)]),
    "G2": ([Fraction(2, 3), Fraction(2)],
           [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)]),
}


def positive_coroots(cartan):
    rank = len(cartan)
    roots = {tuple(int(i == j) for i in range(rank)) for j in range(rank)}
    frontier = list(roots)
    while frontier:
        c = frontier.pop()
        for i in range(rank):
            # Reflection s_i(c) = c - <alpha_i, c> alpha_i^vee.
            pairing = sum(c[j] * cartan[j][i] for j in range(rank))
            reflected = list(c)
            reflected[i] -= pairing
            reflected = tuple(reflected)
            if reflected not in roots:
                roots.add(reflected)
                frontier.append(reflected)
    return sorted(c for c in roots if all(x >= 0 for x in c))


def ratio_deficit(coroots, dynkin_labels):
    """Return exact sum_i (1 - d_Lambda/d_(Lambda+omega_i))."""
    rank = len(dynkin_labels)
    total = Fraction(0)
    for i in range(rank):
        ratio = Fraction(1)
        for coroot in coroots:
            x = sum(coroot[j] * (dynkin_labels[j] + 1)
                    for j in range(rank))
            ratio *= Fraction(x, x + coroot[i])
        total += 1 - ratio
    return total


def main():
    records = {}
    for name, cartan in CARTAN.items():
        coroots = positive_coroots(cartan)
        p = len(coroots)
        assert p == len(GEOMETRY[name][1])
        rank = len(cartan)
        checked = 0
        max_ratio_to_bound = Fraction(0)
        worst = None
        for labels in product(range(1, 9), repeat=rank):
            N = sum(labels)
            min_label = min(labels)
            deficit = ratio_deficit(coroots, labels)
            bound = Fraction(p, min_label + 1)  # eta N = min_i n_i
            assert deficit <= bound
            checked += 1
            ratio = deficit / bound
            if ratio > max_ratio_to_bound:
                max_ratio_to_bound, worst = ratio, labels

        lengths, roots = GEOMETRY[name]
        coefficients = [
            sum(q * length for q, length in zip(root, lengths)) / 4
            for root in roots
        ]
        local_min = min(coefficients)
        predicted = min(lengths) / 4
        assert local_min == predicted

        records[name] = {
            "rank": rank,
            "positive_coroot_count": p,
            "positive_coroot_coefficients": [list(c) for c in coroots],
            "regular_labels_checked": checked,
            "moment_bound": "sum_i(1-d_Lambda/d_(Lambda+omega_i)) <= p/(min_i n_i+1)",
            "largest_checked_deficit_over_bound": str(max_ratio_to_bound),
            "labels_at_largest_checked_ratio": list(worst),
            "local_hessian_minimum": str(local_min),
            "predicted_min_simple_root_length_over_4": str(predicted),
        }

    output = {
        "status": "FINITE-EVIDENCE",
        "scope": "Exact rational checks for five low-rank root systems; not a general proof and not a gamma_G far-set computation.",
        "results": records,
    }
    out_path = Path(__file__).with_name("root_kernel_moment_check.json")
    out_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
