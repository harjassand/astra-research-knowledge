#!/usr/bin/env python3
"""Exact small checks for the linear-identification examples in REPORT.md.

Uses fractions only. This checks algebra/examples, not chemistry or external
correctness of the literature claims.
"""

from fractions import Fraction as F
import json
from pathlib import Path


def rank_2(rows):
    """Rank of a matrix with two columns over the rationals."""
    nonzero = [row for row in rows if row[0] or row[1]]
    if not nonzero:
        return 0
    first = nonzero[0]
    return 1 if all(first[0] * row[1] == first[1] * row[0] for row in nonzero) else 2


def two_state_mark(e_a, e_b, d, s):
    kappa = d * (1 - s) + (1 - d) * s
    h_a = e_a * kappa
    h_b = e_b * (1 - kappa)
    return h_a, h_b, h_a - h_b


def feasible_theta_interval(h_lo, h_hi, a_lo, a_hi, i_lo, i_hi, k):
    """Exact interval for the independent box-calibration model in REPORT.md."""
    def feasible(t):
        lower = a_lo * t + i_lo * (1 - t) - k
        upper = a_hi * t + i_hi * (1 - t) + k
        return lower <= h_hi and upper >= h_lo

    grid = [F(i, 10000) for i in range(10001)]
    accepted = [t for t in grid if feasible(t)]
    assert accepted
    return accepted[0], accepted[-1]


def main():
    # Isotope-only observation row is constant on the two models; the targeted
    # intervention creates a rank-2 design when calibrated as external-only.
    isotope_rows = [[F(1), F(1)]]
    selective_rows = [[F(1), F(1)], [F(1), F(0)]]
    assert rank_2(isotope_rows) == 1
    assert rank_2(selective_rows) == 2

    # Two exact same-baseline models in the report.
    model_a = (F(1), F(1, 2))
    model_b = (F(3, 2), F(0))
    base_a = sum(model_a)
    base_b = sum(model_b)
    treated_a = model_a[0]  # internal remains; external fully suppressed
    treated_b = model_b[0]
    assert base_a == base_b == F(3, 2)
    assert treated_a == 1 and treated_b == F(3, 2)
    # Unknown collateral in B can exactly mimic A's treated observation.
    assert treated_b + F(-1, 2) == treated_a

    h_a, h_b, delta = two_state_mark(F(4, 5), F(4, 5), F(19, 20), F(1, 10))
    assert delta == F(72, 125)  # e*(2d-1)*(1-2s)
    scrambled_a, scrambled_b, scrambled_delta = two_state_mark(
        F(4, 5), F(4, 5), F(19, 20), F(1, 2)
    )
    assert scrambled_delta == 0 and scrambled_a == scrambled_b
    observed = F(1, 2)
    mark_x = (observed - h_b) / delta
    assert mark_x == F(97, 144)

    # The sharp box interval from the report's illustrative—not empirical—
    # calibration/noise values. Grid resolution verifies the stated endpoints.
    grid_lo, grid_hi = feasible_theta_interval(
        F(35, 100), F(65, 100), F(90, 100), F(1), F(0), F(5, 100), F(5, 100)
    )
    analytic_lo = F(25, 95)
    analytic_hi = F(70, 90)
    assert abs(grid_lo - analytic_lo) <= F(1, 10000)
    assert abs(grid_hi - analytic_hi) <= F(1, 10000)

    result = {
        "scope": "exact rational/algebraic checks only; not chemistry validation",
        "isotope_only_design_rank": 1,
        "calibrated_selective_design_rank": 2,
        "same_baseline_rate": str(base_a),
        "model_A_treated_rate": str(treated_a),
        "model_B_treated_rate": str(treated_b),
        "model_B_collateral_to_match_A": "-1/2",
        "mark_example": {
            "e_A": "4/5", "e_B": "4/5", "detector_correct": "19/20",
            "scrambling_swap": "1/10", "effective_A_response": str(h_a),
            "effective_B_response": str(h_b), "contrast": str(delta),
            "x_A_when_observed_A_rate_is_1/2": str(mark_x),
            "contrast_at_half_scrambling": str(scrambled_delta),
        },
        "illustrative_partial_identification": {
            "h_interval": ["35/100", "65/100"],
            "selectivity_bounds": {"a_E": ["90/100", "1"], "a_I": ["0", "5/100"]},
            "collateral_bound": "5/100",
            "theta_E_interval_exact": [str(analytic_lo), str(analytic_hi)],
            "grid_check_resolution": "1/10000",
        },
    }
    out = Path(__file__).with_name("CHECK_RESULTS.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
