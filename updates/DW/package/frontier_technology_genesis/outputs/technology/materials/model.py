"""Conditional calculations for the materials candidate; no experimental validation.

Run: python3 work/genesis_materials/model.py
Only Python's standard library is needed. Numbers are order-of-magnitude design
budgets, not measured instrument performance or an optimization result.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

EPS0 = 8.8541878128e-12
KB = 1.380649e-23


def spheroid_trace_factor(c_over_a: float) -> float:
    """Tr(alpha)/(9 eps0 V), using exact conducting-spheroid factors."""
    k = c_over_a
    if abs(k - 1.0) < 1e-8:
        return 1.0
    if k > 1.0:
        e = math.sqrt(1.0 - k ** -2)
        lz = (1.0 - e * e) / (2 * e**3) * (
            math.log((1 + e) / (1 - e)) - 2 * e
        )
    else:
        xi = math.sqrt(k ** -2 - 1.0)
        lz = (1 + xi * xi) / xi**3 * (xi - math.atan(xi))
    lx = (1 - lz) / 2
    return (2 / lx + 1 / lz) / 9


def prolate_for_factor(target: float) -> float:
    lo, hi = 1.0, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if spheroid_trace_factor(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def vec_add(a, b):
    return [x + y for x, y in zip(a, b)]


def vec_scale(c, a):
    return [c * x for x in a]


def mat_vec(a, x):
    return [sum(ai * xi for ai, xi in zip(row, x)) for row in a]


def parity_force_demo():
    """Finite-body algebra with deliberately nonzero gradient-induced dipole.

    This is a coefficient identity test, not a boundary-element simulation.
    The 'b' input represents B:G, which a point-dipole model omits.
    """
    alpha = [[2.0, .2, .3], [.2, 1.0, -.1], [.3, -.1, 1.5]]
    gradient = [[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0]]
    e = [1.0, 0.0, 0.0]
    r = [.2, -.1, .1]
    b = [.7, -.2, .4]
    p_q = [.03, -.02, .01]
    charge = .5
    result = [0.0] * 3
    phases = []
    for s in [-1, 1]:
        for t in [-1, 1]:
            # Laboratory dipole includes q r, fixed-charge dipole, uniform
            # response, position-induced response, and gradient response.
            p = vec_add(vec_scale(charge, r), p_q)
            p = vec_add(p, mat_vec(alpha, vec_scale(s, e)))
            p = vec_add(p, mat_vec(alpha, vec_scale(t, mat_vec(gradient, r))))
            p = vec_add(p, vec_scale(t, b))
            force = vec_add(vec_scale(charge * s, e),
                            vec_scale(t, mat_vec(gradient, p)))
            phases.append({"s": s, "t": t, "force": force})
            result = vec_add(result, vec_scale(s * t / 4, force))
    exact = mat_vec(gradient, mat_vec(alpha, e))
    error = max(abs(x - y) for x, y in zip(result, exact))
    assert error < 1e-12
    return {"phases": phases, "demodulated_force": result,
            "G_alpha_e": exact, "max_error": error,
            "status": "algebraic finite coefficient check only"}


def trace_field_demo():
    alpha = [[2.0, .2, .3], [.2, 1.0, -.1], [.3, -.1, 1.5]]
    gradients = [
        [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
    ]
    forces = []
    for j, gradient in enumerate(gradients):
        e = [int(i == j) for i in range(3)]
        forces.append(mat_vec(gradient, mat_vec(alpha, e)))
    mean = [sum(f[i] for f in forces) / 3 for i in range(3)]
    trace = sum(alpha[i][i] for i in range(3))
    assert abs(mean[0] - trace / 3) < 1e-12
    # The transverse force is real; exact full-vector trace cancellation fails.
    assert abs(mean[2] - alpha[0][2] / 3) < 1e-12
    return {"forces": forces, "average": mean, "trace_over_three": trace / 3,
            "transverse_xz_over_three": alpha[0][2] / 3}


def main():
    radius, rho = 15e-6, 2700.0
    volume = 4 * math.pi * radius**3 / 3
    mass = rho * volume
    field, gradient = 1e6, 1e9
    a = 3 * EPS0 * field * gradient / rho
    kick, drift = 1e-3, 10e-3
    displacement = a * kick * (drift + kick / 2)
    void = .01
    signal = displacement * (1 / (1 - void) - 1)
    throughput = (1 / 3600) / mass  # particles/s at 1 kg/h
    lane_speed, separation = 5.0, .5e-3
    rate_per_lane = lane_speed / separation
    phi_max = .01
    eta_max, eps_alpha, eps_r, rho_rel_max = .001, .001, .002, 1.001
    measured_accept_threshold = ((1 - eta_max) * (1 - eps_alpha) /
                                 ((1 - phi_max) * rho_rel_max * (1 + eps_r)))

    # Epstein drag approximation in nitrogen; accommodation prefactor omitted.
    pressure, temperature, molecule_mass = .1, 300, 28 * 1.66053906660e-27
    gas_rho = pressure * molecule_mass / (KB * temperature)
    cbar = math.sqrt(8 * KB * temperature / (math.pi * molecule_mass))
    drag_tau = rho * radius / (gas_rho * cbar)
    alpha_sphere = 3 * EPS0 * volume
    charge = 1e-13
    charge_terms = []
    electrical_terms = []
    for frequency in [1e5, 1e6, 1e7, 2e7]:
        omega = 2 * math.pi * frequency
        charge_terms.append({"frequency_Hz": frequency,
                             "q_C": charge,
                             "ponderomotive_ratio_q2_over_mw2alpha":
                                 charge**2 / (mass * omega**2 * alpha_sphere),
                             "charge_driven_position_amplitude_m":
                                 charge * field / (mass * omega**2)})
        # Arbitrary illustrative 10 pF, 1 kV RMS capacitive load with Q=100.
        c_load, voltage, q_factor = 10e-12, 1000, 100
        reactive_va = omega * c_load * voltage**2
        electrical_terms.append({"frequency_Hz": frequency,
                                 "capacitance_F": c_load, "voltage_rms_V": voltage,
                                 "reactive_VA": reactive_va,
                                 "loss_at_Q100_W": reactive_va / q_factor})

    # Gradient modulation must be mechanically resolved for parity subtraction.
    # x=A/(2 pi f)^2 for an acceleration harmonic of amplitude A.
    demodulation = []
    for frequency in [100, 1000, 10000, 100000, 1000000]:
        displacement_amp = a / (2 * math.pi * frequency)**2
        # Conditional rotation error scale chi*omega_rot/f, not a rigorous bound.
        demodulation.append({"modulation_Hz": frequency,
                             "mechanical_response_amplitude_m": displacement_amp,
                             "one_percent_response_m": .01 * displacement_amp,
                             "rotation_scale_chi0p2_omega1e5": .2 * 1e5 / frequency})

    # Rigorous coarse bound for equal three slots if ||alpha_dot||<=2 Omega||alpha||:
    # Relative trace-extraction error <= 2 Omega h, h=full frame duration.
    rotation_bound = {"angular_speed_bound_rad_s": 1e5,
                      "required_frame_duration_for_0p1pct_s": .001 / (2e5),
                      "comment": "coarse worst-case PSD bound; symmetric scheduling can improve only with additional smoothness bounds"}

    # Off-axis scalar lower coefficient divided by central coefficient.
    # This applies to the point-dipole three-field average, not the exact parity
    # acquisition, which cancels all even-gradient terms at fixed configuration.
    off_axis = []
    for x, z in [(0, 0), (0, 15e-6), (0, 50e-6), (0, 100e-6),
                 (50e-6, 50e-6)]:
        c_ratio = (field + gradient * x - abs(gradient * z) / 2) / field
        off_axis.append({"x_m": x, "z_m": z,
                         "conservative_force_coefficient_ratio": c_ratio,
                         "trace_upper_bound_inflation_over_center": 1 / c_ratio})

    result = {
        "status": "conditional equations and numerical budgets; no experimental validation",
        "sphere": {"radius_m": radius, "rho_kg_m3": rho, "volume_m3": volume,
                   "mass_kg": mass, "trace_alpha_over_mass_SI": 9 * EPS0 / rho,
                   "E0_V_m": field, "g_V_m2": gradient, "acceleration_m_s2": a,
                   "kick_s": kick, "drift_s": drift,
                   "displacement_m": displacement,
                   "extra_displacement_at_1pct_void_m": signal,
                   "radius_over_field_length": radius * gradient / field},
        "shape": [{"aspect_c_over_a": k, "trace_factor": spheroid_trace_factor(k)}
                  for k in [.5, .8, .9, 1, 1.02, 1.05, 1.1, 1.2, 1.5, 2]],
        "shape_inverse_counterexample": {
            "porous_sphere_void_fraction": void,
            "dense_prolate_aspect_with_same_trace_per_mass":
                prolate_for_factor(1 / (1 - void)),
            "comment": "High alpha/m cannot identify porosity; low-value acceptance remains one-sided."},
        "robust_certificate_example": {
            "porosity_target": phi_max, "eta_max": eta_max,
            "finite_conductor_loss_fraction": eps_alpha,
            "measurement_relative_upper_error": eps_r,
            "rho_max_over_nominal": rho_rel_max,
            "normalized_measured_accept_threshold": measured_accept_threshold,
            "largest_dense_prolate_aspect_accepted_at_threshold":
                prolate_for_factor(measured_accept_threshold)},
        "composition_counterexample": {
            "void_volume_fraction": .02,
            "high_density_inclusion_volume_fraction": .02,
            "inclusion_rho_over_nominal": 2,
            "mass_over_nominal_filled_mass": (1 - .02 - .02) + 2 * .02,
            "comment": "A nominal-density certificate falsely accepts this particle unless per-particle density/composition is bounded."},
        "throughput": {"kg_h": 1, "particles_s": throughput,
                       "lane_speed_m_s": lane_speed, "spacing_m": separation,
                       "particles_s_lane": rate_per_lane,
                       "lanes_required": math.ceil(throughput / rate_per_lane),
                       "illustrative_12_phase_records_s": 12 * throughput,
                       "minimum_one_error_free_false_accept_trial_count_for_95pct_bound_1e_minus6":
                           math.ceil(math.log(.05) / math.log(1 - 1e-6))},
        "vacuum": {"pressure_Pa": pressure, "temperature_K": temperature,
                   "gas_density_kg_m3": gas_rho, "mean_molecular_speed_m_s": cbar,
                   "epstein_time_s_approx": drag_tau,
                   "kick_plus_drift_over_drag_time": (kick + drift) / drag_tau},
        "charge": charge_terms, "illustrative_capacitive_cost": electrical_terms,
        "signed_force_mechanical_readout": demodulation,
        "rotation_bound": rotation_bound, "point_dipole_off_axis_bound": off_axis,
        "parity_identity_check": parity_force_demo(),
        "scalar_trace_field_check": trace_field_demo(),
    }
    path = Path(__file__).with_name("model_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
