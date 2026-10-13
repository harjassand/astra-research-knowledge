#!/usr/bin/env python3
"""Matched-steady rheology witnesses for the inherited fixed-end pipe model.

Reads the pinned transport source tree without modifying it. Model A uses the
inherited cycle-averaged orthogonal-superposition closure. Model B uses the
same measured unactuated steady flow curve and the same active rheometry at
primary rate 0.2 s^-1, but attenuates active weakening with a one-pole passive
memory kernel at higher local primary rates. The chosen memory law is a
counterexample witness, not a fit to unacquired pipe rheology.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time

# The immutable source checkout has its own frozen NumPy/SciPy environment.
# This script must not create bytecode or result files inside that checkout.
sys.dont_write_bytecode = True

SOURCE = Path(
    "/Users/harjas/Documents/Codex/2026-10-13/"
    "astra-genesis-civilization-enabling-breakthrough-discovery"
)
TRANSPORT = SOURCE / "work/phase5/transport_operation"
sys.path.insert(0, str(TRANSPORT))

import numpy as np  # noqa: E402
from scipy.integrate import simpson  # noqa: E402

import nonlinear_transport as material  # noqa: E402
import standing_mode as fixed_end  # noqa: E402


CURRENT_OMEGA = 0.0
ORIGINAL_COUPLED = material.coupled
ORIGINAL_AXIAL_FROM_CROSS = material.axial_from_cross


def with_current_frequency(gradient, omega, velocity, p, *args, **kwargs):
    global CURRENT_OMEGA
    CURRENT_OMEGA = float(omega)
    return ORIGINAL_COUPLED(gradient, omega, velocity, p, *args, **kwargs)


def memory_time(gammadot: np.ndarray) -> np.ndarray:
    """A smooth high-shear structural mode, zero at the measured 0.2 s^-1.

    tau = 20 ms * x^2/(1+x^2), x=max(gammadot-0.2,0)/0.05.
    The threshold and time are deliberately exposed as unmeasured witness
    parameters.  The mode is consistent with the same steady curve because
    the weakening multiplier vanishes when there is no OSP.
    """
    x = np.maximum(np.asarray(gammadot) - 0.2, 0.0) / 0.05
    return 0.020 * x * x / (1.0 + x * x)


def filtered_axial_from_cross(shear, pressure_gradient, p):
    """Solve the same local axial force balance with a relaxation-filtered
    structural weakening.  The attenuation is the in-phase gain of a
    first-order mode, 1/(1+(omega*tau)^2), and lies in [0,1].
    """
    n = len(shear) - 1
    r = np.linspace(0.0, p.radius, n + 1)
    stress = pressure_gradient * r / 2.0
    cross = np.abs(shear)
    low = np.zeros_like(stress)
    high = np.maximum(stress * 200.0, 2000.0)
    for _ in range(56):
        h = 0.5 * (low + high)
        gamma = material.unactuated_rate(h, p)
        eta0 = np.divide(h, gamma, out=np.full_like(h, p.eta_high), where=gamma > 0)
        chi = np.divide(cross, gamma, out=np.zeros_like(cross), where=gamma > 0)
        measured = material.empirical.empirical_viscosity(chi, p, "primary")
        fraction = np.clip(
            (measured - p.hydrodynamic_parallel)
            / (p.eta_high - p.hydrodynamic_parallel),
            0.0,
            1.0,
        )
        eta_a = p.hydrodynamic_parallel + (eta0 - p.hydrodynamic_parallel) * fraction
        tau = memory_time(gamma)
        beta = 1.0 / (1.0 + (CURRENT_OMEGA * tau) ** 2)
        eta_eff = eta0 - beta * (eta0 - eta_a)
        below = gamma * eta_eff < stress
        low = np.where(below, h, low)
        high = np.where(below, high, h)

    h = 0.5 * (low + high)
    gamma = material.unactuated_rate(h, p)
    eta0 = np.divide(h, gamma, out=np.full_like(h, p.eta_high), where=gamma > 0)
    chi = np.divide(cross, gamma, out=np.zeros_like(cross), where=gamma > 0)
    measured = material.empirical.empirical_viscosity(chi, p, "primary")
    fraction = np.clip(
        (measured - p.hydrodynamic_parallel)
        / (p.eta_high - p.hydrodynamic_parallel),
        0.0,
        1.0,
    )
    eta_a = p.hydrodynamic_parallel + (eta0 - p.hydrodynamic_parallel) * fraction
    tau = memory_time(gamma)
    beta = 1.0 / (1.0 + (CURRENT_OMEGA * tau) ** 2)
    eta_parallel = eta0 - beta * (eta0 - eta_a)
    eta_cross = material.empirical.empirical_viscosity(chi, p, "OSP")
    mean = simpson(r * r * gamma, x=r) / (p.radius * p.radius)
    return mean, eta_parallel, eta_cross, gamma, chi, h


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def model_case(kind: str, p, nz=11, nr=24):
    material.coupled = with_current_frequency
    material.axial_from_cross = (
        ORIGINAL_AXIAL_FROM_CROSS if kind == "instantaneous" else filtered_axial_from_cross
    )
    # Same reported operating point and mechanical inputs.  The 11-node
    # layout preserves the inherited 2 m support spacing; the 24-cell radial
    # grid is half the source grid and keeps this a bounded witness replay.
    return fixed_end.solve_mode(
        0.00625,
        0.010,
        p,
        nz=nz,
        nr=nr,
        lever=0.5,
        quality=20.0,
        support_k=100.0,
        max_steps=8,
    )


def main():
    tic = time.perf_counter()
    p = material.Parameters()
    source_files = {
        "nonlinear_transport.py": TRANSPORT / "nonlinear_transport.py",
        "standing_mode.py": TRANSPORT / "standing_mode.py",
        "empirical_transport.py": TRANSPORT / "empirical_transport.py",
        "lin_fig6_digitised.csv": TRANSPORT / "sources/lin_fig6_digitised.csv",
        "fig1d_1.0_primary.csv": TRANSPORT / "sources/biaxial_raw/biaxial_repository/fig1d/fig1d_1.0_primary.csv",
        "fig1d_1.0_OSP.csv": TRANSPORT / "sources/biaxial_raw/biaxial_repository/fig1d/fig1d_1.0_OSP.csv",
        "fig1c_primary.csv": TRANSPORT / "sources/biaxial_raw/biaxial_repository/fig1c/fig1c_primary.csv",
        "fig1c_OSP.csv": TRANSPORT / "sources/biaxial_raw/biaxial_repository/fig1c/fig1c_OSP.csv",
        "fig3a_frequency.csv": TRANSPORT / "sources/biaxial_raw/biaxial_repository/fig3a/fig3a_frequency.csv",
        "fig3a_exp_matrix.csv": TRANSPORT / "sources/biaxial_raw/biaxial_repository/fig3a/fig3a_exp_matrix.csv",
        "fig3a_amplitude.csv": TRANSPORT / "sources/biaxial_raw/biaxial_repository/fig3a/fig3a_amplitude.csv",
        "standing_mode.json": TRANSPORT / "standing_mode.json",
    }
    input_hashes = {name: sha256(path) for name, path in source_files.items()}
    omega_raw, eta1c = np.loadtxt(source_files["fig1c_primary.csv"], delimiter=",").T
    omega_osp, eta1c_osp = np.loadtxt(source_files["fig1c_OSP.csv"], delimiter=",").T
    chi1d, eta1d = np.loadtxt(source_files["fig1d_1.0_primary.csv"], delimiter=",").T
    chi1d_osp, eta1d_osp = np.loadtxt(source_files["fig1d_1.0_OSP.csv"], delimiter=",").T
    fig3_frequency = np.loadtxt(source_files["fig3a_frequency.csv"], delimiter=",")
    fig3_amplitude = np.loadtxt(source_files["fig3a_amplitude.csv"], delimiter=",")
    fig3_matrix = np.loadtxt(source_files["fig3a_exp_matrix.csv"], delimiter=",")
    fig3_expected_from_omega = omega_raw * math.pi / (2 * 0.2)
    fig3_published_axis = omega_raw / (2 * math.pi * 0.2)
    fig3_relation_error = float(np.max(np.abs(fig3_frequency - fig3_expected_from_omega) / fig3_frequency))
    fig3_expected_error = float(np.max(np.abs(fig3_frequency - fig3_published_axis) / fig3_frequency))
    fig1d_formula_error = float(np.max(np.abs(chi1d - 0.01 * omega_raw / 0.2)))
    fig1c_pair_error = float(np.max(np.abs(omega_raw - omega_osp)))
    fig3_matrix_row2_error = float(np.max(np.abs(fig3_matrix[2] - eta1c)))
    source_json = json.loads(source_files["standing_mode.json"].read_text())
    source_case = next(c for c in source_json["cases"] if abs(c["wall_velocity_peak"] - 0.010) < 1e-12)

    grid = (11, 24)
    stdout = []
    cases = {}
    for kind in ("instantaneous", "finite_memory"):
        from io import StringIO

        stream = StringIO()
        with contextlib.redirect_stdout(stream):
            cases[kind] = model_case(kind, p, nz=grid[0], nr=grid[1])
        stdout.append({"model": kind, "solver_log": stream.getvalue()})

    # Keep the complete result deterministic except for elapsed time and
    # solver iteration logs; round only for a compact human-readable receipt.
    summary_keys = (
        "converged_mode_iteration", "frequency_hz", "omega", "flow_L_min",
        "axial_pressure_drop_Pa", "baseline_electric_W", "axial_fluid_power_W",
        "cross_fluid_power_W", "structural_loss_W", "actuator_copper_loss_W",
        "drive_mechanical_power_W", "total_electric_before_idle_W", "electric_ratio",
        "maximum_material_strain", "maximum_chi", "any_OSP_chi_extrapolation",
        "any_unactuated_extrapolation", "primary_rate_wall",
        "final_shape_self_consistency_error",
        "axial_nodes", "radial_cells", "support_spacing_m", "assumed_structural_quality",
        "assumed_support_rotational_stiffness_Nm_rad", "actuator_peak_force_N",
        "actuator_rms_current_A", "actuator_stroke_amplitude_m",
    )
    summaries = {
        name: {k: cases[name].get(k) for k in summary_keys}
        for name in cases
    }
    out = {
        "status": "internally reconstructed low-resolution constitutive counterexample; no rheology or device validation",
        "contract": {
            "steady_curve": "Both models use the same measured unactuated stress-rate curve from Lin et al. and exactly the same no-OSP constitutive law.",
            "source_active_match": "The finite-memory witness has tau(0.2 s^-1)=0 and therefore reproduces the inherited active law at the only primary shear rate used for Lin et al. OSP measurements; the rheometer frequency sweep is otherwise not refit.",
            "memory_witness": "tau(gamma)=0.020 s * x^2/(1+x^2), x=max(gamma-0.2,0)/0.05; beta=1/(1+(omega*tau)^2); eta_B=eta_0-beta*(eta_0-eta_A).",
            "passivity": "A causal thixotropic state q obeys tau*q_dot+q=gamma_OSP(t). For sinusoidal gamma_OSP=a*sin(omega*t), m=2*mean(q*gamma_OSP)/a^2=1/(1+(omega*tau)^2). Set eta_B=eta_0-m*(eta_0-eta_A); with eta_0>=eta_A>0 and 0<=m<=1, the cycle-averaged axial stress power is eta_B*gamma_dot_parallel^2>=0. Use a positive cross dashpot eta_perp>0 and zero stored structural free energy for q; then total mechanical dissipation is eta_B*gamma_dot_parallel^2+eta_perp*gamma_dot_OSP^2>=0. This is a passive cycle-averaged thixotropic closure, not a fitted particle-level law or a full transient fit.",
            "fixed_inputs": "Same geometry, source OSP curves, flow, steel, actuator, pump efficiency, support stiffness and fixed structural Q=20. The Q is inherited and held fixed; it is not fitted.",
            "resolution": f"{grid[0]} axial nodes and {grid[1]} radial cells; 2 m support spacing is preserved, but the radial grid is half the 48-cell source grid.",
        },
        "source_frequency_reconciliation": {
            "fig1c_physical_angular_frequency_rad_s": {"min": float(np.min(omega_raw)), "max": float(np.max(omega_raw)), "count": int(omega_raw.size)},
            "fig1d_amplitude_1pct_relative_osp_rate_chi": {"min": float(np.min(chi1d)), "max": float(np.max(chi1d)), "count": int(chi1d.size), "relation": "chi=0.01*omega/0.2"},
            "fig1c_primary_and_osp_share_omega_grid": bool(fig1c_pair_error == 0),
            "fig1d_axis_formula_max_abs_error": fig1d_formula_error,
            "fig3a_deposited_coordinate": {"min": float(np.min(fig3_frequency)), "max": float(np.max(fig3_frequency)), "count": int(fig3_frequency.size), "matrix_shape": list(fig3_matrix.shape), "amplitude_points": fig3_amplitude.tolist()},
            "fig3a_coordinate_relation": "deposited coordinate follows omega*pi/(2*0.2), not physical rad/s",
            "fig3a_relation_max_relative_error_from_omega_pi_over_2gamma": fig3_relation_error,
            "fig3a_publication_axis_label": "omega/(2*pi*dotgamma0), read visually from accepted Lin PDF p.4; SI p.8 labels the same coordinate ambiguously as gamma0*omega/(2*pi)",
            "fig3a_published_label_vs_deposited_coordinate_max_relative_error": fig3_expected_error,
            "fig3a_matrix_row_2_vs_fig1c_primary_max_abs_error_Pa_s": fig3_matrix_row2_error,
            "pipe_to_fig1c_physical_frequency_ratio": float(source_case["omega"] / np.max(omega_raw)),
            "interpretation": "Preserve the published-axis/deposited-coordinate pi^2 discrepancy; Fig3a is not a physical frequency sweep. The transport code uses Fig1d curves, not Fig3a."
        },
        "source_fixed_end_case_full_resolution": {k: source_case.get(k) for k in summary_keys},
        "reduced_grid_cases": summaries,
        "source_sha256": input_hashes,
        "stdout": stdout,
        "elapsed_s": time.perf_counter() - tic,
    }
    target = Path(__file__).with_name(f"witness_results_{grid[0]}x{grid[1]}.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "stdout"}, indent=2))


if __name__ == "__main__":
    main()
