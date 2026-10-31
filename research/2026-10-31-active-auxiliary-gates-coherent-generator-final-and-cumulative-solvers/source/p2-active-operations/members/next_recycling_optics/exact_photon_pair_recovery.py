"""Exact static photon-pair recovery algebra in the actual split 12-level model.

The outlet is the stipulated D_l^dagger tensor I_source model. Coherent
collection and a Bell measurement of two x/y photons are additional resources.
"""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import expm, norm

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from recycling_and_sidebands import operators


def embeddings():
    c = np.zeros((12, 6), complex)
    for j in range(2):
        c[j, 3*j] = 1
        c[3+6+j, 3*j+1] = 1  # e_zj
        c[3+3*j+2, 3*j+2] = 1  # e_jz
    b = np.zeros((12, 3), complex)
    b[2, 0] = 1; b[11, 1] = 1
    b[3, 2] = b[7, 2] = 1/np.sqrt(2)
    return c, b


def audit():
    d1, d2, gamma = 20., 22., 1.
    h0, v, js = operators(d1, d2, gamma)
    c, b = embeddings(); n = np.column_stack([c, b])
    sx = np.array([[0., 1.], [1., 0.]])
    sy = np.array([[0., -1j], [1j, 0.]])
    sz = np.diag([1., -1.]); ie = np.eye(2)
    ce = np.kron(c, ie); be = np.kron(b, ie); ne = np.kron(n, ie)
    ae = ie+.17*sx+.11j*sz
    he = .37*sx+2.41*sz

    def hamiltonian(a, source):
        return (np.kron(h0, ie)+np.kron(v, a)+np.kron(v.conj().T, a.conj().T)
                +np.kron(np.eye(12), source))

    h = hamiltonian(ae, he)
    au = np.array([[0, 0, 0], [0, (d1+d2)/2, (d2-d1)/2],
                   [0, (d2-d1)/2, (d1+d2)/2]], complex)
    lift = np.zeros((3, 3), complex); lift[1, 0] = np.sqrt(3)
    hc = (np.kron(au, ie)+np.kron(lift, ae)+np.kron(lift.conj().T, ae.conj().T)
          +np.kron(np.eye(3), he))
    br = np.array([[0, 0, 0], [0, 2*d2/3, -np.sqrt(2)*d2/3],
                   [0, -np.sqrt(2)*d2/3, d2/3]], complex)
    hb = (np.kron(br, ie)+np.kron(lift, ae)+np.kron(lift.conj().T, ae.conj().T)
          +np.kron(np.eye(3), he))
    out = {
        "reachable_isometry_error": float(norm(n.conj().T@n-np.eye(9))),
        "reachable_H_closure_error": float(norm(h@ne-ne@(ne.conj().T@h@ne))),
        "logical_auxiliary_H_factorization_error": float(norm(h@ce-ce@np.kron(np.eye(2), hc))),
        "bright_chain_H_error": float(norm(h@be-be@hb)),
        "reachable_jump_closure_error": max(float(norm(j@n-n@(n.conj().T@j@n))) for j in js),
    }
    jz = np.zeros((3, 3)); jz[0, 1] = np.sqrt(gamma)
    out["safe_z_jump_factorization_error"] = float(norm(js[2]@c-c@np.kron(np.eye(2), jz)))
    swap_errors = []
    for j in range(2):
        cb = np.zeros((3, 6)); cb[0, 3*j+2] = np.sqrt(gamma)
        bc = np.zeros((6, 3)); bc[3*j, 2] = np.sqrt(gamma/2)
        swap_errors.append(float(norm(js[j]@c-b@cb)))
        swap_errors.append(float(norm(js[j]@b-c@bc)))
    out["xy_transfer_and_entangler_errors"] = swap_errors

    # A fine pair history with safe z recycling on each side and a changing,
    # noncommuting complex quantum gain. Matrix identity, not a chosen state.
    pe = np.kron(sum(j.conj().T@j for j in js), ie)
    je = [np.kron(j, ie) for j in js]
    def no_photon(a, source, time):
        return expm((-1j*hamiltonian(a, source)-pe/2)*time)
    a2 = ie-.13*sz+.09j*sx
    he2 = -1.73*sx+.22*sy
    nc = no_photon(a2, he2, .31)@je[2]@no_photon(ae, he, .17)
    nb = no_photon(ae, he2, .43)@je[2]@no_photon(a2, he, .29)
    pair = [ce.conj().T@je[k]@nb@je[j]@nc@ce for k in range(2) for j in range(2)]
    common = pair[0][:6, :6]
    factor_errors = []
    for k in range(2):
        for j in range(2):
            unit = np.zeros((2, 2)); unit[k, j] = 1
            factor_errors.append(float(norm(pair[2*k+j]-np.kron(unit, common))))
    out["pair_history_logical_matrix_unit_factorization_errors"] = factor_errors
    out["common_history_operator_norm"] = float(norm(common))
    bell = np.array([[1, 0, 0, 1], [0, 1, 1, 0],
                     [0, -1j, 1j, 0], [1, 0, 0, -1]], complex)/np.sqrt(2)
    paulis = [ie, sx, sy, sz]
    rec = []
    for p, coeff in zip(paulis, bell):
        kh = sum(coeff[j]*pair[j] for j in range(4))
        corrected = np.kron(p.conj().T, np.eye(6))@kh
        rec.append(float(norm(corrected-np.kron(ie, common)/np.sqrt(2))))
    out["bell_measurement_corrected_identity_factorization_errors"] = rec
    return out


if __name__ == "__main__":
    out = audit()
    (ROOT/"exact_photon_pair_recovery_results.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))
