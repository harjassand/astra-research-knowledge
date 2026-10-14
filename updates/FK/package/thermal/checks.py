#!/usr/bin/env python3
"""Reproducible falsification checks for a finite-anchor thermal-response sampler.

These are deterministic floating-point diagnostics, not a general-purpose
many-body solver, a replay of an author's implementation, or interval proofs.
Run with: OPENBLAS_NUM_THREADS=1 python checks.py --out results
Dependencies: Python >= 3.10, NumPy, SciPy.
"""
from __future__ import annotations
import argparse
import csv
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import scipy
from scipy.linalg import eigh, solve_continuous_lyapunov

BETAS = (1.0, 0.5, 0.25)


def thermal_weights(energies: np.ndarray, beta: float | None) -> np.ndarray:
    if beta is None:
        p = np.zeros_like(energies)
        p[0] = 1.0
        return p
    if beta <= 0:
        raise ValueError("beta must be positive")
    w = np.exp(-beta * (energies - energies[0]))
    return w / w.sum()


def susceptibility(energies: np.ndarray, observable: np.ndarray,
                   beta: float | None, eta: float = 0.0,
                   time_step: float | None = None) -> float:
    """Off-diagonal response; q has zero diagonal by parity in these tests.

    With time_step supplied, return the discrete Euclidean zero-Matsubara
    sum; beta must be an integer multiple of time_step. Otherwise return
    the continuum spectral susceptibility at the supplied eta >= 0.
    """
    if eta < 0:
        raise ValueError("eta must be nonnegative")
    p = thermal_weights(energies, beta)
    i, j = np.triu_indices(len(energies), 1)
    gap = energies[j] - energies[i]
    if np.any(gap <= 0):
        raise ValueError("This check assumes a nondegenerate ordered spectrum")
    weights = (p[i] - p[j]) * np.abs(observable[i, j]) ** 2
    if time_step is not None:
        if eta != 0 or time_step <= 0:
            raise ValueError("Discrete-time kernel implemented only for eta=0")
        if beta is not None and not np.isclose(beta / time_step,
                                              round(beta / time_step)):
            raise ValueError("beta must be a multiple of time_step")
        kernel = time_step / np.tanh(0.5 * time_step * gap)
    else:
        kernel = 2 * gap / (gap * gap + eta * eta)
    return float(np.dot(weights, kernel))


def harmonic_basis(dimension: int) -> tuple[np.ndarray, np.ndarray]:
    """Galerkin H=p^2/2+q^2/2+q^4; pad q before taking its fourth power.

    The padding makes the retained q^4 matrix the actual infinite-basis
    matrix restricted to the first dimension states, rather than q_d^4.
    """
    if dimension < 8:
        raise ValueError("dimension must be at least 8")
    padded = dimension + 4
    lowering = np.diag(np.sqrt(np.arange(1, padded)), 1)
    qfull = (lowering + lowering.T) / np.sqrt(2.0)
    qfour = np.linalg.matrix_power(qfull, 4)[:dimension, :dimension]
    hamiltonian = np.diag(np.arange(dimension) + 0.5) + qfour
    energies, vectors = eigh(hamiltonian)
    q = qfull[:dimension, :dimension]
    return energies, vectors.T @ q @ vectors


