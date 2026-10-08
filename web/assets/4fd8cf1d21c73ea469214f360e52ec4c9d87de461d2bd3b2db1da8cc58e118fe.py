#!/usr/bin/env python3
"""Design a single intermediate snapshot for an endpoint-aliased two-state CTMC.

The script constructs two strictly positive-rate CTMCs with the same terminal
state-1 probability, but different integrated state-1 occupancy. It then picks
the intermediate observation time minimizing the Hoeffding sample bound for
deciding which of two interventions has the larger occupancy. The time grid is
searched exhaustively, so the reported optimum is grid-relative.

Observation model: known sensitivity Se and specificity Sp, equal across arms
and times. Per-founder assay cost is constant unless --time-cost-weight is set;
then cost is 1 + weight * t/T. The independent unit is a founder lineage, not a
descendant cell. No division, death, censoring, batch effects, or interference
are represented here.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Rates:
    alpha: float  # state 0 -> state 1
    beta: float   # state 1 -> state 0

    @property
    def speed(self) -> float:
        return self.alpha + self.beta

    @property
    def stationary_state1(self) -> float:
        return self.alpha / self.speed

    def p1(self, t: float) -> float:
        return self.stationary_state1 * (-math.expm1(-self.speed * t))

    def occupancy(self, horizon: float) -> float:
        lam = self.speed
        return self.stationary_state1 * (
            horizon - (-math.expm1(-lam * horizon)) / lam
        )


def same_terminal_rates(horizon: float, terminal_probability: float, speed: float) -> Rates:
    """Return positive rates at the requested total speed and endpoint mass."""
    transition_mass = -math.expm1(-speed * horizon)
    alpha = speed * terminal_probability / transition_mass
    beta = speed - alpha
    if not (0.0 < terminal_probability < 1.0 and alpha > 0.0 and beta > 0.0):
        raise ValueError("The chosen speed must give strictly positive alpha and beta")
    return Rates(alpha=alpha, beta=beta)


def observed_probability(p: float, sensitivity: float, specificity: float) -> float:
    # P(reported 1) = false-positive rate + Youden index * P(true state 1).
    return (1.0 - specificity) + (sensitivity + specificity - 1.0) * p


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--horizon", type=float, default=1.0)
    parser.add_argument("--terminal-probability", type=float, default=0.5)
    parser.add_argument("--slow-speed-times-horizon", type=float, default=0.7)
    parser.add_argument("--fast-speed-times-horizon", type=float, default=10.0)
    parser.add_argument("--delta", type=float, default=0.05)
    parser.add_argument("--sensitivity", type=float, default=1.0)
    parser.add_argument("--specificity", type=float, default=1.0)
    parser.add_argument("--grid-size", type=int, default=20000)
    parser.add_argument("--time-cost-weight", type=float, default=0.0)
    args = parser.parse_args()

    if args.horizon <= 0 or args.grid_size < 2:
        raise ValueError("horizon must be positive and grid-size at least 2")
    if not (0.0 < args.delta < 1.0):
        raise ValueError("delta must lie strictly between 0 and 1")
    if not (0.0 <= args.sensitivity <= 1.0 and 0.0 <= args.specificity <= 1.0):
        raise ValueError("sensitivity and specificity must be probabilities")
    if args.time_cost_weight < 0.0:
        raise ValueError("time-cost-weight must be nonnegative")
    if args.sensitivity + args.specificity <= 1.0:
        raise ValueError("The calibrated reporter must have positive Youden index")

    slow = same_terminal_rates(
        args.horizon,
        args.terminal_probability,
        args.slow_speed_times_horizon / args.horizon,
    )
    fast = same_terminal_rates(
        args.horizon,
        args.terminal_probability,
        args.fast_speed_times_horizon / args.horizon,
    )

    best = None
    for i in range(1, args.grid_size):
        tau = args.horizon * i / args.grid_size
        q_slow = observed_probability(slow.p1(tau), args.sensitivity, args.specificity)
        q_fast = observed_probability(fast.p1(tau), args.sensitivity, args.specificity)
        gap = abs(q_fast - q_slow)
        if gap <= 0.0:
            continue
        n_per_arm = math.ceil(math.log(1.0 / args.delta) / (gap * gap))
        per_founder_cost = 1.0 + args.time_cost_weight * tau / args.horizon
        total_cost = 2.0 * n_per_arm * per_founder_cost
        # Primary objective is total cost; among equal-cost grid points retain
        # the larger separation (smaller actual error bound), then the earlier time.
        candidate = (total_cost, -gap, tau, n_per_arm, q_fast, q_slow, per_founder_cost)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        raise ValueError("No informative observation time exists for this reporter")

    total_cost, neg_gap, tau, n_per_arm, q_fast, q_slow, per_founder_cost = best
    gap = -neg_gap
    result = {
        "scope": "two specified worlds that swap fast and slow CTMCs across arms",
        "horizon": args.horizon,
        "terminal_probability_target": args.terminal_probability,
        "slow_rates": asdict(slow),
        "fast_rates": asdict(fast),
        "terminal_probabilities": {
            "slow": slow.p1(args.horizon),
            "fast": fast.p1(args.horizon),
        },
        "integrated_state1_occupancy": {
            "slow": slow.occupancy(args.horizon),
            "fast": fast.occupancy(args.horizon),
            "gap": fast.occupancy(args.horizon) - slow.occupancy(args.horizon),
            "minimax_regret_lower_bound": (
                fast.occupancy(args.horizon) - slow.occupancy(args.horizon)
            ) / 2.0,
        },
        "reporter": {
            "sensitivity": args.sensitivity,
            "specificity": args.specificity,
            "youden_index": args.sensitivity + args.specificity - 1.0,
        },
        "chosen_intermediate_time": tau,
        "chosen_intermediate_time_fraction": tau / args.horizon,
        "reported_state1_probabilities_at_chosen_time": {
            "slow": q_slow,
            "fast": q_fast,
        },
        "reported_probability_gap": gap,
        "per_arm_founder_lineages_for_error_at_most_delta": n_per_arm,
        "total_founder_lineages_across_two_arms": 2 * n_per_arm,
        "hoeffding_error_bound": math.exp(-n_per_arm * gap * gap),
        "assumed_per_founder_cost": per_founder_cost,
        "total_intermediate_assay_cost_units": total_cost,
        "grid_size": args.grid_size,
        "cost_model": "per founder = 1 + time_cost_weight * tau/horizon",
        "limitations": [
            "grid optimum only; continuous optimum not certified",
            "assumes independent randomized founder lineages",
            "assumes the supplied CTMC alternatives and known nondifferential reporter error",
            "does not model division, death, censoring, batch effects, or interference",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
