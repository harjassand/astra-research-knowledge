#!/usr/bin/env python3
"""Cost calculator for the Astra N35 example and a black-box rare-risk audit."""

import argparse
import json
import math


def n35_exit_bound(volume: int, horizon: float) -> float:
    """Equation (7): two-species finite-volume exit bound, clipped at one."""
    if volume <= 0 or horizon < 0:
        raise ValueError("volume must be positive and horizon nonnegative")
    a = 2.0 * math.exp(-3.0 * volume / 25.0)
    b = (108.0 / 35.0) * volume * horizon * math.exp(-3.0 * volume / 200.0)
    return min(1.0, a + b)


def n35_max_horizon(volume: int, risk: float) -> float:
    """Largest T certified by equation (7) for the supplied risk threshold."""
    if volume <= 0 or not 0.0 < risk < 1.0:
        raise ValueError("volume must be positive and risk must lie in (0, 1)")
    initial = 2.0 * math.exp(-3.0 * volume / 25.0)
    if risk <= initial:
        return 0.0
    return (risk - initial) * (35.0 / (108.0 * volume)) * math.exp(3.0 * volume / 200.0)


def zero_failure_episodes(alpha: float, risk: float) -> int:
    """One-sided exact-binomial zero-failure sample threshold."""
    if not 0.0 < alpha < 1.0 or not 0.0 < risk < 1.0:
        raise ValueError("alpha and risk must lie in (0, 1)")
    return math.ceil(math.log(alpha) / math.log1p(-risk))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--volume", type=int, default=3000)
    parser.add_argument("--risk", type=float, default=1e-6)
    parser.add_argument("--confidence-failure", type=float, default=0.05)
    parser.add_argument("--horizon-steps", type=int, default=1_000_000)
    args = parser.parse_args()

    t_max = n35_max_horizon(args.volume, args.risk)
    episodes = zero_failure_episodes(args.confidence_failure, args.risk)
    per_step_risk = -math.expm1(math.log1p(-args.risk) / args.horizon_steps)
    transition_exposures = math.ceil(
        math.log(args.confidence_failure) / math.log1p(-per_step_risk)
    )
    activity_bound = 2.5 * args.volume
    report = {
        "interface": {
            "n35": "supplied integer reaction model and strict inward certificate",
            "black_box": "frozen feedback policy; independent reset trajectories; event-only lower bound",
        },
        "n35": {
            "volume": args.volume,
            "risk_target": args.risk,
            "max_certified_horizon_rate_time": t_max,
            "bound_at_max_horizon": n35_exit_bound(args.volume, t_max),
            "expected_thinning_candidates_upper_bound": activity_bound * t_max,
            "bound_at_exponential_horizon": n35_exit_bound(
                args.volume, math.exp(3.0 * args.volume / 400.0)
            ),
            "exponential_horizon": math.exp(3.0 * args.volume / 400.0),
        },
        "black_box_zero_failure": {
            "confidence": 1.0 - args.confidence_failure,
            "horizon_steps": args.horizon_steps,
            "trajectory_risk_target": args.risk,
            "required_independent_episodes": episodes,
            "transition_evaluations": episodes * args.horizon_steps,
            "per_step_hazard_threshold": per_step_risk,
            "required_independent_transition_exposures": transition_exposures,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
