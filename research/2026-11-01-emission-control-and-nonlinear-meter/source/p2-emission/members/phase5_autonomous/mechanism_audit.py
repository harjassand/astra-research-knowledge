"""Small, no-jump-complete audits of the autonomous/parity route.

This is an exactly specified effective model, not a full cat-device simulation.
It tests what the proposed mechanism protects and deliberately probes failures.
Requires numpy and scipy. Writes results.json beside this file.
"""
from pathlib import Path
import itertools
import json
import math
import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import expm_multiply


def lindblad(H, jumps):
    d = H.shape[0]
    eye = sp.eye(d, format="csr")
    L = -1j * (sp.kron(eye, H) - sp.kron(H.T, eye))
    for J in jumps:
        Q = J.conj().T @ J
        L += sp.kron(J.conj(), J) - 0.5 * sp.kron(eye, Q) - 0.5 * sp.kron(Q.T, eye)
    return L.tocsr()


def evolve(rho, H, jumps, duration):
    d = rho.shape[0]
    return expm_multiply(lindblad(H, jumps) * duration,
                        rho.reshape(-1, order="F")).reshape((d, d), order="F")


def reservoir_audit(nb=14):
    I4 = sp.eye(4, format="csr")
    ib = sp.eye(nb, format="csr")
    A = sp.diags([1, -1, -1, 1], format="csr")  # Z tensor Z
    b = sp.diags(np.sqrt(np.arange(1, nb)), 1, shape=(nb, nb), format="csr")
    n = b.conj().T @ b
    Aall = sp.kron(A, ib).tocsr()
    Ball = sp.kron(I4, b).tocsr()
    Nall = sp.kron(I4, n).tocsr()
    kappa, drive, T, theta = 1.0, 0.25, 8.0, np.pi / 4
    Hgate = (theta / (2 * T)) * Aall + drive * sp.kron(A, b + b.conj().T)
    Hidle = sp.csr_matrix(Hgate.shape, dtype=complex)
    psi0 = np.zeros(4 * nb, dtype=complex)
    psi0[::nb] = 0.5
    rho0 = np.outer(psi0, psi0.conj())
    psiideal = 0.5 * np.exp(-0.5j * theta * np.array([1, -1, -1, 1]))
    parity = sp.diags((-1.0)**np.arange(nb), format="csr")
    Pp, Pm = (I4 + A) / 2, (I4 - A) / 2
    U = sp.kron(Pp, ib) + sp.kron(Pm, parity)
    Jcorr = np.sqrt(kappa) * sp.kron(A, b).tocsr()
    factorization_residual = float(sp.linalg.norm(U @ Jcorr @ U - Ball))
    factorization_H_residual = float(sp.linalg.norm(
        U @ Hgate @ U - (theta / (2 * T) * Aall + drive * sp.kron(I4, b + b.conj().T))))

    def metrics(rho):
        rd = np.trace(rho.reshape(4, nb, 4, nb), axis1=1, axis2=3)
        fidelity = float(np.real(psiideal.conj() @ rd @ psiideal))
        return {"state_infidelity": 1 - fidelity,
                "trace": float(np.real(np.trace(rho))),
                "mean_buffer_n": float(np.real(np.trace(Nall @ rho)))}

    cases = {
        "ordinary_buffer_loss": [np.sqrt(kappa) * Ball],
        "corrected_buffer_loss": [Jcorr],
        "corrected_plus_buffer_dephasing_0.15": [Jcorr, np.sqrt(0.15) * Nall],
        "corrected_plus_physical_heating_0.001": [Jcorr, np.sqrt(0.001) * Ball.conj().T],
        "90_percent_corrected_10_percent_ordinary_loss": [np.sqrt(0.9) * Jcorr, np.sqrt(0.1) * Ball],
    }
    result = {"parameters": {"buffer_cutoff": nb, "kappa": kappa, "drive": drive,
                              "gate_duration": T, "theta": theta},
              "factorization_jump_residual": factorization_residual,
              "factorization_H_residual": factorization_H_residual,
              "cases": {}}
    for name, jumps in cases.items():
        rho_gate = evolve(rho0, Hgate, jumps, T)
        table = {"at_gate_end": metrics(rho_gate)}
        for tr in (6.0, 12.0, 24.0):
            table[f"after_ringdown_{tr:g}"] = metrics(evolve(rho_gate, Hidle, jumps, tr))
        result["cases"][name] = table

    # A tiny defect in the correction operator makes the silent/no-jump branch
    # state dependent. Full non-Hermitian propagation, no post-hoc projection.
    result["no_jump_branches"] = {}
    for eps in (0.0, 0.1, 0.25):
        J = sp.kron(A + eps * I4, b).tocsr()
        Q = J.conj().T @ J
        psig = expm_multiply((-1j * Hgate - 0.5 * Q) * T, psi0)
        psif = expm_multiply(-0.5 * Q * 24.0, psig)
        prob = float(np.real(np.vdot(psif, psif)))
        rf = np.outer(psif, psif.conj()) / prob
        result["no_jump_branches"][str(eps)] = {"probability": prob, **metrics(rf)}
    return result


