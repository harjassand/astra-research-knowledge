#!/usr/bin/env python3
"""Reproduce source-calibrated calculations for cycle7b.

Run from any directory.  It reads the 500 K coverage row from the public
Materials Cloud source-data archive if that archive is present beside this
file.  Other source parameters are transcribed explicitly below; this is not a
microkinetic solver and does not create missing barriers or measurements.
"""
from __future__ import annotations

import csv
import io
import json
import math
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
KB_EV_K = 8.617333262145e-5
R_J_MOL_K = 8.31446261815324
NA = 6.02214076e23
EV_J = 1.602176634e-19


def source_coverages(archive: Path = RAW / "Source File.zip") -> tuple[float, float]:
    """Return (theta_H2*, theta_H*) from the published automated MKM output."""
    internal = (
        "Source File/Main Figures/Fig 4/Fig 4c/Automated Reactions/500/coverage.dat"
    )
    with zipfile.ZipFile(archive) as zf:
        raw = zf.read(internal).decode("utf-8-sig")
    lines = raw.splitlines()
    header = [field.strip() for field in lines[0].split("\t")]
    rows = csv.DictReader(io.StringIO("\n".join(lines[1:])), fieldnames=header, delimiter="\t")
    row = next(r for r in rows if float(r["Temperature"]) == 500.0)
    return float(row["H2*"]), float(row["H*"])


def h2_transfer_calculation() -> dict:
    theta_h2, theta_h = source_coverages()
    rho = theta_h2 / theta_h
    kbt = KB_EV_K * 500.0
    # (molecular-H2-assisted barrier, atomic-H-assisted barrier), eV at 500 K.
    pairs = {
        "CO2_to_COOH": (0.61, 1.43),
        "CO2_to_HCOO": (0.18, 0.64),
        "HCOOH_to_H2COOH": (0.54, 0.91),
        "CH3O_to_CH3OH": (0.44, 1.06),
    }
    result = {}
    for name, (barrier_h2, barrier_h) in pairs.items():
        delta = barrier_h - barrier_h2
        threshold = math.exp(-delta / kbt)
        # Mean-field TST ratio, with the same substrate coverage and equal
        # prefactors/site molecularities. A prefactor ratio multiplies this.
        result[name] = {
            "barrier_h2_eV": barrier_h2,
            "barrier_atomic_h_eV": barrier_h,
            "delta_barrier_eV": delta,
            "coverage_ratio_h2_over_h": rho,
            "equal_prefactor_crossover_coverage_ratio": threshold,
            "molecular_to_atomic_rate_ratio": rho / threshold,
        }
    # A reported mean absolute error is not a per-edge confidence interval;
    # this is just the Arrhenius amplification scale for a 0.13 eV error.
    return {
        "temperature_K": 500.0,
        "kBT_eV": kbt,
        "theta_H2_star": theta_h2,
        "theta_H_star": theta_h,
        "theta_H2_over_theta_H": rho,
        "route_pairs": result,
        "rate_factor_for_0p13_eV_barrier_shift": math.exp(0.13 / kbt),
        "rate_ratio_factor_for_opposite_0p13_eV_errors_in_competing_barriers": math.exp(0.26 / kbt),
        "assumptions": [
            "The path-specific substrate coverage cancels.",
            "Equal transition-state prefactors and equal effective site molecularities.",
            "Published MKM coverages are model outputs, not measured coverages.",
            "Published DFT free-energy barriers are used as transcribed; no missing barrier is imputed.",
        ],
    }


