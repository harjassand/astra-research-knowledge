"""Finite-prior limiting Fock experiment; numerical diagnostics only.

U~prior, Z=U+N(0,1), Y=r U+N(0,1), r=eta/(1-eta).
E additionally holds pure states with amplitude overlaps
exp[-nu(nu+1)(u-u')^2/2].  The exact finite-prior objective is
H(J|Z)-H(J|Y)-E_Z S(Gram(prior conditioned on Z)).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def entropy(probabilities):
    vals = np.asarray(probabilities)
    vals = vals[vals > 0]
    return float(-(vals * np.log(vals)).sum())


def posterior_at(value, means, prior):
    logw = np.log(prior) - 0.5 * (value - means) ** 2
    logw -= logw.max()
    vals = np.exp(logw)
    return vals / vals.sum()


def evaluate(u, prior, eta, nu, order=160):
    u, prior = np.asarray(u, dtype=float), np.asarray(prior, dtype=float)
    prior = prior / prior.sum()
    if not np.all(prior > 0):
        raise ValueError("All retained prior masses must be positive")
    c2 = nu * (nu + 1)
    ratio = eta / (1 - eta)
    overlap = np.exp(-0.5 * c2 * (u[:, None] - u[None, :]) ** 2)
    nodes, weights = np.polynomial.hermite.hermgauss(order)
    noises, weights = math.sqrt(2) * nodes, weights / math.sqrt(math.pi)
    hz = hy = quantum_penalty = 0.0
    for index, mass in enumerate(prior):
        for noise, weight in zip(noises, weights):
            postz = posterior_at(u[index] + noise, u, prior)
            posty = posterior_at(ratio * u[index] + noise, ratio * u, prior)
            gram = np.sqrt(postz[:, None] * postz[None, :]) * overlap
            eig = np.linalg.eigvalsh(gram)
            total_weight = mass * weight
            hz += total_weight * entropy(postz)
            hy += total_weight * entropy(posty)
            quantum_penalty += total_weight * entropy(np.maximum(eig, 0))
    result = hz - hy - quantum_penalty
    return {
        "eta": eta, "nu": nu, "quadrature_order": order,
        "prior_u": u.tolist(), "prior_probabilities": prior.tolist(),
        "I_c_limit_nats_float": result,
        "I_c_limit_bits_float": result / math.log(2),
        "H_J_given_Z_nats_float": hz,
        "H_J_given_Y_nats_float": hy,
        "conditional_quantum_entropy_nats_float": quantum_penalty,
    }


def gaussian_prior_value(variance, eta, nu):
    ratio = eta / (1 - eta)
    c2 = nu * (nu + 1)
    occupation = (math.sqrt(1 + 4 * c2 * variance / (1 + variance)) - 1) / 2
    g = (occupation + 1) * math.log(occupation + 1)
    if occupation > 0:
        g -= occupation * math.log(occupation)
    return 0.5 * math.log((1 + ratio * ratio * variance) / (1 + variance)) - g


def main():
    results = []
    for eta in [0.75, 0.78, 0.8, 0.81]:
        for order in [80, 160]:
            for gap in [0.25, 1.0, 3.0]:
                results.append(evaluate([-gap / 2, gap / 2], [0.5, 0.5], eta, 1.0, order))
    target = Path(__file__).with_name("e3_local_experiment_results.json")
    target.write_text(json.dumps({
        "status": "FLOATING_POINT_DIAGNOSTIC_NOT_A_CERTIFICATE",
        "results": results,
        "gaussian_prior_checks": [
            {"eta": eta, "variance": variance, "I_c_limit_nats": gaussian_prior_value(variance, eta, 1)}
            for eta in [0.75, 0.78, 0.8, 0.81] for variance in [0.1, 1, 10, 100]
        ],
    }, indent=2) + "\n")
    for result in results:
        print(json.dumps({key: value for key, value in result.items() if key not in ["prior_probabilities"]}))


if __name__ == "__main__":
    main()
