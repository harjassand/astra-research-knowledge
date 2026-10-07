#!/usr/bin/env python3
"""Exact arithmetic for the proposed family-029 analytic re-tuning.

This checks exponents, not the theta/reflection identities or zero-freeness.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

a, h, b = Q(159, 200), Q(41, 200), Q(7, 30)
M = a + b
sigma_zero = Q(917, 1000)
smooth, prefix = Q(181, 50), Q(363, 100)
alpha = Q(61, 100)
sigma_good, w, z = Q(919, 1000), Q(41, 500), Q(2, 5)
small_cut, far_cut = Q(13, 100), h + Q(1, 100000)
delta_init = Q(1, 10000000)
far_z = Q(400000)
C = a / 2 + h / 6
probe = (2 * M - 1 - b) / 2

def relative(sx, sw, sz):
    return sx - 1 + h * (sz - Q(1, 6)) + b * (sw - 1)

values = {
    "M": M,
    "principal_exponent": C,
    "probe_exponent": probe,
    "probe_saving": C - probe,
    "detector_shift_before_height_and_epsilon": smooth * (Q(1, 2) - sigma_zero) + Q(3, 2),
    "density_exponent_before_height_and_epsilon": prefix * (2 - 2 * sigma_zero),
    "density_slack": alpha - prefix * (2 - 2 * sigma_zero),
    "principal_w_remainder_saving": -relative(1 + delta_init, Q(4, 5), Q(1, 6) + delta_init),
    "principal_z_remainder_saving": -relative(1 + delta_init, 1, Q(1, 25)),
    "small_rows_saving": -(relative(1 + delta_init, w, z) + small_cut * (Q(3, 2) - z)),
    "exception_rows_saving": -(relative(1 + delta_init, w, z) + far_cut * (alpha + Q(1, 2) - z)),
    "good_rows_saving": -(relative(sigma_good, w, z) + far_cut * (Q(3, 2) - z)),
    "far_rows_saving": -(relative(4, 4, far_z) + far_cut * (1 - far_z)),
}

# Euler correction is locally normally convergent if all listed margins
# are positive; these are obtained from its exact closed local formula.
regions = {
    "nonprincipal": (sigma_good, w, z),
    "principal_w_shift": (Q(49, 50), Q(4, 5), Q(1, 6)),
    "principal_z_shift": (Q(49, 50), Q(1), Q(1, 25)),
}
euler = {}
for name, (sx, sw, sz) in regions.items():
    euler[name] = {
        "VW": sw + 6 * sz - 1,
        "D1V": sx + 6 * sz - 1,
        "D1W": sx + sw - 1,
        "Q_D1WV": sx + sw + 6 * sz - 2,
        "E1": 6 * sx + 6 * sz - 5,
        "bad_t1_k1": sx + sw - 1,
        "bad_l1_e0": 3 * sx - 2 - max(Q(0), Q(1, 2) - sw),
    }
    assert all(v > 0 for v in euler[name].values())

assert h == 1 - a
assert 0 < b < a and M > 1
assert prefix > smooth > 2
assert values["detector_shift_before_height_and_epsilon"] < 0
assert values["density_slack"] > 0
assert values["probe_saving"] == Q(1, 50)
for key, value in values.items():
    if key.endswith("_saving") and key != "probe_saving":
        assert value > Q(1, 50) + Q(1, 2000), (key, value)

def encode(v):
    if isinstance(v, Q):
        return {"rational": str(v), "decimal": float(v)}
    if isinstance(v, dict):
        return {k: encode(t) for k, t in v.items()}
    return v

payload = {
    "status": "exact_exponents_pass_only_not_a_theorem_validation",
    "parameters": encode({"a": a, "b": b, "h": h, "sigma_zero": sigma_zero,
                          "smooth": smooth, "prefix": prefix, "alpha": alpha,
                          "sigma_good": sigma_good, "w": w, "z": z,
                          "small_cut": small_cut, "far_cut": far_cut,
                          "far_z": far_z, "delta_init": delta_init}),
    "values": encode(values),
    "euler_region_margins": encode(euler),
}
Path(__file__).with_name("schedule_certificate.json").write_text(json.dumps(payload, indent=2) + "\n")
for key, value in values.items():
    print(f"{key}: {value} = {float(value):.12f}")
print("All exact schedule assertions passed.")
