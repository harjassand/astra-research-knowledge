#!/usr/bin/env python3
"""Executable checks/design bounds for one-lag phenotype/growth inference.

Uses NumPy only. The observed endpoint matrix is reconstructed columnwise as
M[:, i] = (N_i(tau)/N_i(0)) * p_i(tau). Independent experimental units are
replicate wells/inoculations, never descendant cells within one well.
"""

from __future__ import annotations

import json
import math
from typing import Iterable, Sequence

import numpy as np


def expm(A: np.ndarray) -> np.ndarray:
    """Scaling-and-squaring Taylor exponential for the small audit matrices."""
    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    norm1 = float(np.linalg.norm(A, 1))
    squarings = max(0, int(math.ceil(math.log2(norm1 / 0.5)))) if norm1 > 0.5 else 0
    X = A / (2**squarings)
    term = np.eye(n)
    total = term.copy()
    for k in range(1, 300):
        term = term @ X / k
        total += term
        if np.linalg.norm(term, 1) <= 2e-16 * max(1.0, np.linalg.norm(total, 1)):
            break
    else:
        raise ArithmeticError("Taylor exponential did not converge")
    for _ in range(squarings):
        total = total @ total
    return total


def log_near_identity(M: np.ndarray, tol: float = 2e-16) -> np.ndarray:
    """Power-series log, valid when ||M-I||_1 < 1."""
    M = np.asarray(M, dtype=float)
    X = M - np.eye(M.shape[0])
    if np.linalg.norm(X, 1) >= 1:
        raise ValueError("log series requires ||M-I||_1 < 1")
    total = np.zeros_like(M)
    power = X.copy()
    for k in range(1, 10000):
        term = power / k
        total += term if k % 2 else -term
        if np.linalg.norm(term, 1) <= tol * max(1.0, np.linalg.norm(total, 1)):
            break
        power = power @ X
    else:
        raise ArithmeticError("Taylor logarithm did not converge")
    return total


def cycle_generator(u: float, v: float) -> np.ndarray:
    """Three-state clockwise/counterclockwise generator; columns are sources."""
    Q = np.zeros((3, 3), dtype=float)
    for i in range(3):
        Q[(i + 1) % 3, i] = u
        Q[(i - 1) % 3, i] = v
        Q[i, i] = -(u + v)
    return Q


def generator_from_edges(K: int, edges: Iterable[tuple[int, int, float]]) -> np.ndarray:
    """Construct column-generator Q from (source, destination, rate) edges."""
    Q = np.zeros((K, K), dtype=float)
    for source, dest, rate in edges:
        if source == dest or rate < 0:
            raise ValueError("edges must be off-diagonal with nonnegative rate")
        Q[dest, source] += rate
        Q[source, source] -= rate
    return Q


def rate_bias_certificate(B: float, tau: float) -> dict[str, float]:
    """First-order endpoint estimator bias under ||A||_1 <= B."""
    remainder = math.expm1(B * tau) - B * tau
    return {
        "B_tau": B * tau,
        "matrix_remainder_bound": remainder,
        "coordinate_rate_bias_bound": remainder / tau,
        "small_tau_leading_bound": 0.5 * B * B * tau,
    }


