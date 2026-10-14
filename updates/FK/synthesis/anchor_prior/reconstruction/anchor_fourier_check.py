"""Independent finite-lattice check of the one-slice source drift.

The code differentiates the stationary covariance of the quadratic target SDE
at lambda=0.  It uses the physical Euclidean lattice action normalization
K_a = a(-Delta_a + m^2), g_a = a*lambda/6, and an independent, centered
thermal source in the one interaction slice.  This is a narrow replay of the
equation-level countertest, not a simulation of Pawlowski-Rothkopf code.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def euclidean_matrix(n: int, spacing: float, mass: float) -> np.ndarray:
    """Hessian of a periodic 1D Euclidean action on n sites."""
    lap = 2.0 * np.eye(n)
    for j in range(n):
        lap[j, (j - 1) % n] -= 1.0
        lap[j, (j + 1) % n] -= 1.0
    return lap / spacing + spacing * mass**2 * np.eye(n)


def thermal_variance_lattice(n: int, beta: float, mass: float) -> float:
    spacing = beta / n
    return float(np.linalg.inv(euclidean_matrix(n, spacing, mass))[0, 0])


def anchor_mode_derivative(n: int, spacing: float, mass: float, q: int) -> dict:
    """Return d/dlambda of the intensive frequency correlator at lambda=0."""
    k = euclidean_matrix(n, spacing, mass)
    cov = np.linalg.inv(k)
    c0_lattice = float(cov[0, 0])

    # P fixes one site (the initial-condition slice in 0+1d); all other
    # quartic drifts act on the noncompact target X.  Y is independent at
    # lambda=0, so E[Y^3 X_j] = 0 and it drops from the first derivative.
    p = np.zeros((n, n))
    p[0, 0] = 1.0
    qmask = np.eye(n) - p

    # d/dlambda of the drift coefficient a*lambda/6 times X^3, followed by
    # Wick contraction E[X_i^3 X_j] = 3 C_ii C_ij.
    rhs = -(spacing * c0_lattice / 2.0) * (qmask @ cov + cov @ qmask)
    eigval, eigvec = np.linalg.eigh(k)
    rhs_eig = eigvec.T @ rhs @ eigvec
    dc_eig = rhs_eig / (eigval[:, None] + eigval[None, :])
    dc = eigvec @ dc_eig @ eigvec.T
    residual = float(np.linalg.norm(k @ dc + dc @ k - rhs, ord="fro"))

    site = np.arange(n)
    mode = np.exp(2j * np.pi * q * site / n) / math.sqrt(n)
    p_q = 4.0 / spacing**2 * math.sin(math.pi * q / n) ** 2
    h_q = mass**2 + p_q
    intensive_derivative = float(spacing * np.vdot(mode, dc @ mode).real)
    formula_derivative = -c0_lattice * (1.0 - 1.0 / n) / (2.0 * h_q**2)
    return {
        "N_omega": n,
        "a": spacing,
        "physical_length": n * spacing,
        "mode_index": q,
        "omega_grid": 2.0 * math.pi * q / (n * spacing),
        "lattice_P_omega": p_q,
        "c_noncompact_finite_N": c0_lattice,
        "dG_intensive_dlambda_matrix": intensive_derivative,
        "dG_intensive_dlambda_closed_form": formula_derivative,
        "closed_form_abs_residual": abs(intensive_derivative - formula_derivative),
        "sylvester_frobenius_residual": residual,
    }


def main() -> None:
    beta = 1.0
    mass = 1.0
    compact_n = 16
    a = beta / compact_n
    c_beta_lattice = thermal_variance_lattice(compact_n, beta, mass)
    c_beta_continuum = 0.5 / math.tanh(beta * mass / 2.0)
    c_zero_lattice_limit = 1.0 / (mass * math.sqrt(4.0 + (a * mass) ** 2))
    c_zero_continuum = 1.0 / (2.0 * mass)

    ns = [8, 16, 32, 64, 128, 256, 512]
    outputs = []
    for n in ns:
        q = int(round(0.5 * (n * a) / (2.0 * math.pi)))
        row = anchor_mode_derivative(n, a, mass, q)
        h_q = mass**2 + row["lattice_P_omega"]
        thermal_derivative = -c_beta_lattice / (2.0 * h_q**2)
        row["dG_intensive_dlambda_thermal_lattice"] = thermal_derivative
        row["fraction_thermal_derivative_missing"] = 1.0 - abs(
            row["dG_intensive_dlambda_matrix"] / thermal_derivative
        )
        outputs.append(row)

    physical_eta = 0.5
    eta_h = mass**2 + physical_eta**2
    target_zero_continuum = -c_beta_continuum / (2.0 * eta_h**2)
    anchor_zero_continuum = -c_zero_continuum / (2.0 * eta_h**2)
    missing_fraction = 1.0 - abs(anchor_zero_continuum / target_zero_continuum)

    report = {
        "scope": "Independent weak-coupling equation check for one fixed thermal anchor in 0+1d.",
        "parameters": {"beta": beta, "mass": mass, "N_tau": compact_n, "a": a},
        "compact_source_free_variance_lattice": c_beta_lattice,
        "compact_source_free_variance_continuum": c_beta_continuum,
        "noncompact_target_free_variance_lattice_limit": c_zero_lattice_limit,
        "noncompact_target_free_variance_continuum": c_zero_continuum,
        "target_source_first_derivative_at_eta_0.5_continuum": target_zero_continuum,
        "one_anchor_target_first_derivative_at_eta_0.5_continuum": anchor_zero_continuum,
        "fraction_of_target_thermal_derivative_missing": missing_fraction,
        "finite_N_sylvester_results": outputs,
        "interpretation": (
            "The anchor source variance c_beta does not enter the order-lambda target covariance "
            "because its independent centered cubic force has zero cross term at lambda=0. "
            "The N_omega-normalized mode derivative tends to the noncompact/vacuum coefficient; "
            "the full thermal path instead carries c_beta."
        ),
    }
    out = Path(__file__).with_name("anchor_fourier_results.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
