"""Constructive floating-point demonstration of the noisy design certificate.

The optimizer uses an explicit inexact Richardson solver and bounded-error
matrix-vector actions; exact dense solves are used only for independent checks.
This is not interval arithmetic and does not prove a finite-bit implementation.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def main() -> dict:
    rng = np.random.default_rng(20261031)
    n, k = 24, 6
    alpha, spectral_bound = 1.0, 1.01
    target_gap = 0.01
    gradient_budget = target_gap / 16.0
    orthogonal, _ = np.linalg.qr(rng.normal(size=(n, n)))
    matrices = []
    for j in range(k):
        raw = rng.normal(size=(n, n))
        tail = raw @ raw.T
        tail *= 0.005 / np.linalg.norm(tail, 2)
        bj = np.outer(orthogonal[:, j], orthogonal[:, j]) + tail
        matrices.append(bj)
        assert np.linalg.eigvalsh(bj)[0] > 0.0
        assert np.linalg.norm(bj, 2) <= spectral_bound
    matrices = np.asarray(matrices)
    b = np.sum(orthogonal[:, :k], axis=1) / np.sqrt(k)
    b /= np.linalg.norm(b)
    costs = np.array([0.01, -0.015, 0.02, -0.01, 0.005, -0.005])
    tau = min(alpha / 2.0, gradient_budget * alpha**3 / (20.0 * spectral_bound))
    eta = min(gradient_budget * alpha**2 / 8.0, tau / 8.0)
    source_calls = 0
    solve_calls = 0
    max_interval_violation = 0.0
    max_residual_bound_violation = 0.0
    max_gradient_budget_seen = 0.0
    noise_seeds = rng.normal(size=(k, n))

    def source_actions(x: np.ndarray) -> np.ndarray:
        nonlocal source_calls
        xnorm = np.linalg.norm(x)
        answers = []
        for j, bj in enumerate(matrices):
            source_calls += 1
            # Query-dependent deterministic error, with a known norm bound.
            raw_noise = np.sin(noise_seeds[j] + 0.7 * x)
            raw_noise /= np.linalg.norm(raw_noise)
            answers.append(bj @ x + eta * xnorm * raw_noise)
        return np.asarray(answers)

    def audited_richardson(theta: np.ndarray, warm_start: np.ndarray):
        nonlocal solve_calls, max_residual_bound_violation
        solve_calls += 1
        x = warm_start.copy()
        step = 1.0 / (alpha + spectral_bound)
        for iteration in range(10000):
            actions = source_actions(x)
            observed_ax = alpha * x + np.einsum("k,kn->n", theta, actions)
            observed_residual = b - observed_ax
            rho = np.linalg.norm(observed_residual) + eta * np.linalg.norm(x)
            # True residual is checked here, but never used for decisions.
            actual_a = alpha * np.eye(n) + np.einsum("k,knm->nm", theta, matrices)
            actual_residual = np.linalg.norm(b - actual_a @ x)
            max_residual_bound_violation = max(max_residual_bound_violation, actual_residual - rho)
            if rho <= tau * np.linalg.norm(x):
                return x, rho, actions, iteration + 1
            x += step * observed_residual
        raise RuntimeError("Richardson solver exceeded the explicit safety cap")

    theta = np.zeros(k)
    theta[0] = 1.0
    x = np.zeros(n)
    curvature = 2.0 * spectral_bound**2 * np.linalg.norm(b) ** 2 / alpha**3
    max_iterations = 2 * max(1, int(np.ceil(8.0 * curvature / target_gap)))
    trace = []
    initial_value = None

    for t in range(max_iterations):
        x, rho, actions, solve_iterations = audited_richardson(theta, x)
        xnorm = np.linalg.norm(x)
        error_norm = rho / alpha
        gradient_radius = eta * xnorm**2 + spectral_bound * error_norm * (2.0 * xnorm + error_norm)
        max_gradient_budget_seen = max(max_gradient_budget_seen, gradient_radius)
        assert gradient_radius <= gradient_budget * (1.0 + 1e-10)
        approximate_gradient = costs - np.einsum("n,kn->k", x, actions)
        upper_gap = float(theta @ approximate_gradient - np.min(approximate_gradient) + 2.0 * gradient_radius)

        # Independent exact references, not used by the optimizer.
        actual_a = alpha * np.eye(n) + np.einsum("k,knm->nm", theta, matrices)
        exact_x = np.linalg.solve(actual_a, b)
        exact_gradient = costs - np.einsum("n,knm,m->k", exact_x, matrices, exact_x)
        exact_gap = float(theta @ exact_gradient - np.min(exact_gradient))
        objective = float(costs @ theta + b @ exact_x)
        if initial_value is None:
            initial_value = objective
        max_interval_violation = max(
            max_interval_violation,
            float(np.max(np.abs(approximate_gradient - exact_gradient)) - gradient_radius),
        )
        assert exact_gap <= upper_gap + 1e-12
        trace.append({
            "iteration": t,
            "objective_reference_only": objective,
            "computed_global_gap_upper_bound": upper_gap,
            "actual_frank_wolfe_gap_reference_only": exact_gap,
            "gradient_interval_radius": float(gradient_radius),
            "solver_source_rounds": solve_iterations,
        })
        if upper_gap <= target_gap:
            break
        chosen_vertex = int(np.argmin(approximate_gradient))
        gamma = 2.0 / (t + 2.0)
        theta *= 1.0 - gamma
        theta[chosen_vertex] += gamma
    else:
        raise AssertionError("The proven finite iteration cap was exceeded")

    assert max_interval_violation < 1e-12
    assert max_residual_bound_violation < 1e-12
    result = {
        "status": "PASS; floating-point construction and independent checks, not interval-arithmetic certification",
        "seed": 20261031,
        "dimension": n,
        "operators": k,
        "alpha": alpha,
        "admitted_spectral_bound": spectral_bound,
        "target_design_gap": target_gap,
        "source_action_tolerance": eta,
        "relative_residual_target": tau,
        "design_iterations": len(trace),
        "proven_iteration_cap": max_iterations,
        "audited_linear_solves": solve_calls,
        "total_source_actions_including_unsuccessful_iterations": source_calls,
        "initial_objective_reference_only": initial_value,
        "final_objective_reference_only": trace[-1]["objective_reference_only"],
        "final_computed_global_gap_upper_bound": trace[-1]["computed_global_gap_upper_bound"],
        "final_actual_frank_wolfe_gap_reference_only": trace[-1]["actual_frank_wolfe_gap_reference_only"],
        "maximum_gradient_interval_violation": max_interval_violation,
        "maximum_residual_bound_violation": max_residual_bound_violation,
        "maximum_gradient_radius": max_gradient_budget_seen,
        "theta": theta.tolist(),
        "trace": trace,
        "limitations": [
            "the baseline audited Richardson solver does not exploit the root's reusable cache",
            "dense exact solves appear only in independent reference checks",
            "the code uses ordinary floating point, not certified outward interval arithmetic",
            "source errors are controlled synthetic errors, not a physical noise model",
        ],
    }
    output = Path(__file__).with_name("convex_design_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    return {key: value for key, value in result.items() if key != "trace"}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
