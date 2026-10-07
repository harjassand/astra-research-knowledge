#!/usr/bin/env python3
"""Small spin-1 diagnostic for the positive forward/reverse split."""
import json
import numpy as np


def superop_exp(a, t):
    vals, vecs = np.linalg.eigh((a + a.conj().T) / 2)
    return (vecs * np.exp(t * vals)) @ vecs.conj().T


def spin_one():
    jp = np.array([[0, np.sqrt(2), 0], [0, 0, np.sqrt(2)], [0, 0, 0]], complex)
    jm = jp.conj().T
    return [(jp + jm) / 2, (jp - jm) / (2j), np.diag([1, 0, -1]).astype(complex)]


def to_matrix(v, d):
    return np.asarray(v).reshape((d, d), order="F")


def normalized(v, d):
    x = to_matrix(v, d)
    return x / np.trace(x)


def trace_distance(x, y):
    return float(0.5 * np.linalg.svd(x - y, compute_uv=False).sum())


def main():
    n = 8
    j = 1
    d = 2 * j + 1
    spins = spin_one()
    lambdas = [0.2, 0.4, 0.7]
    b = np.array([0.3, -0.2, 0.1])
    c = np.array(lambdas) / n**1.5
    v = b / n**0.75
    f2 = [f @ f for f in spins]
    h = sum(c[i] * f2[i] for i in range(3)) + sum(v[i] * spins[i] for i in range(3))
    ident = np.eye(d, dtype=complex)
    eye_super = np.eye(d * d, dtype=complex)

    # Column-vectorization convention: vec(A X B)=(B.T kron A)vec(X).
    l0 = 0.5 * (np.kron(ident, h) + np.kron(h.T, ident))
    lis = []
    for i, f in enumerate(spins):
        lis.append(c[i] / 4 * (np.kron(ident, f2[i]) + 2 * np.kron(f.T, f) + np.kron(f2[i].T, ident)))
    components = [l0] + lis
    total = sum(components)
    exact_map = superop_exp(total, 1.0)
    id_vec = ident.reshape(-1, order="F")
    exact_state = normalized(exact_map @ id_vec, d)

    rows = []
    for m in [1, 2, 4, 8, 16, 32, 64]:
        step = 1.0 / m
        forward = eye_super.copy()
        reverse = eye_super.copy()
        for a in components:
            forward = forward @ superop_exp(a, step)
        for a in reversed(components):
            reverse = reverse @ superop_exp(a, step)
        sym = (forward + reverse) / 2
        first_state = normalized(np.linalg.matrix_power(forward, m) @ id_vec, d)
        sym_state = normalized(np.linalg.matrix_power(sym, m) @ id_vec, d)
        first_err = trace_distance(first_state, exact_state)
        sym_err = trace_distance(sym_state, exact_state)
        eigmin = float(np.linalg.eigvalsh((to_matrix(np.linalg.matrix_power(sym, m) @ id_vec, d) + to_matrix(np.linalg.matrix_power(sym, m) @ id_vec, d).conj().T) / 2).min())
        rows.append({"m": m, "first_order_trace_distance": first_err, "symmetrized_trace_distance": sym_err,
                     "m_times_first_error": m * first_err, "m2_times_symmetrized_error": m * m * sym_err,
                     "minimum_unnormalized_eigenvalue": eigmin})

    print(json.dumps({"diagnostic": "spin-1 finite-sector only; floating-point evidence, not proof",
                      "N_label": n, "spin_sector": j, "A_plus_MI_eigenvalues": lambdas,
                      "b": b.tolist(), "results": rows}, indent=2))


if __name__ == "__main__":
    main()
