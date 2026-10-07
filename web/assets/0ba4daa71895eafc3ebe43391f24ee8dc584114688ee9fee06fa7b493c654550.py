#!/usr/bin/env python3
"""Bounded exploratory scan of N76 F on the two-jump event-chain skeleton."""

from __future__ import annotations

from math import log

from s02_boundary_audit import residual_factorial, transitions


def f_jump_drift(x: tuple[int, int, int]) -> float:
    fx = residual_factorial(x)
    edges = transitions(x)
    total = sum(rate for rate, _ in edges)
    return sum(rate * log(residual_factorial(y) / fx) for rate, y in edges) / total


def f_two_jump_drift(x: tuple[int, int, int]) -> float:
    fx = residual_factorial(x)
    edges = transitions(x)
    total = sum(rate for rate, _ in edges)
    first = sum(rate * log(residual_factorial(y) / fx) for rate, y in edges)
    second = sum(rate * f_jump_drift(y) for rate, y in edges)
    return (first + second) / total


def main() -> None:
    limit = 21
    states = [
        (a, b, c)
        for a in range(limit)
        for b in range(limit)
        for c in range(limit)
        if a + b >= 1
    ]
    one_pos = [(x, f_jump_drift(x)) for x in states if f_jump_drift(x) > 1e-10]
    two_pos = [(x, f_two_jump_drift(x)) for x in states if f_two_jump_drift(x) > 1e-10]
    two_neg = [(x, f_two_jump_drift(x)) for x in states if f_two_jump_drift(x) < -1e-10]
    high_states = [x for x in states if sum(x) >= 15]
    high_pos = [(x, f_two_jump_drift(x)) for x in high_states if f_two_jump_drift(x) > 1e-10]
    print(
        {
            "box": f"0..{limit - 1} each coordinate",
            "states_in_Gamma": len(states),
            "one_jump_positive_count": len(one_pos),
            "one_jump_positive_examples": one_pos[:8],
            "two_jump_positive_count": len(two_pos),
            "two_jump_positive_examples": two_pos[:8],
            "largest_total_count_with_positive_two_jump_drift": max((sum(x) for x, _ in two_pos), default=None),
            "positive_two_jump_states_with_N_at_least_15": len(high_pos),
            "two_jump_negative_count": len(two_neg),
            "two_jump_most_negative": sorted(two_neg, key=lambda item: item[1])[:5],
            "status": "diagnostic only; decimal log signs are not proof",
        }
    )


if __name__ == "__main__":
    main()
