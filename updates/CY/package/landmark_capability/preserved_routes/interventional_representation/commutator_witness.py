#!/usr/bin/env python3
"""Exact toy demonstration of a black-box controlled-commutator witness.

The hidden state is (q,z), the sensor sees only z, and neither primitive
action changes z from the chosen initial state. The four-action loop exposes
their mixed coupling while returning q to its initial value.
"""

from __future__ import annotations

from collections.abc import Callable
from math import isclose

State = tuple[float, float]


def F(state: State, a: float) -> State:
    q, z = state
    return q + a, z


def G(state: State, b: float) -> State:
    q, z = state
    return q, z + b * q


def commutator(state: State, a: float, b: float,
                f: Callable[[State, float], State] = F,
                g: Callable[[State, float], State] = G) -> State:
    """Chronological loop: G_b, F_a, G_-b, F_-a."""
    state = g(state, b)
    state = f(state, a)
    state = g(state, -b)
    state = f(state, -a)
    return state


def cross_estimate(a: float, b: float) -> float:
    y_pp = commutator((0.0, 0.0), a, b)[1]
    y_pm = commutator((0.0, 0.0), a, -b)[1]
    y_mp = commutator((0.0, 0.0), -a, b)[1]
    y_mm = commutator((0.0, 0.0), -a, -b)[1]
    return (y_pp - y_pm - y_mp + y_mm) / (4.0 * a * b)


def uncoupled_with_drift(state: State, action: str, amount: float,
                         drift: float) -> State:
    """Commuting actions with an unmodeled per-call sensor drift."""
    q, z = state
    if action == "F":
        q += amount
    elif action == "G":
        z += amount
    else:
        raise ValueError(action)
    return q, z + drift


def main() -> None:
    start = (0.0, 0.0)
    a, b = 0.2, 0.3
    y_after_f = F(start, a)[1]
    y_after_g = G(start, b)[1]
    endpoint = commutator(start, a, b)

    q, z = start
    loops = 7
    for _ in range(loops):
        q, z = commutator((q, z), a, b)

    # First failure: the commutator moves hidden z, but sensor h(q,z,w)=w
    # is blind to that direction. Here the third coordinate is unchanged.
    invisible_endpoint = (endpoint[0], endpoint[1], 0.0)
    invisible_sensor_delta = invisible_endpoint[2] - 0.0

    # Second failure: perfectly commuting action maps plus a tiny per-call
    # unmodeled sensor drift produce a false residual in the 4-pulse loop.
    eta = 1e-4
    state = start
    for action, amount in (("G", b), ("F", a), ("G", -b), ("F", -a)):
        state = uncoupled_with_drift(state, action, amount, eta)

    print("controlled-commutator witness (exact hidden shear fixture)")
    print(f"single-action readout deltas at start: F={y_after_f:g}, G={y_after_g:g}")
    print(f"one four-pulse endpoint: q={endpoint[0]:g}, z={endpoint[1]:g}")
    print(f"four-sign cross estimate: {cross_estimate(a, b):g} (true projected coefficient -1)")
    print(f"{loops} repeated loops: q={q:g}, z={z:g}, expected z={-loops*a*b:g}")
    print(f"hidden bracket motion with blind sensor: measured delta={invisible_sensor_delta:g}")
    print(f"uncoupled actions plus per-call drift eta={eta:g}: false loop residual={state[1]:g}")

    assert y_after_f == 0.0 and y_after_g == 0.0
    assert endpoint == (0.0, -a * b)
    assert cross_estimate(a, b) == -1.0
    assert q == 0.0 and isclose(z, -loops * a * b, rel_tol=0.0, abs_tol=1e-14)
    assert invisible_sensor_delta == 0.0
    assert abs(state[1] - 4.0 * eta) < 1e-15


if __name__ == "__main__":
    main()