def oscillator_checks() -> dict[str, Any]:
    rows = []
    all_values: dict[int, np.ndarray] = {}
    for dimension in (64, 96, 144, 192):
        start = time.perf_counter()
        energies, q = harmonic_basis(dimension)
        values = []
        for beta in (None, *BETAS):
            value = susceptibility(energies, q, beta)
            rows.append({"dimension": dimension,
                         "beta": "infinity" if beta is None else beta,
                         "chi_zero": value, "ground_energy": float(energies[0]),
                         "lowest_gap": float(energies[1] - energies[0])})
            values.append(value)
        all_values[dimension] = np.asarray(values)
        rows[-1]["entire_dimension_seconds"] = time.perf_counter() - start
    err = float(np.max(np.abs(all_values[144] - all_values[192])))
    assert err < 1e-9, f"Basis convergence failed: {err}"
    energies, q = harmonic_basis(192)
    vacuum = susceptibility(energies, q, None)
    summary = []
    for beta in BETAS:
        val = susceptibility(energies, q, beta)
        summary.append({"beta": beta, "thermal_chi_zero": val,
                        "vacuum_chi_zero": vacuum,
                        "relative_vacuum_bias": (vacuum - val) / val})
    curve = []
    for eta in np.linspace(0, 4, 81):
        row = {"eta": float(eta), "vacuum": susceptibility(energies, q, None, eta)}
        for beta in BETAS:
            row[f"beta_{beta}"] = susceptibility(energies, q, beta, eta)
        curve.append(row)
    # The f-sum equals 1 for an untruncated canonical oscillator.
    fsum = []
    for beta in (None, *BETAS):
        p = thermal_weights(energies, beta)
        i, j = np.triu_indices(len(energies), 1)
        mass = float(np.sum(2 * (p[i] - p[j]) * (energies[j] - energies[i])
                            * q[i, j] ** 2))
        fsum.append({"beta": "infinity" if beta is None else beta, "M1": mass})
        assert abs(mass - 1) < 1e-7
    return {"cutoff_rows": rows, "summary": summary,
            "max_144_vs_192_difference": err, "curve": curve, "f_sum": fsum}


def transfer_matrix(grid_points: int, time_step: float,
                    half_width: float = 6.0, levels: int = 70
                    ) -> tuple[np.ndarray, np.ndarray]:
    """Nystrom discretization of the symmetric primitive path-integral kernel.

    This is an independent representation, at fixed nonzero imaginary-time
    lattice spacing. Its output should NOT equal the continuum result exactly.
    Small positive eigenvalues are truncated; convergence is numerical only.
    """
    q = np.linspace(-half_width, half_width, grid_points)
    dq = q[1] - q[0]
    potential = q * q / 2 + q ** 4
    kernel = dq / np.sqrt(2 * np.pi * time_step) * np.exp(
        -(q[:, None] - q[None, :]) ** 2 / (2 * time_step)
        - time_step * (potential[:, None] + potential[None, :]) / 2)
    vals, vectors = eigh(kernel, subset_by_index=[grid_points - levels, grid_points - 1])
    vals, vectors = vals[::-1], vectors[:, ::-1]
    keep = vals > 1e-14 * vals[0]
    vals, vectors = vals[keep], vectors[:, keep]
    energies = -np.log(vals / vals[0]) / time_step
    return energies, vectors.T @ (q[:, None] * vectors)


def transfer_checks() -> dict[str, Any]:
    rows = []
    compare = []
    for points in (401, 601, 801):
        energies, q = transfer_matrix(points, 1 / 16)
        values = []
        for beta in (None, *BETAS):
            val = susceptibility(energies, q, beta, time_step=1 / 16)
            values.append(val)
            rows.append({"grid_points": points, "time_step": 1 / 16,
                         "beta": "infinity" if beta is None else beta,
                         "chi_zero": val, "lowest_gap": float(energies[1])})
        compare.append(values)
    error = float(np.max(np.abs(np.asarray(compare[-1]) - compare[-2])))
    assert error < 1e-9
    # Approach the continuum independently by reducing the time spacing.
    continuum = []
    reference_e, reference_q = harmonic_basis(192)
    for a in (1 / 16, 1 / 32, 1 / 64, 1 / 128):
        e, q = transfer_matrix(801, a)
        val = susceptibility(e, q, 1.0, time_step=a)
        reference = susceptibility(reference_e, reference_q, 1.0)
        continuum.append({"time_step": a, "chi_beta1": val,
                          "difference_from_continuum_basis": val - reference})
    assert abs(continuum[-1]["difference_from_continuum_basis"]) < 1e-5
    return {"grid_rows": rows, "max_601_vs_801_difference": error,
            "time_spacing_rows": continuum}


