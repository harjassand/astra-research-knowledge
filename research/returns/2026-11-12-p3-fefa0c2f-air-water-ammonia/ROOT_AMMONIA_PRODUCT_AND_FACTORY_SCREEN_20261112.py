"""Independent conditional checks using the available FEFA0C2F process tables.

No producer code or artifact is collected/run; no catalyst or membrane is supplied.
"""
import json
import math

R = 8.314462618
M_NH3 = .0170305


def main():
    costs = dict(electricity=.621, capital=1.279, maintenance=.219,
                 labor_site_quality=.213, water_guards_waste=.157,
                 membrane_renewal=.235, catalyst_renewal=.381,
                 sorbent_renewal=.232, structures_renewal=.025,
                 decommissioning=.017)
    p0, p1, pstar, inhibition = .04, .4, .001, 1.1
    mass_factor = ((1 + p1 / pstar) / (1 + p0 / pstar))**inhibition
    # Extra compression only for a hypothetical fresh 1bar stoichiometric feed.
    # Not a comparison using an actual electrolyzer's possibly pressurized output.
    fresh_moles_kg = 2 / M_NH3
    comp = {str(p): fresh_moles_kg * R * 298.15 * math.log(p) / .6 / 3.6e6
            for p in [20, 100, 200]}
    salt_kg = 2 * 1.204 * .4
    base_ammonia = salt_kg / .095211 * 2 * M_NH3
    working_ammonia = 2 * 1.204 * .08
    out = {
        "scope": "Conditional bookkeeping/transport diagnostics; no device or independently validated producer model.",
        "producer_table_total_USDkg": sum(costs.values()),
        "even_if_all_capital_maintenance_decommissioning_free_USDkg":
            sum(v for k, v in costs.items() if k not in ['capital', 'maintenance', 'decommissioning']),
        "replacing_only_all_membrane_catalyst_sorbent_renewal_with_zero_USDkg":
            sum(v for k, v in costs.items() if k not in ['membrane_renewal', 'catalyst_renewal', 'sorbent_renewal']),
        "hypothetical_model_inhibition": {
            "representative_start_NH3_pressure_bar": p0,
            "hypothetical_new_NH3_pressure_bar": p1,
            "catalyst_mass_multiplier_if_the_same_rate_law_were_extended": mass_factor,
            "qualification": "0.4bar extrapolates beyond the producer's model range; it is algebra, not measured kinetics.",
        },
        "ideal_constant_permeance_hot_extraction_screen": {
            "H2_pressure_bar": 12.15,
            "NH3_pressure_bar": .05,
            "allowed_lost_H2_relative_to_stoichiometric_useful_H2": .02,
            "minimum_NH3_to_H2_permeance_ratio_if_both_have_zero_permeate_pressure": 12.15 / (.05 * 1.5 * .02),
            "minimum_isothermal_pure_NH3_pumping_kWhkg_0.05to1bar_at_245C":
                R * 518.15 * math.log(1 / .05) / M_NH3 / 3.6e6,
            "qualification": "No actual membrane, selective chemistry, guard or compressor is supplied. Recycle or a pressure-balanced receiver changes the model.",
        },
        "fresh_gas_hypothetical_compression_kWhkg": comp,
        "additional_100bar_versus20bar_kWhkg": comp['100'] - comp['20'],
        "salt_initial_inventory_kg_NH3": {
            "diammine_baseline": base_ammonia,
            "both_beds_working_capacity": working_ammonia,
            "sum_illustrative": base_ammonia + working_ammonia,
            "qualification": "Rounded source parameters and illustrative bed loading, not an independently simulated cycle.",
        },
        "production_hours_to_make_0.535kg_initial_NH3_at_1kg_day": .535 * 24,
        "startup_9.12kWh_allocated_over_100h_product_kWhkg": 9.12 / (100 / 24),
        "time_to_exhaust_5pct_reserve_if_1pct_per100h_loss_continues_h":
            100 * math.log(1 / 1.05) / math.log(.99),
    }
    print(json.dumps(out, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
