#!/usr/bin/env python3
"""Exact rational min-knapsack threshold for edge-disjoint parallel corridors."""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import lcm


def lcm_many(values: list[int]) -> int:
    out = 1
    for x in values:
        out = lcm(out, x)
    return out


def exact_budget(g: list[Fraction], c: list[Fraction], target: Fraction) -> dict:
    if len(g) != len(c) or not g:
        raise ValueError("conductance and cost lists must be equal-length and nonempty")
    total = sum(g, Fraction(0))
    if not (0 < target <= total) or any(x <= 0 for x in g + c):
        raise ValueError("require positive conductances/costs and 0 < target <= total")

    deficit = total - target
    scale_g = lcm_many([x.denominator for x in g] + [deficit.denominator])
    weights = [int(scale_g * x) for x in g]
    strict_threshold = int(scale_g * deficit) + 1  # all inputs are rational

    scale_c = lcm_many([x.denominator for x in c])
    costs = [int(scale_c * x) for x in c]

    # dp[x] is the least cost to delete routes with total lost conductance >= x.
    inf = sum(costs) + 1
    dp = [0] + [inf] * strict_threshold
    for w, v in zip(weights, costs):
        for x in range(strict_threshold, -1, -1):
            if dp[x] < inf:
                y = min(strict_threshold, x + w)
                dp[y] = min(dp[y], dp[x] + v)

    dynamic_answer = Fraction(dp[strict_threshold], scale_c)
    qualifying = []
    for r in range(len(g) + 1):
        for ids in combinations(range(len(g)), r):
            lost = sum((g[i] for i in ids), Fraction(0))
            cost = sum((c[i] for i in ids), Fraction(0))
            if lost > deficit:
                qualifying.append((cost, ids, lost))
    brute_answer, ids, lost = min(qualifying)
    assert dynamic_answer == brute_answer
    remaining = total - lost
    assert remaining < target

    return {
        "conductances": [str(x) for x in g],
        "occlusion_costs": [str(x) for x in c],
        "target": str(target),
        "intact_total": str(total),
        "strict_lost_conductance_threshold": str(deficit),
        "exact_minimum_occlusion_cost": str(dynamic_answer),
        "minimizing_destroyed_corridors_zero_indexed": list(ids),
        "lost_conductance": str(lost),
        "post_damage_conductance": str(remaining),
        "algorithm": "exact 0/1 dynamic program after clearing rational denominators",
        "cost": f"O(m W) time, O(W) memory, W=floor(L_g*(G0-G*))+1; pseudo-polynomial, not polynomial in input bit length",
        "independent_bruteforce_agreement": True,
        "scope": "exact parallel edge-disjoint corridor model only; not material validation",
    }


if __name__ == "__main__":
    from json import dumps
    from pathlib import Path

    result = exact_budget(
        [Fraction(3, 5), Fraction(3, 5), Fraction(3, 5)],
        [Fraction(1), Fraction(1), Fraction(100)],
        Fraction(7, 10),
    )
    serialized = dumps(result, indent=2) + "\n"
    Path(__file__).with_name("parallel_path_budget_output.json").write_text(serialized)
    print(serialized, end="")
