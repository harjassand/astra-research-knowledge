"""GLS estimator and lack-of-fit diagnostic for multi-colour dispersion barometry.

This is a model-level design check using the first-order helium slopes reported
by Yang, Stone & Egan (2025). It is not a replay of their instrument data.
"""

from __future__ import annotations

import json
from math import sqrt
from pathlib import Path

import numpy as np

R = 8.31446261815324
T = 303.0
A_EPS_CM3_MOL = 0.51725408
A2_CM3_MOL = 1.332465e-4
CM3_TO_M3 = 1e-6
FREQUENCIES_HZ = np.array([194.368624e12, 473.611873e12, 750.0e12])
SIGMA_F_HZ = 200.0


def pressure_slopes(frequencies_hz: np.ndarray) -> np.ndarray:
    x = frequencies_hz / 1e14
    ar_m3_mol = (A_EPS_CM3_MOL + A2_CM3_MOL * x**2) * CM3_TO_M3
    return 3.0 * ar_m3_mol / (2.0 * R * T)


def gls_fit(z: np.ndarray, a: np.ndarray, covariance: np.ndarray,
            nuisance: np.ndarray | None = None) -> dict[str, np.ndarray | float | int]:
    """Fit z = p*a + nuisance@theta using generalized least squares."""
    if nuisance is None:
        nuisance = np.ones((len(a), 1))
    design = np.column_stack((a, nuisance))
    precision = np.linalg.inv(covariance)
    information = design.T @ precision @ design
    rank = int(np.linalg.matrix_rank(design))
    if rank != design.shape[1]:
        raise ValueError("pressure and nuisance coefficients are not identifiable")
    coefficient_covariance = np.linalg.inv(information)
    theta = coefficient_covariance @ design.T @ precision @ z
    residual = z - design @ theta
    chi2 = float(residual.T @ precision @ residual)
    return {
        "theta": theta,
        "coefficient_covariance": coefficient_covariance,
        "residual": residual,
        "chi2": chi2,
        "degrees_of_freedom": len(a) - rank,
        "design_rank": rank,
    }


def main() -> None:
    a = pressure_slopes(FREQUENCIES_HZ)
    # Frequency-change noise is converted to the dimensionless fractional
    # resonance coordinate separately in each colour.
    sigma_z = SIGMA_F_HZ / FREQUENCIES_HZ
    covariance = np.diag(sigma_z**2)
    p_true = 250e3
    d_true = -1e-11 * p_true  # illustrative shared deformation, not source fit
    z = a * p_true + d_true

    fit = gls_fit(z, a, covariance)
    theta = np.asarray(fit["theta"])
    fit_cov = np.asarray(fit["coefficient_covariance"])
    p_se = sqrt(float(fit_cov[0, 0]))

    # Exact third-colour contrast against the first-two-colour estimate.
    q = (a[2] - a[0]) / (a[1] - a[0])
    contrast = np.array([q - 1.0, -q, 1.0])
    contrast_sigma = sqrt(float(contrast @ covariance @ contrast))
    contrast_source = float(contrast @ z)

    # A 2e-12 dimensionless offset on the third channel is synthetic. It
    # demonstrates the residual test's sensitivity to one non-collinear error.
    injected_chromatic = np.array([0.0, 0.0, 2e-12])
    bad_fit = gls_fit(z + injected_chromatic, a, covariance)
    bad_contrast = float(contrast @ (z + injected_chromatic))
    bad_fit_se = sqrt(float(np.asarray(bad_fit["coefficient_covariance"])[0, 0]))

    # An error parallel to the pressure-response vector is exactly aliased with
    # pressure for any number of wavelengths; the residual is identically zero.
    eta = 5.7e-6
    aliased_z = a * p_true * (1.0 + eta) + d_true
    alias_fit = gls_fit(aliased_z, a, covariance)
    alias_residual_norm = float(np.linalg.norm(np.asarray(alias_fit["residual"])))

    result = {
        "frequencies_Hz": FREQUENCIES_HZ.tolist(),
        "pressure_slopes_Pa-1": a.tolist(),
        "assumptions": {
            "temperature_K": T,
            "per_colour_frequency_noise_Hz": SIGMA_F_HZ,
            "noise_covariance": "independent diagonal; design illustration only",
            "shared_deformation_slope_Pa-1": -1e-11,
        },
        "common_mode_fit": {
            "pressure_Pa": float(theta[0]),
            "pressure_standard_error_Pa": p_se,
            "relative_pressure_standard_error_ppm_at_250kPa": p_se / p_true * 1e6,
            "chi2": float(fit["chi2"]),
            "degrees_of_freedom": int(fit["degrees_of_freedom"]),
        },
        "third_colour_lack_of_fit": {
            "contrast_weights": contrast.tolist(),
            "contrast_sigma": contrast_sigma,
            "common_mode_contrast": contrast_source,
            "synthetic_third_colour_offset": 2e-12,
            "synthetic_offset_z_score": bad_contrast / contrast_sigma,
            "synthetic_offset_pressure_bias_ppm": (float(np.asarray(bad_fit["theta"])[0]) / p_true - 1.0) * 1e6,
        },
        "exact_alias_counterexample": {
            "parallel_dispersion_scale_error_eta": eta,
            "fitted_pressure_bias_ppm": (float(np.asarray(alias_fit["theta"])[0]) / p_true - 1.0) * 1e6,
            "residual_norm": alias_residual_norm,
        },
        "status": "finite model calculation; no raw source data replay or device validation",
    }
    out = Path(__file__).with_name("multicolor_design_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    assert abs(float(theta[0]) - p_true) < 1e-6
    assert int(fit["degrees_of_freedom"]) == 1
    assert abs((float(np.asarray(alias_fit["theta"])[0]) / p_true - 1.0) - eta) < 1e-10
    assert alias_residual_norm < 1e-12
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
