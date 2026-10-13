#!/usr/bin/env python3
"""Attach corrected source-axis metadata to the preserved max-8 replay."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = Path(
    "/Users/harjas/Documents/Codex/2026-10-13/"
    "astra-genesis-civilization-enabling-breakthrough-discovery"
)
TRANSPORT = SOURCE / "work/phase5/transport_operation"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    data = json.loads((HERE / "witness_results_11x24_max8.json").read_text())
    axes = json.loads((HERE / "axis_reconciliation.json").read_text())
    data.pop("source_dynamic_frequency_axis_rad_s", None)
    data["status"] = (
        "Bounded 11x24 fixed-end replay; Model B converged, Model A mode iteration not marked converged at max_steps=8. "
        "No rheology/device validation. Frequency-axis metadata corrected after replay; numerical rows unchanged."
    )
    data["contract"]["passivity"] = (
        "A causal thixotropic state q obeys tau*q_dot+q=gamma_OSP(t). For sinusoidal gamma_OSP=a*sin(omega*t), "
        "m=2*mean(q*gamma_OSP)/a^2=1/(1+(omega*tau)^2). Set eta_B=eta_0-m*(eta_0-eta_A); with "
        "eta_0>=eta_A>0 and 0<=m<=1, the cycle-averaged axial stress power is eta_B*gamma_dot_parallel^2>=0. "
        "Use a positive cross dashpot eta_perp>0 and zero stored structural free energy for q; then total "
        "mechanical dissipation is eta_B*gamma_dot_parallel^2+eta_perp*gamma_dot_OSP^2>=0. This is a passive "
        "cycle-averaged thixotropic closure, not a fitted particle-level law or full transient fit."
    )
    for label, case in data["reduced_grid_cases"].items():
        case["any_OSP_chi_extrapolation"] = bool(case["maximum_chi"] > 4.71239)
    cdir = TRANSPORT / "sources/biaxial_raw/biaxial_repository"
    inputs = {
        "fig1c_primary.csv": cdir / "fig1c/fig1c_primary.csv",
        "fig1c_OSP.csv": cdir / "fig1c/fig1c_OSP.csv",
        "fig1d_1.0_primary.csv": cdir / "fig1d/fig1d_1.0_primary.csv",
        "fig1d_1.0_OSP.csv": cdir / "fig1d/fig1d_1.0_OSP.csv",
        "fig3a_frequency.csv": cdir / "fig3a/fig3a_frequency.csv",
        "fig3a_exp_matrix.csv": cdir / "fig3a/fig3a_exp_matrix.csv",
        "fig3a_amplitude.csv": cdir / "fig3a/fig3a_amplitude.csv",
    }
    data["source_sha256"].update({name: sha256(path) for name, path in inputs.items()})
    data["source_frequency_reconciliation"] = {
        "fig1c_physical_angular_frequency_rad_s": axes["fig1c_primary"]["omega_range_rad_s"],
        "fig1d_amplitude_1pct_relative_osp_rate_chi": axes["fig1d_amplitude_1pct"]["chi_range"],
        "fig1d_chi_formula_error": axes["fig1d_amplitude_1pct"]["chi_equals_0p01_omega_over_0p2_max_abs_error"],
        "fig3a_deposited_coordinate": axes["fig3a_deposited"]["frequency_coordinate_range"],
        "fig3a_coordinate_relation": axes["fig3a_deposited"]["coordinate_relation_to_fig1c_omega"],
        "fig3a_relation_max_relative_error": axes["fig3a_deposited"]["relation_max_relative_error"],
        "fig3a_printed_axis": axes["fig3a_deposited"]["printed_fig3_axis_from_accepted_pdf_p4"],
        "fig3a_deposited_vs_printed_factor": axes["fig3a_deposited"]["deposited_vs_printed_axis_factor"],
        "fig3a_matrix_row_2_vs_fig1c_eta_parallel_error_Pa_s": axes["fig3a_deposited"]["matrix_row_2_equals_fig1c_primary_max_abs_error_Pa_s"],
        "pipe_mode_omega_rad_s": axes["pipe_mode"]["omega_rad_s"],
        "pipe_to_fig1c_max_ratio": axes["pipe_mode"]["ratio_to_fig1c_max_omega"],
        "note": "Fig3a deposited and printed axis disagree by pi^2; deposited values are not physical rad/s. The transport solver uses Fig1d, not Fig3a.",
    }
    data["receipt_annotation"] = (
        "All fixed-end numerical rows copied unchanged from witness_results_11x24_max8.json; "
        "only axis metadata, provenance labels, and extrapolation flags were corrected."
    )
    target = HERE / "witness_results_11x24.json"
    target.write_text(json.dumps(data, indent=2) + "\n")
    print(target)


if __name__ == "__main__":
    main()
