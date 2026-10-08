#!/usr/bin/env python3
"""Finite algebra/numerical checks for the exact controlled-CTMC witness."""

from fractions import Fraction
import json
import math
from pathlib import Path


INCREMENTS = (-2, -1, 1, 2)
BASE = (1, 1, 1, 1)
NULL_DIRECTION = (1, -3, -1, 0)

assert sum(c * d for c, d in zip(NULL_DIRECTION, INCREMENTS)) == 0
assert sum(c * d * d for c, d in zip(NULL_DIRECTION, INCREMENTS)) == 0
assert sum(c * d**3 for c, d in zip(NULL_DIRECTION, INCREMENTS)) == -6
assert sum(r * d for r, d in zip(BASE, INCREMENTS)) == 0
assert sum(r * d * d for r, d in zip(BASE, INCREMENTS)) == 10


def endpoint_prob(theta: float, tau: float) -> float:
    rate = 4.0 - 3.0 * theta
    return (1.0 + theta) / rate * (1.0 - math.exp(-rate * tau))


def rate_vector(theta: Fraction, action: int) -> tuple[Fraction, ...]:
    return (
        1 + action * theta,
        1 - 3 * action * theta,
        1 - action * theta,
        Fraction(1),
    )


for theta in (Fraction(1, 10), Fraction(-1, 10)):
    for action in (0, 1):
        rates = rate_vector(theta, action)
        assert min(rates) > 0
        assert sum(r * d for r, d in zip(rates, INCREMENTS)) == 0
        assert sum(r * d * d for r, d in zip(rates, INCREMENTS)) == 10
        assert sum(r * d**3 for r, d in zip(rates, INCREMENTS)) == -6 * action * theta

kappa, tau = 0.1, 1.0
p_control = endpoint_prob(0.0, tau)
p_plus = endpoint_prob(kappa, tau)
p_minus = endpoint_prob(-kappa, tau)
assert p_plus > p_control > p_minus

result = {
    "increment_order": list(INCREMENTS),
    "baseline_rates": list(BASE),
    "null_direction": list(NULL_DIRECTION),
    "first_moment_of_null_direction": 0,
    "second_moment_of_null_direction": 0,
    "third_moment_of_null_direction": -6,
    "example": {
        "kappa": kappa,
        "tau": tau,
        "p_control": p_control,
        "p_source_and_invariant_target": p_plus,
        "effect_in_invariant_target": p_plus - p_control,
        "p_reversed_target": p_minus,
        "effect_in_reversed_target": p_minus - p_control,
    },
    "checks": "exact rational moment and positivity identities passed; finite-horizon sign order passed",
}
Path(__file__).with_name("witness_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
