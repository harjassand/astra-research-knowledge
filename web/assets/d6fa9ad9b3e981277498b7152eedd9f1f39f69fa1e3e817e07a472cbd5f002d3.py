#!/usr/bin/env python3
"""Numerical diagnostic for the A16 Gaussian fixed-window model.

This samples the declared stochastic model. It is not a device simulation or
experimental validation. All parameters are exposed in main().
"""

from math import ceil, erfc, log, sqrt
from random import Random
from statistics import NormalDist


KB = 1.380649e-23


def gaussian_tail(z):
    return 0.5 * erfc(z / sqrt(2.0))


def integration_time(kbt, lam, voltage, weight_l1, kappa, margin, delta,
                     capacitance, readout_charge_sd):
    q = NormalDist().inv_cdf(1.0 - delta)
    signal_rate = lam * voltage * margin * weight_l1
    noise_rate = 2.0 * kbt * lam * kappa * weight_l1
    initial_variance = capacitance * kbt + readout_charge_sd**2
    return (q*q*noise_rate + sqrt(q**4*noise_rate**2
                                  + 4.0*q*q*signal_rate**2*initial_variance)) \
           / (2.0*signal_rate**2)


def main():
    # Deliberately explicit illustrative values; these are not claimed as a
    # measured implementation. A 3-bit ADC is the digital input interface.
    temperature = 300.0
    kbt = KB * temperature
    lam = 1.0e-4       # S, total differential conductance scale for ||w||_1=1
    voltage = 0.05     # V
    weight_l1 = 1.0
    kappa = 1.5         # equivalent Johnson-noise conductance factor
    gamma = 0.25
    rho = 0.02
    epsilon_x = 0.02
    epsilon_o = 0.01
    margin = gamma - rho - epsilon_x - epsilon_o
    delta = 0.01
    capacitance = 1.0e-13  # F
    readout_charge_sd = 1.0e-17  # C, illustrative comparator/sampling noise
    front_end_time_floor = 1.0e-9  # s, illustrative measured-bandwidth slot
    switch_cap = 1.0e-16  # F per input gate
    switch_voltage = 0.5  # V
    switches_per_input = 2
    control_cap = 1.0e-14  # F, illustrative broadcast line
    latch_energy = 1.0e-14  # J, illustrative, not measured
    adc_fj_per_level = 0.85  # source-reported 200-kHz example, not matched
    n = 256

    t_noise = integration_time(kbt, lam, voltage, weight_l1, kappa, margin,
                               delta, capacitance, readout_charge_sd)
    # The bandwidth/settling slot is a separately charged physical constraint.
    t = max(t_noise, front_end_time_floor)
    q = NormalDist().inv_cdf(1.0 - delta)
    signal_noise = lam * voltage * margin * weight_l1 * t_noise
    variance_noise = (2.0*kbt*lam*kappa*weight_l1*t_noise
                      + capacitance*kbt + readout_charge_sd**2)
    predicted_noise_error = gaussian_tail(signal_noise / sqrt(variance_noise))
    signal = lam * voltage * margin * weight_l1 * t
    variance = (2.0*kbt*lam*kappa*weight_l1*t
                + capacitance*kbt + readout_charge_sd**2)
    predicted_error = gaussian_tail(signal / sqrt(variance))

    trials = 300_000
    rng = Random(20261009)
    noise_bound_errors = sum(
        signal_noise + rng.gauss(0.0, sqrt(variance_noise)) < 0.0
        for _ in range(trials)
    )
    actual_errors = sum(
        signal + rng.gauss(0.0, sqrt(variance)) < 0.0
        for _ in range(trials)
    )

    branch_energy = lam * voltage**2 * weight_l1 * t
    q_full_scale = lam * voltage * weight_l1 * t
    capacitor_energy = q_full_scale**2 / (2.0*capacitance)
    gate_energy = (switches_per_input*n*0.5*switch_cap*switch_voltage**2
                   + 0.5*control_cap*switch_voltage**2)
    physical_subtotal = branch_energy + capacitor_energy + gate_energy + latch_energy
    adc_bits = ceil(log(2.0/gamma, 2.0))
    adc_energy_per_input = adc_fj_per_level * (2**adc_bits) * 1.0e-15
    digital_adc_energy = n * adc_energy_per_input

    print(f"N={n}, gamma={gamma}, deterministic_error_budget="
          f"{rho+epsilon_x+epsilon_o}, effective_margin={margin}")
    print(f"q_delta={q:.9f}, t_noise_bound_s={t_noise:.9e}, "
          f"analytic_error_at_bound={predicted_noise_error:.9g}, "
          f"MC_errors_at_bound={noise_bound_errors}/{trials}, "
          f"MC_rate_at_bound={noise_bound_errors/trials:.9g}")
    print(f"front_end_floor_s={front_end_time_floor:.9e}, "
          f"operation_integration_s={t:.9e}, analytic_error_at_operation="
          f"{predicted_error:.9g}, MC_errors_at_operation={actual_errors}/{trials}")
    print(f"branch_dissipation_J={branch_energy:.9e}, "
          f"full_scale_capacitor_energy_J={capacitor_energy:.9e}")
    print(f"switch_and_control_energy_J={gate_energy:.9e}, "
          f"illustrative_latch_energy_J={latch_energy:.9e}")
    print(f"illustrative_physical_subtotal_J={physical_subtotal:.9e}")
    print(f"ADC_bits={adc_bits}, source_example_ADC_energy_per_channel_J="
          f"{adc_energy_per_input:.9e}, N_channel_ADC_energy_J={digital_adc_energy:.9e}")
    print("WARNING: the ADC datum is a source-reported low-rate example; these "
          "numbers do not match process, latency, volume, calibration, or "
          "complete peripherals and are not an energy-advantage claim.")


if __name__ == "__main__":
    main()
