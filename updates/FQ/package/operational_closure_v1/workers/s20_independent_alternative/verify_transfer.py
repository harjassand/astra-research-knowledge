#!/usr/bin/env python3
"""Dimensionless checks for the ideal persistent-reserve quench model.

These are circuit identities and hypothetical arithmetic, not a magnet simulation.
"""

from math import exp, sqrt


def record(k: float, energy_joule: float) -> dict[str, float]:
    if not (0 < k < 1):
        raise ValueError("k must lie strictly between zero and one")
    return {
        "k": k,
        "leakage_fraction": 1 - k * k,
        "retained_field_fraction_equal_coils": k,
        "primary_joule_heat": energy_joule * (1 - k * k),
    }


def trajectory(k: float, t_over_tau: float) -> tuple[float, float]:
    """(primary current, reserve current) / initial primary current."""
    primary = exp(-t_over_tau)
    reserve = k * (1 - primary)
    return primary, reserve


def main() -> None:
    # A primary source reports k=0.97 for a small bifilar REBCO coil.
    # The 436.6 MJ comparison is for a different proposed magnet; this is
    # strictly a scale illustration, not a physical prediction for it.
    energy = 436.6e6
    for k in (0.97, 0.999, 0.999999):
        print(record(k, energy))

    # Exact energy bookkeeping at a finite dimensionless time with L=I0=1.
    for k in (0.97, 0.999):
        for t in (0.0, 0.1, 1.0, 10.0):
            i1, i2 = trajectory(k, t)
            magnetic = 0.5 * (i1 * i1 + i2 * i2 + 2 * k * i1 * i2)
            heat = 0.5 * (1 - k * k) * (1 - i1 * i1)
            assert abs(magnetic + heat - 0.5) < 1e-12
    print("finite-time energy identity: PASS")

    for allowed_heat_fraction in (0.01, 0.001, 1e-6):
        print({
            "allowed_heat_fraction": allowed_heat_fraction,
            "minimum_k": sqrt(1 - allowed_heat_fraction),
        })

    e = 0.01
    k_modes = (1 - e * e) / (1 + e * e)
    print({
        "two_mode_e": e,
        "two_mode_k": k_modes,
        "two_mode_heat_fraction": 1 - k_modes * k_modes,
        "weak_harmonic_final_over_initial": -k_modes,
    })


if __name__ == "__main__":
    main()
