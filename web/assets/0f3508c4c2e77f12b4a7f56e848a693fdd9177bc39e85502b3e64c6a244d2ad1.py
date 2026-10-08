"""Finite-grid resource/suppression frontier for the cycle-7 model.

This module is an arithmetic helper, not a biological parameter estimator.
All inputs are paid, measured rate bounds from the declared assay panel.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log, sqrt
from typing import Sequence


@dataclass(frozen=True)
class FrontierPoint:
    suppression_rate: float
    weights: tuple[tuple[int, float], ...]
    resource_rate: float


def one_context_frontier(
    resource_upper: Sequence[float],
    suppression_lower: Sequence[float],
    budget_rate: float,
) -> FrontierPoint | None:
    """Maximize the lower suppression rate under an upper resource budget.

    A schedule is a probability vector over tested dose levels. Enumerating
    every pair is sufficient in one context because the feasible set is the
    convex hull of points in R^2 and an upper-frontier point lies on a vertex
    or edge. Indices in the result refer to the caller's dose grid.
    """
    if len(resource_upper) != len(suppression_lower):
        raise ValueError("resource and suppression arrays must have equal length")
    if not resource_upper:
        raise ValueError("at least one measured dose is required")
    if budget_rate < 0:
        raise ValueError("budget_rate must be nonnegative")

    n = len(resource_upper)
    best: FrontierPoint | None = None

    def consider(i: int, wi: float, j: int, wj: float) -> None:
        nonlocal best
        weights = ((i, wi),) if i == j else ((i, wi), (j, wj))
        resource = wi * resource_upper[i] + wj * resource_upper[j]
        suppression = wi * suppression_lower[i] + wj * suppression_lower[j]
        if resource > budget_rate + 1e-12:
            return
        if best is None or suppression > best.suppression_rate + 1e-12:
            best = FrontierPoint(suppression, weights, resource)

    for i in range(n):
        if resource_upper[i] <= budget_rate + 1e-12:
            consider(i, 1.0, i, 0.0)

    for i in range(n):
        for j in range(i + 1, n):
            ri, rj = resource_upper[i], resource_upper[j]
            si, sj = suppression_lower[i], suppression_lower[j]
            dr = ri - rj
            if abs(dr) <= 1e-15:
                if ri <= budget_rate + 1e-12:
                    candidates = (0.0, 1.0)
                else:
                    continue
            elif dr > 0:
                xmax = min(1.0, (budget_rate - rj) / dr)
                if xmax < -1e-12:
                    continue
                candidates = (0.0, max(0.0, xmax))
            else:
                xmin = max(0.0, (budget_rate - rj) / dr)
                if xmin > 1.0 + 1e-12:
                    continue
                candidates = (min(1.0, xmin), 1.0)

            for wi in candidates:
                wi = min(1.0, max(0.0, wi))
                consider(i, wi, j, 1.0 - wi)

    return best


def collapse_context_bounds(
    resource_upper_by_context: Sequence[Sequence[float]],
    suppression_lower_by_context: Sequence[Sequence[float]],
) -> tuple[list[float], list[float]]:
    """Return a conservative per-dose envelope across a finite context panel.

    This loses cross-dose context correlation and can be conservative. Use the
    full per-context linear constraints in PROOF.md for an exact robust LP.
    """
    if not resource_upper_by_context or not suppression_lower_by_context:
        raise ValueError("at least one context is required")
    if len(resource_upper_by_context) != len(suppression_lower_by_context):
        raise ValueError("resource and suppression context counts must match")
    width = len(resource_upper_by_context[0])
    if width == 0:
        raise ValueError("at least one dose is required")
    for row in list(resource_upper_by_context) + list(suppression_lower_by_context):
        if len(row) != width:
            raise ValueError("all context rows must use the same dose grid")

    resource = [max(row[j] for row in resource_upper_by_context) for j in range(width)]
    suppression = [min(row[j] for row in suppression_lower_by_context) for j in range(width)]
    return resource, suppression


def hoeffding_radius(replicates: int, endpoint_count: int, failure_probability: float) -> float:
    """Simultaneous radius for endpoint means in [0, 1]."""
    if replicates <= 0 or endpoint_count <= 0:
        raise ValueError("replicates and endpoint_count must be positive")
    if not 0 < failure_probability < 1:
        raise ValueError("failure_probability must lie in (0, 1)")
    return sqrt(log(2 * endpoint_count / failure_probability) / (2 * replicates))


def replicates_for_radius(endpoint_count: int, failure_probability: float, epsilon: float) -> int:
    """Conservative independent biological-block count for a target radius."""
    if endpoint_count <= 0:
        raise ValueError("endpoint_count must be positive")
    if not 0 < failure_probability < 1 or epsilon <= 0:
        raise ValueError("invalid failure probability or epsilon")
    x = log(2 * endpoint_count / failure_probability) / (2 * epsilon**2)
    return int(x) if x.is_integer() else int(x) + 1


def required_net_suppression_rate(target_fraction: float, horizon_hours: float) -> float:
    """Constant net log-suppression rate needed to reach target_fraction."""
    if not 0 < target_fraction < 1 or horizon_hours <= 0:
        raise ValueError("target_fraction must be in (0,1), horizon must be positive")
    return log(1 / target_fraction) / horizon_hours
