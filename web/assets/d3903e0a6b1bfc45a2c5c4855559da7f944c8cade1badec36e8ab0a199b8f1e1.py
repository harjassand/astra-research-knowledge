#!/usr/bin/env python3
"""Exact equality witness for the all-size exchange bound.

The coefficient model is h(x)=prod_i (1 + lambda_i x_{2i}x_{2i+1}),
whose support consists of unions of fixed coordinate pairs. For every tested
even symmetric difference D, only the partner of a contributes, and that
term has exactly the endpoint product. This is a finite sharpness diagnostic,
not a proof of the general stable-polynomial theorem.
"""

from itertools import combinations
import json
from pathlib import Path


LAMBDAS = (2, 3, 5, 7, 11, 13, 17)
N_PAIRS = len(LAMBDAS)


def coeff(site_set):
    """Coefficient of a site subset, zero unless it is a union of pairs."""
    mask = set(site_set)
    value = 1
    for i, lam in enumerate(LAMBDAS):
        pair = {2 * i, 2 * i + 1}
        overlap = mask & pair
        if overlap and overlap != pair:
            return 0
        if overlap == pair:
            value *= lam
    return value


cases = []
for r in range(1, N_PAIRS + 1):
    # The symmetric difference consists of the first r pairs. For r<=5,
    # keep one pair as common holes and one additional pair outside both hole
    # sets (a shared occupied core in the ambient-complement convention).
    d_pairs = set(range(r))
    common_hole_pairs = {r} if r <= 5 else set()
    common_occupied_core_pairs = {r + 1} if r <= 5 else ({6} if r == 6 else set())
    s_pairs = d_pairs | common_hole_pairs
    t_pairs = common_hole_pairs
    S = {site for i in s_pairs for site in (2 * i, 2 * i + 1)}
    T = {site for i in t_pairs for site in (2 * i, 2 * i + 1)}
    D = S ^ T
    a = 0
    partner = 1
    left = coeff(S) * coeff(T)
    terms = {}
    for j in sorted(D - {a}):
        S2 = S ^ {a, j}
        T2 = T ^ {a, j}
        terms[j] = coeff(S2) * coeff(T2)
    assert len(D) == 2 * r
    assert left > 0
    assert terms[partner] == left
    assert all(value == 0 for j, value in terms.items() if j != partner)
    cases.append({
        "difference_pairs": r,
        "difference_size": len(D),
        "common_hole_pairs": len(common_hole_pairs),
        "common_occupied_core_pairs": len(common_occupied_core_pairs),
        "endpoint_product": left,
        "positive_exchange_index": partner,
        "exchange_term_product": terms[partner],
        "all_other_exchange_products_zero": True,
    })

result = {
    "status": "EXACT_ASSERTIONS_PASSED",
    "family": "product_i (1 + lambda_i x_{2i} x_{2i+1})",
    "lambda_values": list(LAMBDAS),
    "scope": "Finite exact sharpness witness only; no general proof or sampler.",
    "cases": cases,
}
print(json.dumps(result, indent=2))