def lattice_variances(side: int, beta: float, mass: float = 1.0,
                      spatial_coupling: float = 1.0) -> tuple[float, float]:
    """Exact free-theory variances that determine the first quartic derivative.

    This evaluates sums for an interacting-in-space 3D oscillator lattice.
    It is NOT a finite-coupling quantum many-body simulation.
    """
    s = np.sin(np.pi * np.arange(side) / side) ** 2
    omega = np.sqrt(mass * mass + 4 * spatial_coupling *
                    (s[:, None, None] + s[None, :, None] + s[None, None, :]))
    zero = float(np.mean(1 / (2 * omega)))
    thermal = float(np.mean(1 / (2 * omega * np.tanh(beta * omega / 2))))
    return zero, thermal


def many_site_checks() -> list[dict[str, Any]]:
    rows = []
    for side in (8, 16, 32, 64):
        for beta in (1.0, 0.5, 0.25):
            start = time.perf_counter()
            vacuum, thermal = lattice_variances(side, beta)
            rows.append({"side": side, "spatial_sites": side ** 3,
                         "beta": beta, "mass": 1, "coupling": 1,
                         "vacuum_variance": vacuum, "thermal_variance": thermal,
                         "fractional_missing_first_order_coefficient":
                             (thermal - vacuum) / thermal,
                         "seconds": time.perf_counter() - start})
            assert thermal > vacuum
    return rows


def cycle_laplacian(n: int) -> np.ndarray:
    eye = np.eye(n)
    return 2 * eye - np.roll(eye, 1, axis=0) - np.roll(eye, -1, axis=0)


def finite_matrix_checks() -> dict[str, Any]:
    """Verify the exact first-order Lyapunov identity and Green-function sum."""
    nt, nx = 12, 5
    mass_squared, time_coupling, space_coupling = 1.21, 1.3, 0.7
    K = (mass_squared * np.eye(nt * nx)
         + time_coupling * np.kron(cycle_laplacian(nt), np.eye(nx))
         + space_coupling * np.kron(np.eye(nt), cycle_laplacian(nx)))
    covariance = np.linalg.inv(K)
    c = float(covariance[0, 0])
    anchors = (0, 3)
    p = np.zeros(nt * nx)
    for anchor in anchors:
        p[anchor * nx: (anchor + 1) * nx] = 1
    unanchored = np.diag(1 - p)
    rhs = -(c / 2) * (unanchored @ covariance + covariance @ unanchored)
    derivative = solve_continuous_lyapunov(K, rhs)
    residual = float(np.max(np.abs(K @ derivative + derivative @ K - rhs)))
    mode_errors = []
    anchor_fraction = len(anchors) / nt
    for r in range(nt):
        for k in range(nx):
            z = np.exp(2j * np.pi * (r * np.arange(nt)[:, None] / nt
                                      + k * np.arange(nx)[None, :] / nx))
            z = z.ravel() / np.sqrt(nt * nx)
            eigenvalue = (mass_squared + 4 * time_coupling * np.sin(np.pi * r / nt) ** 2
                          + 4 * space_coupling * np.sin(np.pi * k / nx) ** 2)
            expected = -(1 - anchor_fraction) * c / (2 * eigenvalue ** 2)
            actual = np.vdot(z, derivative @ z)
            mode_errors.append(abs(actual - expected))
    greens_errors = []
    target_x = 2
    rows = np.arange(nt) * nx + target_x
    for anchor in anchors:
        cols = anchor * nx + np.arange(nx)
        greens_errors.append(abs(covariance[np.ix_(rows, cols)].sum()
                                 - 1 / mass_squared))
    result = {"time_sites": nt, "space_sites": nx, "anchors": list(anchors),
              "lyapunov_residual_max": residual,
              "fourier_derivative_error_max": float(max(mode_errors)),
              "greens_identity_error_max": float(max(greens_errors)),
              "inverse_K_minimum_entry": float(covariance.min())}
    assert residual < 1e-11 and max(mode_errors) < 1e-11 and max(greens_errors) < 1e-11
    assert covariance.min() >= -1e-12
    return result


