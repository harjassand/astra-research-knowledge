"""Source-linked arithmetic and analytic thresholds; no simulated material data.

Run from any directory with Python 3. Writes screening_calculations.json beside
this file. The approximate Cu-ZIF-gis capacity is a visual Fig. 3d reading, not
raw source data. All-D graphene occupation is an upper-bound scenario.
"""

import json
import math
from pathlib import Path

AVOGADRO = 6.02214076e23
DEUTERIUM_ATOM_G_PER_MOL = 2.01410177812


def compute():
    thresholds = []
    for retained in (0.99, 0.95, 0.9, 0.8, 0.5):
        for gain in (2.0, 10.0):
            thresholds.append({
                "retained_D_fraction": retained,
                "additional_odds_gain": gain,
                "required_H_to_D_integrated_escape_ratio":
                    1 + math.log(gain) / -math.log(retained),
            })

    density_cm2 = 1e14
    area_micro_cm2 = math.pi * (15e-4 / 2) ** 2
    stored_micro_mol = density_cm2 * area_micro_cm2 / AVOGADRO
    stored_mol_per_m2 = density_cm2 * 1e4 / AVOGADRO
    return {
        "status": "NOT_ACHIEVED",
        "calculation_type": "analytic screening thresholds and source-linked arithmetic; no material simulation",
        "purge_thresholds": thresholds,
        "graphene_capacity": {
            "source_adsorbed_atoms_per_cm2": density_cm2,
            "source_exposed_hole_diameter_um": 15.0,
            "microdevice_area_cm2": area_micro_cm2,
            "microdevice_max_stored_hydrons_mol": stored_micro_mol,
            "microdevice_mass_if_all_D_femtograms":
                stored_micro_mol * DEUTERIUM_ATOM_G_PER_MOL * 1e15,
            "max_stored_hydrons_mol_per_m2": stored_mol_per_m2,
            "mass_if_all_D_micrograms_per_m2":
                stored_mol_per_m2 * DEUTERIUM_ATOM_G_PER_MOL * 1e6,
            "scope": "Capacity arithmetic only. All-D occupation is an upper-bound scenario, not measured mixture separation.",
        },
        "CuZIF_gis_protocol_arithmetic": {
            "mixed_D2_uptake_mmol_per_g_figure_read": 0.45,
            "figure_read_precision": "Approximate visual Fig. 3d reading; 120 K, 2 bar, 1:1 H2:D2, published TDS protocol",
            "exposure_min": 60.0,
            "readout_ramp_start_K": 18.0,
            "readout_ramp_end_K": 240.0,
            "ramp_K_per_min": 6.0,
            "readout_ramp_min": (240 - 18) / 6,
            "exposure_plus_ramp_min": 60 + (240 - 18) / 6,
            "capacity_divided_by_exposure_plus_ramp_mmol_per_g_per_h":
                0.45 / ((60 + (240 - 18) / 6) / 60),
            "scope": "Protocol arithmetic excludes cooling, evacuation and losses; not measured production throughput or a universal bound.",
        },
        "random_pairing_at_illustrative_atomic_D_fraction": {
            "x": 1.5e-4,
            "H2": (1 - 1.5e-4) ** 2,
            "HD": 2 * 1.5e-4 * (1 - 1.5e-4),
            "D2": (1.5e-4) ** 2,
            "scope": "Combinatorial scenario; does not establish that a particular feed is equilibrated.",
        },
        "Carnot_refrigeration_at_ambient_298K": [
            {"cold_temperature_K": t,
             "minimum_refrigerator_work_J_per_J_heat_at_constant_T": 298 / t - 1}
            for t in (18.0, 23.3, 60.0, 77.0, 115.0, 120.0, 159.0)
        ],
        "doubled_1p7_odds_D_fraction": 3.4 / 4.4,
    }


if __name__ == "__main__":
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(compute(), indent=2) + "\n")
    print(target)
