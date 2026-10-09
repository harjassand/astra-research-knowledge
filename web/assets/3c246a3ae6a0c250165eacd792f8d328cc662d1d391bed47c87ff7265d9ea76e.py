"""Finite diagnostics for the independently derived Cycle06 controls.

No optimization over global B bases; no test of the unresolved uniform gate.
Run with OPENBLAS_NUM_THREADS=1 python3 replay_controls.py.
"""

from pathlib import Path
import json
import math
import numpy as np


X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.diag([1.0, -1.0]).astype(complex)
I2 = np.eye(2, dtype=complex)


def kron_all(items):
    out = np.ones((1, 1), dtype=complex)
    for item in items:
        out = np.kron(out, item)
    return out


def trace_distance(a, b):
    return float(np.abs(np.linalg.eigvalsh((a - b + (a - b).conj().T) / 2)).sum() / 2)


def binary_entropy(p):
    return -p * math.log(p) - (1 - p) * math.log1p(-p)


def weak_product(n):
    s = 1 / math.sqrt(n)
    kappa = math.sqrt(1 - s * s)
    sigma = (I2 + s * X) / 2
    sigmap = (I2 + s * X + s * Z) / 2
    sigmap_out = (I2 + s * X + s * kappa * Z) / 2
    omega = [(I2 + s * X + z * kappa * Z) / 2 for z in (1, -1)]
    fixed_error = float(np.linalg.norm(sum(omega) / 2 - sigma))
    pure_error = max(float(np.linalg.norm(w @ w - w)) for w in omega)
    joint_error = trace_distance(kron_all([sigmap] * n), kron_all([sigmap_out] * n))
    info = n * (
        binary_entropy((1 + s) / 2)
        - binary_entropy((1 + math.sqrt(2) * s) / 2)
    )
    delta = s * (1 - kappa)
    fidelity_bound = math.sqrt(n) * delta
    assert fixed_error < 1e-12
    assert pure_error < 1e-12
    assert joint_error <= fidelity_bound + 1e-10
    assert fidelity_bound <= 1 / n + 1e-12
    assert info <= 1 + 1e-12
    return {
        "N": n,
        "s": s,
        "I_nats_exact_entropy_formula": info,
        "actual_displayed_broadcaster_joint_marginal_error": joint_error,
        "proved_fidelity_error_bound": fidelity_bound,
        "coarser_bound_1_over_N": 1 / n,
        "sigma_fixed_residual": fixed_error,
        "prepared_state_purity_residual": pure_error,
        "q_global_basis_status": "UNKNOWN; not computed or lower bounded",
    }


def clifford_frame(n):
    m = 2 ** n
    d = m // 2
    identity = np.eye(m, dtype=complex)
    zz = [kron_all([Z if j == i else I2 for j in range(n)]) for i in range(n)]
    gg = [kron_all([Z if j < i else X if j == i else I2 for j in range(n)])
          for i in range(n)]
    h = sum(gg) / math.sqrt(n)
    p = (identity + h) / 2
    r = gg[-1]
    ss = sum(gg[:-1]) / math.sqrt(n - 1)
    a = 1 / math.sqrt(n)
    c = math.sqrt((1 + a) / 2)
    u = (1 - a) / 2
    rotation = c * identity + math.sqrt(u) * ss @ r

    vr = np.zeros((m, d), dtype=complex)
    for prefix in range(d):
        sign = (-1) ** prefix.bit_count()
        vr[2 * prefix, prefix] = 1 / math.sqrt(2)
        vr[2 * prefix + 1, prefix] = sign / math.sqrt(2)
    v = rotation @ vr
    ortho = float(np.linalg.norm(v.conj().T @ v - np.eye(d)))
    support = float(np.linalg.norm(p @ v - v))
    rotation_residual = float(np.linalg.norm(rotation @ r @ rotation.conj().T - h))
    bb = [v.conj().T @ z @ v for z in zz]
    eigen_residual = 0.0
    hs_energy = 0.0
    variance_sum = 0.0
    for b in bb:
        ambient = v @ b @ v.conj().T
        gamma_b = 2 * v.conj().T @ np.diag(np.diag(ambient)) @ v
        eigen_residual = max(eigen_residual,
                             float(np.linalg.norm(gamma_b - (1 - 1 / n) * b)))
        diff = b - np.diag(np.diag(b))
        hs_energy += float(np.trace(diff.conj().T @ diff).real / d / n)
        variance_sum += float(1 - np.mean(np.abs(np.diag(b)) ** 2))

    alpha = 0.9
    q_op = sum(np.kron(g, b) for g, b in zip(gg, bb)) / math.sqrt(n)
    q_diag = sum(np.kron(g, np.diag(np.diag(b))) for g, b in zip(gg, bb)) / math.sqrt(n)
    rho = (np.eye(m * d) + alpha * q_op) / (m * d)
    rho_dephased = (np.eye(m * d) + alpha * q_diag) / (m * d)
    rho_reconstructed = (np.eye(m * d) + alpha * (1 - 1 / n) * q_op) / (m * d)
    q_upper = trace_distance(rho, rho_dephased)
    eb_error = trace_distance(rho, rho_reconstructed)
    hs_bound = alpha * math.sqrt(hs_energy) / 2
    proof_q_bound = alpha * math.sqrt(3 / n) / 2
    min_eigenvalue = float(np.linalg.eigvalsh(rho).min())
    assert max(ortho, support, rotation_residual, eigen_residual) < 1e-10
    assert hs_energy <= 3 / n + 1e-10
    assert variance_sum < 3 + 1e-10
    assert q_upper <= hs_bound + 1e-10
    assert hs_bound <= proof_q_bound + 1e-10
    assert eb_error <= alpha / (2 * n) + 1e-10
    assert min_eigenvalue > -1e-12
    return {
        "n": n,
        "B_dimension": d,
        "alpha": alpha,
        "orthonormality_residual": ortho,
        "P_support_residual": support,
        "rotation_identity_residual": rotation_residual,
        "canonical_frame_eigen_identity_residual": eigen_residual,
        "sum_Z_variance_in_constructed_basis": variance_sum,
        "mean_HS_dephasing_energy": hs_energy,
        "actual_EB_reconstruction_error": eb_error,
        "actual_CQ_candidate_trace_error": q_upper,
        "computed_HS_trace_upper_bound": hs_bound,
        "proved_coarser_CQ_upper_bound": proof_q_bound,
        "rho_min_eigenvalue": min_eigenvalue,
        "gate_verdict_for_this_family": "NOT A COUNTEREXAMPLE: explicit q upper bound tends to zero",
    }


result = {
    "status": "PASS finite diagnostics only",
    "unresolved_gate_status": "UNKNOWN",
    "weak_qubit_product": [weak_product(n) for n in (4, 5, 6, 7)],
    "clifford_frame_failed_counterexample": [clifford_frame(n) for n in (3, 4, 5)],
}
path = Path(__file__).with_name("CONTROLS_REPLAY.json")
path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
