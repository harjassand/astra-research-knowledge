"""Conditional stoichiometric, purge and energy screens for a thermal NH3 loop.

No catalyst kinetics, equilibrium constant, separator or electrolyzer performance
is supplied. In particular an inaccessible H2 thermochemistry table is not
replaced by remembered coefficients. All numerical process inputs are scenarios.
"""
import json
import math

R = 8.314462618
M_NH3 = 0.0170305  # kg/mol, NIST SRD69 ammonia entry read this session
M_N2 = 0.0280134  # kg/mol, NIST SRD69 nitrogen entry read this session
M_H2 = (2 * M_NH3 - M_N2) / 3  # stoichiometric mass balance, kg/mol
M_WATER = 0.01801528


def purge_screen(conversion, inlet_inert_fraction, fresh_inert_per_n2=0.012,
                 electrolyzer_kwh_kg_h2=53.0, pressure_bar=20.0,
                 compressor_efficiency=0.60, temperature_k=298.15):
    # Fresh H2/N2=3, all NH3 removed between passes, constant inert molar ratio.
    # The inert is not removed otherwise; purge loses both H2 and N2.
    c = conversion
    y = inlet_inert_fraction
    a = fresh_inert_per_n2
    inert_per_reactor_n2 = 4 * y / (1 - y)
    denominator = inert_per_reactor_n2 - a * (1 - c)
    if denominator <= 0:
        return {"conversion": c, "inlet_inert_fraction": y, "feasible": False}
    p = a * c / denominator
    if not 0 < p <= 1:
        return {"conversion": c, "inlet_inert_fraction": y, "feasible": False}
    fresh_per_reactor_n2 = c + p * (1 - c)
    utilization = c / fresh_per_reactor_n2
    h2_kg_per_kg_nh3 = 1.5 * M_H2 / M_NH3 / utilization
    h2_energy = h2_kg_per_kg_nh3 * electrolyzer_kwh_kg_h2
    fresh_moles_per_kg_nh3 = (4 + a) / (2 * utilization * M_NH3)
    compression = (fresh_moles_per_kg_nh3 * R * temperature_k
                   * math.log(pressure_bar) / 3.6e6 / compressor_efficiency)
    # Reaction quotient N2+3H2 ->2NH3 at the hypothetical single-pass exit.
    # Ideal gases, pure-gas standard state 1bar; NOT an equilibrium prediction.
    n_total_exit = 4 - 2 * c + inert_per_reactor_n2
    quotient = (4 * c * c * n_total_exit * n_total_exit
                / (27 * (1 - c)**4 * pressure_bar**2))
    inert_balance_residual = a * fresh_per_reactor_n2 - p * inert_per_reactor_n2
    n2_balance_residual = fresh_per_reactor_n2 - c - p * (1 - c)
    return {
        "single_pass_N2_conversion": c,
        "reactor_inlet_inert_mole_fraction": y,
        "fresh_inert_per_fresh_N2": a,
        "purge_fraction_of_post_removal_gas": p,
        "hydrogen_and_nitrogen_utilization": utilization,
        "fresh_hydrogen_kg_per_kg_NH3": h2_kg_per_kg_nh3,
        "hypothetical_electrolysis_kWh_per_kg_NH3": h2_energy,
        "hypothetical_fresh_compression_kWh_per_kg_NH3": compression,
        "remaining_of_12kWhkg_before_other_aux": 12 - h2_energy - compression,
        "ideal_exit_reaction_quotient": quotient,
        "maximum_standard_deltaG_kJ_for_that_conversion_at_250C": -R * 523.15 * math.log(quotient) / 1000,
        "actual_equilibrium_constant": "UNASSESSED",
        "inert_balance_residual": inert_balance_residual,
        "N2_balance_residual": n2_balance_residual,
    }


def main():
    nh3_mol_day = 1 / M_NH3
    h2_stoich = 1.5 * M_H2 / M_NH3
    water_stoich = 1.5 * M_WATER / M_NH3
    crf = 0.08 / (1 - 1.08**(-15))
    output = {
        "scope": "Hypothetical engineering balances; no physical invention, measured electrolyzer, catalyst rate or purge design.",
        "NH3_mol_per_hour_at_1kg_day": nh3_mol_day / 24,
        "N2_mol_per_hour_at_1kg_day": nh3_mol_day / 48,
        "H2_mol_per_hour_at_1kg_day": nh3_mol_day / 16,
        "stoichiometric_H2_kg_per_kg_NH3": h2_stoich,
        "water_net_reaction_kg_per_kg_NH3": water_stoich,
        "additional_solvent_water_at_10wtpct_kg_per_kg_NH3": 9,
        "example_no_purge_electrolysis_kWhkg_at_53kWhkgH2": h2_stoich * 53,
        "electrolyzer_scenario_boundary": "Hypothetical 53kWh/kgH2 at 1bar dry H2 outlet; not an actual stack datum. Do not add the same compression twice.",
        "NH3_formation_heat_at_298K_kWhkg": 45.89806e3 / M_NH3 / 3.6e6,
        "reactor_operating_heat_at_250C": "NOT_CALCULATED; H2 heat-capacity source unavailable",
        "catalyst_rate_examples": [
            {"hypothetical_useful_rate_molNH3_gcat_s": rate,
             "catalyst_kg_at_1kgNH3_day": (nh3_mol_day / 86400 / rate) / 1000}
            for rate in [1e-6, 1e-7, 1e-8]
        ],
        "purge_examples": [purge_screen(c, y) for c in [.1, .4] for y in [.01, .05]],
        "cost_screen": {
            "production_kg_per_year": 1000 * 365 * .9,
            "example_electricity_USDkg_at_12kWhkg_and_0.05USDkWh": .6,
            "max_installed_capital_USD_if_no_other_variable_costs_and_30k_fixed_labour":
                ((1000 * 365 * .9) * (1 - .6) - 30000) / (crf + .03),
            "qualification": "No allowance here for material renewal, water, site or waste; not a component quote or plant cost.",
        },
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
