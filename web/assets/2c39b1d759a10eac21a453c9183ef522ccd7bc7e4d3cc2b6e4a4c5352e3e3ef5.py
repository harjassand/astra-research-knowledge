#!/usr/bin/env python3
"""Exact rational feasibility checks for a shared glucose actuator.

The two cells lie on opposing FBP faces of the previously studied safety
box.  A common extracellular glucose concentration must satisfy both face
conditions at once.  Fraction arithmetic makes the reported endpoints exact.
The +/-10% ranges are a declared genotype-uncertainty stress box around the
PLOS 2021 IC genotype; they are not measured confidence intervals.
"""

from fractions import Fraction as Q
import json
from pathlib import Path


P = dict(
    vu=Q("10.92211"), vl=Q("5.65143"), katp=Q("4.82003"), kp=Q("2.07099"),
    kmg=Q("0.1"), kma=Q("0.1"), ki=Q("3"), atot=Q("5"),
    kmf=Q("1"), kmd=Q("0.1"), kmp=Q("2"), pvmax=Q("10"), kvac=Q("250"),
)


def upper_capacity(a, vu):
    """v_up saturation as external glucose tends to infinity."""
    return vu * a / (P["kma"] + a * (1 + a / P["ki"]))


def lower_flux(f, a, pi, vl):
    d = P["atot"] - a
    return (vl * f / (P["kmf"] + f) * d / (P["kmd"] + d) *
            pi / (P["kmp"] + pi))


def glucose_for_flux(u, a, vu):
    b = upper_capacity(a, vu)
    if not (0 <= u < b):
        raise ValueError((u, b))
    return P["kmg"] * u / (b - u)


def source_parameter_pi_margin(f, pi, vl, kp, a=Q(0)):
    d = P["atot"] - a
    t = pi + 2 * f + a
    pv = P["pvmax"] / (1 + (t / P["kvac"]) ** 4)
    L = lower_flux(f, a, pi, vl)
    # Full-source Pi face derivative; at ATP=0 growth is zero because
    # vatpg=katp*A-vatpe<0.  The no-growth dilution term is therefore zero.
    return kp * (pv - pi) - 2 * L


def frac_text(x):
    return {"fraction": f"{x.numerator}/{x.denominator}", "decimal": float(x)}


def main():
    # Both states are within F in [1.8,2.2], ATP>=0.3, Pi>=1,
    # ATP+Pi<=14.  Growth is zero at ATP=0.3 for the source IC expression cost.
    upper_cell = (Q("2.2"), Q("0.3"), Q("1"))
    lower_cell = (Q("1.8"), Q("0.3"), Q("10"))

    # Nominal exact-input interval.
    f_hi, a_hi, pi_hi = upper_cell
    L_hi = lower_flux(f_hi, a_hi, pi_hi, P["vl"])
    B_hi = upper_capacity(a_hi, P["vu"])
    G_hi_nom = glucose_for_flux(L_hi, a_hi, P["vu"])

    f_lo, a_lo, pi_lo = lower_cell
    L_lo = lower_flux(f_lo, a_lo, pi_lo, P["vl"])
    B_lo = upper_capacity(a_lo, P["vu"])
    G_lo_nom = glucose_for_flux(L_lo, a_lo, P["vu"])

    # Robust simultaneous guarantee over +/-10% uncertainty in only the four
    # genotype values; common Michaelis/Pi-store constants stay at Table 1.
    L_hi_min = lower_flux(f_hi, a_hi, pi_hi, P["vl"] * Q("0.9"))
    B_hi_max = upper_capacity(a_hi, P["vu"] * Q("1.1"))
    G_hi_robust = glucose_for_flux(L_hi_min, a_hi, P["vu"] * Q("1.1"))

    L_lo_max = lower_flux(f_lo, a_lo, pi_lo, P["vl"] * Q("1.1"))
    B_lo_min = upper_capacity(a_lo, P["vu"] * Q("0.9"))
    G_lo_robust = glucose_for_flux(L_lo_max, a_lo, P["vu"] * Q("0.9"))

    # ATP-face condition at the lower-F cell: A'= -2U+4L-kA.  The
    # uncertainty-worst admissible flux is 2 L_min - k_max A/2.
    L_lo_min = lower_flux(f_lo, a_lo, pi_lo, P["vl"] * Q("0.9"))
    u_atp_max = 2 * L_lo_min - P["katp"] * Q("1.1") * a_lo / 2
    G_atp_max = glucose_for_flux(u_atp_max, a_lo, P["vu"] * Q("1.1"))

    # Pi-floor viability boundary with ATP=0 and Pi*=0.05 mM.
    p_floor = Q("0.05")
    pi_thresholds = {}
    for f in (250, 300, 325, 350):
        margin_ref = source_parameter_pi_margin(Q(f), p_floor, P["vl"], P["kp"])
        margin_robust = source_parameter_pi_margin(
            Q(f), p_floor, P["vl"] * Q("1.1"), P["kp"] * Q("0.9"))
        pi_thresholds[str(f)] = {
            "nominal_margin": frac_text(margin_ref),
            "minus10kp_plus10vl_margin": frac_text(margin_robust),
        }

    data = {
        "model": "PLOS 2021 core glycolysis, IC Table 2 genotype; Table 1 common kinetics",
        "units": {"concentration": "mM", "time": "min"},
        "shared_actuator_conflict": {
            "high_FBP_face_state": list(map(str, upper_cell)),
            "low_FBP_face_state": list(map(str, lower_cell)),
            "nominal_upper_G_at_high_FBP": frac_text(G_hi_nom),
            "nominal_lower_G_at_low_FBP": frac_text(G_lo_nom),
            "robust_upper_G_at_high_FBP_pm10_genotype": frac_text(G_hi_robust),
            "robust_lower_G_at_low_FBP_pm10_genotype": frac_text(G_lo_robust),
            "robust_lower_face_ATP_upper_G": frac_text(G_atp_max),
            "robust_interval_empty": G_lo_robust > G_hi_robust,
            "proof": "At the FBP=2.2 state invariance requires G<=G_hi; at the FBP=1.8 state it requires G>=G_lo. These inequalities are incompatible even under exact kinetics, and remain incompatible over the declared +/-10% genotype box.",
        },
        "uncontrollable_Pi_face": {
            "state_definition": "ATP=0, Pi=0.05 mM, FBP=F; no growth because ATPase flux is below the IC expression cost.",
            "robust_parameter_range": "vl in [0.9,1.1]*5.65143; kp in [0.9,1.1]*2.07099; other Table 1 kinetics fixed",
            "margins": pi_thresholds,
            "interpretation": "Pi derivative is independent of glucose at ATP=0. If a margin is negative, no glucose policy can make that Pi floor inward at that state; it must first move the state (e.g. lower FBP or raise ATP).",
        },
        "parameter_uncertainty_status": "The +/-10% box is a stress-test assumption, not an experimental confidence set.",
        "arithmetic": "All displayed endpoints and margins are computed with fractions from decimal source values; only decimal renderings are rounded.",
    }
    out = Path(__file__).with_name("shared_actuator_certificate.json")
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
