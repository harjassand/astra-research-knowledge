#!/usr/bin/env python3
"""Evaluate a conditional linear-invasion threshold for a finite HAC boundary.

This is a screening formula, not a fitted biological model. No source-derived
values for D, a, gamma, C_star, or local replication age are available. Supply
them explicitly; the output is conditional on a uniform vulnerable segment,
fixed low-H3K9 endpoints, and a logistic H3K9 reaction linearized near zero.

Example (dimensionless placeholders only; NOT empirical):
  python3 boundary_threshold.py --bins 8 --spread 0.02 --amplification 0.4 \
      --clearance 0.05 --c-star 1.0
"""
from __future__ import annotations

import argparse
import math


def threshold(bins: int, spread: float, amplification: float,
              clearance: float, c_star: float) -> dict[str, float | str]:
    if bins < 1:
        raise ValueError("bins must be at least 1")
    if min(spread, amplification, clearance, c_star) < 0 or c_star == 0:
        raise ValueError("rates and C_star must be nonnegative, with C_star > 0")
    laplacian_penalty = 4.0 * spread * math.sin(math.pi / (2.0 * (bins + 1))) ** 2
    critical_deficit = (clearance + laplacian_penalty) / amplification if amplification else math.inf
    if critical_deficit > 1:
        critical_c = 0.0
        regime = "no_invasion_even_at_maximal_deficit_in_this_linear_screen"
    elif critical_deficit < 0:
        critical_c = c_star
        regime = "invasion_for_all_deficits_in_this_linear_screen"
    else:
        critical_c = c_star * (1.0 - critical_deficit)
        regime = "invasion_when_CENP_A_below_critical_level"
    dominant_growth = amplification - clearance - laplacian_penalty
    return {
        "bins": bins,
        "effective_spatial_spread_D": spread,
        "deficit_amplification_a": amplification,
        "clearance_gamma": clearance,
        "C_star": c_star,
        "diffusion_eigenvalue_penalty": laplacian_penalty,
        "critical_CENP_A_deficit_q": critical_deficit,
        "critical_CENP_A_level": critical_c,
        "max_deficit_dominant_growth_rate_per_hour": dominant_growth,
        "maximum_deficit_invades": dominant_growth > 0,
        "regime": regime,
        "status": "conditional_model_output_not_measurement_or_validated_prediction",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bins", type=int, required=True)
    parser.add_argument("--spread", type=float, required=True,
                        help="effective spatial coupling D, per hour")
    parser.add_argument("--amplification", type=float, required=True,
                        help="max deficit-linked H3K9 growth a, per hour")
    parser.add_argument("--clearance", type=float, required=True,
                        help="H3K9 clearance gamma, per hour")
    parser.add_argument("--c-star", type=float, required=True,
                        help="CENP-A reference level C_star")
    args = parser.parse_args()
    import json
    print(json.dumps(threshold(args.bins, args.spread, args.amplification,
                               args.clearance, args.c_star), indent=2))


if __name__ == "__main__":
    main()
