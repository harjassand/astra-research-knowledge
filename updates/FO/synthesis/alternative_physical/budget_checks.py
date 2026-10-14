#!/usr/bin/env python3
"""Reproduce only arithmetic derived from the cited LiNbO3 writing papers."""

import json
import math
from pathlib import Path


root = Path(__file__).resolve().parent
mm2_cm2 = 0.01

cases = {
    "2024_fe_ln_example_86p4_W_cm2_60_s": 86.4 * 60,
    "2025_structured_example_537_W_cm2_30_s": 537 * 30,
    "2025_large_ring_14_W_cm2_1200_s": 14 * 1200,
}

uniform_window_J_cm2 = [8000, 16000]
energy_per_mm2_J = [x * mm2_cm2 for x in uniform_window_J_cm2]

# For two polar variants P = s P_s, s in {-1,+1}, and field-coupling
# density f_s = f_0 - E.P, the signed splitting is f_(+)-f_(-).
P_dot_E = 1.0  # symbolic unit-normalized projection, used only to check sign.
signed_splitting_unit = (0 - P_dot_E) - (0 + P_dot_E)

# Idealized Beer-Lambert attenuation across 1 mm, ignoring reflection,
# focusing, field redistribution, and the actual depth profile.
alpha_cm_inv = 20.4
thickness_cm = 0.1
transmission_1mm = math.exp(-alpha_cm_inv * thickness_cm)

assert cases["2024_fe_ln_example_86p4_W_cm2_60_s"] == 5184
assert cases["2025_structured_example_537_W_cm2_30_s"] == 16110
assert cases["2025_large_ring_14_W_cm2_1200_s"] == 16800
assert energy_per_mm2_J == [80.0, 160.0]
assert signed_splitting_unit == -2.0
assert abs(transmission_1mm - 0.1300) < 0.0001

result = {
    "status": "arithmetic_only; no physical cost or mechanism validation",
    "reported_intensity_time_products_J_cm2": cases,
    "structured_uniform_window_J_cm2": uniform_window_J_cm2,
    "incident_energy_for_uniformly_exposed_1_mm2_J": energy_per_mm2_J,
    "signed_field_splitting_for_unit_PdotE": signed_splitting_unit,
    "idealized_1mm_beer_lambert_transmission": transmission_1mm,
    "assumptions_and_exclusions": [
        "Dose products inherit each paper's reported intensity convention.",
        "Joules per projected area are incident optical dose, not wall-plug or absorbed energy.",
        "Beer-Lambert estimate ignores focusing, reflections, interfaces, and spatial attenuation.",
        "The sign check is a unit-normalized algebraic identity, not a material parameter."
    ]
}

(root / "budget_checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
