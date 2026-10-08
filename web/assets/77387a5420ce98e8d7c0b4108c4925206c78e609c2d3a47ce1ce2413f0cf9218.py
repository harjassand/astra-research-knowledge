"""Design a first-order action-matched pulse from a measured kernel.

This module implements only the finite-dimensional pulse-allocation step.
The stochastic model, action path, kernel, observation-noise law, and actuator
calibration must be acquired separately. It does not certify biological
validity or the Freidlin--Wentzell approximation.
"""

from __future__ import annotations

import math
from typing import Any, Sequence


def _trapz(values: Sequence[float], times: Sequence[float]) -> float:
    if len(values) != len(times) or len(values) < 2:
        raise ValueError("values and times must have the same length >= 2")
    out = 0.0
    for i in range(len(values) - 1):
        dt = times[i + 1] - times[i]
        if dt <= 0:
            raise ValueError("times must be strictly increasing")
        out += 0.5 * dt * (values[i] + values[i + 1])
    return out


def design_matched_pulse(
    times: Sequence[float],
    kernel_estimate: Sequence[float],
    *,
    observation_sigma: float,
    observations_per_bin: int,
    observation_alpha: float,
    dose_energy: float,
    required_action_decrease: float,
    actuator_gain_sigma: float,
    actuator_z: float,
    timing_jitter_sigma: float = 0.0,
    max_amplitude: float | None = None,
    endpoint_sensitivity: float | None = None,
    endpoint_specificity: float | None = None,
    endpoint_delta: float | None = None,
    endpoint_alpha: float = 0.05,
) -> dict[str, Any]:
    """Return a lower-kernel positive pulse and acquisition-cost estimates.

    The action kernel is assumed nonnegative only where its lower confidence
    bound is positive; bins with uncertain sign receive no dose. Confidence
    uses a union bound over bins and sub-Gaussian per-cell measurement noise.
    Multiplicative actuator error is debited with a one-sided normal quantile.
    Timing jitter uses a small-jitter expected-gain expansion; callers should
    replace it by direct convolution when jitter is not small. That timing
    adjustment is not a confidence bound.
    """
    if len(times) != len(kernel_estimate) or len(times) < 2:
        raise ValueError("times and kernel_estimate must have the same length >= 2")
    if observations_per_bin < 1 or observation_sigma < 0:
        raise ValueError("invalid observation model")
    if not 0 < observation_alpha < 1:
        raise ValueError("observation_alpha must lie in (0,1)")
    if dose_energy < 0 or required_action_decrease < 0:
        raise ValueError("dose_energy and required_action_decrease must be nonnegative")

    bins = len(times)
    point_error = observation_sigma * math.sqrt(
        2.0 * math.log(2.0 * bins / observation_alpha) / observations_per_bin
    )
    lower_kernel = [max(0.0, float(k) - point_error) for k in kernel_estimate]
    lower_norm = math.sqrt(_trapz([k * k for k in lower_kernel], times))
    if max_amplitude is not None and max_amplitude < 0:
        raise ValueError("max_amplitude must be nonnegative")
    if lower_norm == 0.0:
        pulse = [0.0] * bins
        nominal_gain = 0.0
    else:
        scale = math.sqrt(dose_energy) / lower_norm
        pulse = [scale * k for k in lower_kernel]
        if max_amplitude is not None:
            def capped_waveform(lam: float) -> list[float]:
                return [min(max_amplitude, lam * k) for k in lower_kernel]

            if max(pulse) > max_amplitude:
                max_energy = _trapz(
                    [max_amplitude**2 if k > 0 else 0.0 for k in lower_kernel],
                    times,
                )
                energy_target = min(dose_energy, max_energy)
                # Monotone KKT water-filling for u=min(u_max,lambda*kappa).
                if energy_target <= 0:
                    pulse = [0.0] * bins
                else:
                    lo, hi = 0.0, max(1.0, scale)
                    while _trapz([u * u for u in capped_waveform(hi)], times) < energy_target:
                        hi *= 2.0
                    for _ in range(80):
                        lam = 0.5 * (lo + hi)
                        candidate = capped_waveform(lam)
                        if _trapz([u * u for u in candidate], times) < energy_target:
                            lo = lam
                        else:
                            hi = lam
                    pulse = capped_waveform(hi)
        nominal_gain = _trapz(
            [u * k for u, k in zip(pulse, lower_kernel)], times
        )

    actuator_gain_factor = 1.0 - actuator_z * actuator_gain_sigma
    if actuator_gain_factor < 0:
        actuator_gain_factor = 0.0

    # Estimate ||kappa'||_2^2 by centered finite differences for the local
    # small-jitter approximation to the pulse/kernel autocorrelation.
    if bins >= 3:
        derivative = []
        for i in range(bins):
            if i == 0:
                derivative.append((lower_kernel[1] - lower_kernel[0]) / (times[1] - times[0]))
            elif i == bins - 1:
                derivative.append((lower_kernel[-1] - lower_kernel[-2]) / (times[-1] - times[-2]))
            else:
                derivative.append((lower_kernel[i + 1] - lower_kernel[i - 1]) / (times[i + 1] - times[i - 1]))
        derivative_norm2 = _trapz([d * d for d in derivative], times)
    else:
        derivative_norm2 = 0.0
    timing_factor = 1.0
    if lower_norm > 0:
        timing_factor = max(
            0.0,
            1.0
            - timing_jitter_sigma**2
            * derivative_norm2
            / (2.0 * lower_norm**2),
        )
    adjusted_gain = nominal_gain * actuator_gain_factor * timing_factor
    required_mean_gain = math.inf
    if actuator_gain_factor > 0 and timing_factor > 0:
        required_mean_gain = required_action_decrease / (
            actuator_gain_factor * timing_factor
        )

    def energy_for_gain(target_gain: float) -> float:
        if target_gain <= 0:
            return 0.0
        if lower_norm == 0:
            return math.inf
        if max_amplitude is None:
            return (target_gain / lower_norm) ** 2
        window = times[-1] - times[0]
        maximum_gain = max_amplitude * _trapz(lower_kernel, times)
        if target_gain > maximum_gain:
            return math.inf
        lo, hi = 0.0, 1.0
        def gain_at(lam: float) -> float:
            candidate = [min(max_amplitude, lam * k) for k in lower_kernel]
            return _trapz([u * k for u, k in zip(candidate, lower_kernel)], times)
        while gain_at(hi) < target_gain:
            hi *= 2.0
        for _ in range(80):
            lam = 0.5 * (lo + hi)
            if gain_at(lam) < target_gain:
                lo = lam
            else:
                hi = lam
        candidate = [min(max_amplitude, hi * k) for k in lower_kernel]
        return _trapz([u * u for u in candidate], times)

    required_energy = energy_for_gain(required_action_decrease)
    adjusted_required_energy = energy_for_gain(required_mean_gain)

    result: dict[str, Any] = {
        "pulse": pulse,
        "lower_kernel": lower_kernel,
        "pointwise_observation_error": point_error,
        "simultaneous_kernel_confidence": 1.0 - observation_alpha,
        "lineage_observations": observations_per_bin * bins,
        "lower_kernel_l2_norm": lower_norm,
        "nominal_action_decrease_at_requested_energy": nominal_gain,
        "actuator_gain_lower_factor": actuator_gain_factor,
        "timing_jitter_small_noise_factor": timing_factor,
        "action_decrease_after_amplitude_lcb_and_mean_timing_adjustment": adjusted_gain,
        "required_energy_for_action_decrease_nominal": required_energy,
        "required_energy_after_amplitude_lcb_and_mean_timing_adjustment": adjusted_required_energy,
    }

    if endpoint_sensitivity is not None or endpoint_specificity is not None or endpoint_delta is not None:
        if endpoint_sensitivity is None or endpoint_specificity is None or endpoint_delta is None:
            raise ValueError("supply sensitivity, specificity, and endpoint_delta together")
        margin = endpoint_sensitivity + endpoint_specificity - 1.0
        if margin <= 0 or not 0 < endpoint_alpha < 1 or endpoint_delta <= 0:
            raise ValueError("invalid endpoint assay parameters")
        result["endpoint_cells_for_precision"] = math.ceil(
            math.log(2.0 / endpoint_alpha)
            / (2.0 * margin**2 * endpoint_delta**2)
        )
        result["endpoint_probability_half_width_bound"] = math.sqrt(
            math.log(2.0 / endpoint_alpha)
            / (2.0 * result["endpoint_cells_for_precision"])
        ) / margin

    return result
