"""Finite cold reset of the three-mode mediator, including an exact certificate.

The float eigenspectrum and numerical cooldown times are estimates.
The envelope ||exp(A*t)||_2^2 <= (145/1000)^floor(t/4) is certified
by integer Taylor arithmetic and rational positive-definiteness tests.
"""
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import expm, svdvals, solve_continuous_lyapunov
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parent
A0 = np.array([[0, 0, -1j], [0, -2j, -1j], [-1j, -1j, -2]], complex)
MAX_STORAGE_LOSS = Fraction(1, 10000)
A = A0 - np.diag([float(MAX_STORAGE_LOSS) / 2,
                    float(MAX_STORAGE_LOSS) / 2, 0])


def bareiss_determinant(source):
    a = [[int(x) for x in row] for row in source]
    n = len(a)
    if n == 1:
        return a[0][0]
    previous = 1
    for k in range(n - 1):
        pivot = a[k][k]
        if not pivot:
            raise ValueError("Unexpected zero leading pivot")
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return a[-1][-1]


def certify_four_unit_contraction(order=60):
    ar, ai = A0.real.astype(int), A0.imag.astype(int)
    realification = np.block([[ar, -ai], [ai, ar]]).astype(object)
    y = 4 * realification
    denominator = math.factorial(order)
    power = np.eye(6, dtype=object)
    numerator = denominator * power
    coefficient = denominator
    for k in range(1, order + 1):
        power = power @ y
        coefficient //= k
        numerator = numerator + coefficient * power
    # Tighten the zero-storage-loss Taylor bound to leave room for Duhamel.
    # Prove ||Taylor_60(4A0)||^2 < 0.1448 via Sylvester's criterion.
    certificate = (1448 * denominator ** 2 * np.eye(6, dtype=object)
                   - 10000 * numerator.T @ numerator)
    leading_minors = [bareiss_determinant(certificate[:k, :k]) for k in range(1, 7)]
    assert all(x > 0 for x in leading_minors)
    # ||4A|| <= 4||A||_F = 4sqrt(12) < 14; bound the Taylor tail geometrically.
    tail = Fraction(14 ** (order + 1) * (order + 2),
                    math.factorial(order + 1) * (order + 2 - 14))
    # Both A0 and A_loss generate contractions. Duhamel bounds their
    # difference at time 4 by 4*max(kb,kc)/2 <= 0.0002.
    duhamel = 4 * MAX_STORAGE_LOSS / 2
    combined_remainder = tail + duhamel
    norm_squared_upper = (Fraction(1448, 10000)
                          + Fraction(762, 1000) * combined_remainder
                          + combined_remainder ** 2)
    assert norm_squared_upper < Fraction(145, 1000)
    return {"taylor_order": order,
            "integer_PSD_leading_minors_positive": [x > 0 for x in leading_minors],
            "tail_operator_norm_bound": float(tail),
            "base_taylor_norm_squared_upper_bound": 0.1448,
            "max_allowed_kb_and_kc": float(MAX_STORAGE_LOSS),
            "duhamel_operator_norm_allowance_at_t4": float(duhamel),
            "rational_combined_norm_squared_upper_bound": float(norm_squared_upper),
            "certified_four_unit_energy_contraction_upper_bound": 0.145,
            "proof": "Exact integer Sylvester certificate for Taylor_60(4A0) norm^2<0.1448; rational Taylor tail plus Duhamel 4*max(kb,kc)/2 for the contractive damped perturbation. Valid for 0<=kb,kc<=1e-4 and both Z1 signs."}


def contraction(t):
    return float(svdvals(expm(A * t))[0] ** 2)


def allowed_nonvacuum_probability(epsilon):
    # sqrt(p)+p/2 <= epsilon, stable for small epsilon.
    return float(np.expm1(np.log1p(2 * epsilon) / 2) ** 2)


def reset_times(energy, epsilon):
    allowed = allowed_nonvacuum_probability(epsilon)
    if energy <= allowed:
        return {"energy_bound": energy, "trace_distance_target": epsilon,
                "allowed_nonvacuum_probability": allowed,
                "numerical_matrix_time": 0., "certified_envelope_time": 0.}
    hi = 4.
    while energy * contraction(hi) > allowed:
        hi *= 2
    exact_matrix_time = brentq(lambda t: energy * contraction(t) - allowed,
                               0, hi, xtol=1e-11)
    blocks = math.ceil(math.log(allowed / energy) / math.log(0.145))
    certified_time = 4 * blocks
    p_cert = energy * 0.145 ** blocks
    return {"energy_bound": energy, "trace_distance_target": epsilon,
            "allowed_nonvacuum_probability": allowed,
            "numerical_matrix_time": exact_matrix_time,
            "certified_envelope_time": certified_time,
            "certified_nonvacuum_probability_bound": p_cert,
            "certified_trace_distance_bound": math.sqrt(p_cert) + p_cert / 2}


