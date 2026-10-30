"""Independent finite checks of the Gaussian quadratic two-round compiler.

The central final-risk check uses tensor three-point Gauss--Hermite integration,
which integrates the squared polynomial error exactly in exact arithmetic.
These are floating-point checks of finite examples, not substitutes for proof.
Run: python p1_next/alternative/check_gaussian_quadratic.py
"""

from itertools import product
from pathlib import Path
import json
import numpy as np


def spectral_data(a):
    values, vectors = np.linalg.eigh(a)
    positive = sorted((i for i, x in enumerate(values) if x > 1e-10),
                      key=lambda i: -values[i])
    negative = sorted((i for i, x in enumerate(values) if x < -1e-10),
                      key=lambda i: values[i])
    return values, vectors, positive, negative


def compile_first(a, k):
    values, vectors, positive, negative = spectral_data(a)
    pairs = min(k, len(positive), len(negative))
    columns = []
    for i in range(pairs):
        ep, en = vectors[:, positive[i]], vectors[:, negative[i]]
        lam, mu = values[positive[i]], -values[negative[i]]
        columns.append((np.sqrt(lam) * ep - np.sqrt(mu) * en)
                       / np.sqrt(lam + mu))
    for indices in (positive, negative):
        for i in indices[pairs:k]:
            columns.append(vectors[:, i])
    u = np.column_stack(columns) if columns else np.zeros((len(a), 0))
    tail = 2 * sum(values[i] ** 2 for i in positive[k:] + negative[k:])
    return u, tail


def complement(u):
    n, rank = u.shape
    if rank == 0:
        return np.eye(n)
    return np.linalg.qr(u, mode="complete")[0][:, rank:]


def gaussian_grid(d):
    nodes = (-np.sqrt(3.0), 0.0, np.sqrt(3.0))
    weights = (1 / 6, 2 / 3, 1 / 6)
    for ix in product(range(3), repeat=d):
        yield np.array([nodes[i] for i in ix]), np.prod([weights[i] for i in ix])


def integrated_error(a, b, c, u, first_y):
    n = len(a)
    m = u @ first_y
    v = complement(u)
    q = v @ v.T
    compressed = q @ a @ q
    t = q @ (b + 2 * a @ m)
    tnorm = np.linalg.norm(t)
    w = t / tnorm if tnorm > 1e-10 else np.zeros(n)
    alpha = w @ compressed @ w
    base = m @ a @ m + b @ m + c + np.trace(compressed)
    error = 0.0
    for z, weight in gaussian_grid(v.shape[1]):
        x = m + v @ z
        last_y = w @ x
        prediction = base + tnorm * last_y + alpha * (last_y**2 - 1)
        target = x @ a @ x + b @ x + c
        error += weight * (target - prediction)**2
    expected = 2 * np.sum(compressed**2) - 2 * alpha**2
    return float(error), float(expected), float(np.linalg.norm(compressed @ t))


def main():
    rng = np.random.default_rng(20261030)
    spectra = [
        [0.0], [2.0], [-3.0], [2.0, -1.0],
        [4.0, 2.0, -3.0, -0.5],
        [4.0, 2.0, 1.0, -3.0, 0.0],
        [1.0, 0.5, -4.0, -2.0, -1.0, 0.0],
        [6.0, 5.0, 4.0, 3.0, 2.0, 1.0],
        [-6.0, -5.0, -4.0, -3.0, -2.0, -1.0],
        [3.0, 3.0, -3.0, -3.0, 0.0, 0.0],
    ]
    result = dict(seed=20261030, quadrature="tensor 3-point standard Gaussian",
                  spectra=len(spectra), rotations=4, risk_checks=0,
                  compression_checks=0, random_interlacing_checks=0,
                  exact_reconstruction_checks=0, max_risk_relative_error=0.0,
                  max_compression_relative_error=0.0,
                  minimum_random_interlacing_margin=0.0,
                  max_homogeneous_kernel_error=0.0,
                  max_exact_reconstruction_error=0.0)
    for spectrum in spectra:
        n = len(spectrum)
        for _ in range(4):
            rotation = np.linalg.qr(rng.normal(size=(n, n)))[0]
            a = (rotation * np.array(spectrum)) @ rotation.T
            arbitrary_b = rng.normal(size=n)
            for k in range(n + 1):
                u, bound = compile_first(a, k)
                q = np.eye(n) - u @ u.T
                compressed_risk = 2 * np.sum((q @ a @ q)**2)
                residual = abs(compressed_risk - bound) / (1 + bound)
                result["max_compression_relative_error"] = max(
                    result["max_compression_relative_error"], residual)
                assert residual < 1e-10
                assert u.shape[1] <= k
                assert np.linalg.norm(u.T @ u - np.eye(u.shape[1])) < 1e-10
                result["compression_checks"] += 1
                first_y = rng.normal(size=u.shape[1])
                for homogeneous in (True, False):
                    b = np.zeros(n) if homogeneous else arbitrary_b
                    measured, expected, kernel = integrated_error(
                        a, b, 0.73, u, first_y)
                    error = abs(measured - expected) / (1 + expected)
                    result["max_risk_relative_error"] = max(
                        result["max_risk_relative_error"], error)
                    assert error < 1e-10
                    assert measured <= bound + 1e-8 * (1 + bound)
                    if homogeneous:
                        result["max_homogeneous_kernel_error"] = max(
                            result["max_homogeneous_kernel_error"], kernel)
                        assert abs(measured - bound) < 1e-8 * (1 + bound)
                    result["risk_checks"] += 1
                for _ in range(3):
                    arbitrary_u = np.linalg.qr(rng.normal(size=(n, n)))[0][:, :k]
                    arbitrary_q = np.eye(n) - arbitrary_u @ arbitrary_u.T
                    margin = 2 * np.sum((arbitrary_q @ a @ arbitrary_q)**2) - bound
                    result["minimum_random_interlacing_margin"] = min(
                        result["minimum_random_interlacing_margin"], float(margin))
                    assert margin >= -1e-9 * (1 + bound)
                    result["random_interlacing_checks"] += 1
            _, _, positive, negative = spectral_data(a)
            exact_u, bound = compile_first(a, max(len(positive), len(negative)))
            q = np.eye(n) - exact_u @ exact_u.T
            assert bound == 0
            for _ in range(12):
                x = rng.normal(size=n)
                m = exact_u @ (exact_u.T @ x)
                t = q @ (arbitrary_b + 2 * a @ m)
                prediction = m @ a @ m + arbitrary_b @ m + 0.73 + t @ x
                target = x @ a @ x + arbitrary_b @ x + 0.73
                error = abs(prediction - target)
                result["max_exact_reconstruction_error"] = max(
                    result["max_exact_reconstruction_error"], float(error))
                assert error < 1e-9 * (1 + abs(target))
                result["exact_reconstruction_checks"] += 1
    result["status"] = "PASS"
    path = Path(__file__).with_name("check_gaussian_quadratic_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
