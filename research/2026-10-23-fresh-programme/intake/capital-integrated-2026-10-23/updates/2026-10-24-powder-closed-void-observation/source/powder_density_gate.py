#!/usr/bin/env python3
"""Exact interface checks and assumed physical scales; no acquired experiment."""
from fractions import Fraction as F
import json
import math
from pathlib import Path


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inv(a):
    n = len(a)
    b = [[F(x) for x in row] + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        k = next(k for k in range(j, n) if b[k][j])
        b[j], b[k] = b[k], b[j]
        z = b[j][j]
        b[j] = [x / z for x in b[j]]
        for i in range(n):
            if i != j:
                z = b[i][j]
                b[i] = [x - z * y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def diag(xs):
    return [[F(x) if i == j else F(0) for j in range(len(xs))] for i, x in enumerate(xs)]


def exact_checks():
    rho = F(2700)
    cutoff = F(1, 100)
    eta = F(0)
    bath = rho * (1 - cutoff) / (1 - eta)
    assert bath == 2673
    # One equal-volume bad grain and one dense grain are an exact max-tail failure.
    bad_phi = F(3, 200)
    bad_rho = rho * (1 - bad_phi)
    aggregate_rho = (bad_rho + rho) / 2
    assert bad_rho < bath < aggregate_rho
    # Unknown fluid-access state: same two buoyant masses, different dry masses.
    cases = [(F(10), F(1), F(1)), (F(12), F(3), F(2))]
    outputs = [(m - v1, m - 2 * v2) for m, v1, v2 in cases]
    assert outputs[0] == outputs[1] == (9, 8)
    # Exact finite-body affine-force Jacobian trace and constant-readout invariance.
    alpha = [[F(3), F(1), F(0)], [F(1), F(4), F(1)], [F(0), F(1), F(2)]]
    q, mass, g = F(7), F(2), F(3)
    gs = [diag([g, -g, 0]), diag([0, g, -g]), diag([-g, 0, g])]
    sensor = [[2, 1, 0], [0, 3, 1], [0, 0, 4]]
    sensor_inverse = inv(sensor)
    jacobians = []
    for G in gs:
        gag = mm(mm(G, alpha), G)
        J = [[(q * G[i][j] + gag[i][j]) / mass for j in range(3)] for i in range(3)]
        assert tr(mm(mm(sensor, J), sensor_inverse)) == tr(J)
        jacobians.append(J)
    trace_sum = sum(map(tr, jacobians))
    assert trace_sum == 2 * g * g * tr(alpha) / mass == 81
    # Rotation between probes can conceal a 2% cavity. Units: epsilon0*V=1.
    # A prolate ellipsoid with depolarization factors (2/5,2/5,1/5)
    # has response eigenvalues (5/2,5/2,5); the long-axis factor 1/5
    # occurs at a finite aspect ratio by continuity of the prolate formula.
    eigs = [F(5, 2), F(5, 2), F(5)]
    assert sum(1 / x for x in eigs) == 1
    # Each gradient's null direction sees 4.1, with long-axis cosine 4/5.
    null_response = F(41, 10)
    assert min(eigs) < null_response < max(eigs)
    assert (null_response - min(eigs)) / (max(eigs) - min(eigs)) == F(16, 25)
    frozen_trace = sum(eigs)
    apparent_trace = F(3, 2) * (frozen_trace - null_response)
    true_phi = F(1, 50)
    normalized_response = apparent_trace / (1 - true_phi)
    apparent_phi_bound = 1 - 9 / normalized_response
    assert apparent_phi_bound == F(1, 295) < cutoff < true_phi
    return {
        "ideal_bath_cut_kg_m3": bath,
        "bad_grain_phi": bad_phi,
        "bad_grain_density_kg_m3": bad_rho,
        "two_grain_aggregate_density_kg_m3": aggregate_rho,
        "two_fluid_same_outputs": outputs,
        "fixed_orientation_affine_trace_sum": trace_sum,
        "rotation_counterexample_true_phi": true_phi,
        "rotation_counterexample_apparent_phi_bound": apparent_phi_bound,
        "scope": "Exact ideal algebra, not an acquired sensor or calibrated particle class",
    }


def model_scales():
    d, rho, bath = 30e-6, 2700.0, 2673.0
    temperature, kb, gravity = 298.15, 1.380649e-23, 9.80665
    rows = []
    for mu in [0.001, 0.01, 0.1]:
        drag = 3 * math.pi * mu * d
        D = kb * temperature / drag
        for phi in [0.0, 0.005, 0.0099, 0.01, 0.015]:
            delta_rho = rho * (1 - phi) - bath
            speed = gravity * d * d * delta_rho / (18 * mu)
            rows.append({
                "assumed_viscosity_Pa_s": mu,
                "phi": phi,
                "density_margin_kg_m3": delta_rho,
                "Stokes_terminal_speed_um_s": speed * 1e6,
                "one_mm_drift_seconds": 1e-3 / speed if speed > 0 else None,
                "Brownian_D_m2_s": D,
                "Brownian_sd_after_60s_um": math.sqrt(2 * D * 60) * 1e6,
            })
    # Explicit invalid observation contracts: startup and common fluid flow.
    bad_terminal_speed, startup_speed, tau, time = -1.0, 10.0, 1.0, 0.5
    startup_observed = bad_terminal_speed + (startup_speed - bad_terminal_speed) * math.exp(-time / tau)
    flow_observed = 2.0 + bad_terminal_speed
    assert startup_observed > 0 and flow_observed > 0
    eps0, g = 8.8541878128e-12, 1e9
    alpha_over_mass = 3 * eps0 / rho
    stiffness_trace_sum = 6 * g * g * alpha_over_mass
    f0 = 100.0
    changed_frequency = math.sqrt((2 * math.pi * f0) ** 2 - g * g * alpha_over_mass) / (2 * math.pi)
    return {
        "all_scales_assumed_not_measured": True,
        "diameter_m": d,
        "rho_s_kg_m3": rho,
        "rho_bath_kg_m3": bath,
        "sphere_drag_and_Einstein_diffusion_only": rows,
        "bad_particle_downward_startup_speed_arbitrary_units": startup_observed,
        "bad_particle_downward_lab_speed_with_fluid_flow": flow_observed,
        "quadrupole_g_V_m2": g,
        "quadrupole_sum_acceleration_jacobian_trace_s2": stiffness_trace_sum,
        "one_axis_100Hz_baseline_frequency_shift_Hz": changed_frequency - f0,
        "limits": "No measured Al bath viscosity, flow, surface preservation, per-particle density, shape drag, or uncertainty coverage is supplied",
    }


def encode(x):
    if isinstance(x, F):
        return {"exact": str(x), "float": float(x)}
    raise TypeError(type(x).__name__)


if __name__ == "__main__":
    out = {"exact_checks": exact_checks(), "assumed_scales": model_scales()}
    path = Path(__file__).with_name("powder_density_gate_results.json")
    path.write_text(json.dumps(out, default=encode, indent=2) + "\n")
    print("PASS: exact gate, aggregate, wetting-alias, affine-Jacobian and rotation checks")
    print("Assumed scale calculations saved; no experimental result")
