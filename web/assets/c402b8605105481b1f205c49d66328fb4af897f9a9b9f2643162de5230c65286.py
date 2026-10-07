"""Finite checks for the positive periodic Gaussian-memory quantizer.

These check conventions and quadrature behavior. They are not an independent
proof of the sharp memory law, a quantum simulator, or a novelty certificate.
"""
import json
import math
from pathlib import Path
from statistics import NormalDist

import numpy as np


def hats(u, vertices, h):
    distance = np.abs(np.asarray(u)[..., None] - vertices)
    distance = np.minimum(distance, 1 - distance)
    return np.maximum(1 - distance / h, 0)


def local_moments(j, v):
    h = 1 / j
    vertices = np.arange(j) * h
    weights = hats(v, vertices, h)
    # Lift the circle to v+[-2h,2h] and split at all hat vertices.
    breaks = [-2 * h, 2 * h]
    for k in range(-3 * j, 3 * j + 1):
        t = k * h - v
        if -2 * h < t < 2 * h:
            breaks.append(t)
    breaks = sorted(set(breaks))
    nodes, quadrature_weights = np.polynomial.legendre.leggauss(4)
    out = np.zeros(3)
    for left, right in zip(breaks[:-1], breaks[1:]):
        t = (left + right) / 2 + (right - left) / 2 * nodes
        u = (v + t) % 1
        kernel = hats(u, vertices, h) @ weights / h
        for order in range(3):
            out[order] += (right - left) / 2 * np.dot(
                quadrature_weights, kernel * t**order
            )
    assert abs(out[0] - 1) < 1e-12
    assert abs(out[1]) < 1e-12
    assert 0 < out[2] < 4 * h**2
    return {"J": j, "v": v, "mass": float(out[0]),
            "first_moment": float(out[1]), "second_moment": float(out[2])}


def gaussian_diagnostics(theta, grid_size=131072):
    u = (np.arange(grid_size) + 0.5) / grid_size
    standard_normal = NormalDist()
    x = 2 * np.fromiter((standard_normal.inv_cdf(float(z)) for z in u),
                        dtype=float, count=grid_size)
    q = 2 * np.exp(-(x - theta)**2 / 2 + x**2 / 8)
    input_mass = float(q.mean())
    rows = []
    for j in [8, 16, 32, 64, 128]:
        cell = np.floor(j * u).astype(int)
        fraction = j * u - cell
        right = (cell + 1) % j
        vertex_probabilities = (
            np.bincount(cell, q * (1 - fraction), minlength=j)
            + np.bincount(right, q * fraction, minlength=j)
        ) / grid_size
        # Numerical integration estimates encode probabilities; normalization
        # changes only this finite diagnostic, not the analytic kernel formula.
        vertex_probabilities /= vertex_probabilities.sum()
        decoded_density = j * ((1 - fraction) * vertex_probabilities[cell]
                               + fraction * vertex_probabilities[right])
        tv = float(np.abs(decoded_density - q).mean() / 2)
        rows.append({"J": j, "tv_midpoint_estimate": tv, "J_squared_tv": j*j*tv})
    # The transformed second derivative's L1 norm is a real-line Gaussian
    # integral; a broad finite window checks the constant and sign polynomial.
    z = np.linspace(-18, 18, 262145)
    polynomial = 3 * z*z / 8 + theta * z / 4 - 3 / 4
    integrand = np.abs(polynomial) * 4 * math.sqrt(2 * math.pi) * np.exp(
        -z*z / 4 + theta*theta / 2
    )
    norm = float(np.trapezoid(integrand, z))
    bound = 8 * math.sqrt(2) * math.pi * math.exp(theta*theta / 2) * (
        1.5 + abs(theta) / (2 * math.sqrt(math.pi))
    )
    assert norm <= bound * (1 + 1e-8)
    return {"theta": theta, "midpoint_input_mass": input_mass,
            "q_second_derivative_L1_window_estimate": norm,
            "q_second_derivative_L1_analytic_bound": bound,
            "reconstruction": rows}


def main():
    moment_rows = []
    for j in [5, 8, 16, 64]:
        for v in [0, 1e-12, 0.25 / j, 0.51 / j, 0.317, 1 - 1e-12]:
            moment_rows.append(local_moments(j, v))
    output = {
        "scope": "Finite quadrature fixtures only; no theorem or novelty validation.",
        "periodic_local_moments": moment_rows,
        "transformed_gaussian_rows": [gaussian_diagnostics(t) for t in [0, 0.5, 1, 2]],
    }
    path = Path(__file__).with_name("gaussian_periodic_diagnostics.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"path": str(path), "moment_fixtures": len(moment_rows),
                      "gaussian_rows": output["transformed_gaussian_rows"]}, indent=2))


if __name__ == "__main__":
    main()
