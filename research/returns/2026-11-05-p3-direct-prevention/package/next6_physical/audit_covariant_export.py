#!/usr/bin/env python3
"""Finite mathematical diagnostics for the retained-output averaging theorem.

No device, pure Markov reservoir, bounded receiver, or calibration experiment is
simulated.  The full-output check is on a finite pure collision dilation.  It
computes normalized Choi trace norm (a lower bound on diamond distance), not an
unlabelled substitute for a diamond norm or an interval proof.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
import scipy
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULIS = [I, X, Y, Z]


def kron_all(matrices):
    ans = np.array([[1]], dtype=complex)
    for matrix in matrices:
        ans = np.kron(ans, matrix)
    return ans


def swap_matrix(qubits, a, b):
    dimension = 1 << qubits
    out = np.zeros((dimension, dimension), dtype=complex)
    for j in range(dimension):
        abit = (j >> (qubits - 1 - a)) & 1
        bbit = (j >> (qubits - 1 - b)) & 1
        k = j
        if abit != bbit:
            k ^= (1 << (qubits - 1 - a)) | (1 << (qubits - 1 - b))
        out[k, j] = 1
    return out


def signed_low_rank_trace_norm(columns, signs):
    """Trace norm of A diag(signs) A* through a small QR factor."""
    _, r = np.linalg.qr(np.column_stack(columns), mode="reduced")
    small = (r * np.asarray(signs)[None, :]) @ r.conj().T
    small = (small + small.conj().T) / 2
    return float(np.abs(np.linalg.eigvalsh(small)).sum())


def collision_case(n):
    d = 1 << n
    if n == 1:
        h = 0.7 * X + 0.31 * Z
        certified_norm_bound = 1.01
    elif n == 2:
        h = (0.7 * np.kron(X, I) + 0.31 * np.kron(I, Z)
             + 0.47 * np.kron(X, Y) + 0.19 * np.kron(Z, X))
        certified_norm_bound = 1.67
    else:
        raise ValueError("Only the explicitly declared finite instances run.")

    group = [kron_all(factors) for factors in itertools.product(PAULIS, repeat=n)]
    environment_dimension = d * d
    e0 = np.zeros(environment_dimension, dtype=complex)
    for a in range(d):
        e0[a * d + a] = 1 / math.sqrt(d)
    embedding = np.kron(np.eye(d), e0[:, None])
    full_dimension = d * environment_dimension
    collision_generator = sum(
        (swap_matrix(3 * n, i, n + i) for i in range(n)),
        np.zeros((full_dimension, full_dimension), dtype=complex),
    )
    rows = []
    for dwell in [0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625]:
        # Partial SWAP with a Bell-purified maximally mixed ancilla gives the
        # exact single-collision depolarizing reduced channel exp(-dwell) id
        # + (1-exp(-dwell)) D.  It is not asserted to be a continuous bath.
        theta = math.acos(math.exp(-dwell / 2))
        v0 = expm(-1j * theta * collision_generator) @ embedding
        choi0 = v0.reshape(-1, order="F") / math.sqrt(d)
        choi_columns = []
        keyed_choi_error = 0.0
        covariance_residual = 0.0
        original_v = expm(-1j * (theta * collision_generator
                          + dwell * np.kron(h, np.eye(environment_dimension)))) @ embedding
        for g in group:
            hg = g.conj().T @ h @ g
            vg = expm(-1j * (theta * collision_generator
                      + dwell * np.kron(hg, np.eye(environment_dimension)))) @ embedding
            # Explicit coherent environment correction: g* on the Bell partner
            # and g on the interacting ancilla, with a returned source frame.
            corrected_v = np.kron(g.conj().T, np.kron(g.conj().T, g.T)) @ original_v @ g
            covariance_residual = max(
                covariance_residual, float(np.linalg.norm(corrected_v - vg, 2))
            )
            choig = vg.reshape(-1, order="F") / math.sqrt(d)
            choi_columns.append(choig / math.sqrt(len(group)))
            overlap = float(abs(np.vdot(choi0, choig)) ** 2)
            keyed_choi_error += 2 * math.sqrt(max(0.0, 1.0 - overlap)) / len(group)
        averaged_error = signed_low_rank_trace_norm(
            choi_columns + [choi0], [1] * len(group) + [-1]
        )
        theorem_bound = 2 * certified_norm_bound ** 2 * dwell ** 2
        if averaged_error > theorem_bound + 2e-12:
            raise AssertionError("Floating Choi diagnostic exceeded the analytic bound.")
        if covariance_residual > 2e-12:
            raise AssertionError("Full finite-dilation covariance failed numerically.")
        rows.append({
            "dwell": dwell,
            "full_output_normalized_choi_trace_norm": averaged_error,
            "key_retained_choi_trace_norm": keyed_choi_error,
            "analytic_full_diamond_upper_bound": theorem_bound,
            "joint_choi_error_divided_by_dwell_squared": averaged_error / dwell**2,
            "key_retained_error_divided_by_dwell": keyed_choi_error / dwell,
            "full_dilation_covariance_operator_residual": covariance_residual,
        })
    return {
        "source_qubits": n,
        "source_dimension": d,
        "environment_dimension": environment_dimension,
        "joint_output_dimension": full_dimension,
        "normalized_choi_dimension": full_dimension * d,
        "random_pauli_group_size_enumerated_only_for_diagnostic": len(group),
        "hamiltonian_spectral_norm_float": float(np.linalg.norm(h, 2)),
        "hamiltonian_l1_bound": certified_norm_bound,
        "rows": rows,
    }


def evaluate_schedule(n, r=1.0, j=1.0, epsilon=0.1):
    lam = n * j
    t = math.log(8 * n / epsilon) / r
    blocks = max(1, math.ceil(8 * lam * lam * t * t / epsilon))
    rounds = blocks + 1
    width = epsilon / (8 * (lam + n * r) * rounds)
    peak = math.pi / width
    slew = math.pi ** 2 / width ** 2
    return {
        "n": n, "r": r, "J": j, "Lambda": lam, "epsilon": epsilon,
        "useful_collection_time": t,
        "blocks": blocks,
        "pulse_rounds": rounds,
        "pulse_width": width,
        "per_site_peak_Hamiltonian_norm": peak,
        "per_site_peak_slew": slew,
        "local_rotation_upper_count": n * rounds,
        "random_key_bits": 2 * n * blocks,
        "control_action_upper_bound": n * rounds * math.pi / 2,
        "useful_output_mean_photon_count": 3 * n * r * t / 4,
        "source_wall_time_excluding_guards_and_receiver": t + rounds * width,
        "ideal_export_error_bound": 2 * n * math.exp(-r * t),
        "full_output_twirl_error_bound": 2 * lam * lam * t * t / blocks,
        "discarded_pulse_error_bound": 2 * (lam + n * r) * rounds * width,
        "remaining_interface_error_allocation": epsilon / 4,
        "receiver_cost_status": "Accepted finite receiver bill is additional; not evaluated or simulated here.",
        "units": "Thermal-free quantum model units with hbar=1; no SI device interpretation.",
        "cost_status": "Sufficient schedule, not a lower bound or a useful-hardware claim.",
    }


def main():
    start = time.perf_counter()
    results = {
        "status": "completed finite mathematical diagnostics",
        "proof_governs": "CONTROL_FOR_CALIBRATION.md",
        "execution_scope": (
            "Two finite collision dilations, full-output Choi calculations, exact analytic "
            "key identities, and sufficient schedule evaluation. No hardware, continuous "
            "Markov field, receiver, or physical calibration is simulated."
        ),
        "collision_cases": [collision_case(1), collision_case(2)],
        "key_identity": [
            {"omega_dwell": x, "discard_key_diamond": 2 * math.sin(x)**2,
             "keep_key_diamond": 2 * abs(math.sin(x))}
            for x in [0.1, 0.01, 0.001]
        ],
        "scalable_schedule_family": [evaluate_schedule(n) for n in [1, 4, 16, 64]],
        "environment": {
            "python": platform.python_version(), "numpy": np.__version__,
            "scipy": scipy.__version__, "platform": platform.platform(),
        },
    }
    results["classical_arithmetic_elapsed_seconds"] = time.perf_counter() - start
    path = ROOT / "audit_results.json"
    path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(path), "collision_parameter_points": 12,
        "scalable_schedule_points": 4,
        "max_covariance_residual": max(row["full_dilation_covariance_operator_residual"]
            for case in results["collision_cases"] for row in case["rows"]),
        "last_joint_error_ratios": [case["rows"][-1]["joint_choi_error_divided_by_dwell_squared"]
            for case in results["collision_cases"]],
        "elapsed_seconds": results["classical_arithmetic_elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
