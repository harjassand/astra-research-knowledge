#!/usr/bin/env python3
"""Independent explicit-FD replay of the pinned SkullWave notebook model.

This directly transcribes its centered-space/forward-time scheme and Dirichlet
boundary conditions. It is an independent implementation, not Mathematica
execution. See source_refs/Tissue_model_simulator.nb around PDEsys,
discretization1, In[534], and In[546].
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def solve_tridiagonal(rhs: np.ndarray, dx: float, eta: float, gamma: float) -> np.ndarray:
    """Solve (eta*dxx-gamma) v = rhs with zero Dirichlet endpoints."""
    n = rhs.size
    off = eta / (dx * dx)
    diag = 2.0 * off + gamma
    # Multiply equation by -1 so the Thomas pivots are positive.
    cp = np.empty(n, dtype=float)
    dp = np.empty(n, dtype=float)
    denom = diag
    cp[0] = -off / denom
    dp[0] = -rhs[0] / denom
    for i in range(1, n):
        denom = diag + off * cp[i - 1]
        cp[i] = (-off / denom) if i < n - 1 else 0.0
        dp[i] = (-rhs[i] + off * dp[i - 1]) / denom
    out = np.empty(n, dtype=float)
    out[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        out[i] = dp[i] - cp[i] * out[i + 1]
    return out


def solve_tridiagonal_fft(rhs: np.ndarray, dx: float, eta: float, gamma: float) -> np.ndarray:
    """Diagonalize the same zero-Dirichlet tridiagonal operator by DST-I.

    This is an exact spectral solve of the discrete linear system (up to
    floating-point roundoff), used only to accelerate high-resolution sweeps.
    """
    n = rhs.size + 1
    odd_extension = np.zeros(2 * n, dtype=float)
    odd_extension[1:n] = rhs
    odd_extension[n + 1 :] = -rhs[::-1]
    sine_rhs = -np.fft.fft(odd_extension)[1:n].imag / 2.0
    k = np.arange(1, n, dtype=float)
    eigenvalues = -gamma - 4.0 * eta / (dx * dx) * np.sin(np.pi * k / (2.0 * n)) ** 2
    sine_solution = sine_rhs / eigenvalues
    spectrum = np.zeros(2 * n, dtype=complex)
    spectrum[1:n] = -2j * sine_solution
    spectrum[n + 1 :] = 2j * sine_solution[::-1]
    return np.fft.ifft(spectrum).real[1:n]


def run(
    nx: int = 200,
    nt: int = 100,
    a_phi: float = 4.0,
    alpha: float = 3.5e-6,
    eta_scale: float = 1.0,
    a_rho: float = 4.0,
    fast_solve: bool = False,
) -> dict:
    # Values copied from the pinned notebook's parameter and mesh cells.
    L = 1500.0
    tmax = 8.0
    dt = tmax / nt
    dx = 2.0 * L / nx
    x = np.linspace(-L, L, nx + 1)
    t = np.linspace(0.0, tmax, nt + 1)

    rho_a, rho_b, tau = 0.0067, 0.0077, 10.0
    D = 15.0
    e_m, e_o = 30.0 * 12.96, 1000.0 * 12.96
    eta = eta_scale * 1000.0 * 12.96 / 3600.0
    gamma = 0.8 * 1000.0 * 12.96 / 3600.0
    rho_h = 1.0 / 1000.0
    rho = 0.5 * (np.tanh(a_rho * x / L) + 1.0) * (rho_a - rho_b) + rho_b
    phi = 0.5 * (1.0 - np.tanh(a_phi * x / L))
    # Enforce the source's Dirichlet values at each step (also equal to these
    # analytical endpoint values in exact arithmetic).
    rho_left, rho_right = float(rho[0]), float(rho[-1])
    phi_left, phi_right = float(phi[0]), float(phi[-1])

    rho_out = np.empty((nx + 1, nt + 1), dtype=float)
    phi_out = np.empty_like(rho_out)
    vel_out = np.empty_like(rho_out)
    rho_out[:, 0], phi_out[:, 0] = rho, phi
    vel_out[:, 0] = 0.0

    for j in range(nt + 1):
        rho_x = (rho[2:] - rho[:-2]) / (2.0 * dx)
        phi_x = (phi[2:] - phi[:-2]) / (2.0 * dx)
        e = e_m + (e_o - e_m) * phi
        e_x = (e_o - e_m) * phi_x
        force_rhs = e[1:-1] * rho_x / rho[1:-1] + e_x * np.log(rho[1:-1] / rho_h)
        v = np.zeros(nx + 1, dtype=float)
        solve = solve_tridiagonal_fft if fast_solve else solve_tridiagonal
        v[1:-1] = solve(force_rhs, dx, eta, gamma)
        vel_out[:, j] = v
        if j == nt:
            break

        # Notebook In[534]: central spatial differences, forward Euler time.
        v_x = (v[2:] - v[:-2]) / (2.0 * dx)
        k_a = (rho_a - rho[1:-1]) / (rho_a * tau)
        k_b = (rho_b - rho[1:-1]) / (rho_b * tau)
        growth = k_a * (1.0 - phi[1:-1]) + k_b * phi[1:-1]
        rho_new = rho.copy()
        rho_new[1:-1] += dt * (
            rho[1:-1] * growth - rho[1:-1] * v_x - v[1:-1] * rho_x
        )

        e_x_phi = (e_o - e_m) * phi_x
        delta_k = k_b - k_a
        k_d = alpha * (e[1:-1] - e_m)
        phi_xx = (phi[2:] - 2.0 * phi[1:-1] + phi[:-2]) / (dx * dx)
        phi_rhs = (
            D * phi_xx
            + D * rho_x * phi_x / rho[1:-1]
            + delta_k * phi[1:-1] * (1.0 - phi[1:-1])
            + k_d * (1.0 - phi[1:-1])
            - v[1:-1] * phi_x
        )
        phi_new = phi.copy()
        phi_new[1:-1] += dt * phi_rhs

        rho_new[0], rho_new[-1] = rho_left, rho_right
        phi_new[0], phi_new[-1] = phi_left, phi_right
        rho, phi = rho_new, phi_new
        rho_out[:, j + 1], phi_out[:, j + 1] = rho, phi

    return {
        "x": x,
        "time": t,
        "rho": rho_out,
        "phi": phi_out,
        "velocity": vel_out,
        "dx_um": dx,
        "dt_hr": dt,
        "nx": nx,
        "nt": nt,
        "a_phi": a_phi,
        "a_rho": a_rho,
        "alpha": alpha,
        "eta_scale": eta_scale,
        "fast_solve": fast_solve,
        "parameters": {
            "D_um2_per_hr": D,
            "alpha": alpha,
            "eM": e_m,
            "eO": e_o,
            "eta": eta,
            "gamma": gamma,
            "rhoh": rho_h,
            "rhoA": rho_a,
            "rhoB": rho_b,
            "tau_hr": tau,
        },
    }


def front_crossings(x: np.ndarray, phi: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    out = []
    for j in range(phi.shape[1]):
        profile = phi[:, j]
        ix = np.flatnonzero((profile[:-1] >= threshold) & (profile[1:] < threshold))
        if len(ix) != 1:
            out.append(float("nan"))
            continue
        i = int(ix[0])
        frac = (threshold - profile[i]) / (profile[i + 1] - profile[i])
        out.append(float(x[i] + frac * (x[i + 1] - x[i])))
    return np.asarray(out)


def summary(run_result: dict, reference_dir: Path | None = None) -> dict:
    x, t = run_result["x"], run_result["time"]
    rho, phi, velocity = run_result["rho"], run_result["phi"], run_result["velocity"]
    front = front_crossings(x, phi)
    slope = float(np.polyfit(t, front, 1)[0])
    front_dot = np.gradient(front, t, edge_order=2)
    front_rho = np.array([np.interp(front[j], x, rho[:, j]) for j in range(len(t))])
    front_v = np.array([np.interp(front[j], x, velocity[:, j]) for j in range(len(t))])
    dlogrho = np.gradient(rho, x, axis=0, edge_order=2) / rho
    front_dlogrho = np.array([np.interp(front[j], x, dlogrho[:, j]) for j in range(len(t))])
    phi_x = np.gradient(phi, x, axis=0, edge_order=2)
    phi_xx = np.gradient(phi_x, x, axis=0, edge_order=2)
    front_phi_x = np.array([np.interp(front[j], x, phi_x[:, j]) for j in range(len(t))])
    front_phi_xx = np.array([np.interp(front[j], x, phi_xx[:, j]) for j in range(len(t))])
    D = run_result["parameters"]["D_um2_per_hr"]
    rho_a, rho_b, tau = 0.0067, 0.0077, 10.0
    delta_k = (rho_b - rho_a) / (tau * rho_b)
    alpha = run_result["parameters"]["alpha"]
    delta_e = run_result["parameters"]["eO"] - run_result["parameters"]["eM"]
    r = delta_k + alpha * delta_e
    q0 = 2.0 * run_result["a_phi"] / 1500.0
    qstar = math.sqrt(r / D)
    scalar_relative = D * q0 + r / q0 if q0 < qstar else 2.0 * math.sqrt(D * r)
    mean_v = float(front_v.mean())
    mean_density_drift = float(D * front_dlogrho.mean())
    secant_speed = float((front[-1] - front[0]) / (t[-1] - t[0]))
    mean_v_integrated = float(np.trapezoid(front_v, t) / (t[-1] - t[0]))
    mean_dlogrho_integrated = float(np.trapezoid(front_dlogrho, t) / (t[-1] - t[0]))
    mean_material_relative_speed = secant_speed - mean_v_integrated
    curvature_term = -D * front_phi_xx / front_phi_x
    density_term = -D * front_dlogrho
    delta_k_front = (rho_b - front_rho) / (tau * rho_b) - (rho_a - front_rho) / (tau * rho_a)
    reaction_rate_front = 0.25 * (delta_k_front + alpha * delta_e)
    reaction_term = -reaction_rate_front / front_phi_x
    level_identity_speed = front_v + curvature_term + density_term + reaction_term
    observed_instantaneous = front_dot
    closure_error = observed_instantaneous - level_identity_speed
    stats: dict = {
        "nx": run_result["nx"],
        "nt": run_result["nt"],
        "dx_um": run_result["dx_um"],
        "dt_hr": run_result["dt_hr"],
        "a_phi": run_result["a_phi"],
        "a_rho": run_result["a_rho"],
        "alpha": run_result["alpha"],
        "eta_scale": run_result["eta_scale"],
        "fast_solve": run_result["fast_solve"],
        "phi_half_start_um": float(front[0]),
        "phi_half_end_um": float(front[-1]),
        "phi_half_ols_0_to_8_um_per_hr": slope,
        "phi_half_secant_0_to_8_um_per_hr": secant_speed,
        "mean_V_at_phi_half_um_per_hr": mean_v,
        "mean_V_at_phi_half_trapezoid_um_per_hr": mean_v_integrated,
        "mean_D_dlogrho_dx_at_phi_half_um_per_hr": mean_density_drift,
        "mean_material_relative_front_speed_0_to_8_um_per_hr": mean_material_relative_speed,
        "level_set_identity_terms_mean_um_per_hr": {
            "tissue_velocity_v": float(front_v.mean()),
            "profile_curvature_minus_D_phi_xx_over_phi_x": float(curvature_term.mean()),
            "density_gradient_minus_D_dlogrho_dx": float(density_term.mean()),
            "local_reaction_minus_R_over_phi_x": float(reaction_term.mean()),
            "sum": float(level_identity_speed.mean()),
            "finite_difference_front_velocity_mean": float(observed_instantaneous.mean()),
            "closure_rmse_vs_front_derivative": float(np.sqrt(np.mean(closure_error**2))),
            "closure_max_abs_vs_front_derivative": float(np.max(np.abs(closure_error))),
        },
        "scalar_leading_edge_q_per_um": q0,
        "scalar_leading_edge_q_over_qstar": q0 / qstar,
        "scalar_leading_edge_qstar_per_um": qstar,
        "scalar_KPP_branch_comparator_relative_speed_um_per_hr": scalar_relative,
        "scalar_KPP_comparator_total_with_sampled_drift_um_per_hr": scalar_relative + mean_v_integrated - D * mean_dlogrho_integrated,
        "full_solver_minus_scalar_total_speed_um_per_hr": secant_speed - (scalar_relative + mean_v_integrated - D * mean_dlogrho_integrated),
        "matched_time_window_speeds_um_per_hr": {},
        "phi_half_front_positions_um": front.tolist(),
        "all_finite": bool(
            np.isfinite(run_result["rho"]).all()
            and np.isfinite(run_result["phi"]).all()
            and np.isfinite(run_result["velocity"]).all()
        ),
        "rho_min": float(np.min(run_result["rho"])),
        "rho_max": float(np.max(run_result["rho"])),
        "phi_min": float(np.min(run_result["phi"])),
        "phi_max": float(np.max(run_result["phi"])),
        "parameters": run_result["parameters"],
    }
    for lo, hi in ((0.0, 2.0), (2.0, 4.0), (4.0, 6.0), (6.0, 8.0)):
        keep = (t >= lo) & (t <= hi)
        duration = hi - lo
        window_t = t[keep]
        window_front = front[keep]
        window_v = front_v[keep]
        window_dlogrho = front_dlogrho[keep]
        front_secant = float((window_front[-1] - window_front[0]) / duration)
        mean_window_v = float(np.trapezoid(window_v, window_t) / duration)
        mean_window_dlogrho = float(np.trapezoid(window_dlogrho, window_t) / duration)
        scalar_window = scalar_relative + mean_window_v - D * mean_window_dlogrho
        stats["matched_time_window_speeds_um_per_hr"][f"{lo:g}-{hi:g}"] = {
            "front_secant": front_secant,
            "front_ols": float(np.polyfit(window_t, window_front, 1)[0]),
            "mean_tissue_velocity": mean_window_v,
            "mean_material_relative_front": front_secant - mean_window_v,
            "mean_D_dlogrho_dx": D * mean_window_dlogrho,
            "scalar_KPP_plus_matched_drift": scalar_window,
            "full_minus_scalar_secant": front_secant - scalar_window,
        }
    if reference_dir is not None:
        ref_phi = np.loadtxt(reference_dir / "best_model_data_phi_1.csv", delimiter=",")
        ref_rho = np.loadtxt(reference_dir / "best_model_data_rho_1.csv", delimiter=",")
        ref_v = np.loadtxt(reference_dir / "best_model_data_V_1.csv", delimiter=",")
        stats["released_output_comparison"] = {
            "phi_max_abs_difference": float(np.max(np.abs(ref_phi - run_result["phi"]))),
            "phi_rmse": float(np.sqrt(np.mean((ref_phi - run_result["phi"]) ** 2))),
            "rho_max_abs_difference": float(np.max(np.abs(ref_rho - run_result["rho"]))),
            "rho_rmse": float(np.sqrt(np.mean((ref_rho - run_result["rho"]) ** 2))),
            "velocity_max_abs_difference": float(np.max(np.abs(ref_v - run_result["velocity"]))),
            "velocity_rmse": float(np.sqrt(np.mean((ref_v - run_result["velocity"]) ** 2))),
        }
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nx", type=int, default=200)
    parser.add_argument("--nt", type=int, default=100)
    parser.add_argument("--a-phi", type=float, default=4.0)
    parser.add_argument("--alpha", type=float, default=3.5e-6)
    parser.add_argument("--eta-scale", type=float, default=1.0)
    parser.add_argument("--a-rho", type=float, default=4.0)
    parser.add_argument("--fast-solve", action="store_true", help="use DST-I diagonalization of the same discrete force operator")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compare-released", action="store_true")
    args = parser.parse_args()
    sim = run(args.nx, args.nt, args.a_phi, args.alpha, args.eta_scale, args.a_rho, args.fast_solve)
    stats = summary(sim, HERE / "source_data" if args.compare_released else None)
    if args.output:
        args.output.write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
