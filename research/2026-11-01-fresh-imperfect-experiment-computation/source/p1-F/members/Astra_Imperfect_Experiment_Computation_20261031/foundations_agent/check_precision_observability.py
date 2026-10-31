"""Reproducible checks for precision_observability.md; not a proof substitute.

No dense n by n matrix is formed. All action costs and errors are explicit.
Run with Python 3 and NumPy. Writes precision_observability_results.json.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def action(v: np.ndarray, u: np.ndarray, a: float) -> np.ndarray:
    return v + a * u * np.dot(u, v)


def inverse_action(v: np.ndarray, u: np.ndarray, a: float) -> np.ndarray:
    return v - (a / (1.0 + a)) * u * np.dot(u, v)


def clipped_oracle(v: np.ndarray, u: np.ndarray, a: float, sigma: float) -> np.ndarray:
    coefficient = a * np.dot(u, v)
    radius = sigma * np.linalg.norm(v)
    return action(v, u, a) - np.clip(coefficient, -radius, radius) * u


def main() -> dict:
    rng = np.random.default_rng(20261031)
    n, a = 4096, 1.0
    u_flat = np.ones(n) / math.sqrt(n)
    sigma_flat = 0.02

    # All n coordinate queries are hidden, exactly in real arithmetic.
    # Checking the scalar coefficient suffices and avoids allocating n^2 data.
    coordinate_signal = a * np.abs(u_flat)
    assert np.max(coordinate_signal) <= sigma_flat
    worst_source_error = float(np.max(coordinate_signal))
    identity_relative_error = float(
        np.linalg.norm(u_flat - inverse_action(u_flat, u_flat, a))
        / np.linalg.norm(inverse_action(u_flat, u_flat, a))
    )
    assert abs(identity_relative_error - a) < 1e-12

    # Randomized probes also disappear at a larger fixed tolerance.
    u_random = rng.normal(size=n)
    u_random /= np.linalg.norm(u_random)
    sigma_random, q = 0.1, 256
    maximum_probe_overlap = 0.0
    maximum_oracle_error = 0.0
    maximum_transcript_deviation = 0.0
    for _ in range(q):
        v = rng.normal(size=n)
        v /= np.linalg.norm(v)
        observed = clipped_oracle(v, u_random, a, sigma_random)
        maximum_probe_overlap = max(maximum_probe_overlap, float(abs(u_random @ v)))
        maximum_oracle_error = max(
            maximum_oracle_error, float(np.linalg.norm(observed - action(v, u_random, a)))
        )
        maximum_transcript_deviation = max(
            maximum_transcript_deviation, float(np.linalg.norm(observed - v))
        )
    assert maximum_oracle_error <= sigma_random + 1e-12
    assert maximum_transcript_deviation < 1e-12

    # Task-first one-action solver, worst-direction load and adverse allowed noise.
    target_epsilon = 0.025
    b = u_random.copy()
    source_error = target_epsilon * b
    y = action(b, u_random, a) + source_error
    recovered = ((2.0 + a) * b - y) / (1.0 + a)
    exact = inverse_action(b, u_random, a)
    task_first_relative_error = float(np.linalg.norm(recovered - exact) / np.linalg.norm(exact))
    assert task_first_relative_error <= target_epsilon + 1e-12

    # Average future tasks versus targeted future task.
    trials, beta = 5000, a / (1.0 + a)
    average_squared_error = 0.0
    average_squared_solution = 0.0
    for _ in range(trials):
        b = rng.normal(size=n)
        b /= np.linalg.norm(b)
        overlap2 = float((u_random @ b) ** 2)
        average_squared_error += beta**2 * overlap2 / trials
        average_squared_solution += (1.0 - (2.0 * beta - beta**2) * overlap2) / trials

    # Bound checks for price versus cap exponent, over a wide precision range.
    price_p = 2.0
    tolerances = np.geomspace(1e-6, 2.0, 10000)
    lhs = np.exp(-n * tolerances**2 / (2.0 * a**2))
    bound = (price_p * a**2 / (math.e * n)) ** (price_p / 2.0) * tolerances ** (-price_p)
    assert np.max(lhs - bound) <= 1e-14

    delta = 1.0 / 3.0
    result = {
        "status": "PASS; numerical checks support stated examples, not novelty or the general proof",
        "seed": 20261031,
        "n": n,
        "a": a,
        "exact_algebra_dimension": 2,
        "matrix_condition_number": 1.0 + a,
        "flat_spike_coordinate_queries": {
            "queries": n,
            "requested_sigma": sigma_flat,
            "largest_allowed_masking_error": worst_source_error,
            "all_coordinate_responses_equal_identity": True,
            "later_b_equals_u_relative_solve_error_using_identity": identity_relative_error,
        },
        "random_probes": {
            "queries": q,
            "requested_sigma": sigma_random,
            "maximum_probe_overlap": maximum_probe_overlap,
            "maximum_actual_source_error": maximum_oracle_error,
            "maximum_difference_from_identity_transcript": maximum_transcript_deviation,
            "theorem_upper_bound_on_breakout_probability": min(
                1.0, 2.0 * q * math.exp(-n * sigma_random**2 / (2.0 * a**2))
            ),
        },
        "task_first_solver": {
            "source_actions": 1,
            "requested_sigma": target_epsilon,
            "relative_solve_error": task_first_relative_error,
            "precision_squared_price": target_epsilon ** (-2),
        },
        "isotropic_future_task_mean": {
            "trials": trials,
            "empirical_squared_error": average_squared_error,
            "theoretical_squared_error": beta**2 / n,
            "empirical_squared_solution_norm": average_squared_solution,
            "theoretical_squared_solution_norm": 1.0 - (2.0 * beta - beta**2) / n,
            "rms_relative_scale": math.sqrt(average_squared_error / average_squared_solution),
        },
        "necessary_precision_squared_price_at_failure_one_third": math.e * n / (12.0 * a**2),
        "limitations": [
            "adversarial actionwise norm-bounded errors; not independent isotropic noise",
            "offline bound requires source-free future solves for all right-hand sides",
            "price sigma^-2 is a declared contract, not an unproved physical sampling law",
            "full-vector input/output arithmetic remains linear in n",
        ],
    }
    output_path = Path(__file__).with_name("precision_observability_results.json")
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
