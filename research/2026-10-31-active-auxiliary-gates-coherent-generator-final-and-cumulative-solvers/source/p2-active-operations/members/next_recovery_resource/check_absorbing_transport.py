"""Independent finite-matrix checks of absorbing unitary transport.

No device claim. Checks complete logical/source matrices, not only a chosen
source state. The only trajectory approximation is emission-time quadrature,
whose normalization residual is reported explicitly.
"""

import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, norm


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
I4 = np.eye(4, dtype=complex)
ZA, ZB = np.kron(Z, I2), np.kron(I2, Z)
M = (ZA + 1j * ZB) / np.sqrt(2)
S = np.diag([1, 1j])
Tgate = np.diag([1, np.exp(1j * np.pi / 4)])
CZ = np.diag([1, 1, 1, -1])

g, e, f = np.eye(3)
eg, fe = np.outer(e, g), np.outer(f, e)
Pg, Pe, Pf = (np.outer(v, v) for v in (g, e, f))
kappa = 2.0
dimL, dimE = 4, 2
G = np.kron(I4, np.kron(Pg, I2)) + np.kron(M, np.kron(Pe + Pf, I2))
Pgin = np.kron(I4, np.kron(g[:, None], I2))
Pgeout = [np.kron(I4, np.kron(v[None, :], I2)) for v in (g, e, f)]
J = np.sqrt(kappa) * np.kron(I4, np.kron(fe, I2))

# Abrupt source switching is intentional. No derivative or slow-source
# condition appears in the theorem.
configs = [
    (1.5 * I2 + 0.4 * X, 1.7 * Z, 0.3 * X),
    (1.7 * I2 + 0.5 * Z, 1.1 * X + 0.6 * Y, -0.25 * Y),
    (1.6 * I2 + 0.35 * Y, -1.4 * Z + 0.7 * X, 0.2 * Z),
]


def source_block(K, logical_factor):
    """Hilbert-Schmidt coefficient in K=logical_factor tensor B."""
    block = K.reshape(dimL, dimE, dimL, dimE)
    B = np.einsum("ij,iajb->ab", logical_factor.conj(), block) / dimL
    return B, float(norm(K - np.kron(logical_factor, B), 2))


def model(A, HE, D):
    Haux = np.kron(np.eye(3), HE) + np.kron(Pe, D)
    H = np.kron(I4, Haux)
    H += np.kron(M, np.kron(eg, A))
    H += np.kron(M.conj().T, np.kron(eg.T, A.conj().T))
    h = Haux + np.kron(eg, A) + np.kron(eg.T, A.conj().T)
    gauge_residual = norm(G.conj().T @ H @ G - np.kron(I4, h), 2)
    Heff = H - 0.5j * J.conj().T @ J
    return Heff, float(gauge_residual)


models = [model(*p) for p in configs]
gain_lo = min(np.linalg.eigvalsh(A).min() for A, _, _ in configs)
gain_hi = max(np.linalg.eigvalsh(A).max() for A, _, _ in configs)
dmax = max(norm(D, 2) for _, _, D in configs)
alpha = min(1.0, kappa / (2 * gain_hi + (kappa / 2 + dmax) ** 2 / gain_lo))
C = np.sqrt((2 + alpha) / (2 - alpha))
lam = alpha * gain_lo / (2 * (2 + alpha))


