#!/usr/bin/env python3
"""48-cell radial-resolution replay of the finite-memory witness."""
from __future__ import annotations

import contextlib
import json
from pathlib import Path
from time import perf_counter

import constitutive_witness as witness


def main():
    tic = perf_counter()
    p = witness.material.Parameters()
    from io import StringIO
    stream = StringIO()
    with contextlib.redirect_stdout(stream):
        case = witness.model_case("finite_memory", p, nz=11, nr=48)
    keys = (
        "converged_mode_iteration", "frequency_hz", "omega", "flow_L_min",
        "axial_pressure_drop_Pa", "baseline_electric_W", "axial_fluid_power_W",
        "cross_fluid_power_W", "structural_loss_W", "actuator_copper_loss_W",
        "drive_mechanical_power_W", "total_electric_before_idle_W", "electric_ratio",
        "maximum_material_strain", "maximum_chi", "any_OSP_chi_extrapolation",
        "final_shape_self_consistency_error", "support_spacing_m",
        "assumed_structural_quality", "assumed_support_rotational_stiffness_Nm_rad",
        "actuator_peak_force_N", "actuator_rms_current_A", "actuator_stroke_amplitude_m",
    )
    out = {
        "status": "internally reconstructed finite-memory witness at inherited radial resolution; not material validation",
        "grid": {"axial_nodes": 11, "radial_cells": 48, "support_spacing_m": case["support_spacing_m"]},
        "case": {k: case.get(k) for k in keys},
        "solver_log": stream.getvalue(),
        "elapsed_s": perf_counter() - tic,
    }
    dest = Path(__file__).with_name("witness_memory_11x48.json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "solver_log"}, indent=2))


if __name__ == "__main__":
    main()
