#!/usr/bin/env python3
"""Finite matrix diagnostics for the sourced three-spin path inequality."""
import json
import numpy as np


def spin_matrices(S: float):
    d = round(2 * S + 1)
    labels = [S - k for k in range(d)]
    plus = np.zeros((d, d), dtype=complex)
    for col, m in enumerate(labels):
        m_up = m + 1
        if m_up in labels:
            row = labels.index(m_up)
            plus[row, col] = np.sqrt(S * (S + 1) - m * (m + 1))
    minus = plus.conj().T
    sx = (plus + minus) / 2
    sy = (plus - minus) / (2j)
    sz = np.diag(labels).astype(complex)
    return sx, sy, sz


def check(S: float) -> dict:
    spins = spin_matrices(S)
    d = len(spins[0])
    ident = np.eye(d, dtype=complex)

    def dot(i: int, j: int):
        out = np.zeros((d**3, d**3), dtype=complex)
        for axis in range(3):
            factors = [ident, ident, ident]
            factors[i] = spins[axis]
            factors[j] = spins[axis]
            term = factors[0]
            for factor in factors[1:]:
                term = np.kron(term, factor)
            out += term
        return out

    q01 = S**2 * np.eye(d**3) - dot(0, 1)
    q12 = S**2 * np.eye(d**3) - dot(1, 2)
    q02 = S**2 * np.eye(d**3) - dot(0, 2)
    test = q01 + q12 - 0.5 * q02
    eigen_min = float(np.linalg.eigvalsh(test).min())
    return {"S": S, "dimension": d**3, "min_eigenvalue": eigen_min,
            "pass_with_1e-10_tolerance": eigen_min >= -1e-10}


def main():
    rows = [check(S) for S in (0.5, 1.0, 1.5, 2.0)]
    print(json.dumps({"rows": rows,
                      "status": "PASS" if all(r["pass_with_1e-10_tolerance"] for r in rows) else "FAIL"},
                     indent=2))


if __name__ == "__main__":
    main()
