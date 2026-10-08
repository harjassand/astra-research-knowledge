#!/usr/bin/env python3
"""Exact-rational facet and shared-actuator audit for the PLOS source model.

This checks the source-reference genotype, full health-gated growth/dilution,
the feedback tube S, and a two-cell common-glucose impossibility witness.
It is a model certificate, not a biological validation.  Only the displayed
bound ln(2)<7/10 uses a standard elementary real inequality; the rest is exact
Fraction arithmetic from the decimal source parameters.
"""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


# Source-reference genotype and Table 1 kinetics (concentrations in mM,
# rates in mM/min, first-order constants in 1/min).
VU = VL = KATP = PV_MAX = Q(10)
KP = Q("0.3")
KMG = KMATP = Q("0.1")
KIATP = Q(3)
ATOT = Q(5)
KMF = Q(1)
KMADP = Q("0.1")
KMP = Q(2)
KVAC = Q(250)
VATPER = Q(5)
VATPRB = Q("12.7")
TAUG = Q(90)
EPS = Q("0.17")
FLO, FHI = Q("1.8"), Q("2.2")
ALO, AHI = Q("0.5"), Q("1.5")
PLO, SUMHI = Q(2), Q(14)

# At the source reference genotype, CellML's n=4 cost ratio equals 5 exactly.
# ug = ln(2)/(90*(12.7-5)) = ln(2)/693.  Since ln(2)<0.7,
# g <= 10 ln(2)/693 < 7/693 on A<=1.5 in S.
G_UPPER = Q(7, 693)


def vlo(f, a, p):
    d = ATOT - a
    return VL * f * d * p / ((KMF + f) * (KMADP + d) * (KMP + p))


def uptake_capacity(a):
    return VU * a / (KMATP + a * (1 + a / KIATP))


def p_vac(f, a, p):
    ptotal = p + 2 * f + a
    return PV_MAX / (1 + (ptotal / KVAC) ** 4)


def show(x):
    return {"fraction": f"{x.numerator}/{x.denominator}", "decimal": float(x)}


