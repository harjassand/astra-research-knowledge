#!/usr/bin/env python3
"""Numerical replay of a positive nonlocal spring kernel with axial rods.

Only numpy and the Python standard library are required.  The output counts
all roots x=cos(q) in (-1,1) of the supplied secular polynomial, so each
generic simple root contributes one right-moving channel.  The eliminated-rod
formula is singular at exact rod poles; compatible node-bearing modes can
exist there.  The midpoint integral skips those isolated frequencies, which
do not affect its frequency integral.
"""
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from numpy.polynomial import chebyshev as cheb


R_FRACTION = 0.1             # connector mass / fixed total mass
ETA = 0.08                   # omega_u * a/c
U_CUTOFF = 15.0
GRID_SIZES = (75001, 150001, 300001)
N_VALUES = (2, 4, 8, 16, 32)
T_K = 0.100
C_SOUND = 5000.0
K_B = 1.380649e-23
HBAR = 1.054571817e-34


def weights(N):
    n = np.arange(1, N, dtype=float)
    w = 12.0 * (N - n) / (N * N * (N * N - 1.0))
    return n.astype(int), w


def root_count(N, alpha, r=R_FRACTION):
    """Count simple real x roots in (-1,1) of D(alpha,x)=0."""
    n, w = weights(N)
    theta = n * alpha
    sn = np.sin(theta)
    if np.min(np.abs(sn)) < 1e-14:
        # The midpoint grid should not hit these poles; the perturbation is
        # only a fallback for floating-point coincidences with exact poles.
        alpha += 1.23456789e-12
        theta = n * alpha
        sn = np.sin(theta)
    # D/K = -Mpoint*alpha^2/r + 2 sum w_n theta_n(cos(theta_n)-T_n(x))/sin(theta_n)
    c = np.empty(N, dtype=float)
    c[0] = -(1.0 - r) * alpha * alpha / r + 2.0 * np.sum(
        w * theta * np.cos(theta) / sn
    )
    c[1:] = -2.0 * w * theta / sn
    scale = np.max(np.abs(c))
    if not np.isfinite(scale) or scale == 0.0:
        return 0
    roots = cheb.chebroots(c / scale)
    tol_im = 2e-7
    tol_edge = 2e-9
    count = sum(
        abs(z.imag) <= tol_im * (1.0 + abs(z.real))
        # Include numerical roots just outside an endpoint by the root-solver
        # tolerance. Exact x=±1 roots are band edges and have measure zero.
        and -1.0 - tol_edge < z.real < 1.0 + tol_edge
        for z in roots
    )
    return int(count)


def bose(u):
    u = np.asarray(u)
    y = np.ones_like(u, dtype=float)
    nz = u > 0.0
    y[nz] = (2.0 * u[nz] * np.exp(-u[nz]) /
             (-np.expm1(-2.0 * u[nz]))) ** 2
    return y


def channel_integral(N, points, r=R_FRACTION, cutoff=U_CUTOFF, return_profile=False):
    """Midpoint integral of Bose weight times exact all-root channel count."""
    du = cutoff / points
    u = (np.arange(points, dtype=float) + 0.5) * du
    alpha = ETA * u
    counts = np.fromiter((root_count(N, a, r) for a in alpha),
                         dtype=np.int16, count=points)
    vals = bose(u) * counts
    J = float(np.sum(vals) * du)
    info = {
        "J": J,
        "grid_points": int(points),
        "du": float(du),
        "max_channels_seen": int(counts.max(initial=0)),
        "samples_with_multiple_channels": int(np.count_nonzero(counts > 1)),
        "integral_tail_bound_after_cutoff": int(N - 1) * bose_tail(cutoff),
    }
    if return_profile:
        info["u"] = u
        info["counts"] = counts
    return info


def bose_tail(U):
    e = math.exp(-2.0 * U)
    return e * (2.0 * U * U + 2.0 * U + 1.0) / (1.0 - e) ** 2


