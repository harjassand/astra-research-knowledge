#!/usr/bin/env python3
"""Replay tail-selection diagnostics from the released SkullWave output CSVs.

This is an analysis of the authors' published model output, not a reimplementation
or rerun of their coupled PDE solver.  It uses only NumPy and the source CSVs
under source_data/.
"""

from __future__ import annotations

import argparse
import csv
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
DEFAULT_DATA = HERE / "source_data"


def load_matrix(path: Path) -> np.ndarray:
    data = np.loadtxt(path, delimiter=",")
    if data.ndim != 2 or not np.isfinite(data).all():
        raise ValueError(f"Expected a finite 2-D CSV matrix: {path}")
    return data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def interp_at_x(grid: np.ndarray, values: np.ndarray, x: float) -> float:
    return float(np.interp(x, grid, values))


def fit_speed(times: np.ndarray, front: np.ndarray, lower: float, upper: float) -> float:
    keep = (times >= lower) & (times <= upper)
    return float(np.polyfit(times[keep], front[keep], 1)[0])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, help="Optional path for JSON results")
    args = parser.parse_args()
    data_dir = args.data.resolve()

    names = {
        "phi": "best_model_data_phi_1.csv",
        "velocity": "best_model_data_V_1.csv",
        "density": "best_model_data_rho_1.csv",
        "notebook_velocity_estimate": "best_model_wave_velocity_est.csv",
        "parameters": "best_model_data_parameters.csv",
    }
    paths = {key: data_dir / name for key, name in names.items()}
    interface_path = data_dir / "data_ex_vivo_videos_1_to_4_all_interfaces.csv"
    velocity_means_path = data_dir / "Velocities_means.csv"
    phi = load_matrix(paths["phi"])
    velocity = load_matrix(paths["velocity"])
    density = load_matrix(paths["density"])
    if phi.shape != (201, 101) or velocity.shape != phi.shape or density.shape != phi.shape:
        raise ValueError(f"Unexpected array shapes: phi={phi.shape}, V={velocity.shape}, rho={density.shape}")

    # The companion Rmd maps rows to x=-L+2L(X-1)/Nx; the notebook uses
    # L=1500 um, Nx=200, T=100, tmax=8 h.
    L, Nx, tmax, Nt = 1500.0, 200, 8.0, 100
    x = np.linspace(-L, L, Nx + 1)
    times = np.linspace(0.0, tmax, Nt + 1)
    dx = float(x[1] - x[0])

    # Track the phi=1/2 level continuously in x at each released time point.
    front = np.empty(Nt + 1)
    front_velocity = np.empty(Nt + 1)
    front_density = np.empty(Nt + 1)
    for j in range(Nt + 1):
        profile = phi[:, j]
        crossings = np.flatnonzero((profile[:-1] >= 0.5) & (profile[1:] < 0.5))
        if len(crossings) != 1:
            raise ValueError(f"Expected one descending phi=1/2 crossing at output {j}; found {len(crossings)}")
        i = int(crossings[0])
        fraction = (0.5 - profile[i]) / (profile[i + 1] - profile[i])
        front[j] = x[i] + fraction * dx
        front_velocity[j] = velocity[i, j] + fraction * (velocity[i + 1, j] - velocity[i, j])
        front_density[j] = density[i, j] + fraction * (density[i + 1, j] - density[i, j])

    density_gradient = np.gradient(density, x, axis=0, edge_order=2)
    log_density_gradient = density_gradient / density
    grad_at_front = np.array([
        interp_at_x(x, log_density_gradient[:, j], front[j]) for j in range(Nt + 1)
    ])

    # Parameters copied from the published parameter CSV / notebook.  eO/eM
    # are the converted model units used with time in hours and x in microns.
    D = 15.0
    alpha = 3.5e-6
    eO, eM = 12960.0, 388.8
    rhoA, rhoB, tau = 0.0067, 0.0077, 10.0
    a_phi = 4.0
    delta_E = eO - eM
    delta_k_Ahead = (rhoB - rhoA) / (tau * rhoB)
    r = delta_k_Ahead + alpha * delta_E
    q0 = 2.0 * a_phi / L
    q_star = math.sqrt(r / D)

    # In the constant-leading-edge reduction, the composition equation is
    # phi_t = D phi_xx + r phi(1-phi), after removing uniform material drift.
    # Exponential initial tail q<sqrt(r/D) selects Dq+r/q; a steep tail selects
    # the pulled minimum 2sqrt(Dr). These are comparison baselines, not a theorem
    # for the source's fully coupled variable-density, variable-velocity PDE.
    c_shallow = D * q0 + r / q0
    c_pulled = 2.0 * math.sqrt(D * r)
    front_speed_ols = fit_speed(times, front, 0.0, tmax)
    front_speed_secant = float((front[-1] - front[0]) / (times[-1] - times[0]))
    mean_velocity_integrated = float(np.trapezoid(front_velocity, times) / (times[-1] - times[0]))
    mean_log_gradient_integrated = float(np.trapezoid(grad_at_front, times) / (times[-1] - times[0]))
    relative_speed_adjusted = front_speed_secant - mean_velocity_integrated + D * mean_log_gradient_integrated
    alpha_from_shallow_tail = (q0 * (relative_speed_adjusted - D * q0) - delta_k_Ahead) / delta_E
    alpha_from_pulled_law = (relative_speed_adjusted**2 / (4.0 * D) - delta_k_Ahead) / delta_E

    # Independent released experimental comparators: regress each explant's
    # front interface over the first six hours; use the authors' summarized
    # single-cell velocity means as a separate cell-motion readout.
    grouped_interfaces: dict[str, list[tuple[float, float]]] = {}
    with interface_path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            t = float(row["time"])
            if 0.0 <= t <= 6.0:
                grouped_interfaces.setdefault(row["data_set"], []).append(
                    (t, float(row["interface_height"]))
                )
    experimental_front_slopes = []
    for rows in grouped_interfaces.values():
        if len(rows) >= 3:
            t, h = np.asarray(rows, dtype=float).T
            experimental_front_slopes.append(float(np.polyfit(t, h, 1)[0]))
    if len(experimental_front_slopes) < 2:
        raise ValueError("Need at least two released ex-vivo interface time series")
    experimental_front_mean = float(np.mean(experimental_front_slopes))
    experimental_front_sd = float(np.std(experimental_front_slopes, ddof=1))
    cell_velocity_means = {}
    with velocity_means_path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            cell_velocity_means[row["Location"]] = {
                "mean_um_per_hr": float(row["V.mean.mean"]),
                "between_track_sd_um_per_hr": float(row["V.mean.sd"]),
            }

    # Reproduce the notebook's profile-shift diagnostic exactly.  Its source
    # uses Abs[Sum[phi_t-phi_shifted]], not Sum[Abs[...]], and the vp grid is
    # expressed as grid cells per output-time index.
    notebook_delta_steps = 30
    notebook_t1_indices = (20, 50)  # Mathematica's 1-based time-array indices
    notebook_profile_shift = []
    for shift_cells in range(16):  # vp = 0, 1/30, ..., 15/30
        signed_mass_error = []
        shape_l1_error = []
        for t1_mathematica in notebook_t1_indices:
            t0 = t1_mathematica - 1
            t1 = t1_mathematica + notebook_delta_steps - 1
            diff = phi[:Nx - shift_cells, t0] - phi[shift_cells:Nx, t1]
            signed_mass_error.append(abs(float(np.sum(diff))))
            shape_l1_error.append(float(np.sum(np.abs(diff))))
        notebook_profile_shift.append({
            "shift_cells": shift_cells,
            "v_grid_per_output_step": shift_cells / notebook_delta_steps,
            "mean_abs_signed_mass_error": float(np.mean(signed_mass_error)),
            "mean_L1_shape_error": float(np.mean(shape_l1_error)),
        })
    min_signed = min(notebook_profile_shift, key=lambda item: item["mean_abs_signed_mass_error"])
    min_shape = min(notebook_profile_shift, key=lambda item: item["mean_L1_shape_error"])
    physical_notebook_interval = notebook_delta_steps * (tmax / Nt)
    notebook_speed_step = dx / physical_notebook_interval
    source_notebook_velocity = min_signed["shift_cells"] * notebook_speed_step

    # Reproduce the published Rmd's different plotted-front estimator: strict
    # phi<0.5 row minimum, displacement relative to the first output, then an
    # origin-constrained OLS fit against its literal T.all expression.
    rmd_first_below_half = np.array([
        int(np.flatnonzero(phi[:, j] < 0.5)[0] + 1) for j in range(Nt + 1)
    ])
    rmd_displacement = (rmd_first_below_half - rmd_first_below_half[0]) * dx
    # In R, seq(0:nT) uses the one-argument length form and returns 1:101;
    # after subtracting one, this is the expected 0:100 time index.
    rmd_times_literal = np.arange(Nt + 1, dtype=float) / Nt * tmax
    rmd_origin_speed = float(np.dot(rmd_times_literal, rmd_displacement) / np.dot(rmd_times_literal, rmd_times_literal))
    rmd_ordinary_speed = float(np.polyfit(rmd_times_literal, rmd_displacement, 1)[0])

    alpha_aliases = []
    for q in (q0, 0.01, 0.02):
        r_alias = q * (relative_speed_adjusted - D * q)
        alpha_alias = (r_alias - delta_k_Ahead) / delta_E
        q_star_alias = math.sqrt(r_alias / D)
        c_alias = D * q + r_alias / q
        alpha_aliases.append({
            "q_per_um": q,
            "alpha_in_simulator_units": alpha_alias,
            "r_per_hr": r_alias,
            "qstar_per_um": q_star_alias,
            "is_shallow_tail": q < q_star_alias,
            "reconstructed_relative_speed_um_per_hr": c_alias,
        })
    if any(item["alpha_in_simulator_units"] <= 0 or not item["is_shallow_tail"] for item in alpha_aliases):
        raise AssertionError("The displayed alpha/q speed aliases must be positive shallow-tail cases")
    if not all(math.isclose(item["reconstructed_relative_speed_um_per_hr"], relative_speed_adjusted, rel_tol=1e-12) for item in alpha_aliases):
        raise AssertionError("The candidate (alpha,q) pairs failed to reconstruct the same speed")
    if min_signed["shift_cells"] != min_shape["shift_cells"]:
        raise AssertionError("The source-output L1 recheck no longer selects the same shift grid point")
    exported_velocity_field = next(
        (field for row in csv.reader(paths["notebook_velocity_estimate"].open(newline="", encoding="utf-8"))
         for field in row if field.startswith("{") and "18.75" in field),
        None,
    )
    if exported_velocity_field is None:
        raise ValueError("Could not locate the notebook's exported wave-velocity row")
    exported_velocity_tokens = exported_velocity_field.strip("{}").split(",")
    exported_notebook_velocity = float(exported_velocity_tokens[2])
    if not math.isclose(source_notebook_velocity, exported_notebook_velocity, rel_tol=0.0, abs_tol=1e-12):
        raise AssertionError("Replayed notebook speed does not match its exported estimate")

    result = {
        "status": "FINITE_REPLAY_OF_RELEASED_MODEL_OUTPUT_NOT_PDE_RERUN",
        "source_files": {
            key: {"name": paths[key].name, "sha256": sha256(paths[key])}
            for key in paths
        } | {
            "ex_vivo_interfaces": {"name": interface_path.name, "sha256": sha256(interface_path)},
            "ex_vivo_cell_velocity_summary": {"name": velocity_means_path.name, "sha256": sha256(velocity_means_path)},
        },
        "axes_and_resolution": {
            "source_mapping": "x=-L+2L(X-1)/Nx from plot_results_with_data.Rmd",
            "x_min_um": -L,
            "x_max_um": L,
            "Nx": Nx,
            "dx_um": dx,
            "time_min_hr": 0.0,
            "time_max_hr": tmax,
            "Nt": Nt,
            "dt_output_hr": tmax / Nt,
        },
        "released_phi_half_level": {
            "x_start_um": float(front[0]),
            "x_end_um": float(front[-1]),
            "ols_speed_0_to_8_um_per_hr": front_speed_ols,
            "secant_speed_0_to_8_um_per_hr": front_speed_secant,
            "mean_V_trapezoid_at_phi_half_um_per_hr": mean_velocity_integrated,
            "mean_dlogrho_dx_trapezoid_at_phi_half_per_um": mean_log_gradient_integrated,
            "ols_speed_2_to_8_um_per_hr": fit_speed(times, front, 2.0, 8.0),
            "rmd_literal_strict_phi_lt_half_through_origin_speed_um_per_hr": rmd_origin_speed,
            "rmd_literal_strict_phi_lt_half_unconstrained_speed_um_per_hr": rmd_ordinary_speed,
            "rmd_literal_time_vector_start_hr": float(rmd_times_literal[0]),
            "rmd_literal_time_vector_end_hr": float(rmd_times_literal[-1]),
            "mean_V_sampled_at_phi_half_um_per_hr": float(front_velocity.mean()),
            "mean_D_dlogrho_dx_um_per_hr": D * float(grad_at_front.mean()),
            "relative_speed_after_local_drift_adjustment_um_per_hr": relative_speed_adjusted,
            "mean_density_at_phi_half": float(front_density.mean()),
            "released_ex_vivo_interface_slopes_0_to_6_um_per_hr_by_dataset": experimental_front_slopes,
            "released_ex_vivo_interface_slope_mean_um_per_hr": experimental_front_mean,
            "released_ex_vivo_interface_slope_sample_sd_um_per_hr": experimental_front_sd,
            "model_front_speed_minus_ex_vivo_mean_um_per_hr": front_speed_secant - experimental_front_mean,
            "model_front_speed_in_ex_vivo_mean_plusminus_1sd": abs(front_speed_secant - experimental_front_mean) <= experimental_front_sd,
            "released_ex_vivo_cell_velocity_summary_um_per_hr": cell_velocity_means,
        },
        "notebook_profile_shift_diagnostic": {
            "source_method": "Two profile pairs at Mathematica indices t1={20,50}, delta-index=30; candidate shifts 0..15 grid cells.",
            "source_metric_literal": "Abs[Sum(phi(x,t)-phi(x+shift,t+delta_t),x)] then mean over the two windows.",
            "source_metric_minimizer_shift_cells": min_signed["shift_cells"],
            "source_metric_minimum_mean_abs_signed_mass_error": min_signed["mean_abs_signed_mass_error"],
            "source_metric_implied_speed_um_per_hr": source_notebook_velocity,
            "notebook_exported_source_velocity_um_per_hr": exported_notebook_velocity,
            "difference_phi_half_ols_minus_notebook_profile_shift_um_per_hr": front_speed_ols - source_notebook_velocity,
            "difference_phi_half_secant_minus_notebook_profile_shift_um_per_hr": front_speed_secant - source_notebook_velocity,
            "difference_rmd_through_origin_minus_notebook_profile_shift_um_per_hr": rmd_origin_speed - source_notebook_velocity,
            "L1_shape_error_minimizer_shift_cells": min_shape["shift_cells"],
            "L1_shape_error_at_source_metric_minimizer": min_signed["mean_L1_shape_error"],
            "L1_shape_error_minimum": min_shape["mean_L1_shape_error"],
            "physical_time_between_profiles_hr": physical_notebook_interval,
            "coarse_speed_grid_step_um_per_hr": notebook_speed_step,
            "reported_notebook_deltavUnits": 0.5,
            "reported_deltavUnits_interpretation": "The notebook calculates dx_um/30 output indices = 0.5; converting the 30 indices to 2.4 physical hours gives a velocity grid step of 6.25 um/hr.",
            "candidate_shift_curve": notebook_profile_shift,
            "metric_warning": "The L1 minimizer happens to be the same grid point in this released output, but the notebook's reported error 0.03728 is not an L1 shape mismatch; L1 at that shift is 0.41495.",
        },
        "constant_leading_edge_reduction": {
            "D_um2_per_hr": D,
            "rho_A_c": rhoA,
            "rho_B_c": rhoB,
            "tau_hr": tau,
            "delta_k_at_A_homeostasis_per_hr": delta_k_Ahead,
            "alpha_in_simulator_model_units": alpha,
            "delta_E_model_units": delta_E,
            "alpha_delta_E_per_hr": alpha * delta_E,
            "r_per_hr": r,
            "initial_tail_q0_per_um": q0,
            "initial_tail_length_um": 1.0 / q0,
            "pulled_threshold_qstar_per_um": q_star,
            "pulled_threshold_length_um": 1.0 / q_star,
            "q0_over_qstar": q0 / q_star,
            "qstar_times_grid_dx": q_star * dx,
            "phi_at_plus_L_from_initial_tanh": 1.0 / (1.0 + math.exp(2.0 * a_phi)),
            "shallow_tail_speed_Dq_plus_r_over_q_um_per_hr": c_shallow,
            "pulled_minimum_speed_2sqrtDr_um_per_hr": c_pulled,
            "shallow_prediction_total_speed_using_mean_V_and_density_drift_um_per_hr": mean_velocity_integrated + c_shallow - D * mean_log_gradient_integrated,
            "relative_replay_minus_shallow_prediction_um_per_hr": relative_speed_adjusted - c_shallow,
            "alpha_inferred_if_shallow_tail_law_used": alpha_from_shallow_tail,
            "alpha_inferred_if_pulled_minimum_law_used": alpha_from_pulled_law,
            "pulled_alpha_inferred_over_source_alpha": alpha_from_pulled_law / alpha,
            "same_speed_alpha_q_counterexamples": alpha_aliases,
        },
        "scope": [
            "The output matrices are the authors' released best_model simulation results; this script does not rerun the Mathematica finite-difference solver.",
            "The notebook's separate profile-shift estimator uses only two windows and a coarse discrete speed grid; its signed-sum objective can cancel spatial shape errors.",
            "The Fisher tail-selection expressions assume constant D, constant leading-edge growth, a scalar KPP reaction, and uniform material advection; the full source PDE couples density and velocity to phenotype.",
            "The computed phi=1/2 line and V/rho samples are properties of the released finite simulation, not a direct estimate of in-vivo wave speed or a proof that nature is pulled or pushed.",
            "The source's a_phi=4 initial tail is much shallower than q_star; q_star*dx is near one, so the released 15-um grid cannot resolve an intervention near the steep-tail threshold.",
        ],
        "internal_checks": {
            "all_three_alpha_q_pairs_positive_and_shallow": True,
            "all_three_pairs_reconstruct_same_relative_speed_to_1e-12": True,
            "notebook_and_L1_shift_argmins_match_for_this_output": True,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
