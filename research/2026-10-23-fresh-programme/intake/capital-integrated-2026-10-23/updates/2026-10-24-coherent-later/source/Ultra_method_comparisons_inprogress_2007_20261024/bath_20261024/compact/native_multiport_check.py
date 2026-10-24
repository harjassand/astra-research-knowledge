#!/usr/bin/env python3
"""Finite native-collision dilation for the compact bath-access construction.

Only numpy and the standard library are needed.  This is a model calculation,
not acquired mechanical hardware data.  No peer-arm files are read.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np


def pulse(t, gamma, kappa, amplitude=1.0):
    # u = sin(t/2)^6, with endpoint derivatives through third order zero.
    terms = [(0, 10 / 32), (1, -15 / 32), (2, 6 / 32), (3, -1 / 32)]
    deriv = []
    for order in range(5):
        value = 0.0
        for frequency, coefficient in terms:
            if frequency == 0:
                value += coefficient if order == 0 else 0.0
            else:
                value += coefficient * frequency**order * math.cos(
                    frequency * t + order * math.pi / 2
                )
        deriv.append(amplitude * value)
    u, du, ddu, d3u, d4u = deriv
    z = 1 + gamma * gamma / 4
    d = ddu + gamma * du + z * u
    force = d4u + 2 * gamma * d3u + (2 * z + gamma**2) * ddu
    force += 2 * gamma * z * du + (z * z - kappa * kappa) * u
    return u, d, -kappa * u, force


def mechanical_flow(t, kappa):
    # Coordinates [QA,PA,QB,PB], m=hbar=omega=1.
    normal = np.array(
        [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, -1, 0], [0, 1, 0, -1]]
    ) / math.sqrt(2)
    blocks = np.zeros((4, 4))
    for start, frequency in [(0, math.sqrt(1 + kappa)), (2, math.sqrt(1 - kappa))]:
        c, s = math.cos(frequency * t), math.sin(frequency * t)
        blocks[start : start + 2, start : start + 2] = [
            [c, s / frequency], [-frequency * s, c]
        ]
    return normal.T @ blocks @ normal


def make_dilation(bins, gamma, kappa):
    duration = 2 * math.pi
    dt = duration / bins
    flow = mechanical_flow(dt / 2, kappa)
    drift = np.array(
        [[0, 1, 0, 0], [-1, 0, -kappa, 0], [0, 0, 0, 1], [-kappa, 0, -1, 0]],
        dtype=float,
    )
    force_basis = np.array([[0, 0], [1, 0], [0, 0], [0, 1]], dtype=float)
    integral_flow = np.linalg.solve(drift, flow - np.eye(4))
    double_integral = np.linalg.solve(drift, integral_flow - dt / 2 * np.eye(4))
    affine = integral_flow @ force_basis
    transmission = math.exp(-gamma * dt / 2)
    reflection = math.sqrt(-math.expm1(-gamma * dt))
    initial_dim = 4 + 4 * bins
    system = np.zeros((4, initial_dim))
    system[:, :4] = np.eye(4)
    outputs = np.zeros((4 * bins, initial_dim))
    response = np.zeros((4, 2))
    output_response = np.zeros((4 * bins, 2))
    raw_phase = 0.0

    def half_step(state_response, force):
        nonlocal raw_phase
        response_integral = integral_flow @ state_response
        response_integral += double_integral @ force_basis * force
        raw_phase += force / 2 * (response_integral[0, 1] + response_integral[2, 0])
        return flow @ state_response + affine * force

    for index in range(bins):
        _, _, _, force = pulse((index + 0.5) * dt, gamma, kappa)
        system = flow @ system
        response = half_step(response, force)
        selector = np.zeros_like(system)
        selector[:, 4 + 4 * index : 8 + 4 * index] = np.eye(4)
        outputs[4 * index : 4 * index + 4] = transmission * selector - reflection * system
        output_response[4 * index : 4 * index + 4] = -reflection * response
        system = transmission * system + reflection * selector
        response *= transmission
        system = flow @ system
        response = half_step(response, force)

    q, c, p = (np.zeros(bins) for _ in range(3))
    aligned_p = np.zeros((2 * bins, 4 * bins))
    branch_generator = np.zeros((2, 4 * bins))
    symmetry_error = 0.0
    for index in range(bins):
        self_vector = output_response[4 * index : 4 * index + 2, 0]
        cross_vector = output_response[4 * index : 4 * index + 2, 1]
        q[index] = np.linalg.norm(self_vector)
        q_axis = self_vector / q[index]
        p_axis = np.array([-q_axis[1], q_axis[0]])
        c[index], p[index] = q_axis @ cross_vector, p_axis @ cross_vector
        symmetry_error = max(
            symmetry_error,
            float(np.max(np.abs(output_response[4 * index + 2 : 4 * index + 4, 1] - self_vector))),
            float(np.max(np.abs(output_response[4 * index + 2 : 4 * index + 4, 0] - cross_vector))),
        )
        for site in range(2):
            loc = slice(4 * index + 2 * site, 4 * index + 2 * site + 2)
            aligned_p[site * bins + index, loc] = p_axis
            branch_generator[site, loc] += q[index] * p_axis
            branch_generator[1 - site, loc] += c[index] * p_axis - p[index] * q_axis

    # Canonical row check for all generated output modes and final mechanics.
    omega4 = np.kron(np.eye(2), np.array([[0, 1], [-1, 0]]))
    final = np.vstack([system, outputs])
    omega_all = np.kron(np.eye(2 + 2 * bins), np.array([[0, 1], [-1, 0]]))
    # Fast symplectic product without dense omega @ matrix multiplication.
    rotated = np.empty_like(final)
    rotated[:, 0::2] = -final[:, 1::2]
    rotated[:, 1::2] = final[:, 0::2]
    commutator_error = float(np.max(np.abs(rotated @ final.T - omega_all)))
    return {
        "bins": bins, "gamma": gamma, "kappa": kappa,
        "outputs": outputs, "aligned_p": aligned_p, "generator": branch_generator,
        "q": q, "c": c, "p": p, "raw_phase": raw_phase,
        "closure_error": float(np.max(np.abs(response))),
        "symmetry_error": symmetry_error, "commutator_error": commutator_error,
        "phase_ideal": raw_phase + float(q @ p),
        "cross_norm2": float(c @ c + p @ p),
        "own_norm2": float(q @ q),
    }


def evaluate(model, f, eta, bath_v, mechanical_v, dark_v, strategy, temporal_basis=None):
    outputs, bins = model["outputs"], model["bins"]
    initial_variances = np.full(outputs.shape[1], bath_v)
    initial_variances[:4] = mechanical_v
    vb = (outputs * initial_variances) @ outputs.T
    yy, ll = model["aligned_p"], model["generator"]
    detector_noise = (1 - eta) / (2 * eta)
    if strategy == "none":
        gain = np.zeros(bins)
    elif strategy == "bright_cancel":
        gain = model["q"] / math.sqrt(f)
    elif strategy in ("wiener_local", "wiener_fixed_phase"):
        y_local = yy[:bins]
        record_covariance = f * y_local @ vb @ y_local.T
        record_covariance += ((1 - f) * dark_v + detector_noise) * np.eye(bins)
        cross = math.sqrt(f) * y_local @ vb @ ll[0]
        if temporal_basis is None:
            gain = np.linalg.solve(record_covariance, cross)
        else:
            basis = temporal_basis
            gain = basis @ np.linalg.solve(basis.T @ record_covariance @ basis, basis.T @ cross)
        if strategy == "wiener_fixed_phase":
            constraint = math.sqrt(f) * model["p"]
            desired = float(model["q"] @ model["p"])
            adjustment = np.linalg.solve(record_covariance, constraint)
            gain += adjustment * (desired - constraint @ gain) / (constraint @ adjustment)
    else:
        raise ValueError(strategy)
    residual = ll.copy()
    residual[0] -= math.sqrt(f) * gain @ yy[:bins]
    residual[1] -= math.sqrt(f) * gain @ yy[bins:]
    covariance = residual @ vb @ residual.T
    added = ((1 - f) * dark_v + detector_noise) * float(gain @ gain)
    covariance += added * np.eye(2)
    phase = model["raw_phase"] + math.sqrt(f) * float(gain @ model["p"])
    # For +/-1 spin labels, a single flip has Delta s=2, exponent=2 Var(G).
    return {
        "f": f, "eta": eta, "bath_v": bath_v, "mechanical_v": mechanical_v,
        "dark_v": dark_v, "strategy": strategy, "theta": phase,
        "phase_fraction_of_full_erasure": phase / model["phase_ideal"],
        "residual_phase_covariance": covariance.tolist(),
        "single_flip_exponent": float(2 * covariance[0, 0]),
        "single_flip_exponent_at_abs_theta_pi_over_4": float(2 * covariance[0, 0] * (math.pi / 4) / abs(phase)),
        "dark_and_detector_variance": added,
        "gain_norm2": float(gain @ gain),
    }


def scalar_tests():
    out = []
    for f in [0.01, 0.25, 0.9]:
        for v in [0.5, 10.5, 1000.5, 1000000.5]:
            for dark_v, name in [(v, "native_hot"), (0.5, "vacuum_downstream")]:
                g = math.sqrt(f) * v / (f * v + (1 - f) * dark_v)
                direct = v * (1 - math.sqrt(f) * g) ** 2 + (1 - f) * dark_v * g * g
                closed = v * (1 - f) * dark_v / (f * v + (1 - f) * dark_v)
                assert abs(direct - closed) < 1e-8 * max(1, closed)
                out.append({"f": f, "v_bright": v, "topology": name, "optimized_variance_q1": closed})
    return out


def tapped_dark_variance(v, tap_fraction):
    """Actual input tap, not a freely supplied correlated reference.

    D_t = sqrt(1-r) D + sqrt(r) vacuum is sent into the native dark input.
    R = sqrt(r) D - sqrt(1-r) vacuum is homodyned ideally.
    Their covariance determinant is v/2.
    """
    r = tap_fraction
    transmitted = (1 - r) * v + r / 2
    reference = r * v + (1 - r) / 2
    cross = math.sqrt(r * (1 - r)) * (v - 0.5)
    conditional = v / (2 * reference)
    assert abs(transmitted - cross * cross / reference - conditional) < 1e-7 * max(1, conditional)
    return conditional


def continuum_values(gamma, kappa):
    a0 = 10 / 32
    harmonics = [(1, -15 / 32), (2, 6 / 32), (3, -1 / 32)]
    z = 1 + gamma * gamma / 4
    iu2 = 2 * math.pi * a0 * a0 + math.pi * sum(a * a for _, a in harmonics)
    idu2 = math.pi * sum(l * l * a * a for l, a in harmonics)
    id2 = 2 * math.pi * (z * a0) ** 2
    id2 += math.pi * sum(a * a * ((z - l * l)**2 + gamma * gamma * l * l) for l, a in harmonics)
    ip2 = 2 * math.pi * (gamma * z * a0 / 2)**2
    ip2 += math.pi * sum(
        a * a * ((gamma * (z - 3 * l * l) / 2)**2 + (l * (z - l * l + gamma * gamma / 2))**2)
        for l, a in harmonics
    )
    phase = -kappa * (id2 - kappa * kappa * iu2)
    return {
        "phase_ideal": phase,
        "raw_phase": phase + 2 * kappa * gamma * gamma * idu2,
        "feedback_phase": -2 * kappa * gamma * gamma * idu2,
        "own_norm2": gamma * (id2 + ip2),
        "cross_norm2": gamma * kappa * kappa * ((1 + gamma * gamma / 4) * iu2 + idu2),
    }


def spin_channel_metrics(theta, phase_covariance):
    labels = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
    zz = labels[:, 0] * labels[:, 1]
    delta = labels[:, None, :] - labels[None, :, :]
    exponents = np.einsum("ijk,kl,ijl->ij", delta, phase_covariance, delta) / 2
    rho = np.exp(1j * theta * (zz[:, None] - zz[None, :]) - exponents) / 4
    partial_transpose = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    minimum = float(np.linalg.eigvalsh(partial_transpose)[0])
    negativity = float(np.maximum(-np.linalg.eigvalsh(partial_transpose), 0).sum())
    target = np.exp(1j * theta * zz) / 2
    return {
        "theta": theta,
        "minimum_partial_transpose_eigenvalue": minimum,
        "negativity": negativity,
        "fidelity_to_same_theta_ideal_state": float(np.vdot(target, rho @ target).real),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bins", type=int, default=160)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("native_multiport_data.json"))
    args = parser.parse_args()
    models = [make_dilation(n, 0.08, 0.01) for n in [args.bins // 2, args.bins]]
    for model in models:
        assert model["symmetry_error"] < 1e-10
        assert model["commutator_error"] < 1e-10
    model = models[-1]
    cases = []
    for hot_v in [0.5, 10.5, 1000.5]:
        for f, dark_v, topology in [(0.25, hot_v, "partial_native"), (0.25, 0.5, "true_vacuum_mixing"), (1.0, hot_v, "bright_collected")]:
            for strategy in ["none", "bright_cancel", "wiener_local", "wiener_fixed_phase"]:
                result = evaluate(model, f, 0.9, hot_v, hot_v, dark_v, strategy)
                result["topology"] = topology
                cases.append(result)
    # Cold bath comparator preserves the initially hot mechanical state.
    cases.append({"topology": "cold_native_inputs_hot_initial_mechanics", **evaluate(model, 0.25, 0.9, 0.5, 1000.5, 0.5, "wiener_local")})
    reference_cases = []
    for hot_v in [10.5, 1000.5, 1000000.5]:
        for tap_fraction in [0.01, 0.1, 1.0]:
            effective_dark_v = tapped_dark_variance(hot_v, tap_fraction)
            reference_cases.append({
                "tap_fraction": tap_fraction,
                "original_dark_v": hot_v,
                "conditional_dark_v": effective_dark_v,
                "hot_limit_conditional_dark_v": 1 / (2 * tap_fraction),
                "declared_resource": "passive native bright/dark INPUT rotation, tap into independent vacuum, ideal homodyne of tap, local reference subtraction",
                **evaluate(model, 0.25, 0.9, hot_v, hot_v, effective_dark_v, "bright_cancel"),
            })
    temporal_mode_cases = []
    n = model["bins"]
    for basis_name, basis in [
        ("one_boxcar_mode", np.ones((n, 1)) / math.sqrt(n)),
        ("one_self_response_matched_mode", model["q"].reshape(n, 1) / np.linalg.norm(model["q"])),
    ]:
        result = evaluate(model, 1.0, 1.0, 1000.5, 1000.5, 1000.5, "wiener_local", basis)
        result["available_temporal_basis"] = basis_name
        result["self_displacement_projection_fraction"] = float(np.linalg.norm(basis.T @ model["q"])**2 / model["own_norm2"])
        temporal_mode_cases.append(result)
    assert abs(spin_channel_metrics(math.pi / 4, np.zeros((2, 2)))["negativity"] - 0.5) < 1e-12
    assert spin_channel_metrics(0, np.zeros((2, 2)))["negativity"] < 1e-12
    entanglement_examples = []
    for f in [1.0, 0.999, 0.99, 0.25]:
        for strategy in ["bright_cancel", "wiener_local", "wiener_fixed_phase"]:
            raw = evaluate(model, f, 0.9999, 10.5, 10.5, 10.5, strategy)
            scale = (math.pi / 4) / abs(raw["theta"])
            covariance = np.array(raw["residual_phase_covariance"]) * scale
            target_theta = math.copysign(math.pi / 4, raw["theta"])
            entanglement_examples.append({
                "f_native_signal": f,
                "eta_detector": 0.9999,
                "thermal_v": 10.5,
                "strategy": strategy,
                "pulse_amplitude_for_actual_theta": math.sqrt(scale),
                "phase_covariance_at_actual_target": covariance.tolist(),
                **spin_channel_metrics(target_theta, covariance),
            })
    # Full erasure leaves only cross-response bath scaling and vacuum detector noise.
    header = [{key: value for key, value in m.items() if not isinstance(value, np.ndarray)} for m in models]
    continuum = continuum_values(model["gamma"], model["kappa"])
    data = {"model": "finite Strang mechanical Hamiltonian / exact thermal beam-splitter collision dilation; two independent native inputs, bright/dark rotation", "units": "m=hbar=omega=1", "not_hardware": True, "continuum_analytic": continuum, "convergence": header, "scalar_checks": scalar_tests(), "cases": cases, "paid_reference_cases": reference_cases, "temporal_mode_cases": temporal_mode_cases, "entanglement_examples_at_actual_target_phase": entanglement_examples}
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "convergence": header}, indent=2))
    for result in cases:
        if result["bath_v"] == 1000.5:
            print(f'{result["topology"]:24s} {result["strategy"]:20s} D1={result["single_flip_exponent"]:.8g} theta={result["theta"]:.8g}')


if __name__ == "__main__":
    main()