def hoeffding_plan(
    K: int,
    tau: float,
    B: float,
    rate_error: float,
    delta: float,
    coordinate_bound: float,
    actions: int = 1,
    culture_cost: float = 0.0,
    pure_start_cost: float = 0.0,
    fraction_panel_cost: float = 0.0,
    absolute_count_cost: float = 0.0,
    calibration_cost: float = 0.0,
) -> dict[str, float | int | str]:
    """Plan independent replicate wells for a sup-norm q error guarantee.

    Assumption: each normalized count coordinate Y=N_j(tau)/N(0) is an
    independent, unbiased observation in [0, coordinate_bound]. If an assay
    clips counts, its clipping bias must be added separately.
    """
    rem = math.expm1(B * tau) - B * tau
    allowed_mean_error = tau * rate_error - rem
    if allowed_mean_error <= 0:
        return {
            "status": "INFEASIBLE_AT_TAU",
            "reason": "finite-tau truncation already exceeds target rate error",
            "remainder_rate_bound": rem / tau,
        }
    log_factor = math.log(2 * actions * K * K / delta)
    n = math.ceil(coordinate_bound**2 * log_factor / (2 * allowed_mean_error**2))
    units = actions * K * n
    per_well = culture_cost + pure_start_cost + fraction_panel_cost + absolute_count_cost
    return {
        "status": "OK",
        "replicate_wells_per_action_per_pure_start": n,
        "number_of_actions": actions,
        "number_of_pure_starts": K,
        "total_independent_wells": units,
        "max_coordinate_mean_error": allowed_mean_error,
        "finite_tau_rate_bias_bound": rem / tau,
        "total_cost": units * per_well + calibration_cost,
        "cost_accounting": (
            "K pure starts x n independent wells x actions; each well charged for "
            "culture, pure-start sorting/verification, all-state fraction panel, "
            "and absolute count; calibration charged once"
        ),
    }


def choose_tau_on_grid(
    candidate_times: Sequence[float],
    **plan_kwargs: object,
) -> dict[str, object]:
    """Choose the least-cost admissible single read time on a supplied grid."""
    feasible: list[tuple[float, dict[str, object]]] = []
    failures = 0
    for tau in candidate_times:
        plan = hoeffding_plan(tau=float(tau), **plan_kwargs)  # type: ignore[arg-type]
        if plan["status"] == "OK":
            feasible.append((float(tau), plan))
        else:
            failures += 1
    if not feasible:
        return {"status": "UNKNOWN", "reason": "no candidate time meets the bias budget"}
    tau, plan = min(feasible, key=lambda item: float(item[1]["total_cost"]))
    return {
        "status": "OK",
        "selected_tau": tau,
        "grid_size": len(candidate_times),
        "infeasible_grid_points": failures,
        "plan": plan,
    }


def absorbing_generator(Q: np.ndarray, target: Sequence[int], unsafe: Sequence[int]) -> np.ndarray:
    """Make target and unsafe states absorbing for a first-hit reach-avoid event."""
    Qa = np.asarray(Q, dtype=float).copy()
    for state in set(target) | set(unsafe):
        Qa[:, state] = 0.0
    return Qa


def reach_avoid_value(
    Q: np.ndarray,
    target: Sequence[int],
    unsafe: Sequence[int],
    initial: Sequence[float],
    horizon: float,
) -> float:
    Qa = absorbing_generator(Q, target, unsafe)
    mass = expm(Qa * horizon) @ np.asarray(initial, dtype=float)
    return float(np.sum(mass[list(target)]))


def robust_reach_avoid(
    action_generators: dict[str, np.ndarray],
    coordinate_radius: float,
    target: Sequence[int],
    unsafe: Sequence[int],
    initial: Sequence[float],
    horizon: float,
) -> dict[str, object]:
    """Certified box-confidence bounds and a finite-action maximin choice.

    Every off-diagonal rate in an action's confidence set lies within
    coordinate_radius of its center and is nonnegative. Duhamel's formula and
    Markov-semigroup contraction give |V(Q)-V(Qhat)| <=
    horizon * 2(K-1) * coordinate_radius.
    """
    K = next(iter(action_generators.values())).shape[0]
    radius = min(1.0, horizon * 2 * (K - 1) * coordinate_radius)
    intervals: dict[str, dict[str, float]] = {}
    for name, Q in action_generators.items():
        center = reach_avoid_value(Q, target, unsafe, initial, horizon)
        intervals[name] = {
            "center": center,
            "lower": max(0.0, center - radius),
            "upper": min(1.0, center + radius),
        }
    choice = max(intervals, key=lambda name: intervals[name]["lower"])
    unique = all(
        intervals[choice]["lower"] > intervals[name]["upper"]
        for name in intervals
        if name != choice
    )
    return {
        "action_intervals": intervals,
        "maximin_action": choice,
        "robustly_unique_best": unique,
        "reach_target_threshold_0_5_certified": intervals[choice]["lower"] >= 0.5,
        "lipschitz_radius": radius,
    }


