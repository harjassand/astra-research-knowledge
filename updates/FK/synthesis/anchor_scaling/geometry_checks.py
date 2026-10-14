#!/usr/bin/env python3
"""Independent checks for massive-Green anchor geometry and source covariance.

Exact Fraction arithmetic checks the 1D spatial Green matrix and its row-sum /
walk-decay bounds. Floating point linear-algebra checks the general-mask
first-order Lyapunov identity. The covariance scaling formulas are evaluated
exactly for coherent and iid stationary sources in a linear forced comparator.
These are controlled mathematical diagnostics, not a simulation of the
nonlinear anchored quantum-response sampler.
"""
from __future__ import annotations

from fractions import Fraction
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import solve_sylvester


def inverse_fraction(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(matrix)
    a = [row[:] + [Fraction(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for r in range(n):
            if r == col:
                continue
            factor = a[r][col]
            if factor:
                a[r] = [x - factor * y for x, y in zip(a[r], a[col])]
    return [row[n:] for row in a]


def cycle_laplacian(n: int) -> list[list[Fraction]]:
    out = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        out[i][i] = Fraction(2)
        out[i][(i - 1) % n] -= 1
        out[i][(i + 1) % n] -= 1
    return out


def exact_green_check() -> dict:
    n = 13
    alpha, kappa = Fraction(1), Fraction(1)
    lap = cycle_laplacian(n)
    k = [[alpha * Fraction(i == j) + kappa * lap[i][j]
          for j in range(n)] for i in range(n)]
    g = inverse_fraction(k)
    rho = Fraction(2 * kappa, alpha + 2 * kappa)
    row_sums = [sum(row, Fraction(0)) for row in g]
    assert all(s == 1 / alpha for s in row_sums)
    assert all(g[i][j] >= 0 for i in range(n) for j in range(n))
    distances = [min(i, n - i) for i in range(n)]
    bounds = [Fraction(1, 1) / alpha * rho ** d for d in distances]
    assert all(g[0][j] <= bounds[j] for j in range(n))
    return {
        "n_cycle": n,
        "alpha": str(alpha),
        "kappa": str(kappa),
        "row_sum_exact": str(row_sums[0]),
        "neumann_rho_exact": str(rho),
        "green_row_from_site_0": [str(x) for x in g[0]],
        "distance_bounds_from_site_0": [str(x) for x in bounds],
        "all_nonnegative": True,
        "all_walk_bounds_pass": True,
    }


def temporal_geometry_check() -> dict:
    # Exact row sum gives exact random-placement means. Small moving-cycle
    # inverses independently illustrate the graph-distance suppression.
    alpha = Fraction(1)
    kappa = Fraction(1)
    rho = Fraction(2, 3)  # Neumann-walk upper bound for degree two.
    rows = []
    for n in (100, 400, 1600):
        root = math.isqrt(n)
        assert root * root == n
        r = root
        full_slice = Fraction(r, root)  # r full spatial slices, row sum 1/alpha.

        # One site is anchored each time at graph distance R_N. Choose R_N so
        # the proved walk bound is <=1/log(N), and invert that finite cycle
        # exactly as an additional check.
        R = (math.ceil(math.log(root) / -math.log(float(rho)))
             + math.ceil(math.log(math.log(n)) / -math.log(float(rho))))
        m_remote = 2 * R + 1
        lap_r = cycle_laplacian(m_remote)
        k_r = [[alpha * Fraction(i == j) + kappa * lap_r[i][j]
                for j in range(m_remote)] for i in range(m_remote)]
        g_r = inverse_fraction(k_r)
        remote_value = g_r[0][R]
        remote_exposure = root * remote_value
        remote_bound = root * rho ** R
        assert remote_exposure <= remote_bound

        # One independent uniform spatial anchor at each time. The exposure
        # mean is sqrt(N)/(alpha*M); its variance is <=1/(alpha^2 M).
        m_sqrt = root
        m_large = n
        rows.append({
            "N": n,
            "full_space_r_slices_r_eq_sqrtN_exposure_exact": str(full_slice),
            "moving_anchor_distance_R": R,
            "moving_cycle_size": m_remote,
            "moving_anchor_G_exact": str(remote_value),
            "moving_anchor_exposure_exact": str(remote_exposure),
            "moving_anchor_walk_bound": str(remote_bound),
            "moving_anchor_walk_bound_decimal": float(remote_bound),
            "random_one_per_slice_M_eq_sqrtN_expected_exposure": str(Fraction(root, m_sqrt)),
            "random_one_per_slice_M_eq_N_expected_exposure": str(Fraction(root, m_large)),
            "random_M_eq_sqrtN_variance_upper_bound": str(Fraction(1, m_sqrt)),
            "random_M_eq_N_variance_upper_bound": str(Fraction(1, m_large)),
        })
    return {
        "alpha": str(alpha),
        "kappa": str(kappa),
        "neumann_rho": str(rho),
        "random_geometry_expectation_identity": "E[G(x,Y)] = 1/(alpha*M)",
        "random_geometry_variance_bound": "Var(N^-1/2 sum_s G(x,Y_s)) <= 1/(alpha^2*M)",
        "rows": rows,
    }


def source_covariance_check() -> dict:
    # In the exact linear comparator, a local zero-frequency output has
    # F_delta = G_xx/sqrt(N) * sum_{s in S} xi_s. Both source families below
    # are centered, stationary, and have the same unit one-site variance.
    nspace = 13
    alpha = Fraction(1)
    kappa = Fraction(1)
    lap = cycle_laplacian(nspace)
    k = [[alpha * Fraction(i == j) + kappa * lap[i][j]
          for j in range(nspace)] for i in range(nspace)]
    g = inverse_fraction(k)
    h = g[0][0]
    rows = []
    for n in (100, 400, 1600):
        r = math.isqrt(n)
        # Common-mode source xi_s=Z: C(s,t)=1, exactly stationary but not
        # mixing. iid source has C(s,t)=1_{s=t}, also stationary.
        var_common = h * h * Fraction(r * r, n)
        var_iid = h * h * Fraction(r, n)
        rows.append({
            "N": n,
            "r": r,
            "Var_common_mode_exact": str(var_common),
            "Var_iid_exact": str(var_iid),
            "Var_common_mode_float": float(var_common),
            "Var_iid_float": float(var_iid),
        })
    return {
        "Gxx": str(h),
        "same_marginal_variance": 1,
        "common_mode_covariance": "C(s,t)=1 for all s,t",
        "iid_covariance": "C(s,t)=1{s=t}",
        "rows": rows,
    }


def lyapunov_mask_check() -> dict:
    # Independent dense implementation of the first right derivative for a
    # symmetric independent source. Q=I-P is the set whose cubic is retained.
    n = 12
    alpha, kappa = 1.3, 0.7
    lap = np.zeros((n, n))
    for i in range(n):
        lap[i, i] = 2.0
        lap[i, (i - 1) % n] -= 1.0
        lap[i, (i + 1) % n] -= 1.0
    k = alpha * np.eye(n) + kappa * lap
    cmat = np.linalg.inv(k)
    c = float(np.diag(cmat)[0])
    masks = [
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    ]
    rows = []
    for mask in masks:
        p = np.diag(np.asarray(mask, dtype=float))
        q = np.eye(n) - p
        rhs = -(c / 2.0) * (q @ cmat + cmat @ q)
        c1 = solve_sylvester(k, k, rhs)
        maxerr = 0.0
        mode_rows = []
        for j in range(n):
            phase = np.exp(2j * np.pi * j * np.arange(n) / n)
            v = phase / np.sqrt(n)
            eigenvalue = alpha + 4 * kappa * math.sin(math.pi * j / n) ** 2
            actual = float(np.real(np.vdot(v, c1 @ v)))
            fraction = float(np.sum(mask) / n)
            predicted = -c * (1 - fraction) / (2 * eigenvalue ** 2)
            err = abs(actual - predicted)
            maxerr = max(maxerr, err)
            if j in (0, 1, n // 2):
                mode_rows.append({
                    "mode": j,
                    "anchor_fraction": fraction,
                    "actual": actual,
                    "predicted": predicted,
                    "absolute_error": err,
                })
        assert maxerr < 2e-12, maxerr
        rows.append({"mask": mask, "max_mode_error": maxerr,
                     "selected_modes": mode_rows})
    return {
        "N_cycle": n,
        "alpha": alpha,
        "kappa": kappa,
        "onsite_reference_variance": c,
        "identity": "d C_vv/dlambda = -c*(1-f)/(2*k_q^2)",
        "rows": rows,
    }


def continuum_scaling_check() -> dict:
    # Discretized oscillator action on a periodic interval of physical length
    # T=N*a, with a separate compact source period beta=1.
    mass, lam, beta_source = 1.0, 1.0, 1.0
    c_source = 0.5 / math.tanh(beta_source * mass / 2.0)
    c_zero = 1.0 / (2.0 * mass)
    rows = []
    for target_length in (1.0, 4.0, 16.0):
        for a in (1 / 16, 1 / 32, 1 / 64):
            n = round(target_length / a)
            modes = np.arange(n)
            eig = a * mass * mass + (4.0 / a) * np.sin(np.pi * modes / n) ** 2
            local_c_target = float(np.mean(1.0 / eig))
            g = a * lam / 6.0
            # BL sub-Gaussian sixth moments for the compact beta-source and
            # the finite-T target; both are O(1) in a. Also retain the
            # long-target vacuum asymptotic separately.
            b_bound = math.sqrt(96.0) * g * (c_source ** 1.5 + local_c_target ** 1.5)
            b_bound_long = math.sqrt(96.0) * g * (c_source ** 1.5 + c_zero ** 1.5)
            alpha = a * mass * mass
            r_exposure = min(n, math.ceil(math.sqrt(target_length) / a))
            row = {"target_length_T": target_length, "N": n, "a": a,
                   "alpha": alpha, "kappa_tau": 1.0 / a,
                   "kappa_x_over_fixed_graph": a, "g": g,
                   "target_local_green_diagonal_c_a": local_c_target,
                   "target_continuum_c_T": 0.5 / math.tanh(target_length * mass / 2.0),
                   "compact_source_c_beta": c_source,
                   "vacuum_reference_c_infinity": c_zero,
                   "B_local_moment_bound": b_bound,
                   "B_asymptotic_long_target_bound": b_bound_long,
                   "B_over_alpha": b_bound / alpha,
                   "physical_zero_mode_reference_bound_a_over_alpha": a / alpha,
                   "r_exposure_scale": r_exposure,
                   "r_exposure_scale_temporal_fraction": r_exposure / n}
            for label, r in (("r1", 1), ("rsqrtN", math.isqrt(n)),
                             ("rexposure", r_exposure), ("rN", n)):
                # F_phys=sqrt(a)*F_N; D_phys=r*B/(m^2*sqrt(T)).
                row[f"physical_amplitude_bound_{label}"] = (
                    math.sqrt(a) * r * b_bound / (alpha * math.sqrt(n)))
            rows.append(row)
    return {
        "action": "sum_t[(q[t+1]-q[t])^2/(2a)+a*m^2*q[t]^2/2+a*lambda*q[t]^4/24]",
        "mapping": {"alpha": "a*m^2", "kappa_tau": "1/a", "kappa_x": "a*kappa", "g": "a*lambda/6"},
        "compact_source_beta": beta_source,
        "mass": mass,
        "quartic_lambda": lam,
        "continuum_compact_source_variance": c_source,
        "continuum_zero_temperature_target_variance": c_zero,
        "rows": rows,
        "scope": "temporal continuum scaling with fixed compact source beta, finite spatial cutoff, and target length T; not a spatial continuum/renormalization result",
    }


def main() -> None:
    result = {
        "scope": "independent exact/controlled checks; not a nonlinear sampler replay",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "exact_spatial_green": exact_green_check(),
        "moving_random_geometry": temporal_geometry_check(),
        "stationary_source_covariance": source_covariance_check(),
        "arbitrary_mask_first_order": lyapunov_mask_check(),
        "fixed_beta_temporal_continuum_scaling": continuum_scaling_check(),
    }
    out = Path(__file__).parent / "results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(out)
    print(json.dumps({
        "green_exact_row_sum": result["exact_spatial_green"]["row_sum_exact"],
        "green_rho": result["exact_spatial_green"]["neumann_rho_exact"],
        "covariance_scaling": result["stationary_source_covariance"]["rows"],
        "max_lyapunov_error": max(x["max_mode_error"]
                                    for x in result["arbitrary_mask_first_order"]["rows"]),
        "continuum_scaling": result["fixed_beta_temporal_continuum_scaling"]["rows"],
    }, indent=2))


if __name__ == "__main__":
    main()