def parity_cnot_audit():
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.diag([1, -1])
    paulis = {"I": I, "X": X, "Y": Y, "Z": Z}
    kron = np.kron
    ZZca = kron(kron(Z, Z), I)
    XXat = kron(kron(I, X), X)
    vplus = np.array([1, 1]) / np.sqrt(2)
    prep = kron(kron(I, vplus[:, None]), I)
    cn = np.array([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]])
    eye8 = np.eye(8)
    def K(records, fault_position=None, fault=None, reported=None):
        m1, m2, m3 = records
        R1, R2 = (eye8 + m1 * ZZca)/2, (eye8 + m2 * XXat)/2
        zbra = np.array([1,0]) if m3 == 1 else np.array([0,1])
        measure = kron(kron(I, zbra[None,:]), I)
        ops = [prep, R1, R2, measure]
        if fault_position is not None:
            ops[fault_position] = fault @ ops[fault_position]
        out = ops[3] @ ops[2] @ ops[1] @ ops[0]
        r1, r2, r3 = records if reported is None else reported
        corr = kron(Z if r2 == -1 else I, X if r1*r3 == -1 else I)
        return corr @ out
    def error_label(k):
        err = k @ cn.conj().T
        coeffs = {a+b: np.trace(kron(paulis[a],paulis[b]).conj().T @ err)/4
                  for a in paulis for b in paulis}
        active = {p:complex(c) for p,c in coeffs.items() if abs(c)>1e-10}
        return sorted(active)
    records_list = list(itertools.product((1,-1), repeat=3))
    ideal_residual = max(float(np.linalg.norm(K(r) @ cn.conj().T -
                    np.trace(K(r) @ cn.conj().T)/4*np.eye(4))) for r in records_list)
    phase_faults = {}
    for pos in (0,1,2):
        for q in range(3):
            ops = [I,I,I]
            ops[q] = Z
            fault = kron(kron(ops[0],ops[1]),ops[2])
            phase_faults[f"after_stage_{pos}_Z_on_{'cat'[q]}"] = sorted(set(
                lab for r in records_list for lab in error_label(K(r,pos,fault))))
    record_faults = {}
    for j in range(3):
        labs = set()
        for r in records_list:
            reported = list(r); reported[j] *= -1
            labs.update(error_label(K(r,reported=reported)))
        record_faults[f"flip_record_{j+1}"] = sorted(labs)
    readout_majority = {}
    for q in (0.001, 0.01, 0.05):
        readout_majority[str(q)] = {
            str(r):sum(math.comb(r,k)*q**k*(1-q)**(r-k) for k in range((r+1)//2,r+1))
            for r in (1,3,5,7,9,11)}
    return {"ideal_all_branches_scalar_CNOT_residual":ideal_residual,
            "phase_fault_output_Paulis":phase_faults,
            "wrong_record_output_Paulis":record_faults,
            "independent_readout_majority_error":readout_majority}


if __name__ == "__main__":
    result = {"scope":"Effective-model mechanism audit; not a device or threshold certification.",
              "reservoir":reservoir_audit(),"measurement_CNOT":parity_cnot_audit()}
    dest = Path(__file__).with_name("results.json")
    dest.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
