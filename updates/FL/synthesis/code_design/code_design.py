#!/usr/bin/env python3
"""Reproduce the finite-slew isotope-code design calculations.

Uses only the Python standard library. The waveform is the peak-slew,
tau-antiperiodic ramp/plateau code derived in PROOF.md. Product histories are
the synthetic E/O four-carbon age laws from the supplied FL ancestry report.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


CONTRAST = 0.98
PURE_H = (1.0 + CONTRAST) / 2.0
PURE_L = (1.0 - CONTRAST) / 2.0
TARGET_Z = (0.5, 1.0, 1.5, 2.0, 3.0, math.pi, 4.0, 5.0, 10.0)


def q_slew_opt(z: float) -> float:
    """Maximum mean u^4 for a tau-antiperiodic code with ||u'|| <= M, z=M*tau."""
    if z <= 2.0:
        return z**4 / 80.0
    return 1.0 - 8.0 / (5.0 * z)


def q_single_sine(z: float) -> float:
    """Mean u^4 for u=A*cos(pi*t/tau), with the same maximum slew M."""
    amplitude = min(1.0, z / math.pi)
    return 3.0 * amplitude**4 / 8.0


def u_phase(phase: float, z: float) -> float:
    """Unit-period-in-tau antiperiodic peak-slew waveform, period 2 tau."""
    phase %= 2.0
    if z <= 2.0:
        amplitude = z / 2.0
        if phase < 1.0:
            return -amplitude + z * phase
        return amplitude - z * (phase - 1.0)

    ramp = 2.0 / z
    if phase < ramp:
        return -1.0 + z * phase
    if phase < 1.0:
        return 1.0
    if phase < 1.0 + ramp:
        return 1.0 - z * (phase - 1.0)
    return -1.0


def count_distribution(high_probabilities: list[float]) -> list[float]:
    dist = [1.0]
    for p in high_probabilities:
        nxt = [0.0] * (len(dist) + 1)
        for k, mass in enumerate(dist):
            nxt[k] += mass * (1.0 - p)
            nxt[k + 1] += mass * p
        dist = nxt
    return dist


def pooled_histogram_tv(z: float) -> tuple[float, list[float], list[float], float]:
    """Integrate the E/O count laws exactly with 3-point Gaussian quadrature.

    Each waveform segment is affine or constant, while each isotope-count
    probability is a polynomial of degree at most four in the waveform value.
    Three-point Gauss-Legendre integration is therefore exact on every segment.
    """
    p_even = [0.0] * 5
    p_odd = [0.0] * 5
    q_numeric = 0.0
    gl_nodes = (-math.sqrt(3.0 / 5.0), 0.0, math.sqrt(3.0 / 5.0))
    gl_weights = (5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0)
    if z <= 2.0:
        segments = ((0.0, 1.0), (1.0, 2.0))
    else:
        ramp = 2.0 / z
        segments = ((0.0, ramp), (ramp, 1.0), (1.0, 1.0 + ramp), (1.0 + ramp, 2.0))
    for lo, hi in segments:
        mid = (lo + hi) / 2.0
        half = (hi - lo) / 2.0
        for node, gl_weight in zip(gl_nodes, gl_weights):
            phase = mid + half * node
            v = u_phase(phase, z)
            phase_weight = half * gl_weight / 2.0  # normalized by the period 2*tau
            q_numeric += phase_weight * v**4
            for bits in itertools.product((0, 1), repeat=4):
                parity = sum(bits) & 1
                target = p_odd if parity else p_even
                probs = [
                    (1.0 + CONTRAST * ((-1.0) ** (j + bit)) * v) / 2.0
                    for j, bit in enumerate(bits)
                ]
                mass = phase_weight / 8.0
                for k, value in enumerate(count_distribution(probs)):
                    target[k] += mass * value

    tv = 0.5 * sum(abs(e - o) for e, o in zip(p_even, p_odd))
    return tv, p_even, p_odd, q_numeric


def hoeffding_odd_n95(signal: float) -> int:
    """Odd N sufficient for <=5% majority-parity error by Hoeffding's bound."""
    if signal <= 0.0:
        return math.inf  # type: ignore[return-value]
    n = math.ceil(2.0 * math.log(20.0) / signal**2)
    if n % 2 == 0:
        n += 1
    return n


def row(z: float) -> dict[str, float | int]:
    q_square = q_slew_opt(z)
    q_sine = q_single_sine(z)
    signal = CONTRAST**4 * q_square
    return {
        "slew_times_tau_z": z,
        "q_slew_opt": q_square,
        "q_single_sine": q_sine,
        "q_ratio_square_to_sine": q_square / q_sine if q_sine else math.inf,
        "purity_contrast_a": CONTRAST,
        "a4": CONTRAST**4,
        "raw_parity_gap_E_minus_O": 2.0 * signal,
        "single_product_TV": signal,
        "single_product_equal_prior_bayes_error": (1.0 - signal) / 2.0,
        "odd_N_sufficient_for_95pct_majority": hoeffding_odd_n95(signal),
    }


def main() -> None:
    rows = [row(z) for z in TARGET_Z]
    hist_checks = []
    for z in (0.5, 1.0, 2.0, math.pi, 5.0, 10.0):
        tv, pe, po, q_num = pooled_histogram_tv(z)
        tv_exact = CONTRAST**4 * q_slew_opt(z)
        hist_checks.append(
            {
                "z": z,
                "q_numeric": q_num,
                "q_formula": q_slew_opt(z),
                "TV_numeric_full_five_bin": tv,
                "TV_formula": tv_exact,
                "absolute_TV_residual": abs(tv - tv_exact),
                "even_count_distribution": pe,
                "odd_count_distribution": po,
            }
        )
        if abs(tv - tv_exact) > 2e-12:
            raise AssertionError(f"full histogram TV identity failed at z={z}: {tv} vs {tv_exact}")

    payload = {
        "schema": "fl-code-design-results/1",
        "scope": "Synthetic four-carbon E/O benchmark; deterministic, phase-pooled code; independent product draws only.",
        "contrast": CONTRAST,
        "p_low": PURE_L,
        "p_high": PURE_H,
        "table": rows,
        "full_histogram_checks": hist_checks,
        "periodic_code_accounting": {
            "period_over_tau": 2,
            "switches_per_tau": 1,
            "switches_in_2000_tau": 2000,
            "cycles_in_2000_tau": 1000,
            "heavy_fraction_per_integer_cycle": 0.5,
            "heavy_feed_dose_in_2000_tau": "1000 * F * tau",
            "minimum_precode_history_for_Cmax": "Cmax + 4*tau",
            "unknown_Cmax": "UNKNOWN; carry an explicit unprepared-history fraction or measure wash-in",
        },
    }
    out = Path(__file__).with_name("CODE_DESIGN_NUMERICS.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    print("z,q_slew,q_sine,TV,one_product_error,N95_Hoeffding")
    for item in rows:
        print(
            f"{item['slew_times_tau_z']:.6g},"
            f"{item['q_slew_opt']:.8g},"
            f"{item['q_single_sine']:.8g},"
            f"{item['single_product_TV']:.8g},"
            f"{item['single_product_equal_prior_bayes_error']:.8g},"
            f"{item['odd_N_sufficient_for_95pct_majority']}"
        )
    print(f"max full-histogram TV residual: {max(x['absolute_TV_residual'] for x in hist_checks):.3g}")


if __name__ == "__main__":
    main()
