"""Finite Gaussian-coordinate diagnostics for the all-normal form proof.

No infinite-bath infrared or finite-temperature heat claim is inferred.
"""

import json
import numpy as np


def check():
    h, maximum = 12, 8
    recoil, coupling, eta = 8.0, 0.4, 0.02
    hg = np.diag(np.arange(h) + 0.5)
    an = np.diag(np.sqrt(np.arange(1, h)), 1)
    y = (an + an.T) / np.sqrt(2)
    ih = np.eye(h)
    sx = np.array([[0.0, 1.0], [1.0, 0.0]])
    sz = np.diag([1.0, -1.0])
    z = 1.5
    gamma = np.sqrt(2 / recoil + 1 / recoil**2)  # C=1,Vg=1/2
    q = 2 * coupling * gamma
    assert q <= 0.5

    def resolvent(n, sign, energy=z):
        d = np.arange(1, n + 1) + 0.5
        t = np.diag(np.ones(n - 1), 1) + np.diag(np.ones(n - 1), -1)
        mat = np.kron(np.eye(n), hg) + recoil * np.kron(np.diag((d + sign * eta)**2), ih)
        mat -= coupling * np.kron(t, y)
        mat = mat.astype(complex) - energy * np.eye(n * h)
        return np.linalg.inv(mat)

    full_r = {s: resolvent(maximum, s) for s in [1, -1]}
    sigma = {s: coupling**2 * y @ full_r[s][:h, :h] @ y for s in [1, -1]}
    sigma0 = (sigma[1] + sigma[-1]) / 2
    sigmax = (sigma[1] - sigma[-1]) / 2
    rows = []
    for n in [1, 2, 3]:
        rn = resolvent(n, 1)[:h, :h]
        diff = full_r[1][:h, :h] - rn
        actual = float(np.linalg.norm(diff, 2))
        bound = q**(2 * n) / (recoil * (1 - q))
        assert actual <= bound
        assert np.linalg.eigvalsh(diff)[0] > -1e-12
        rows.append({"excited_levels": n, "observed_first_block_error": actual, "proved_upper": bound})

    d = np.arange(maximum + 1) + 0.5
    adjacency = np.diag(np.ones(maximum), 1) + np.diag(np.ones(maximum), -1)
    boundary = np.zeros((maximum + 1, maximum + 1))
    boundary[0, 0] = 1
    ident = np.eye((maximum + 1) * h * 2)
    full_h = np.kron(np.eye(maximum + 1), np.kron(hg, np.eye(2)))
    full_h += recoil * np.kron(np.diag(d**2), np.kron(ih, np.eye(2)))
    full_h -= coupling * np.kron(adjacency, np.kron(y, np.eye(2)))
    full_h -= coupling * np.kron(boundary, np.kron(y, sz))
    full_h += 2 * recoil * eta * np.kron(np.diag(d), np.kron(ih, sx))
    full_h += recoil * eta**2 * ident
    actual_p = np.linalg.inv(full_h - z * ident)[:2*h, :2*h]
    schur = np.kron(hg + (recoil / 4 + recoil * eta**2 - z) * ih - sigma0, np.eye(2))
    schur += np.kron(recoil * eta * ih - sigmax, sx) - coupling * np.kron(y, sz)
    error = float(np.linalg.norm(actual_p - np.linalg.inv(schur), 2))
    assert error < 1e-11

    common_upper = 2 * coupling**2 / recoil * (y @ y) - sigma0
    relative_upper = 16 * coupling**2 * eta / recoil * (y @ y) + sigmax
    assert np.linalg.eigvalsh(common_upper)[0] > -1e-11
    assert np.linalg.eigvalsh(-sigmax)[0] > -1e-11
    assert np.linalg.eigvalsh(relative_upper)[0] > -1e-11
    for s in [1, -1]:
        prime = coupling**2 * y @ (full_r[s] @ full_r[s])[:h, :h] @ y
        assert np.linalg.eigvalsh(4 * coupling**2 / recoil**2 * (y @ y) - prime)[0] > -1e-11

    complex_z = z + 0.3j
    complex_diff = resolvent(maximum, 1, complex_z)[:h, :h] - resolvent(2, 1, complex_z)[:h, :h]
    complex_error = float(np.linalg.norm(complex_diff, 2))
    complex_bound = q**4 / (recoil * (1 - q))
    assert complex_error < complex_bound
    return {
        "relative_walk_majorant_q": float(q),
        "normal_truncation_checks": rows,
        "full_Schur_resolvent_difference": error,
        "transverse_selfenergy_max_eigenvalue": float(np.linalg.eigvalsh(sigmax)[-1]),
        "relative_transverse_bound_min_margin": float(np.linalg.eigvalsh(relative_upper)[0]),
        "complex_normal_error": complex_error,
        "complex_normal_upper_bound": complex_bound,
        "all_assertions": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
