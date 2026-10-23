"""One finite-frequency reciprocal RC edge and local phasor-square update.

This is an analytic circuit check, not a device simulation or experiment.
The AD5292 wiper resistance and multiplier imperfections are deliberately
excluded from the ideal network calculation and are charged in the note.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


def main() -> None:
    # One output node is fed from a 10 V-peak AC source through the trainable
    # AD5292 rheostat, with a 100 kOhm load and 1 nF shunt capacitance.
    code = 683
    rab_ohm = 100_000.0
    g0_s = 10e-6
    cap_f = 1e-9
    frequency_hz = 1_000.0
    omega = 2 * math.pi * frequency_hz
    vin = 10.0 + 0.0j
    target = 6.0 - 1.0j
    teacher_transconductance_s = 10e-6
    probe_fraction = 0.1

    def state_for_code(wiper_code: int) -> tuple[float, complex, complex, float]:
        resistance = rab_ohm * wiper_code / 1024.0  # ideal tap law, no RW
        conductance = 1.0 / resistance
        admittance = conductance + g0_s + 1j * omega * cap_f
        output = conductance * vin / admittance
        edge_voltage = vin - output
        loss = 0.5 * abs(output - target) ** 2
        return conductance, output, edge_voltage, loss

    conductance, output, edge_voltage, loss_before = state_for_code(code)
    error = output - target
    admittance = conductance + g0_s + 1j * omega * cap_f

    # The free-run error is measured as an I/Q phasor, conjugated, and held.
    # A calibrated output transconductance turns it into the two signed probes.
    held_error_conjugate = error.conjugate()
    probe_current = probe_fraction * teacher_transconductance_s * held_error_conjugate
    adjoint_edge_response = -teacher_transconductance_s * held_error_conjugate / admittance
    edge_plus = edge_voltage + probe_fraction * adjoint_edge_response
    edge_minus = edge_voltage - probe_fraction * adjoint_edge_response

    # Local AD633 squaring followed by 2f I/Q lock-in. With unit peak references,
    # one AD633 square and two AD633 mixers return S/400 before post-gain,
    # where S is the complex phasor square of the edge voltage.
    square_plus = edge_plus**2
    square_minus = edge_minus**2
    normalized_lockin_difference = (square_plus - square_minus) / 400.0

    gradient_from_local_cell = -(
        (square_plus - square_minus).real / (4 * probe_fraction * teacher_transconductance_s)
    )
    dy_dg = vin * (g0_s + 1j * omega * cap_f) / admittance**2
    gradient_analytic = (error.conjugate() * dy_dg).real

    # Descend one AD5292 tap. Lower code means lower resistance and higher g.
    next_code = code - 1
    next_conductance, next_output, _, loss_after = state_for_code(next_code)

    tau_s = cap_f / (conductance + g0_s)
    cycles_per_lockin = 100
    epoch_s = 5 * tau_s + cycles_per_lockin / frequency_hz
    trainable_resistor_power_w = 0.5 * abs(edge_voltage) ** 2 * conductance
    load_power_w = 0.5 * abs(output) ** 2 * g0_s
    passive_real_power_w = trainable_resistor_power_w + load_power_w
    three_ad633_typical_power_w = 3 * 0.12

    data = {
        "scope": "one ideal reciprocal one-node RC network; analytic check only",
        "network": {
            "frequency_hz": frequency_hz,
            "omega_tau": omega * tau_s,
            "settling_tau_us": tau_s * 1e6,
            "settle_5tau_ms": 5 * tau_s * 1e3,
            "source_phasor_peak_V": [vin.real, vin.imag],
            "target_output_phasor_peak_V": [target.real, target.imag],
            "load_conductance_uS": g0_s * 1e6,
            "shunt_capacitance_nF": cap_f * 1e9,
            "digipot_code_ideal": code,
            "digipot_resistance_ohm_ideal": rab_ohm * code / 1024.0,
            "conductance_uS_ideal": conductance * 1e6,
            "output_phasor_peak_V": [output.real, output.imag],
            "edge_phasor_peak_V": [edge_voltage.real, edge_voltage.imag],
            "output_error_phasor_peak_V": [error.real, error.imag],
            "loss_before": loss_before,
        },
        "teacher_probe": {
            "held_error_conjugate_phasor_V": [held_error_conjugate.real, held_error_conjugate.imag],
            "teacher_transconductance_uS": teacher_transconductance_s * 1e6,
            "probe_fraction": probe_fraction,
            "signed_probe_current_phasor_peak_uA": [probe_current.real * 1e6, probe_current.imag * 1e6],
            "adjoint_edge_response_per_unit_probe_fraction_V": [
                adjoint_edge_response.real,
                adjoint_edge_response.imag,
            ],
            "edge_plus_phasor_peak_V": [edge_plus.real, edge_plus.imag],
            "edge_minus_phasor_peak_V": [edge_minus.real, edge_minus.imag],
        },
        "local_lockin": {
            "square_and_IQ_mixer_count_per_edge": 3,
            "complex_phasor_square_difference_V2": [
                (square_plus - square_minus).real,
                (square_plus - square_minus).imag,
            ],
            "raw_S_over_400_lockin_difference_V": [
                normalized_lockin_difference.real,
                normalized_lockin_difference.imag,
            ],
            "gradient_from_local_cell_V2_per_S": gradient_from_local_cell,
            "analytic_gradient_V2_per_S": gradient_analytic,
            "gradient_relative_error": abs(gradient_from_local_cell - gradient_analytic)
            / max(1.0, abs(gradient_analytic)),
        },
        "one_quantized_update": {
            "old_code": code,
            "new_code": next_code,
            "conductance_uS_before": conductance * 1e6,
            "conductance_uS_after": next_conductance * 1e6,
            "loss_before": loss_before,
            "loss_after": loss_after,
            "loss_decrease": loss_before - loss_after,
        },
        "timing": {
            "lockin_cycles_per_phase": cycles_per_lockin,
            "one_phase_s_including_5tau": epoch_s,
            "free_plus_plus_minus_update_s_approx": 3 * epoch_s,
        },
        "resource_estimates": {
            "trainable_r_real_power_mW": trainable_resistor_power_w * 1e3,
            "load_real_power_mW": load_power_w * 1e3,
            "passive_network_total_real_power_mW": passive_real_power_w * 1e3,
            "passive_network_energy_3epochs_mJ": passive_real_power_w * 3 * epoch_s * 1e3,
            "three_ad633_quiescent_power_typical_W_conservative_two_rail": three_ad633_typical_power_w,
            "three_ad633_energy_one_update_typical_J": three_ad633_typical_power_w * 3 * epoch_s,
        },
    }

    assert abs(gradient_from_local_cell - gradient_analytic) < 1e-7 * abs(gradient_analytic)
    assert loss_after < loss_before
    out = Path(__file__).with_name("cell_check.json")
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
