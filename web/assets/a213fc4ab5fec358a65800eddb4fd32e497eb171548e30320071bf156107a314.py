#!/usr/bin/env python3
"""Historical ideal isotope-bookkeeping fixture for acetate carbon maps.

Inputs are measured 13C fractions of the reacting precursor pools, not bulk
feed fractions unless the experiment independently verifies that equivalence.
Tuple keys are (methyl-13C, carboxyl-13C).

The executable example at the bottom uses invented 0.20/0.80 fractions. It is
only an arithmetic fixture, not a Cu-Fe measurement or prediction. See
transient_identifiability.py for the source-independent exact overlap result.
"""

from __future__ import annotations

from collections.abc import Mapping

Label = tuple[int, int]


def direct_co_ch2(x_co_carbonyl: float, x_ch2_methyl: float) -> dict[Label, float]:
    """CO supplies the acetate carboxyl C; CH2 supplies the methyl C."""
    x_c = _fraction(x_co_carbonyl, "x_co_carbonyl")
    x_m = _fraction(x_ch2_methyl, "x_ch2_methyl")
    return {
        (1, 1): x_m * x_c,
        (1, 0): x_m * (1.0 - x_c),
        (0, 1): (1.0 - x_m) * x_c,
        (0, 0): (1.0 - x_m) * (1.0 - x_c),
    }


def co_dimer_then_hydrogenate(
    x_site_a: float, x_site_b: float, alpha_a_to_methyl: float
) -> dict[Label, float]:
    """Two site-specific CO pools couple; alpha assigns site A to methyl."""
    x_a = _fraction(x_site_a, "x_site_a")
    x_b = _fraction(x_site_b, "x_site_b")
    alpha = _fraction(alpha_a_to_methyl, "alpha_a_to_methyl")
    return {
        (1, 1): x_a * x_b,
        (0, 0): (1.0 - x_a) * (1.0 - x_b),
        (1, 0): alpha * x_a * (1.0 - x_b) + (1.0 - alpha) * x_b * (1.0 - x_a),
        (0, 1): alpha * (1.0 - x_a) * x_b + (1.0 - alpha) * (1.0 - x_b) * x_a,
    }


def mass_only(probabilities: Mapping[Label, float]) -> dict[int, float]:
    """Collapse positional isotopomers to the count of 13C atoms."""
    result = {0: 0.0, 1: 0.0, 2: 0.0}
    for (methyl, carboxyl), probability in probabilities.items():
        result[methyl + carboxyl] += probability
    return result


def total_variation(a: Mapping[Label, float], b: Mapping[Label, float]) -> float:
    """Position-resolved TV distance between predicted isotopomer laws."""
    return 0.5 * sum(abs(a.get(z, 0.0) - b.get(z, 0.0)) for z in set(a) | set(b))


def _fraction(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")
    return float(value)


if __name__ == "__main__":
    # Synthetic illustration only: these are not published or measured pool
    # enrichments and cannot serve as a Cu-Fe pathway prediction.
    print("SYNTHETIC ARITHMETIC FIXTURE ONLY; not Cu-Fe data or prediction")
    direct = direct_co_ch2(x_co_carbonyl=0.20, x_ch2_methyl=0.80)
    dimer = co_dimer_then_hydrogenate(x_site_a=0.20, x_site_b=0.80, alpha_a_to_methyl=1.0)
    print("direct CO* + CH2*:", direct)
    print("CO* dimer then asymmetric hydrogenation:", dimer)
    print("mass-only direct:", mass_only(direct))
    print("mass-only dimer:", mass_only(dimer))
    print("position-resolved TV:", total_variation(direct, dimer))
