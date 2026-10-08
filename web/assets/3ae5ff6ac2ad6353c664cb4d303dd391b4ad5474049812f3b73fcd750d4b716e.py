"""Exact response and finite diagnostics for the U <-> C <-> B RNA CTMC.

This script implements the model formulas in CYCLE2_REPORT.md.  Its numerical
checks are finite diagnostics; the all-dose/all-time ordering is established by
the proof in the report, not by grid testing.
"""

from __future__ import annotations

import math
from typing import Mapping


def p_bound(alpha: float, beta: float, kon: float, koff: float,
            concentration: float, time: float) -> float:
    """P(B at time) from initial U, with concentration in matching units."""
    if min(alpha, beta, kon, koff, concentration, time) < 0:
        raise ValueError("rates, concentration, and time must be nonnegative")
    gamma = concentration * kon
    if gamma == 0 or alpha == 0 or time == 0:
        return 0.0

    S = alpha + beta + gamma + koff
    D = alpha * gamma + alpha * koff + beta * koff
    if D == 0:
        return 0.0
    discriminant = max(0.0, S * S - 4.0 * D)
    gap = math.sqrt(discriminant)
    r_minus = (S - gap) / 2.0
    r_plus = (S + gap) / 2.0
    pi_bound = alpha * gamma / D

    if gap <= 1e-10 * max(1.0, S):
        r = S / 2.0
        return pi_bound * (1.0 - (1.0 + r * time) * math.exp(-r * time))

    numerator = (r_plus * math.exp(-r_minus * time)
                 - r_minus * math.exp(-r_plus * time))
    return pi_bound * (1.0 - numerator / gap)


def robustly_dominates(a: Mapping[str, float], b: Mapping[str, float]) -> bool:
    """Sufficient rate order for all concentration/time response dominance."""
    return (a["alpha"] >= b["alpha"]
            and a["beta"] <= b["beta"]
            and a["kon"] >= b["kon"]
            and a["koff"] <= b["koff"])


def response_band(box: Mapping[str, tuple[float, float]],
                  concentration: float, time: float) -> tuple[float, float]:
    """Monotone-corner response interval for a rectangular rate confidence set."""
    lower = p_bound(box["alpha"][0], box["beta"][1], box["kon"][0],
                    box["koff"][1], concentration, time)
    upper = p_bound(box["alpha"][1], box["beta"][0], box["kon"][1],
                    box["koff"][0], concentration, time)
    return lower, upper


def rk4_bound(alpha: float, beta: float, kon: float, koff: float,
              concentration: float, time: float, steps: int = 20000) -> float:
    """Independent RK4 solution of the forward equations for finite checks."""
    if time == 0:
        return 0.0
    gamma = concentration * kon
    h = time / steps
    state = (1.0, 0.0, 0.0)

    def rhs(p: tuple[float, float, float]) -> tuple[float, float, float]:
        u, c_state, bound = p
        return (-alpha * u + beta * c_state,
                alpha * u - (beta + gamma) * c_state + koff * bound,
                gamma * c_state - koff * bound)

    def add(p: tuple[float, float, float],
            q: tuple[float, float, float], scale: float) -> tuple[float, float, float]:
        return tuple(x + scale * y for x, y in zip(p, q))

    for _ in range(steps):
        k1 = rhs(state)
        k2 = rhs(add(state, k1, h / 2.0))
        k3 = rhs(add(state, k2, h / 2.0))
        k4 = rhs(add(state, k3, h))
        state = tuple(x + h * (a + 2 * b + 2 * c + d) / 6.0
                      for x, a, b, c, d in zip(state, k1, k2, k3, k4))
    return state[2]


def first_crossing(a: Mapping[str, float], b: Mapping[str, float],
                   concentration: float, lo: float, hi: float,
                   iterations: int = 100) -> float:
    """Bisection for a sign-changing response difference on [lo, hi]."""
    def difference(t: float) -> float:
        return (p_bound(**a, concentration=concentration, time=t)
                - p_bound(**b, concentration=concentration, time=t))

    left_value = difference(lo)
    right_value = difference(hi)
    if left_value == 0:
        return lo
    if right_value == 0:
        return hi
    if left_value * right_value > 0:
        raise ValueError("interval does not bracket a crossing")
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        mid_value = difference(mid)
        if left_value * mid_value <= 0:
            hi = mid
            right_value = mid_value
        else:
            lo = mid
            left_value = mid_value
    return (lo + hi) / 2.0


def main() -> None:
    kon_pbuE = 2.6e5  # M^-1 s^-1; reported at 35 C
    koff_pbuE = 0.15  # s^-1; reported at 35 C
    favorable_a = {"alpha": 2.0, "beta": 0.5,
                   "kon": kon_pbuE, "koff": koff_pbuE}
    favorable_b = {"alpha": 0.5, "beta": 2.0,
                   "kon": kon_pbuE, "koff": koff_pbuE}
    assert robustly_dominates(favorable_a, favorable_b)
    at_c = 10e-6
    at_t = 2.0
    p_a = p_bound(**favorable_a, concentration=at_c, time=at_t)
    p_b = p_bound(**favorable_b, concentration=at_c, time=at_t)
    print(f"favorable example at 10 uM, 2 s: A={p_a:.6f}, B={p_b:.6f}, gap={p_a-p_b:.6f}")
    assert abs(p_a - rk4_bound(**favorable_a, concentration=at_c, time=at_t)) < 1e-9
    assert abs(p_b - rk4_bound(**favorable_b, concentration=at_c, time=at_t)) < 1e-9

    # Finite diagnostic grid only; the proof covers the continuum.
    for c in (0.0, 0.1e-6, 1e-6, 10e-6, 100e-6, 1e-3):
        for t in (0.0, 0.01, 0.1, 0.5, 2.0, 10.0, 100.0):
            assert p_bound(**favorable_a, concentration=c, time=t) + 1e-12 >= p_bound(
                **favorable_b, concentration=c, time=t)

    crossing_a = {"alpha": 1.0, "beta": 1.0, "kon": 2.0, "koff": 10.0}
    crossing_b = {"alpha": 1.0, "beta": 1.0, "kon": 1.0, "koff": 1.0}
    crossing = first_crossing(crossing_a, crossing_b, 1.0, 0.1, 0.3)
    print(f"tradeoff example crossing at {crossing:.12f} s")
    print("A(0.1), B(0.1):",
          f"{p_bound(**crossing_a, concentration=1.0, time=0.1):.8f}",
          f"{p_bound(**crossing_b, concentration=1.0, time=0.1):.8f}")
    print("A(0.3), B(0.3):",
          f"{p_bound(**crossing_a, concentration=1.0, time=0.3):.8f}",
          f"{p_bound(**crossing_b, concentration=1.0, time=0.3):.8f}")


if __name__ == "__main__":
    main()
