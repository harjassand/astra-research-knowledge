#!/usr/bin/env python3
"""Exact static selectivity/throughput gates for reversible-SET branch networks.

Model boundary: each channel i is fed at rate alpha_i * D, where
alpha_i = k_ET,i [S_i]; its radical intermediate is lost either to product at
first-order rate c_i or by back electron transfer at pseudo-first-order rate
b_i A. D and A are the reduced and oxidized catalyst concentrations. This is
an exact QSS model for the declared two-state network, not a fit to the Nature
reaction or a claim that a multi-step pathway has a single measured c_i.

All arithmetic in the certificate uses fractions. Rates, concentrations, and
the linear catalyst-pool constraint D + A = C_total must be supplied in
consistent units.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from typing import Iterable


def as_fraction(value: str | int | F) -> F:
    return value if isinstance(value, F) else F(value)


def flux_weight(alpha: F, c: F, b: F, acceptor: F) -> F:
    """Product flux divided by reduced catalyst D: alpha*c/(c+b*A)."""
    if alpha <= 0 or c <= 0 or b <= 0 or acceptor < 0:
        raise ValueError("alpha, c, b must be positive and A must be nonnegative")
    return alpha * c / (c + b * acceptor)


def target_fraction(
    alpha_target: F,
    c_target: F,
    b_target: F,
    alpha_side: F,
    c_side: F,
    b_side: F,
    acceptor: F,
) -> F:
    """Target-product fraction for two competing channels."""
    target = flux_weight(alpha_target, c_target, b_target, acceptor)
    side = flux_weight(alpha_side, c_side, b_side, acceptor)
    return target / (target + side)


def maximum_target_fraction(
    alpha_target: F,
    c_target: F,
    b_target: F,
    alpha_side: F,
    c_side: F,
    b_side: F,
) -> F:
    """Limiting target fraction as A -> infinity (fixed D for selectivity)."""
    target = alpha_target * c_target / b_target
    side = alpha_side * c_side / b_side
    return target / (target + side)


def minimum_acceptor(
    alpha_target: F,
    c_target: F,
    b_target: F,
    alpha_side: F,
    c_side: F,
    b_side: F,
    desired_fraction: F,
) -> F | None:
    """Smallest finite A meeting a selectivity floor, if it is reachable.

    Requires target kinetic commitment q_target=c_target/b_target to be at
    least that of the competing side channel. Returns None if the desired
    fraction exceeds the large-A limit; returns 0 if already satisfied at A=0.
    """
    if not (0 < desired_fraction < 1):
        raise ValueError("desired_fraction must lie strictly between zero and one")
    rho = desired_fraction / (1 - desired_fraction)
    zero_acceptor_odds = alpha_target / alpha_side
    if zero_acceptor_odds >= rho:
        return F(0)
    ceiling = maximum_target_fraction(
        alpha_target, c_target, b_target, alpha_side, c_side, b_side
    )
    if desired_fraction >= ceiling:
        return None
    denominator = alpha_target * c_target * b_side - rho * c_side * b_target
    numerator = c_target * c_side * (rho - zero_acceptor_odds)
    if denominator <= 0:
        return None
    result = numerator / denominator
    if result < 0:
        raise AssertionError("positive target above its zero-A ratio yielded A < 0")
    return result


def target_throughput(
    alpha_target: F,
    c_target: F,
    b_target: F,
    acceptor: F,
    catalyst_total: F,
) -> F:
    """Target product flux for D=C_total-A; zero if A exceeds pool size."""
    if catalyst_total < 0 or acceptor < 0:
        raise ValueError("concentrations must be nonnegative")
    if acceptor > catalyst_total:
        return F(0)
    donor = catalyst_total - acceptor
    return donor * flux_weight(alpha_target, c_target, b_target, acceptor)


def minimum_commitment_rate_ratio(g: F, beta: F, target_odds: F) -> F | None:
    """Minimum u=c_target/c_easy at fixed common BET exposure.

    Here g=(kET_target[S_target])/(kET_easy[S_easy]) and
    beta=(kBET[A])/c_easy. The product odds are
        R = g*u*(1+beta)/(u+beta).
    None means the requested odds exceed the u -> infinity ceiling.
    """
    if g <= 0 or beta < 0 or target_odds <= 0:
        raise ValueError("g and target_odds must be positive; beta nonnegative")
    denominator = g * (1 + beta) - target_odds
    if denominator <= 0:
        return None
    return target_odds * beta / denominator


def robust_multichannel_gate(
    channels: list[dict[str, F]],
    target_index: int,
    catalyst_pool: F,
    desired_fraction: F,
    bisection_steps: int = 80,
) -> dict[str, object]:
    """Certified rational bracket for a robust N-channel static design.

    Each channel supplies rectangular intervals for alpha=k_ET[S] and
    q=c/b (productive commitment concentration): alpha_lo/hi and q_lo/hi.
    For a given A the robust lower bound uses the target's lower values and
    every competitor's upper values. A monotone threshold is certified only
    when q_target_lo >= max(q_competitor_hi); otherwise the result is UNKNOWN.
    """
    if len(channels) < 2 or not (0 <= target_index < len(channels)):
        raise ValueError("need at least two channels and a valid target index")
    if catalyst_pool < 0 or not (0 < desired_fraction < 1) or bisection_steps < 1:
        raise ValueError("invalid pool, selectivity floor, or bisection count")
    for ch in channels:
        if not (0 < ch["alpha_lo"] <= ch["alpha_hi"]):
            raise ValueError("alpha intervals must be positive and ordered")
        if not (0 < ch["q_lo"] <= ch["q_hi"]):
            raise ValueError("q intervals must be positive and ordered")

    target = channels[target_index]
    competitors = [ch for i, ch in enumerate(channels) if i != target_index]
    if target["q_lo"] < max(ch["q_hi"] for ch in competitors):
        return {"status": "UNKNOWN", "reason": "robust commitment ordering is not certified"}

    def lower_share(acceptor: F) -> F:
        good = target["alpha_lo"] * target["q_lo"] / (acceptor + target["q_lo"])
        bad = sum(
            (ch["alpha_hi"] * ch["q_hi"] / (acceptor + ch["q_hi"])
             for ch in competitors),
            F(0),
        )
        return good / (good + bad)

    asymptotic = (
        target["alpha_lo"] * target["q_lo"]
        / (target["alpha_lo"] * target["q_lo"]
           + sum((ch["alpha_hi"] * ch["q_hi"] for ch in competitors), F(0)))
    )
    if lower_share(F(0)) >= desired_fraction:
        donor = catalyst_pool
        target_flux_lower = target["alpha_lo"] * donor
        return {
            "status": "CERTIFIED_BRACKET",
            "acceptor_root_bracket": [F(0), F(0)],
            "lower_share_at_low": lower_share(F(0)),
            "lower_share_at_high": lower_share(F(0)),
            "robust_high_A_ceiling": asymptotic,
            "conservative_setpoint_A": F(0),
            "donor_at_setpoint": donor,
            "target_flux_lower_bound": target_flux_lower,
            "target_SET_attempts_per_product_upper_bound": F(1),
            "bisection_steps": 0,
        }
    if desired_fraction >= asymptotic:
        return {
            "status": "REFUTED",
            "reason": "selectivity floor reaches or exceeds the robust infinite-A ceiling",
            "robust_high_A_ceiling": asymptotic,
        }

    low, high = F(0), catalyst_pool
    if lower_share(low) >= desired_fraction:
        high = low
    elif lower_share(high) < desired_fraction:
        return {
            "status": "REFUTED",
            "reason": "selectivity floor is not reached before the finite catalyst pool is exhausted",
            "robust_share_at_pool": lower_share(catalyst_pool),
            "robust_high_A_ceiling": asymptotic,
        }
    else:
        for _ in range(bisection_steps):
            mid = (low + high) / 2
            if lower_share(mid) >= desired_fraction:
                high = mid
            else:
                low = mid

    # Choose the upper rational endpoint for a conservative implementable
    # setpoint; its selectivity is verified directly by exact arithmetic.
    acceptor_setpoint = high
    donor = catalyst_pool - acceptor_setpoint
    target_flux_lower = (
        donor * target["alpha_lo"] * target["q_lo"]
        / (acceptor_setpoint + target["q_lo"])
    )
    return {
        "status": "CERTIFIED_BRACKET",
        "acceptor_root_bracket": [low, high],
        "lower_share_at_low": lower_share(low),
        "lower_share_at_high": lower_share(high),
        "robust_high_A_ceiling": asymptotic,
        "conservative_setpoint_A": acceptor_setpoint,
        "donor_at_setpoint": donor,
        "target_flux_lower_bound": target_flux_lower,
        "target_SET_attempts_per_product_upper_bound": 1 + acceptor_setpoint / target["q_lo"],
        "bisection_steps": bisection_steps,
    }


def exact_certificate() -> dict[str, object]:
    # SI Figure S2.18's fit label and its later discussion give 4e9 for Ket-1;
    # the same figure caption inconsistently says 3e10. The caption-consistent
    # source ratio is not silently used: both values are exposed here.
    alpha_hard_over_easy = F(4, 30)  # equal substrate concentrations
    ratios = {
        str(p): F(p, 1 - p) / alpha_hard_over_easy
        for p in (F(7, 10), F(9, 10), F(19, 20))
    }
    # SI's Fig. 5c illustration: kdiff=1e10 M^-1s^-1, [A]=5.6e-5 M,
    # and competing sink k2=1e3 s^-1, hence beta=kdiff[A]/k2=560.
    beta_illustration = F(560)
    finite_beta_gates = {}
    for g_name, g in (("SI_ideal_equal_forward", F(1)), ("caption_consistent_measured_ratio", alpha_hard_over_easy)):
        finite_beta_gates[g_name] = {}
        for p, label in ((F(9, 10), "90% target share"), (F(10, 11), "10:1 product odds")):
            rho = p / (1 - p)
            u = minimum_commitment_rate_ratio(g, beta_illustration, rho)
            if u is None:
                raise AssertionError("finite-beta example should be feasible")
            target_commitment = u / (beta_illustration + u)
            side_commitment = F(1, 1 + beta_illustration)
            finite_beta_gates[g_name][label] = {
                "minimum_u": str(u),
                "target_commitment_per_SET_attempt": str(target_commitment),
                "target_SET_attempts_per_product": str(1 / target_commitment),
                "side_commitment_per_SET_attempt": str(side_commitment),
                "side_SET_attempts_per_product": str(1 / side_commitment),
                "selectivity_check": str(
                    (g * u * (1 + beta_illustration) / (u + beta_illustration))
                    / (1 + g * u * (1 + beta_illustration) / (u + beta_illustration))
                ),
            }
    # Constructed exact witness for the static setpoint result. These are not
    # measured chemical parameters; they only exercise the theorem/checker.
    params = {
        "alpha_target": F(2, 15),
        "c_target": F(1),
        "b_target": F(10_000),
        "alpha_side": F(1),
        "c_side": F(1),
        "b_side": F(1_000_000),
        "pool": F(1, 1000),  # 1 mM in matching concentration units
        "floor": F(9, 10),
    }
    a_star = minimum_acceptor(
        params["alpha_target"], params["c_target"], params["b_target"],
        params["alpha_side"], params["c_side"], params["b_side"],
        params["floor"],
    )
    feasible = a_star is not None and a_star <= params["pool"]
    if not feasible or a_star is None:
        raise AssertionError("constructed witness should meet the 90% floor")
    got = target_fraction(
        params["alpha_target"], params["c_target"], params["b_target"],
        params["alpha_side"], params["c_side"], params["b_side"], a_star,
    )
    if got != params["floor"]:
        raise AssertionError(f"threshold equality failed: {got} != {params['floor']}")
    rate_at_threshold = target_throughput(
        params["alpha_target"], params["c_target"], params["b_target"],
        a_star, params["pool"],
    )
    # A larger A decreases target throughput when the catalyst pool is fixed.
    a_larger = (a_star + params["pool"]) / 2
    if a_larger <= a_star or target_throughput(
        params["alpha_target"], params["c_target"], params["b_target"],
        a_larger, params["pool"],
    ) >= rate_at_threshold:
        raise AssertionError("target flux must decrease beyond the minimum-A setpoint")
    # Exact monotonicity witness for q_target > q_side.
    test_points = [F(0), F(1, 1_000_000), F(1, 1000), F(1, 100), F(1, 10)]
    values = [
        target_fraction(
            params["alpha_target"], params["c_target"], params["b_target"],
            params["alpha_side"], params["c_side"], params["b_side"], a,
        )
        for a in test_points
    ]
    if values != sorted(values):
        raise AssertionError("target fraction did not increase on the exact witness")
    # If the high-A commitment ceiling is below the target, no A can achieve it.
    impossible = minimum_acceptor(
        F(2, 15), F(1), F(1), F(1), F(1), F(1), F(4, 5)
    )
    if impossible is not None:
        raise AssertionError("an 80% target above its high-A ceiling must be rejected")
    if minimum_commitment_rate_ratio(F(2, 15), beta_illustration, F(9)) != F(25200, 329):
        raise AssertionError("finite-beta unequal-SET 90% gate changed")
    if minimum_commitment_rate_ratio(F(2, 15), beta_illustration, F(10)) != F(7000, 81):
        raise AssertionError("finite-beta unequal-SET 10:1 gate changed")

    # Three-channel rectangular-uncertainty design. The target has a certified
    # larger c/b commitment scale than either side channel; exact bisection
    # finds a conservative A setpoint under a finite catalyst pool.
    multi = robust_multichannel_gate(
        [
            {"alpha_lo": F(10), "alpha_hi": F(12), "q_lo": F(1, 100), "q_hi": F(1, 50)},
            {"alpha_lo": F(1, 2), "alpha_hi": F(1), "q_lo": F(1, 1000), "q_hi": F(1, 1000)},
            {"alpha_lo": F(1, 2), "alpha_hi": F(1), "q_lo": F(1, 500), "q_hi": F(3, 1000)},
        ],
        target_index=0,
        catalyst_pool=F(1, 10),
        desired_fraction=F(9, 10),
        bisection_steps=40,
    )
    if multi["status"] != "CERTIFIED_BRACKET":
        raise AssertionError(f"expected a certified multichannel setpoint: {multi}")
    if multi["lower_share_at_high"] < F(9, 10):
        raise AssertionError("multichannel upper endpoint failed the exact robust share floor")
    if multi["lower_share_at_low"] >= F(9, 10):
        raise AssertionError("multichannel lower endpoint should remain below the root")
    unordered = robust_multichannel_gate(
        [
            {"alpha_lo": F(1), "alpha_hi": F(2), "q_lo": F(1), "q_hi": F(3)},
            {"alpha_lo": F(1), "alpha_hi": F(2), "q_lo": F(2), "q_hi": F(4)},
        ],
        target_index=0,
        catalyst_pool=F(1),
        desired_fraction=F(1, 2),
        bisection_steps=10,
    )
    if unordered["status"] != "UNKNOWN":
        raise AssertionError("unverified commitment ordering must return UNKNOWN")
    constant_share = robust_multichannel_gate(
        [
            {"alpha_lo": F(1), "alpha_hi": F(1), "q_lo": F(1), "q_hi": F(1)},
            {"alpha_lo": F(1), "alpha_hi": F(1), "q_lo": F(1), "q_hi": F(1)},
        ],
        target_index=0,
        catalyst_pool=F(1),
        desired_fraction=F(1, 2),
        bisection_steps=10,
    )
    if constant_share["status"] != "CERTIFIED_BRACKET" or constant_share["conservative_setpoint_A"] != F(0):
        raise AssertionError("a floor met at zero acceptor must remain feasible at the asymptotic ceiling")

    return {
        "source_input": {
            "kET_hard_over_easy": "2/15",
            "basis": "equal substrate concentration; Figure S2.18 plot label / later SI note",
            "figure_caption_conflict": "caption says 3e10 for Ket-1; plot label says 4e9",
        },
        "required_commitment_ratio_q_hard_over_q_easy": {
            str(p): str(v) for p, v in ratios.items()
        },
        "finite_acceptor_model_gate": {
            "beta": str(beta_illustration),
            "definition": "beta = k_diff*[A]/k2 = 560 from the SI Figure 5c settings (S97); illustrative, not fitted to Ket-1",
            "minimum_chemical_rate_ratio_u": finite_beta_gates,
        },
        "interpretation": {
            "70% hard product": "q_hard/q_easy >= 17.5 in the high-A limit",
            "90% hard product": "q_hard/q_easy >= 67.5 in the high-A limit",
            "95% hard product": "q_hard/q_easy >= 142.5 in the high-A limit",
            "observed 70:7 A:B odds": "q_hard/q_easy >= 75 in the high-A limit",
            "status": "conditional thresholds, not measured q values or a fit",
        },
        "constructed_exact_setpoint_witness": {
            "A_min": str(a_star),
            "pool": str(params["pool"]),
            "selectivity_at_A_min": str(got),
            "target_flux_at_A_min": str(rate_at_threshold),
            "selectivity_samples": [str(x) for x in values],
            "unreachable_example": impossible is None,
            "parameters_status": "constructed mathematical witness only",
        },
        "robust_three_channel_interval_witness": {
            key: str(value) if isinstance(value, F) else (
                [str(x) for x in value] if isinstance(value, list) else value
            )
            for key, value in multi.items()
        },
        "checks": [
            "exact rational 70/90/95-percent kinetic-commitment thresholds",
            "exact threshold equality at the calculated A_min",
            "exact monotonicity samples for the constructed q_target>q_side witness",
            "exact impossibility rejection above the high-A selectivity ceiling",
            "fixed-pool target-throughput decreases beyond the minimum feasible A",
            "exact finite-BET commitment-rate gates for both measured and ideal equal-SET branches",
            "exact rational bisection bracket for an interval-robust three-channel setpoint",
            "UNKNOWN returned when target commitment ordering is not established",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(exact_certificate(), indent=2))