def dynamic_activation_calculation() -> dict:
    # The 2025 article reports 360 mL/min, 3 H2:1 CO2, 2.0 MPa, 300 C,
    # 452 m/s gas-jet speed, and about 0.34 W kinetic power. 22.414 L/mol is
    # used conditionally as the STP molar volume; this reproduces the reported
    # jet power closely and is therefore a transparent basis reconstruction.
    flow_L_min = 0.360
    molar_volume_L_mol = 22.414
    n_dot = flow_L_min / molar_volume_L_mol / 60.0
    m_h2_g_mol = 2.01588
    m_co2_g_mol = 44.0095
    mean_molar_mass_kg_mol = (3.0 * m_h2_g_mol + m_co2_g_mol) / 4.0 / 1000.0
    mass_dot = n_dot * mean_molar_mass_kg_mol
    gas_speed_m_s = 452.0
    kinetic_power_W = 0.5 * mass_dot * gas_speed_m_s**2

    p_ratio = 20.0  # 2.0 MPa relative to 0.1 MPa
    t_ambient_K = 298.15
    compression_W = n_dot * R_J_MOL_K * t_ambient_K * math.log(p_ratio)
    cp_h2 = 28.836  # J mol^-1 K^-1 near 298 K; ideal-gas estimate
    cp_co2 = 37.135
    cp_mix = (3.0 * cp_h2 + cp_co2) / 4.0
    t_reactor_K = 573.15
    sensible_heat_W = n_dot * cp_mix * (t_reactor_K - t_ambient_K)

    methanol_mw_g_mol = 32.04186
    dar_sty_g_h_gcat = 0.660
    fbr_sty_g_h_gcat = 0.100
    dar_rate_mol_s_gcat = dar_sty_g_h_gcat / methanol_mw_g_mol / 3600.0
    fbr_rate_mol_s_gcat = fbr_sty_g_h_gcat / methanol_mw_g_mol / 3600.0
    delta_rate = dar_rate_mol_s_gcat - fbr_rate_mol_s_gcat

    # Reconstruct the source's nanoscale impact-energy argument.
    diameter_nm = 20.0
    length_nm = 100.0
    density_g_cm3 = 4.0
    cu_mass_fraction = 0.40
    particle_speed_m_s = 75.0
    cu_molar_mass_g_mol = 63.546
    particle_energy_source_eV = 1840.0
    particle_energy_recomputed_eV = (
        0.5
        * (density_g_cm3 * math.pi * (diameter_nm / 2.0) ** 2 * length_nm * 1e-21 / 1000.0)
        * particle_speed_m_s**2
        / EV_J
    )
    particle_volume_cm3 = math.pi * (diameter_nm / 2.0) ** 2 * length_nm * 1e-21
    particle_mass_g = density_g_cm3 * particle_volume_cm3
    cu_atoms_geometry = (
        particle_mass_g * cu_mass_fraction / cu_molar_mass_g_mol * NA
    )
    cu_atoms_reported = 13000.0
    affected_fraction = 1.0 / 3.0
    absorbed_fraction = 0.5
    e_per_affected_source = (
        particle_energy_source_eV * absorbed_fraction
        / (cu_atoms_geometry * affected_fraction)
    )
    e_per_affected_formula = (
        particle_energy_recomputed_eV * absorbed_fraction
        / (cu_atoms_geometry * affected_fraction)
    )
    excess_state_eV_per_atom = 0.17
    max_affected_atoms_source_energy = (
        particle_energy_source_eV * absorbed_fraction / excess_state_eV_per_atom
    )
    required_affected_fraction_source_energy = (
        max_affected_atoms_source_energy / cu_atoms_geometry
    )

    return {
        "basis": {
            "flow_mL_min": flow_L_min * 1000.0,
            "assumed_molar_volume_L_mol": molar_volume_L_mol,
            "feed_ratio_H2_CO2": "3:1",
            "pressure_ratio": p_ratio,
            "temperature_in_K": t_ambient_K,
            "temperature_out_K": t_reactor_K,
            "gas_speed_m_s": gas_speed_m_s,
        },
        "flow_and_power": {
            "molar_flow_mol_s": n_dot,
            "mean_molar_mass_kg_mol": mean_molar_mass_kg_mol,
            "mass_flow_kg_s": mass_dot,
            "kinetic_power_reconstructed_W": kinetic_power_W,
            "reported_kinetic_power_W": 0.34,
            "ideal_reversible_isothermal_compression_from_1bar_W": compression_W,
            "ideal_sensible_heating_from_298K_to_573K_W": sensible_heat_W,
            "warning": "Kinetic jet power is drawn from the pressurized gas stream; do not add it again to compressor work as an independent actuator load.",
        },
        "reported_STY_and_specific_energy_scales": {
            "DAR_methanol_rate_mol_s_gcat": dar_rate_mol_s_gcat,
            "FBR_methanol_rate_mol_s_gcat": fbr_rate_mol_s_gcat,
            "DAR_to_FBR_STY_ratio": dar_sty_g_h_gcat / fbr_sty_g_h_gcat,
            "kinetic_stream_energy_per_DAR_mol_J_mol": kinetic_power_W / dar_rate_mol_s_gcat,
            "kinetic_stream_energy_per_incremental_mol_J_mol": kinetic_power_W / delta_rate,
            "ideal_compression_work_per_DAR_mol_J_mol": compression_W / dar_rate_mol_s_gcat,
            "ideal_heating_duty_per_DAR_mol_J_mol": sensible_heat_W / dar_rate_mol_s_gcat,
        },
        "source_particle_energy_argument": {
            "geometry_diameter_nm": diameter_nm,
            "geometry_length_nm": length_nm,
            "particle_impact_speed_m_s": particle_speed_m_s,
            "density_g_cm3": density_g_cm3,
            "cu_mass_fraction": cu_mass_fraction,
            "calculated_Cu_atoms_from_stated_geometry": cu_atoms_geometry,
            "Cu_atoms_reported_by_source": cu_atoms_reported,
            "geometry_to_reported_atom_count_ratio": cu_atoms_geometry / cu_atoms_reported,
            "source_reported_particle_kinetic_energy_eV": particle_energy_source_eV,
            "particle_kinetic_energy_from_stated_geometry_eV": particle_energy_recomputed_eV,
            "source_energy_per_affected_Cu_eV_using_geometry_count": e_per_affected_source,
            "formula_energy_per_affected_Cu_eV_using_geometry_count": e_per_affected_formula,
            "DFT_excess_energy_eV_per_Cu_atom": excess_state_eV_per_atom,
            "maximum_affected_Cu_atoms_at_half_source_energy": max_affected_atoms_source_energy,
            "maximum_affected_fraction_at_half_source_energy": required_affected_fraction_source_energy,
            "assumptions": [
                "Cylinder geometry with diameter 20 nm and length 100 nm.",
                "Density 4 g cm^-3 and 40 wt% Cu, as stated in the SI.",
                "Half of the particle kinetic energy is absorbed and one third of Cu atoms are affected, as stated in the SI.",
                "The 0.17 eV/atom DFT difference is compared as though it were a stored energetic cost; this is not a measured free energy.",
            ],
        },
    }


def main() -> None:
    print(json.dumps({
        "molecular_H2_path_test": h2_transfer_calculation(),
        "dynamic_activation_energy_audit": dynamic_activation_calculation(),
    }, indent=2))


if __name__ == "__main__":
    main()
