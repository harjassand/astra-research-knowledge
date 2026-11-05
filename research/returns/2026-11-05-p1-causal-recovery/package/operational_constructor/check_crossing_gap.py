"""Finite numerical audit of crossing/interpolation and the cycle estimate.

The theorem is proved in crossing_gap_proof.md. These checks are corroboration,
not a replacement for that proof. Requires only NumPy. Run with Python 3.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def swap_matrix(qubits: int, first: int, second: int) -> np.ndarray:
    dim = 1 << qubits
    result = np.zeros((dim, dim), dtype=complex)
    mask_first = 1 << (qubits - 1 - first)
    mask_second = 1 << (qubits - 1 - second)
    for column in range(dim):
        row = column
        if bool(column & mask_first) != bool(column & mask_second):
            row ^= mask_first | mask_second
        result[row, column] = 1
    return result


def monodromy(n: int, z: complex) -> np.ndarray:
    dim = 1 << (n + 1)
    result = np.eye(dim, dtype=complex)
    for site in range(1, n + 1):
        result = (z * np.eye(dim) + 1j * swap_matrix(n + 1, 0, site)) @ result
    return result


def crossing(matrix: np.ndarray) -> np.ndarray:
    bath_dim = matrix.shape[0] // 2
    transposed = matrix.reshape(2, bath_dim, 2, bath_dim).transpose(2, 1, 0, 3)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    rotation = np.kron(sy, np.eye(bath_dim))
    return rotation @ transposed.reshape(matrix.shape) @ rotation


def normalized_hs(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix) / np.sqrt(matrix.shape[0]))


def relative_error(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(np.linalg.norm(left), np.linalg.norm(right), 1e-300))


def bath_channel(unitary: np.ndarray, x: np.ndarray) -> np.ndarray:
    d = x.shape[0]
    blocks = unitary.reshape(2, d, 2, d)
    result = np.zeros_like(x, dtype=complex)
    for a in range(2):
        for b in range(2):
            k = blocks[a, :, b, :]
            result += k @ x @ k.conj().T / 2
    return result


def bath_superoperator(unitary: np.ndarray) -> np.ndarray:
    d = unitary.shape[0] // 2
    blocks = unitary.reshape(2, d, 2, d)
    result = np.zeros((d * d, d * d), dtype=complex)
    for a in range(2):
        for b in range(2):
            k = blocks[a, :, b, :]
            result += np.kron(k.conj(), k) / 2
    return result


def cycle_minimum(n: int) -> dict:
    d = 1 << n
    cycle = monodromy(n, 0) / (1j ** n)
    columns = []
    for column in range(d):
        for row in range(d):
            x = np.zeros((d, d), dtype=complex)
            x[row, column] = 1
            xb = np.kron(np.eye(2), x)
            change = cycle @ xb @ cycle.conj().T - xb
            columns.append(change.reshape(-1, order="F") / np.sqrt(2))
    differential = np.stack(columns, axis=1)
    eigenvalues = np.linalg.eigvalsh(differential.conj().T @ differential)
    alpha = 4 * math.sin(math.pi / (2 * (n + 1))) ** 2
    assert abs(float(eigenvalues[0])) < 1e-11
    assert abs(float(eigenvalues[1]) - alpha) < 1e-11
    return {"n": n, "observed_cycle_gap": float(eigenvalues[1]), "alpha_n": alpha}


def check_instance(n: int, u: float, rng: np.random.Generator) -> dict:
    d = 1 << n
    raw = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    x = (raw + raw.conj().T) / 2
    x -= np.trace(x) * np.eye(d) / d
    x /= normalized_hs(x)
    unitary = monodromy(n, u) / ((u * u + 1) ** (n / 2))
    y = bath_channel(unitary, x)
    xb, yb = np.kron(np.eye(2), x), np.kron(np.eye(2), y)
    delta = normalized_hs(unitary @ xb - yb @ unitary)
    projection_error = abs(delta * delta - (1 - normalized_hs(y) ** 2))
    assert projection_error < 1e-11

    def defect(z: complex, swap: bool = False) -> np.ndarray:
        t = monodromy(n, z)
        left, right = (yb, xb) if swap else (xb, yb)
        return t @ left - right @ t

    crossing_errors, intertwining_errors, propagation_ratios = [], [], []
    for k in range(2 * n):
        z = u - 1j * k
        t = monodromy(n, z)
        inverse = np.linalg.inv(t)
        lhs = crossing(monodromy(n, z - 1j))
        rhs = (z * z + 1) ** n * inverse
        crossing_errors.append(relative_error(lhs, rhs))
        lhs_d = defect(z - 1j, swap=((k + 1) % 2 == 1))
        rhs_d = -(z * z + 1) ** n * crossing(inverse @ defect(z, swap=(k % 2 == 1)) @ inverse)
        intertwining_errors.append(relative_error(lhs_d, rhs_d))
        m = k + 1
        bound = (((u * u + (m - 1) ** 2) * (u * u + m * m)) / (u * u)) ** (n / 2) * delta
        propagation_ratios.append(normalized_hs(lhs_d) / bound)
    assert max(crossing_errors) < 1e-10
    assert max(intertwining_errors) < 1e-10
    assert max(propagation_ratios) <= 1 + 1e-11

    nodes = [u - 2j * k for k in range(n + 1)]
    leading = np.zeros_like(xb)
    at_zero = np.zeros_like(xb)
    for k, node in enumerate(nodes):
        denominator = np.prod([node - other for j, other in enumerate(nodes) if j != k])
        value = defect(node)
        leading += value / denominator
        numerator = np.prod([-other for j, other in enumerate(nodes) if j != k])
        at_zero += value * numerator / denominator
    leading_error = relative_error(leading, xb - yb)
    zero_error = relative_error(at_zero, defect(0))
    assert leading_error < 1e-9
    assert zero_error < 1e-9

    b = (u * u + 4 * n * n) / abs(u)
    k_bound = b ** n * ((abs(u) + 2 * n) ** n + 1) / math.factorial(n)
    cycle = monodromy(n, 0) / (1j ** n)
    commutator_ratio = normalized_hs(cycle @ xb - xb @ cycle) / (k_bound * delta)
    assert commutator_ratio <= 1 + 1e-11
    singular_values = np.linalg.svd(bath_superoperator(unitary), compute_uv=False)
    assert abs(float(singular_values[0]) - 1) < 1e-11
    observed_gap = 1 - float(singular_values[1]) ** 2
    alpha = 4 * math.sin(math.pi / (2 * (n + 1))) ** 2
    gap_bound = alpha / (k_bound * k_bound)
    assert observed_gap + 1e-13 >= gap_bound

    return {
        "n": n, "u": u,
        "max_crossing_relative_error": max(crossing_errors),
        "max_intertwiner_relative_error": max(intertwining_errors),
        "projection_identity_error": projection_error,
        "max_propagation_ratio": max(propagation_ratios),
        "leading_interpolation_relative_error": leading_error,
        "zero_interpolation_relative_error": zero_error,
        "cycle_commutator_bound_ratio": commutator_ratio,
        "observed_gamma_n": observed_gap,
        "proved_gamma_lower_bound": gap_bound,
    }


def main() -> None:
    rng = np.random.default_rng(240511)
    output = {"scope": "Numerical checks corroborate, but do not prove, the accompanying analytic theorem.",
              "cycle": [], "instances": []}
    for n in range(1, 5):
        output["cycle"].append(cycle_minimum(n))
        for u in [0.4, 1.0, 3.0, 10.0, -0.7]:
            output["instances"].append(check_instance(n, u, rng))
        rows = [r for r in output["instances"] if r["n"] == n]
        err = max(max(r["max_crossing_relative_error"], r["max_intertwiner_relative_error"],
                      r["leading_interpolation_relative_error"], r["zero_interpolation_relative_error"]) for r in rows)
        print(f"n={n}: five u values passed; largest relative identity error {err:.3e}", flush=True)
    destination = Path(__file__).with_name("crossing_gap_checks.json")
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(f"Saved {destination}")


if __name__ == "__main__":
    main()
