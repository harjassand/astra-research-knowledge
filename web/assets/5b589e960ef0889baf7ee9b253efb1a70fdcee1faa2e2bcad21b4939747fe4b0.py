#!/usr/bin/env python3
"""Reproduce source-specific scalar-reduction and shift-estimator checks.

Run from workspace root with Python 3 + NumPy. This is a finite diagnostic,
not a proof about the full biological PDE.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from replay_model import level_position, run_full

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "work/agents/c8_morphogenesis_control/cycle9/deeper_attack/source_data"
OUT = ROOT / "work/agents/c9_skull_wave_hostile/results"


def read_matrix(path: Path) -> np.ndarray:
    with path.open(newline="") as f:
        return np.asarray([[float(v) for v in row] for row in csv.reader(f)])


def x_at_level(x: np.ndarray, y: np.ndarray, level: float = 0.5) -> float:
    hits = np.flatnonzero((y[:-1] >= level) & (y[1:] <= level))
    if not hits.size:
        return float("nan")
    i = int(hits[0])
    return float(x[i] + (level - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i]))


def scalar_fkpp(D: float, r: float, q: float, *, L: float = 1500.0,
                dx: float = 1.0, dt: float = 0.002, tmax: float = 8.0) -> dict:
    """Explicit FD of u_t=D u_xx+r u(1-u), initialized with logistic tail e^-qx."""
    x = np.arange(-L, L + 0.5 * dx, dx)
    # Algebraically identical to the released tanh seed when q=2/375.
    z = np.clip(q * x, -700.0, 700.0)
    u = 1.0 / (1.0 + np.exp(z))
    left, right = float(u[0]), float(u[-1])
    steps = round(tmax / dt)
    sample_every = round(0.2 / dt)
    records = []
    for k in range(steps + 1):
        if k % sample_every == 0 or k == steps:
            records.append((k * dt, x_at_level(x, u)))
        if k == steps:
            break
        lap = (u[2:] - 2.0 * u[1:-1] + u[:-2]) / dx**2
        u[1:-1] += dt * (D * lap + r * u[1:-1] * (1.0 - u[1:-1]))
        u[0], u[-1] = left, right
    arr = np.asarray(records)
    slope = float(np.polyfit(arr[:, 0], arr[:, 1], 1)[0])
    return {
        "q_um_inv": q,
        "lambda_star_um_inv": math.sqrt(r / D),
        "q_is_shallow": q < math.sqrt(r / D),
        "c_min_steep_kpp_um_per_h": 2.0 * math.sqrt(D * r),
        "linear_dispersion_Dq_plus_r_over_q_um_per_h": D * q + r / q,
        "finite_0_to_8h_level_ols_um_per_h": slope,
        "positions": records,
    }


def shift_objective() -> dict:
    """Compare the notebook's signed-sum objective with an L1 profile norm."""
    # Repository matrices are rows=time, columns=space; Mathematica uses the
    # transposed orientation. Notebook T1=20, delta_t=30, T=100, Nx=200.
    # Public Mathematica matrix is x-by-time; use time-by-x for indexing.
    phi = read_matrix(SOURCE / "best_model_data_phi_1.csv").T
    times_one_based = (20, 50)
    delta_index = 30
    candidates = []
    for shift in range(16):
        signed_abs_by_window = []
        l1_by_window = []
        for t1 in times_one_based:
            ti = t1 - 1
            n = 200 - shift  # notebook Sum[{x,1,Nx-shift}], inclusive
            diff = phi[ti, :n] - phi[ti + delta_index, shift:shift + n]
            signed_abs_by_window.append(float(abs(np.sum(diff))))
            l1_by_window.append(float(np.sum(np.abs(diff))))
        candidates.append({
            "shift_grid_cells": shift,
            "velocity_grid_units_per_output_step": shift / 30.0,
            "notebook_mean_abs_signed_sum": float(np.mean(signed_abs_by_window)),
            "l1_mean_pointwise_abs_sum": float(np.mean(l1_by_window)),
            "notebook_per_window": signed_abs_by_window,
            "l1_per_window": l1_by_window,
        })
    best_signed = min(candidates, key=lambda z: z["notebook_mean_abs_signed_sum"])
    best_l1 = min(candidates, key=lambda z: z["l1_mean_pointwise_abs_sum"])
    # Explicit counterexample: equal spatial sums, different profiles.
    p = np.asarray([1.0, 0.0])
    q = np.asarray([0.5, 0.5])
    toy = {
        "abs_signed_sum": float(abs(np.sum(p - q))),
        "pointwise_l1": float(np.sum(np.abs(p - q))),
    }
    return {
        "notebook_source_settings": {
            "T1_one_based": 20,
            "delta_t_output_indices": 30,
            "T": 100,
            "Nx": 200,
            "window_indices_one_based": [[20, 50], [50, 80]],
            "candidate_shift_cells": [0, 15],
        },
        "best_notebook_objective": best_signed,
        "best_l1_objective": best_l1,
        "selected_grid_point_unchanged_here": best_signed["shift_grid_cells"] == best_l1["shift_grid_cells"],
        "source_reported_delta_phi_inferred": 0.03728287449886646,
        "notebook_delta_t_physical_h": 30 * 0.08,
        "space_step_um": 15.0,
        "physical_velocity_grid_spacing_um_per_h": 15.0 / (30 * 0.08),
        "toy_equal_integral_profiles": toy,
        "all_candidates": candidates,
    }


