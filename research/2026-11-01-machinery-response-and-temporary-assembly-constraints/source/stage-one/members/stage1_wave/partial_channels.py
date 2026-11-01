"""Exact passive reciprocal counterexample to partial-channel work inference.

This script is original analytical evidence, not a simulation of any experiment.
Run: python stage1_wave/partial_channels.py
Only NumPy and the Python standard library are required.
"""
from pathlib import Path
import json
import numpy as np


H = np.diag([-1.0, 1.0])


def scattering(q, eta=0.98, a=1.0, b=0.0):
    """Four-port instantaneous S; first two ports are observed and driven."""
    I = np.eye(2)
    S0 = np.block([[np.sqrt(eta) * I, np.sqrt(1 - eta) * I],
                   [np.sqrt(1 - eta) * I, -np.sqrt(eta) * I]])
    d = np.r_[np.exp(0.5j * a * np.diag(H) * q),
              np.exp(1j * (b - a / 2) * np.diag(H) * q)]
    return d[:, None] * S0 * d[None, :]


def work_numeric(q, eta, a, b, eps=1e-6):
    S = scattering(q, eta, a, b)
    dS = (scattering(q + eps, eta, a, b)
          - scattering(q - eps, eta, a, b)) / (2 * eps)
    Q = -1j * S.conj().T @ dS
    return (Q + Q.conj().T)[:2, :2] / 2


def run():
    eta, a = 0.98, 1.0
    b_values = [0.0, -100.0]
    q_values = np.linspace(-0.5, 0.5, 101)
    max_unitarity = max_reciprocity = max_derivative_error = 0.0
    max_observed_difference = max_lost_power_difference = 0.0
    for q in q_values:
        Sfirst = scattering(q, eta, a, b_values[0])
        Ssecond = scattering(q, eta, a, b_values[1])
        for b, S in zip(b_values, [Sfirst, Ssecond]):
            max_unitarity = max(max_unitarity,
                                float(np.linalg.norm(S.conj().T @ S - np.eye(4))))
            max_reciprocity = max(max_reciprocity,
                                 float(np.linalg.norm(S - S.T)))
            Q_exact = (eta * a + (1 - eta) * b) * H
            max_derivative_error = max(max_derivative_error,
                                      float(np.linalg.norm(work_numeric(q, eta, a, b) - Q_exact)))
        max_observed_difference = max(max_observed_difference,
                                      float(np.linalg.norm(Sfirst[:2, :2] - Ssecond[:2, :2])))
        B1, B2 = Sfirst[2:, :2], Ssecond[2:, :2]
        max_lost_power_difference = max(max_lost_power_difference,
                                       float(np.linalg.norm(B1.conj().T @ B1 - B2.conj().T @ B2)))

    Q_observed = eta * a * H
    values, vectors = np.linalg.eigh(Q_observed)
    probe = vectors[:, 0]
    works = [float(np.real(probe.conj() @ ((eta * a + (1 - eta) * b) * H) @ probe))
             for b in b_values]

    # Additional, genuinely stronger assumption: the hidden phase rate is bounded.
    # The exact B obeys dB/dq=i b H B. Therefore |b|<=L gives
    # -L C <= Q_hidden <= L C, C=B*B, in Loewner order.
    L = 100.0
    C = (1 - eta) * np.eye(2)
    robust_upper = Q_observed + L * C
    guaranteed_negative_exists = bool(np.linalg.eigvalsh(robust_upper)[0] < 0)
    assert max_unitarity < 1e-12
    assert max_reciprocity < 1e-12
    assert max_observed_difference == 0.0
    assert max_lost_power_difference < 1e-12
    assert max_derivative_error < 1e-6
    assert works[0] < 0 < works[1]
    assert not guaranteed_negative_exists

    result = {
        "model": "Four-port reciprocal unitary phase-lead network; two accessible ports",
        "scope": "Exact work ambiguity from accessible S histories and lost power alone; not a no-go theorem for additional mechanical response observations",
        "eta": eta,
        "a": a,
        "hidden_phase_slopes": b_values,
        "observed_work_eigenvalues": values.tolist(),
        "true_work_on_observed_minimizer": works,
        "max_unitarity_residual": max_unitarity,
        "max_reciprocity_residual": max_reciprocity,
        "max_observed_history_difference": max_observed_difference,
        "max_lost_power_difference": max_lost_power_difference,
        "max_finite_difference_work_error": max_derivative_error,
        "hidden_rate_bound_L": L,
        "robust_upper_eigenvalues": np.linalg.eigvalsh(robust_upper).tolist(),
        "guaranteed_negative_direction_with_bound": guaranteed_negative_exists,
        "sampled_parameter_points": len(q_values),
    }
    output = Path(__file__).with_name("results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
