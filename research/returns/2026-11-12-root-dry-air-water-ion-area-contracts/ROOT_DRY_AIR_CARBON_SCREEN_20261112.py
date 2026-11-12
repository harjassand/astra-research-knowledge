"""Conditional transport/cost screens, not a simulated or measured DAC device.

Two different layers are considered: an outer air/liquid gas barrier and an
inner ion-conducting carbon-pump separator. No material is assumed to possess
the independent example properties simultaneously. Standard library only.
"""
import json
import math

F = 96485.33212
R = 8.314462618
MC = 0.0440095
MW = 0.01801528
P = 101325.0
X = 425e-6
REMOVAL = 0.5
BARRER = 1.0 / 2.99e15  # mol m / (m2 s Pa), reported conversion in Papchenko.
GPU = BARRER / 1e-6


def psat_water(t_c):
    """Buck-type saturation fit (Pa), a declared engineering approximation."""
    return 611.21 * math.exp((18.678 - t_c / 234.5) * t_c / (257.14 + t_c))


def outer_barrier(t_c, rh, internal_aw=0.9, evaporation_kg_per_kg=1.0):
    # Dilute, constant-total-airflow, plug flow; perfect CO2 sink at interface.
    # CO2 and water have constant permeance; gas films/support losses omitted.
    # Log mean is exact within that idealisation, not at arbitrary kinetics.
    x_out = X * (1 - REMOVAL)
    p_logmean = P * (X - x_out) / math.log(X / x_out)
    dw = max(0.0, (internal_aw - rh) * psat_water(t_c))
    max_molar_ratio = evaporation_kg_per_kg * MC / MW
    s_required = dw / (p_logmean * max_molar_ratio)
    target_flux = 0.19 / 3600.0  # illustrative net mol CO2 / m2 / s
    return {
        "T_C": t_c, "ambient_RH": rh, "internal_aw": internal_aw,
        "evaporation_budget_kg_per_kg": evaporation_kg_per_kg,
        "CO2_logmean_driving_pressure_Pa": p_logmean,
        "water_driving_pressure_Pa": dw,
        "minimum_CO2_to_H2O_permeance_ratio": s_required,
        "CO2_permeance_GPU_for_0.19_mol_m2_h": target_flux / (GPU * p_logmean),
    }


def ion_separator(p_c_barrer, sigma_ms_cm, thickness_um, net_flux_mol_m2_h=0.19,
                  charge_efficiency=1.0, z=2.0, co2_delta_pa=95000.0):
    # Conditional homogeneous layer, steady diffusion and linear ohmic law.
    # P_C and sigma must be established TOGETHER in the actual hydrated state.
    # z=2 is a hypothetical carbonate pump, not an imported Ni battery identity.
    pc = p_c_barrer * BARRER
    sig = sigma_ms_cm * 0.1  # mS/cm -> S/m
    length = thickness_um * 1e-6
    net = net_flux_mol_m2_h / 3600
    a = pc * co2_delta_pa
    back = a / length
    current = z * F * (net + back) / charge_efficiency
    ohmic_v = current * length / sig
    specific = current * ohmic_v / net / MC / 3.6e6
    lower = 4 * (z * F / charge_efficiency)**2 * a / sig / MC / 3.6e6
    return {
        "hypothetical_P_CO2_Barrer": p_c_barrer,
        "hypothetical_conductivity_mS_cm": sigma_ms_cm,
        "thickness_um": thickness_um,
        "net_flux_mol_m2_h": net_flux_mol_m2_h,
        "backdiffusion_to_net_ratio": back / net,
        "current_A_m2": current,
        "membrane_ohmic_drop_V": ohmic_v,
        "membrane_ohmic_kWh_per_kg_net": specific,
        "unconstrained_thickness_optimum_um": a / net * 1e6,
        "unconstrained_minimum_membrane_ohmic_kWh_per_kg_net": lower,
        "identity_residual": (
            (net * net * length + 2 * net * a + a * a / length)
            - (4 * net * a + (net * length - a)**2 / length)
        ),
    }


def area_cost(flux, installed_active_dollars_m2=10, replacement_dollars_m2=10,
              replacement_years=3):
    rate_kg_day = 1000.0
    annual_tonnes = rate_kg_day * 365 * 0.9 / 1000
    area = rate_kg_day / MC / 24 / flux
    crf = 0.08 / (1 - (1.08)**(-15))
    return {
        "net_productivity_mol_m2_h": flux,
        "active_area_m2_at_1_tonne_day": area,
        "conditional_active_capital_USD_per_tonne": area * crf * installed_active_dollars_m2 / annual_tonnes,
        "conditional_replacement_USD_per_tonne": area * replacement_dollars_m2 / replacement_years / annual_tonnes,
    }


def main():
    charge_ah_kg = 2 * F / MC / 3600
    air_m3_kg = R * 298.15 / (P * X * REMOVAL * MC)
    out = {
        "scope": "Analytic conditional screens; no actual device, joint material or chemistry is supplied.",
        "pressure_Pa": P,
        "airflow_m3_per_kg_at_25C_half_capture": air_m3_kg,
        "fan_kWh_per_kg_at_50Pa_60pct": air_m3_kg * 50 / 0.6 / 3.6e6,
        "hypothetical_2electron_charge_Ah_per_kg": charge_ah_kg,
        "hypothetical_2electron_current_A_at_1kg_day": charge_ah_kg / 24,
        "effective_voltage_ceiling_at_0.5kWhkg_before_aux": 500 / charge_ah_kg,
        "effective_voltage_ceiling_after_example_fan_only": (500 - air_m3_kg * 50 / 0.6 / 3600) / charge_ah_kg,
        "outer_barrier": [outer_barrier(t, rh, evaporation_kg_per_kg=w)
                          for t, rh in [(20, .4), (25, .3), (30, .2)] for w in [1, 2]],
        "inner_separator_examples": [ion_separator(pc, sig, 50)
                                     for pc in [3.43, .72] for sig in [.01, .25]],
        "area_cost_examples": [area_cost(f) for f in [.19, 1.9]],
    }
    print(json.dumps(out, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
