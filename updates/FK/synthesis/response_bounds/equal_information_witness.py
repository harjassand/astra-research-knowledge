#!/usr/bin/env python3
"""Reproduce an equal-information thermal-response witness and noisy readout.

The certification rule receives only the Euclidean data, the exact first
commutator moment, and an optional static-response calibration.  The spectral
atoms below are hidden benchmark-generator inputs; they are not inputs to the
rule.  Noise is a declared independent Gaussian instrument model, not physical
device data or an MCMC error model.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import NormalDist

import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
BETA = mp.mpf(1)
ETA = mp.mpf(1)
TAUS = [mp.mpf(0)] + [mp.mpf(k) / 12 for k in range(1, 6)]
OMEGAS = list(
    map(mp.mpf, ["0.07", "0.16", "1.9", "5.3", "9", "15", "21.5", "28.5", "40"])
)
SEED = 20261014


def euclidean_kernel(tau: mp.mpf, omega: mp.mpf) -> mp.mpf:
    return (mp.exp(-tau * omega) + mp.exp(-(BETA - tau) * omega)) / (
        1 - mp.exp(-BETA * omega)
    )


def response_kernel(eta: mp.mpf, omega: mp.mpf) -> mp.mpf:
    return 2 * omega / (omega * omega + eta * eta)


def static_kernel(omega: mp.mpf) -> mp.mpf:
    return 2 / omega


def finite_duration_response(weight: mp.mpf, omega: mp.mpf, eta: mp.mpf, tmax: mp.mpf) -> mp.mpf:
    """Integral_0^T exp(-eta*t) 2*weight*sin(omega*t) dt."""
    numerator = omega - mp.exp(-eta * tmax) * (
        eta * mp.sin(omega * tmax) + omega * mp.cos(omega * tmax)
    )
    return 2 * weight * numerator / (omega * omega + eta * eta)


def make_pair() -> dict:
    # Six Euclidean correlators, M_1=2 int omega dmu, and chi(0).
    constraints = [
        [euclidean_kernel(tau, omega) for omega in OMEGAS] for tau in TAUS
    ] + [
        [2 * omega for omega in OMEGAS],
        [static_kernel(omega) for omega in OMEGAS],
    ]
    a = mp.matrix(constraints)
    # Define the null vector exactly in terms of the displayed real matrix.
    # The first eight columns have nonzero determinant for this fixed support;
    # interval determinant/Cramer checks below certify the sign and positivity.
    v_head = mp.lu_solve(a[:, 0:8], -a[:, 8])
    v = list(v_head) + [mp.mpf(1)]

    # Positive reference measure with M_1 exactly one.
    base = [1 / (2 * len(OMEGAS) * omega) for omega in OMEGAS]
    delta = mp.mpf("0.000001")
    plus = [b + delta * q for b, q in zip(base, v)]
    minus = [b - delta * q for b, q in zip(base, v)]
    assert min(plus + minus) > 0

    def integrate(weights: list[mp.mpf], fn) -> mp.mpf:
        return mp.fsum(w * fn(x) for w, x in zip(weights, OMEGAS))

    c_plus = [integrate(plus, lambda x: euclidean_kernel(tau, x)) for tau in TAUS]
    c_minus = [integrate(minus, lambda x: euclidean_kernel(tau, x)) for tau in TAUS]
    m1_plus = integrate(plus, lambda x: 2 * x)
    m1_minus = integrate(minus, lambda x: 2 * x)
    static_plus = integrate(plus, static_kernel)
    static_minus = integrate(minus, static_kernel)
    chi_plus = integrate(plus, lambda x: response_kernel(ETA, x))
    chi_minus = integrate(minus, lambda x: response_kernel(ETA, x))

    residual = max(
        [abs(x - y) for x, y in zip(c_plus, c_minus)]
        + [abs(m1_plus - m1_minus), abs(static_plus - static_minus)]
    )
    assert residual < mp.mpf("1e-80")
    return {
        "matrix": a,
        "null_vector": v,
        "base": base,
        "delta": delta,
        "plus": plus,
        "minus": minus,
        "correlators": c_plus,
        "m1": m1_plus,
        "static": static_plus,
        "chi_plus": chi_plus,
        "chi_minus": chi_minus,
        "gap": abs(chi_plus - chi_minus),
        "residual": residual,
    }


def interval_audit() -> dict:
    """Outward interval checks for the concrete support and delta=10^-6."""
    iv = mp.iv
    iv.dps = 60
    beta, eta = iv.mpf(1), iv.mpf(1)
    frequencies = [
        iv.mpf(x) for x in ["0.07", "0.16", "1.9", "5.3", "9", "15", "21.5", "28.5", "40"]
    ]
    taus = [iv.mpf(0)] + [iv.mpf(k) / 12 for k in range(1, 6)]

    def k_iv(tau, omega):
        return (iv.exp(-tau * omega) + iv.exp(-(beta - tau) * omega)) / (
            1 - iv.exp(-beta * omega)
        )

    constraints = [
        [k_iv(tau, omega) for omega in frequencies] for tau in taus
    ] + [[2 * omega for omega in frequencies], [2 / omega for omega in frequencies]]
    matrix = iv.matrix(constraints)
    square = matrix[:, 0:8]
    determinant = iv.det(square)
    if not float(determinant.b) < 0:
        raise ArithmeticError("interval determinant did not exclude zero")

    v_bounds = []
    for column in range(8):
        replaced = iv.matrix(square)
        for row in range(8):
            replaced[row, column] = matrix[row, 8]
        v_bounds.append(-iv.det(replaced) / determinant)
    v_bounds.append(iv.mpf(1))

    delta = iv.mpf("0.000001")
    base = [1 / (18 * omega) for omega in frequencies]
    weights = []
    for b, v in zip(base, v_bounds):
        wp, wm = b + delta * v, b - delta * v
        if min(float(wp.a), float(wm.a)) <= 0:
            raise ArithmeticError("interval positivity check failed")
        weights.append((wp, wm))

    target = [2 * omega / (omega * omega + eta * eta) for omega in frequencies]
    gap = 2 * delta * sum((v * g for v, g in zip(v_bounds, target)), iv.mpf(0))
    if not (float(gap.a) > 0 or float(gap.b) < 0):
        raise ArithmeticError("interval response-gap check failed")
    return {
        "determinant_interval": str(determinant),
        "response_gap_interval_signed": str(gap),
        "minimum_weight_lower_endpoint": min(
            min(float(wp.a), float(wm.a)) for wp, wm in weights
        ),
    }


def s(x: mp.mpf, digits: int = 15) -> str:
    return mp.nstr(x, digits)


def main() -> None:
    mp.mp.dps = 100
    pair = make_pair()
    audited = interval_audit()

    # A single realized data vector under the common Gaussian mean model.
    rng = np.random.default_rng(SEED)
    sigma_euclidean = 0.02
    sigma_static = 0.05
    cmean = np.array([float(x) for x in pair["correlators"]])
    observed_c = cmean + rng.normal(0.0, sigma_euclidean, size=len(cmean))
    observed_static = float(pair["static"]) + rng.normal(0.0, sigma_static)

    # A finite-duration exponentially ramped source probes the desired
    # susceptibility directly in linear response.  Simulate its calibrated
    # central-difference readout; all calibration bounds are explicit below.
    eta_f = float(ETA)
    tmax_f = 12.0
    f0 = 0.1
    n_per_sign = 10_000
    sigma_A = 0.02
    sigma_Abar = sigma_A / math.sqrt(n_per_sign)
    chi_t = mp.fsum(
        finite_duration_response(w, om, ETA, mp.mpf(str(tmax_f)))
        for w, om in zip(pair["plus"], OMEGAS)
    )
    a_plus_mean = f0 * float(chi_t)
    a_minus_mean = -f0 * float(chi_t)
    a_plus_obs = a_plus_mean + rng.normal(0.0, sigma_Abar)
    a_minus_obs = a_minus_mean + rng.normal(0.0, sigma_Abar)
    chi_hat = (a_plus_obs - a_minus_obs) / (2 * f0)

    alpha_intervention = 0.01
    z_intervention = NormalDist().inv_cdf(1 - alpha_intervention / 2)
    stat_radius = z_intervention * sigma_A / (math.sqrt(2 * n_per_sign) * f0)

    # Declared conditional systematic bounds for this simulated instrument.
    alpha_euclidean = 0.01
    z_euclidean = NormalDist().inv_cdf(1 - alpha_euclidean / (2 * len(observed_c)))
    c0_upper = observed_c[0] + z_euclidean * sigma_euclidean
    m0_upper = 2 * c0_upper
    tail_radius = m0_upper * math.exp(-eta_f * tmax_f) / eta_f
    gain_A_rel = 0.003
    force_rel = 0.002
    cal_factor_high = (1 + gain_A_rel) ** 2 * (1 + force_rel) - 1
    cal_factor_low = 1 - (1 - gain_A_rel) ** 2 * (1 - force_rel)
    calibration_radius = max(cal_factor_high, cal_factor_low) * abs(chi_hat)
    B3 = 0.3
    nonlinear_radius = B3 * f0 * f0 / 6
    waveform_l1_error = 1e-5
    waveform_radius = m0_upper * waveform_l1_error
    total_radius = (
        stat_radius + tail_radius + calibration_radius + nonlinear_radius + waveform_radius
    )

    result = {
        "scope": {
            "status": "reproducible synthetic Gaussian acquisition; not physical device data",
            "noise_law": "independent Gaussian additive Euclidean/static readout; Gaussian central-difference readout",
            "hidden_generator_inputs_not_given_to_certifier": "finite positive spectral atoms in the script",
            "physical_acquisition": False,
            "MCMC_or_autocorrelation_model": False,
        },
        "model": {
            "beta": 1.0,
            "eta": 1.0,
            "first_matsubara": 2 * math.pi,
            "eta_over_first_matsubara": 1 / (2 * math.pi),
            "tau": [float(t) for t in TAUS],
            "frequencies": [float(x) for x in OMEGAS],
            "M1_exact": s(pair["m1"]),
        },
        "equal_information_pair": {
            "weights_plus": [s(x) for x in pair["plus"]],
            "weights_minus": [s(x) for x in pair["minus"]],
            "null_vector_definition_values": [s(x) for x in pair["null_vector"]],
            "null_vector_scale_delta": s(pair["delta"]),
            "euclidean_means_common": [s(x) for x in pair["correlators"]],
            "static_response_common": s(pair["static"]),
            "target_chi_eta_plus": s(pair["chi_plus"]),
            "target_chi_eta_minus": s(pair["chi_minus"]),
            "target_gap": s(pair["gap"]),
            "max_equal_information_residual_100dps": s(pair["residual"], 8),
            "first_8_column_determinant_100dps_diagnostic": s(mp.det(pair["matrix"][:, 0:8]), 20),
            "interval_audit": audited,
        },
        "noisy_euclidean_acquisition": {
            "seed": SEED,
            "sigma_each": sigma_euclidean,
            "observed_values": observed_c.tolist(),
            "known_simulator_standard_errors": [sigma_euclidean] * len(observed_c),
            "same_distribution_under_plus_and_minus": True,
            "static_response_sigma": sigma_static,
            "static_response_observed": observed_static,
            "static_response_same_distribution_under_plus_and_minus": True,
        },
        "calibrated_exponential_drive_demo": {
            "drive": "f(t)=+/-f0*exp(eta*t), -T<=t<=0; linear-response output is +/-f0*int_0^T exp(-eta*s)R(s)ds",
            "T": tmax_f,
            "f0": f0,
            "samples_per_sign": n_per_sign,
            "per_sample_A_standard_deviation": sigma_A,
            "finite_T_mean_plus": a_plus_mean,
            "finite_T_mean_minus": a_minus_mean,
            "observed_chi_estimate": chi_hat,
            "statistical_radius_99pct": stat_radius,
            "C0_upper_from_euclidean_data": c0_upper,
            "M0_upper": m0_upper,
            "tail_radius": tail_radius,
            "relative_A_gain_bound": gain_A_rel,
            "relative_force_calibration_bound": force_rel,
            "maximum_multiplicative_error_factor": max(cal_factor_high, cal_factor_low),
            "calibration_radius": calibration_radius,
            "declared_third_derivative_bound": B3,
            "nonlinear_radius": nonlinear_radius,
            "source_waveform_L1_error_bound": waveform_l1_error,
            "waveform_radius": waveform_radius,
            "total_radius_under_declared_bounds": total_radius,
            "joint_coverage_lower_bound": 1 - alpha_intervention - alpha_euclidean / len(observed_c),
            "conditional_interval": [chi_hat - total_radius, chi_hat + total_radius],
            "warning": "synthetic acquisition only; real-system gain, waveform, nonlinear-response and thermalization bounds require independent receipts",
        },
    }
    (HERE / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    with (HERE / "noisy_euclidean.csv").open("w") as f:
        f.write("tau,observed_C,simulated_sigma\n")
        for tau, val in zip(TAUS, observed_c):
            f.write(f"{float(tau):.12g},{val:.17g},{sigma_euclidean:.17g}\n")

    print(json.dumps({
        "euclidean_means": result["equal_information_pair"]["euclidean_means_common"],
        "static": result["equal_information_pair"]["static_response_common"],
        "chi_plus": result["equal_information_pair"]["target_chi_eta_plus"],
        "chi_minus": result["equal_information_pair"]["target_chi_eta_minus"],
        "gap": result["equal_information_pair"]["target_gap"],
        "equal_residual": result["equal_information_pair"]["max_equal_information_residual_100dps"],
        "noisy_euclidean": observed_c.tolist(),
        "intervention_center": chi_hat,
        "intervention_total_radius": total_radius,
        "intervention_interval": result["calibrated_exponential_drive_demo"]["conditional_interval"],
    }, indent=2))


if __name__ == "__main__":
    main()
