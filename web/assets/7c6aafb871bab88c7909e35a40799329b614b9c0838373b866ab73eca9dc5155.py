#!/usr/bin/env python3
"""Exact rational ensemble-feed and genotype-specific tube audit.

This is a source-model certificate for the PLOS 2021 CellML glycolysis model.
All decimal Table 2 values are treated as exact rationals at their published
precision.  The only transcendental estimate is ln(2) < 7/10.  The script
does not validate those genotype values against living cells.
"""

from fractions import Fraction as Q
import json
from pathlib import Path


REF = {
    "Vmaxup": Q(10), "Vmaxlo": Q(10), "katp": Q(10), "kp": Q("0.3")
}
GENOTYPES = {
    # PLOS 2021 Table 2 values, used in its no-mutation BC/IC coexistence
    # simulations.  These are model-selected genotypes, not measured strains.
    "BC": {
        "Vmaxup": Q("9.90956"), "Vmaxlo": Q("6.97388"),
        "katp": Q("6.14105"), "kp": Q("1.27357")
    },
    "IC": {
        "Vmaxup": Q("10.92211"), "Vmaxlo": Q("5.65143"),
        "katp": Q("4.82003"), "kp": Q("2.07099")
    },
}

F_LO, F_HI = Q("1.8"), Q("2.2")
A_LO, A_HI = Q("0.585"), Q("1.5")
P_LO, AP_HI = Q(2), Q(14)
DELTA = Q("0.15")
LN2_UB = Q("0.7")
KM_GLC, KM_ATP, KI_ATP = Q("0.1"), Q("0.1"), Q(3)
ATOT, KM_FBP, KM_ADP, KM_PI = Q(5), Q(1), Q("0.1"), Q(2)
PIVAC_MAX, K_VAC = Q(10), Q(250)
VATP_RB, TAU_G = Q("12.7"), Q(90)
VATP_RI, TAU_D = Q("0.46"), Q(420)
VATP_ER, VATP_MAINT = Q(5), Q(0)


def frac(x):
    return {"fraction": f"{x.numerator}/{x.denominator}", "decimal": float(x)}


def rate_capacity(a):
    return a / (KM_ATP + a * (1 + a / KI_ATP))


def lower_flux(q, f, a, p):
    d = ATOT - a
    return q["Vmaxlo"] * f / (KM_FBP + f) * d / (KM_ADP + d) * p / (KM_PI + p)


def vac_pi(f, a, p):
    ptot = p + 2 * f + a
    return PIVAC_MAX / (1 + (ptot / K_VAC) ** 4)


def expression_cost(q):
    numerator = (q["Vmaxup"] ** 4 + q["Vmaxlo"] ** 4
                 + q["katp"] ** 4 + q["kp"] ** 4)
    denominator = (REF["Vmaxup"] ** 4 + REF["Vmaxlo"] ** 4
                   + REF["katp"] ** 4 + REF["kp"] ** 4)
    return Q(5) * numerator / denominator


def growth_upper(q, a):
    """Upper bound on source g using ln(2)<0.7 and H<=Hmax."""
    cost = expression_cost(q)
    profit = q["katp"] * a - cost
    if profit <= 0:
        return Q(0)
    # CellML uses vatpgrb=vatprb-(vatper+vatpm) in ug.  vatper is fixed
    # at 5 even when genotype-dependent vatpe changes.
    return (LN2_UB * profit
            / (TAU_G * (VATP_RB - VATP_ER - VATP_MAINT)))


def uptake(q, a, glucose):
    return (q["Vmaxup"] * rate_capacity(a) * glucose
            / (KM_GLC + glucose))


