"""Small exact-structure diagnostics for the c05_l04 initial attack.

The symbolic proofs are in INITIAL.txt. This script checks the Pauli Choi
witness spectra and one instrument-derived self-compatible channel in small
dimensions; it does not certify any growing-dimension statement.
"""

import itertools
import numpy as np


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = (I2, X, Y, Z)


def pauli_basis(qubits):
    result = []
    for labels in itertools.product(range(4), repeat=qubits):
        if any(labels):
            result.append(kron_all([PAULI[i] for i in labels]))
    return result


def kron_all(items):
    result = items[0]
    for item in items[1:]:
        result = np.kron(result, item)
    return result


def pauli_witness(qubits):
    basis = pauli_basis(qubits)
    d = 2**qubits
    eye = np.eye(d, dtype=complex)
    witness = np.zeros((d**3, d**3), dtype=complex)
    for p in basis:
        witness += np.kron(p.T, np.kron(p, eye))
        witness += np.kron(p.T, np.kron(eye, p))
    eigenvalues = np.linalg.eigvalsh(witness)
    expected = d * d + d - 2
    return d, len(basis), float(eigenvalues[-1]), float(eigenvalues[0]), expected


def superoperator(channel, d):
    columns = []
    for j in range(d * d):
        e = np.zeros((d, d), dtype=complex)
        e.flat[j] = 1
        columns.append(channel(e).flatten())
    return np.column_stack(columns)


def instrument_example(p=0.37):
    d = 2
    # A bistochastic random-unitary instrument with Kraus operators
    # sqrt(p) I and sqrt(1-p) X. Its effects are scalar multiples of I,
    # so the canonical measurement channel is depolarizing.
    unitaries = ((p, I2), (1 - p, X))

    def L(a):
        return sum(weight * u @ a @ u.conj().T for weight, u in unitaries)

    def D(a):
        return np.trace(a) * I2 / d

    C = (superoperator(L, d) + superoperator(D, d)) / 2
    Phi = C.conj().T @ C
    traceless = [X, Y, Z]
    ratios = []
    for a in traceless:
        out = (Phi @ a.flatten()).reshape((d, d))
        ratios.append(np.linalg.norm(out, "fro") / np.linalg.norm(a, "fro"))
    return max(ratios)


if __name__ == "__main__":
    for q in (1, 2, 3):
        print("pauli_witness", pauli_witness(q))
    print("instrument_traceless_2_to_2", instrument_example())
    print("instrument_bound", 0.25)