def main():
    cert = certify_four_unit_contraction()
    eigenvalues, vectors = np.linalg.eig(A)
    faults = json.loads((ROOT.parent / "root/mediator_fault_results.json").read_text())
    energies = [{"qubit": f["physical_qubit"], "time_fraction": f["time_fraction"],
                 "residual_energy": max(p["max_final_mode_photons"] for p in f["pairs"])}
                for f in faults["X_faults"]]
    sample_max = max(x["residual_energy"] for x in energies)
    module_path = ROOT.parent / "root/finite_mediator_parity.py"
    spec = importlib.util.spec_from_file_location("finite_reset_root_model", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    report, _, _ = module.solve(module.Model(T=8))
    action = report["action_u"] + report["action_w"]
    warm_unit_covariance = solve_continuous_lyapunov(A, -np.diag([0., 0., 4.]))
    warm_example_n = 0.001
    warm_example_nonvacuum = float(1 - np.linalg.det(np.eye(3) + warm_example_n * warm_unit_covariance).real ** -1)
    optimized = json.loads((ROOT.parent / "conventional_routes/finite_mediator_optimization_results.json").read_text())
    optimized_matches = []
    def collect_actions(obj):
        if isinstance(obj, dict):
            if "action_u" in obj and abs(obj["action_u"] - 3.512284354200664) < 1e-8:
                optimized_matches.append({"action_u": obj["action_u"], "action_w": obj["action_w"]})
            for value in obj.values():
                collect_actions(value)
        elif isinstance(obj, list):
            for value in obj:
                collect_actions(value)
    collect_actions(optimized)
    out = {
        "scope": "Forces off, g=1 Gamma=4 chi=2; certificate covers 0<=kb,kc<=1e-4 with all baths cold and fixed data Z1. Default numerical values use adopted kb=kc=1e-4.",
        "adopted_numerical_model": {"g": 1., "Gamma": 4., "chi": 2., "kb": 0.0001, "kc": 0.0001},
        "baseline_kb_kc_zero_contraction_at_t4": float(svdvals(expm(A0 * 4))[0] ** 2),
        "eigenvalues": [{"real": float(z.real), "imag": float(z.imag)} for z in eigenvalues],
        "amplitude_decay_gap": float(-max(eigenvalues.real)),
        "asymptotic_energy_decay_rate": float(-2 * max(eigenvalues.real)),
        "eigenvector_condition_number": float(np.linalg.cond(vectors)),
        "contractions": [{"t": t, "energy_contraction": contraction(t)}
                         for t in [0, 1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 40, 48]],
        "exact_arithmetic_certificate": cert,
        "sampled_fault_energies": energies,
        "sampled_maximum_not_a_uniform_fault_time_bound": sample_max,
        "nominal_control_action_integral": action,
        "uniform_energy_bound_from_nominal_action_numeric": 8 * action,
        "uniform_energy_bound_if_action_is_enforced_at_most_20": 160,
        "optimized_pulse_stored_actions": optimized_matches,
        "optimized_uniform_energy_bound_if_action_is_enforced_at_most_30": 240,
        "hard_amplitude_cap_energy_bound_T8_abs_u_and_w_at_most_3": 1152,
        "cooldown_tables": [reset_times(e, eps) for e in [sample_max, 1, 10, 160, 240, 1152]
                            for eps in [0.01, 0.001, 0.0001, 0.000001]],
        "warm_bath_kb_kc_zero_only": {
            "mean_energy_floor": "3*n_input",
            "nonvacuum_steady_state_probability": "1-(1+n_input)^(-3)"},
        "warm_bath_adopted_kb_kc_numerical_not_part_of_cold_certificate": {
            "bath_model": "m bath thermal with flat occupancy n_input; b,c baths vacuum",
            "unit_occupation_stationary_covariance_real": warm_unit_covariance.real.tolist(),
            "unit_occupation_stationary_covariance_imag": warm_unit_covariance.imag.tolist(),
            "stationary_mean_number_per_input_n": float(np.trace(warm_unit_covariance).real),
            "n_input_example": warm_example_n,
            "stationary_nonvacuum_probability_example": warm_example_nonvacuum,
            "formula": "C_inf solves A C_inf+C_inf A^dagger=-Gamma*n_input*|m><m|; p_nonvac=1-1/det(I+C_inf)."},
    }
    (ROOT / "finite_reset_results.json").write_text(json.dumps(out, indent=2) + "\n")
    print("Decay gap", out["amplitude_decay_gap"])
    print("Certificate", cert)
    print("Nominal action", action, "uniform energy bound", 8 * action)
    for row in out["cooldown_tables"]:
        print(row)


if __name__ == "__main__":
    main()
