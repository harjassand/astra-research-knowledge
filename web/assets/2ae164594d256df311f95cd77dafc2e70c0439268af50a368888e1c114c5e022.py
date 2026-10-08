#!/usr/bin/env python3
"""Synthetic algebra check for the finite-memory enhancer kernel; no data loaded."""
from __future__ import annotations
import json
import math


def f(z: float) -> float:
    if z < 0:
        raise ValueError("z=beta*T must be nonnegative")
    if z == 0:
        return 0.5
    if z < 1e-3:
        # Taylor series of (z - 1 + exp(-z))/z**2.
        return 0.5 - z / 6 + z * z / 24 - z**3 / 120 + z**4 / 720
    return (z + math.expm1(-z)) / (z * z)


def opening_term(alpha: float, area: float, beta: float, duration: float) -> float:
    return alpha * area * area * f(beta * duration)


def main() -> None:
    alpha, area, beta = 0.02, 100.0, 0.02
    t_short, t_long = 10.0, 60.0
    q_short = opening_term(alpha, area, beta, t_short)
    q_long = opening_term(alpha, area, beta, t_long)
    assert f(0.0) == 0.5
    assert f(beta * t_short) > f(beta * t_long)
    assert math.isclose(q_short / q_long, f(beta * t_short) / f(beta * t_long))
    print(json.dumps({
        "status": "synthetic_closed_form_check_only",
        "parameters": {"alpha": alpha, "matched_TF_area": area, "beta_per_min": beta},
        "durations_minutes": {
            str(int(t_short)): {"beta_T": beta * t_short, "f": f(beta*t_short), "opening_term": q_short},
            str(int(t_long)): {"beta_T": beta * t_long, "f": f(beta*t_long), "opening_term": q_long}
        },
        "short_over_long_opening_component": q_short / q_long,
        "meaning": "Same synthetic TF area gives different effective-enhancer contribution under the stated finite-memory model; no biological parameter estimates or data are used."
    }, indent=2))


if __name__ == "__main__":
    main()
