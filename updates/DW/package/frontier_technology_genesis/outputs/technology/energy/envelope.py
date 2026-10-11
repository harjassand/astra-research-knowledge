#!/usr/bin/env python3
"""Reproducible optimistic physical envelopes; no device-performance prediction.

The water model uses constant heat capacities, ideal vapor, incompressible liquid,
and an exactly consistent integrated Clausius-Clapeyron saturation curve. It is
an approximate research model, NOT an IAPWS implementation or measurement.
Membrane R_A and alpha values below are hypotheses, NOT measured 2022 values.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

R = 461.5       # J/(kg K), rounded water-specific gas constant
CPV = 1860.0   # J/(kg K), stipulated constant vapor heat capacity
CPL = 4180.0   # J/(kg K), stipulated constant liquid heat capacity
T0 = 273.15    # K, reference
P0 = 611.657   # Pa, rounded reference near the triple point
L0 = 2_500_900.0  # J/kg, stipulated latent heat at reference
RHO_L = 1000.0   # kg/m^3, rounded liquid density


def latent(t: float) -> float:
    return L0 + (CPV - CPL) * (t - T0)


def saturation(t: float) -> float:
    dc = CPV - CPL
    ln_ratio = ((L0 - dc*T0) * (1/T0 - 1/t) + dc*math.log(t/T0)) / R
    return P0 * math.exp(ln_ratio)


def water_envelope(tc: float = 283.15, th: float = 308.15,
                   cooling_w: float = 1000.0, frequency_hz: float = 5.0,
                   stroke_m: float = 0.01, target_cop: float = 6.0) -> dict:
    pc, ph = saturation(tc), saturation(th)
    ratio = ph / pc
    cold_heat = latent(tc) - CPL*(th-tc)  # saturated vapor minus throttled liquid
    iso_work = R*th*math.log(ratio)      # preheated vapor, isothermal at hot sink
    adiabatic_work = CPV*tc*(ratio**(R/CPV)-1)
    rev_work = cold_heat*(th-tc)/tc
    entropy_preheat = CPV*(math.log(th/tc)-(th-tc)/th)
    entropy_throttle = CPL*(math.log(tc/th)+(th-tc)/tc)
    assert entropy_preheat >= 0 and entropy_throttle >= 0
    assert math.isclose(iso_work-rev_work,
                        th*(entropy_preheat+entropy_throttle), rel_tol=1e-10)
    assert cold_heat/iso_work <= tc/(th-tc)
    rho_v_hot_suction = pc/(R*th)
    cold_j_per_m3 = rho_v_hot_suction*cold_heat
    suction_m3s = cooling_w/cold_j_per_m3
    swept_m3 = suction_m3s/frequency_hz
    area_m2 = swept_m3/stroke_m
    ideal_input = cooling_w*iso_work/cold_heat
    parasitic_budget = cooling_w/target_cop-ideal_input
    # Retained hot liquid releases sensible heat by flash evaporation on refill.
    # This is a conservative budget proxy, not a transient two-phase CFD model.
    film_limit_5pct_m = (0.05*rho_v_hot_suction*stroke_m*cold_heat /
                        (RHO_L*CPL*(th-tc)))
    film_1um_loss_ratio = 0.05*1e-6/film_limit_5pct_m
    return {
        "model_status": "APPROXIMATE_OPTIMISTIC_NOT_DEVICE_DATA",
        "cold_K": tc, "hot_K": th,
        "suction_pressure_Pa": pc, "discharge_pressure_Pa": ph,
        "pressure_ratio": ratio, "cold_heat_J_per_kg": cold_heat,
        "hot_isothermal_work_J_per_kg": iso_work,
        "cold_inlet_adiabatic_work_J_per_kg": adiabatic_work,
        "Carnot_COP": tc/(th-tc), "ideal_hot_isothermal_COP": cold_heat/iso_work,
        "ideal_adiabatic_COP": cold_heat/adiabatic_work,
        "heat_pump_work_identity_relative_error": abs(
            (iso_work-rev_work-th*(entropy_preheat+entropy_throttle))/iso_work),
        "cooling_W": cooling_w, "hot_suction_volume_L_per_s": suction_m3s*1000,
        "frequency_Hz": frequency_hz, "stroke_mm": stroke_m*1000,
        "ideal_swept_volume_L": swept_m3*1000, "ideal_active_area_m2": area_m2,
        "target_COP": target_cop, "ideal_input_W": ideal_input,
        "all_other_loss_budget_W": parasitic_budget,
        "continuous_cycles_per_year": frequency_hz*365.25*24*3600,
        "hot_retained_film_limit_for_5pct_heat_penalty_nm": film_limit_5pct_m*1e9,
        "illustrative_1um_hot_film_heat_penalty_ratio": film_1um_loss_ratio,
        "warnings": ["No clearance, manifold, valve, actuator, vacuum-purge, or heat-leak losses.",
                     "Hot isothermal compression includes sink-supplied suction preheat.",
                     "Hot film estimate applies only to an in-place condensing chamber.",
                     "No new or validated compressor mechanism is claimed."]
    }


def membrane_envelope() -> dict:
    tc, th = 283.15, 308.91
    result = []
    for alpha in (0.5, 1.0, 2.0):
        for ra in (0.001, 0.01, 0.04):
            for cop in (3.0, 6.0):
                budget = 1/cop-(th-tc)/tc
                q = alpha*alpha/ra*budget
                result.append({"alpha_V_hypothesis": alpha,
                               "R_A_ohm_m2_hypothesis": ra, "required_COP": cop,
                               "optimistic_flux_W_per_m2": q,
                               "area_m2_per_kW_lower_bound": 1000/q})
    return {
        "status": "SYMBOLIC_BOUND_AND_EXPLICIT_HYPOTHESES",
        "equation": "Qdot <= integral_A(alpha^2/R_A) * (1/COP - (Th-Tc)/Tc)",
        "reported_high_efficiency_current_A_per_m2": 5.0,
        "reported_voltage_V_not_matched_to_same_point": 0.22,
        "measured_isolated_R_A": None,
        "illustrative_alpha_V": 1.0,
        "illustrative_flux_at_reported_j_W_per_m2": 5.0,
        "illustrative_area_m2_per_kW": 200.0,
        "sensitivity_cases": result,
    }


if __name__ == "__main__":
    result = {"membrane": membrane_envelope(), "water": water_envelope()}
    destination = Path(__file__).with_name("envelope_results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