def point_fejer_integral(N, q_points=1_000_001, r=R_FRACTION, eta=ETA):
    """Same-total-mass point-spring reference, with connectors treated as massless.

    This keeps Mtot at each site; it is not the fixed-Mpoint limit of the
    distributed-rod family.
    """
    n, w = weights(N)
    q = np.linspace(0.0, math.pi, q_points)
    S = np.zeros_like(q)
    Sp = np.zeros_like(q)
    for nj, wj in zip(n, w):
        S += wj * (1.0 - np.cos(nj * q))
        Sp += wj * nj * np.sin(nj * q)
    u = np.sqrt(np.maximum(0.0, 2.0 * r * S)) / eta
    up = np.zeros_like(q)
    nz = S > 1e-28
    up[nz] = r * Sp[nz] / (eta * np.sqrt(2.0 * r * S[nz]))
    up[0] = math.sqrt(r) / eta
    dq = math.pi / (q_points - 1)
    y = bose(u) * np.abs(up)
    # Composite Simpson, q_points is odd.
    return float(dq / 3.0 * (y[0] + y[-1] +
                               4.0 * np.sum(y[1:-1:2]) +
                               2.0 * np.sum(y[2:-1:2])))


def local_one_rod_integral(points=300001, r=R_FRACTION, eta=ETA, cutoff=U_CUTOFF):
    """Nearest-neighbour axial rod with same K, Mtotal, a/c, and rod-mass share."""
    du = cutoff / points
    u = (np.arange(points, dtype=float) + 0.5) * du
    alpha = eta * u
    # The degree-one secular root is x=cos(alpha)-(Mpoint/r)*alpha*sin(alpha)/2.
    x = np.cos(alpha) - ((1.0 - r) / r) * alpha * np.sin(alpha) / 2.0
    count = ((x > -1.0) & (x < 1.0)).astype(np.int8)
    return {
        "J": float(np.sum(bose(u) * count) * du),
        "grid_points": int(points),
        "du": float(du),
        "max_channels_seen": int(count.max(initial=0)),
        "samples_with_multiple_channels": 0,
        "integral_tail_bound_after_cutoff": bose_tail(cutoff),
    }


def pole_summary(N, eta=ETA, cutoff=U_CUTOFF):
    first_highest_range = math.pi / ((N - 1) * eta)
    # Include all unique poles alpha=m*pi/n within the chosen alpha interval.
    poles = set()
    amax = eta * cutoff
    for n in range(1, N):
        for m in range(1, int(amax * n / math.pi) + 1):
            a = m * math.pi / n
            if a < amax:
                poles.add(Fraction(m, n))
    return {
        "first_pole_of_longest_rod_u": first_highest_range,
        "alpha_cutoff": amax,
        "distinct_rod_pole_locations_below_cutoff": len(poles),
    }


def kernel_identity_checks(N_values, r=R_FRACTION):
    checks = {}
    for N in N_values:
        n, w = weights(N)
        stiffness_ratio = float(np.sum(n.astype(float) ** 2 * w))
        rod_mass_fraction = float(r * stiffness_ratio)
        checks[str(N)] = {
            "sum_n2_kappa_over_K": stiffness_ratio,
            "sum_axial_rod_mass_over_Mtotal": rod_mass_fraction,
            "minimum_kappa_over_K": float(np.min(w)),
            "all_axial_rigidities_positive": bool(np.all(w > 0.0)),
            "point_mass_fraction": float(1.0 - rod_mass_fraction),
        }
        if abs(stiffness_ratio - 1.0) > 2e-14:
            raise AssertionError(f"K_eff identity failed for N={N}: {stiffness_ratio}")
        if rod_mass_fraction >= 1.0:
            raise AssertionError(f"point mass is not positive for N={N}")
    return checks


