"""Finite diagnostics for random conjugate involution frames.

This only checks the transcription of the frame covariance calculation on
small dimensions.  The dimension-uniform existence claim uses a matrix
Chernoff theorem and the proof recorded in random_frame_choi_witness.txt.
"""

import itertools
import json
import numpy as np


def pauli_basis(q):
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    mats = []
    for word in itertools.product((I, X, Y, Z), repeat=q):
        p = word[0]
        for a in word[1:]:
            p = np.kron(p, a)
        mats.append(p)
    return mats[1:]


def haar_unitary(rng, d):
    z = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    diag = np.diag(r)
    phases = np.where(np.abs(diag) > 0, diag / np.abs(diag), 1.0)
    return q @ np.diag(phases)


def run_case(q, multiplier, seed):
    rng = np.random.default_rng(seed)
    d = 2**q
    n = d * d - 1
    count = multiplier * n
    p = np.diag([1.0] * (d // 2) + [-1.0] * (d // 2)).astype(complex)
    basis = pauli_basis(q)
    coords = np.empty((count, n), dtype=float)
    for k in range(count):
        u = haar_unitary(rng, d)
        h = u @ p @ u.conj().T
        coords[k] = [float(np.trace(b @ h).real / d) for b in basis]
    frame = coords.T @ coords
    eig = np.linalg.eigvalsh(frame)
    kappa = count / n
    return {
        "d": d,
        "n_traceless": n,
        "samples": count,
        "seed": seed,
        "frame_mean_eigenvalue": float(np.trace(frame) / n),
        "target_kappa": kappa,
        "min_eigenvalue_over_kappa": float(eig[0] / kappa),
        "max_eigenvalue_over_kappa": float(eig[-1] / kappa),
        "max_hs_norm_error": float(np.max(np.abs(np.sum(coords * coords, axis=1) - 1.0))),
        "note": "finite diagnostic only; not a proof of random-frame concentration",
    }


if __name__ == "__main__":
    print(json.dumps({
        "generator": "numpy QR Haar-unitary prototype",
        "cases": [run_case(1, 40, 20261007), run_case(2, 24, 20261008), run_case(3, 16, 20261009)],
    }, indent=2, sort_keys=True))
