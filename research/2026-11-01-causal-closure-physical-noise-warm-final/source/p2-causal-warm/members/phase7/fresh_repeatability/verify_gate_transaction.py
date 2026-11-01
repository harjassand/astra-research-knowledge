"""Exact discrete transaction checks and finite-ramp linear-response audit.

The bosonic whole-space identity is analytic in gate_transaction_addendum.md;
no truncated Fock matrix is used to assert that identity.
"""
from itertools import product
from pathlib import Path
import importlib.util
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.special import erfc

HERE = Path(__file__).resolve().parent
receiver_path = HERE.parent / "persistent_faults" / "check_persistent_receiver.py"
spec = importlib.util.spec_from_file_location("receiver", receiver_path)
receiver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receiver)

z = np.array([1, -1])
z1 = np.kron(z, np.ones(2))
z2 = np.kron(np.ones(2), z)
loop = np.diag(np.exp(1j * np.pi / 4 * (z1 + z1 * z2)))
Z1 = np.diag(z1)
S2 = np.diag([1, 1j, 1, 1j])
CZ = np.diag([1, 1, 1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
H2 = np.kron(np.eye(2), H)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                 [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
cz_error = float(np.linalg.norm(Z1 @ S2 @ loop - 1j * CZ, 2))
cnot_error = float(np.linalg.norm(Z1 @ H2 @ S2 @ loop @ H2 - 1j * CNOT, 2))
assert cz_error < 1e-14 and cnot_error < 1e-14

# Units: g=1.  Linear ramps of duration 0.1; positive chi only.
chi_max = 2.0
ramp = 0.1
duration = 2 * np.pi / chi_max + ramp


def chi(t):
    if t < ramp:
        return chi_max * t / ramp
    if t <= duration - ramp:
        return chi_max
    return chi_max * (duration - t) / ramp


def theta(t):
    if t < ramp:
        return chi_max * t * t / (2 * ramp)
    if t <= duration - ramp:
        return chi_max * (t - ramp / 2)
    return 2 * np.pi - chi_max * (duration - t)**2 / (2 * ramp)


def integrate_real(f):
    points = [0, ramp, duration - ramp, duration]
    return sum(quad(f, a, b, epsabs=1e-12, epsrel=1e-12)[0]
               for a, b in zip(points[:-1], points[1:]))


area = integrate_real(chi)
closures = []
for kappa in [0.0, 0.01, 0.2]:
    attenuation = np.exp(-kappa * duration / 2)
    magnus_phase = integrate_real(lambda t: chi(t) * np.exp(-kappa * t)
                                 * (1 - np.cos(theta(t))))
    for q1, q2 in product([-1, 1], repeat=2):
        force = (1 + q2) / 4
        integral = integrate_real(lambda t: chi(t) * np.cos(q1 * theta(t)))
        integral += 1j * integrate_real(lambda t: chi(t) * np.sin(q1 * theta(t)))
        displacement = -1j * force * attenuation * integral
        passive = attenuation * np.exp(-1j * q1 * area)
        assert abs(displacement) < 1e-11
        assert abs(passive - attenuation) < 1e-11
        closures.append({"kappa": kappa, "z1": q1, "z2": q2,
                         "closure_displacement_abs": float(abs(displacement)),
                         "passive_factor": float(attenuation),
                         "drive_magnus_phase_coefficient": float(magnus_phase)})

# CNOT propagation of row/column parities.  Faults on a physical interblock
# pair can have independent Pauli components in its two blocks, but share
# the row (for X components) and column (for Z components).
n = 7
one = [0] + [1 << k for k in range(n)]
input_components = [(a, b) for a in one for b in one]
propagation_cases = 0
max_x = [0, 0]
max_z = [0, 0]
for a, b in input_components:
    for k in range(n):
        for fa, fb in product([0, 1 << k], repeat=2):
            xa, xb = a ^ fa, a ^ b ^ fb
            za, zb = a ^ b ^ fa, b ^ fb
            assert max(xa.bit_count(), xb.bit_count(),
                       za.bit_count(), zb.bit_count()) <= 3
            max_x = [max(max_x[0], xa.bit_count()), max(max_x[1], xb.bit_count())]
            max_z = [max(max_z[0], za.bit_count()), max(max_z[1], zb.bit_count())]
            for value in [xa, xb, za, zb]:
                assert value ^ receiver.correction(receiver.syndrome(value, n), n) == 0
            propagation_cases += 1

# The actual two-identical-full-vectors/cap-four receiver, now with arbitrary
# incoming weight <=2 from two prior blocks, not only old weight <=1.
initial = [v for v in range(1 << n) if v.bit_count() <= 2]
temporal_cases = 0
max_rounds = 0
for old, flip, fault_round, report in product(initial, one, range(1, 5), range(1 << (n - 1))):
    out = receiver.temporal_recovery(n, old, flip, fault_round, report)
    assert not out["flag"]
    assert out["residual"] in (0, flip)
    max_rounds = max(max_rounds, out["rounds"])
    temporal_cases += 1


def preparation_module_orientation(size=7):
    """One directed 4-cycle plus a forest directed toward that cycle.

    Source = dispersive participant; target's conditioned force is off
    during single-qubit preparation/readout.  No new edges are introduced.
    """
    edges = set()
    for row in range(size):
        for col in range(size):
            if col + 1 < size:
                edges.add(tuple(sorted(((row, col), (row, col + 1)))))
            if row + 1 < size:
                edges.add(tuple(sorted(((row, col), (row + 1, col)))))
    cycle = [(0, 0), (0, 1), (1, 1), (1, 0)]
    next_cycle = {cycle[k]: cycle[(k + 1) % 4] for k in range(4)}
    chosen = {}
    for row in range(size):
        for col in range(size):
            source = (row, col)
            if source in next_cycle:
                target = next_cycle[source]
            elif row >= 2:
                target = (row - 1, col)
            else:
                target = (row, col - 1)
            key = tuple(sorted((source, target)))
            assert key in edges and key not in chosen
            chosen[key] = (source, target)
    assert len(chosen) == size * size
    assignment = []
    for module_id, key in enumerate(sorted(edges)):
        source, target = chosen.get(key, key)
        assignment.append({"module_id": module_id, "dispersive_source": source,
                           "conditional_force_target": target,
                           "selected_for_single_qubit_preparation_and_readout": key in chosen})
    selected = [m for m in assignment if m["selected_for_single_qubit_preparation_and_readout"]]
    assert {m["dispersive_source"] for m in selected} == {
        (r, c) for r in range(size) for c in range(size)}
    assert len({m["module_id"] for m in selected}) == size * size
    return assignment


orientation = preparation_module_orientation()
(HERE / "preparation_module_assignment.json").write_text(json.dumps(orientation, indent=2) + "\n")

# For symmetric pure coherent pointers +/- beta and a threshold homodyne
# decision, this is the constant-weight projective GOOD component, not just
# the smaller raw misclassification tail.  The matrix inequality proves CP
# uniformly over arbitrary retained memory once the selected-pointer
# factorization has been earned by the physical receiver.
cp_examples = []
for beta in [0.1, 0.5, 1.0, 2.0]:
    classification_tail = float(0.5 * erfc(np.sqrt(2) * beta))
    cross_overlap = float(0.5 * np.exp(-2 * beta**2))
    bad_weight = classification_tail + cross_overlap**2 / classification_tail
    good_weight = 1 - bad_weight
    outcome_gram = np.array([[1 - classification_tail, cross_overlap],
                            [cross_overlap, classification_tail]])
    remainder = outcome_gram - np.diag([good_weight, 0])
    minimum_eigenvalue = float(np.linalg.eigvalsh(remainder)[0])
    assert 0 <= good_weight <= 1 and minimum_eigenvalue >= -1e-14
    cp_examples.append({"coherent_pointer_amplitude": beta,
                        "raw_classification_tail": classification_tail,
                        "CP_bad_component_weight": bad_weight,
                        "CP_good_projective_weight": good_weight,
                        "remainder_minimum_eigenvalue": minimum_eigenvalue})

result = {
    "CZ_identity_spectral_error": cz_error,
    "CNOT_identity_spectral_error": cnot_error,
    "positive_chi_ramp_duration_g_inverse": duration,
    "chi_area": area,
    "unconditional_drive_peak_in_g_units": chi_max / 4,
    "conditional_drive_peak_in_g_units": chi_max / 4,
    "total_branch_force_peak_in_g_units": chi_max / 2,
    "finite_loss_response_checks": closures,
    "CNOT_component_propagation_cases": propagation_cases,
    "max_X_row_weights_control_target_after_one_pair_fault": max_x,
    "max_Z_column_weights_control_target_after_one_pair_fault": max_z,
    "incoming_component_vectors_weight_at_most_two": len(initial),
    "temporal_receiver_histories_checked": temporal_cases,
    "temporal_receiver_max_snapshots": max_rounds,
    "temporal_receiver_failures": 0,
    "preparation_module_assignment": {
        "existing_gauge_modules_per_block": len(orientation),
        "selected_distinct_modules_per_block": sum(m["selected_for_single_qubit_preparation_and_readout"] for m in orientation),
        "every_qubit_is_a_selected_dispersive_source": True,
        "new_edges_or_apparatus_modes_required_by_this_orientation": 0,
        "unconditional_drive_upgrades_per_block": 49,
        "assignment_file": "preparation_module_assignment.json"
    },
    "pure_pointer_CP_decomposition_examples": cp_examples,
    "transaction_costs": {
        "data_qubits_two_blocks": 98,
        "physical_pair_loops": 49,
        "gate_target_Hadamards": 98,
        "gate_target_S_pulses": 49,
        "recovery_Hadamards_two_blocks": 196,
        "gauge_meter_uses_two_clean_recoveries": 336,
        "gauge_meter_uses_max_one_fresh_event_total": 420,
        "gauge_meter_uses_hard_cap_two_recoveries": 672,
        "dedicated_path_gauge_modules_two_blocks": 168,
        "additional_interblock_modules_if_dedicated": 49,
        "two_mode_apparatus_modes_if_all_217_modules_dedicated": 434,
        "serial_49_loop_mapping_time_only_g_inverse": float(49 * duration)
    },
    "preparation_and_readout_costs_per_block": {
        "single_qubit_measurement_reset_meter_calls": 49,
        "maximum_conditional_X_pulses_for_zero_preparation": 49,
        "additional_H_pulses_for_plus_preparation": 49,
        "encoded_zero_preparation_fault_free_total_meter_calls": 217,
        "encoded_zero_preparation_meter_calls_with_one_fresh_event_total": 301,
        "terminal_Z_meter_calls": 49,
        "terminal_X_additional_H_pulses": 49,
        "additional_modules_with_oriented_existing_grid": 0,
        "dedicated_additional_modules_if_grid_sources_unavailable": 49
    },
    "scope": "Conditional deterministic gate/recovery checks, not a physical error-rate or threshold estimate. Gate locality, finite-memory receiver contract, controller reliability, and imperfect isolation remain explicit physical requirements."
}
(HERE / "gate_transaction_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "finite_loss_response_checks"}, indent=2))
