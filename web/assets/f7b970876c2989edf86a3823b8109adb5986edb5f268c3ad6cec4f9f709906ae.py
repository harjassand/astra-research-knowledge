#!/usr/bin/env python3
"""Local D/G-optimal reference design for Y=c+a*k/(b+k).

This is a conditional design calculator. It assumes exact certified k values,
one stable probe epoch, and homoscedastic independent voltage errors. It does
not fit the source authors' AFM data or certify a real tip/sample interface.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def gradient(k: float, a: float, b: float) -> np.ndarray:
    z = k / (b + k)
    return np.array([z, -(a / b) * z * (1.0 - z), 1.0], dtype=float)


def transformed_midpoint(k_lo: float, k_hi: float, b: float) -> float:
    """Conductivity whose z=k/(b+k) is midway between endpoint z values."""
    if not (0 < k_lo < k_hi and b > 0):
        raise ValueError("require 0 < k_lo < k_hi and b > 0")
    return (b * (k_lo + k_hi) + 2 * k_lo * k_hi) / (2 * b + k_lo + k_hi)


def mean_information(ks: np.ndarray, a: float, b: float) -> np.ndarray:
    jac = np.vstack([gradient(float(k), a, b) for k in ks])
    return jac.T @ jac / len(ks)


def leverage(k: float, info: np.ndarray, a: float, b: float) -> float:
    g = gradient(k, a, b)
    return float(g @ np.linalg.solve(info, g))


def inverse_sd(k: float, design_info: np.ndarray, n: int,
               sigma_ref_y: float, sigma_unknown_y: float,
               a: float, b: float) -> float:
    curve_var = sigma_ref_y**2 * leverage(k, design_info, a, b) / n
    total_y_var = sigma_unknown_y**2 + curve_var
    slope = a * b / (b + k) ** 2
    return math.sqrt(total_y_var) / slope


def run() -> dict:
    # Published dataset-3 local fit and published approximate useful range.
    a, b, c = 0.8245, 0.1892, -0.7128
    k_lo, k_hi = 0.1, 10.0
    n = 6
    k_mid = transformed_midpoint(k_lo, k_hi, b)

    d_opt_ks = np.array([k_lo, k_mid, k_hi] * 2, dtype=float)
    log_uniform_ks = np.geomspace(k_lo, k_hi, n)
    d_info = mean_information(d_opt_ks, a, b)
    base_info = mean_information(log_uniform_ks, a, b)

    grid = np.geomspace(k_lo, k_hi, 10001)
    d_lev = np.array([leverage(float(k), d_info, a, b) for k in grid])
    base_lev = np.array([leverage(float(k), base_info, a, b) for k in grid])
    det_ratio = float(np.linalg.det(d_info) / np.linalg.det(base_info))

    # Sensitivity illustration only; sigma is in the paper's voltage-difference units.
    sigma_y = 1e-3
    inverse_examples = {
        f"{k:g}": inverse_sd(k, d_info, n, sigma_y, sigma_y, a, b)
        for k in (k_lo, k_mid, 1.0, k_hi)
    }
    response = lambda k: c + a * k / (b + k)

    return {
        "model": "Y=c+a*k/(b+k)",
        "nominal_parameters_source_dataset3": {"a": a, "b": b, "c": c},
        "design_domain_W_mK": [k_lo, k_hi],
        "n_reference_measurements": n,
        "d_optimal_support_W_mK": [k_lo, k_mid, k_hi],
        "d_optimal_replicates": [2, 2, 2],
        "log_uniform_comparator_W_mK": log_uniform_ks.tolist(),
        "local_information_determinant_ratio_Dopt_to_log_uniform": det_ratio,
        "max_response_leverage_Dopt": float(d_lev.max()),
        "max_response_leverage_log_uniform": float(base_lev.max()),
        "sharp_theorem_bound": 3.0,
        "nominal_voltage_response_at_support": [response(float(k)) for k in (k_lo, k_mid, k_hi)],
        "inverse_sd_W_mK_if_sigma_ref_and_unknown_each_1e-3": inverse_examples,
        "assumptions": [
            "correct rational calibration law",
            "single stable probe/electronics epoch",
            "exact reference conductivities",
            "independent homoscedastic reference-voltage errors",
            "local Fisher/delta-method uncertainty only",
        ],
        "not_validated": [
            "real material standard availability at k_mid",
            "errors-in-variables shifts from certificate uncertainty",
            "shared reference and drift covariance",
            "probe-apex changes and calibration-model misspecification",
        ],
    }


if __name__ == "__main__":
    result = run()
    out = Path(__file__).with_name("design_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    assert result["max_response_leverage_Dopt"] <= 3.0 + 1e-10
    assert result["max_response_leverage_Dopt"] >= 3.0 - 1e-8
    assert result["local_information_determinant_ratio_Dopt_to_log_uniform"] > 1.0
