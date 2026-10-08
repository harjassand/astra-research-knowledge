"""Illustrative Poisson-arrival continuity and phase-readout budget.

This is a design fixture, not data from the cited optical-clock apparatus.
"""

from __future__ import annotations

import json
import math


def main() -> None:
    tau_s = 0.75
    flux_per_s = 24.0
    averaging_s = 86_400.0
    contrast = 1.0

    mean_occupancy = flux_per_s * tau_s
    expected_long_gaps = flux_per_s * averaging_s * math.exp(-mean_occupancy)
    atoms = flux_per_s * averaging_s
    qpn_frequency_sd_hz = 1.0 / (
        2.0 * math.pi * contrast * tau_s * math.sqrt(atoms)
    )
    result = {
        "status": "illustrative model fixture, not device data",
        "transit_time_s": tau_s,
        "arrival_flux_per_s": flux_per_s,
        "averaging_time_s": averaging_s,
        "mean_in_zone_atoms": mean_occupancy,
        "poisson_pointwise_empty_probability": math.exp(-mean_occupancy),
        "poisson_pointwise_occupancy_cv": 1.0 / math.sqrt(mean_occupancy),
        "expected_uncovered_gaps_upper_scale": expected_long_gaps,
        "total_atoms": atoms,
        "ideal_midfringe_qpn_sd_hz": qpn_frequency_sd_hz,
        "first_rectangular_kernel_zero_hz": 1.0 / tau_s,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
