"""Conditional full-cycle, cost and iron-electrode geometry screens.

Not a cell model, performance measurement, commodity quote or plant design.
"""
import json
import math

F = 96485.33212
MFE = .055845


def main():
    q_theory = 2 * F / MFE / 3600  # declared Fe/Fe(OH)2 two-electron window
    eta_c, eta_d, eta_q, eta_hold, eta_aux = .97, .97, .98, .99, .98
    voltage_prefactor = eta_c * eta_d * eta_q * eta_hold * eta_aux
    crf = .08 / (1 - 1.08**-20)
    cycle_hours = 100 + 144 + 100
    cycles_year = 8760 * .9 / cycle_hours
    cases = []
    for current_density in [10., 100.]:  # A/m2 = 1 and 10mA/cm2
        vd, utilization = .9, .2
        area = 100000 / (eta_d * eta_aux * vd * current_density)
        mass_areal = current_density * 100 / (q_theory * utilization * eta_hold)
        mass = mass_areal * area
        thickness = mass_areal / (7860 * .5)  # hypothetical 50% Fe volume fraction
        conductivity = 10.  # hypothetical effective S/m, NOT a KOH datum
        cases.append(dict(current_A_m2=current_density, current_mA_cm2=current_density/10,
            area_m2_at_100kW=area, Fe_kg_per_m2=mass_areal,
            Fe_kg_at_10MWh_useful_output=mass,
            hypothetical_bed_thickness_m=thickness,
            hypothetical_ohmic_drop_V=current_density * thickness / conductivity,
            Fe_cost_USD_per_useful_kWh_at_unquoted_1USDkg=mass/10000,
            area_cost_USD_per_useful_kWh_at_unquoted_10USDm2=area*10/10000))
    out = {
        "scope": "Conditional energy/cost screens, no supplied material or storage device.",
        "cycle_hours": cycle_hours,
        "maximum_full_cycles_per_year_at_90pct_availability": cycles_year,
        "Fe_two_electron_theoretical_Ah_per_kg": q_theory,
        "hypothetical_voltage_efficiency_prefactor": voltage_prefactor,
        "maximum_charge_discharge_voltage_ratio_for_65pct_full_RTE": voltage_prefactor/.65,
        "maximum_mean_charge_voltage_if_discharge_0.9V": .9*voltage_prefactor/.65,
        "qualification_efficiency": "The factors must coexist in a real full device; electrode-only Coulombic efficiency supplies none of the others.",
        "geometry_cases": cases,
        "financial_screen": {
            "capital_recovery_factor_8pct_20yr": crf,
            "initial_capital_USD_per_MWh_delivered_at_15USDusablekWh": 15000*crf/cycles_year,
            "annual_maintenance_2pct_capital_USD_per_MWh_delivered": 15000*.02/cycles_year,
            "charging_USD_per_MWh_delivered_20USDinput_65pctRTE": 20/.65,
            "charging_USD_per_MWh_delivered_40USDinput_65pctRTE": 40/.65,
            "subtotal_20USD_charging_BEFORE_replacement_calendar_fade_other_OM":
                15000*(crf+.02)/cycles_year+20/.65,
            "qualification": "No firm quote, lifetime or complete levelized-cost pass is established.",
        },
        "heat_engine_bookkeeping": {
            "conditional_base_cost_USD_per_100W": 183.04,
            "if_insulation_47.23USD_free_and_engine_61.82USD_halved": 183.04-47.23-61.82/2,
            "35pct_heat_margin_W_at_100W_and_285.620W_input": 100/.35-285.620,
            "withdrawal_break_even_idle_heat_daily_W_with_200Wh_restart_14h_and_1W_OFF": 1+200/14,
            "withdrawal_break_even_idle_heat_long_W_with_200Wh_restart_144h_and_1W_OFF": 1+200/144,
            "qualification": "Simplified thresholds omit paid actuator/electrical/other heat terms; the producer's more complete thresholds are15.84W/2.49W.",
        },
    }
    print(json.dumps(out, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
