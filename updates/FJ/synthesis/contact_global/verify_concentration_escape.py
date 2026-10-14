#!/usr/bin/env python3
"""Exact rational check of the scaled N803 concentration escape formulas."""
from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


beta = F(283, 5670)
h = F(179, 540)
c = F(5951, 58800)
y4 = F(2641, 198450)
y2 = F(4, 45)
loss = beta**2 / (2*h)
optimizer_coefficient = beta/h
profile_gap = c - loss
l4_ratio_fourth_power_factor = 2*y4

assert loss == F(80089, 21313530)
assert optimizer_coefficient == F(566, 3759)
assert profile_gap == F(83079989, 852541200) > 0
assert l4_ratio_fourth_power_factor == F(2641, 99225)

cases = []
for base_amplitude, bump_amplitude in ((F(1), F(1)), (F(10), F(1)), (F(100), F(1)), (F(10), F(1, 10))):
    limiting_gap = F(3, 2)*base_amplitude**4 + bump_amplitude**4*profile_gap
    relative_y4_fourth_power = (bump_amplitude/base_amplitude)**4*l4_ratio_fourth_power_factor
    assert limiting_gap > 0
    cases.append({
        "M": str(base_amplitude),
        "alpha": str(bump_amplitude),
        "limiting_gap": str(limiting_gap),
        "relative_transverse_L4_fourth_power": str(relative_y4_fourth_power),
        "sqrt_rho_background_coefficient": str(-optimizer_coefficient*bump_amplitude),
    })

out = {
    "profile_loss": str(loss),
    "profile_energy": str(c),
    "profile_gap": str(profile_gap),
    "optimizer_coefficient": str(optimizer_coefficient),
    "relative_L4_factor": str(l4_ratio_fourth_power_factor),
    "relative_L2_squared_factor": str(2*y2),
    "cases": cases,
    "scope": "rational scaling check of the supplied exact profile; not a new Hessian integration or quasiconvexity proof",
}
Path(__file__).with_name("concentration_escape_checks.json").write_text(json.dumps(out, indent=2)+"\n")
print("PASS: exact positive limiting gaps coexist with an optimizer coefficient growing like rho^(-1/2).")
