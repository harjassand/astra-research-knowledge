"""ROOT derived balances; introduced salt thermodynamics and equipment inputs.
No producer code, external packages, actual membrane/ice qualification or quote.
"""
import json
import math
from pathlib import Path

R = 8.314462618
MW = 0.01801528
MS = 0.05844
TM = 273.15
LATENT = 333500.0  # J/kg, introduced constant over this diagnostic


def crf(rate=0.08, years=20):
    return rate / (1 - (1 + rate) ** -years)


def ideal_mixture_g(mass, salt_fraction, temp=298.15):
    nw = mass * (1 - salt_fraction) / MW
    ns = mass * salt_fraction / MS
    nt = nw + 2 * ns  # ideal complete NaCl dissociation, not actual activity
    return R * temp * sum(n * math.log(n / nt) for n in (nw, ns, ns) if n)


def freezing_kelvin(water_removed):
    nw = (1.8 - water_removed) / MW  # initial 2 kg 10wt% feed
    ns = 0.2 / MS
    aw = nw / (nw + 2 * ns)
    return 1 / (1 / TM - R * math.log(aw) / (LATENT * MW))


def phase_case(wash_fraction, carnot_fraction, approach, sensible_recovery=0.95):
    # Per 1 tonne NET product; diverted melt is internally refrozen.
    # This is an aggregate thermal-duty surrogate, not a wash-column solution.
    n = 2000
    inv_cop = sum((TM + approach - (freezing_kelvin((i + 0.5) / n) - approach)) /
                  (freezing_kelvin((i + 0.5) / n) - approach) for i in range(n)) / n
    gross_ice_per_net = 1 / (1 - wash_fraction)
    latent_kWh = LATENT * 1000 / 3_600_000 * gross_ice_per_net
    cold_sensible_kWh = (1 - sensible_recovery) * 2 * 1000 * 3800 * 35 / 3_600_000
    main_work = (latent_kWh + cold_sensible_kWh) * inv_cop / carnot_fraction
    # All excess low-temperature condenser heat is removed by a paid trim HP.
    # Ambient warming returns unrecuperated output sensible heat separately;
    # net ambient rejection equals total work, no double latent heat credit.
    trim_TL, trim_TH = TM + approach - 1, 313.15
    trim_cop = 0.5 * trim_TL / (trim_TH - trim_TL)
    excess_heat = cold_sensible_kWh + main_work
    trim_work = excess_heat / trim_cop
    aux = 0.75  # introduced all other duties; not a component map
    total = main_work + trim_work + aux
    return {
        "introduced_wash_melt_diversion_fraction": wash_fraction,
        "introduced_main_Carnot_fraction": carnot_fraction,
        "introduced_approach_each_K": approach,
        "introduced_sensible_recovery": sensible_recovery,
        "gross_ice_t_per_t_net": gross_ice_per_net,
        "latent_kWh_thermal_per_t_net": latent_kWh,
        "unrecovered_sensible_kWh_thermal_per_t_net": cold_sensible_kWh,
        "main_HP_kWh_per_t_net": main_work,
        "excess_low_temperature_heat_kWh_per_t_net": excess_heat,
        "trim_HP_COP_INTRODUCED": trim_cop,
        "trim_HP_kWh_per_t_net": trim_work,
        "other_aux_kWh_per_t_net_INTRODUCED": aux,
        "total_kWh_per_t_net_conditional": total,
    }


