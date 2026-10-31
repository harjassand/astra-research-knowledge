"""Exact finite 3D Coulomb matrix for the improved perpendicular carrier.

Data: a real localized x-doublet. Helper: even/odd ENERGY modes along y.
Disjoint hard-wall channels prevent data/helper exchange exactly. All terms
are retained. An ordinary linear y-potential cancels the known common
helper X-force while having no nonconstant projected action on data.
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


def coefficient_matrix(a=1.0, b=0.15, separation=1.5, nlong=128, ntrans=36, nouter=160):
    x, wx = rule(nlong, a)
    s, ws = rule(nlong, a)
    t, wt = rule(ntrans, b)
    p0x = np.cos(np.pi * x / (2 * a)) / np.sqrt(a)
    p1x = np.sin(np.pi * x / a) / np.sqrt(a)
    wl = (p0x + p1x) / np.sqrt(2)
    wr = (p0x - p1x) / np.sqrt(2)
    data_basis = np.stack([(wl * wl + wr * wr) / 2, wl * wl - wr * wr, wl * wr], axis=1)
    p0s = np.cos(np.pi * s / (2 * a)) / np.sqrt(a)
    p1s = np.sin(np.pi * s / a) / np.sqrt(a)
    helper_basis = np.stack([(p0s * p0s + p1s * p1s) / 2,
                             p0s * p0s - p1s * p1s, p0s * p1s], axis=1)
    fd = wx[:, None] * data_basis
    fh = ws[:, None] * helper_basis
    gt = wt * np.cos(np.pi * t / (2 * b)) ** 2 / b
    distance_min = separation - a - b
    assert distance_min > 0
    umax = 8 / distance_min
    u, wu = rule(nouter, umax / 2)
    u = u + umax / 2
    dx2 = (x[:, None] - t[None, :]) ** 2
    dy2 = (t[:, None] - (separation + s)[None, :]) ** 2
    dz2 = (t[:, None] - t[None, :]) ** 2
    matrix = np.zeros((3, 3))
    for value, weight in zip(u, wu):
        xx = fd.T @ np.exp(-value * value * dx2) @ gt
        yy = gt @ np.exp(-value * value * dy2) @ fh
        zz = gt @ np.exp(-value * value * dz2) @ gt
        matrix += (2 / np.sqrt(np.pi)) * weight * np.outer(xx, yy) * zz
    dh = float(np.dot(ws, s * p0s * p1s))
    qd = float(np.dot(wx, x * x * wl * wr))
    assert abs(dh - 32 * a / (9 * np.pi ** 2)) < 1e-12
    assert abs(qd + 3 * a * a / (4 * np.pi ** 2)) < 1e-12
    assert np.max(np.abs(matrix[1, :])) < 1e-13
    assert matrix[2, 2] < 0
    xi = float(2 * matrix[0, 2])
    field = -xi / dh
    # A y-directed linear field is odd in each data transverse wavefunction.
    data_field = float(np.dot(gt, t))
    assert abs(data_field) < 1e-14
    assert abs(xi + field * dh) < 1e-14
    coeff = {
        "constant": float(2 * matrix[0, 0]),
        "z_data": float(matrix[1, 0]),
        "common_helper_Z": float(matrix[0, 1]),
        "z_data_Z_helper": float(matrix[1, 1] / 2),
        "kappa_K_data": float(matrix[2, 0]),
        "common_helper_X_before_compensation": xi,
        "z_data_X_helper": float(matrix[1, 2]),
        "zeta_K_data_Z_helper": float(matrix[2, 1] / 2),
        "lambda_K_data_X_helper": float(matrix[2, 2]),
    }
    return {
        "a": a, "transverse_halfwidth": b, "separation": separation,
        "Coulomb_density_basis_matrix": matrix.tolist(),
        "coefficients_units_C_over_a": coeff,
        "helper_transition_dipole": dh,
        "data_transition_quadrupole_xx": qd,
        "far_field_lambda": float(-4 * a ** 3 / (np.pi ** 4 * separation ** 4)),
        "far_field_kappa": float(3 * a * a / (8 * np.pi ** 2 * separation ** 3)),
        "compensation_field_energy_per_length": field,
        "common_helper_X_after_compensation": xi + field * dh,
        "projected_data_field": data_field,
        "cross_channel_overlap_and_exchange": 0.0,
        "laplace_tail_bound": float(4 * erfc(umax * distance_min) / distance_min),
    }


def main():
    rows = [coefficient_matrix(separation=r) for r in [1.5, 2.0, 4.0, 8.0]]
    fine = coefficient_matrix(separation=1.5, nlong=160, ntrans=48, nouter=200)
    error = np.max(np.abs(np.array(rows[0]["Coulomb_density_basis_matrix"])
                          - np.array(fine["Coulomb_density_basis_matrix"])))
    assert error < 1e-10
    result = {
        "status": "All checks passed",
        "coefficient_units": "C/a; a=1 in table",
        "finite_3D_integrals": rows,
        "quadrature_refinement_max_difference": float(error),
        "scope": "Exact disjoint-support finite-orbital model; mode admission and finite-barrier tails remain separate",
    }
    (OUT / "perpendicular_energy_carrier_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "quadrature_refinement_max_difference": float(error),
                      "couplings": [{"R": row["separation"],
                          **row["coefficients_units_C_over_a"],
                          "compensation_field": row["compensation_field_energy_per_length"]} for row in rows]}, indent=2))


if __name__ == "__main__":
    main()
