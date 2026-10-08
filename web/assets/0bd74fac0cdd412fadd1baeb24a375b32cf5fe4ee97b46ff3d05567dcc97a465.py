#!/usr/bin/env python3
"""Finite arithmetic check for the conditional two-class selection bound."""

from __future__ import annotations

import json


def fixed_class_yields(p: float, q: float, total_yield: float) -> tuple[float, float]:
    return q * total_yield / p, (1.0 - q) * total_yield / (1.0 - p)


def switch_fraction(p: float, q: float) -> float:
    if p > q:
        raise ValueError("This one-way N-to-R construction requires p <= q")
    if p == 1.0:
        raise ValueError("No N class exists when p=1")
    return (q - p) / (1.0 - p)


def audit_case(p: float, q: float, total_yield: float) -> dict[str, float]:
    g_r, g_n = fixed_class_yields(p, q, total_yield)
    alpha = switch_fraction(p, q)

    # Fixed classes reproduce the endpoint fraction and total yield.
    end_r_selection = p * g_r
    end_n_selection = (1.0 - p) * g_n
    assert abs(end_r_selection + end_n_selection - total_yield) < 1e-12
    assert abs(end_r_selection / total_yield - q) < 1e-12

    # Common-yield switching reproduces the same endpoint fraction and total.
    end_r_switch = total_yield * (p + (1.0 - p) * alpha)
    assert abs(end_r_switch / total_yield - q) < 1e-12
    assert abs(p + alpha * (1.0 - p) - q) < 1e-12

    return {
        "p": p,
        "q": q,
        "total_yield": total_yield,
        "g_responder_fixed": g_r,
        "g_nonresponder_fixed": g_n,
        "switch_fraction_N_to_R_common_growth": alpha,
    }


def main() -> None:
    q = 0.985
    doublings = 2.3
    total_yield = 2.0**doublings
    threshold_p = 1.0 - total_yield * (1.0 - q)

    result = {
        "source_reported_mean_inputs": {
            "endpoint_positive_fraction_q": q,
            "cumulative_population_doublings_D": doublings,
            "total_yield_G_equals_2_to_D": total_yield,
        },
        "minimum_rest_start_p_without_N_subreplacement": threshold_p,
        "illustrative_unlicensed_p_0_702": audit_case(0.702, q, total_yield),
        "within_barcode_exact_alias": audit_case(0.5, 0.9, 2.0),
        "scope": "arithmetic check of conditional models, not biological evidence",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
