#!/usr/bin/env python3
"""Exact finite audit of a hidden-channel rare-event computation contract.

This is an arithmetic check and transparent comparator, not molecular data.
All counts charge calls to the classical local transition oracle.
"""

from fractions import Fraction
from itertools import combinations
import json
import math


def rate(candidate_count: int, barrier_levels: int, gateway_count: int) -> Fraction:
    return Fraction(gateway_count, (candidate_count + 1) * (1 << barrier_levels))


def relative_importance_variance(candidate_count: int, epsilon: Fraction) -> Fraction:
    """Variance/mean^2 with a known gateway plus one hidden gateway.

    Proposal branch probabilities are proportional to (1, epsilon, ..., epsilon).
    The barrier factor is assumed removed perfectly, favouring the proposal.
    """
    n = candidate_count
    assert epsilon > 0
    proposal_base = Fraction(1, 1) / (1 + n * epsilon)
    proposal_other = epsilon / (1 + n * epsilon)
    probability = Fraction(2, n + 1)
    second_moment = (
        Fraction(1, proposal_base) + Fraction(1, proposal_other)
    ) / (n + 1) ** 2
    closed_form = (1 + n * epsilon) * (1 + 1 / epsilon) / 4 - 1
    answer = second_moment / probability**2 - 1
    assert answer == closed_form
    return answer


def exhaustive_coverage_audit() -> int:
    cases = 0
    for n in range(2, 9):
        for q in range(n + 1):
            for selected in combinations(range(1, n + 1), q):
                discoveries = sum(j in selected for j in range(1, n + 1))
                assert Fraction(discoveries, n) == Fraction(q, n)
                cases += 1
    return cases


def direct_draws_for_two_thirds(delta: Fraction) -> int:
    """Minimum iid forward trajectories to hit the extra channel with probability 2/3."""
    target = math.log(1 / 3) / math.log1p(-float(delta))
    count = math.ceil(target)
    # Float logarithms choose a nearby integer; verify the threshold exactly.
    while (1 - delta) ** count > Fraction(1, 3):
        count += 1
    while count > 0 and (1 - delta) ** (count - 1) <= Fraction(1, 3):
        count -= 1
    return count


def main() -> None:
    levels = 8
    rows = []
    for n in (64, 256, 1024):
        root = math.isqrt(n)
        assert root * root == n
        p0 = rate(n, levels, 1)
        p1 = rate(n, levels, 2)
        delta = p1 - p0
        epsilon_opt = Fraction(1, root)
        direct_draws = direct_draws_for_two_thirds(delta)
        # One start transition, a truncated geometric number of barrier moves,
        # and a terminal move only when every barrier stage is crossed.
        expected_steps_per_forward_path = Fraction(3) - Fraction(1, 1 << levels)
        expected_unknown_terminal_calls_per_forward_path = Fraction(
            n, (n + 1) * (1 << levels)
        )
        rows.append(
            {
                "candidate_count": n,
                "barrier_levels": levels,
                "p0_exact": str(p0),
                "p1_exact": str(p1),
                "p0_decimal": float(p0),
                "p1_decimal": float(p1),
                "all_terminal_queries_for_exact_answer": n,
                "random_stopping_min_expected_terminal_queries_under_H0": f"{n}/3",
                "fixed_query_min_terminal_queries_for_two_thirds": n // 2,
                "direct_forward_trajectories_for_two_thirds_extra_channel_detection": direct_draws,
                "direct_expected_all_transition_evaluations_at_fixed_trial_count": float(
                    direct_draws * expected_steps_per_forward_path
                ),
                "direct_expected_unknown_terminal_queries_at_fixed_trial_count": float(
                    direct_draws * expected_unknown_terminal_calls_per_forward_path
                ),
                "relative_variance_uniform_branch_proposal": str(relative_importance_variance(n, Fraction(1))),
                "relative_variance_best_symmetric_branch_proposal": str(relative_importance_variance(n, epsilon_opt)),
                "best_symmetric_epsilon": str(epsilon_opt),
            }
        )
    print(json.dumps({"exhaustive_coverage_cases": exhaustive_coverage_audit(), "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
