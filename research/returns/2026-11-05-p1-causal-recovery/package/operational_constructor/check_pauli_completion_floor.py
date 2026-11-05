"""Check the exact first-tick error floor of the Pauli-completed filter."""
import json
from pathlib import Path

import numpy as np

from check_crossing_gap import swap_matrix


I = np.eye(2, dtype=complex)
P = [I, np.array([[0, 1], [1, 0]], dtype=complex),
     np.array([[0, -1j], [1j, 0]], dtype=complex), np.diag([1, -1])]
bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
phi = np.outer(bell, bell.conj())


def kron(*matrices):
    result = np.ones((1, 1), dtype=complex)
    for matrix in matrices:
        result = np.kron(result, matrix)
    return result


def trace_e(matrix):
    return np.einsum("aibi->ab", matrix.reshape(8, 2, 8, 2))


def main():
    rows = []
    for theta in [0.02, 0.1, 0.4, 0.8, 1.2, 1.55, -0.4]:
        c, s = np.cos(theta), np.sin(theta)
        local_v = c * np.eye(4) - 2j * s * phi
        kraus = [local_v @ kron(p, I) / 2 for p in P]
        completeness_error = np.linalg.norm(sum(k.conj().T @ k for k in kraus) - np.eye(4))
        assert completeness_error < 1e-12
        u = c * np.eye(16) + 1j * s * swap_matrix(4, 0, 3)
        v = kron(I, I, local_v)
        initial = kron(P[3] / 2, phi, I / 2)
        delta = trace_e(v @ u @ initial @ u.conj().T @ v.conj().T)
        observed = float(np.sum(np.abs(np.linalg.eigvalsh(delta))))
        x = float(s * s)
        r = np.sqrt(4 * (1 - x) ** 4 + 4 * x - 3 * x * x)
        predicted = float((x + r) / 2)
        expected_spectrum = np.sort([
            -x / 8, -x / 8, x / 8, x / 8,
            -(r + 2 * (1 - x) ** 2) / 8,
            (r + 2 * (1 - x) ** 2) / 8,
            -(r - 2 * (1 - x) ** 2) / 8,
            (r - 2 * (1 - x) ** 2) / 8,
        ])
        spectrum_error = float(np.max(np.abs(np.linalg.eigvalsh(delta) - expected_spectrum)))
        assert spectrum_error < 1e-12
        assert abs(observed - predicted) < 1e-12
        assert predicted < 1
        rows.append({"theta": theta, "completeness_error": float(completeness_error),
                     "spectrum_error": spectrum_error, "observed_trace_distance": observed,
                     "predicted_trace_distance": predicted,
                     "irreversible_error_floor": float((1 - predicted) / 2)})
    target = Path(__file__).with_name("pauli_completion_floor_checks.json")
    target.write_text(json.dumps(rows, indent=2) + "\n")
    print(f"Seven angles passed; maximum spectral error {max(r['spectrum_error'] for r in rows):.3e}")
    print(f"Saved {target}")


if __name__ == "__main__":
    main()
