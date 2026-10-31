"""Audit three distinct measurement resources for the optical sideband branch.

Fixed Cartesian photon records, optimized first-photon measurement, and a
joint measurement of first and recovery photons are not interchangeable.
"""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent


def sqrt_hermitian(m):
    e, v = np.linalg.eigh((m+m.conj().T)/2)
    # Remove roundoff eigenvalues at the exactly rank-one B=1 endpoint.
    e = np.where(e > 1e-14*max(1., max(e)), e, 0.)
    return (v*np.sqrt(e))@v.conj().T


def choi(kraus):
    return sum(np.outer(k.reshape(-1, order="F"), k.reshape(-1, order="F").conj())
               for k in kraus)/2


def error(kraus):
    target = np.eye(2).reshape(-1, order="F")/np.sqrt(2)
    target = np.outer(target, target.conj())
    return float(np.sum(abs(np.linalg.eigvalsh(choi(kraus)-target)))/2)


def audit(b):
    eye = np.eye(2, dtype=complex)
    paulis = [eye, np.array([[0, 1], [1, 0]], complex),
              np.array([[0, -1j], [1j, 0]], complex), np.diag([1., -1.])]
    k0 = np.vstack([np.sqrt(1-b)*eye, np.zeros((1, 2))])
    k1 = np.zeros((3, 2), complex); k1[2, 0] = np.sqrt(b)
    k2 = np.zeros((3, 2), complex); k2[2, 1] = np.sqrt(b)
    ks = [k0, k1, k2]
    fourier = np.exp(2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
    measured = [sum(fourier[j, m]*ks[m] for m in range(3)) for j in range(3)]
    # The conditional polar isometry is undone by the recovery. The remaining
    # logical Kraus operator is sqrt(K^dagger K).
    corrected = [sqrt_hermitian(k.conj().T@k) for k in measured]
    assisted_fidelity = sum(abs(np.trace(k))**2 for k in corrected)/4
    predicted = (1+np.sqrt(1-b*b))/2
    cartesian = [np.sqrt(1-b)*eye]
    for j in range(2):
        k = np.zeros((2, 2)); k[j, j] = np.sqrt(b); cartesian.append(k)
    # After complete natural bright recovery: four bad Cartesian histories.
    matrix_units = []
    for k in range(2):
        for j in range(2):
            m = np.zeros((2, 2), complex); m[k, j] = np.sqrt(b/2)
            matrix_units.append(m)
    bell = np.array([[1, 0, 0, 1], [0, 1, 1, 0],
                     [0, -1j, 1j, 0], [1, 0, 0, -1]], complex)/np.sqrt(2)
    bell_kraus = [sum(bell[a, m]*matrix_units[m] for m in range(4)) for a in range(4)]
    pauli_residual = max(float(np.linalg.norm(k-np.sqrt(b)*p/2))
                         for k, p in zip(bell_kraus, paulis))
    feedforward = [np.sqrt(1-b)*eye]+[p.conj().T@k for p, k in zip(paulis, bell_kraus)]
    return {"harmful_probability": b,
            "fixed_cartesian_optimal_choi_error": error(cartesian),
            "first_photon_optimal_fidelity": float(assisted_fidelity.real),
            "first_photon_fidelity_formula": float(predicted),
            "first_photon_optimal_choi_error": error(corrected),
            "full_recovery_bell_measurement_pauli_residual": pauli_residual,
            "full_recovery_bell_measurement_choi_error": error(feedforward),
            "first_photon_trace_preservation_error": float(np.linalg.norm(sum(k.conj().T@k for k in corrected)-eye))}


if __name__ == "__main__":
    out = {"measurement_resources": [audit(b) for b in [0., .01, .1, 1376/3129, .5, 1.]]}
    (ROOT/"environment_recovery_results.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))
