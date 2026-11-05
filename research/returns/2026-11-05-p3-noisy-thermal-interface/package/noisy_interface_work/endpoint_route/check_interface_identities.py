"""Finite-dimensional checks of the exact identities, not a FT-device simulation."""

import json
import itertools
import numpy as np

rng = np.random.default_rng(20261105)
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
Y = 1j * X @ Z
paulis = [I, X, Y, Z]
real_bell_frames = [I, X, Z, X @ Z]
phi = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
Phi = np.outer(phi, phi.conj())


def pure(dim):
    v = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    return v / np.linalg.norm(v)


def random_channel():
    a = rng.normal(size=(6, 2)) + 1j * rng.normal(size=(6, 2))
    q, _ = np.linalg.qr(a)
    return [q.reshape(3, 2, 2)[j] for j in range(3)]


def apply(kraus, rho):
    return sum(k @ rho @ k.conj().T for k in kraus)


def apply_first(kraus, rho):
    return apply([np.kron(k, I) for k in kraus], rho)


def depol_first(rho, a):
    reduced = np.einsum("arad->rd", rho.reshape(2, 2, 2, 2))
    return (1 - a) * rho + a * np.kron(I / 2, reduced)


def distance(rho, sigma):
    return np.abs(np.linalg.eigvalsh(rho - sigma)).sum() / 2


floor_residual = 0.0
floor_gap_min = float("inf")
for _ in range(100):
    a, b = rng.uniform(0, 0.9, size=2)
    kraus = random_channel()
    choi_r = apply_first(kraus, Phi)
    result = depol_first(apply_first(kraus, depol_first(Phi, a)), b)
    fe_r = np.vdot(phi, choi_r @ phi).real
    fe = np.vdot(phi, result @ phi).real
    expected = (1 - a) * (1 - b) * fe_r + (a + b - a * b) / 4
    floor_residual = max(floor_residual, abs(fe - expected))
    floor = 3 * (a + b - a * b) / 4
    floor_gap_min = min(floor_gap_min, distance(result, Phi) - floor)
    identity_result = depol_first(depol_first(Phi, a), b)
    assert abs(distance(identity_result, Phi) - floor) < 1e-12
assert floor_residual < 1e-12
assert floor_gap_min > -1e-12


refresh_residual = 0.0
outcome_residual = 0.0
for _ in range(100):
    # D logical, D syndrome, arbitrary reference. Fresh Bell A logical/B logical.
    # Fresh A syndrome/B syndrome can be entangled.
    psi = pure(8).reshape(2, 2, 2)
    tau = pure(4).reshape(2, 2)
    bell = I / np.sqrt(2)
    total = np.zeros((8, 8), dtype=complex)  # output B logical, reference, B syndrome
    for frame in real_bell_frames:
        measured_bell = np.einsum("ad,de->ae", bell, frame.T)
        # Contract Bell bra on incoming D logical and A logical.
        v = np.einsum("dsr,ab,xy,da->srbxy", psi, bell, tau, measured_bell.conj())
        v = np.einsum("cb,srbxy->srcxy", frame.conj().T, v)
        probability = np.vdot(v, v).real
        outcome_residual = max(outcome_residual, abs(probability - 0.25))
        # Trace the old D syndrome and measured A syndrome.
        rho = np.einsum("srbxy,stcxz->bryctz", v, v.conj()).reshape(8, 8)
        total += rho
    rho_lr = np.einsum("dsr,est->dret", psi, psi.conj()).reshape(4, 4)
    rho_bsyndrome = tau.T @ tau.conj()
    expected = np.kron(rho_lr, rho_bsyndrome)
    refresh_residual = max(refresh_residual, np.linalg.norm(total - expected, ord=1))
assert refresh_residual < 1e-12
assert outcome_residual < 1e-12


twirl_offdiagonal = 0.0
for _ in range(100):
    kraus = random_channel()

    def twirled(rho):
        return sum(p @ apply(kraus, p @ rho @ p) @ p for p in paulis) / 4

    transfer = np.array([[np.trace(a @ twirled(b)) / 2 for b in paulis] for a in paulis])
    twirl_offdiagonal = max(twirl_offdiagonal, np.max(np.abs(transfer - np.diag(np.diag(transfer)))))
assert twirl_offdiagonal < 1e-12


def noisy_majority(inputs, faults):
    a, b, c = inputs
    # After each native gate, arbitrary Pauli faults reduce to these X bits
    # on a computational-basis input. Z factors change only a global phase.
    b ^= a
    a ^= faults[0]
    b ^= faults[1]
    c ^= a
    a ^= faults[2]
    c ^= faults[3]
    a ^= b & c
    a ^= faults[4]
    b ^= faults[5]
    c ^= faults[6]
    return a


majority_cases = 0
for inp in itertools.product(range(2), repeat=3):
    assert noisy_majority(inp, (0,) * 7) == int(sum(inp) >= 2)
    for faults in itertools.product(range(2), repeat=7):
        y0 = noisy_majority(inp, faults)
        y1 = noisy_majority(tuple(x ^ 1 for x in inp), faults)
        assert y1 == y0 ^ 1
        majority_cases += 1

report = {
    "random_trials_per_identity": 100,
    "entanglement_fidelity_formula_max_residual": floor_residual,
    "sampled_channels_min_distance_minus_exact_floor": floor_gap_min,
    "bell_refresh_trace_norm_upper_residual": refresh_residual,
    "bell_outcome_uniformity_max_residual": outcome_residual,
    "pauli_twirl_off_diagonal_max_residual": twirl_offdiagonal,
    "majority_native_fault_truth_tables_checked": majority_cases,
    "majority_complement_covariance": True,
    "scope": "Checks finite-dimensional algebra only; not a fault-tolerance or physical-layout simulation.",
}
print(json.dumps(report, indent=2))
