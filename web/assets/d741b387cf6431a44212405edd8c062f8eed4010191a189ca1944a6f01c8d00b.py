"""Robust finite-state nutrient-program compiler.

Arithmetic only: each row's fixed charged upper nutrient cost and its set of
possible next-state/lower-suppression outcomes must be measured from the
declared construct/context interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import inf
from typing import Hashable, Mapping, Sequence

State = Hashable
Action = Hashable
Budget = tuple[float, ...]
Outcome = tuple[State, Budget, float]


def _row_cost(outcomes: Sequence[Outcome], budget_dimensions: int) -> Budget:
    costs = {cost for _, cost, _ in outcomes}
    if len(costs) != 1:
        raise ValueError("charge one known upper cost vector per state/action row")
    cost = next(iter(costs))
    if len(cost) != budget_dimensions:
        raise ValueError("each cost vector must match the budget dimension")
    return cost


@dataclass(frozen=True)
class DynamicPlan:
    suppression_lower: float
    policy: tuple[tuple[int, State, Budget, Action], ...]


def robust_open_loop_value(
    initial_state: State,
    action_sequence: Sequence[Action],
    outcomes: Mapping[tuple[int, State, Action], Sequence[Outcome]],
    budget: Budget,
) -> float:
    """Evaluate a fixed action sequence against all possible row outcomes."""
    if not budget:
        raise ValueError("at least one resource budget is required")
    if any(b < 0 for b in budget):
        raise ValueError("budgets must be nonnegative")

    def visit(t: int, x: State, remaining: Budget) -> float:
        if t == len(action_sequence):
            return 0.0
        a = action_sequence[t]
        key = (t, x, a)
        if key not in outcomes or not outcomes[key]:
            raise ValueError(f"missing nonempty joint outcome set for {key!r}")
        c = _row_cost(outcomes[key], len(budget))
        if any(ci > bi + 1e-12 for ci, bi in zip(c, remaining)):
            return -inf
        return min(
            r + visit(t + 1, x2, tuple(max(0.0, bi - ci) for bi, ci in zip(remaining, c)))
            for x2, _, r in outcomes[key]
        )

    return visit(0, initial_state, budget)


def robust_state_feedback_plan(
    initial_state: State,
    actions_by_stage: Sequence[Sequence[Action]],
    outcomes: Mapping[tuple[int, State, Action], Sequence[Outcome]],
    budget: Budget,
) -> DynamicPlan | None:
    """Choose actions from the observed state bin to maximize worst-case sum.

    This policy is implementable only when the state bin is observable at each
    decision. Destructive assays on sister aliquots do not qualify as live,
    per-cell feedback; use robust_open_loop_value for open-loop schedules.
    """
    if not budget:
        raise ValueError("at least one resource budget is required")
    if any(b < 0 for b in budget):
        raise ValueError("budgets must be nonnegative")

    @lru_cache(maxsize=None)
    def value(t: int, x: State, remaining: Budget) -> float:
        if t == len(actions_by_stage):
            return 0.0
        best = -inf
        for action in actions_by_stage[t]:
            key = (t, x, action)
            if key not in outcomes or not outcomes[key]:
                continue
            c = _row_cost(outcomes[key], len(budget))
            if any(ci > bi + 1e-12 for ci, bi in zip(c, remaining)):
                continue
            candidate = min(
                r + value(t + 1, x2, tuple(max(0.0, bi - ci) for bi, ci in zip(remaining, c)))
                for x2, _, r in outcomes[key]
            )
            best = max(best, candidate)
        return best

    optimum = value(0, initial_state, budget)
    if optimum == -inf:
        return None

    policy: dict[tuple[int, State, Budget], Action] = {}

    def recover(t: int, x: State, remaining: Budget) -> None:
        if t == len(actions_by_stage):
            return
        target_value = value(t, x, remaining)
        for action in actions_by_stage[t]:
            key = (t, x, action)
            if key not in outcomes or not outcomes[key]:
                continue
            c = _row_cost(outcomes[key], len(budget))
            if any(ci > bi + 1e-12 for ci, bi in zip(c, remaining)):
                continue
            candidate = min(
                r + value(t + 1, x2, tuple(max(0.0, bi - ci) for bi, ci in zip(remaining, c)))
                for x2, _, r in outcomes[key]
            )
            if abs(candidate - target_value) <= 1e-12:
                policy[(t, x, remaining)] = action
                for x2, _, _ in outcomes[key]:
                    recover(t + 1, x2, tuple(max(0.0, bi - ci) for bi, ci in zip(remaining, c)))
                return
        raise RuntimeError("could not recover an optimal policy")

    recover(0, initial_state, budget)
    entries = tuple((t, x, remaining, a) for (t, x, remaining), a in sorted(
        policy.items(), key=lambda item: (item[0][0], repr(item[0][1]), item[0][2])
    ))
    return DynamicPlan(optimum, entries)


def required_log_suppression(target_fraction: float) -> float:
    """Log reduction required to reach a target fraction in (0, 1)."""
    from math import log

    if not 0 < target_fraction < 1:
        raise ValueError("target_fraction must lie in (0, 1)")
    return log(1.0 / target_fraction)
