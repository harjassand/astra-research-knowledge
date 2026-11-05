#!/usr/bin/env python3
"""Finite matrix checks for the noninteracting blackout boundary.

These checks verify algebraic identities, not the lifetime of a memory family.
Run: python3 verify_blackout_boundary.py
Dependencies: numpy, scipy.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.linalg import expm


def vec(a):
    return a.reshape(-1, order="F")


def unvec(a, n):
    return a.reshape((n, n), order="F")


def dissipator(jump):
    n = jump.shape[0]
    identity = np.eye(n)
    jj = jump.conj().T @ jump
    return np.kron(jump.conj(), jump) - 0.5 * (
        np.kron(identity, jj) + np.kron(jj.T, identity)
    )


def choi_of_map(channel, input_dim, output_dim):
    result = np.zeros((input_dim * output_dim,) * 2, dtype=complex)
    for i in range(input_dim):
        for j in range(input_dim):
            basis = np.zeros((input_dim, input_dim), dtype=complex)
            basis[i, j] = 1
            result += np.kron(basis, channel(basis)) / input_dim
    return result


def partial_trace(state, dims, traced):
    dims = list(dims)
    value = state.reshape(dims + dims)
    for axis in sorted(traced, reverse=True):
        value = np.trace(value, axis1=axis, axis2=axis + len(dims))
        dims.pop(axis)
    remaining = math.prod(dims)
    return value.reshape(remaining, remaining)


def main():
    nu = 0.13
    identity = np.eye(2)
    lower = np.array([[0, 1], [0, 0]], dtype=complex)
    z = np.diag([1, -1]).astype(complex)
    max_channel_residual = 0.0
    channel_cases = 0
    for beta in (0.0, 0.5, 3.0, 100.0):
        for gap in (0.0, 0.7, 4.0):
            excited = 1.0 / (1.0 + math.exp(beta * gap))
            tau = np.diag([1.0 - excited, excited])
            hamiltonian = np.diag([0.0, gap])
            down = 2.0 * nu * (1.0 - excited)
            up = 2.0 * nu * excited
            generator = (
                2.0 * down * dissipator(lower)
                + 2.0 * up * dissipator(lower.conj().T)
                + nu * dissipator(z)
                - 1j * (np.kron(identity, hamiltonian)
                        - np.kron(hamiltonian.T, identity))
            )
            for time in (0.01, math.log(2.0) / (4.0 * nu), 10.0):
                physical = expm(time * generator)
                decay = math.exp(-4.0 * nu * time)
                unitary = expm(-1j * time * hamiltonian)
                expected = decay * np.kron(unitary.conj(), unitary)
                expected += (1.0 - decay) * np.outer(vec(tau), vec(identity))
                residual = float(np.linalg.norm(physical - expected, ord=2))
                max_channel_residual = max(max_channel_residual, residual)
                channel_cases += 1

    minimum_extension_eigenvalue = 1.0
    max_marginal_residual = 0.0
    extension_cases = 0
    for decay in (0.0, 0.3, 0.5):
        for excited in (0.0, 0.1, 0.5):
            tau = np.diag([1.0 - excited, excited])

            def broadcast(rho):
                return (decay * np.kron(rho, tau)
                        + decay * np.kron(tau, rho)
                        + (1.0 - 2.0 * decay) * np.trace(rho)
                          * np.kron(tau, tau))

            def boundary(rho):
                return decay * rho + (1.0 - decay) * tau * np.trace(rho)

            extended = choi_of_map(broadcast, 2, 4)
            marginal = choi_of_map(boundary, 2, 2)
            minimum_extension_eigenvalue = min(
                minimum_extension_eigenvalue,
                float(np.linalg.eigvalsh(extended).min()),
            )
            for discarded in ([1], [2]):
                residual = np.linalg.norm(
                    partial_trace(extended, (2, 2, 2), discarded) - marginal,
                    ord=2,
                )
                max_marginal_residual = max(max_marginal_residual, float(residual))
            extension_cases += 1

    bell_vector = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2.0)
    bell = np.outer(bell_vector, bell_vector.conj())
    bell_ra = np.kron(bell, identity)
    swap_ab = np.zeros((8, 8))
    for r in range(2):
        for a in range(2):
            for b in range(2):
                swap_ab[4 * r + 2 * b + a, 4 * r + 2 * a + b] = 1
    bell_rb = swap_ab @ bell_ra @ swap_ab.T
    projector_sum_norm = float(np.linalg.eigvalsh(bell_ra + bell_rb).max())

    result = {
        "scope": "Finite algebra checks only; no physical lifetime simulation.",
        "channel_cases": channel_cases,
        "channel_formula_max_operator_norm_residual": max_channel_residual,
        "broadcast_extension_cases": extension_cases,
        "extension_choi_min_eigenvalue": minimum_extension_eigenvalue,
        "extension_marginal_max_operator_norm_residual": max_marginal_residual,
        "bell_projector_sum_operator_norm": projector_sum_norm,
        "two_extendible_bell_fidelity_upper_bound": projector_sum_norm / 2.0,
        "half_diamond_error_lower_bound": 1.0 - projector_sum_norm / 2.0,
        "no_correction_interval_threshold": "log(2)/(4*nu)",
        "assumptions": [
            "Unobserved independent isotropic XYZ Davies bath.",
            "g_beta(omega) = 2*nu/(1+exp(-beta*omega)).",
            "Static noninteracting Hamiltonian; arbitrary local gaps and beta.",
            "No retained quantum system outside the declared holding channel.",
            "Arbitrary encoding, classical side records, and final decoding allowed."
        ],
    }
    assert channel_cases == 36
    assert max_channel_residual < 1e-12
    assert minimum_extension_eigenvalue > -1e-12
    assert max_marginal_residual < 1e-12
    assert abs(projector_sum_norm - 1.5) < 1e-12
    destination = Path(__file__).with_name("blackout_boundary_checks.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
