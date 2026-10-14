#!/usr/bin/env python3
"""Independent exact checks for the finite-patch thermal-response note.

The harmonic-chain check uses a closed-form Green function and a dense matrix
inverse.  The Ising checks enumerate every computational-basis state and
evaluate the supplied positive spectral response exactly up to floating-point
rounding.  No producer script from the source packages is imported.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np


def harmonic_closed(R: int, kappa: float, eta: float) -> tuple[float, float, float]:
    theta = math.acosh(1.0 + eta * eta / (2.0 * kappa))
    finite = math.tanh((R + 1) * theta) / (2.0 * kappa * math.sinh(theta))
    infinite = 1.0 / (2.0 * kappa * math.sinh(theta))
    relative_error = (infinite - finite) / infinite
    return finite, infinite, relative_error


def harmonic_dense(R: int, kappa: float, eta: float) -> float:
    n = 2 * R + 1
    mat = np.zeros((n, n), dtype=float)
    for i in range(n):
        mat[i, i] = 2.0 * kappa + eta * eta
        if i:
            mat[i, i - 1] = -kappa
        if i + 1 < n:
            mat[i, i + 1] = -kappa
    rhs = np.zeros(n)
    rhs[R] = 1.0
    return float(np.linalg.solve(mat, rhs)[R])


def ising_energy(spins: tuple[int, ...], J: float, h: float,
                 boundary_field: float) -> float:
    n = len(spins)
    e = -J * sum(spins[i] * spins[i + 1] for i in range(n - 1))
    e -= h * spins[n // 2]
    e -= boundary_field * (spins[0] + spins[-1])
    return e


def ising_response(n: int, beta: float, eta: float, J: float,
                    h: float, boundary_field: float) -> float:
    """chi(i eta) for A=X_center of a finite diagonal Ising chain."""
    center = n // 2
    states = list(itertools.product((-1, 1), repeat=n))
    energies = {s: ising_energy(s, J, h, boundary_field) for s in states}
    emin = min(energies.values())
    weights = {s: math.exp(-beta * (e - emin)) for s, e in energies.items()}
    z = sum(weights.values())
    total = 0.0
    for rest in itertools.product((-1, 1), repeat=n - 1):
        plus = list(rest)
        plus.insert(center, 1)
        minus = list(rest)
        minus.insert(center, -1)
        sp, sm = tuple(plus), tuple(minus)
        gap = abs(energies[sp] - energies[sm])
        if gap:
            total += abs(weights[sp] - weights[sm]) / z * (2.0 * gap / (gap * gap + eta * eta))
    return total


def hidden_two_qubit_response(beta: float, eta: float, h: float,
                              lam: float, remote_field: float) -> float:
    """A=X_0, H=-h Z_0-lam Z_0 Z_1-remote_field Z_1."""
    energies: dict[tuple[int, int], float] = {}
    for z0, z1 in itertools.product((-1, 1), repeat=2):
        energies[(z0, z1)] = -h * z0 - lam * z0 * z1 - remote_field * z1
    emin = min(energies.values())
    weights = {s: math.exp(-beta * (e - emin)) for s, e in energies.items()}
    z = sum(weights.values())
    total = 0.0
    for z1 in (-1, 1):
        up, down = (1, z1), (-1, z1)
        gap = abs(energies[up] - energies[down])
        if gap:
            total += abs(weights[up] - weights[down]) / z * (2.0 * gap / (gap * gap + eta * eta))
    return total


def quantum_ising_center_response(n: int, beta: float, eta: float, J: float,
                                  h: float, transverse: float,
                                  boundary_field: float) -> float:
    """Exact chi(i eta) for A=Z_center with only center X transverse field.

    All spins except the center are conserved.  Conditional on their values,
    the center is a two-level Hamiltonian -b_eff Z - transverse X, so its
    partition function and transition matrix element are analytic.
    """
    center = n // 2
    total_z = 0.0
    total_chi = 0.0
    for rest in itertools.product((-1, 1), repeat=n - 1):
        spins = list(rest)
        spins.insert(center, 1)  # placeholder; center bonds are excluded below
        e_out = -J * sum(spins[i] * spins[i + 1]
                         for i in range(n - 1)
                         if i != center - 1 and i != center)
        e_out -= boundary_field * (spins[0] + spins[-1])
        b_eff = h + J * (spins[center - 1] + spins[center + 1])
        e = math.sqrt(b_eff * b_eff + transverse * transverse)
        block_z = 2.0 * math.exp(-beta * e_out) * math.cosh(beta * e)
        total_z += block_z
        if transverse != 0.0:
            mass = 2.0 * math.exp(-beta * e_out) * math.sinh(beta * e)
            total_chi += mass * (4.0 * e / (4.0 * e * e + eta * eta)) * \
                         (transverse * transverse / (e * e))
    return total_chi / total_z


def main() -> None:
    harmonic_rows = []
    for eta in (0.05, 0.1, 0.25, 0.5):
        R = max(2, math.ceil(1.5 / eta))
        closed, infinite, rel = harmonic_closed(R, 1.0, eta)
        dense = harmonic_dense(R, 1.0, eta)
        predicted_min_R = math.ceil(0.5 * math.log((2.0 - 0.01) / 0.01) /
                                    math.acosh(1.0 + eta * eta / 2.0)) - 1
        _, _, threshold_error = harmonic_closed(predicted_min_R, 1.0, eta)
        harmonic_rows.append({
            "eta": eta,
            "R": R,
            "closed_patch_response": closed,
            "dense_inverse_response": dense,
            "infinite_chain_response": infinite,
            "relative_patch_error": rel,
            "matrix_formula_abs_error": abs(closed - dense),
            "radius_for_1pct_relative_error": predicted_min_R,
            "threshold_relative_error": threshold_error,
        })
        assert abs(closed - dense) < 2e-11
        assert threshold_error <= 0.0100000001

    # The two full chains agree on every interaction near the center.  Only
    # the remote endpoint fields change sign; the patch H[-1,1] is identical.
    beta, eta, J, h, b = 5.0, 0.25, 1.0, 0.5, 2.0
    R, L = 1, 3
    patch = ising_response(2 * R + 1, beta, eta, J, h, 0.0)
    plus = ising_response(2 * L + 1, beta, eta, J, h, b)
    minus = ising_response(2 * L + 1, beta, eta, J, h, -b)
    ising = {
        "parameters": {"beta": beta, "eta": eta, "J": J, "h_center": h,
                       "remote_endpoint_field_magnitude": b,
                       "patch_radius": R, "full_chain_radius": L},
        "open_patch_response": patch,
        "plus_remote_boundary_response": plus,
        "minus_remote_boundary_response": minus,
        "remote_boundary_response_gap": abs(plus - minus),
        "patch_error_plus": abs(patch - plus),
        "patch_error_minus": abs(patch - minus),
        "same_local_hamiltonian_inside_patch": True,
    }
    assert abs(plus - minus) > 0.15

    qbeta, qeta, qJ, qh, qg, qb = 5.0, 0.25, 1.0, 0.5, 1.0, 2.0
    qR, qL = 1, 3
    qpatch = quantum_ising_center_response(2 * qR + 1, qbeta, qeta, qJ,
                                           qh, qg, 0.0)
    qplus = quantum_ising_center_response(2 * qL + 1, qbeta, qeta, qJ,
                                          qh, qg, qb)
    qminus = quantum_ising_center_response(2 * qL + 1, qbeta, qeta, qJ,
                                           qh, qg, -qb)
    quantum_ising = {
        "parameters": {"beta": qbeta, "eta": qeta, "J": qJ,
                       "h_center": qh, "center_transverse_field": qg,
                       "remote_end_fields_magnitude": qb,
                       "patch_radius": qR, "full_chain_radius": qL},
        "observable": "Z at the center",
        "open_patch_response": qpatch,
        "plus_remote_boundary_response": qplus,
        "minus_remote_boundary_response": qminus,
        "remote_boundary_response_gap": abs(qplus - qminus),
        "patch_error_plus": abs(qpatch - qplus),
        "patch_error_minus": abs(qpatch - qminus),
        "same_local_hamiltonian_inside_patch": True,
        "evaluation": "exact two-level block decomposition and finite thermal trace",
    }
    assert abs(qplus - qminus) > 0.1

    # Exact nonlocal hidden-sector example: an unbounded interaction range
    # lets an unseen remote qubit alter the local transition gap at any R.
    hidden = {
        "parameters": {"beta": 2.0, "eta": 0.25, "h": 0.3,
                       "long_range_coupling": 1.0,
                       "remote_field_magnitude": 1.0},
        "remote_plus_response": hidden_two_qubit_response(2.0, 0.25, 0.3, 1.0, 1.0),
        "remote_minus_response": hidden_two_qubit_response(2.0, 0.25, 0.3, 1.0, -1.0),
        "scope": "Exact counterexample when no finite interaction-range promise is supplied.",
    }
    hidden["response_gap"] = abs(hidden["remote_plus_response"] - hidden["remote_minus_response"])
    assert hidden["response_gap"] > 0.1

    results = {
        "status": "independent exact small-model checks; floating-point evaluation",
        "harmonic_gapless_chain": harmonic_rows,
        "finite_range_hidden_boundary_ising_chain": ising,
        "finite_range_hidden_boundary_quantum_ising_chain": quantum_ising,
        "unbounded_range_hidden_sector": hidden,
    }
    out = Path(__file__).with_name("exact_patch_results.json")
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
