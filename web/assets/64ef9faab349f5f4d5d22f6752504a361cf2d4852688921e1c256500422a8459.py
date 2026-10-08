#!/usr/bin/env python3
"""Exact rational check for the parallel-channel LDB selectivity obstruction.

No simulation is involved. Rates are per one catalyst. The factor-two/half
choice corresponds to A = log(4), so all event-rate checks are rational.
"""
from fractions import Fraction as F

GAMMA = F(1, 1)              # s^-1 per catalyst
FORWARD_FACTOR = F(2, 1)     # exp(A/2), hence A = log(4)
REVERSE_FACTOR = F(1, 2)     # exp(-A/2)
HORIZON = F(1, 1)            # seconds


def module(theta: F) -> dict[str, F]:
    weights = (theta, 1 - theta)
    forward = tuple(w * GAMMA * FORWARD_FACTOR for w in weights)
    reverse = tuple(w * GAMMA * REVERSE_FACTOR for w in weights)
    currents = tuple(f - r for f, r in zip(forward, reverse))
    traffics = tuple(f + r for f, r in zip(forward, reverse))
    total_forward = sum(forward, F(0))
    total_reverse = sum(reverse, F(0))
    total_current = sum(currents, F(0))
    total_traffic = sum(traffics, F(0))
    return {
        "target_selectivity": currents[0] / total_current,
        "target_traffic_share": traffics[0] / total_traffic,
        "total_forward_rate": total_forward,
        "total_reverse_rate": total_reverse,
        "total_net_flux": total_current,
        "total_physical_traffic": total_traffic,
        "expected_forward_marks_at_horizon": total_forward * HORIZON,
        "expected_reverse_events_at_horizon": total_reverse * HORIZON,
        "expected_all_events_at_horizon": total_traffic * HORIZON,
        "expected_net_product_at_horizon": total_current * HORIZON,
        # Reservoir chemical work in units of k_B T is log(4) per net event.
        "expected_chemical_work_coefficient_at_horizon": total_current * HORIZON,
    }


def main() -> None:
    low = module(F(1, 10))
    high = module(F(9, 10))
    assert low == {
        "target_selectivity": F(1, 10),
        "target_traffic_share": F(1, 10),
        "total_forward_rate": F(2),
        "total_reverse_rate": F(1, 2),
        "total_net_flux": F(3, 2),
        "total_physical_traffic": F(5, 2),
        "expected_forward_marks_at_horizon": F(2),
        "expected_reverse_events_at_horizon": F(1, 2),
        "expected_all_events_at_horizon": F(5, 2),
        "expected_net_product_at_horizon": F(3, 2),
        "expected_chemical_work_coefficient_at_horizon": F(3, 2),
    }
    assert high["target_selectivity"] == F(9, 10)
    for k in low:
        if k not in {"target_selectivity", "target_traffic_share"}:
            assert low[k] == high[k], k
    # Conditional on n total forward product-formation events, the target
    # mark count is Binomial(n, theta). No event count is supplied for free:
    # E[n] = 2 s^-1 * horizon, and all-direction E[N] = 2.5 s^-1 * horizon.
    print("A = log(4); horizon = 1 s; Gamma = 1 s^-1; per-catalyst exact rates")
    print("theta=1/10:", {k: str(v) for k, v in low.items()})
    print("theta=9/10:", {k: str(v) for k, v in high.items()})
    print("common expected chemical work = (3/2) log(4) k_B T")
    print("common event-count laws: N+~Poisson(2), N-~Poisson(1/2), independent")


if __name__ == "__main__":
    main()
