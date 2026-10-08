#!/usr/bin/env python3
"""Finite arithmetic checks for the cycle-3 actionwise-CLE CTMC witness.

This uses only the standard library. It checks the pointwise observable CLE
fields for two theta values and evaluates the closed-form first-exit survival
probabilities at the nuisance-rate interval endpoints. It is not a proof and
does not validate a biological model.
"""

from __future__ import annotations

import json
import math


def cle_fields(x: int, h: int, action: str, theta: float, c: float, kappa: float):
    """Return b,A for observable x by summing all CTMC jump increments."""
    jumps: list[tuple[int, float]] = []
    if x == 2:
        if h == 0:
            jumps.extend([(-1, c), (1, c)])
        else:
            jumps.extend([(-2, c / 4.0), (2, c / 4.0)])
    elif action == "reset":
        jumps.append((2 - x, kappa))

    # Hidden switches are included as zero observed increments.
    if action == "active":
        jumps.append((0, theta))

    drift = sum(nu * rate for nu, rate in jumps)
    covariance = sum(nu * nu * rate for nu, rate in jumps)
    return drift, covariance


def survival(theta: float, c: float, t: float, h: int) -> float:
    """S_h = e_h^T exp((G_theta - diag(2c,c/2))t) 1, by 2x2 formula."""
    d = 0.75 * c
    m = -theta - 1.25 * c
    k = math.sqrt(theta * theta + d * d)
    phase_term = theta - d if h == 0 else theta + d
    return math.exp(m * t) * (
        math.cosh(k * t) + phase_term * math.sinh(k * t) / k
    )


def bernoulli_kl(p: float, q: float) -> float:
    return p * math.log(p / q) + (1.0 - p) * math.log((1.0 - p) / (1.0 - q))


def main() -> None:
    theta_values = (0.1, 3.0)
    actions = ("passive", "active", "reset")
    field_max_difference = 0.0
    field_checks = 0
    for x in range(5):
        for h in (0, 1):
            for action in actions:
                fields = [cle_fields(x, h, action, theta, 1.0, 0.7) for theta in theta_values]
                field_max_difference = max(
                    field_max_difference,
                    abs(fields[0][0] - fields[1][0]),
                    abs(fields[0][1] - fields[1][1]),
                )
                field_checks += 1
    assert field_max_difference == 0.0

    rate_box = (0.9, 1.1)
    classes = (0.1, 3.0)
    intervals: dict[str, dict[str, list[float]]] = {"h0": {}, "h1": {}}
    for h in (0, 1):
        for theta in classes:
            vals = [survival(theta, c, 1.0, h) for c in rate_box]
            # S_h is decreasing in c, so these two endpoint values give the
            # exact interval over the continuous nuisance-rate interval.
            intervals[f"h{h}"][str(theta)] = [min(vals), max(vals)]

    h0_a = intervals["h0"]["0.1"]
    h0_b = intervals["h0"]["3.0"]
    h1_a = intervals["h1"]["0.1"]
    h1_b = intervals["h1"]["3.0"]
    gap_h0 = h0_b[0] - h0_a[1]
    gap_h1 = h1_a[0] - h1_b[1]
    assert gap_h0 > 0.0576
    assert gap_h1 > 0.1651
    delta = min(gap_h0, gap_h1)
    n_fixed_h0 = math.ceil(2.0 / (gap_h0 * gap_h0) * math.log(20.0))
    n_fixed_h1 = math.ceil(2.0 / (gap_h1 * gap_h1) * math.log(20.0))
    # For unknown/mixed hidden phases, center oriented Bernoulli outcomes at
    # the phase-specific midpoint. Values are in [-1,1], hence the /8 exponent.
    n_mixed = math.ceil(8.0 / (delta * delta) * math.log(20.0))

    # Bretagnolle-Huber lower bound for the fixed h=0,c=0.9 binary endpoint
    # pair: sum of type-I and type-II errors >= 0.5 exp(-N KL).
    p_lower = survival(0.1, 0.9, 1.0, 0)
    q_lower = survival(3.0, 0.9, 1.0, 0)
    kl_lower_pair = bernoulli_kl(p_lower, q_lower)
    n_bh_lower = math.ceil(math.log(1.0 / (4.0 * 0.05)) / kl_lower_pair)

    # Taylor coefficient check: (S0(thetaA)-S0(thetaB))/t^2 approaches
    # 3c(thetaA-thetaB)/4; reverse sign for h=1.
    theta_a, theta_b, c = 0.1, 0.8, 1.0
    expected = 0.75 * c * (theta_a - theta_b)
    taylor_errors = {}
    for t in (1e-2, 5e-3, 2.5e-3):
        observed = (survival(theta_a, c, t, 0) - survival(theta_b, c, t, 0)) / (t * t)
        observed_h1 = (survival(theta_a, c, t, 1) - survival(theta_b, c, t, 1)) / (t * t)
        taylor_errors[str(t)] = {
            "h0_coefficient_error": observed - expected,
            "h1_coefficient_error": observed_h1 + expected,
        }

    print(
        json.dumps(
            {
                "cle_field_checks": field_checks,
                "max_actionwise_field_difference": field_max_difference,
                "survival_intervals_c_0_9_to_1_1": intervals,
                "robust_phase_gaps": {"h0": gap_h0, "h1": gap_h1},
                "hoeffding_units_for_5pct_per_hypothesis": {
                    "known_h0_stratum": n_fixed_h0,
                    "known_h1_stratum": n_fixed_h1,
                    "unknown_mixture_phase_centered_score": n_mixed,
                },
                "binary_endpoint_lower_bound_pair": {
                    "h": 0,
                    "c": 0.9,
                    "p_theta_0_1": p_lower,
                    "p_theta_3": q_lower,
                    "kl_nats": kl_lower_pair,
                    "minimum_units_from_bretagnolle_huber_for_5pct_each": n_bh_lower,
                },
                "small_time_coefficient_errors": taylor_errors,
                "scope": "finite numerical checks only; algebraic claims are in CYCLE3_CONTINUATION.md",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