def independent_noise_check() -> dict[str, Any]:
    """A separate covariance obstruction for a proposed thermal-field repair.

    The finite-temperature Euclidean covariance on its physical strip is
    NOT the response covariance used elsewhere; keep this distinction.
    """
    beta, omega, separation = 1.0, 1.0, 0.5
    bose = 1 / np.expm1(beta * omega)
    d0 = bose / omega
    dt = d0 * np.cosh(omega * separation)
    eigenvalues = np.linalg.eigvalsh([[d0, dt], [dt, d0]])
    assert eigenvalues[0] < 0
    return {"beta": beta, "omega": omega, "separation": separation,
            "covariance_difference_eigenvalues": eigenvalues.tolist(),
            "interpretation": "No independent stationary positive additive thermal-field correction"}


def perturbative_oscillator_checks() -> list[dict[str, Any]]:
    """Independent finite-difference check of the right derivative at lambda=0."""
    dimension = 144
    lowering = np.diag(np.sqrt(np.arange(1, dimension + 4)), 1)
    qfull = (lowering + lowering.T) / np.sqrt(2.0)
    q = qfull[:dimension, :dimension]
    qfour = np.linalg.matrix_power(qfull, 4)[:dimension, :dimension]
    hzero = np.diag(np.arange(dimension) + 0.5)
    spectra = []
    for coupling in (1e-4, 5e-5):
        e, u = eigh(hzero + coupling * qfour / 24)
        spectra.append((coupling, e, u.T @ q @ u))
    rows = []
    for beta in BETAS:
        for eta in (0.0, 0.7, 2.0):
            predicted = -(0.5 / np.tanh(beta / 2)) / (2 * (1 + eta * eta) ** 2)
            differences = [(susceptibility(e, q_e, beta, eta)
                            - 1 / (1 + eta * eta)) / coupling
                           for coupling, e, q_e in spectra]
            extrapolated = 2 * differences[1] - differences[0]
            error = abs(extrapolated - predicted)
            assert error < 1e-6
            rows.append({"beta": beta, "eta": eta,
                         "predicted_right_derivative": predicted,
                         "extrapolated_finite_difference": extrapolated,
                         "absolute_difference": error})
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "results")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    results = {
        "status": "Deterministic floating-point checks only; no speedup or novelty certification",
        "environment": {"python": sys.version, "numpy": np.__version__,
                        "scipy": scipy.__version__, "platform": platform.platform()},
        "oscillator": oscillator_checks(),
        "transfer_matrix": transfer_checks(),
        "coupled_lattice_first_order": many_site_checks(),
        "finite_matrix_identities": finite_matrix_checks(),
        "oscillator_first_order": perturbative_oscillator_checks(),
        "independent_additive_noise": independent_noise_check(),
    }
    results["entire_run_seconds"] = time.perf_counter() - start
    (args.out / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_csv(args.out / "oscillator.csv", results["oscillator"]["summary"])
    write_csv(args.out / "oscillator_cutoffs.csv", results["oscillator"]["cutoff_rows"])
    write_csv(args.out / "response_curves.csv", results["oscillator"]["curve"])
    write_csv(args.out / "coupled_lattice.csv", results["coupled_lattice_first_order"])
    write_csv(args.out / "transfer_time_spacings.csv", results["transfer_matrix"]["time_spacing_rows"])
    print(json.dumps({"oscillator": results["oscillator"]["summary"],
                      "finite_matrix_checks": results["finite_matrix_identities"],
                      "seconds": results["entire_run_seconds"],
                      "output_directory": str(args.out.resolve())}, indent=2))


if __name__ == "__main__":
    main()
