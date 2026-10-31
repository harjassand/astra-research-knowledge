"""Finite 3D Coulomb integrals for an explicit orbital energy carrier.

Two disjoint parallel rectangular channels have exactly orthogonal orbitals.
The Laplace representation of 1/r reduces all six-dimensional direct
integrals to one outer quadrature and three two-dimensional quadratures.
All allowed and symmetry-forbidden projected Coulomb coefficients are kept.
This is a finite-orbital construction, not a qualified finite-barrier device.
"""

from pathlib import Path
import json
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import erfc


OUT = Path(__file__).resolve().parent


def rule(n, halfwidth):
    x, w = leggauss(n)
    return halfwidth * x, halfwidth * w


def coefficients(a=1.0, b=0.15, separation=1.0, nlong=128, ntrans=36, nouter=160):
    x, wx = rule(nlong, a)
    y, wy = rule(ntrans, b)
    psi0 = np.cos(np.pi * x / (2 * a)) / np.sqrt(a)
    psi1 = np.sin(np.pi * x / a) / np.sqrt(a)
    wl = (psi0 + psi1) / np.sqrt(2)
    wr = (psi0 - psi1) / np.sqrt(2)
    # avg density, difference density, transition density.
    basis = np.stack([(wl * wl + wr * wr) / 2, wl * wl - wr * wr, wl * wr], axis=1)
    f = wx[:, None] * basis
    transverse_density = np.cos(np.pi * y / (2 * b)) ** 2 / b
    gy = wy * transverse_density
    distance_min = separation - 2 * b
    assert distance_min > 0
    umax = 8 / distance_min
    u, wu = rule(nouter, umax / 2)
    u = u + umax / 2
    matrix = np.zeros((3, 3))
    dx2 = (x[:, None] - x[None, :]) ** 2
    dy2 = (y[:, None] - y[None, :] - separation) ** 2
    dz2 = (y[:, None] - y[None, :]) ** 2
    for value, weight in zip(u, wu):
        xx = f.T @ (np.exp(-value * value * dx2) @ f)
        yy = gy @ np.exp(-value * value * dy2) @ gy
        zz = gy @ np.exp(-value * value * dz2) @ gy
        matrix += (2 / np.sqrt(np.pi)) * weight * xx * yy * zz
    norm0 = float(np.dot(wx, wl * wl))
    norm1 = float(np.dot(wx, wr * wr))
    overlap = float(np.dot(wx, wl * wr))
    transition_moment = float(np.dot(wx, x * x * wl * wr))
    dipole_difference = float(np.dot(wx, x * (wl * wl - wr * wr)))
    assert abs(norm0 - 1) < 1e-12 and abs(norm1 - 1) < 1e-12
    assert abs(overlap) < 1e-12
    assert abs(transition_moment + 3 * a * a / (4 * np.pi ** 2)) < 1e-12
    assert abs(dipole_difference - 64 * a / (9 * np.pi ** 2)) < 1e-12
    assert abs(matrix[1, 2]) < 1e-13 and abs(matrix[2, 1]) < 1e-13
    assert matrix[2, 2] > 0
    return {
        "a": a, "transverse_halfwidth": b, "separation": separation,
        "mode_norms": [norm0, norm1], "within_channel_overlap": overlap,
        "cross_channel_overlap_and_exchange": 0.0,
        "transition_quadrupole_xx": transition_moment,
        "difference_density_dipole_x": dipole_difference,
        "Coulomb_density_basis_matrix_units_C_over_a": matrix.tolist(),
        "coefficients": {
            "constant": float(2 * matrix[0, 0]),
            "z_data": float(matrix[1, 0]),
            "Z_helper": float(matrix[0, 1]),
            "chi_z_data_Z_helper": float(matrix[1, 1] / 2),
            "kappa_K_data": float(matrix[2, 0]),
            "xi_X_helper": float(2 * matrix[0, 2]),
            "alpha_z_data_X_helper": float(matrix[1, 2]),
            "beta_K_data_Z_helper": float(matrix[2, 1] / 2),
            "lambda_K_data_X_helper": float(matrix[2, 2]),
        },
        "far_field_lambda": float(81 * a ** 4 / (64 * np.pi ** 4 * separation ** 5)),
        "far_field_chi": float(2048 * a * a / (81 * np.pi ** 4 * separation ** 3)),
        "lambda_over_chi": float(2 * matrix[2, 2] / matrix[1, 1]),
        "laplace_tail_bound_all_coefficients": float(4 * erfc(umax * distance_min) / distance_min),
    }


def main():
    rows = [coefficients(separation=r) for r in [1.0, 2.0, 4.0, 8.0]]
    fine = coefficients(separation=1.0, nlong=160, ntrans=48, nouter=200)
    difference = np.max(np.abs(np.array(rows[0]["Coulomb_density_basis_matrix_units_C_over_a"])
                               - np.array(fine["Coulomb_density_basis_matrix_units_C_over_a"])))
    assert difference < 1e-10
    result = {"status": "All checks passed", "coefficient_units": "C/a; a=1 in table",
              "finite_3D_integrals": rows,
              "quadrature_refinement_max_difference": float(difference),
              "scope": "Exact hard-wall orbital projection; no finite-barrier, source-spectrum, or gate window asserted"}
    (OUT / "energy_carrier_coulomb_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "quadrature_refinement_max_difference": float(difference),
                      "couplings": [{"R": row["separation"],
                          **row["coefficients"],
                          "lambda_over_chi": row["lambda_over_chi"]} for row in rows]}, indent=2))


if __name__ == "__main__":
    main()
