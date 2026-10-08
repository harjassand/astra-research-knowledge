#!/usr/bin/env python3
"""Independent Fraction-arithmetic audit of the PLOS 2021 full-growth tube.

No imports from the C4 candidate calculator.  The source equations are
transcribed from sources/plos_2021_S1_Model.cellml.  The program audits both
the proposed S=(F:[1.8,2.2], A:[.3,1.5], Pi>=1, A+Pi<=14) and the viable-profit
sub-tube S+=(F:[1.8,2.2], A:[.5,1.5], Pi>=2, A+Pi<=14), under reference
genotype and actual-flux feedback.  It is a conditional model calculation.
"""

from fractions import Fraction as Q
import json
from pathlib import Path


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
VATPM = Q(0)
VATPRB = Q("12.7")
VATPRI = Q("0.46")
TAUG = Q(90)
TAUD = Q(420)
EPS = Q("0.17")
FLO, FHI = Q("1.8"), Q("2.2")
ALO_OLD, ALO = Q("0.3"), Q("0.5")
AHI = Q("1.5")
PLO_OLD, PLO = Q(1), Q(2)
SUMHI = Q(14)
G_UPPER = Q(7, 693)  # ln(2)<0.7 and max vatpg=10 mM/min on A<=1.5


def vlo(f, a, p, vl=VL):
    d = ATOT - a
    return vl * f / (KMF + f) * d / (KMADP + d) * p / (KMP + p)


def capacity(a, vu=VU):
    return vu * a / (KMATP + a * (1 + a / KIATP))


def pivac_from_total(ptot, kvac=KVAC):
    return PV_MAX / (1 + (ptot / kvac) ** 4)


def display(x):
    return {"fraction": f"{x.numerator}/{x.denominator}", "decimal": float(x)}


def glucose_for_flux(u, a):
    c = capacity(a)
    if not (0 < u < c):
        raise ValueError((u, c))
    return KMG * u / (c - u)


