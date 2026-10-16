#!/usr/bin/env python3
"""Recalculate published aggregates; this is NOT a raw-data replication.

Python 3.10+, standard library only. Source values are transcribed from the
2025 author preprint and 2026 supplementary information, kept version-separated.
The flux interpretation is conditional on flow normalization and the stated
C2-only reaction network. No uncertainty estimate is inferred from rounding.
"""
from __future__ import annotations
import csv
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FARADAY = 96485.33212  # C/mol; numerical constant, adequate for these rounded data.
M_PD = 106.42         # g/mol; conventional atomic weight used for inventory count.


def fluxes(x: float, s: float) -> dict[str, float]:
    """Normalize C2H2 consumption and C2H6 production to incoming C2H2.

    Assumes X is a molar-flow conversion and S=a/(a+b), with no side-product
    carbon loss. Negative net ethylene production is permitted in a co-feed.
    """
    if not (0 <= x <= 1 and 0 < s <= 1):
        raise ValueError("Require conversion in [0,1] and selectivity in (0,1].")
    b = x * (1 / s - 1)
    return {"conversion": x, "paper_selectivity": s,
            "ethane_per_incoming_acetylene": b,
            "net_ethylene_per_consumed_acetylene": 2 - 1 / s,
            "net_ethylene_per_incoming_acetylene": x - b}


def concentration_sensitivity(x: float, s: float, inlet_a_fraction: float = .01) -> dict[str, float]:
    """Alternative scenario: printed concentrations are literal mole fractions.

    Assume zero incoming ethane, only A+H2->B and B+H2->C, ideal gases,
    no leaks/storage/side reactions. Solve total-flow contraction exactly.
    This is a sensitivity scenario, not a correction established from raw data.
    """
    fluxes(x, s)  # validation
    if not 0 < inlet_a_fraction < 1:
        raise ValueError("Inlet acetylene fraction must lie in (0,1).")
    yaout = inlet_a_fraction * (1 - x)
    ycout = inlet_a_fraction * x * (1 / s - 1)
    flow_ratio = (1 - inlet_a_fraction) / (1 - yaout + ycout)
    true_x = 1 - flow_ratio * (1 - x)
    b = flow_ratio * x * (1 / s - 1)
    return {"outlet_to_inlet_total_molar_flow": flow_ratio,
            "conversion": true_x,
            "ethane_per_incoming_acetylene": b,
            "net_ethylene_per_incoming_acetylene": true_x - b}


