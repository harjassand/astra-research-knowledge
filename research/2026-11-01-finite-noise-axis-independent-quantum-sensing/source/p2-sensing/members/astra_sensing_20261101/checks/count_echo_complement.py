"""Executable checks for the complementary counted-jump construction.

Only finite-dimensional identities and Monte Carlo checks; no experimental data.
"""
import json
import numpy as np


def cyclic_identity(rng, q, cycles):
    phases = rng.uniform(-np.pi, np.pi, q)
    h = rng.normal(size=q)
    omega = 0.73
    jump = np.zeros((q, q), complex)
    for k in range(q):
        jump[(k + 1) % q, k] = np.exp(1j * phases[k])
    waits = rng.exponential(size=q * cycles)
    actual = np.eye(q, dtype=complex)
    accumulated = np.zeros(q)
    for r, wait in enumerate(waits):
        actual = jump @ np.diag(np.exp(-1j * omega * wait * h)) @ actual
        accumulated += wait * np.roll(h, -r)
    expected = np.diag(np.exp(-1j * omega * accumulated))
    expected *= np.exp(1j * cycles * phases.sum())
    return float(np.linalg.norm(actual - expected, 2))


def robust_qec_identity(gamma_even, gamma_odd):
    eye = np.eye(2)
    x = np.array([[0, 1], [1, 0]], complex)
    y = np.array([[0, -1j], [1j, 0]], complex)
    z = np.diag([1, -1])
    zs = np.kron(np.kron(z, eye), eye)
    za = np.kron(np.kron(eye, z), eye)
    pe = (np.eye(8) + zs @ za) / 2
    po = np.eye(8) - pe
    rate_root = np.sqrt(gamma_even) * pe + np.sqrt(gamma_odd) * po
    lx = np.kron(np.kron(x, eye), eye) @ rate_root
    ly = np.kron(np.kron(y, eye), eye) @ rate_root
    a = (gamma_even + gamma_odd) / 2
    b = (gamma_even - gamma_odd) / 2
    v = -b / a
    code = np.zeros((8, 2), complex)
    code[0, 0] = np.sqrt((1 + v) / 2)  # |000>
    code[5, 0] = np.sqrt((1 - v) / 2)  # |101>
    code[2, 1] = np.sqrt((1 - v) / 2)  # |010>
    code[7, 1] = np.sqrt((1 + v) / 2)  # |111>
    errors = [np.eye(8), lx, ly]
    kl_residual = 0.0
    for ei in errors:
        for ej in errors:
            block = code.conj().T @ ei.conj().T @ ej @ code
            kl_residual = max(kl_residual, np.linalg.norm(block - np.trace(block) / 2 * np.eye(2), 2))
    signal_residual = np.linalg.norm(code.conj().T @ zs @ code - v * z, 2)
    return {"v": v, "kl_residual": float(kl_residual), "signal_residual": float(signal_residual)}


def waiting_time_check(rng):
    n, g1, g2, samples = 200, 1.0, 4.0, 200000
    slow = rng.gamma(n, 1 / g1, samples)
    fast = rng.gamma(n, 1 / g2, samples)
    signed = slow - fast
    theory = n * n * (1 / g1 - 1 / g2) ** 2 + n * (1 / g1 ** 2 + 1 / g2 ** 2)
    empirical = np.mean(signed ** 2)
    se = np.std(signed ** 2, ddof=1) / np.sqrt(samples)
    return {"n": n, "gamma_slow": g1, "gamma_fast": g2,
            "mean_time_theory": n * (1 / g1 + 1 / g2),
            "qfi_theory": theory, "qfi_monte_carlo": float(empirical),
            "mc_standard_error": float(se), "mc_z_score": float((empirical - theory) / se)}


def main():
    rng = np.random.default_rng(20261101)
    identities = {str(q): max(cyclic_identity(rng, q, 7) for _ in range(30)) for q in [2, 3, 5]}
    result = {"cyclic_operator_norm_residuals": identities,
              "robust_qec_baseline": robust_qec_identity(1.0, 4.0),
              "waiting_time_moments": waiting_time_check(rng)}
    assert max(identities.values()) < 1e-11
    assert result["robust_qec_baseline"]["kl_residual"] < 1e-12
    assert result["robust_qec_baseline"]["signal_residual"] < 1e-12
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
