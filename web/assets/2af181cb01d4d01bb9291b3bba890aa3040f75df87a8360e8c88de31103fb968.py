#!/usr/bin/env python3
"""Dimensionless exact Phi^4 wall-mode prediction and tolerance arithmetic.

This calculator evaluates the internally derived continuum-model formulas; it
does not solve an FEM model or validate a fabricated material.
"""

import json
import math


def evaluate(delta: float = 0.1) -> dict:
    if not (0 <= delta < 0.5):
        raise ValueError("the certified additive-Hessian-disorder range is 0 <= delta < 1/2")

    # H = -d^2/dy^2 + 4 - 6 sech(y)^2 has its shape mode at E=3,
    # and its essential spectrum starts at E=4.
    mode_low = 3.0 - delta
    mode_high = 3.0 + delta
    continuum_low = 4.0 - delta
    gap_low = math.sqrt(mode_low / 4.0)
    gap_high = math.sqrt(mode_high / 4.0)
    continuum_edge_low = math.sqrt(continuum_low / 4.0)
    ell_tail = math.atanh(0.99)
    length_for_two_1pct_tails_in_units_ell = 2.0 * ell_tail

    return {
        "delta_dimensionless": delta,
        "unperturbed_internal_mode_E": 3.0,
        "unperturbed_bulk_threshold_E": 4.0,
        "internal_mode_E_interval": [mode_low, mode_high],
        "other_continuum_E_lower_bound": continuum_low,
        "frequency_ratio_to_bulk_edge_interval": [gap_low, gap_high],
        "perturbed_bulk_edge_ratio_lower_bound": continuum_edge_low,
        "minimum_frequency_separation_ratio": continuum_edge_low - gap_high,
        "wall_width_for_1pct_tail_in_ell": ell_tail,
        "total_span_for_two_1pct_tails_in_ell": length_for_two_1pct_tails_in_units_ell,
        "cells_for_span_if_cell_over_ell_is_0.1": math.ceil(length_for_two_1pct_tails_in_units_ell / 0.1),
        "status": "conditional continuum-model calculation; material parameters and coupling unvalidated",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
