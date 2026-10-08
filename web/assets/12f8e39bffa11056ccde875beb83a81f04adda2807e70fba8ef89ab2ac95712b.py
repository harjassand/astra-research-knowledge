#!/usr/bin/env python3
"""Conditional sensitivity of sister-pair rate inference to pair purity.

This computes the algebra in proof/proximity_pair_rate_bias.md. The example is
synthetic; it is not an estimate for the macrophage preprint.
"""

from __future__ import annotations

import json
import math


def u_from_or(f_on: float, odds_ratio: float) -> float:
    c = f_on * (1.0 - f_on)
    if odds_ratio < 1.0:
        raise ValueError("odds_ratio < 1 is outside the positive-association model")
    if math.isclose(odds_ratio, 1.0):
        return c
    return (math.sqrt(1.0 + 4.0 * c * (odds_ratio - 1.0)) - 1.0) / (2.0 * (odds_ratio - 1.0))


def or_from_u(f_on: float, u: float) -> float:
    c = f_on * (1.0 - f_on)
    if not (0.0 < u <= c):
        raise ValueError("u must lie in (0, f(1-f)]")
    return ((f_on - u) * (1.0 - f_on - u)) / (u * u)


def total_switch_rate(f_on: float, odds_ratio: float, birth_rate: float) -> float:
    c = f_on * (1.0 - f_on)
    delta = odds_ratio - 1.0
    if delta <= 0.0:
        return math.inf
    return 2.0 * birth_rate / (math.sqrt(1.0 + 4.0 * c * delta) - 1.0)


def correct_for_pair_purity(f_on: float, observed_or: float, purity: float, birth_rate: float) -> dict[str, float]:
    if not (0.0 < purity <= 1.0):
        raise ValueError("purity must be in (0, 1]")
    c = f_on * (1.0 - f_on)
    u_obs = u_from_or(f_on, observed_or)
    u_true = (u_obs - (1.0 - purity) * c) / purity
    true_or = or_from_u(f_on, u_true)
    return {
        "f_on": f_on,
        "observed_or": observed_or,
        "true_sister_fraction": purity,
        "observed_mixed_orientation_probability": u_obs,
        "corrected_sister_mixed_orientation_probability": u_true,
        "corrected_true_sister_or": true_or,
        "uncorrected_total_switch_rate": total_switch_rate(f_on, observed_or, birth_rate),
        "corrected_total_switch_rate": total_switch_rate(f_on, true_or, birth_rate),
        "uncorrected_over_corrected_rate_ratio": total_switch_rate(f_on, observed_or, birth_rate) / total_switch_rate(f_on, true_or, birth_rate),
    }


if __name__ == "__main__":
    lam = math.log(2.0) / 14.4
    result = correct_for_pair_purity(f_on=0.5, observed_or=4.0, purity=0.5, birth_rate=lam)
    assert math.isclose(result["corrected_true_sister_or"], 25.0)
    assert math.isclose(result["uncorrected_over_corrected_rate_ratio"], 4.0)
    print(json.dumps({"synthetic_example_only": True, **result}, indent=2))