def main():
    # Whole-tube vacuolar lower bound from Ptot<=14+2*2.2=18.4.
    ptotal_max = SUMHI + 2 * FHI
    pv_min = PV_MAX / (1 + (ptotal_max / KVAC) ** 4)

    # Full-source derivatives under actual-flux feedback
    # U=L-(F-2)+e, |e|<=0.17:
    # Fdot=2-F+e-F*g
    # Adot=2L+2(F-2)-2e-10A-A*g
    # Pdot=-2L+10A+kp(Pv-P)-P*g
    # (A+P)dot=2(F-2)-2e+kp(Pv-P)-(A+P)*g.
    # At A=0.5 ATPase equals expression cost, so g=0 exactly. For A>0.5,
    # the source health law has nonnegative Hdot.
    f_lower = (Q(2) - FLO - EPS) - FLO * G_UPPER
    f_upper = Q(2) - FHI + EPS  # maximum uses g=0
    a_lower = (2 * vlo(FLO, ALO, PLO) + 2 * (FLO - 2)
               - 2 * EPS - KATP * ALO)
    a_upper = (2 * vlo(FHI, AHI, SUMHI - AHI) + 2 * (FHI - 2)
               + 2 * EPS - KATP * AHI)  # dilution only improves this face
    pi_lower = (-2 * vlo(FHI, ALO, PLO) + KATP * ALO
                + KP * (pv_min - PLO) - PLO * G_UPPER)
    sum_upper = (2 * (FHI - 2) + 2 * EPS
                 + KP * (PV_MAX - (SUMHI - AHI)))

    # Static inversion exists over the full tube.  Use independent extrema,
    # which are conservative but easy to verify exactly.
    l_min = vlo(FLO, AHI, PLO)
    l_max = vlo(FHI, ALO, SUMHI - ALO)
    u_min = l_min - (FHI - 2) - EPS
    u_max = l_max + (FHI - 2) + EPS
    # C'(A) has sign 0.1-A^2/3, so its minimum on [.5,1.5]
    # occurs at one of the two endpoints.
    cu_min = min(uptake_capacity(ALO), uptake_capacity(AHI))
    saturation_gap = cu_min - u_max
    glucose_max = KMG * u_max / saturation_gap

    # Simultaneous opposite F faces under a shared extracellular glucose G.
    # At x_low, A=0.5 gives g=0 and inwardness needs U_low>=L_low.
    # At x_high, U_high<=L_high+F_high*g_max.
    x_low = (FLO, ALO, SUMHI - ALO)
    x_high = (FHI, AHI, PLO)
    l_low = vlo(*x_low)
    l_high = vlo(*x_high)
    c_low, c_high = uptake_capacity(ALO), uptake_capacity(AHI)
    ratio = c_high / c_low
    common_u_high_lower = ratio * l_low
    high_face_u_upper = l_high + FHI * G_UPPER

    # A low-ATP phosphate boundary outside S on which glucose has no direct
    # authority: at A=0, U=0 for every finite G and growth is off.
    pi_stress_state = (Q(200), Q(0), Q("0.05"))
    f_stress, a_stress, p_stress = pi_stress_state
    l_stress = vlo(f_stress, a_stress, p_stress)
    pv_stress = p_vac(f_stress, a_stress, p_stress)
    pi_stress_margin = (-2 * l_stress + KATP * a_stress
                        + KP * (pv_stress - p_stress))

    # Verify the CellML fourth-power expression cost away from the reference
    # genotype too; the imbalanced-cell parameter is not a fixed rounded 2.63.
    ref_cost_sum = sum(x ** 4 for x in
                       (Q(10), Q(10), Q(10), Q("0.3")))
    ic_base = tuple(map(Q, ("10.92211", "5.65143", "4.82003", "2.07099")))
    def expression_cost(theta):
        return VATPER * sum(x ** 4 for x in theta) / ref_cost_sum
    ic_cost = expression_cost(ic_base)
    corner_costs = []
    for signs in product((-1, 1), repeat=4):
        theta = tuple(x * (1 + Q("0.1") * sign)
                      for x, sign in zip(ic_base, signs))
        corner_costs.append(expression_cost(theta))

    # Sensing delay certificate for F-only stale state, with A/P and all other
    # parameters/actuation exact.  |e_delay| <= (1+sup dL/dF)*sup|Fdot|*tau.
    l_f_bound = (VL / (1 + FLO) ** 2
                 * (ATOT - ALO) / (KMADP + ATOT - ALO)
                 * (SUMHI - ALO) / (KMP + SUMHI - ALO))
    f_speed_bound = max(FHI - 2 + EPS + FHI * G_UPPER,
                        2 - FLO + EPS)
    delay_gain = (1 + l_f_bound) * f_speed_bound
    delay_max = EPS / delay_gain

    # Sum-face parameter boundary: with |e|<=eps, source kp must satisfy
    # 0.4+2 eps - 2.5 kp <= 0; at eps=.17 this means kp>=.296.
    # The required condition is kp >= (0.4+2eps)/(2.5), where
    # 0.4=2(Fhi-2) and 2.5=14-Ahi-Pvmax.
    kp_required = (Q("0.4") + 2 * EPS) / (SUMHI - AHI - PV_MAX)
    assert kp_required == Q("0.296")

    data = {
        "model": "PLOS 2021 CellML source-reference genotype, full H-gated growth/dilution",
        "source_parameter_facts": {
            "enzyme_expression_cost_vatpe": "5 exactly at source reference genotype (CellML n=4 formula)",
            "IC_Table_2_vatpe_exact": show(ic_cost),
            "IC_Table_2_vatpe_pm10_corner_range": [show(min(corner_costs)), show(max(corner_costs))],
            "PLOS_2021_CellML_default_F_A_P_mM": ["2", "1", "10.4"],
            "cross_source_2014_failure_reconstruction_F_A_P_mM": ["2", "1", "9.4"],
            "growth_law": "g=0 unless H>=Hmax and 10*A-5>0; otherwise g=(ln 2/693)*(10*A-5)",
            "health_law_on_tube": "A>=0.5 implies 10*A-5>=0; Hdot=0 at equality and Hdot>=0 above it",
            "growth_upper_on_S": "g < 7/693 per min using ln(2)<0.7",
            "feedback_error_bound_mM_per_min": show(EPS),
            "feedback": "U=L-(F-2)+e",
        },
        "full_growth_face_upper_lower_bounds_mM_per_min": {
            "F=1.8_minimum_strictly_above": show(f_lower),
            "F=2.2_maximum": show(f_upper),
            "A=0.5_minimum": show(a_lower),
            "A=1.5_maximum_ignoring_helpful_dilution": show(a_upper),
            "P=2_minimum": show(pi_lower),
            "A_plus_P=14_maximum_ignoring_helpful_dilution": show(sum_upper),
            "whole_tube_Pvac_lower_bound": show(pv_min),
        },
        "inverse_glucose_feasibility": {
            "lower_flux_command_bound": show(u_min),
            "upper_flux_command_bound": show(u_max),
            "minimum_uptake_saturation_capacity": show(cu_min),
            "uniform_saturation_gap": show(saturation_gap),
            "conservative_G_upper_mM": show(glucose_max),
            "published_failure_start_G_at_e_zero_mM": show(
                KMG * vlo(Q(2), Q(1), Q("9.4")) /
                (uptake_capacity(Q(1)) - vlo(Q(2), Q(1), Q("9.4")))
            ),
        },
        "shared_glucose_impossibility": {
            "low_F_cell_state_F_A_P": list(map(str, x_low)),
            "high_F_cell_state_F_A_P": list(map(str, x_high)),
            "lower_face_requires_U_low_at_least": show(l_low),
            "common_G_implies_U_high_over_U_low": show(ratio),
            "therefore_U_high_at_least": show(common_u_high_lower),
            "upper_face_allows_U_high_at_most": show(high_face_u_upper),
            "strict_conflict": common_u_high_lower > high_face_u_upper,
        },
        "uncontrollable_low_ATP_Pi_face": {
            "state_F_A_P": list(map(str, pi_stress_state)),
            "vacuolar_Pi": show(pv_stress),
            "lower_flux": show(l_stress),
            "Pi_derivative_for_every_G": show(pi_stress_margin),
            "interpretation": "At ATP=0 the source uptake U is zero for every glucose concentration; ATPase expression demand exceeds ATP production, so growth is off. With fixed F=200 and P=0.05, Pi is decreasing for all glucose commands. For fixed A=0,P=0.05 the margin decreases with F because L increases and Pvac decreases, so every F>=200 has the same outward-face obstruction.",
        },
        "finite_bandwidth_bound": {
            "assumptions": "only F is delayed; A and P are current; exact source parameters and zero feed/estimation error otherwise",
            "sup_dL_dF_on_tube": show(l_f_bound),
            "sup_abs_Fdot_on_tube": show(f_speed_bound),
            "e_delay_per_minute_of_delay": show(delay_gain),
            "sufficient_F_measurement_to_actuation_delay_minutes": show(delay_max),
            "sufficient_delay_seconds": float(delay_max * 60),
            "general_budget": "(1+sup|dL/dF|)*sup|Fdot|*tau + other_flux_error <= 0.17 mM/min",
        },
        "parameter_boundary": {
            "minimum_effective_kp_for_sum_face_at_delta_0p17": show(kp_required),
            "source_kp": show(KP),
            "nominal_sum_face_margin_before_growth": show(-sum_upper),
            "kp_uncertainty_note": "No measured interval is supplied; a 1.33% downward shift from source kp=0.3 reaches the boundary.",
        },
        "scope": "Exact source-model facet calculations and a two-cell common-input counterexample. No biological validation, arbitrary-basin recovery, or robust measured parameter confidence set.",
    }

    assert f_lower > 0 and f_upper < 0
    assert a_lower > 0 and a_upper < 0 and pi_lower > 0 and sum_upper < 0
    assert KATP * ALO == VATPER and KATP * AHI > VATPER
    assert FLO <= Q(2) <= FHI and ALO <= Q(1) <= AHI and PLO <= Q("9.4")
    assert Q(1) + Q("9.4") <= SUMHI
    assert u_min > 0 and saturation_gap > 0
    assert common_u_high_lower > high_face_u_upper
    assert pi_stress_margin < 0
    assert KP > kp_required

    out = Path(__file__).with_name("full_growth_control_certificate.json")
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
