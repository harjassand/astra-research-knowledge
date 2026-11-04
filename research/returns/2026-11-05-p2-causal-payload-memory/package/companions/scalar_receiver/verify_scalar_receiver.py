"""Full-matrix check of the one-qubit receiver recurrence, not its proof."""
import json
from pathlib import Path
import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)


def swap(n, left, right):
    matrix = np.zeros((2**n, 2**n), complex)
    for before in range(2**n):
        bits = [(before >> (n - 1 - k)) & 1 for k in range(n)]
        bits[left], bits[right] = bits[right], bits[left]
        after = sum(v << (n - 1 - k) for k, v in enumerate(bits))
        matrix[after, before] = 1
    return matrix


W_SE, W_ME, I8 = swap(3, 0, 2), swap(3, 1, 2), np.eye(8)
BASIS = [np.kron(Z, I2), np.kron(I2, Z),
         np.kron(X, Y) - np.kron(Y, X)]


def direct_update(theta, phi):
    c, s, a, b = np.cos(theta), np.sin(theta), np.cos(phi), np.sin(phi)
    unitary = (a * I8 + 1j * b * W_ME) @ (c * I8 + 1j * s * W_SE)
    matrix = np.zeros((3, 3))
    residue = 0.0
    for col, operator in enumerate(BASIS):
        evolved = unitary @ np.kron(operator, I2) @ unitary.conj().T
        evolved = np.trace(evolved.reshape(4, 2, 4, 2),
                           axis1=1, axis2=3) / 2
        for row, basis in enumerate(BASIS):
            matrix[row, col] = (np.trace(basis.conj().T @ evolved)
                                / np.trace(basis.conj().T @ basis)).real
        residue = max(residue, np.linalg.norm(
            evolved - sum(matrix[row, col] * basis
                          for row, basis in enumerate(BASIS))))
    predicted = np.array([
        [c*c, 0, 0],
        [s*s*b*b, a*a, -2*s*s*a*b],
        [-c*s*b*b, 0, c*c*a*a+c*s*a*b],
    ])
    return float(np.max(np.abs(matrix - predicted))), float(residue)


def main():
    rng = np.random.default_rng(20261105)
    angles = [(0.1, 0.2), (0.3, -0.5), (0.7, 1.2)]
    angles += [(float(rng.uniform(0.001, 1.55)),
                float(rng.uniform(-np.pi, np.pi))) for _ in range(100)]
    errors = [direct_update(t, p) for t, p in angles]
    theta = 0.1
    c, s = np.cos(theta), np.sin(theta)
    bound = s * np.sqrt(1 / (1 + c*c) + 32*s*s / (3-c)**2)
    results = {
        "seed": 20261105,
        "matrix_comparisons": len(angles),
        "max_recurrence_entry_error": max(x[0] for x in errors),
        "max_invariant_subspace_residue": max(x[1] for x in errors),
        "theta": theta,
        "uniform_visibility_bound": float(bound),
        "half_diamond_error_lower_bound": float(0.75 * (1-bound)),
        "scope": "One tracial receiver qubit; predetermined scalar partial-SWAP updates only.",
    }
    assert results["max_recurrence_entry_error"] < 1e-12
    assert results["max_invariant_subspace_residue"] < 1e-12
    Path(__file__).with_name("scalar_receiver_verification.json").write_text(
        json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