def genotype_tube(q):
    """Exact inward bounds for the full-growth tube under actual-flux law.

    Tube: 1.8<=F<=2.2, 0.55<=A<=1.5, P>=2, A+P<=14.
    Actual U = L-(F-2)+e, |e|<=0.15 mM/min.
    """
    cost = expression_cost(q)
    threshold = cost / q["katp"]
    g_hi = growth_upper(q, A_HI)
    g_at_a_lo = growth_upper(q, A_LO)
    pv_lo = PIVAC_MAX / (1 + ((AP_HI + 2 * F_HI) / K_VAC) ** 4)

    # Signed positive values point inward.  Upper-face signs are negated.
    f_lower = Q(2) - F_LO - DELTA - F_LO * g_hi
    f_upper = F_HI - Q(2) - DELTA
    a_lower = (2 * lower_flux(q, F_LO, A_LO, P_LO)
               + 2 * (F_LO - 2) - 2 * DELTA
               - q["katp"] * A_LO - A_LO * g_at_a_lo)
    a_upper = (q["katp"] * A_HI
               - 2 * lower_flux(q, F_HI, A_HI, AP_HI - A_HI)
               - 2 * (F_HI - 2) - 2 * DELTA)
    p_lower = (-2 * lower_flux(q, F_HI, A_LO, P_LO)
               + q["katp"] * A_LO
               + q["kp"] * (pv_lo - P_LO) - P_LO * g_hi)
    sum_upper = (-2 * (F_HI - 2) - 2 * DELTA
                 - q["kp"] * (pv_lo - (AP_HI - A_LO)))

    # Uniform source-flux band U0 +/- DELTA across this tube.
    l_min = lower_flux(q, F_LO, A_HI, P_LO)
    l_max = lower_flux(q, F_HI, A_LO, AP_HI - A_LO)
    u_min = l_min - (F_HI - 2) - DELTA
    u_max = l_max + (F_HI - 2) + DELTA
    c_min = q["Vmaxup"] * min(rate_capacity(A_LO), rate_capacity(A_HI))
    sat_gap = c_min - u_max
    glucose_upper = KM_GLC * u_max / sat_gap

    # F-only stale-sensor bound; all other errors use the same DELTA budget.
    l_f_max = (q["Vmaxlo"] * (ATOT - A_LO) / (KM_ADP + ATOT - A_LO)
               * (AP_HI - A_LO) / (KM_PI + AP_HI - A_LO)
               / (1 + F_LO) ** 2)
    f_speed = max(F_LO * 0 + (2 - F_LO + DELTA),
                  F_HI - 2 + DELTA + F_HI * g_hi)
    delay_gain = (1 + l_f_max) * f_speed
    delay_max = DELTA / delay_gain

    faces = {
        "F_lower": f_lower,
        "F_upper_inward": f_upper,
        "ATP_lower": a_lower,
        "ATP_upper_inward": a_upper,
        "Pi_lower": p_lower,
        "ATP_plus_Pi_upper_inward": sum_upper,
    }
    assert threshold < A_LO
    assert all(x > 0 for x in faces.values()), (q, faces)
    assert u_min > 0 and sat_gap > 0
    assert c_min > u_max
    return {
        "expression_cost_vatpe": frac(cost),
        "ATP_profit_threshold_vatpe_over_katp_mM": frac(threshold),
        "ATP_profit_at_tube_floor_mM_per_min": frac(q["katp"] * A_LO - cost),
        "growth_upper_at_A_1p5_per_min": frac(g_hi),
        "tube": {
            "F_mM": [frac(F_LO), frac(F_HI)],
            "A_mM": [frac(A_LO), frac(A_HI)],
            "P_lower_mM": frac(P_LO),
            "A_plus_P_upper_mM": frac(AP_HI),
            "total_actual_upper_flux_error_mM_per_min": frac(DELTA),
        },
        "full_growth_inward_margins_mM_per_min": {
            k: frac(v) for k, v in faces.items()
        },
        "inverse_glucose_feasibility": {
            "actual_flux_lower_bound_mM_per_min": frac(u_min),
            "actual_flux_upper_bound_mM_per_min": frac(u_max),
            "minimum_saturated_uptake_capacity_mM_per_min": frac(c_min),
            "uptake_capacity_gap_mM_per_min": frac(sat_gap),
            "conservative_G_upper_mM": frac(glucose_upper),
        },
        "F_only_staleness_sufficient_bound": {
            "sup_dL_dF": frac(l_f_max),
            "sup_abs_Fdot_mM_per_min": frac(f_speed),
            "flux_error_per_minute_staleness_mM_per_min_squared": frac(delay_gain),
            "max_delay_minutes_if_other_errors_zero": frac(delay_max),
            "max_delay_seconds_if_other_errors_zero": float(60 * delay_max),
            "budget": "delay_gain*tau + all_other_flux_error <= 0.15 mM/min",
        },
    }


