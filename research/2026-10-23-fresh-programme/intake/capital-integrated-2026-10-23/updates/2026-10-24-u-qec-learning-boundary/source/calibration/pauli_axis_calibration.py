"""Finite-count Pauli-axis learner for the supplied single-Pauli noise class.

This module consumes only nine cumulative +/-1 setting counts and public
channel constants. It has no simulator seed, hidden axis, or exact channel
matrix input.
"""
from __future__ import annotations

import math
from typing import Any

import numpy as np


def checkpoint_alpha(alpha_source: float, checkpoint_index: int) -> float:
    """Summable confidence allocation for checkpoints indexed from one."""
    if not (0.0 < alpha_source < 1.0):
        raise ValueError("alpha_source must lie in (0, 1)")
    if checkpoint_index < 1:
        raise ValueError("checkpoint_index is one-based and must be positive")
    return alpha_source * 6.0 / (math.pi**2 * checkpoint_index**2)


def planned_trials_per_setting(
    *, q: float, max_sin_angle: float, alpha_at_checkpoint: float
) -> int:
    """Sufficient fixed-k design from the known gap lambda=1-q.

    This is a conservative concentration-based planning bound. The observed
    certificate remains based on the sample counts and the empirical top
    eigenvalue.
    """
    if not (0.0 <= q < 1.0):
        raise ValueError("q must lie in [0, 1); q=1 has no identifiable axis")
    if not (0.0 < max_sin_angle < 1.0):
        raise ValueError("max_sin_angle must lie in (0, 1)")
    if not (0.0 < alpha_at_checkpoint < 1.0):
        raise ValueError("alpha_at_checkpoint must lie in (0, 1)")
    gap = 1.0 - q
    factor = (1.0 + max_sin_angle) / (gap * max_sin_angle)
    return math.ceil(18.0 * math.log(18.0 / alpha_at_checkpoint) * factor**2)


def estimate_axis_from_counts(
    plus_counts: np.ndarray,
    minus_counts: np.ndarray,
    *,
    k_per_setting: int,
    q: float,
    tau: float,
    alpha_source: float = 0.02,
    checkpoint_index: int = 1,
    max_source_checkpoints: int | None = None,
    previous_k_per_setting: int = 0,
    max_sin_angle: float | None = None,
) -> dict[str, Any]:
    """Estimate the unoriented noise axis and return its simultaneous bound.

    `plus_counts[i,j]` and `minus_counts[i,j]` are the counts of outcomes
    +/-1 after preparing +sigma_j, waiting tau, and measuring sigma_i.
    Counts are cumulative through this checkpoint. Samples at all nine
    settings must be independent draws from the supplied stationary channel.
    """
    plus = np.asarray(plus_counts)
    minus = np.asarray(minus_counts)
    if plus.shape != (3, 3) or minus.shape != (3, 3):
        raise ValueError("plus_counts and minus_counts must each have shape (3,3)")
    if not np.issubdtype(plus.dtype, np.integer) or not np.issubdtype(minus.dtype, np.integer):
        raise TypeError("count arrays must have integer dtype")
    if np.any(plus < 0) or np.any(minus < 0):
        raise ValueError("counts cannot be negative")
    if k_per_setting < 1 or previous_k_per_setting < 0 or previous_k_per_setting > k_per_setting:
        raise ValueError("invalid cumulative or previous per-setting count")
    if np.any(plus + minus != k_per_setting):
        raise ValueError("each of the nine settings must have exactly k_per_setting outcomes")
    if not (0.0 <= q < 1.0):
        raise ValueError("q must lie in [0, 1); q=1 has no identifiable axis")
    if tau <= 0.0:
        raise ValueError("tau must be positive")
    if max_sin_angle is not None and not (0.0 < max_sin_angle < 1.0):
        raise ValueError("max_sin_angle must lie in (0, 1)")
    if max_source_checkpoints is not None and (
        max_source_checkpoints < checkpoint_index or max_source_checkpoints < 1
    ):
        raise ValueError("max_source_checkpoints must include the current checkpoint")

    alpha_j = checkpoint_alpha(alpha_source, checkpoint_index)
    u = math.sqrt(2.0 * math.log(18.0 / alpha_j) / k_per_setting)
    m_hat = (plus.astype(np.float64) - minus.astype(np.float64)) / k_per_setting
    s_hat = 0.5 * (m_hat + m_hat.T) - q * np.eye(3)
    eigenvalues, eigenvectors = np.linalg.eigh(s_hat)
    top_index = int(np.argmax(eigenvalues))
    lambda_hat = float(eigenvalues[top_index])
    axis_hat = eigenvectors[:, top_index]
    # Fix a deterministic sign convention for serialization; the statistical
    # target remains the projector and is invariant under axis sign.
    first_nonzero = np.flatnonzero(np.abs(axis_hat) > 1e-14)
    if first_nonzero.size and axis_hat[first_nonzero[0]] < 0:
        axis_hat = -axis_hat
    projector_hat = np.outer(axis_hat, axis_hat)

    perturbation_bound = 3.0 * u
    coverage_gate = lambda_hat > perturbation_bound
    if coverage_gate:
        sin_bound = perturbation_bound / lambda_hat
        sin2_bound = sin_bound**2
    else:
        sin_bound = 1.0
        sin2_bound = 1.0
    precision_gate = (
        bool(coverage_gate and sin_bound <= max_sin_angle)
        if max_sin_angle is not None else None
    )
    alpha_sum_observed = sum(
        checkpoint_alpha(alpha_source, j) for j in range(1, checkpoint_index + 1)
    )
    alpha_union_all_allowed = (
        alpha_source if max_source_checkpoints is None else sum(
            checkpoint_alpha(alpha_source, j)
            for j in range(1, max_source_checkpoints + 1)
        )
    )
    new_k = k_per_setting - previous_k_per_setting
    cumulative_shots = 9 * k_per_setting
    new_shots = 9 * new_k
    return {
        "checkpoint_index": int(checkpoint_index),
        "alpha_checkpoint": float(alpha_j),
        "alpha_sum_through_observed_checkpoint_diagnostic_not_stopping_valid": float(alpha_sum_observed),
        "source_alpha_union_bound_all_allowed_checkpoints": float(alpha_union_all_allowed),
        "k_per_setting": int(k_per_setting),
        "previous_k_per_setting": int(previous_k_per_setting),
        "new_k_per_setting": int(new_k),
        "entry_radius_hoeffding": float(u),
        "operator_error_radius": float(perturbation_bound),
        "lambda_hat": lambda_hat,
        "eigenvalues_hat_descending": eigenvalues[::-1].astype(float).tolist(),
        "coverage_gate_open": bool(coverage_gate),
        "sin_angle_bound": float(sin_bound),
        "sin2_angle_bound": float(sin2_bound),
        "requested_max_sin_angle": max_sin_angle,
        "precision_gate_open": precision_gate,
        "axis_hat_sign_convention_only": axis_hat.astype(float).tolist(),
        "axis_projector_hat": projector_hat.astype(float).tolist(),
        "source_cost": {
            "settings": 9,
            "cumulative_preparations": cumulative_shots,
            "cumulative_waits": cumulative_shots,
            "cumulative_wait_time": float(cumulative_shots * tau),
            "cumulative_pauli_readouts": cumulative_shots,
            "new_preparations_this_checkpoint": new_shots,
            "new_waits_this_checkpoint": new_shots,
            "new_wait_time_this_checkpoint": float(new_shots * tau),
            "new_pauli_readouts_this_checkpoint": new_shots,
            "physical_energy_cost": "not assigned; report operation counts and wait time only",
        },
    }
