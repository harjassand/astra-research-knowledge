#!/usr/bin/env python3
"""Conditional-mean lag check for the macrophage preprint's two-state model.

This is a deterministic-size mean-field calculation, not a Gillespie replay or
a biological inference. Rates are taken from the public GitHub scripts.
"""

from __future__ import annotations

import json
import math


def hill_on_rate(n_cells: float, minimum: float, maximum: float, half: float, hill: float) -> float:
    return minimum + (maximum - minimum) * n_cells**hill / (half**hill + n_cells**hill)


def integrate(case: dict[str, float], dt_h: float = 0.001) -> dict[str, float | str]:
    lam = math.log(2.0) / 14.4
    time_h = 0.0
    p_on = case["p0"]
    while time_h < case["time_h"]:
        step = min(dt_h, case["time_h"] - time_h)
        n_cells = math.exp(lam * time_h)
        kon = hill_on_rate(
            n_cells,
            case["kmin"],
            case["kmax"],
            case["K"],
            case["hill"],
        )
        r = kon + case["koff"]
        q = kon / r
        # Exact update for rates frozen over this short time step.
        p_on = q + (p_on - q) * math.exp(-r * step)
        time_h += step

    n_cells = math.exp(lam * case["time_h"])
    kon_end = hill_on_rate(
        n_cells,
        case["kmin"],
        case["kmax"],
        case["K"],
        case["hill"],
    )
    q_end = kon_end / (kon_end + case["koff"])
    return {
        "case": case["name"],
        "lambda_per_hour": lam,
        "final_time_h": case["time_h"],
        "deterministic_final_N": n_cells,
        "p_on_mean_at_final_time": p_on,
        "instantaneous_equilibrium_at_final_N": q_end,
        "lag_q_minus_p": q_end - p_on,
        "initial_q": case["kmin"] / (case["kmin"] + case["koff"]),
    }


CASES = [
    {
        "name": "fixed-kmax public diagnostic",
        "kmin": 0.001622386,
        "kmax": 0.01707356,
        "K": 2**6.4,
        "hill": 3.0,
        "koff": 0.02277356,
        "p0": 0.075,
        "time_h": 144.0,
    },
    {
        "name": "Beta-kmax mean-parameter plug-in (not Beta expectation)",
        "kmin": 0.000672175,
        "kmax": (0.379920291 / (0.379920291 + 1.180804238)) * 0.151922586,
        "K": 77.412515570,
        "hill": 8.648981295,
        "koff": 0.028,
        "p0": 0.003,
        "time_h": 144.0,
    },
]


if __name__ == "__main__":
    print(json.dumps([integrate(case) for case in CASES], indent=2))
