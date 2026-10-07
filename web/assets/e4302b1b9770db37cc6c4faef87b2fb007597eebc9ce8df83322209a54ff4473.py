#!/usr/bin/env python3
"""Exact scalar checks for the sharp dimension-uniform cloner lift."""

from fractions import Fraction as Q
import json
from pathlib import Path


def kappa(d: int) -> Q:
    return Q(4 * ((d * d) // 4), d * d)


def cloner_parameter(d: int) -> Q:
    return Q(d + 2, 2 * (d + 1))


def eb_distance(d: int, m: int) -> Q:
    p_m = cloner_parameter(d) ** m
    threshold = Q(1, d + 1)
    return kappa(d) * max(Q(0), p_m - threshold)


def main() -> None:
    finite_grid = []
    for d in range(2, 65):
        for m in range(1, 13):
            dist = eb_distance(d, m)
            bound = Q(1, 2**m)
            assert dist <= bound
            finite_grid.append({
                "d": d,
                "m": m,
                "distance": str(dist),
                "2^-m_bound": str(bound),
                "verified": True,
            })

    growing_sequence = []
    for m in range(1, 17):
        d = 2 ** (m + 1)
        p_m = cloner_parameter(d) ** m
        threshold = Q(1, d + 1)
        dist = eb_distance(d, m)
        bound = Q(1, 2**m)
        assert p_m > threshold
        assert kappa(d) == 1
        assert dist <= bound
        growing_sequence.append({
            "m": m,
            "d_even": d,
            "p_d^m": str(p_m),
            "EB_threshold": str(threshold),
            "non_EB": True,
            "exact_EB_distance": str(dist),
            "2^-m": str(bound),
            "gap_to_uniform_supremum": str(bound - dist),
        })

    result = {
        "arithmetic": "fractions.Fraction; exact rational scalar calculations",
        "finite_grid_rows": len(finite_grid),
        "finite_grid_dimensions": "2..64",
        "finite_grid_depths": "1..12",
        "all_grid_values_below_2^-m": True,
        "growing_even_non_EB_sequence": growing_sequence,
        "proof_status": "finite rows are diagnostics; all-d supremum proof is in CP_RANGE_SHARPENING.txt",
        "solver_used": False,
        "floating_point_used": False,
    }
    Path(__file__).with_name("power_range_checks.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps({
        "finite_grid_rows": len(finite_grid),
        "growing_sequence_rows": len(growing_sequence),
        "all_exact_checks_passed": True,
        "last_sequence_gap": growing_sequence[-1]["gap_to_uniform_supremum"],
    }, indent=2))


if __name__ == "__main__":
    main()
