#!/usr/bin/env python3
"""Introduced acoustic-write chemistry diagnostics; no material or acoustic fit.

All kinetic, geometric, concentration and acceptance numbers below are introduced.
This is a scalar, ideal fast-scavenging model, NOT a propagation solver, chemical
recipe, measured resin, physical validation, or new manufacturing process.
No producer code or external data is used. Python standard library only.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ON_CONVERSION = 0.95
OFF_CONVERSION = 0.01
D_ON = -math.log1p(-ON_CONVERSION)
D_OFF = -math.log1p(-OFF_CONVERSION)
GAMMA = 3.0  # phenomenological conversion per normalized unscavenged radical dose
R_ON = 2.0  # introduced normalized radical production per second at intensity 1
R_REPLENISH = 1.0  # ideal constant-concentration reservoir, per second
GAP_S = 0.1
BACKGROUND_INTENSITY = 0.02  # relative INTENSITY, not pressure amplitude
PULSE_S = math.log(2.0) + D_ON / GAMMA  # fresh q=1, r=1, R=2
TARGET_PULSES = [1, 10, 100, 1000, 10000]


def conversion(polymerizing_radical_dose: float, gamma: float = GAMMA) -> float:
    return -math.expm1(-gamma * max(0.0, polymerizing_radical_dose))


def inhibited_step(q0: float, radical_rate: float, dt: float,
                   replenish_rate: float, bypass: float = 0.0) -> dict:
    """Exact constant-input step of an explicitly ideal stoichiometric model.

    q is local inhibitor amount divided by its initial local amount C0*V.
    (1-bypass)*R is scavenged first while q>0. Reservoir replenishment is
    r*(1-q). At q=0 at most r radicals/s can be scavenged; excess polymerizes.
    bypass*R polymerizes directly. Each radical goes to exactly one sink.

    q' = r*(1-q) - (1-bypass)*R, with reflection at q=0.
    Polymerization conversion is a SEPARATE phenomenological function of the
    unscavenged dose; q and radical accounting do not establish real kinetics.
    """
    assert 0 <= q0 <= 1 and radical_rate >= 0 and dt >= 0
    assert replenish_rate >= 0 and 0 <= bypass <= 1
    rs = (1.0 - bypass) * radical_rate
    r = replenish_rate
    hit = None
    if r == 0:
        scavenged = min(q0, rs * dt)
        q1 = q0 - scavenged
        if rs > 0 and rs * dt >= q0:
            hit = q0 / rs
    else:
        qss = 1.0 - rs / r
        candidate = q0 + (qss - q0) * (-math.expm1(-r * dt))
        if qss < 0 and candidate <= 0:
            hit = math.log1p(q0 / (-qss)) / r
            hit = min(dt, max(0.0, hit))
            q1 = 0.0
            scavenged = rs * hit + r * (dt - hit)
        else:
            q1 = min(1.0, max(0.0, candidate))
            scavenged = rs * dt
    raw = radical_rate * dt
    polymerizing = max(0.0, raw - scavenged)
    supplied = q1 - q0 + scavenged
    if supplied < 0 and supplied > -1e-12:
        supplied = 0.0
    assert supplied >= -1e-10
    return {
        "q0": q0, "q1": q1, "raw": raw, "scavenged": scavenged,
        "polymerizing": polymerizing, "supplied": supplied,
        "time_to_depletion_within_step_s": hit,
        "inhibitor_balance_error": q0 + supplied - scavenged - q1,
        "radical_balance_error": raw - scavenged - polymerizing,
    }


def schedule(n: int, relative_intensity: float, replenish_rate: float,
             bypass: float = 0.0, q_initial: float = 1.0,
             exponent: float = 1.0) -> dict:
    q = q_initial
    totals = dict(raw=0.0, scavenged=0.0, polymerizing=0.0, supplied=0.0)
    first_depletion = None
    min_q = q
    for index in range(n):
        s = inhibited_step(q, R_ON * relative_intensity**exponent,
                           PULSE_S, replenish_rate, bypass)
        q = s["q1"]
        min_q = min(min_q, q)
        if first_depletion is None and s["time_to_depletion_within_step_s"] is not None:
            first_depletion = index + 1
        for k in totals:
            totals[k] += s[k]
        if index + 1 < n:
            idle = inhibited_step(q, 0.0, GAP_S, replenish_rate, bypass)
            q = idle["q1"]
            for k in totals:
                totals[k] += idle[k]
    balance_q = q_initial + totals["supplied"] - totals["scavenged"] - q
    balance_r = totals["raw"] - totals["scavenged"] - totals["polymerizing"]
    assert abs(balance_q) < 2e-8 and abs(balance_r) < 2e-8
    return {
        "pulses": n, "relative_intensity": relative_intensity,
        "intensity_to_radical_rate_exponent": exponent,
        "replenish_rate_per_s": replenish_rate, "bypass_fraction": bypass,
        "active_time_s": n * PULSE_S,
        "elapsed_time_s": n * PULSE_S + max(0, n - 1) * GAP_S,
        "final_q": q, "minimum_q": min_q,
        "first_depletion_pulse": first_depletion,
        "conversion": conversion(totals["polymerizing"]),
        "within_introduced_1pct_off_conversion_limit":
            conversion(totals["polymerizing"]) <= OFF_CONVERSION,
        "inhibitor_balance_error": balance_q,
        "radical_balance_error": balance_r, **totals,
    }


def integrate_leaky_intermediate(tau: float) -> dict:
    """Numerical check of u'=R-u/tau; X'=gamma*u/tau*(1-X).

    Exact input/decay updates; trapezoidal u quadrature plus analytic final tail.
    The integrated conversion dose equals gamma*integral(R dt), independent of
    tau for a complete history, although conversion timing changes.
    This identity is specific to these equations, not all intermediate chemistry.
    """
    u = 0.0
    integrated_u = 0.0
    input_dose = 0.0
    segments = [(0.04, PULSE_S), (0.0, GAP_S)] * 20
    for rate, duration in segments:
        steps = max(1, math.ceil(duration / min(tau / 200.0, 0.01)))
        dt = duration / steps
        decay = math.exp(-dt / tau)
        for _ in range(steps):
            u_next = rate * tau + (u - rate * tau) * decay
            integrated_u += (u + u_next) * dt / 2.0
            input_dose += rate * dt
            u = u_next
    integrated_u += tau * u  # all later decay included, no hidden discarded tail
    estimated_dose = GAMMA * integrated_u / tau
    exact_dose = GAMMA * input_dose
    assert abs(estimated_dose - exact_dose) < 2e-6
    return {
        "tau_s": tau, "conversion_exponent_exact": exact_dose,
        "conversion_exponent_quadrature_with_exact_tail": estimated_dose,
        "absolute_quadrature_error": abs(estimated_dose - exact_dose),
        "conversion_after_complete_tail": -math.expm1(-exact_dose),
    }


def main() -> None:
    direct = []
    for n in TARGET_PULSES:
        for exponent in [1, 2, 3, 4]:
            off_dose = n * BACKGROUND_INTENSITY**exponent * D_ON
            direct.append({
                "target_writes": n, "intensity_exponent": exponent,
                "background_intensity_ratio": BACKGROUND_INTENSITY,
                "off_conversion": -math.expm1(-off_dose),
                "within_introduced_limit": off_dose <= D_OFF,
            })
    required_exponent = math.log(D_OFF / (10000 * D_ON)) / math.log(
        BACKGROUND_INTENSITY)
    fresh = inhibited_step(1.0, R_ON, PULSE_S, R_REPLENISH)
    depleted = inhibited_step(0.0, R_ON, 1.0, R_REPLENISH)
    fresh_one_second = inhibited_step(1.0, R_ON, 1.0, R_REPLENISH)
    assert abs(conversion(fresh["polymerizing"]) - ON_CONVERSION) < 1e-12

    diffusion_m2_s = 1e-9
    reservoir_distance_m = 1e-3
    tau_diffusion_s = reservoir_distance_m**2 / (
        math.pi**2 * diffusion_m2_s)
    diffusion_r = 1.0 / tau_diffusion_s

    no_bypass = [
        schedule(n, BACKGROUND_INTENSITY, r)
        for r in [1.0, diffusion_r, 0.0] for n in TARGET_PULSES
    ]
    leakage = [
        schedule(10000, BACKGROUND_INTENSITY, 1.0, bypass=b)
        for b in [0.0, 1e-6, 5e-6, 1e-5, 1e-4]
    ]
    spatial_window = [
        schedule(10000, intensity, 1.0)
        for intensity in [0.005, 0.02, 0.20, 0.49, 0.51]
    ]
    fastest = schedule(10000, BACKGROUND_INTENSITY, 1.0)
    c0_mol_m3 = 1.0  # introduced 1 millimolar equivalent, not a selected molecule
    voxel_volume_m3 = 1e-9  # introduced 1 microliter
    hypothetical_uniform_bath_volume_m3 = 1e-5  # introduced 10 milliliters

    # Independent exact limits, not inferred from an assumed physical material.
    leakage_bound = D_OFF / (
        GAMMA * R_ON * BACKGROUND_INTENSITY * PULSE_S * 10000)
    raw_closed_pulses = 1.0 / (
        R_ON * BACKGROUND_INTENSITY * PULSE_S)
    tau_min = 1.0 / R_ON
    tau_max = 1.0 / (R_ON * BACKGROUND_INTENSITY)
    length_min = math.pi * math.sqrt(diffusion_m2_s * tau_min)
    length_max = math.pi * math.sqrt(diffusion_m2_s * tau_max)

    # Transport screen: a well-mixed V/Q model is a different introduced route
    # from diffusion. It DOES NOT provide an actual supply/return geometry.
    volume_mm3 = 1.0
    flow_mm3_s = R_REPLENISH * volume_mm3
    flow_area_mm2 = 1.0
    advection_mm_s = flow_mm3_s / flow_area_mm2

    # Deterministic finite corner checks of balance and concatenation.
    checks = 0
    for q0 in [0.0, 0.1, 1.0]:
        for rate in [0.0, 0.04, 2.0]:
            for r in [0.0, diffusion_r, 1.0]:
                for bypass in [0.0, 1e-5, 0.5]:
                    whole = inhibited_step(q0, rate, 2.0, r, bypass)
                    first = inhibited_step(q0, rate, 0.7, r, bypass)
                    second = inhibited_step(first["q1"], rate, 1.3, r, bypass)
                    assert abs(whole["q1"] - second["q1"]) < 1e-12
                    for k in ["raw", "scavenged", "polymerizing", "supplied"]:
                        assert abs(whole[k] - first[k] - second[k]) < 1e-12
                    checks += 1

    result = {
        "status": "INTRODUCED_MODEL_ONLY_NOT_A_PHYSICAL_INVENTION",
        "scope": [
            "No acoustic propagation, fitted cavitation or resin chemistry.",
            "Intensity contrast, radical power law, reservoirs and all numerical points introduced.",
            "Ideal stoichiometric scavenging with a reflected q>=0 state; finite bypass examined.",
            "No biological system, hardware, source recovery, producer execution or external dataset.",
            "Finite synthetic schedules are not material life, measured yield or full-cost advantage.",
        ],
        "inputs": {
            "on_conversion": ON_CONVERSION, "off_conversion_limit": OFF_CONVERSION,
            "on_log_conversion_dose": D_ON, "off_log_conversion_dose": D_OFF,
            "gamma": GAMMA, "on_radical_rate_per_s": R_ON,
            "background_intensity_ratio": BACKGROUND_INTENSITY,
            "replenish_rate_per_s_reference": R_REPLENISH,
            "active_pulse_s": PULSE_S, "between_pulse_idle_s": GAP_S,
        },
        "ordinary_positive_cumulative_conversion": {
            "rows": direct,
            "required_intensity_rate_exponent_at_10000_writes":
                required_exponent,
            "formula": "Xoff=1-exp(-N*eta**m*(-log(1-Xon)))",
        },
        "decaying_intermediate_without_resetting_irreversible_conversion": {
            "equations": "u'=R-u/tau; X'=gamma*u/tau*(1-X)",
            "complete_history_identity": "-log(1-X_final)=gamma*integral(R dt)",
            "rows": [integrate_leaky_intermediate(t) for t in [0.05, 1.0, 30.0]],
        },
        "ideal_scavenger_threshold_positive_opening": {
            "fresh_on_pulse": {**fresh, "conversion":
                conversion(fresh["polymerizing"])},
            "condition_for_constant_subthreshold_off_exposure":
                "(1-bypass)*Roff <= r; bypass=0 gives no conversion in THIS ideal model",
            "condition_for_finite_on_depletion": "(1-bypass)*Ron > r",
            "source_of_renewal": "constant-concentration external reservoir, all supplied inhibitor counted",
            "ordinary_same_gamma_on_time_without_inhibitor_s": D_ON / (GAMMA * R_ON),
            "on_time_factor_vs_same_gamma_uninhibited_rate":
                PULSE_S / (D_ON / (GAMMA * R_ON)),
            "no_bypass_schedules": no_bypass,
            "spatial_threshold_sensitivity": spatial_window,
        },
        "finite_bypass_and_finite_stock": {
            "leakage_schedules_10000": leakage,
            "maximum_bypass_for_1pct_off_conversion_at_reference": leakage_bound,
            "closed_uniform_initial_q_one_background_pulses_until_depletion":
                raw_closed_pulses,
            "fast_reference_10000_account": fastest,
            "introduced_C0_mol_per_m3": c0_mol_m3,
            "introduced_voxel_volume_m3": voxel_volume_m3,
            "inhibitor_consumed_at_one_voxel_mol":
                fastest["scavenged"] * c0_mol_m3 * voxel_volume_m3,
            "hypothetical_uniform_10ml_bath_consumption_mol":
                fastest["scavenged"] * c0_mol_m3 *
                hypothetical_uniform_bath_volume_m3,
            "uniform_bath_extrapolation_scope":
                "Only IF every bath voxel sees the SAME introduced background; not a computed field.",
        },
        "diffusion_and_flow_supply": {
            "introduced_diffusivity_m2_s": diffusion_m2_s,
            "introduced_reservoir_distance_m": reservoir_distance_m,
            "assumed_slab_relaxation_formula": "tau=L^2/(pi^2*D)",
            "diffusion_tau_s": tau_diffusion_s,
            "diffusion_rate_per_s": diffusion_r,
            "tau_window_s_strict": [tau_min, tau_max],
            "distance_window_m_strict_for_assumed_slab": [length_min, length_max],
            "introduced_well_mixed_voxel_mm3": volume_mm3,
            "required_throughflow_mm3_s_at_r_one": flow_mm3_s,
            "introduced_flow_cross_section_mm2": flow_area_mm2,
            "corresponding_mean_advection_mm_s": advection_mm_s,
            "advected_distance_in_fresh_on_pulse_mm": advection_mm_s * PULSE_S,
            "limits":
                "Neither a slab's dominant diffusion mode nor V/Q constructs coupled chemistry, a return route, stationary material, or finite reservoir restoration.",
        },
        "same_radical_emission_different_inhibitor_state_witness": {
            "common_radical_rate": R_ON, "common_duration_s": 1.0,
            "fresh_q_one_conversion": conversion(fresh_one_second["polymerizing"]),
            "depleted_q_zero_conversion": conversion(depleted["polymerizing"]),
            "scope":
                "Even exact observation of introduced R(t) alone does not reveal unknown initial q. Not an all-sensor impossibility or a calibrated acoustic observation law.",
        },
        "verification": {
            "analytic_constant_input_and_split_step_balance_checks": checks,
            "pulse_target_conversion_absolute_error":
                abs(conversion(fresh["polymerizing"]) - ON_CONVERSION),
            "finite_accounting_tolerance": 2e-8,
            "no_random_sampling": True,
        },
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n",
                   encoding="ascii")
    print(json.dumps({
        "output": str(out), "bytes": out.stat().st_size,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "on_pulse_s": PULSE_S,
        "required_power_order": required_exponent,
        "bypass_limit": leakage_bound,
        "diffusion_tau_s": tau_diffusion_s,
        "finite_closed_stock_pulses": raw_closed_pulses,
        "balance_checks": checks,
    }, indent=2))


if __name__ == "__main__":
    main()