def main() -> None:
    tau = 1.0
    s = 10.0
    d0 = 0.0
    d1 = d0 + 4 * math.pi / (math.sqrt(3) * tau)
    u0, v0 = (s + d0) / 2, (s - d0) / 2
    u1, v1 = (s + d1) / 2, (s - d1) / 2
    Q0, Q1 = cycle_generator(u0, v0), cycle_generator(u1, v1)
    M0, M1 = expm(Q0 * tau), expm(Q1 * tau)

    # Missing-pure-start counterexample: state 2 is unreachable from starts 0,1.
    Qa = generator_from_edges(3, [(0, 1, 0.3), (1, 0, 0.2), (2, 0, 0.7)])
    Qb = generator_from_edges(3, [(0, 1, 0.3), (1, 0, 0.2), (2, 0, 4.7)])
    Ma, Mb = expm(Qa * 0.6), expm(Qb * 0.6)

    # Short-time first-order estimator and its deterministic remainder bound.
    tau_short = 0.01
    Mshort = expm(Q0 * tau_short)
    qhat = (Mshort - np.eye(3)) / tau_short
    B = float(np.linalg.norm(Q0, 1))
    bias = rate_bias_certificate(B, tau_short)
    offdiag_error = max(
        abs(qhat[j, i] - Q0[j, i]) for i in range(3) for j in range(3) if i != j
    )

    # Principal-log reconstruction in the near-identity regime.
    A = Q0 + np.diag([0.2, -0.1, 0.05])
    tau_log = 0.01
    Mlog = expm(A * tau_log)
    Ahat = log_near_identity(Mlog) / tau_log

    # Finite action robust reach-avoid illustration: state 2 is target, 1 unsafe.
    action_Q = {
        "A": generator_from_edges(3, [(0, 1, 0.10), (0, 2, 0.50)]),
        "B": generator_from_edges(3, [(0, 1, 0.40), (0, 2, 0.90)]),
    }
    robust = robust_reach_avoid(
        action_Q,
        coordinate_radius=0.04,
        target=[2],
        unsafe=[1],
        initial=[1.0, 0.0, 0.0],
        horizon=1.0,
    )

    plan = choose_tau_on_grid(
        candidate_times=np.linspace(0.005, 0.2, 100),
        K=3,
        B=2.0,
        rate_error=0.4,
        delta=0.05,
        coordinate_bound=1.5,
        actions=2,
        culture_cost=2.0,
        pure_start_cost=0.5,
        fraction_panel_cost=1.0,
        absolute_count_cost=0.5,
        calibration_cost=5.0,
    )

    result = {
        "three_state_alias": {
            "tau": tau,
            "rates_1_clockwise_counterclockwise": [u0, v0],
            "rates_2_clockwise_counterclockwise": [u1, v1],
            "all_rates_positive": bool(min(u0, v0, u1, v1) > 0),
            "max_abs_endpoint_matrix_difference": float(np.max(np.abs(M0 - M1))),
            "max_abs_generator_difference": float(np.max(np.abs(Q0 - Q1))),
        },
        "two_pure_starts_not_sufficient_without_reachability": {
            "tau": 0.6,
            "max_abs_observed_column_difference_starts_0_1": float(
                np.max(np.abs(Ma[:, :2] - Mb[:, :2]))
            ),
            "unobserved_source_2_outgoing_rate_change": 4.0,
        },
        "finite_tau_first_order": {
            "tau": tau_short,
            "B": B,
            "actual_max_offdiag_rate_error": offdiag_error,
            **bias,
            "bound_holds": bool(offdiag_error <= bias["coordinate_rate_bias_bound"] + 1e-12),
        },
        "near_identity_log": {
            "tau": tau_log,
            "B": float(np.linalg.norm(A, 1)),
            "B_tau_less_log_2": bool(np.linalg.norm(A, 1) * tau_log < math.log(2)),
            "max_abs_A_reconstruction_error": float(np.max(np.abs(Ahat - A))),
        },
        "finite_action_robust_reach_avoid": robust,
        "sampling_and_cost_plan": plan,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
