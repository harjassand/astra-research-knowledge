#!/usr/bin/env python3
"""Reconstruct a conditional electrokinetic two-port figure of merit.

Inputs are reported by Pingulkar, Ayela & Salmon (Lab Chip 24, 5328 (2024))
for their 0.1 mM NaCl, 2 cm packed-colloid plug. This is a unit conversion
and model calculation, not a new measurement or validation of the reported
coefficients. The source did not directly acquire both reciprocal cross
responses on the same plug.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


SSTR_A_PER_BAR = 25e-9
R_H_BAR_MIN_PER_UL = 1.0
R_C_OHM = 25e6
R_C_RANGE_OHM = (20e6, 30e6)  # reported 25 +/- 5 MOhm fit
BAR_PA = 1e5
MIN_S = 60.0
UL_M3 = 1e-9


def eta_converter(z: float) -> float:
    root = math.sqrt(1.0 + z)
    return (root - 1.0) / (root + 1.0)


def calculate(rc_ohm: float) -> dict[str, float]:
    # Q/p = 1/Rh; convert bar*min/uL into Pa*s/m^3 first.
    rh_pa_s_per_m3 = R_H_BAR_MIN_PER_UL * BAR_PA * MIN_S / UL_M3
    k_m3_per_pa_s = 1.0 / rh_pa_s_per_m3
    c_a_per_pa = SSTR_A_PER_BAR / BAR_PA
    g_s = 1.0 / rc_ohm
    chi = c_a_per_pa**2 / (k_m3_per_pa_s * g_s)
    if chi >= 1.0:
        raise ValueError("reported coefficients violate the passive reciprocal bound chi < 1")
    z = chi / (1.0 - chi)
    eta = eta_converter(z)
    # Same grounded, three-terminal, quasistatic two-converter topology as
    # the incoming physical source; not a universal isolator limit.
    eta_isolator = 0.25 * eta**2
    return {
        "R_h_Pa_s_per_m3": rh_pa_s_per_m3,
        "K_m3_per_Pa_s": k_m3_per_pa_s,
        "S_str_A_per_Pa": c_a_per_pa,
        "R_C_ohm": rc_ohm,
        "G_S": g_s,
        "chi_dimensionless": chi,
        "Z_dimensionless": z,
        "single_converter_eta_max_fraction": eta,
        "two_converter_isolator_eta_upper_fraction": eta_isolator,
    }


base = calculate(R_C_OHM)
low_rc = calculate(R_C_RANGE_OHM[0])
high_rc = calculate(R_C_RANGE_OHM[1])
result = {
    "scope": "conditional reconstruction from a reported fitted S_str, R_C, and R_h; no assembled isolator experiment",
    "base": base,
    "R_C_fit_range_sensitivity": {
        "R_C_range_ohm": list(R_C_RANGE_OHM),
        "Z_range": [high_rc["Z_dimensionless"], low_rc["Z_dimensionless"]],
        "single_converter_eta_max_fraction_range": [high_rc["single_converter_eta_max_fraction"], low_rc["single_converter_eta_max_fraction"]],
        "two_converter_isolator_eta_upper_fraction_range": [high_rc["two_converter_isolator_eta_upper_fraction"], low_rc["two_converter_isolator_eta_upper_fraction"]],
    },
    "caveats": [
        "The paper fits S_str and R_C from loaded streaming-voltage data; it does not independently measure the reverse electro-osmotic coefficient on the same plug.",
        "The two-converter bound assumes the incoming source's grounded three-contact quasistatic topology and is not a universal limit.",
        "Reported errors for S_str and R_h are not available in the paper text; the displayed range varies only R_C by its stated +/-5 MOhm fit uncertainty.",
    ],
}
out = Path(__file__).with_name("electrokinetic_bound.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
