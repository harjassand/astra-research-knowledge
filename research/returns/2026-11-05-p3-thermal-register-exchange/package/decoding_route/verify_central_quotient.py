"""Independent finite-matrix check of central-parity Gibbs transduction.

The proof is algebraic; this computation checks its realization for four cells.
"""

import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm


def bits(value, width):
    return np.array([(value >> i) & 1 for i in range(width)], dtype=np.uint8)


def pauli_term(n, z_positions=(), x_position=None):
    dim = 1 << n
    out = np.zeros((dim, dim), dtype=float)
    z_mask = sum(1 << j for j in z_positions)
    x_mask = 0 if x_position is None else 1 << x_position
    for col in range(dim):
        sign = -1.0 if (col & z_mask).bit_count() % 2 else 1.0
        out[col ^ x_mask, col] = sign
    return out


def main():
    # Vertex order is the row-snake source chain on a 2 x 2 grid:
    # coordinates (0,0), (0,1), (1,1), (1,0).
    n = 4
    source_path = [(0, 1), (1, 2), (2, 3)]
    tree_edges = [(0, 3), (3, 2), (2, 1)]  # Column-snake tree.
    incidence = np.zeros((n - 1, n), dtype=np.uint8)
    for e, (u, v) in enumerate(tree_edges):
        incidence[e, u] = incidence[e, v] = 1

    x = np.array([0.31, -0.47, 0.59, -0.23])
    z = np.array([-0.19, 0.41, -0.37, 0.29])
    c = np.array([0.17, -0.13, 0.11, -0.07])
    cq = np.array([-0.43, 0.53, -0.61, 0.39])
    zz = np.array([0.67, -0.71, 0.73])
    ha = np.zeros((1 << (2 * n),) * 2, dtype=float)
    hb = np.zeros((1 << (2 * n - 1),) * 2, dtype=float)
    for i in range(n):
        ha += x[i] * pauli_term(2 * n, x_position=i)
        hb += x[i] * pauli_term(2 * n - 1, x_position=i)
        ha += z[i] * pauli_term(2 * n, z_positions=(i,))
        hb += z[i] * pauli_term(2 * n - 1, z_positions=(i,))
        ha += c[i] * pauli_term(2 * n, z_positions=(n + i,))
        ha += cq[i] * pauli_term(2 * n, z_positions=(i, n + i))
        incident = tuple(n + int(e) for e in np.flatnonzero(incidence[:, i]))
        hb += c[i] * pauli_term(2 * n - 1, z_positions=incident)
        hb += cq[i] * pauli_term(2 * n - 1, z_positions=(i,) + incident)
    for j, (u, v) in enumerate(source_path):
        ha += zz[j] * pauli_term(2 * n, z_positions=(u, v))
        hb += zz[j] * pauli_term(2 * n - 1, z_positions=(u, v))

    # V maps target edge bits r to source vertex bits c = F^T r.
    v = np.zeros((ha.shape[0], hb.shape[0]), dtype=float)
    for col in range(hb.shape[0]):
        q = col & ((1 << n) - 1)
        r = bits(col >> n, n - 1)
        vertex = (incidence.T @ r) % 2
        c_int = sum(int(vertex[i]) << i for i in range(n))
        v[q + (c_int << n), col] = 1.0

    projector = v @ v.T
    errors = {
        "isometry": float(np.max(np.abs(v.T @ v - np.eye(hb.shape[0])))),
        "Hamiltonian_intertwining": float(np.max(np.abs(ha @ v - v @ hb))),
        "sector_commutator": float(np.max(np.abs(ha @ projector - projector @ ha))),
    }
    delta = float(np.min(2 * (np.abs(c) + np.abs(cq))))
    rows = []
    for beta in [0.0, 0.2, 1.0, 3.0, 8.0]:
        ga = expm(-beta * ha)
        gb = expm(-beta * hb)
        za = float(np.trace(ga))
        zb = float(np.trace(gb))
        p = float(np.trace(projector @ ga) / za)
        rho_cond = (v.T @ ga @ v) / float(np.trace(projector @ ga))
        rho_target = gb / zb
        error = float(np.linalg.norm(rho_cond - rho_target, ord="nuc") / 2)
        bound = float(1 / (1 + np.exp(beta * delta)))
        rows.append({"beta": beta, "sector_probability": p,
                     "proved_lower_bound": bound,
                     "trace_distance": error})
        assert p + 1e-12 >= bound
        assert error < 1e-10
    assert max(errors.values()) < 1e-12
    report = {"n_vertices": n, "source_qubits": 2 * n,
              "target_qubits": 2 * n - 1,
              "tree_incidence": incidence.tolist(),
              "uniform_sector_energy_shift_bound": delta,
              "algebraic_errors": errors,
              "thermal_checks": rows}
    Path(__file__).with_name("central_quotient_verification.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
