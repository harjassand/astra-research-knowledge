"""Conditional full-module screens; no fitted electrode or manufactured plant."""
import json
import math
from pathlib import Path

F = 96485.33212
R = 8.314462618
M_H2 = 0.00201588
M_NiOH2 = 0.09270808
Ah_kg = 2 * F / (3600 * M_H2)
q_DC = Ah_kg * 1.50 / 1000 / 0.995
q_AC = q_DC / 0.96
compression = R * 298.15 / M_H2 * math.log(30) / 3_600_000 / 0.65
heat_room = 45 - q_AC - compression
active_per_kg = 2 * M_NiOH2 / M_H2

thermal = []
for utilization in (1, 0.1):
    for effective_cp in (0.5, 4.0):
        gross = active_per_kg / utilization * effective_cp * 70 / 3600
        thermal.append({
            "introduced_redox_utilization": utilization,
            "introduced_total_heat_capacity_kJ_per_kg_active_K": effective_cp,
            "gross_25_to_95C_kWh_per_kg_H2": gross,
            "minimum_recuperation_if_all_remaining_budget_is_heat":
                max(0, 1 - heat_room / gross),
        })

rate_kg_h = 1000 / 24
rate_kg_y = 1000 * 365 * 0.90
power_kW = rate_kg_h * 45
r = 0.08
n = 20
crf = r * (1 + r)**n / ((1 + r)**n - 1)
maximum_capital = (2.0 - 45 * 0.02) * rate_kg_y / (crf + 0.03)

result = {
    "status": "CONDITIONAL_ANALYTIC_SCREEN_NOT_A_DEVICE",
    "hydrogen_Ah_per_kg": Ah_kg,
    "introduced_1point5V_99point5pct_charge_96pct_rectifier_AC_kWh_kg": q_AC,
    "introduced_isothermal_1_to_30bar_65pct_compressor_kWh_kg": compression,
    "remaining_kWh_kg_before_heat_auxiliaries_at_45target": heat_room,
    "hydroxide_kg_cycled_per_kg_H2_at_full_utilization": active_per_kg,
    "single_1kg_day_100s_charge_100s_regen_total_mean_A": 1000/M_H2/1000*2*F/86400,
    "total_area_m2_at_50mA_cm2_50pct_H2_duty_1kg_day":
        (2 * F / M_H2 / 86400) / (500 * 0.5),
    "thermal_cases": thermal,
    "one_tonne_day_45kWhkg_nameplate_power_kW": power_kW,
    "upper_capital_USD_at_2USDkg_20USDperMWh_3pct_annual_maintenance": maximum_capital,
    "upper_capital_USD_kW_before_other_opex_replacements": maximum_capital / power_kW,
    "P3_old_11point5_to_10kWhkg_cost_saving_USDkg": (11.5-10)*0.05,
    "P3_old_total_USDkg_if_initial_capital_recovery_free": 1.503 - 0.505,
    "limits": [
        "Introduced capacities, temperatures, heat capacities and efficiencies must coexist in real hardware.",
        "Effective heat capacity includes all switched support and entrained liquid per kg active mediator.",
        "Compression is a low-pressure reference, not added again to a pressurized cell terminal ledger.",
        "Remaining thermal budget excludes other auxiliaries, so recuperation thresholds are favorable.",
        "Capital bound grants no replacement, labor, site, water or disposal allowance; it is not a quote.",
        "No H2 thermochemical table or held NIST coefficients were used.",
    ],
}
p = Path(__file__).with_suffix('.json')
p.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