def selected_q_sign_crosschecks():
    """Independent dense-q sign-crossing checks away from poles/edges."""
    cases = []
    q = np.linspace(0.0, math.pi, 65537)
    for N in N_VALUES:
        n, w = weights(N)
        for alpha in (0.037, 0.173, 0.411, 0.673, 1.137):
            theta = n * alpha
            sn = np.sin(theta)
            if np.min(np.abs(sn)) < 1e-5:
                continue
            c = np.empty(N, dtype=float)
            c[0] = -(1.0 - R_FRACTION) * alpha * alpha / R_FRACTION + 2.0 * np.sum(
                w * theta * np.cos(theta) / sn
            )
            c[1:] = -2.0 * w * theta / sn
            roots = cheb.chebroots(c / np.max(np.abs(c)))
            poly_count = sum(
                abs(z.imag) <= 2e-7 * (1.0 + abs(z.real))
                and -1.0 - 2e-9 < z.real < 1.0 + 2e-9
                for z in roots
            )
            values = cheb.chebval(np.cos(q), c)
            sign_count = int(np.count_nonzero(values[:-1] * values[1:] < 0.0))
            cases.append({
                "N": N,
                "alpha": alpha,
                "polynomial_root_count": int(poly_count),
                "dense_q_sign_change_count": sign_count,
                "agreement": int(poly_count) == sign_count,
            })
    return {
        "cases": cases,
        "all_agree": all(c["agreement"] for c in cases),
        "count": len(cases),
        "q_grid_points_per_case": len(q),
    }


def main():
    omega_u = 2.0 * K_B * T_K / HBAR
    a = ETA * C_SOUND / omega_u
    # Normalize Mtotal=1; then K/Mtotal = r*c^2/a^2 = r*omega_u^2/eta^2.
    K_over_Mtotal = R_FRACTION * omega_u**2 / ETA**2
    result = {
        "declared_model": "periodic point masses joined by separate uniform axial rods of lengths n*a",
        "temperature_K": T_K,
        "omega_thermal_rad_s": omega_u,
        "eta_omega_thermal_a_over_c": ETA,
        "connector_rod_mass_fraction": R_FRACTION,
        "point_mass_fraction_of_total": 1.0 - R_FRACTION,
        "example_sound_speed_m_s": C_SOUND,
        "implied_cell_length_m": a,
        "stiffness_per_total_mass_s_minus2": K_over_Mtotal,
        "kernel": "kappa_n/K=12*(N-n)/(N^2*(N^2-1)), n=1..N-1",
        "kernel_checks_by_N": kernel_identity_checks(N_VALUES),
        "selected_q_sign_crosschecks": selected_q_sign_crosschecks(),
        "rod_pole_summary": {str(N): pole_summary(N) for N in N_VALUES},
        "continuum_rod_results": {},
        "local_nearest_neighbor_rod_same_resources": local_one_rod_integral(),
        "massless_point_Fejér_reference": {},
        "integration": {
            "variable": "u=omega/omega_thermal",
            "range": [0.0, U_CUTOFF],
            "channel_bound": "N_ch <= N-1 away from exact rod poles, by polynomial degree",
            "tail_bound_per_max_channel": bose_tail(U_CUTOFF),
            "root_rule": "count simple real roots x in (-1,1); each yields one positive-velocity root among q=±acos(x)",
        },
        "scope": "ideal axial-rod graph with distributed rod modes; no packing, junction, damping, or device claim",
    }
    # Grid refinement. N=32 can be expensive, but is included under the same
    # bounded run with the coarsest/finer replay visible in the JSON.
    for N in N_VALUES:
        rows = []
        points_to_run = GRID_SIZES + ((600001,) if N == 32 else ())
        for pts in points_to_run:
            rows.append(channel_integral(N, pts))
        result["continuum_rod_results"][str(N)] = {
            "point_mass_fejer_J_same_total_mass_and_K": point_fejer_integral(N),
            "refinements": rows,
        }
    local_j = result["local_nearest_neighbor_rod_same_resources"]["J"]
    n2_j = result["continuum_rod_results"]["2"]["refinements"][-1]["J"]
    result["crosscheck_N2_equals_local_one_rod"] = {
        "N2_finiterange_J": n2_j,
        "local_one_rod_J": local_j,
        "absolute_difference": abs(n2_j - local_j),
        "interpretation": "same one-rod model at N=2; difference is only finite quadrature/root tolerance",
    }
    out_path = Path(__file__).with_name("nonlocal_distributed_rods_results.json")
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
