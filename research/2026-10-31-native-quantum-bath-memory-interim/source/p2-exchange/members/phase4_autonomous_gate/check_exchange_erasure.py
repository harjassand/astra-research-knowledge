"""Exact six-spin exchange filters and a probabilistic-recovery obstruction.

All spins are 1/2, hbar=1. No effective master equation is used.
The model is a uniform Heisenberg quartet and a singlet helper pair.
"""
import json
from pathlib import Path
from functools import reduce
import numpy as np
from scipy.linalg import eigh, expm
from scipy.optimize import root


I2 = np.eye(2)
pauli_half = [np.array([[0, 1], [1, 0]]) / 2,
              np.array([[0, -1j], [1j, 0]]) / 2,
              np.diag([1, -1]) / 2]


def kron(ops):
    return reduce(np.kron, ops)


def spin_ops(n):
    return [[kron([p if j == i else I2 for j in range(n)])
             for p in pauli_half] for i in range(n)]


def project(A, eigenvalue):
    w, v = eigh(A)
    q = v[:, np.abs(w - eigenvalue) < 1e-8]
    return q @ q.conj().T, q


sd = spin_ops(4)
sh = spin_ops(2)
JD = [sum(sd[i][a] for i in range(4)) for a in range(3)]
JH = [sum(sh[i][a] for i in range(2)) for a in range(3)]
JD2 = sum(A @ A for A in JD)
JH2 = sum(A @ A for A in JH)
P0, C0 = project(JD2, 0)
P1, C1 = project(JD2, 2)
P2, C2 = project(JD2, 6)
singlet = np.array([0, 1, -1, 0]) / np.sqrt(2)
PS = np.outer(singlet, singlet)
PT = np.eye(4) - PS
Vin = np.kron(np.eye(16), singlet[:, None])
link = [sum(np.kron(sd[i][a], sh[0][a]) for a in range(3))
        for i in range(4)]
dark = []
bright = []
for i in range(4):
    rest = [sum(sd[j][a] for j in range(4) if j != i) for a in range(3)]
    R2 = sum(A @ A for A in rest)
    d = P1 @ (R2 - 0.75 * np.eye(16)) / 3
    dark.append(d)
    bright.append(P1 - d)


def contact(delta, helper_gap, duration, site=0, coupling=1.):
    H = (np.kron(delta * JD2 / 2, np.eye(4)) +
         np.kron(np.eye(16), helper_gap * JH2 / 2) + coupling * link[site])
    U = expm(-1j * H * duration)
    K = Vin.conj().T @ U @ Vin
    alpha = np.trace(P0 @ K) / 2
    cb = np.trace(bright[site] @ K) / 6
    cd = np.trace(dark[site] @ K) / 3
    c2 = np.trace(P2 @ K) / 5
    predicted = alpha * P0 + cb * bright[site] + cd * dark[site] + c2 * P2
    residual = np.linalg.norm(K - predicted, 2)
    assert residual < 2e-10
    return K, alpha, cb, cd, c2, residual


def r_magic(n):
    return (n*n + np.sqrt(n**4 - (2*n-1)**2)) / (2*n-1)


def clean_false_flag_bound(delta, helper_gap, coupling=1.):
    return 3*coupling**2 / (4*(delta+helper_gap-coupling/2)**2 + 3*coupling**2)


def j2_return_amplitude(delta, helper_gap, duration):
    g = np.sqrt(6) / 8
    A = np.array([[0, g, g], [g, -1/8, -3/8], [g, -3/8, -1/8]])
    H = np.diag([3*delta, delta+helper_gap, 3*delta+helper_gap]) + A
    return expm(-1j * (H - 3*delta*np.eye(3)) * duration)[0, 0]


results = {
    "model": "Exact six spin-1/2 unitary, all-to-all uniform data exchange, one helper link",
    "dark_overlap_norms": [], "contacts": [], "sequences": []}
for i in range(4):
    for j in range(i+1, 4):
        overlap = np.linalg.norm(dark[j] @ dark[i], 2)
        results["dark_overlap_norms"].append([i, j, float(overlap)])
        assert abs(overlap - 1/3) < 3e-14

