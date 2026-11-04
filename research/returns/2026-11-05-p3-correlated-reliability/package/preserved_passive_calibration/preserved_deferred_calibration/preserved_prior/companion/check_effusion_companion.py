"""Deterministic numerical illustration; the proof is in effusion_companion.md.

Checks the directional quadrature for arbitrary hidden directions and verifies
the finite-width force-response bound on a collection of hidden barrier profiles.
No laboratory claim or simulation of a real material is made.
"""

import json
import math

import numpy as np
from numpy.polynomial.legendre import leggauss


def quadrature(s, absolute_error):
    degree = 0
    if s:
        while (math.log(2) + s + (degree + 1) * math.log(s)
               - math.lgamma(degree + 2) > math.log(absolute_error)):
            degree += 1
    n_z = math.ceil((degree + 1) / 2)
    n_phi = degree + 1
    z, weights_z = leggauss(n_z)
    phi = 2 * math.pi * np.arange(n_phi) / n_phi
    directions = np.array([
        [math.sqrt(1 - zk * zk) * math.cos(p),
         math.sqrt(1 - zk * zk) * math.sin(p), zk]
        for zk in z for p in phi
    ])
    weights = np.repeat(weights_z / (2 * n_phi), n_phi)
    return degree, directions, weights


def main():
    rng = np.random.default_rng(20261105)
    beta, force, ell, width, length = 1.0, 20.0, 1.0, 1e-4, 1.001
    s = beta * force * ell
    gamma = math.sinh(s) / s
    degree, controls, weights = quadrature(s, .01)
    num_channels = 41
    hidden_directions = rng.normal(size=(num_channels, 3))
    hidden_directions /= np.linalg.norm(hidden_directions, axis=1)[:, None]
    h = force * controls @ hidden_directions.T
    exact_shell_acceleration = weights @ np.exp(beta * ell * h)

    # The barrier is zero outside a thin shell. Inside it, many almost-equal
    # potential maxima permit load-induced movement or exchange of the maximum.
    xs = np.linspace(ell - width, ell + width, 201)
    cold_barriers = rng.uniform(30, 45, num_channels)
    barrier_profiles = cold_barriers[:, None] - rng.uniform(
        0, 2 * force * width, (num_channels, len(xs))
    )
    barrier_profiles[np.arange(num_channels),
                     rng.integers(0, len(xs), num_channels)] = cold_barriers
    cold_barriers = barrier_profiles.max(axis=1)
    nu = np.exp(rng.uniform(0, math.log(1e6), num_channels))
    cold_rates = nu * np.exp(-beta * cold_barriers)
    acceleration = np.empty(num_channels)
    maximum_motion = []
    for j in range(num_channels):
        tilted = barrier_profiles[j][None, :] - h[:, j, None] * xs
        maximizers = tilted.argmax(axis=1)
        actual_maximum = tilted.max(axis=1)
        # Endpoint maxima outside the shell cannot win by the design inequality.
        assert cold_barriers[j] > force * length
        assert np.all(actual_maximum > np.maximum(0, -h[:, j] * length))
        response = np.exp(-beta * (actual_maximum - cold_barriers[j]))
        ideal_response = np.exp(beta * ell * h[:, j])
        assert np.max(np.abs(np.log(response / ideal_response))) <= beta * force * width + 1e-12
        acceleration[j] = weights @ response
        maximum_motion.append(float(xs[maximizers].max() - xs[maximizers].min()))
    pooled_acceleration = float(np.dot(cold_rates, acceleration) / cold_rates.sum())
    assert np.max(np.abs(exact_shell_acceleration / gamma - 1)) < 1e-10
    assert gamma * math.exp(-beta * force * width) <= pooled_acceleration
    assert pooled_acceleration <= gamma * math.exp(beta * force * width)
    output = {
        "model": "dimensionless ideal collisionless finite-shell guide family",
        "seed": 20261105,
        "channels": num_channels,
        "force_work_s": s,
        "quadrature_degree": degree,
        "force_settings": len(weights),
        "Gamma_3": gamma,
        "sharp_shell_max_relative_quadrature_error": float(
            np.max(np.abs(exact_shell_acceleration / gamma - 1))),
        "finite_shell_log_error_budget": beta * force * width,
        "pooled_acceleration": pooled_acceleration,
        "proved_acceleration_interval": [
            gamma * math.exp(-beta * force * width),
            gamma * math.exp(beta * force * width)],
        "cold_total_rate": float(cold_rates.sum()),
        "maximum_observed_saddle_motion": max(maximum_motion),
        "no_physical_experiment": True,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
