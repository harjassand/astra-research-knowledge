#!/usr/bin/env python3
"""Reconstruct the 2026 JACS irreversible 1->2->3 model under both volumes.

This is an independent implementation of the paper's stated linear transport
matrix and Table 2 Butler-Volmer/Tafel parameters for its ideal square wave.
It uses a Taylor/scaling-and-squaring matrix exponential, exact constant-rate
half-cycle propagation, and matrix powering for the 3 h wall-clock horizon.
It omits the source's optional square-wave smoothing, double-layer capacitance,
surface chemistry, and side reactions. Therefore its outputs test parameter
sensitivity; they are not represented as a reproduction of Figure 5.
"""
from __future__ import annotations

from math import ceil, log2
import numpy as np


FARADAY = 96485.33212331
GAS = 8.31446261815324
TEMP = 298.0
AREA = 2.0e-4
DIFFUSIVITY = 1.0e-9
LAYER = 1.0e-5
K0 = (2.0e-3, 1.0e-3)  # m/s, for 1->2 and 2->3
ALPHA = 0.5
NE = 2
E0 = (-2.82, -3.15)
HORIZONS = {
    "experiment_3h": 3.0 * 60.0 * 60.0,
    "paper_model_3d": 3.0 * 24.0 * 60.0 * 60.0,
}


def expm_taylor_scaling(a: np.ndarray) -> np.ndarray:
    """Matrix exponential for the small stable matrices used in this audit."""
    norm = float(np.linalg.norm(a, ord=np.inf))
    if norm == 0.0:
        return np.eye(a.shape[0])
    scale = max(0, int(ceil(log2(norm / 0.5))))
    b = a / (2**scale)
    identity = np.eye(a.shape[0])
    total = identity.copy()
    term = identity.copy()
    for k in range(1, 100):
        term = term @ b / k
        total = total + term
        if np.linalg.norm(term, ord=np.inf) < 2.0e-17:
            break
    else:
        raise ArithmeticError("Taylor series did not converge")
    for _ in range(scale):
        total = total @ total
    return total


def rate_matrix(volume: float, potential: float) -> np.ndarray:
    """Copy of the public solver's 3-species, surface/bulk rate matrix."""
    n = 6
    k = np.zeros((n, n), dtype=float)
    k_surface_bulk = DIFFUSIVITY / LAYER**2
    k_bulk_surface = AREA * DIFFUSIVITY / ((volume - AREA * LAYER) * LAYER)
    for species in range(3):
        surface, bulk = 2 * species, 2 * species + 1
        k[surface, surface] -= k_surface_bulk
        k[surface, bulk] += k_surface_bulk
        k[bulk, surface] += k_bulk_surface
        k[bulk, bulk] -= k_bulk_surface

    # Reduction-only branch, matching the irreversible 1+2e->2, 2+2e->3
    # mechanism represented in Table 2.
    f_over_rt = FARADAY / (GAS * TEMP)
    for oxidant_index, k0, e0 in ((0, K0[0], E0[0]), (1, K0[1], E0[1])):
        reductant_index = oxidant_index + 1
        rate = k0 / LAYER * np.exp(-ALPHA * NE * f_over_rt * (potential - e0))
        source = 2 * oxidant_index
        target = 2 * reductant_index
        k[source, source] -= rate
        k[target, source] += rate
    return k


def one_period_map(volume: float, frequency: float) -> np.ndarray:
    """Ideal Table-2 square wave: +0.8 V then -2.8 V, half duty each."""
    half = 0.5 / frequency
    positive = expm_taylor_scaling(rate_matrix(volume, 0.8) * half)
    negative = expm_taylor_scaling(rate_matrix(volume, -2.8) * half)
    return negative @ positive


def weighted_species_fractions(state: np.ndarray, volume: float) -> tuple[float, float, float]:
    surface_volume = AREA * LAYER
    bulk_volume = volume - surface_volume
    amounts = np.array([
        surface_volume * state[2 * i] + bulk_volume * state[2 * i + 1]
        for i in range(3)
    ])
    return tuple(float(x / volume) for x in amounts)


def outcome(volume: float, frequency: float, elapsed: float) -> dict[str, float]:
    # Code initializes every species at the same surface and bulk concentration;
    # set species 1 to one and products to zero as in the source reaction.
    state0 = np.array([1.0, 1.0, 0.0, 0.0, 0.0, 0.0])
    periods = round(elapsed * frequency)
    assert abs(periods / frequency - elapsed) < 1.0e-10
    period = one_period_map(volume, frequency)
    state = np.linalg.matrix_power(period, periods) @ state0
    s1, s2, s3 = weighted_species_fractions(state, volume)
    conversion = 1.0 - s1
    selectivity2 = s2 / (s2 + s3) if s2 + s3 else float("nan")
    q_over_2f = s2 + 2.0 * s3
    return {
        "frequency_hz": frequency,
        "cycles": float(periods),
        "S1_unreacted": s1,
        "S2_intermediate_yield": s2,
        "S3_overreduction_yield": s3,
        "conversion": conversion,
        "selectivity2_among_products": selectivity2,
        "Q_over_2F_per_initial_mole": q_over_2f,
        "mass_balance": s1 + s2 + s3,
    }


def main() -> None:
    volumes = {
        "Table2_4L": 4.0e-3,
        "Methods_4mL": 4.0e-6,
    }
    frequencies = (1.0, 3.0, 10.0, 20.0, 60.0)
    for horizon_name, elapsed in HORIZONS.items():
        for label, volume in volumes.items():
            print(f"\n{horizon_name}, {label}: V={volume:g} m^3, elapsed={elapsed:g} s")
            for frequency in frequencies:
                result = outcome(volume, frequency, elapsed)
                assert abs(result["mass_balance"] - 1.0) < 2e-8, result
                print(" ".join(f"{key}={value:.8g}" for key, value in result.items()))


if __name__ == "__main__":
    main()
