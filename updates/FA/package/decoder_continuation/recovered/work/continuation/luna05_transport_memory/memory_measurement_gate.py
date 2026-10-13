#!/usr/bin/env python3
"""Quantify frequency/memory discrimination and conditional actuator floor."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

SOURCE = Path(
    "/Users/harjas/Documents/Codex/2026-10-13/"
    "astra-genesis-civilization-enabling-breakthrough-discovery"
)
TRANSPORT = SOURCE / "work/phase5/transport_operation"
OUT = Path(__file__).resolve().parent


def tau_witness(gamma: float) -> float:
    x = max(gamma - 0.2, 0.0) / 0.05
    return 0.020 * x * x / (1 + x * x)


def beta(omega: float, tau: float) -> float:
    return 1 / (1 + (omega * tau) ** 2)


def main() -> None:
    source = json.loads((TRANSPORT / "standing_mode.json").read_text())
    case = next(c for c in source["cases"] if abs(c["wall_velocity_peak"] - 0.010) < 1e-12)
    gamma = sorted({float(r["primary_rate_wall"]) for r in case["local_rows"]})
    wpipe = float(case["omega"])
    tau_values = [tau_witness(g) for g in gamma]
    thresholds = {}
    for retained in (0.95, 0.50, 0.05, 0.01):
        # beta=retained means omega*tau=sqrt(1/beta-1).
        tau = math.sqrt(1 / retained - 1) / wpipe
        thresholds[str(retained)] = {"tau_s_at_pipe_omega": tau, "interpretation": f"{retained:.0%} of the instantaneous thinning retained"}

    bcase = {
        f"{g:.12g}": {
            "tau_s": tau_witness(g),
            "beta_at_pipe_omega": beta(wpipe, tau_witness(g)),
            "thinning_suppression_fraction": 1 - beta(wpipe, tau_witness(g)),
            "corner_frequency_hz": 1 / (2 * math.pi * tau_witness(g)) if tau_witness(g) > 0 else None,
        }
        for g in gamma
    }
    result = {
        "status": "formula-derived measurement thresholds and source-model loss ledger; not rheometry or hardware validation",
        "pipe": {"omega_rad_s": wpipe, "frequency_hz": float(case["frequency_hz"]), "strain_amplitude": float(case["maximum_material_strain"]), "local_primary_rates_s-1": gamma},
        "source_fig1c": {"measured_omega_rad_s": [0.314159, 94.2478], "upper_frequency_hz": 94.2478 / (2 * math.pi), "pipe_to_source_max_ratio": wpipe / 94.2478},
        "witness_memory_at_pipe": bcase,
        "attenuation_thresholds": thresholds,
        "measurement_gate": {
            "primary_rates_s-1": [0.2, min(gamma), 0.55, max(gamma)],
            "osp_strain_amplitude": [0.005, float(case["maximum_material_strain"]), 0.01],
            "angular_frequency_rad_s": [0.314159, 50.0, 94.2478, wpipe, 2000.0],
            "measure": ["primary viscosity", "orthogonal complex viscosity magnitude and phase", "startup/cessation and shear-reversal relaxation"],
            "reason": "The source response is at dotgamma0=0.2/s and omega<=94.25rad/s. The pipe needs omega≈453rad/s at local primary rates≈0.37–0.80/s. A log sweep through omega*tau≈1 brackets the witness's 18–20ms relaxation (about 8Hz) and tests the <0.51ms memory bound needed to retain 95% of thinning at the pipe mode.",
        },
        "inherited_actuation_ledger": {
            "source_case_total_electric_before_idle_W": float(case["total_electric_before_idle_W"]),
            "source_case_baseline_electric_W": float(case["baseline_electric_W"]),
            "cross_fluid_dissipation_W": float(case["cross_fluid_power_W"]),
            "structural_loss_W": float(case["structural_loss_W"]),
            "mechanical_drive_W": float(case["drive_mechanical_power_W"]),
            "coil_copper_loss_W": float(case["actuator_copper_loss_W"]),
            "modeled_actuation_draw_before_driver_idle_W": float(case["drive_mechanical_power_W"] + case["actuator_copper_loss_W"]),
            "no_axial_gain_same_flow_electric_lower_bound_W": float(case["baseline_electric_W"] + case["drive_mechanical_power_W"] + case["actuator_copper_loss_W"]),
            "scope": "Conditional on the inherited 72Hz mode, Q=20, wall motion, and H2W voice-coil assumptions. This is a lower bound before driver idle, seal/support losses, and unmodeled hardware; not universal across other architectures.",
        },
    }
    path = OUT / "memory_measurement_gate.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