def run(total_time, steps=2400):
    dt = total_time / steps
    propagators = [expm(-1j * Heff * dt) for Heff, _ in models]
    source_propagators = [expm(-1j * HE * dt) for _, HE, _ in configs]
    # Each third of the interval uses a different noncommuting source.
    config_ids = np.repeat(np.arange(3), steps // 3)
    assert len(config_ids) == steps
    evol = [np.eye(24, dtype=complex)]
    uevol = [np.eye(dimE, dtype=complex)]
    for idx in config_ids:
        evol.append(propagators[idx] @ evol[-1])
        uevol.append(source_propagators[idx] @ uevol[-1])
    UE_T = uevol[-1]
    K0 = evol[-1] @ Pgin
    Kground = Pgeout[0] @ K0
    Kexcited = Pgeout[1] @ K0
    Ug, g_res = source_block(Kground, I4)
    Ue, e_res = source_block(Kexcited, M)
    survival_effect = K0.conj().T @ K0
    pmax = float(np.linalg.eigvalsh(survival_effect).max())
    source_survival = Ug.conj().T @ Ug + Ue.conj().T @ Ue
    effect_res = float(norm(survival_effect - np.kron(I4, source_survival), 2))

    # Every possible emitted photon time contributes. A single event is the
    # COMPLETE nonzero-emission history because f is absorbing.
    success_effect = np.zeros((8, 8), complex)
    max_jump_factorization = 0.0
    for n in range(steps + 1):
        UE_tail = UE_T @ uevol[n].conj().T
        excited = Pgeout[1] @ evol[n] @ Pgin
        Kt = np.sqrt(kappa) * np.kron(I4, UE_tail) @ excited
        _, residual = source_block(Kt, M)
        max_jump_factorization = max(max_jump_factorization, residual)
        weight = dt * (0.5 if n in (0, steps) else 1.0)
        success_effect += weight * (Kt.conj().T @ Kt)
    normalization_residual = float(norm(success_effect + survival_effect - np.eye(8), 2))

    return {
        "T": total_time,
        "worst_source_no_emission_probability": pmax,
        "uniform_proved_bound": float(min(1.0, C * C * np.exp(-2 * lam * total_time))),
        "ground_factorization_residual": g_res,
        "excited_factorization_residual": e_res,
        "all_sampled_emission_histories_factorization_residual": max_jump_factorization,
        "no_emission_effect_logical_blind_residual": effect_res,
        "emission_time_quadrature_normalization_residual": normalization_residual,
    }


def mismatch_example():
    """Individually positive gains can violate the common-source condition."""
    A1 = 1.5 * I2 + 0.5 * Z
    A2 = 1.5 * I2 - 0.5 * Z
    excitation = (np.kron(ZA, A1) + 1j * np.kron(ZB, A2)) / np.sqrt(2)
    _, residual = source_block(excitation, M)
    # Its effect is nevertheless exactly logical-blind, making this a direct
    # counterexample to using equal probabilities as a correction certificate.
    effect = excitation.conj().T @ excitation
    _, effect_res = source_block(effect, I4)
    plusL = np.ones(4, dtype=complex) / 2
    plusE = np.ones(2, dtype=complex) / np.sqrt(2)
    state = excitation @ np.kron(plusL, plusE)
    state /= norm(state)
    reduced = state.reshape(4, 2) @ state.reshape(4, 2).conj().T
    return {
        "positive_gain_eigenvalues": np.linalg.eigvalsh(A1).tolist(),
        "failure_to_factor_as_target_M": residual,
        "logical_blind_effect_residual": effect_res,
        "logical_purity_after_one_fine_operation": float(np.real(np.trace(reduced @ reduced))),
    }


result = {
    "status": "circuit-Hamiltonian model checks, not a device demonstration",
    "unitary_excitation_residual": float(norm(M.conj().T @ M - I4, 2)),
    "CZ_compiler_residual": float(norm(M - np.exp(1j * np.pi / 4) * np.kron(S, S.conj().T) @ CZ, 2)),
    "T_compiler_residual": float(norm(np.cos(3 * np.pi / 8) * Z + 1j * np.sin(3 * np.pi / 8) * I2 - np.exp(3j * np.pi / 8) * Tgate, 2)),
    "full_H_gauge_residuals": [v[1] for v in models],
    "full_jump_gauge_residual": float(norm(G.conj().T @ J @ G - J, 2)),
    "noncommuting_source_commutator_norms": [float(norm(A @ HE - HE @ A, 2)) for A, HE, _ in configs],
    "constants": {"g": float(gain_lo), "h": float(gain_hi), "d": float(dmax), "kappa": kappa, "alpha": float(alpha), "C": float(C), "lambda": float(lam)},
    "runs": [run(t) for t in (2.0, 5.0, 10.0, 20.0)],
    "mismatched_positive_gain_counterexample": mismatch_example(),
}
out = Path(__file__).with_name("absorbing_transport_results.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
