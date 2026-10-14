"""Transparent algebraic checks for the Astra physical-operation audit.

These are NOT simulations of a material, measurements, or proof of novelty.
Run with Python 3.10+: python checks.py
All experimentally motivated values retain source identifiers in the output.
"""
from __future__ import annotations
from fractions import Fraction
from math import ceil, log
import json
from pathlib import Path


def concentration(q: float, rate_ratio: float) -> float:
    """Target occupancy in the explicitly assumed two-state reset model."""
    if not 0.0 < q < 1.0 or rate_ratio <= 0.0:
        raise ValueError("Require 0 < q < 1 and a positive rate ratio.")
    return q * rate_ratio / (q * rate_ratio + 1.0 - q)


def required_ratio(q: float, target: float) -> float:
    if not 0.0 < q < 1.0 or not 0.0 < target < 1.0:
        raise ValueError("Probabilities must lie strictly between zero and one.")
    return target * (1.0 - q) / (q * (1.0 - target))


def main() -> None:
    # Burgers vectors are expressed in units of the lattice constant a.
    b1 = tuple(Fraction(i, 6) for i in (1, -2, 1))
    b2 = tuple(Fraction(i, 6) for i in (2, -1, -1))
    total = tuple(x + y for x, y in zip(b1, b2))
    assert total == (Fraction(1, 2), Fraction(-1, 2), Fraction(0))
    # With line direction [1,-1,0], each partial has cos^2(theta)=3/4.
    t = (1, -1, 0)
    for b in (b1, b2):
        dot = sum(x * y for x, y in zip(b, t))
        norm2 = sum(x * x for x in b)
        assert dot * dot / (norm2 * sum(x*x for x in t)) == Fraction(3, 4)
        assert sum(b) == 0  # Both vectors lie in the (111) plane.

    q, target = 0.01, 0.99
    needed = required_ratio(q, target)
    assert abs(needed - 9801.0) < 1e-8
    assert abs(concentration(q, needed) - target) < 1e-12

    fields = (5.8e6, 2.4e7)  # Li et al.; specimen-specific estimated onset fields.
    peak_speed = 623.5e-9    # Li et al.; maximum, NOT sustained processing speed.
    result = {
        "status": "Analytical checks only; no material simulation or new experiment",
        "repository_revision_consulted": "ace0cfc4437fe91c20ccd24d69e0ee4bb335e871",
        "burgers_counterexample": {
            "b1_over_a": list(map(str, b1)),
            "b2_over_a": list(map(str, b2)),
            "sum_over_a": list(map(str, total)),
            "meaning": "Two 30-degree partials can recombine into a nonzero perfect screw dislocation, not annihilate."
        },
        "spectral_reset_model": {
            "assumptions": "Each reset redraws target membership with probability q; target and non-target departure rates can differ; no additional diffusion or readout perturbation.",
            "q": q, "desired_occupancy": target,
            "required_outside_to_inside_departure_rate_ratio": needed,
            "illustrative_occupancy_at_ratio_100": concentration(q, 100.0),
            "warning": "100 is an illustration, NOT a measured resonance-selective contrast or material upper bound."
        },
        "uniform_field_geometry_arithmetic": {
            "source": "Li et al., Nature Materials (2023), DOI 10.1038/s41563-023-01572-7; author manuscript arXiv:2211.14933",
            "field_V_per_m": list(fields),
            "voltage_over_1_um_V": [E * 1e-6 for E in fields],
            "voltage_over_1_mm_V": [E * 1e-3 for E in fields],
            "warning": "V=E*d for a hypothetical uniform field, not an electrode design or breakdown assessment."
        },
        "constant_peak_speed_extrapolation": {
            "peak_m_per_s": peak_speed,
            "seconds_for_1_um": 1e-6 / peak_speed,
            "seconds_for_100_um": 100e-6 / peak_speed,
            "minutes_for_1_mm": 1e-3 / peak_speed / 60,
            "warning": "Illustrative extrapolation only; neither sustained speed, transport range nor removal yield is established."
        },
        "DFT_field_to_experimental_field_ratio": {
            "illustrative_DFT_field_V_per_m": 3e9,
            "ratios": [3e9 / E for E in fields],
            "warning": "A high-field barrier illustration is not a quantitative barrier calibration at experimental fields. Observed motion is not disputed."
        },
        "zero_failure_binomial_example": {
            "confidence": 0.95,
            "desired_failure_probability_upper_bound": 0.01,
            "independent_successes_needed": ceil(log(0.05) / log(0.99)),
            "warning": "Identically distributed, independent trials are assumed; repeated cycles on one evolving specimen do not automatically qualify."
        }
    }
    path = Path(__file__).with_name("checks.json")
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
