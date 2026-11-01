"""Reproducible algebra checks for a finite dirty mediator comparator.

These checks do not simulate or certify an error-correction threshold.  They
verify the exact gate, the consumed-CNOT branch corrections, and two limits
used in the accompanying report.  Requires numpy and scipy.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
P1 = (I - Z) / 2
PAULIS = {"I": I, "X": X, "Y": Y, "Z": Z}


def kron(*factors):
    answer = np.array([[1.0 + 0.0j]])
    for factor in factors:
        answer = np.kron(answer, factor)
    return answer


def embed(operator, wire, n=3):
    factors = [I] * n
    factors[wire] = operator
    return kron(*factors)


def controlled(operator, control, target, n=3):
    return np.eye(2**n) + embed(P1, control, n) @ (
        embed(operator, target, n) - np.eye(2**n)
    )


def ordered_product(gates):
    answer = np.eye(gates[0].shape[0], dtype=complex)
    for gate in gates:
        answer = gate @ answer
    return answer


def opnorm(matrix):
    return float(np.linalg.norm(matrix, 2))


def pauli_description(operator):
    terms = []
    for labels in itertools.product(PAULIS, repeat=3):
        basis = kron(*(PAULIS[label] for label in labels))
        coefficient = np.trace(basis.conj().T @ operator) / 8
        if abs(coefficient) > 1e-10:
            terms.append({
                "pauli_ABM": "".join(labels),
                "real": float(coefficient.real),
                "imag": float(coefficient.imag),
            })
    return terms


def main():
    # Wire order A, B, M.  Gates are listed in chronological order.
    cx_am = controlled(X, 0, 2)
    cz_bm = controlled(Z, 1, 2)
    gates = [cx_am, cz_bm, cx_am, cz_bm]
    loop = ordered_product(gates)
    target = controlled(Z, 0, 1)
    result = {"dirty_loop_operator_residual": opnorm(loop - target)}

    # Any M-reference entanglement is covered by the operator identity.  An
    # explicit reference check guards the tensor ordering in this script.
    rng = np.random.default_rng(20261031)
    psi = rng.normal(size=16) + 1j * rng.normal(size=16)
    psi /= np.linalg.norm(psi)
    result["entangled_reference_vector_residual"] = float(
        np.linalg.norm(kron(loop, I) @ psi - kron(target, I) @ psi)
    )

    # Equal-component-count parity comparator.  Wire order D1,D2,A,M.
    # The first two and middle two CX operations commute and can be paired
    # into simultaneous stages if the hardware supports both couplings.
    fused_gates = [controlled(X, 0, 3, n=4),
                   controlled(X, 1, 3, n=4),
                   controlled(Z, 2, 3, n=4),
                   controlled(X, 1, 3, n=4),
                   controlled(X, 0, 3, n=4),
                   controlled(Z, 2, 3, n=4)]
    fused = ordered_product(fused_gates)
    fused_target = controlled(Z, 2, 0, n=4) @ controlled(Z, 2, 1, n=4)
    result["fused_parity_dirty_loop_residual"] = opnorm(fused - fused_target)

    # A mediator Pauli at a primitive boundary does not affect data.  A Pauli
    # inserted inside a primitive can affect the current A,B pair.  Complete
    # subsequent ideal primitives still act as identity on this dirty M.
    fault_table = []
    for completed in range(5):
        for name in ("X", "Y", "Z"):
            faulty = np.eye(8, dtype=complex)
            for j, gate in enumerate(gates):
                if j == completed:
                    faulty = embed(PAULIS[name], 2) @ faulty
                faulty = gate @ faulty
            if completed == 4:
                faulty = embed(PAULIS[name], 2) @ faulty
            boundary_error = faulty @ loop.conj().T
            fault_table.append({
                "completed_elementary_gates": completed,
                "mediator_fault": name,
                "effective_output_error": pauli_description(boundary_error),
            })
    result["fault_table"] = fault_table

    # Bounded controlled-Pauli generators, tau=1.
    h_x = np.pi / 2 * embed(P1, 0) @ (np.eye(8) - embed(X, 2))
    h_z = np.pi / 2 * embed(P1, 1) @ (np.eye(8) - embed(Z, 2))
    result["hamiltonian_gate_checks"] = {
        "CX_residual": opnorm(expm(-1j * h_x) - cx_am),
        "CZ_residual": opnorm(expm(-1j * h_z) - cz_bm),
        "generator_norm": opnorm(h_x),
    }
    calibration = []
    for delta in (1e-6, 1e-4, 1e-2, 0.1):
        noisy = ordered_product([
            expm(-1j * (1 + delta) * h_x),
            expm(-1j * (1 + delta) * h_z),
            expm(-1j * (1 + delta) * h_x),
            expm(-1j * (1 + delta) * h_z),
        ])
        calibration.append({
            "relative_angle_error": delta,
            "operator_distance": opnorm(noisy - loop),
            "state_uniform_upper_bound": min(2.0, 4 * np.pi * abs(delta)),
        })
    result["bounded_mediator_calibration"] = calibration

    # Consumed ancilla CNOT.  Input order C,T; internal order C,A,T.
    plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
    preparation = np.zeros((8, 4), dtype=complex)
    for c, t in itertools.product(range(2), repeat=2):
        for a in range(2):
            preparation[4 * c + 2 * a + t, 2 * c + t] = plus[a]
    zz_ca = kron(Z, Z, I)
    xx_at = kron(I, X, X)
    desired_cnot = controlled(X, 0, 1, n=2)
    branches = []
    total_effect = np.zeros((4, 4), dtype=complex)
    for mzz, mxx, mza in itertools.product(range(2), repeat=3):
        select = np.zeros((4, 8), dtype=complex)
        for c, t in itertools.product(range(2), repeat=2):
            select[2 * c + t, 4 * c + 2 * mza + t] = 1
        k = select @ ((np.eye(8) + (-1)**mxx * xx_at) / 2) @ (
            (np.eye(8) + (-1)**mzz * zz_ca) / 2
        ) @ preparation
        frame = kron(np.linalg.matrix_power(Z, mxx),
                     np.linalg.matrix_power(X, mzz ^ mza))
        corrected = frame @ k
        amplitude = np.trace(desired_cnot.conj().T @ corrected) / 4
        branches.append({
            "mZZ_mXX_mZA": [mzz, mxx, mza],
            "corrected_CNOT_residual": opnorm(corrected - amplitude * desired_cnot),
            "branch_probability": float(abs(amplitude)**2),
            "global_amplitude_real": float(amplitude.real),
        })
        total_effect += k.conj().T @ k
    result["consumed_CNOT_branches"] = branches
    result["consumed_CNOT_completeness_residual"] = opnorm(total_effect - np.eye(4))

    # Differential residual displacement beta in a centered thermal mode.
    # Characteristic function is exp[-(nbar+1/2)|beta|^2]; reduced data sees
    # dephasing with pZ=(1-characteristic)/2.
    beta = 1e-3
    result["hot_bus_nonuniform_calibration"] = [
        {"residual_displacement": beta, "nbar": nbar,
         "dephasing_probability": float(-np.expm1(-(nbar + 0.5) * beta**2) / 2)}
        for nbar in (0, 1e2, 1e4, 1e6, 1e8)
    ]

    # An old correctable error plus a fresh error is not a clean-input test.
    state_after_late_fault = [1, 0, 0]
    state_after_next_fault = [1, 1, 0]
    majority = int(sum(state_after_next_fault) >= 2)
    result["survivor_counterexample_repetition_code"] = {
        "late_fault_after_cycle_recovery": state_after_late_fault,
        "fresh_fault_before_next_recovery": state_after_next_fault,
        "majority_recovery_output": [majority] * 3,
        "logical_failure": majority == 1,
        "purpose": "Minimal deterministic illustration of shared error budget, not a quantum-code threshold.",
    }

    assert result["dirty_loop_operator_residual"] < 1e-12
    assert result["fused_parity_dirty_loop_residual"] < 1e-12
    assert result["entangled_reference_vector_residual"] < 1e-12
    assert all(b["corrected_CNOT_residual"] < 1e-12 for b in branches)
    assert result["consumed_CNOT_completeness_residual"] < 1e-12
    assert all(row["operator_distance"] <= row["state_uniform_upper_bound"] + 1e-12
               for row in calibration)

    output = Path(__file__).with_name("verification_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "output": str(output),
        "dirty_loop_residual": result["dirty_loop_operator_residual"],
        "fused_parity_loop_residual": result["fused_parity_dirty_loop_residual"],
        "max_CNOT_branch_residual": max(b["corrected_CNOT_residual"] for b in branches),
        "completeness_residual": result["consumed_CNOT_completeness_residual"],
    }, indent=2))


if __name__ == "__main__":
    main()
