"""Small exact enumeration sanity check; not a theorem or validation substitute."""
import itertools
import json
import math
from pathlib import Path

import numpy as np

BASE = Path(__file__).parent
RNG = np.random.default_rng(9017)
S0 = 1 / (6 * 10**9)
C = 12000


def constants(n, r, b):
    c = n * (r - 1) / (n - 1)
    d = r * (r - 1) / (n * (n - 1)) * (n + n * n * float(b @ b))
    return c, d


def score(n, r, b, axis, x):
    c, d = constants(n, r, b)
    return (3 * x * x - 3 * r - 6 * c * b[axis] * x + d) / r


def product_statistics(v, b, r):
    n = len(v)
    records = []
    subsets = list(itertools.combinations(range(n), r))
    for axis in range(3):
        for subset in subsets:
            for signs in itertools.product((-1, 1), repeat=r):
                probability = math.prod((1 + z * v[i, axis]) / 2 for i, z in zip(subset, signs))
                records.append((probability / (3 * len(subsets)), score(n, r, b, axis, sum(signs))))
    total = sum(p for p, _ in records)
    mean = sum(p * t for p, t in records)
    second = sum(p * t * t for p, t in records)
    # expm1 retains the first-order mgf displacement at the deliberately small s.
    mgf_displacement = sum(p * math.expm1(-S0 * t) for p, t in records)
    vbar = v.mean(axis=0)
    q = np.square(v).sum(axis=1).mean()
    expected_mean = (r - 1) / (n - 1) * (1 - q + n * float((vbar - b) @ (vbar - b)))
    field = r * float((vbar - b) @ (vbar - b))
    assert abs(total - 1) < 1e-11
    assert abs(mean - expected_mean) < 1e-10
    assert min(t for _, t in records) >= -8
    assert second <= 4000 * (1 + field * field)
    assert mgf_displacement <= C * S0 * S0 + 1e-22
    return {
        "N": n, "r": r, "mean": mean, "formula_mean": expected_mean,
        "mean_residual": abs(mean - expected_mean), "second_moment": second,
        "minimum_score": min(t for _, t in records), "mgf_minus_one": mgf_displacement,
        "field": field,
    }


def kron_all(matrices):
    result = np.array([[1]], dtype=complex)
    for matrix in matrices:
        result = np.kron(result, matrix)
    return result


def target_statistics(n, r):
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.diag([1, -1]).astype(complex)
    identity = np.eye(2)
    spin = []
    for pauli in (sx, sy, sz):
        spin.append(sum(kron_all([pauli if i == k else identity for i in range(n)]) for k in range(n)) / 2)
    casimir = sum(j @ j for j in spin)
    eigenvalues, eigenvectors = np.linalg.eigh(casimir)
    rho = np.zeros_like(casimir)
    weights = []
    for j in range(n // 2 + 1):
        mask = np.isclose(eigenvalues, j * (j + 1), atol=1e-8)
        basis = eigenvectors[:, mask]
        p_j = mask.sum() / 2**n
        m_values, m_basis = np.linalg.eigh(basis.conj().T @ spin[2] @ basis)
        highest = basis @ m_basis[:, np.isclose(m_values, j, atol=1e-8)]
        rho += p_j / highest.shape[1] * (highest @ highest.conj().T)
        weights.append({"j": j, "p_j": p_j, "multiplicity": highest.shape[1]})
    b = np.array([float(np.trace(rho @ j).real) * 2 / n for j in spin])
    mean = 0.0
    second = 0.0
    subsets = list(itertools.combinations(range(n), r))
    full_signs = list(itertools.product((1, -1), repeat=n))
    for axis, pauli in enumerate((sx, sy, sz)):
        _, basis = np.linalg.eigh(pauli)
        # eigh orders eigenvalues -1,+1, while computational index here uses +1,-1.
        basis = basis[:, ::-1]
        full_basis = kron_all([basis] * n)
        probabilities = np.diag(full_basis.conj().T @ rho @ full_basis).real
        for signs, probability in zip(full_signs, probabilities):
            for subset in subsets:
                value = score(n, r, b, axis, sum(signs[i] for i in subset))
                weight = probability / (3 * len(subsets))
                mean += weight * value
                second += weight * value * value
    gap = n * float(b @ b) - 1
    expected_mean = -gap * (r - 1) / (n - 1)
    assert abs(float(np.trace(rho).real) - 1) < 1e-10
    assert abs(float(np.trace(rho @ casimir).real) - 3 * n / 4) < 1e-10
    assert gap > 0
    assert abs(mean - expected_mean) < 1e-10
    return {
        "N": n, "r": r, "b": b.tolist(), "kappa": gap + 1,
        "mean": mean, "formula_mean": expected_mean,
        "mean_residual": abs(mean - expected_mean), "second_moment": second,
        "spin_weights": weights,
    }


def main():
    products = []
    for n, r in ((4, 2), (6, 2), (6, 3), (8, 4)):
        b = np.array([0.3, -0.4, math.sqrt(0.75)]) * math.sqrt(2 / n)
        arrays = [np.zeros((n, 3)), np.tile([0, 0, 1], (n, 1)), np.tile(b, (n, 1))]
        for _ in range(12):
            v = RNG.normal(size=(n, 3))
            v /= np.linalg.norm(v, axis=1)[:, None]
            if len(arrays) % 2:
                v *= RNG.random((n, 1))
            arrays.append(v)
        for v in arrays:
            products.append(product_statistics(v, b, r))
    targets = [target_statistics(n, r) for n, r in ((4, 2), (6, 2), (6, 3))]
    result = {
        "status": "FINITE_DIAGNOSTIC_ONLY", "random_seed": 9017,
        "enumerated_product_cases": len(products), "product_cases": products,
        "constructed_targets": targets,
        "max_mean_residual": max(x["mean_residual"] for x in products + targets),
        "scope": "Small N and named examples only; does not replace the analytic null-mixture or target-tail proof.",
    }
    (BASE / "diagnostic_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "enumerated_product_cases", "max_mean_residual")}))


if __name__ == "__main__":
    main()
