#!/usr/bin/env python3
"""Tiny numerical sanity checks for the Gaussian and N66 score constants.

This is not a proof or a theorem test. It checks one explicit regular sensor
h(x)=x/2 under Unif[-1,1] and the quoted Gaussian constant arithmetic.
Run with: python3 check_converse_constants.py
"""

import json
import math


def clipped(value, low=-1.0, high=1.0):
    return min(high, max(low, value))


def regular_sensor_F(p: float, r: float) -> float:
    """Potential with F'(p)=clip(h^{-1}((2p-1)/r)), h(x)=x/2."""
    left = 0.5 - r / 4.0
    right = 0.5 + r / 4.0
    if p <= left:
        return -p
    if p <= right:
        return -left + (2.0 / r) * ((p - 0.5) ** 2 - (left - 0.5) ** 2)
    return p - 1.0


def regular_sensor_Fprime(p: float, r: float) -> float:
    return clipped(2.0 * (2.0 * p - 1.0) / r)


def main() -> None:
    # N36: ratio r/eps = 128.
    gaussian_nats = 0.5 * math.log(128.0) - (1.25 + math.log(2.0))
    gaussian_bits = gaussian_nats / math.log(2.0)
    assert abs(gaussian_nats - 0.4828679513998632) < 1e-14

    # N66 explicit sensor: rho=1/2, h(x)=x/2, c0=H1=1/2.
    r = 0.8
    c0 = 0.5
    H1 = 0.5
    target_regret_constant = c0 * r / 4.0
    grid = [-1.0 + 2.0 * k / 80.0 for k in range(81)]
    max_regret_shortfall = 0.0
    min_loss = math.inf
    max_loss = -math.inf
    for x in grid:
        p_x = (1.0 + r * (x / 2.0)) / 2.0
        for y in grid:
            p_y = (1.0 + r * (y / 2.0)) / 2.0
            regret = (
                regular_sensor_F(p_x, r)
                - regular_sensor_F(p_y, r)
                - (p_x - p_y) * regular_sensor_Fprime(p_y, r)
            )
            required = target_regret_constant * (x - y) ** 2
            max_regret_shortfall = max(max_regret_shortfall, required - regret)
        for t in (0.0, 1.0):
            loss = (
                regular_sensor_F(t, r)
                - regular_sensor_F(p_x, r)
                - (t - p_x) * regular_sensor_Fprime(p_x, r)
            )
            min_loss = min(min_loss, loss)
            max_loss = max(max_loss, loss)

    assert max_regret_shortfall <= 1e-12
    assert min_loss >= -1e-12
    assert max_loss <= 2.0 + 1e-12

    density_bound = 0.5
    A = 16.0 * math.pi * math.e * density_bound**2 / c0
    result = {
        "status": "finite numerical sanity checks only",
        "gaussian_r_over_epsilon": 128,
        "gaussian_lower_nats_per_coordinate": gaussian_nats,
        "gaussian_lower_bits_per_coordinate": gaussian_bits,
        "regular_sensor": {
            "reference": "Unif[-1,1]",
            "h": "x/2",
            "r": r,
            "c0": c0,
            "H1": H1,
            "regret_coefficient_c0_r_over_4": target_regret_constant,
            "max_grid_regret_inequality_shortfall": max_regret_shortfall,
            "loss_grid_min": min_loss,
            "loss_grid_max": max_loss,
            "sensor_A": A,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
