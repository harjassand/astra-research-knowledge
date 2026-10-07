"""Small diagnostics for the tracial finite-net transfer.

No theorem is inferred from these fixtures.  The script checks the algebraic
commutator and EB-reconstruction inequalities on a known compatible qubit
channel (a noisy Z measurement followed by classical preparation).
"""
import json
import numpy as np

SEED = 53107
rng = np.random.default_rng(SEED)
D = 2
THETA = 0.4
EPS = 0.03
LAMBDA = 1.0 - EPS
C0 = 4 + 2 * np.sqrt(2)
I = np.eye(D, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = [X, Y, Z]

def trn(A):
    return np.trace(A) / D

def l1n(A):
    return np.sum(np.linalg.svd(A, compute_uv=False)) / D

def l2n(A):
    return np.sqrt(np.real(np.trace(A.conj().T @ A)) / D)

def phi(A):
    return trn(A) * I + LAMBDA * trn(Z @ A) * Z

def dephase_z(A):
    return np.diag(np.diag(A))

# One full-domain CPTP broadcaster: measure Z, then prepare the same noisy
# diagonal state on both outputs.  Its common marginal is phi.
def broadcaster_marginal(rho):
    return sum(
        np.trace(P @ rho).real * np.kron(state, state)
        for P, state in [
            (np.diag([1, 0]), (I + LAMBDA * Z) / 2),
            (np.diag([0, 1]), (I - LAMBDA * Z) / 2),
        ]
    )

def partial_trace_second(rho2):
    t = rho2.reshape(D, D, D, D)
    return np.einsum("abcb->ac", t)

records = []
max_commutator_ratio = 0.0
max_reconstruction_ratio = 0.0
max_marginal_error = 0.0
for trial in range(40):
    coeffs = rng.normal(size=3)
    coeffs /= np.linalg.norm(coeffs)
    # Keep most weight on the slowly evolving classical axis; the transverse
    # component varies over several small scales.
    transverse = 10 ** rng.uniform(-3.0, -0.5)
    vec = np.array([transverse * coeffs[0], transverse * coeffs[1], coeffs[2]])
    vec /= np.linalg.norm(vec)
    H = THETA * sum(vec[k] * PAULI[k] for k in range(3))
    rho = (I + H) / D
    r = l1n(phi(H) - H)
    A = H / THETA
    comm = l2n(A @ A - A @ A)  # exact self-pair sanity check
    # Compare with a second independently generated nearby likelihood.
    coeffs2 = rng.normal(size=3)
    coeffs2 /= np.linalg.norm(coeffs2)
    transverse2 = 10 ** rng.uniform(-3.0, -0.5)
    vec2 = np.array([transverse2 * coeffs2[0], transverse2 * coeffs2[1], coeffs2[2]])
    vec2 /= np.linalg.norm(vec2)
    H2 = THETA * sum(vec2[k] * PAULI[k] for k in range(3))
    A2 = H2 / THETA
    comm = l2n(A @ A2 - A2 @ A)
    comm_bound = C0 * np.sqrt(max(r, l1n(phi(H2) - H2)) / THETA)
    max_commutator_ratio = max(max_commutator_ratio, comm / max(comm_bound, 1e-15))

    # EB dephasing fixes the retained classical coordinate.  The bound is the
    # c=1 Dirichlet estimate for this channel pair.
    H_round = dephase_z(H)
    err = 0.5 * l1n(H_round - H)
    round_residual = l1n(phi(H) - H)
    max_reconstruction_ratio = max(max_reconstruction_ratio, err**2 / max(THETA * round_residual, 1e-15))

    out = broadcaster_marginal(rho)
    marginal = partial_trace_second(out)
    max_marginal_error = max(max_marginal_error, l1n(marginal - phi(rho)))
    records.append({"trial": trial, "residual": float(r), "commutator": float(comm), "commutator_bound": float(comm_bound), "eb_error": float(err)})

result = {
    "seed": SEED,
    "dimension": D,
    "theta": THETA,
    "lambda_z": LAMBDA,
    "channel": "measure Z; prepare matching noisy diagonal states on both outputs",
    "trials": len(records),
    "max_commutator_to_bound_ratio": float(max_commutator_ratio),
    "max_eb_error_squared_over_theta_residual": float(max_reconstruction_ratio),
    "max_broadcaster_marginal_error": float(max_marginal_error),
    "all_finite": bool(np.all(np.isfinite([max_commutator_ratio, max_reconstruction_ratio, max_marginal_error]))),
    "scope": "diagnostic only; does not implement the finite-tuple rounding theorem or prove a growing-dimension bound",
    "records": records,
}
print(json.dumps(result, indent=2, sort_keys=True))
