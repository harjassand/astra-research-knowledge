#!/usr/bin/env python3
"""Conditional noisy-interface calculation; dimensionless, not material data.

The wall is an existing flat interface. It undergoes overdamped Brownian
motion with constant drive only during the pulse and thermal noise satisfying
D = mu*kBT. Bulk nucleation, pinning, latent heat, and material-specific
couplings are intentionally not assigned values here.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def binary_kl(p: float, q: float) -> float:
    p = min(max(p, 1e-300), 1.0 - 1e-16)
    q = min(max(q, 1e-300), 1.0 - 1e-16)
    return p * math.log(p / q) + (1.0 - p) * math.log((1.0 - p) / (1.0 - q))


def binary_entropy(p: float) -> float:
    p = min(max(p, 1e-300), 1.0 - 1e-16)
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def main() -> None:
    # Illustrative dimensionless values. For a phi^4 kink with delta=1,
    # integral (m')^2 dx = 4/3; Gamma=1 and wall area A=1.
    delta = 1.0
    gamma = 1.0
    area = 1.0
    beta = 1.0
    field_h = 0.02
    pulse_t = 10_000.0
    field_free_hold_t = 100.0
    target_advance = 100.0

    kink_norm = 4.0 / (3.0 * delta)
    mobility = gamma / (area * kink_norm)
    diffusion = mobility / beta
    force = 2.0 * field_h * area
    velocity = mobility * force
    total_observation_t = pulse_t + field_free_hold_t
    variance_x = 2.0 * diffusion * total_observation_t
    sigma_x = math.sqrt(variance_x)

    p_target = cdf((velocity * pulse_t - target_advance) / sigma_x)
    p_target_reversed = cdf((-velocity * pulse_t - target_advance) / sigma_x)
    p_target_unbiased = cdf(-target_advance / sigma_x)
    p_positive_sign = cdf(velocity * pulse_t / sigma_x)
    p_positive_sign_unbiased = 0.5

    mean_work = force * velocity * pulse_t
    work_variance = 2.0 * force * force * diffusion * pulse_t
    path_kl = velocity * velocity * pulse_t / (4.0 * diffusion)
    output = {
        "status": "dimensionless conditional Brownian wall model; not material data",
        "assumptions": [
            "one pre-existing flat boundary; no bulk nucleation or pinning",
            "constant effective force during pulse, then zero drive",
            "overdamped Gaussian thermal noise with Einstein relation",
            "target is final wall advance at least L after the field-free hold",
        ],
        "parameters": {
            "kBT_units": 1.0 / beta,
            "phi4_kink_width_delta": delta,
            "wall_area_A": area,
            "gamma": gamma,
            "field_h_per_volume": field_h,
            "pulse_duration": pulse_t,
            "field_free_hold": field_free_hold_t,
            "target_advance_L": target_advance,
        },
        "derived": {
            "kink_norm_integral_mprime_squared": kink_norm,
            "wall_mobility": mobility,
            "wall_diffusion": diffusion,
            "effective_force": force,
            "drift_velocity": velocity,
            "endpoint_variance": variance_x,
            "endpoint_sigma": sigma_x,
            "target_probability_plus_drive": p_target,
            "target_probability_reversed_drive": p_target_reversed,
            "target_probability_unbiased": p_target_unbiased,
            "positive_sign_probability_plus_drive": p_positive_sign,
            "positive_sign_probability_unbiased": p_positive_sign_unbiased,
            "mean_drive_work_kBT": mean_work,
            "drive_work_variance_kBT_squared": work_variance,
            "controlled_vs_uncontrolled_path_KL": path_kl,
            "binary_endpoint_target_KL_lower_bound": binary_kl(p_target, p_target_unbiased),
            "binary_sign_information_floor_kBT": math.log(2.0) - binary_entropy(p_positive_sign),
            "binary_sign_record_reset_floor_kBT": binary_entropy(p_positive_sign),
        },
        "check": {
            "beta_mean_work_equals_four_times_path_kl": abs(beta * mean_work - 4.0 * path_kl),
            "controlled_vs_uncontrolled_target_KL_le_path_KL": binary_kl(p_target, p_target_unbiased) <= path_kl + 1e-12,
        },
    }
    path = Path(__file__).with_name("continuum_wall_results.json")
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
