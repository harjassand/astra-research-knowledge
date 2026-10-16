"""Numerical algebra check for the exact one-site qutrit recovery in FINITE_DISCHARGE.md.

This verifies finite identities; the theorem still relies on the analytic
Knill--Laflamme argument and its stated restricted fault model.
"""

from itertools import product

import numpy as np


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = {"I": I, "X": X, "Y": Y, "Z": Z}
GENERATORS = ("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ")


def tensor_word(word):
    out = np.array([[1]], dtype=complex)
    for char in word:
        out = np.kron(out, PAULI[char])
    return out


def tensor_power(matrix, n):
    out = np.array([[1]], dtype=complex)
    for _ in range(n):
        out = np.kron(out, matrix)
    return out


def basis_index(digits, radix):
    index = 0
    for digit in digits:
        index = radix * index + digit
    return index


def run():
    projector = np.eye(32, dtype=complex)
    for word in GENERATORS:
        projector = projector @ (np.eye(32) + tensor_word(word)) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    code_qubit = eigenvectors[:, eigenvalues > 0.5]
    assert code_qubit.shape == (32, 2)

    cyclic = (I - 1j * (X + Y + Z)) / 2
    assert np.allclose(cyclic.conj().T @ cyclic, I)
    assert np.allclose(cyclic @ X @ cyclic.conj().T, Y)
    assert np.allclose(cyclic @ Y @ cyclic.conj().T, Z)
    assert np.allclose(cyclic @ Z @ cyclic.conj().T, X)
    cyclic_five = tensor_power(cyclic, 5)
    assert np.allclose(
        cyclic_five @ code_qubit,
        code_qubit @ (code_qubit.conj().T @ cyclic_five @ code_qubit),
    )
    x_logical = code_qubit.conj().T @ tensor_word("XXXXX") @ code_qubit
    c_logical = code_qubit.conj().T @ cyclic_five @ code_qubit
    forward = c_logical @ x_logical
    reverse = x_logical @ c_logical
    channel_distance = np.linalg.norm(
        np.kron(forward, forward.conj()) - np.kron(reverse, reverse.conj())
    )
    assert channel_distance > 1

    # Embed qubit-sector code vectors into five qutrits. E_a V is enough for
    # the Gram calculation, avoiding 243-by-243 matrices for every E_a.
    code = np.zeros((3**5, 2), dtype=complex)
    bits_list = list(product((0, 1), repeat=5))
    for source_index, bits in enumerate(bits_list):
        code[basis_index(bits, 3)] = code_qubit[source_index]

    images = [code]
    for site in range(5):
        for output_symbol in range(3):
            for input_symbol in range(2):
                image = np.zeros_like(code)
                for source_index, bits in enumerate(bits_list):
                    if bits[site] != input_symbol:
                        continue
                    output_digits = list(bits)
                    output_digits[site] = output_symbol
                    image[basis_index(output_digits, 3)] += code_qubit[source_index]
                images.append(image)
    assert len(images) == 31

    gram = np.empty((31, 31), dtype=complex)
    scalar_residual = 0.0
    for a in range(31):
        for b in range(31):
            block = images[a].conj().T @ images[b]
            scalar = np.trace(block) / 2
            gram[a, b] = scalar
            scalar_residual = max(
                scalar_residual, np.linalg.norm(block - scalar * I)
            )
    assert scalar_residual < 1e-10

    values, vectors = np.linalg.eigh(gram)
    assert values.min() > -1e-10
    syndrome_isometries = []
    for mode, value in enumerate(values):
        if value <= 1e-9:
            continue
        operator = sum(
            vectors[a, mode] * images[a] for a in range(31)
        ) / np.sqrt(value)
        syndrome_isometries.append(operator)
    for i, wi in enumerate(syndrome_isometries):
        for j, wj in enumerate(syndrome_isometries):
            expected = I if i == j else np.zeros((2, 2))
            assert np.allclose(wi.conj().T @ wj, expected, atol=1e-9)

    print(
        {
            "error_basis_size": len(images),
            "syndrome_rank": len(syndrome_isometries),
            "max_KL_scalar_residual": scalar_residual,
            "noncommuting_channel_distance": channel_distance,
            "quantum_algebra": "PASS",
        }
    )


if __name__ == "__main__":
    run()