def run() -> dict[str, Any]:
    # Baseline and optimal point from PREPRINT v1, not digitized from final heatmap.
    # Static-positive point is reconstructed from stated percentage-point shifts.
    x0, s0 = .894, .351
    xp, sp = x0 - .086, s0 + .126
    xd, sd = .810, .805
    data = {"preprint_no_applied_voltage": fluxes(x0, s0),
            "preprint_static_positive": fluxes(xp, sp),
            "preprint_optimal_dynamic_10s_0p1s": fluxes(xd, sd),
            "SI_separate_dynamic_10s_1s": fluxes(.810, .783)}
    plus = data["preprint_static_positive"]["ethane_per_incoming_acetylene"]
    dyn = data["preprint_optimal_dynamic_10s_0p1s"]["ethane_per_incoming_acetylene"]
    tp, tm = 10.0, .1
    period = tp + tm
    ratio = dyn / plus
    # Positivity alone gives the bound on the positive-phase mean. These are
    # source-conditional inferences, not measured time-resolved kinetics.
    phase_bound = period / tp * ratio
    suppression_eq = tp - period * ratio
    mass_pd_g = .010 * .01  # 10 mg of 1 wt% Pd/AC
    n_pd = mass_pd_g / M_PD
    activity = 9.918  # mol acetylene / gPd / h; 2026 SI Table 1
    actual_a_rate = activity * mass_pd_g / 3600
    a_in_rate = actual_a_rate / xd
    excess_avoided = a_in_rate * (tp * plus - period * dyn)
    # Allow no ethane production throughout the negative pulse; remaining
    # suppression still exceeds a single product molecule per total Pd atom.
    inventory_ratio = excess_avoided / n_pd

    # Published decimal-rounding scenario, NOT a confidence interval. Conservative
    # rectangular intervals include rounding of both baseline and quoted shifts.
    rlo = (.8095 * (1/.8055 - 1)) / (.809 * (1/.476 - 1))
    rhi = (.8105 * (1/.8045 - 1)) / (.807 * (1/.478 - 1))
    corrected = {key: concentration_sensitivity(v["conversion"], v["paper_selectivity"])
                 for key, v in data.items()}
    cp = corrected["preprint_static_positive"]["ethane_per_incoming_acetylene"]
    cd = corrected["preprint_optimal_dynamic_10s_0p1s"]["ethane_per_incoming_acetylene"]
    cr = cd / cp
    ca_in = actual_a_rate / corrected["preprint_optimal_dynamic_10s_0p1s"]["conversion"]
    c_inventory_ratio = ca_in * (tp*cp-period*cd)/n_pd

    # Separate SI 10s/1s illustration: do not silently substitute for 10s/0.1s.
    a0, b0, ad, bd = 1.81e-5, 3.35e-5, 1.65e-5, .40e-5  # mol/min
    eq_mA = 2 * FARADAY * (abs(ad-a0)+abs(bd-b0))/60*1000
    current_A = .00441
    charge_equiv = current_A*10/FARADAY/n_pd
    result = {
        "status": "published_aggregate_recalculation_not_raw_replication",
        "rows": data,
        "conditional_dynamic_test": {
            "negative_duty_fraction": tm/period,
            "ethane_dynamic_to_static_positive_ratio": ratio,
            "memoryless_lower_bound_ratio": tp/period,
            "positive_phase_mean_ratio_upper_bound": phase_bound,
            "suppression_equivalent_seconds_not_a_measured_lifetime": suppression_eq,
            "total_Pd_inventory_mol": n_pd,
            "author_activity_acetylene_consumption_mol_s": actual_a_rate,
            "inferred_acetylene_feed_mol_s": a_in_rate,
            "extra_avoided_ethane_mol_per_cycle_beyond_zero_negative_phase": excess_avoided,
            "extra_avoided_events_per_total_Pd_atom": inventory_ratio,
            "single_molecule_per_Pd_purge_null_excluded_conditionally": inventory_ratio > 1,
            "required_assumptions": [
                "Preprint endpoints and dynamic point share reactor, feed, specimen class and calibration.",
                "Reported aggregate values represent reproducible periodic/steady operation, not drift or sampling artifacts.",
                "Flux reconstruction uses corrected common flow and C2-only chemistry; sensitivity scenario is provided separately.",
                "Phase-resolved ethane production is nonnegative and integrated storage is closed over a period.",
                "The pure-purge null permits at most one cleared product per TOTAL Pd atom, no larger support reservoir, and no persistent influence on subsequent turnovers.",
                "No claim is made that the state is specifically electronic, located only at Pd, or historically novel."
            ]},
        "decimal_rounding_only_not_statistical_uncertainty": {
            "ratio_range": [rlo,rhi],
            "suppression_equivalent_seconds_range": [tp-period*rhi,tp-period*rlo]},
        "ideal_two_step_flow_contraction_sensitivity": {
            "rows": corrected, "ethane_ratio": cr,
            "suppression_equivalent_seconds": tp-period*cr,
            "avoided_events_per_total_Pd": c_inventory_ratio,
            "status": "hypothetical_exact_stoichiometric_correction_not_raw_flow_validation"},
        "SI_separate_illustration_audit": {
            "SI_reported_selectivity": .783,
            "selectivity_implied_by_SI_printed_rates": ad/(ad+bd),
            "SI_reported_equivalent_current_mA": 95.04,
            "equivalent_current_from_printed_rate_changes_mA": eq_mA,
            "steady_positive_current_mA_excluding_transients": 4.41,
            "10s_current_scale_electrons_per_total_Pd_atom": charge_equiv,
            "qualification": "Charge scale only: 4.41 mA is not a measured whole-cycle integral and electrons do not identify hydrogen uptake."},
        "carbon_accounting": {
            "total_C2_feed_to_acetylene_feed_ratio": 21,
            "one_percent_total_carbon_gap_in_acetylene_feed_equivalents": .01*21,
            "one_point_four_percent_gap_in_acetylene_feed_equivalents": .014*21,
            "qualification": "Closure deficits are NOT calibrated uncertainty intervals; oscillating SI row has no duration identity in Table 2."},
        "technology": {
            "approx_residual_acetylene_ppm_at_81_percent_conversion_from_1_percent": 1e4*(1-.81),
            "conversion_required_from_1_percent_to_1ppm_ignoring_flow_contraction": 1-1/1e4,
            "author_net_productivity_mol_gPd_h": 7.525,
            "author_productivity_to_activity_ratio": 7.525/9.918,
            "net_ethylene_g_h_for_0p1mg_Pd": 7.525*mass_pd_g*28.05,
            "net_ethylene_g_m2_h_for_preprint_5cm2_area": 7.525*mass_pd_g*28.05/(5e-4),
            "qualification": "Net ethylene added is not total purified co-feed throughput; no lifetime/scale or comparative cost claim."}
    }
    # Numerical identity checks, not empirical validation.
    assert math.isclose(sp, .477, abs_tol=1e-12)
    assert math.isclose(xp, .808, abs_tol=1e-12)
    assert math.isclose(fluxes(.81,.5)["net_ethylene_per_incoming_acetylene"],0,abs_tol=1e-12)
    assert math.isclose(fluxes(.81,1)["net_ethylene_per_incoming_acetylene"],.81)
    assert 0 < rlo <= ratio <= rhi < tp/period
    assert suppression_eq > 7 and 2 < inventory_ratio < 3
    assert .21 < cr < .24 and 2 < c_inventory_ratio < 3
    assert not math.isclose(ad/(ad+bd),.783,abs_tol=.001)
    assert 99 < eq_mA < 101
    assert .48 < charge_equiv < .49
    assert data["preprint_no_applied_voltage"]["net_ethylene_per_incoming_acetylene"] < 0
    assert data["preprint_optimal_dynamic_10s_0p1s"]["net_ethylene_per_incoming_acetylene"] > 0
    return result


if __name__ == "__main__":
    results = run()
    (ROOT/"results.json").write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
    rows = [{"condition": name, **v} for name,v in results["rows"].items()]
    with (ROOT/"derived_fluxes.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps(results["conditional_dynamic_test"],indent=2))
    print("Numerical consistency checks passed. No physical experiment or raw-data validation performed.")
