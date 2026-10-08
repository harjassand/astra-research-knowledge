#!/usr/bin/env python3
"""Independent NumPy replay of the released SkullWave forward-difference run.

The only inputs are parameter/initial-condition/discretization definitions
transcribed from Tissue_model_simulator.nb.  No Mathematica kernel is needed.
Run from the workspace root:
    python3 work/agents/c9_skull_wave_hostile/code/replay_model.py
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "work/agents/c8_morphogenesis_control/cycle9/deeper_attack/source_data"
OUT = ROOT / "work/agents/c9_skull_wave_hostile/results"


def tridiagonal_solve(lower: float, diagonal: np.ndarray, upper: float,
                      rhs: np.ndarray) -> np.ndarray:
    """Thomas solve for constant off-diagonals and a general diagonal."""
    n = rhs.size
    c = np.empty(n - 1, dtype=float)
    d = np.empty(n, dtype=float)
    piv = diagonal[0]
    c[0] = upper / piv
    d[0] = rhs[0] / piv
    for i in range(1, n):
        piv = diagonal[i] - lower * c[i - 1]
        if i < n - 1:
            c[i] = upper / piv
        d[i] = (rhs[i] - lower * d[i - 1]) / piv
    x = np.empty(n, dtype=float)
    x[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def source_matrix(path: Path) -> np.ndarray:
    return np.asarray([[float(z) for z in row] for row in csv.reader(path.open())])


def run_full(eta_pa_s: float = 1.0e3, alpha_input: float = 3.5e-6,
             nx: int = 200, tmax: float = 8.0, nt: int = 100,
             alpha_stress_scale: float = 1.0,
             profile_width: float = 375.0) -> dict:
    # SI Table S1 uses 10^4 Pa s; the published Notebook's `params` cell
    # instead uses 10^3 Pa s.  alpha_stress_scale=1 reproduces that Notebook:
    # its alpha is multiplied by E in kg/(um h^2), without division by 12.96.
    L = 1500.0
    dx = 2.0 * L / nx
    dt = tmax / nt
    x = np.linspace(-L, L, nx + 1)
    rhoA, rhoB = 0.0067, 0.0077
    rhoh = 0.001
    tau = 10.0
    D = 15.0
    pa_to_new = 1.0 / (1.0e6 * (1.0 / 3600.0) ** 2)  # 12.96
    sec_to_hr = 1.0 / 3600.0
    EA = 30.0 * pa_to_new
    EB = 1000.0 * pa_to_new
    gapE = EB - EA
    eta = eta_pa_s * pa_to_new * sec_to_hr
    gamma = 0.8e3 * pa_to_new * sec_to_hr  # source parameter cell

    rho = rhoB - 0.0005 * (1.0 + np.tanh(x / profile_width))
    phi = 0.5 * (1.0 - np.tanh(x / profile_width))
    rho_left, rho_right = float(rho[0]), float(rho[-1])
    phi_left, phi_right = float(phi[0]), float(phi[-1])
    rho[0], rho[-1] = rho_left, rho_right
    phi[0], phi[-1] = phi_left, phi_right

    nint = nx - 1
    off = eta / dx**2
    diag = np.full(nint, -2.0 * off - gamma)
    vel_hist = np.zeros((nt + 1, nx + 1), dtype=float)
    rho_hist = np.empty((nt + 1, nx + 1), dtype=float)
    phi_hist = np.empty((nt + 1, nx + 1), dtype=float)
    rho_hist[0], phi_hist[0] = rho, phi

    for m in range(nt):
        drho = (rho[2:] - rho[:-2]) / (2.0 * dx)
        dphi = (phi[2:] - phi[:-2]) / (2.0 * dx)
        E = EA + gapE * phi[1:-1]
        force_per_rho = E * drho / rho[1:-1] + np.log(rho[1:-1] / rhoh) * gapE * dphi
        v_interior = tridiagonal_solve(off, diag, off, force_per_rho)
        v = np.zeros(nx + 1)
        v[1:-1] = v_interior

        # Exactly the expanded product rule in the Notebook's centered
        # discretization of rho_t + rho v_x + v rho_x.
        dv = (v[2:] - v[:-2]) / (2.0 * dx)
        growth_A = (rhoA - rho[1:-1]) / (rhoA * tau)
        growth_B = (rhoB - rho[1:-1]) / (rhoB * tau)
        growth = growth_A * (1.0 - phi[1:-1]) + growth_B * phi[1:-1]
        rho_rhs = -rho[1:-1] * dv - v[1:-1] * drho + growth * rho[1:-1]

        d2phi = (phi[2:] - 2.0 * phi[1:-1] + phi[:-2]) / dx**2
        f_diff = D * (drho / rho[1:-1] * dphi + d2phi)
        adv = -v[1:-1] * dphi
        delta_k = growth_B - growth_A
        stiff = alpha_input * alpha_stress_scale * gapE
        reaction = (delta_k + stiff) * phi[1:-1] * (1.0 - phi[1:-1])
        phi_rhs = adv + f_diff + reaction

        rho_next = rho.copy()
        phi_next = phi.copy()
        rho_next[1:-1] += dt * rho_rhs
        phi_next[1:-1] += dt * phi_rhs
        rho_next[0], rho_next[-1] = rho_left, rho_right
        phi_next[0], phi_next[-1] = phi_left, phi_right
        if not np.all(np.isfinite(rho_next)) or not np.all(np.isfinite(phi_next)):
            raise FloatingPointError(f"nonfinite at time step {m}")
        rho, phi = rho_next, phi_next
        vel_hist[m] = v
        rho_hist[m + 1], phi_hist[m + 1] = rho, phi
    # The final velocity is evaluated from the final rho/phi, matching the
    # source loop's final Solve-for-V iteration.
    drho = (rho[2:] - rho[:-2]) / (2.0 * dx)
    dphi = (phi[2:] - phi[:-2]) / (2.0 * dx)
    E = EA + gapE * phi[1:-1]
    force_per_rho = E * drho / rho[1:-1] + np.log(rho[1:-1] / rhoh) * gapE * dphi
    vel_hist[-1, 1:-1] = tridiagonal_solve(off, diag, off, force_per_rho)

    return {"x": x, "rho": rho_hist, "phi": phi_hist, "v": vel_hist,
            "dx": dx, "dt": dt, "D": D, "EA": EA, "EB": EB,
            "alpha_input": alpha_input, "eta_pa_s": eta_pa_s,
            "eta_internal": eta, "gamma_internal": gamma,
            "stress_scale": alpha_stress_scale,
            "profile_width": profile_width}


def compare_full(run: dict) -> dict:
    comparisons = {}
    for field in ("rho", "phi", "v"):
        saved = source_matrix(SOURCE / f"best_model_data_{field}_1.csv")
        ours = run[field]
        # Saved rows are time x position, while the Mathematica arrays are
        # position x time.  Published matrices contain 101 time rows.
        if saved.shape == ours.shape[::-1]:
            saved = saved.T
        if saved.shape != ours.shape:
            comparisons[field] = {"shape_saved": saved.shape,
                                  "shape_replay": ours.shape}
            continue
        d = np.abs(saved - ours)
        comparisons[field] = {"max_abs": float(np.max(d)),
                              "mean_abs": float(np.mean(d)),
                              "at": [int(i) for i in np.unravel_index(np.argmax(d), d.shape)]}
    return comparisons


def level_position(x: np.ndarray, y: np.ndarray, level: float = 0.5) -> float:
    # First crossing from > level to <= level, linearly interpolated.
    idx = np.where((y[:-1] >= level) & (y[1:] <= level))[0]
    if idx.size == 0:
        return float("nan")
    i = int(idx[0])
    return float(x[i] + (level - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i]))


def scalar_kpp(D: float, r: float, width: float = 375.0,
               L: float = 1500.0, dx: float = 1.0, dt: float = 0.002,
               tmax: float = 8.0) -> dict:
    """Explicit finite-difference scalar FKPP on the released tanh initial state."""
    x = np.arange(-L, L + 0.5 * dx, dx)
    phi = 0.5 * (1.0 - np.tanh(x / width))
    phi[0], phi[-1] = 0.5 * (1.0 - math.tanh(-L / width)), 0.5 * (1.0 - math.tanh(L / width))
    left, right = phi[0], phi[-1]
    n = round(tmax / dt)
    record = []
    for m in range(n + 1):
        if m % max(1, round(0.2 / dt)) == 0 or m == n:
            record.append((m * dt, level_position(x, phi)))
        if m == n:
            break
        d2 = (phi[2:] - 2.0 * phi[1:-1] + phi[:-2]) / dx**2
        rhs = D * d2 + r * phi[1:-1] * (1.0 - phi[1:-1])
        phi[1:-1] += dt * rhs
        phi[0], phi[-1] = left, right
    return {"D": D, "r": r, "width": width, "lambda_tail": 2.0 / width,
            "lambda_star": math.sqrt(r / D),
            "c_min_steep_KPP": 2.0 * math.sqrt(D * r),
            "c_tail_linear_dispersion": D * (2.0 / width) + r / (2.0 / width),
            "positions": record}


def main() -> None:
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    replay = run_full()
    obs = compare_full(replay)
    # An exactly reduced scalar PDE is a deliberate counterexample to using
    # the minimum KPP speed as the realized front speed for arbitrary starts.
    r = replay["alpha_input"] * (replay["EB"] - replay["EA"])
    scalar = scalar_kpp(D=replay["D"], r=r)
    # Parameter sensitivity is a diagnostic, not an alternative fit.  The
    # physical-pressure interpretation of alpha would require alpha/12.96
    # after E is converted to kg/(um h^2).  The table also prints eta=10^4 Pa s
    # while the executable parameter cell uses 10^3 Pa s.
    def model_metrics(z: dict) -> dict:
        positions = np.array([level_position(z["x"], row) for row in z["phi"]])
        times = np.arange(positions.size) * z["dt"]
        use = (times >= 0.0) & (times <= 6.0)
        slope = float(np.polyfit(times[use], positions[use], 1)[0])
        front_v = []
        for j, pos in enumerate(positions):
            idx = int(np.clip(np.searchsorted(z["x"], pos), 1, len(z["x"]) - 1))
            frac = (pos - z["x"][idx - 1]) / (z["x"][idx] - z["x"][idx - 1])
            front_v.append(float((1 - frac) * z["v"][j, idx - 1] + frac * z["v"][j, idx]))
        return {"x_half_6h_um": float(positions[75]),
                "x_half_8h_um": float(positions[-1]),
                "OLS_front_speed_0_6_um_per_h": slope,
                "v_at_x0_t0_um_per_h": float(z["v"][0, 100]),
                "v_at_x0_t6_um_per_h": float(z["v"][75, 100]),
                "v_at_phi_half_t0_um_per_h": front_v[0],
                "v_at_phi_half_t6_um_per_h": front_v[75]}

    scenarios = {}
    for name, kwargs in {
        "released_notebook": {},
        "table_eta_1e4": {"eta_pa_s": 1.0e4},
        "alpha_converted_if_table_alpha_is_per_Pa_per_h": {
            "alpha_stress_scale": 1.0 / 12.96},
        "both_table_eta_and_physical_alpha_conversion": {
            "eta_pa_s": 1.0e4, "alpha_stress_scale": 1.0 / 12.96},
    }.items():
        z = run_full(**kwargs)
        scenarios[name] = {"parameters": {k: z[k] for k in (
            "eta_pa_s", "eta_internal", "alpha_input", "stress_scale",
            "profile_width")}, "metrics": model_metrics(z)}
    # The released full-model profile translation number is parsed from its
    # published parameter CSV (input data, not re-fit here).
    summary = {
        "runtime": {"numpy": np.__version__, "scipy": "not used", "wall_time_s": None},
        "replay": {"parameters": {k: v for k, v in replay.items()
                                   if k not in ("x", "rho", "phi", "v")},
                   "comparison_to_saved_source_arrays": obs,
                   "metrics": model_metrics(replay),
                   "phi_half_positions_um": [level_position(replay["x"], row)
                                              for row in replay["phi"]]},
        "sensitivity_scenarios": scenarios,
        "scalar_kpp_counterexample": scalar,
        "source_model_transcription": {
            "parameters": "Notebook final executable parameter cell, In[513], source lines ~150-202",
            "full_pde": "PDEsys output Out[520], including expanded force balance",
            "scheme": "pdeDiscretized1 centered spatial differences + forward time, In[534], loop In[575]",
            "mesh": "L=1500, Nx=200, tmax=8, T=100; saved evaluation reports dx=15, dt=.08"
        }
    }
    summary["runtime"]["wall_time_s"] = time.perf_counter() - started
    (OUT / "replay_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps(summary, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