def main():
    # CellML source-derived growth and health signs.
    vatpgrb = VATPRB - VATPER - VATPM  # 7.7
    vatpgri = VATPRI - VATPER - VATPM  # -4.54
    ug_denominator = TAUG * vatpgrb   # 693
    ud = 1 / (TAUD * vatpgri)         # negative by construction
    h_coefficient = -ud               # positive, 5/9534 per flux unit

    # Reference genotype has the same fourth-power numerator and denominator.
    ref_sum4 = Q(10)**4 + Q(10)**4 + Q(10)**4 + Q("0.3")**4
    vatpe_reference = VATPER * ref_sum4 / ref_sum4

    # Distinct source Table 2 IC genotype, evaluated through the CellML cost.
    ic = tuple(map(Q, ("10.92211", "5.65143", "4.82003", "2.07099")))
    vatpe_ic = VATPER * sum((x**4 for x in ic), Q(0)) / ref_sum4
    ic_profit_threshold = vatpe_ic / ic[2]

    # Whole-tube bound used by the growth/dilution proof.
    ptot_max = SUMHI + 2 * FHI
    pv_min = pivac_from_total(ptot_max)

    # Original C4 candidate S, to reproduce its key face and lag figures.
    f_lower_old = (2 - FLO - EPS) - FLO * G_UPPER
    f_upper = 2 - FHI + EPS
    l_f_old = (VL * KMF / (KMF + FLO)**2
               * (ATOT - ALO_OLD) / (KMADP + ATOT - ALO_OLD)
               * (SUMHI - ALO_OLD) / (KMP + SUMHI - ALO_OLD))

    # Viable-profit sub-tube S+: A>=0.5 ensures vatpg=10A-5>=0 at reference
    # genotype, and Pi>=2 is the stronger phosphate floor requested for audit.
    a_lower = (2 * vlo(FLO, ALO, PLO) + 2 * (FLO - 2)
               - 2 * EPS - KATP * ALO)
    a_upper = (2 * vlo(FHI, AHI, SUMHI - AHI)
               + 2 * (FHI - 2) + 2 * EPS - KATP * AHI)
    # At Pi=2 use independently worst-case L, ATP, phosphate exchange and
    # growth dilution bounds.  This intentionally sacrifices sharpness.
    pi_lower = (-2 * vlo(FHI, ALO, PLO) + KATP * ALO
                + KP * (pv_min - PLO) - PLO * G_UPPER)
    sum_upper = (2 * (FHI - 2) + 2 * EPS
                 + KP * (PV_MAX - (SUMHI - AHI)))

    # Static external-glucose inversion on S+.
    l_min = vlo(FLO, AHI, PLO)
    l_max = vlo(FHI, ALO, SUMHI - ALO)
    u_min = l_min - (FHI - 2) - EPS
    u_max = l_max + (FHI - 2) + EPS
    # C'(A) has the sign of .1-A^2/3; its minimum on [.5,1.5] is at an endpoint.
    c_min = min(capacity(ALO), capacity(AHI))
    saturation_gap = c_min - u_max
    glucose_max = KMG * u_max / saturation_gap

    # Shared-culture glucose no-go still holds on S+.
    x_low = (FLO, ALO, SUMHI - ALO)       # vatpg=0, so g=0
    x_high = (FHI, AHI, PLO)               # generous g<=G_UPPER
    l_low = vlo(*x_low)
    l_high = vlo(*x_high)
    uptake_ratio = capacity(AHI) / capacity(ALO)
    common_u_high_min = uptake_ratio * l_low
    common_u_high_max = l_high + FHI * G_UPPER

    # F-only stale measurement certificate.  It assumes current exact A/P,
    # exact parameters, and instantaneous flux inversion/actuation.
    l_f_new = (VL * KMF / (KMF + FLO)**2
               * (ATOT - ALO) / (KMADP + ATOT - ALO)
               * (SUMHI - ALO) / (KMP + SUMHI - ALO))
    f_speed = max(FHI - 2 + EPS + FHI * G_UPPER,
                  2 - FLO + EPS)
    delay_gain_old = (1 + l_f_old) * f_speed
    delay_old = EPS / delay_gain_old
    delay_gain_new = (1 + l_f_new) * f_speed
    delay_new = EPS / delay_gain_new

    # Health reserve: for P>=2 and .3<=A<=.5, A-dot is bounded below by its
    # minimum at A=.5, F=1.8, Pi=2, e=+.17.  Health loss is then bounded over
    # the finite crossing time from A=.3 to .5.
    a_rise_min = a_lower
    crossing_time = (Q("0.5") - ALO_OLD) / a_rise_min
    max_health_decay = h_coefficient * Q(2)  # max deficit at A=.3: vatpg=-2
    h_loss = crossing_time * max_health_decay

    # Source starts are distinct.  2014 Fig.4 varies Pi=10.4/9.4 in a
    # three-state core model; 2021 CellML defaults are F=2,A=1,Pi=10.4,H=Hmax
    # and comments that Pi=7 gives imbalanced dynamics.  Flux inversion at
    # F=2,e=0 gives U=L and hence these external glucose settings.
    source_starts = {}
    for label, pi0 in (("2014_Fig4_imbalanced_start", Q("9.4")),
                       ("2021_CellML_imbalanced_comment", Q(7)),
                       ("2021_CellML_default_balanced", Q("10.4"))):
        u0 = vlo(Q(2), Q(1), pi0)
        source_starts[label] = {
            "metabolite_triple_F_A_P": ["2", "1", str(pi0)],
            "zero_error_external_glucose_mM": display(glucose_for_flux(u0, Q(1))),
        }

    assert vatpe_reference == Q(5)
    assert vatpgri == Q("-4.54") and ud < 0 and h_coefficient > 0
    assert f_lower_old == Q(13, 1100) and f_upper == Q(-3, 100)
    assert a_lower > 0 and a_upper < 0 and pi_lower > 0 and sum_upper < 0
    assert u_min > 0 and saturation_gap > 0
    assert common_u_high_min > common_u_high_max
    assert h_loss < 1

    data = {
        "status": "independent exact-rational model audit; not biological validation",
        "source_file": "work/agents/c4_rational_applications/sources/plos_2021_S1_Model.cellml",
        "controller": "U=L-(F-2)+e, |e|<=0.17 mM/min, actual upper flux",
        "reference_genotype": {
            "Vmaxup": "10", "Vmaxlo": "10", "katp": "10", "kp": "0.3",
            "vatpe_from_CellML_fourth_power_cost": display(vatpe_reference),
            "vatpg": "10*A-5 mM/min",
            "g_rule": "g=ug*vatpg only when H>=Hmax and vatpg>0; otherwise g=0",
            "ug": "ln(2)/693 per (mM/min)",
            "g_upper_on_A_le_1p5": display(G_UPPER),
        },
        "health_and_dilution_sign_audit": {
            "vatpgri=vatpri-(vatper+vatpm)": display(vatpgri),
            "ud=1/(taud*vatpgri)": display(ud),
            "Hdot_when_vatpg_le_0": "-ud*vatpg=(5/9534)*(10*A-5), negative for A<0.5",
            "Hdot_when_positive_surplus_and_H_below_Hmax": "ug*vatpg >= 0",
            "Hdot_when_positive_surplus_and_H_at_or_above_Hmax": "0",
            "Vdot": "g*V; g is never negative",
            "metabolite_dilution": "-F*g, -A*g, -Pi*g (all nonpositive)",
            "small_H_counterexample_in_original_S": {
                "state": "F=1.8,A=0.3,Pi=2,H=epsilon_H>0; e=0",
                "vatpg": "-2 mM/min",
                "Hdot": display(-Q(10, 9534)),
                "conclusion": "for sufficiently small positive H the source H=0 death boundary is reached while the metabolite state remains locally inside the tube; the original S alone is not an all-H viability certificate",
            },
            "Hmax_reserve_transient_for_Pi_ge_2": {
                "A_dot_lower_on_0p3_to_0p5": display(a_rise_min),
                "time_to_A_0p5_upper_min": display(crossing_time),
                "max_health_loss_bound_from_H0_equals_Hmax": display(h_loss),
                "H_lower_bound_if_Hmax_1": display(1 - h_loss),
                "assumptions": "reference genotype, Pi>=2, state starts within the full certified metabolic tube, feedback error<=0.17, H0=Hmax; after A>=0.5 H cannot decline",
            },
        },
        "facet_bounds_for_H_safe_subtube_Splus": {
            "Splus": "1.8<=F<=2.2, 0.5<=A<=1.5, Pi>=2, A+Pi<=14",
            "F_lower_minimum": display(f_lower_old),
            "F_upper_maximum": display(f_upper),
            "ATP_lower_minimum": display(a_lower),
            "ATP_upper_maximum_ignoring_helpful_dilution": display(a_upper),
            "Pi_lower_minimum_conservative": display(pi_lower),
            "A_plus_Pi_upper_maximum_ignoring_helpful_dilution": display(sum_upper),
            "whole_tube_Pivac_lower": display(pv_min),
            "growth_profit_on_Splus": "vatpg=10*A-5>=0; therefore Hdot>=0 for 0<=H<=Hmax and H cannot fall to zero from H0>0",
            "initial_failure_mapping": "(F,A,Pi)=(2,1,9.4) and (2,1,7) both lie in Splus; 2021 CellML adds H=Hmax and V=3.35e-15 L, and assumes feedback is active from glucose-onset",
        },
        "static_glucose_inversion_on_Splus": {
            "command_lower": display(u_min),
            "command_upper": display(u_max),
            "minimum_saturation_capacity": display(c_min),
            "uniform_saturation_gap": display(saturation_gap),
            "conservative_G_upper_mM": display(glucose_max),
        },
        "shared_glucose_no_go_on_Splus": {
            "low_F_state": [str(x) for x in x_low],
            "high_F_state": [str(x) for x in x_high],
            "common_input_Uhigh_over_Ulow": display(uptake_ratio),
            "low_face_requires_Ulow_at_least": display(l_low),
            "therefore_Uhigh_at_least": display(common_u_high_min),
            "high_face_allows_Uhigh_at_most_even_using_gmax": display(common_u_high_max),
            "strict_conflict": common_u_high_min > common_u_high_max,
        },
        "delay_audit": {
            "original_S_Lipschitz_dL_dF": display(l_f_old),
            "Splus_Lipschitz_dL_dF": display(l_f_new),
            "sup_abs_Fdot_given_total_flux_error_le_0p17": display(f_speed),
            "original_S_flux_error_gain_per_min_delay": display(delay_gain_old),
            "original_S_sufficient_delay_seconds": float(delay_old * 60),
            "Splus_sufficient_delay_seconds": float(delay_new * 60),
            "validity": "conditional first-exit/bootstrapped bound when the F sample age is tau, A/P are current, exact parameters and glucose inversion are known, and actuator dynamics/additional flux errors are zero; otherwise remaining error budget is below 0.17 and tau must shrink proportionally",
        },
        "genotype_boundary": {
            "IC_Table2_genotype": {
                "Vmaxup": str(ic[0]), "Vmaxlo": str(ic[1]),
                "katp": str(ic[2]), "kp": str(ic[3]),
                "CellML_fourth_power_vatpe": display(vatpe_ic),
                "ATP_threshold_for_nonnegative_vatpg": display(ic_profit_threshold),
                "published_rounded_cost": "2.63 mM/min",
            },
            "scope": "The Splus H-nondepletion argument and all face numbers above are for the source-reference genotype, not the distinct IC Table 2 genotype.",
            "effective_kp_boundary_for_sum_face_at_delta_0p17": display(Q("0.296")),
            "reference_kp": display(KP),
            "downward_fraction_to_boundary": display((KP - Q("0.296")) / KP),
        },
        "source_failure_scope": {
            "2014_Science_Fig4": "generalized three-metabolite core model; panels differ only in initial Pi 10.4 vs 9.4 mM; no H or cell-volume state",
            "2021_PLOS_CellML": "expanded FBP/ATP/Pi plus glucose, H and volume; defaults (F,A,Pi)=(2,1,10.4), H=Hmax=1; source comment says lowering Pi, e.g. to 7, produces imbalanced dynamics",
            "certificate_covers": "the mapped 2014 metabolite triple under the 2021 expanded equations after immediate feedback is applied, and directly includes the 2021 Pi=7 example state; it does not prove recovery from an already developed high-FBP/low-ATP/low-Pi collapsed state",
            "starts": source_starts,
        },
    }

    out = Path(__file__).with_name("FULL_GROWTH_AUDIT.json")
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