def collective_witness():
    """Opposing F-face constraints for the source BC and IC genotypes."""
    bc, ic = GENOTYPES["BC"], GENOTYPES["IC"]
    x_bc = {"F": Q("1.8"), "A": A_LO, "P": Q(7), "H": Q(1)}
    x_ic = {"F": Q("2.2"), "A": Q("0.6"), "P": Q(2), "H": Q(1)}
    cost_bc, cost_ic = expression_cost(bc), expression_cost(ic)
    profit_bc = bc["katp"] * x_bc["A"] - cost_bc
    profit_ic = ic["katp"] * x_ic["A"] - cost_ic
    assert profit_bc > 0 and profit_ic > 0

    # At F=F_lo, Fdot>=0 requires U>=L+Fg>=L; at F=F_hi,
    # Fdot<=0 requires U<=L+Fg<=L+F*g_upper.
    zeta_bc_min = (lower_flux(bc, x_bc["F"], x_bc["A"], x_bc["P"])
                   / (bc["Vmaxup"] * rate_capacity(x_bc["A"])))
    g_ic_upper = growth_upper(ic, x_ic["A"])
    zeta_ic_max = ((lower_flux(ic, x_ic["F"], x_ic["A"], x_ic["P"])
                    + x_ic["F"] * g_ic_upper)
                   / (ic["Vmaxup"] * rate_capacity(x_ic["A"])))
    assert zeta_bc_min > zeta_ic_max
    g_from_zeta = lambda z: KM_GLC * z / (1 - z)

    # Two explicitly distinct, source-external feed lanes satisfy the F-face
    # directions at the witness points.  They are not a full-basin theorem.
    g_bc, g_ic = Q("0.1"), Q("0.03")
    bc_fdot_lower = (uptake(bc, x_bc["A"], g_bc)
                     - lower_flux(bc, x_bc["F"], x_bc["A"], x_bc["P"])
                     - x_bc["F"] * growth_upper(bc, x_bc["A"]))
    bc_adot_lower = (-2 * uptake(bc, x_bc["A"], g_bc)
                     + 4 * lower_flux(bc, x_bc["F"], x_bc["A"], x_bc["P"])
                     - bc["katp"] * x_bc["A"]
                     - x_bc["A"] * growth_upper(bc, x_bc["A"]))
    ic_fdot_upper = (uptake(ic, x_ic["A"], g_ic)
                     - lower_flux(ic, x_ic["F"], x_ic["A"], x_ic["P"]))
    ic_pdot_lower = (-2 * lower_flux(ic, x_ic["F"], x_ic["A"], x_ic["P"])
                     + ic["katp"] * x_ic["A"]
                     + ic["kp"] * (vac_pi(x_ic["F"], x_ic["A"], x_ic["P"])
                                   - x_ic["P"])
                     - x_ic["P"] * growth_upper(ic, x_ic["A"]))
    assert (bc_fdot_lower > 0 and bc_adot_lower > 0
            and ic_fdot_upper < 0 and ic_pdot_lower > 0)

    return {
        "source_table2_genotypes": {
            key: {name: frac(value) for name, value in q.items()}
            for key, q in GENOTYPES.items()
        },
        "states_mM_Hmax": {
            "BC_on_lower_F_face": {k: frac(v) for k, v in x_bc.items()},
            "IC_on_upper_F_face": {k: frac(v) for k, v in x_ic.items()},
        },
        "health_gate": {
            "BC_expression_cost": frac(cost_bc),
            "BC_ATP_profit_threshold": frac(cost_bc / bc["katp"]),
            "BC_ATP_profit_at_witness": frac(profit_bc),
            "IC_expression_cost": frac(cost_ic),
            "IC_ATP_profit_threshold": frac(cost_ic / ic["katp"]),
            "IC_ATP_profit_at_witness": frac(profit_ic),
            "Hdot_at_Hmax_for_both": "0 under the source health law",
        },
        "saturation_zeta_G_over_0p1_plus_G": {
            "BC_lower_F_requires_at_least": frac(zeta_bc_min),
            "IC_upper_F_allows_at_most": frac(zeta_ic_max),
            "strict_disjointness_gap": frac(zeta_bc_min - zeta_ic_max),
            "BC_lower_bound_on_G_mM": frac(g_from_zeta(zeta_bc_min)),
            "IC_upper_bound_on_G_mM": frac(g_from_zeta(zeta_ic_max)),
            "no_common_G_even_time_varying": True,
        },
        "two_lane_local_direction_check": {
            "BC_G_mM": frac(g_bc),
            "BC_Fdot_lower_bound_mM_per_min": frac(bc_fdot_lower),
            "BC_Adot_lower_bound_mM_per_min": frac(bc_adot_lower),
            "IC_G_mM": frac(g_ic),
            "IC_Fdot_upper_bound_mM_per_min": frac(ic_fdot_upper),
            "IC_Pidot_lower_bound_mM_per_min": frac(ic_pdot_lower),
            "scope": "local facet directions at this two-cell witness only; not full recovery or long-term survival",
        },
    }


def main():
    data = {
        "source": "PLOS Computational Biology 17 (2021), e1008547, Table 2 and S1 CellML",
        "arithmetic_scope": "Exact Fraction arithmetic over published rounded Table 2 decimals; ln(2)<0.7 for growth upper bounds.",
        "ensemble_result": collective_witness(),
        "individually_addressable_health_safe_tubes": {
            name: genotype_tube(q) for name, q in GENOTYPES.items()
        },
        "scope": (
            "Source-model theorem and local collective-feed obstruction only. "
            "The Table 2 BC/IC genotypes were simulation-selected, not measured strains. "
            "No claim that the witness states co-occur in a living population, "
            "that the two-lane point command gives a basin guarantee, or that it "
            "outperforms trehalose/T6P regulation or optimized fixed glucose."
        ),
    }
    out = Path(__file__).with_name("collective_feed_certificate.json")
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
