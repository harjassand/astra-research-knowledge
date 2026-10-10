#!/usr/bin/env python3
"""Finite two-mode fixture for intervention-assisted dark-mode spectroscopy.

The unperturbed bright-port impulse response is independent of the hidden
mode rate. A known off-diagonal gate couples the bright and dark modes, making
the hidden rate visible in the same scalar readout. This is an exact 2x2
linear calculation evaluated on a finite time grid; it is not physical data.
"""

from __future__ import annotations

import json
import math

import numpy as np


def impulse_response(lam: float, delta: float, times: np.ndarray) -> np.ndarray:
    """Return e_1^T exp(M t) e_1 for M=[[-1, delta],[delta, lam]]."""
    matrix = np.array([[-1.0, delta], [delta, lam]], dtype=float)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    weights = eigenvectors[0, :] ** 2
    return sum(weights[j] * np.exp(eigenvalues[j] * times) for j in range(2))


def max_gap(lam_a: float, lam_b: float, delta: float,
            times: np.ndarray) -> tuple[float, float, float, float]:
    ya = impulse_response(lam_a, delta, times)
    yb = impulse_response(lam_b, delta, times)
    k = int(np.argmax(np.abs(ya - yb)))
    return float(abs(ya[k] - yb[k])), float(times[k]), float(ya[k]), float(yb[k])


def main() -> None:
    lam_a, lam_b = -0.10, -0.35
    times = np.linspace(0.0, 12.0, 2401)
    baseline_a = impulse_response(lam_a, 0.0, times)
    baseline_b = impulse_response(lam_b, 0.0, times)
    baseline_gap = float(np.max(np.abs(baseline_a - baseline_b)))

    sigma = 0.005
    gate_sweep = []
    for delta in (0.06, 0.12, 0.24):
        gap, t_star, ya, yb = max_gap(lam_a, lam_b, delta, times)
        # Nearest-hypothesis classification from R iid endpoint readings at
        # t_star has error Phi(-gap*sqrt(R)/(2*sigma)).  Ten sigma separation
        # gives a one-sided Gaussian error near 2.9e-7.
        repeats_5sigma = int(math.ceil((10.0 * sigma / gap) ** 2))
        poles_a = np.linalg.eigvalsh(np.array([[-1.0, delta], [delta, lam_a]]))
        poles_b = np.linalg.eigvalsh(np.array([[-1.0, delta], [delta, lam_b]]))
        gate_sweep.append({
            "delta": delta,
            "max_between_hypothesis_gap": gap,
            "time_of_max_gap": t_star,
            "mean_lambda_minus_0_10": ya,
            "mean_lambda_minus_0_35": yb,
            "rho_recovered_from_pole_sum_lambda_minus_0_10": float(-1.0 - np.sum(poles_a)),
            "rho_recovered_from_pole_sum_lambda_minus_0_35": float(-1.0 - np.sum(poles_b)),
            "readout_sd": sigma,
            "repeats_for_5sigma_nearest_hypothesis": repeats_5sigma,
            "endpoint_reads": repeats_5sigma,
            "nonzero_gate_trials": repeats_5sigma,
            "input_impulses": repeats_5sigma,
            "resets": repeats_5sigma,
        })

    delta = 0.12
    y_plus = impulse_response(lam_a, +delta, times)
    y_minus = impulse_response(lam_a, -delta, times)
    even_error = float(np.max(np.abs(y_plus - y_minus)))

    # Verify the exact transfer-function identity at a set of complex s values.
    identity_error = 0.0
    for s in (0.2 + 0.1j, 0.7 + 0.6j, 1.3 + 0.2j):
        M = np.array([[-1.0, delta], [delta, lam_a]], dtype=complex)
        measured = np.linalg.inv(s * np.eye(2) - M)[0, 0]
        formula = (s - lam_a) / ((s + 1.0) * (s - lam_a) - delta * delta)
        identity_error = max(identity_error, float(abs(measured - formula)))

    result = {
        "model": {
            "state_matrix": "M(delta)=[[-1,delta],[delta,lambda_dark]]",
            "input_and_output": "bright coordinate e1; impulse initializes x=e1; read y=e1^T x",
            "gate": "known switchable off-diagonal coupling delta",
            "hypotheses": [lam_a, lam_b],
            "hidden_rate_units": "inverse time",
            "sensor_noise_model_for_resource_estimate": "iid Gaussian endpoint noise with sd 0.005",
        },
        "baseline": {
            "transfer_function_for_both_hypotheses": "1/(s+1)",
            "maximum_impulse_trace_gap_on_grid": baseline_gap,
            "grid_points": int(len(times)),
            "time_window": [float(times[0]), float(times[-1])],
        },
        "gated_transfer_function": "(s-lambda_dark)/((s+1)(s-lambda_dark)-delta^2)",
        "gate_amplitude_sweep": gate_sweep,
        "polarity_evenness_max_error": even_error,
        "transfer_identity_max_error": identity_error,
        "interpretation": [
            "The baseline readout contains exactly no information about lambda_dark in this fixture.",
            "The known gate makes lambda_dark distinguishable from a single scalar port.",
            "Because the gate is purely off-diagonal, the pole sum is trace-invariant and recovers the dark rate without calibrating gate amplitude.",
            "The signal is quadratic in small delta, so endpoint noise drives a delta^-4 repeat cost.",
            "The computed repeat count assumes a known noise sd and exact model class; reset mismatch, gate uncertainty, drift, and model error are excluded.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
