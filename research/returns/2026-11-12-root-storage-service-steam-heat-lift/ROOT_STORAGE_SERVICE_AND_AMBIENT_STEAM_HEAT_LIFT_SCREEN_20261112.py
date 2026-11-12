"""ROOT analytic design screens, not a qualified storage or heat-pump model.

Prices, approaches, heat capacities/latent heat, auxiliary loads and new design
points below are introduced surrogates. They are not borrowed equipment maps.
"""
import json
import math

CRF = 0.08 / (1 - 1.08 ** -20)
annual_h = 8760 * 0.90
storage_cycles = annual_h / 344
annual_storage_MWh = storage_cycles * 100

storage = {
    "reported_model_RTE": 100 / 147.004,
    "annual_delivered_MWh": annual_storage_MWh,
    "unchanged_service_USD_y": 373899,
    "FREE_initial_capital_only_USD_MWh_at_20_power": 373899 / annual_storage_MWh + 20 * 147.004 / 100,
    "FREE_initial_capital_AND_FREE_charging_USD_MWh": 373899 / annual_storage_MWh,
    "initial_capital_multiplier_to_target": 12.371e6 / 1.5e6,
    "scope": "unchanged candidate ledger only, not an all-storage lower bound",
}

# Introduced ideal reversible heating of 90C liquid to saturated 200C steam.
# Constant liquid cp and latent heat are rounded surrogates, not steam-table data.
T0, Tin, Th = 288.15, 363.15, 473.15
cp, latent = 4.18, 1940.0  # kJ/(kg K), kJ/kg
q_per_kg = cp * (Th - Tin) + latent
ds_per_kg = cp * math.log(Th / Tin) + latent / Th
w_rev = q_per_kg - T0 * ds_per_kg
mdot = 1000 / q_per_kg
reference = {
    "introduced_return_water_C": Tin - 273.15,
    "introduced_steam_C": Th - 273.15,
    "introduced_source_C": T0 - 273.15,
    "introduced_cp_kJ_kgK": cp,
    "introduced_latent_kJ_kg": latent,
    "net_added_heat_kJ_kg": q_per_kg,
    "added_entropy_kJ_kgK": ds_per_kg,
    "minimum_reversible_work_kJ_kg": w_rev,
    "ideal_glide_matched_COP": q_per_kg / w_rev,
    "all_heat_at_200C_Carnot_COP": Th / (Th - T0),
    "steam_kg_s_at_1MW_added_heat": mdot,
    "incoming_90C_water_heat_above_15C_kW_NOT_CREDITED_as_output": mdot * cp * (Tin - T0),
    "scope": "declared hot return is an input stream; internally producing it must be paid",
}

# Introduced single condensing hot level with finite 5K hot/cold approaches.
Tc_evap, Tc_cond = 283.15, 478.15
cop_finite = Tc_cond / (Tc_cond - Tc_evap)
w_min = 1000 / cop_finite
target_grid = 1000 / 2.0
aux = 30.0
eta_motor = 0.96
available_shaft = (target_grid - aux) * eta_motor
finite = {
    "introduced_evaporator_C": Tc_evap - 273.15,
    "introduced_condenser_C": Tc_cond - 273.15,
    "single_hot_level_reversible_COP": cop_finite,
    "ideal_work_kW_per_MWheat": w_min,
    "target_all_grid_COP": 2.0,
    "total_nonideal_allowance_kW_per_MWheat": target_grid - w_min,
    "introduced_aux_kW": aux,
    "introduced_motor_efficiency": eta_motor,
    "shaft_irreversibility_budget_after_motor_aux_kW": available_shaft - w_min,
    "scope": "no compressor efficiency, fluid stability, heat exchanger or motor is supplied",
}

# An introduced air coil delivering 500kW from 15C inlet / 11C outlet to 10C.
Qsource, cp_air, rho_air = 500000.0, 1000.0, 1.2
air_in, air_out, evap = 15.0, 11.0, 10.0
lmtd = ((air_in - evap) - (air_out - evap)) / math.log((air_in - evap) / (air_out - evap))
mass_air = Qsource / (cp_air * (air_in - air_out))
flow_air = mass_air / rho_air
air = {
    "introduced_air_mass_kg_s": mass_air,
    "introduced_air_volume_m3_s": flow_air,
    "LMTD_K": lmtd,
    "required_UA_kW_K": Qsource / lmtd / 1000,
    "area_m2_at_INTRODUCED_40W_m2K": Qsource / lmtd / 40,
    "fan_kW_at_INTRODUCED_100Pa_60pct_efficiency": 100 * flow_air / 0.6 / 1000,
    "scope": "dry-air sensible surrogate only, not qualified air coil/icing/fan performance",
}

econ = []
for use in [0.9, 0.6]:
    for price in [40, 80]:
        heat_MWh = 8760 * use
        electric = price / 2
        finance = 500000 * CRF / heat_MWh
        remaining_y = (35 - electric) * heat_MWh - 500000 * CRF
        econ.append({"introduced_use": use, "power_USD_MWh": price,
                     "electric_USD_MWh_heat_at_COP2": electric,
                     "capital_USD_MWh_heat_at_500USD_kW": finance,
                     "all_service_labor_replacement_removal_budget_USD_y_under_35_target": remaining_y})

out = {
    "kind": "ROOT separately derived resource/entropy contracts, not a device simulation",
    "device_validation": False,
    "storage": storage,
    "conditional_gas_matrix_similarity": {
        "assumptions": "ideal gas at fixed T; constant stroke time/flow length; laminar parallel passages",
        "gap_scaling": "g proportional p**(-1/2) keeps rho*cp*g*g/k constant",
        "plate_scaling": "delta proportional p**(1/2) gives constant solid/gas heat-capacity ratio",
        "absolute_liquid_pressure_drop_scaling": "dp proportional 1/g**2 proportional p for constant velocity",
        "per_stage_friction_work_scaling": "dp*V proportional p*p**(-1), hence constant, not free",
        "introduced_105um_gap_plus_10um_diffusion_time_factor": (115 / 105) ** 2,
        "introduced_105um_gap_minus_10um_liquid_dp_factor": (105 / 95) ** 2,
        "scope": "conditional similarity argument, not actual two-phase map, tolerance or aging law",
    },
    "ambient_steam_reference": reference,
    "finite_approach_budget": finite,
    "air_coil_screen": air,
    "heat_economics": econ,
    "cascade_source_payment_example": {
        "introduced_top_COP": 4.4,
        "introduced_lower_COP": 3.0,
        "whole_COP_before_any_MVR": 1 / (1 / 4.4 + (1 - 1 / 4.4) / 3.0),
        "scope": "generic two-heat-pump identity, not an AtmosZero/SPH measurement or a full steam-compression plant",
    },
    "source_temperature_bound_sweep": [
        {"source_C": t, "isothermal_200C_Carnot_COP": Th / (Th - (t + 273.15))}
        for t in [5, 15, 35]
    ],
}
assert 0 < w_rev < q_per_kg
assert math.isclose(mdot * q_per_kg, 1000.0)
assert finite["shaft_irreversibility_budget_after_motor_aux_kW"] > 0
print(json.dumps(out, indent=2, sort_keys=True))
