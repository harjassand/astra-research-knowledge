#!/usr/bin/env python3
"""Exhaustive finite-pixel check of the laminate coupon-law calculation.

This checks one discrete analogue only; it is not a proof of the continuum
homogenization formula or the general total-variation theorem.
"""

from collections import Counter
from fractions import Fraction
import json


def patch_law(period: int, stripe_width: int, coupon_width: int, vertical: bool):
    law = Counter()
    for phase in range(period):
        patch = []
        for y in range(coupon_width):
            row = []
            for x in range(coupon_width):
                coordinate = x if vertical else y
                row.append((coordinate + phase) % period < stripe_width)
            patch.append(tuple(row))
        law[tuple(patch)] += Fraction(1, period)
    return law


def total_variation(p, q):
    keys = set(p) | set(q)
    return sum(abs(p.get(key, 0) - q.get(key, 0)) for key in keys) / 2


def main():
    cases = []
    for stripe_width, coupon_width in [(6, 1), (7, 3), (11, 5), (16, 8)]:
        period = 2 * stripe_width
        vertical = patch_law(period, stripe_width, coupon_width, True)
        horizontal = patch_law(period, stripe_width, coupon_width, False)
        tv = total_variation(vertical, horizontal)
        bound = Fraction(coupon_width - 1, stripe_width)
        assert tv == bound, (stripe_width, coupon_width, tv, bound)
        cases.append({
            "stripe_width_L": stripe_width,
            "coupon_width_w": coupon_width,
            "period": period,
            "enumerated_patch_states_vertical": len(vertical),
            "enumerated_patch_states_horizontal": len(horizontal),
            "exact_discrete_TV": str(tv),
            "bound_(w-1)/L": str(bound),
        })

    K = 100
    H = Fraction(2 * K, K + 1)
    M = Fraction(K + 1, 2)
    cases_summary = {
        "contrast_K": K,
        "harmonic_mean_H": str(H),
        "arithmetic_mean_M": str(M),
        "directional_gap": str(M - H),
        "directional_ratio": str(M / H),
    }
    print(json.dumps({"scope": "finite discrete phase enumeration only", "cases": cases, "K100_laminate_arithmetic": cases_summary}, indent=2))


if __name__ == "__main__":
    main()