def main():
    rate = crf()
    # Unchanged displayed cooling ledger; not a universal price floor.
    cap, cost, cop = 47066, 210.59, 4.102
    cap_cost = cap * rate / 40
    energy_cost = 80 / cop
    other = cost - cap_cost - energy_cost
    cooling = {
        "favorable_displayed_USD_MWh": cost,
        "capital_recovery_USD_MWh": cap_cost,
        "energy_at_component_COP_USD_MWh": energy_cost,
        "other_fixed_ledger_USD_MWh": other,
        "free_initial_capital_only_USD_MWh": cost - cap_cost,
        "free_initial_capital_and_electricity_USD_MWh": other,
        "perfect_drive_component_kW_for_10kW": 10 / 4.503,
        "full_target_kW_for_10kW": 2,
        "gentler_net_heat_kJ_kg_cycle": 10 * 33.024 / 55.89,
        "active_cycles_per_4000h_year": 4000 * 3600 / 33.024,
        "five_million_active_cycles_operating_years_IF_qualified": 5e6 / (4000 * 3600 / 33.024),
        "fouled_slit_pressure_ratio_5um_each_side": (50 / 40) ** 3,
    }
    # Exact feed/product/reject mass closure at prescribed example composition.
    feed, xf, product, xp = 2.0, 0.10, 1.0, 0.0005
    reject = feed - product
    xb = (feed * xf - product * xp) / reject
    gmin = (ideal_mixture_g(product, xp) + ideal_mixture_g(reject, xb)
            - ideal_mixture_g(feed, xf)) * 1000 / 3_600_000
    gmin_pure = (ideal_mixture_g(1, 0) + ideal_mixture_g(1, 0.2)
                 - ideal_mixture_g(2, 0.1)) * 1000 / 3_600_000
    # A separately closed reversible freeze/melt construction in SAME ideal model.
    n = 10000
    rev_main = sum(LATENT * (TM / freezing_kelvin((i + 0.5) / n) - 1)
                   for i in range(n)) / n * 1000 / 3_600_000
    ambient_rejection_correction = rev_main * 298.15 / TM
    assert math.isclose(ambient_rejection_correction, gmin_pure, rel_tol=1e-8)
    # Entrainment example: intrinsic lattice impurity is introduced, not zero.
    xi, rho_ice, rho_brine, porosity = 50e-6, 917, 1200, 0.35
    max_brine_fraction = (xp - xi) / (xb - xi)
    allowed_brine_per_pure_ice = max_brine_fraction / (1 - max_brine_fraction)
    initial_brine_per_ice = porosity * rho_brine / ((1 - porosity) * rho_ice)
    needed_void_exchanges = math.log(initial_brine_per_ice / allowed_brine_per_pure_ice)
    mixed_wash_water_per_ice = needed_void_exchanges * initial_brine_per_ice * 1000 / rho_brine
    annual_t = 10 * 8760 * 0.9
    phase = [phase_case(w, e, a) for w in (0.05, 0.10, 0.20)
             for e in (0.45, 0.60, 0.75) for a in (1, 2)]
    out = {
        "scope": "Introduced thermodynamic/transport/cost diagnostics, not a qualified brine plant or achieved invention.",
        "cooling_unchanged_ledger": cooling,
        "mass_and_ideal_thermodynamics": {
            "feed_kg": feed, "feed_NaCl_fraction": xf,
            "accepted_product_kg": product, "product_NaCl_fraction": xp,
            "reject_kg": reject, "reject_NaCl_fraction": xb,
            "NaCl_mass_retained_fraction": reject * xb / (feed * xf),
            "ideal_fully_dissociated_minimum_kWh_t_product_at_298_15K": gmin,
            "pure_product_same_ideal_minimum_kWh_t": gmin_pure,
            "ideal_liquidus_start_C_NOT_real_NaCl_data": freezing_kelvin(0) - 273.15,
            "ideal_liquidus_end_C_NOT_real_NaCl_data": freezing_kelvin(1) - 273.15,
            "reversible_freeze_to_TM_main_kWh_t": rev_main,
            "after_paying_surplus_heat_lift_to_ambient_kWh_t": ambient_rejection_correction,
            "note": "Complete dissociation/ideal activities/constant fusion enthalpy, no actual high-salt phase diagram or activity coefficients. Perfect reversible heat exchange is only the identity diagnostic.",
        },
        "entrainment_and_wash": {
            "intrinsic_ice_salt_fraction_INTRODUCED": xi,
            "external_brine_salt_fraction": xb,
            "max_final_external_brine_mass_fraction": max_brine_fraction,
            "max_brine_kg_per_kg_pure_ice": allowed_brine_per_pure_ice,
            "initial_external_brine_kg_kg_ice_INTRODUCED_bed": initial_brine_per_ice,
            "fraction_of_initial_brine_mass_to_remove_or_replace": 1 - allowed_brine_per_pure_ice / initial_brine_per_ice,
            "well_mixed_void_exchanges_INTRODUCED_model": needed_void_exchanges,
            "well_mixed_pure_wash_kg_kg_ice": mixed_wash_water_per_ice,
            "note": "Not a wash lower bound. Piston-like displacement/countercurrent flow can differ; actual closed meltwater recycle, trapped internal brine, freeze-back and product withdrawal must be built.",
        },
        "conditional_phase_grid": phase,
        "heat_exchange_and_economy": {
            "introduced_10t_net_h_gross_ice_at_20percent_diversion_t_h": 10 / 0.8,
            "freezing_latent_kW_at_that_gross_rate": 10 / 0.8 * LATENT / 3600,
            "introduced_U_W_m2K": 300,
            "introduced_approach_K": 2,
            "needed_freezing_area_m2_at_that_U_and_approach": 10 / 0.8 * LATENT / 3600 * 1000 / 600,
            "annual_product_t": annual_t,
            "500k_capital_USD_t": 500000 * rate / annual_t,
            "electricity_USD_t_at_10kWh_t_80power": 0.8,
            "remaining_under_2_USD_t_for_all_service": 2 - 0.8 - 500000 * rate / annual_t,
            "hydraulic_only_120bar_kWh_m3_permeate_at_yield_half_pump80_ERD95": 12e6 * (1 + 0.05) / 0.8 / 3_600_000,
            "hydraulic_note": "Not a salt-separation point or full LSRRO energy. High-salt permeate must be recycled/processed with actual osmotic activities, membranes, pumps and paid losses.",
        },
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'conditional_phase_grid'}, indent=2))
    print('SELECTED_PHASE_CASES')
    for row in phase:
        if row['introduced_wash_melt_diversion_fraction'] == 0.1:
            print(json.dumps(row))


if __name__ == '__main__':
    main()