for n in [2, 3, 5, 10, 25, 50, 100]:
    d = r_magic(n)
    tau1 = 2*n*np.pi / np.sqrt(d*d+1)
    K, alpha, cb, cd, c2, res = contact(d, d, tau1)
    false1 = 1-abs(alpha)**2
    bound1 = clean_false_flag_bound(d, d)
    assert abs(cb) < 3e-11
    assert false1 <= bound1 + 2e-11
    g = np.sqrt(6)/8
    v = np.sqrt(15)/8
    tau2 = np.pi/(2*g)
    gap2 = 2*d+1/8
    K2, alpha2, cb2, cd2, c22, res2 = contact(d, gap2, tau2)
    a2 = v/d + tau2*np.exp(v/d)*v*(2*g+v)/(2*d)
    direct = abs(j2_return_amplitude(d, gap2, tau2))
    assert abs(abs(c22)-direct) < 3e-11
    assert abs(c22) <= a2+1e-12
    false2 = 1-abs(alpha2)**2
    bound2 = clean_false_flag_bound(d, gap2)
    assert false2 <= bound2 + 2e-11
    def residual(x):
        a = j2_return_amplitude(d, x[0], x[1])
        return [a.real, a.imag]
    numerical_root = root(residual, [gap2, tau2], tol=1e-11)
    amp_root = abs(j2_return_amplitude(d, *numerical_root.x))
    assert numerical_root.success and amp_root < 1e-10
    results["contacts"].append(dict(
        n=n, delta_over_link=float(d), tau1_link=float(tau1),
        bright_survival_amplitude=float(abs(cb)), dark_survival_amplitude=float(abs(cd)),
        code_false_flag=float(false1), code_false_flag_bound=float(bound1),
        j1_matrix_residual=float(res),
        j2_helper_gap=float(gap2), j2_time=float(tau2),
        j2_survival_amplitude=float(abs(c22)), j2_amplitude_bound=float(a2),
        j2_code_false_flag=float(false2), j2_code_false_flag_bound=float(bound2),
        j2_numerical_zero_gap=float(numerical_root.x[0]),
        j2_numerical_zero_time=float(numerical_root.x[1]),
        j2_numerical_zero_amplitude=float(amp_root)))
    if n in [10, 50]:
        for N, M in [(2, 1), (5, 2), (8, 3)]:
            clean = np.eye(16, dtype=complex)
            clean_alpha = 1+0j
            for t in range(N):
                Ki, ai, *_ = contact(d, d, tau1, site=t % 2)
                clean = Ki @ clean
                clean_alpha *= ai
            for t in range(M):
                Ki, ai, *_ = contact(d, gap2, tau2, site=t % 2)
                clean = Ki @ clean
                clean_alpha *= ai
            actual1 = np.linalg.norm(clean @ P1, 2)
            actual2 = np.linalg.norm(clean @ P2, 2)
            bound = max(3.**(-(N-1)), min(1., a2)**M)
            logical_res = np.linalg.norm(clean @ C0 - clean_alpha * C0, 2)
            assert max(actual1, actual2) <= bound+2e-10
            assert logical_res < 2e-10
            results["sequences"].append(dict(
                n=n, stage1_contacts=N, stage2_contacts=M,
                j1_clean_amplitude=float(actual1), j2_clean_amplitude=float(actual2),
                uniform_leakage_amplitude_bound=float(bound),
                uniform_leakage_probability_bound=float(bound**2),
                coherent_instrument_error_bound=float(min(1., bound+bound**2)),
                clean_code_erasure_probability=float(1-abs(clean_alpha)**2),
                clean_code_scalar_residual=float(logical_res),
                interaction_time=float(N*tau1+M*tau2)))

# No accepted perfect recovery for all unknown single-spin errors.
# Every branch R: J=1 -> code must have R E_{ia} proportional to I.
Es = [C1.conj().T @ sd[i][a] @ C0 for i in range(4) for a in range(3)]
constraints = []
for E in Es:
    for p in pauli_half:
        coeff = np.zeros((2, 9), complex)
        for u in range(2):
            for v in range(9):
                R = np.zeros((2, 9)); R[u, v] = 1
                coeff[u, v] = np.trace(p @ R @ E)
        constraints.append(coeff.ravel())
constraints = np.array(constraints)
singular = np.linalg.svd(constraints, compute_uv=False)
assert np.linalg.matrix_rank(constraints) == 18
results["perfect_unknown_error_recovery_constraints"] = dict(
    shape=list(constraints.shape), rank=18, unknowns=18,
    singular_values=[float(x) for x in singular],
    interpretation="Every accepted exact logical-identity recovery branch vanishes on all J=1")

# Coarse helper readout is enough: no assumptions on fine triplet operations.
# Kraus completeness from each actual unitary, including all four helper outputs.
d = r_magic(10); tau = 20*np.pi/np.sqrt(d*d+1)
H = np.kron(d*JD2/2, np.eye(4)) + np.kron(np.eye(16), d*JH2/2) + link[0]
U = expm(-1j*H*tau)
triplets = [np.array([1,0,0,0]), np.array([0,1,1,0])/np.sqrt(2), np.array([0,0,0,1])]
Ks = []
for state in [singlet]+triplets:
    Vout = np.kron(np.eye(16), state[:,None])
    Ks.append(Vout.conj().T@U@Vin)
complete = sum(K.conj().T@K for K in Ks)
results["helper_instrument_completeness_error"] = float(np.linalg.norm(complete-np.eye(16), 2))
assert results["helper_instrument_completeness_error"] < 2e-11

out = Path(__file__).with_name("exchange_erasure_results.json")
out.write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps({"file": str(out), "contact_parameter_sets": len(results["contacts"]),
                  "complete_sequences": len(results["sequences"]),
                  "constraint_rank": 18,
                  "max_clean_scalar_error": max(x["clean_code_scalar_residual"] for x in results["sequences"]),
                  "instrument_completeness_error": results["helper_instrument_completeness_error"]}, indent=2))
