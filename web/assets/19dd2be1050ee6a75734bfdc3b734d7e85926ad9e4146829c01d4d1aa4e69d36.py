"""Finite illustration of the conditional robust boxcar theorem.

The uncertainty radii below are hypothetical stress-test inputs, not
measurements or typical material uncertainties. The exact robust reduction is proved in
CYCLE2_REPORT.md; this script only enumerates interval endpoints on a finite
grid and compares nominal vs worst-corner objectives for the same center data.
"""
from __future__ import annotations
import json
import math

from pareto_probe import cumulative_moments


def enumerate_profiles(ratio: float, radii: dict[str, float], pf_floor: float):
    xs, pref = cumulative_moments()
    nominal = {"zt_center": -math.inf}
    nominal_robust_pf = {"zt_center": -math.inf}
    robust = {"zt_lower": -math.inf}
    n = len(xs)
    for i in range(n - 1):
        A0, B0, C0 = (pref[k][i] for k in range(3))
        for j in range(i + 1, n):
            A = pref[0][j] - A0
            B = pref[1][j] - B0
            C = pref[2][j] - C0
            if A <= 0 or B <= 0:
                continue
            pf = B * B / A
            z_nom_den = A * (C + ratio) - B * B
            if z_nom_den <= 0:
                continue
            z_nom = B * B / z_nom_den

            # Design-invariant absolute uncertainty radii. The box-corner
            # formula below is exact for this assumed rectangle.
            A_hi = A + radii["A"]
            B_lo = B - radii["B"]
            C_hi = C + radii["C"]
            a_hi = ratio + radii["a"]
            if A_hi <= 0 or a_hi <= 0:
                continue
            pf_lo = B_lo * B_lo / A_hi if B_lo > 0 else 0.0
            den = A_hi * (C_hi + a_hi) - B_lo * B_lo if B_lo > 0 else math.inf
            z_lo = B_lo * B_lo / den if B_lo > 0 and den > 0 else 0.0
            if pf + 1e-12 >= pf_floor and z_nom > nominal["zt_center"]:
                nominal = {"lo": xs[i], "hi": xs[j], "pf_center": pf,
                           "zt_center": z_nom, "pf_lower": pf_lo,
                           "zt_lower": z_lo}
            if pf_lo + 1e-12 >= pf_floor and z_nom > nominal_robust_pf["zt_center"]:
                nominal_robust_pf = {"lo": xs[i], "hi": xs[j],
                                     "pf_center": pf, "pf_lower": pf_lo,
                                     "zt_center": z_nom,
                                     "zt_lower": z_lo}
            if pf_lo + 1e-12 < pf_floor or den <= 0:
                continue
            if z_lo > robust["zt_lower"]:
                robust = {"lo": xs[i], "hi": xs[j], "pf_lower": pf_lo,
                          "zt_lower": z_lo, "pf_center": pf,
                          "zt_center": z_nom}
    return {"nominal_optimum_same_center_data": nominal,
            "center_ZT_optimum_subject_to_same_robust_PF_floor": nominal_robust_pf,
            "robust_optimum_same_center_data": robust}


def main():
    radii = {"A": 0.01, "B": 0.01, "C": 0.02, "a": 0.02}
    result = {
        "status": "finite grid illustration only; no material or typical-error claim",
        "model": "same absolute interval radii at every candidate; independent rectangular box; center a=0.1",
        "absolute_uncertainty_radii": radii,
        "robust_normalized_PF_floor": 1.0,
        "energy_grid": {"min": -1.0, "max": 15.0, "step": 0.02},
        "case": enumerate_profiles(0.1, radii, 1.0),
        "notes": [
            "Center-data nominal optimum and robust optimum use identical center moments and the same stated interval widths.",
            "Robust values are analytical worst corners for the assumed rectangle, evaluated only on the finite endpoint grid.",
            "No confidence level, measurement covariance, acquisition cost, fabrication route, or sample was supplied."
        ]
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
