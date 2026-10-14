"""Arithmetic screens for the energy/control report.

These are conditional engineering examples, not predictions of an integrated
device. The 1 W, 0.2 Hz and 1.43% numbers came from different published
operating points and are deliberately kept as separate labels in the output.
"""

import json
import math
from pathlib import Path


def pump_fraction(delta_p_pa, rho_cp_j_m3_k, fluid_delta_t_k, pump_efficiency):
    return delta_p_pa / (rho_cp_j_m3_k * fluid_delta_t_k * pump_efficiency)


def robust_fraction(resistance_ratio):
    root = math.sqrt(resistance_ratio)
    return 4 * root / (1 + root) ** 2


def thermal_clock(th, tc, t_up, t_down, c, g_on, g_leak):
    g_total = g_on + g_leak
    hot_limit = (g_on * th + g_leak * tc) / g_total
    cold_limit = (g_on * tc + g_leak * th) / g_total
    if not (cold_limit < t_down < t_up < hot_limit):
        return {"oscillates": False, "hot_limit_K": hot_limit, "cold_limit_K": cold_limit}
    hot_time = c / g_total * math.log((hot_limit - t_down) / (hot_limit - t_up))
    cold_time = c / g_total * math.log((t_up - cold_limit) / (t_down - cold_limit))
    return {
        "oscillates": True,
        "hot_limit_K": hot_limit,
        "cold_limit_K": cold_limit,
        "hot_time_s": hot_time,
        "cold_time_s": cold_time,
        "frequency_Hz_before_switching_delay": 1 / (hot_time + cold_time),
    }


def main():
    # 2022 Nature reports up to 1.43% module-level heat-to-electric efficiency.
    # Treating it as if a separate 1 W generator attained that same point is
    # explicitly a counterfactual sensitivity exercise.
    illustrative_conversion_efficiency = 0.0143
    reported_output_w = 1.0
    reported_frequency_hz = 0.2
    rho_cp = 4.2e6  # water, illustrative volumetric heat capacity J/m3/K
    pump_eff = 0.30  # illustrative shaft-to-fluid efficiency
    pump_cases = []
    for dp, dt in [(100_000, 10), (200_000, 5)]:
        f = pump_fraction(dp, rho_cp, dt, pump_eff)
        pump_cases.append(
            {
                "pressure_drop_Pa": dp,
                "fluid_delta_T_K": dt,
                "pump_fraction_of_hot_heat": f,
                "illustrative_hot_heat_for_1_W_W": reported_output_w / illustrative_conversion_efficiency,
                "illustrative_pump_W": f * reported_output_w / illustrative_conversion_efficiency,
                "illustrative_net_before_other_losses_W": reported_output_w
                - f * reported_output_w / illustrative_conversion_efficiency,
            }
        )
    output = {
        "provenance_note": "Conditional arithmetic only; 1 W at 0.2 Hz is the 2026 Joule report, whereas 1.43% is a 2022 Nature best efficiency at a different operating point. Neither paper measured the hybrid device.",
        "source_reported_1W_at_0p2Hz_implies_J_per_cycle": reported_output_w / reported_frequency_hz,
        "pump_break_even_pressure_Pa_at_10K": illustrative_conversion_efficiency * rho_cp * 10 * pump_eff,
        "pump_break_even_pressure_Pa_at_5K": illustrative_conversion_efficiency * rho_cp * 5 * pump_eff,
        "pump_cases": pump_cases,
        "thermal_clock_illustration_not_device_data": thermal_clock(
            th=373.15,
            tc=293.15,
            t_up=353.15,
            t_down=313.15,
            c=10.0,
            g_on=1.0,
            g_leak=0.1,
        ),
        "fixed_load_min_fraction_at_Rs_ratio_4": robust_fraction(4),
        "fixed_load_min_fraction_at_Rs_ratio_16": robust_fraction(16),
    }
    out_path = Path(__file__).with_name("CALCULATIONS.json")
    out_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