def full_transport_diagnostic() -> dict:
    """Measure the released-code level speed and local drift from replay fields."""
    z = run_full()
    x, ph, rho, vel = z["x"], z["phi"], z["rho"], z["v"]
    time = np.arange(ph.shape[0]) * z["dt"]
    pos = np.asarray([level_position(x, row) for row in ph])
    front_v, density_drift = [], []
    log_density_gradient = np.gradient(rho, x, axis=1, edge_order=2) / rho
    for j, p in enumerate(pos):
        i = int(np.clip(np.searchsorted(x, p), 1, len(x) - 1))
        a = (p - x[i - 1]) / (x[i] - x[i - 1])
        front_v.append(float((1 - a) * vel[j, i - 1] + a * vel[j, i]))
        density_drift.append(float(z["D"] * np.interp(p, x, log_density_gradient[j])))
    front_v = np.asarray(front_v)
    density_drift = np.asarray(density_drift)
    use = (time >= 0.0) & (time <= 8.0)
    level_speed = float(np.polyfit(time[use], pos[use], 1)[0])
    mean_v = float(np.mean(front_v[use]))
    mean_density = float(np.mean(density_drift[use]))
    return {
        "phi_half_ols_0_to_8_um_per_h": level_speed,
        "mean_local_tissue_velocity_at_phi_half_0_to_8_um_per_h": mean_v,
        "mean_D_d_x_log_rho_at_phi_half_0_to_8_um_per_h": mean_density,
        "descriptive_adjusted_scalar_comparator_um_per_h": level_speed - mean_v + mean_density,
    }


