#!/usr/bin/env python3
"""Reproduce the illustrative finite-sample Hoeffding design counts."""

from __future__ import annotations

import json
import math


def strict_n_for_radius(coefficient: float, radius: float) -> int:
    """Smallest integer n for sqrt(coefficient / n) < radius."""
    if coefficient <= 0 or radius <= 0:
        raise ValueError("coefficient and radius must be positive")
    return math.floor(coefficient / (radius * radius)) + 1


def main() -> None:
    # Three contexts, one common pre-treatment stratum, one endpoint,
    # two separate guide versions, and alpha/2 assigned to each interval family.
    contexts, strata, outcomes, guides = 3, 1, 1, 2
    familywise_alpha = 0.05
    alpha_means = alpha_arm_differences = familywise_alpha / 2
    arm_comparisons = (contexts - 1) * strata * outcomes * (guides + 1)
    means = contexts * strata * outcomes * guides

    r_coefficient = 2 * math.log(2 * means / alpha_means)
    t_coefficient = 2 * math.log(2 * arm_comparisons / alpha_arm_differences)

    source_and_target_effect = 0.60
    reversal_margin = 0.30
    equivalence_margin = 0.30
    reversal_radius = (source_and_target_effect - reversal_margin) / 2
    equivalence_radius = equivalence_margin / 2

    n_reversal = strict_n_for_radius(r_coefficient, reversal_radius)
    n_equivalence = strict_n_for_radius(t_coefficient, equivalence_radius)

    # Two independent target guides plus a shared matched NTC arm per context.
    arms_per_block = guides + 1
    result = {
        "assumptions": {
            "contexts": contexts,
            "state_strata": strata,
            "outcomes": outcomes,
            "guides": guides,
            "familywise_alpha": familywise_alpha,
            "alpha_means": alpha_means,
            "alpha_arm_differences": alpha_arm_differences,
            "true_reversal_effect_magnitude": source_and_target_effect,
            "reversal_margin": reversal_margin,
            "equivalence_margin": equivalence_margin,
        },
        "r_coefficient": r_coefficient,
        "t_coefficient": t_coefficient,
        "reversal": {
            "sufficient_radius_condition": f"r < {reversal_radius}",
            "n_per_context": n_reversal,
            "randomized_arm_units": arms_per_block * contexts * n_reversal,
        },
        "zero_difference_equivalence": {
            "sufficient_radius_condition": f"t < {equivalence_radius}",
            "n_per_context": n_equivalence,
            "randomized_arm_units": arms_per_block * contexts * n_equivalence,
        },
        "warning": "Counts are conservative distribution-free coverage-based sufficiency values, not a general power calculation; add controls, engagement assays, state assays, pilots, and failures.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
