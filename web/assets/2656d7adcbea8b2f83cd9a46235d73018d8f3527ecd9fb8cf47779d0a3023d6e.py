"""Small diagnostic for the power-range compatible-dilation inequalities."""
import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).with_name("power_range_check.json")
RNG = np.random.default_rng(20261007)
I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)
PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

swap = np.array(
    [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]],
    dtype=complex,
)
p_sym = (I4 + swap) / 2
kraus = []
for b in range(2):
    ket = np.eye(2, dtype=complex)[:, b : b + 1]
    kraus.append(np.sqrt(2 / 3) * p_sym @ np.kron(I2, ket))

v = np.vstack(kraus)  # Stinespring isometry: input C^2 -> (C^2 tensor C^2) tensor C^2_env

def j_map(z):
    return sum(k.conj().T @ z @ k for k in kraus)

def phi(a):
    return j_map(np.kron(a, I2))

def phi_second(a):
    return j_map(np.kron(I2, a))

def power(a, n):
    out = a.copy()
    for _ in range(n):
        out = phi(out)
    return out

def tr_norm2(a):
    return float(np.real(np.trace(a.conj().T @ a)) / 2)

def l2(a):
    return np.sqrt(max(0.0, tr_norm2(a)))

def q_defect(a):
    return float(np.real(np.trace(phi(a @ a) - phi(a) @ phi(a))) / 2)

def contraction(h):
    h = (h + h.conj().T) / 2
    return h / np.linalg.norm(h, ord=2)

assert np.linalg.norm(sum(k.conj().T @ k for k in kraus) - I2) < 1e-12
assert np.linalg.norm(v.conj().T @ v - I2) < 1e-12
marginal_error = max(
    np.linalg.norm(phi(a) - phi_second(a))
    for a in (I2, PAULI_X, PAULI_Y, np.array([[1, 0], [0, -1]], dtype=complex))
)
assert marginal_error < 1e-12

# Verify the exact Stinespring commutator identity for arbitrary contractions.
# The stacked Kraus isometry uses environment-major row order, so the
# Stinespring representation is I_env tensor (output algebra).

def compatible_identity_residual(x, y):
    p = v @ v.conj().T
    q = np.eye(8, dtype=complex) - p
    px = np.kron(I2, np.kron(x, I2))
    py = np.kron(I2, np.kron(I2, y))
    rx = q @ px @ v
    ry = q @ py @ v
    f = rx.conj().T @ ry
    lhs = phi(x) @ phi(y) - phi(y) @ phi(x)
    rhs = f.conj().T - f
    qx = q_defect(x)
    qy = q_defect(y)
    qx_dilation = float(np.real(np.trace(rx.conj().T @ rx)) / 2)
    qy_dilation = float(np.real(np.trace(ry.conj().T @ ry)) / 2)
    return (
        np.linalg.norm(lhs - rhs),
        abs(qx - qx_dilation),
        abs(qy - qy_dilation),
    )

max_identity_residual = 0.0
max_defect_residual = 0.0
max_bound_slack_violation = 0.0
max_band_slack_violation = 0.0
fixtures = 0
for m in range(1, 9):
    for t in range(12):
        a = contraction(RNG.normal(size=(2, 2)) + 1j * RNG.normal(size=(2, 2)))
        c = contraction(RNG.normal(size=(2, 2)) + 1j * RNG.normal(size=(2, 2)))
        x = power(a, m - 1)
        y = power(c, m - 1)
        comm = phi(x) @ phi(y) - phi(y) @ phi(x)
        comm_norm = l2(comm)
        qx, qy = q_defect(x), q_defect(y)
        bound = 2 * np.sqrt(max(0.0, min(qx, qy)))
        max_bound_slack_violation = max(max_bound_slack_violation, comm_norm - bound)

        # For this cloner, Phi has spectrum 1 on scalars and 2/3 on traceless matrices.
        a_tr = a - np.trace(a) * I2 / 2
        c_tr = c - np.trace(c) * I2 / 2
        qx_spectral = (1 - (2 / 3) ** 2) * (2 / 3) ** (2 * (m - 1)) * tr_norm2(a_tr)
        qy_spectral = (1 - (2 / 3) ** 2) * (2 / 3) ** (2 * (m - 1)) * tr_norm2(c_tr)
        max_defect_residual = max(max_defect_residual, abs(qx - qx_spectral), abs(qy - qy_spectral))

        # The nonfixed eigenvalue 2/3 lies in dyadic band I_1=[1/2,3/4).
        k = m - 1
        coarse_band_weight = 2 ** (1 - 1) * np.exp(-k * 2 ** (-1))
        max_band_slack_violation = max(
            max_band_slack_violation,
            qx_spectral - coarse_band_weight * tr_norm2(a_tr),
            qy_spectral - coarse_band_weight * tr_norm2(c_tr),
        )

        identity, dx, dy = compatible_identity_residual(x, y)
        max_identity_residual = max(max_identity_residual, identity)
        max_defect_residual = max(max_defect_residual, dx, dy)
        fixtures += 1

# A hand-picked noncommuting pair exercises an explicit output commutator.
for m in range(1, 9):
    actual = l2(power(PAULI_X, m) @ power(PAULI_Y, m) - power(PAULI_Y, m) @ power(PAULI_X, m))
    q = (1 - (2 / 3) ** 2) * (2 / 3) ** (2 * (m - 1))
    assert actual <= 2 * np.sqrt(q) + 1e-12

result = {
    "model": "qubit universal 1-to-2 cloner; Heisenberg marginal shrink 2/3",
    "seed": 20261007,
    "random_hermitian_contraction_pairs": fixtures,
    "both_compatible_marginals_verified": True,
    "stinespring_isometry_verified": True,
    "max_compatible_identity_residual": max_identity_residual,
    "max_kadison_defect_residual": max_defect_residual,
    "max_uniform_bound_violation": max_bound_slack_violation,
    "max_dyadic_band_bound_violation": max_band_slack_violation,
    "scope": "finite diagnostic only; no general theorem or EB rounding is certified by computation",
}
OUT.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