def main() -> None:
    D = 15.0
    rho_a, rho_b, tau = 0.0067, 0.0077, 10.0
    delta_k = (rho_b - rho_a) / (tau * rho_b)
    E_a_pa, E_b_pa = 30.0, 1000.0
    pa_to_model = 12.96
    gap_e_model = (E_b_pa - E_a_pa) * pa_to_model
    alpha = 3.5e-6
    alpha_delta_e_model = alpha * gap_e_model
    alpha_delta_e_if_per_pa_hr = alpha * (E_b_pa - E_a_pa)
    r_code = delta_k + alpha_delta_e_model
    r_si_if_table_alpha_per_pa_hr = delta_k + alpha_delta_e_if_per_pa_hr
    q_seed = 2.0 * 4.0 / 1500.0
    full_diag = full_transport_diagnostic()
    adjusted_c = full_diag["descriptive_adjusted_scalar_comparator_um_per_h"]
    same_speed_pairs = []
    for q in (q_seed, 0.01, 0.02):
        alpha_q = (q * (adjusted_c - D * q) - delta_k) / gap_e_model
        r_q = delta_k + alpha_q * gap_e_model
        same_speed_pairs.append({
            "q_um_inv": q,
            "alpha_notebook_units": alpha_q,
            "reconstructed_c_um_per_h": D * q + r_q / q,
            "q_over_q_star": q / math.sqrt(r_q / D),
        })
    result = {
        "units": {
            "D": "um^2/h",
            "k_and_r": "1/h",
            "E_table": "Pa",
            "E_notebook": "kg/(um h^2)",
            "Pa_to_notebook_stress_factor": pa_to_model,
            "alpha_required_from_kD=alpha*(E-EA)": "(stress*time)^-1",
            "alpha_table_numeric_units": "not stated in Table S1",
        },
        "leading_edge_rates": {
            "delta_k_at_rho_A_homeostasis_per_h": delta_k,
            "delta_E_table_Pa": E_b_pa - E_a_pa,
            "delta_E_notebook_units": gap_e_model,
            "alpha_times_deltaE_as_executable_notebook_uses_per_h": alpha_delta_e_model,
            "alpha_times_deltaE_if_table_alpha_is_per_Pa_per_h": alpha_delta_e_if_per_pa_hr,
            "r_executable_numeric_convention_per_h": r_code,
            "r_if_alpha_is_per_Pa_per_h_per_h": r_si_if_table_alpha_per_pa_hr,
        },
        "source_seed": {
            "profile": "phi0(x)=(1-tanh(4*x/1500))/2 = 1/(1+exp(8*x/1500))",
            "right_tail_exponent_um_inv": q_seed,
            "right_tail_length_um": 1.0 / q_seed,
        },
        "scalar_fkpp_reductions": {
            "released_notebook_numeric_alpha": {
                "r_per_h": r_code,
                "q_star_um_inv": math.sqrt(r_code / D),
                "c_min_steep_um_per_h": 2.0 * math.sqrt(D * r_code),
                "shallow_tail_linear_dispersion_um_per_h": D * q_seed + r_code / q_seed,
                "finite_simulation_broad_seed": scalar_fkpp(D, r_code, q_seed),
                "finite_simulation_steep_seed_q_0_1": scalar_fkpp(D, r_code, 0.1),
            },
            "if_table_alpha_is_per_Pa_per_h": {
                "r_per_h": r_si_if_table_alpha_per_pa_hr,
                "q_star_um_inv": math.sqrt(r_si_if_table_alpha_per_pa_hr / D),
                "c_min_steep_um_per_h": 2.0 * math.sqrt(D * r_si_if_table_alpha_per_pa_hr),
                "shallow_tail_linear_dispersion_um_per_h": D * q_seed + r_si_if_table_alpha_per_pa_hr / q_seed,
            },
        },
        "shift_estimator_audit": shift_objective(),
        "full_coupled_replay_transport_diagnostic": full_diag,
        "conditional_speed_only_alpha_nonidentifiability": {
            "target_adjusted_c_um_per_h": adjusted_c,
            "same_speed_q_alpha_pairs": same_speed_pairs,
        },
        "source_model_reduction_boundary": [
            "Scalar FKPP requires rho constant, v=0, constant coefficients, and homogeneous D.",
            "Full fraction PDE contains D*(d_xx phi + (d_x ln rho)*(d_x phi)) - v*d_x phi.",
            "A spatially varying v cannot generally be added to a scalar front speed as one constant v_A.",
            "The reduced logistic nonlinearity is KPP; the full coupled PDE is not thereby covered by scalar KPP speed selection.",
        ],
        "execution": {
            "python_numpy_only": True,
            "network_or_wetlab": False,
            "external_nature_claim": False,
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "reduced_front_audit.json"
    out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
