#!/usr/bin/env python3
"""Reproduce stoichiometric ceiling and capture-fraction sensitivity."""

LA_ATOMIC_MASS = 138.90547
MG_ATOMIC_MASS = 24.305

# Ji Supplementary Fig. 10: 2.5 wt% of Mg-1 wt% La master alloy.
master_alloy_wt_percent = 2.5
la_wt_percent = master_alloy_wt_percent * 0.01
mg_wt_percent = master_alloy_wt_percent * 0.99
la_mass_fraction_in_lamg3 = LA_ATOMIC_MASS / (LA_ATOMIC_MASS + 3 * MG_ATOMIC_MASS)
max_lamg3_wt_percent = la_wt_percent / la_mass_fraction_in_lamg3

capture_rows = []
for eta in (1.0, 0.1, 0.01):
    # Under the same spherical-particle/gap/creep model, f_eff=eta*f;
    # the no-initial-coverage Vema critical height/capacity scales as 1/f_eff.
    capture_rows.append({
        "eta": eta,
        "effective_fraction_relative_to_full_capture": eta,
        "critical_capacity_multiplier_vs_eta_1": 1 / eta,
    })

assert abs(la_wt_percent - 0.025) < 1e-12
assert abs(mg_wt_percent - 2.475) < 1e-12
assert 0.0380 < max_lamg3_wt_percent < 0.0383
assert capture_rows[1]["critical_capacity_multiplier_vs_eta_1"] == 10
assert capture_rows[2]["critical_capacity_multiplier_vs_eta_1"] == 100

print({
    "nominal_master_alloy_wt_percent": master_alloy_wt_percent,
    "nominal_La_wt_percent": la_wt_percent,
    "nominal_Mg_wt_percent": mg_wt_percent,
    "La_mass_fraction_in_LaMg3": la_mass_fraction_in_lamg3,
    "maximum_LaMg3_wt_percent_if_all_La_in_LaMg3": max_lamg3_wt_percent,
    "warning": "Mass percentage is not Vema's impurity volume fraction f.",
    "capture_sensitivity": capture_rows,
    "eta_zero": "No Vema-like contact-capacity gate in this model if no phase is captured in a blocking state.",
})
