#!/usr/bin/env python3
"""Reconcile the deposited Lin rheology arrays with the printed axes."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

SOURCE = Path(
    "/Users/harjas/Documents/Codex/2026-10-13/"
    "astra-genesis-civilization-enabling-breakthrough-discovery"
)
DATA = SOURCE / "work/phase5/transport_operation/sources/biaxial_raw/biaxial_repository"


def read(rel: str) -> np.ndarray:
    return np.loadtxt(DATA / rel, delimiter=",")


def main() -> None:
    c_primary = read("fig1c/fig1c_primary.csv")
    c_osp = read("fig1c/fig1c_OSP.csv")
    d_primary = read("fig1d/fig1d_1.0_primary.csv")
    d_osp = read("fig1d/fig1d_1.0_OSP.csv")
    f3 = read("fig3a/fig3a_frequency.csv")
    amp3 = read("fig3a/fig3a_amplitude.csv")
    mat3 = read("fig3a/fig3a_exp_matrix.csv")

    omega = c_primary[:, 0]
    chi = d_primary[:, 0]
    expected_chi = 0.01 * omega / 0.2
    f3_from_raw = omega * math.pi / (2 * 0.2)
    f3_from_printed_axis = omega / (2 * math.pi * 0.2)

    result = {
        "fig1c_primary": {
            "rows": int(c_primary.shape[0]),
            "columns": ["physical angular frequency omega (rad/s)", "primary viscosity eta_parallel (Pa s)"],
            "omega_range_rad_s": [float(omega.min()), float(omega.max())],
        },
        "fig1c_osp": {
            "rows": int(c_osp.shape[0]),
            "columns": ["physical angular frequency omega (rad/s)", "orthogonal complex-viscosity magnitude (Pa s)"],
            "omega_range_rad_s": [float(c_osp[:, 0].min()), float(c_osp[:, 0].max())],
            "same_omega_grid_as_primary": bool(np.array_equal(c_primary[:, 0], c_osp[:, 0])),
        },
        "fig1d_amplitude_1pct": {
            "primary_rows_columns": list(map(int, d_primary.shape)),
            "osp_rows_columns": list(map(int, d_osp.shape)),
            "x_is_relative_osp_rate_chi": True,
            "chi_range": [float(chi.min()), float(chi.max())],
            "chi_equals_0p01_omega_over_0p2_max_abs_error": float(np.max(np.abs(chi - expected_chi))),
            "primary_viscosity_equals_fig1c_max_abs_error_Pa_s": float(np.max(np.abs(d_primary[:, 1] - c_primary[:, 1]))),
            "osp_viscosity_equals_fig1c_max_abs_error_Pa_s": float(np.max(np.abs(d_osp[:, 1] - c_osp[:, 1]))),
        },
        "fig3a_deposited": {
            "frequency_count": int(f3.size),
            "frequency_coordinate_range": [float(f3.min()), float(f3.max())],
            "amplitude_values": amp3.tolist(),
            "experimental_matrix_rows_columns": list(map(int, mat3.shape)),
            "matrix_row_2_equals_fig1c_primary_max_abs_error_Pa_s": float(np.max(np.abs(mat3[2] - c_primary[:, 1]))),
            "coordinate_relation_to_fig1c_omega": "omega*pi/(2*0.2)",
            "relation_max_relative_error": float(np.max(np.abs(f3 - f3_from_raw) / f3)),
            "printed_fig3_axis_from_accepted_pdf_p4": "omega/(2*pi*dotgamma0)",
            "SI_fig7_axis_text_p8": "gamma0*omega/(2*pi) (dot over primary gamma is visually/typographically ambiguous in the PDF extraction)",
            "printed_axis_numeric_range_if_dotgamma0_0p2": [float(f3_from_printed_axis.min()), float(f3_from_printed_axis.max())],
            "deposited_vs_printed_axis_factor": float(np.median(f3 / f3_from_printed_axis)),
            "decision": "Keep both the deposited values and printed-label discrepancy. Do not reinterpret Fig3a coordinates as physical rad/s or silently rescale them.",
        },
    }
    pipe_json = SOURCE / "work/phase5/transport_operation/standing_mode.json"
    if pipe_json.exists():
        data = json.loads(pipe_json.read_text())
        case = next(c for c in data["cases"] if abs(c["wall_velocity_peak"] - 0.010) < 1e-12)
        result["pipe_mode"] = {
            "omega_rad_s": float(case["omega"]),
            "frequency_hz": float(case["frequency_hz"]),
            "ratio_to_fig1c_max_omega": float(case["omega"] / omega.max()),
            "exceeds_fig1c_max": bool(case["omega"] > omega.max()),
        }
    target = Path(__file__).with_name("axis_reconciliation.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
