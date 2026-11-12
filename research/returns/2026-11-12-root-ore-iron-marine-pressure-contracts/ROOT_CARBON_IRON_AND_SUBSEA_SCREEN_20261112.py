"""ROOT conditional engineering arithmetic, not producer code or device validation."""
import json
import math
from pathlib import Path

F = 96485.33212
R = 8.314462618
MFe = 0.055845
MNi = 58.6934  # g/mol
T = 298.15

carbon = {
    "perfect_sink_CO2_logmean_Pa": 101325 * 425e-6 / (2 * math.log(2)),
    "hyp_cover_CO2_permeance": 5e-6,
    "hyp_cover_water_permeance": 2.8e-7,
    "introduced_30C_saturation_pressure_Pa": 4247,
    "introduced_aw": 1,
    "introduced_RH": 0.2,
    "minimum_water_kg_per_CO2_kg_same_window_screen":
        (18.01528 / 44.0095) * (2.8e-7 / 5e-6) * (0.8 * 4247)
        / (101325 * 425e-6 / (2 * math.log(2))),
    "normal_cell_kWh_kg_at_point30V_point282CO2_per_e":
        0.30 * F / (0.282 * 0.0440095 * 3_600_000),
    "returned_candidate_kWh_kg_without_all_reset_and_startup": 1.464 - 0.180 - 0.299,
    "Ni_metal_corrosion_Ah_per_g": 2 * F / (3600 * MNi),
    "Ni_mg_mimicking_one_point1A_2point1h_8pct_reset":
        (0.1 * 2.1 * 0.08) / (2 * F / (3600 * MNi)) * 1000,
}

Ah_per_kg_Fe = 3 * F / (3600 * MFe)
iron = {
    "three_electron_Ah_per_kg_Fe": Ah_per_kg_Fe,
    "source_point_3point2V_point84FE_cell_kWh_kg": Ah_per_kg_Fe * 3.2 / 0.84 / 1000,
    "introduced_4kWh_kg_allplant_cell_voltage_ceiling_at_90pctFE": 4 * 1000 * 0.90 / Ah_per_kg_Fe,
    "source_net_reaction_NaOH_kg_per_kg_Fe": 3 * 0.039997 / MFe,
    "source_net_reaction_Cl2_kg_per_kg_Fe": 1.5 * 0.070906 / MFe,
    "NaOH_kg_for_100kg_SiO2_onepass_leach": 100 * 2 * 0.039997 / 0.0600843,
    "source_point_Fe_kg_m2_h_at_1000A_m2_point84FE":
        1000 * 0.84 * MFe * 3600 / (3 * F),
}

rho_water = 1025
rho_shell = 2400
rho_ballast = 2600
g = 9.81
eta_out = 0.9
subsea = []
for depth_m in (300, 600, 800, 1500):
    p = rho_water * g * depth_m
    for strength_MPa, shell_USD_m3 in ((20, 200), (50, 200), (80, 80)):
        strength = strength_MPa * 1e6
        if strength <= 1.5 * p:
            continue
        wall_per_void = 1.5 * p / (strength - 1.5 * p)
        ballast_per_void = max(0, (rho_water - (rho_shell - rho_water) * wall_per_void)
                               / (rho_ballast - rho_water))
        useful_kWh_per_void_m3 = eta_out * p / 3_600_000
        a = (3 * 100_000 * 3_600_000 / (4 * math.pi * eta_out * p)) ** (1 / 3)
        b = a * (1 + wall_per_void) ** (1 / 3)
        subsea.append({
            "introduced_depth_m": depth_m,
            "introduced_design_compression_MPa": strength_MPa,
            "UNQUOTED_shell_material_USD_m3": shell_USD_m3,
            "UNQUOTED_ballast_material_USD_m3": 20,
            "wall_volume_per_void_volume_Lame_screen": wall_per_void,
            "external_ballast_volume_per_void_volume": ballast_per_void,
            "useful_kWh_per_void_m3": useful_kWh_per_void_m3,
            "shell_only_USD_per_useful_kWh": shell_USD_m3 * wall_per_void / useful_kWh_per_void_m3,
            "shell_plus_ballast_material_USD_per_useful_kWh":
                (shell_USD_m3 * wall_per_void + 20 * ballast_per_void) / useful_kWh_per_void_m3,
            "single_100MWh_void_radius_m": a,
            "single_100MWh_wall_thickness_m": b - a,
        })

hydraulic_factor = 0.85 * 0.90 * 0.97**2 * 0.99
r = 0.08
n = 20
crf = r * (1 + r)**n / ((1 + r)**n - 1)
cycles = 8760 * 0.9 / 344
storage = {
    "introduced_pump85pct_turbine90pct_electric97pct_each_hold99pct_factor": hydraulic_factor,
    "extra_allowable_import_kWh_per_100kWh_at_65pct_target": 100/0.65 - 100/hydraulic_factor,
    "cycles_per_year_344h_schedule_90pct_availability": cycles,
    "15USD_kWh_65pct_RTE_2pct_annual_maintenance_subtotal_USD_MWh":
        1000 * 15 * (crf + 0.02) / cycles + 20/0.65,
    "source_ironchlorine_free_separator_remaining_USD_kWh": (1781.32 - 400) / 10,
}

joint_screen = {
    "scope": "Introduced strip-bending surrogate, not a pressure-tight vault design.",
    "pressure_Pa": rho_water * g * 600,
    "unsupported_liner_span_m": 0.001,
    "introduced_liner_design_stress_Pa": 100e6,
    "simply_supported_strip_thickness_m":
        0.001 * math.sqrt(3 * (rho_water * g * 600) / (4 * 100e6)),
    "compression_only_rectangular_joint_rule":
        "absolute eccentricity <= joint thickness / 6 for linear no-tension stress",
}

result = {
    "status": "CONDITIONAL_ANALYTIC_SCREENS_NOT_A_NEW_DEVICE",
    "carbon": carbon, "iron": iron, "subsea": subsea, "storage": storage,
    "joint_screen": joint_screen,
    "limits": [
        "Carbon cover coefficients are hypotheses from the available return, not joint measurements.",
        "Iron primary point is a short externally heated reagent-oxide experiment, not a whole ore plant.",
        "Lame model assumes homogeneous isotropic elastic spherical shell and uniform pressure.",
        "Compression allowance and prices are unqualified; buckling, creep, joints and ports can dominate.",
        "External ballast, seabed, construction, placement, machinery, cables and service need actual costs.",
        "Hydraulic efficiencies are introduced simultaneous requirements, not measured system performance.",
    ],
}
p = Path(__file__).with_suffix('.json')
p.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
