#!/usr/bin/env python3
"""Exact two-state gate algebra and scoped resonance-check throughput model.

This is a new calculation, not a replay of experimental data. The source inputs
are cited in READ_LEDGER.md; experimental rates are not fitted here.
"""

from fractions import Fraction
import math


def stationary_target(a: Fraction, b: Fraction, rate_ratio: Fraction) -> Fraction:
    """Target occupancy for outside->target probability a and
    target->outside probability b per reset, with r_out/r_in=rate_ratio.
    """
    return rate_ratio * a / (rate_ratio * a + b)


def required_rate_ratio(a: Fraction, b: Fraction, target: Fraction) -> Fraction:
    """Minimum r_out/r_in for stationary target occupancy >= target."""
    return target * b / ((1 - target) * a)


def pair_check_expected_attempts(p: float) -> float:
    """E[max(X1,X2)] for two independent geometric(p) check processes."""
    return 2.0 / p - 1.0 / (2.0 * p - p * p)


def pair_speedup(p: float, linewidth_gain: float) -> float:
    return linewidth_gain**2 / (1.0 + pair_check_expected_attempts(p))


def threshold_bisect(fn, lo: float, hi: float, iterations: int = 100) -> float:
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        if fn(mid) >= 1.0:
            hi = mid
        else:
            lo = mid
    return hi


def main() -> None:
    q = Fraction(1, 100)
    p_star = Fraction(99, 100)
    a, b = q, 1 - q
    ratio = required_rate_ratio(a, b, p_star)
    assert ratio == 9801
    assert stationary_target(a, b, ratio) == p_star

    # With equal event hazards, a/b >= target/(1-target). Keep a=q fixed
    # and solve for the largest permitted target->outside probability b.
    b_max = q * (1 - p_star) / p_star
    retention = 1 - b_max
    zero_failure_n_95 = math.ceil(math.log(0.05) / math.log(float(retention)))

    print("RESET GATE (exact fractions)")
    print(f"iid redraw q={q}; target={p_star}; required r_out/r_in={ratio}")
    print(
        "if outside->target remains q and hazards are equal, "
        f"target retention must be >= {retention} per event"
    )
    print(
        "zero observed exits needed to upper-bound that exit probability at "
        f"95% (iid Bernoulli assumption): {zero_failure_n_95}"
    )
    print(
        "if the two-state reset kernel stays row-identical, then a=q and "
        "b=1-q; any useful memory/correlation must change measured "
        "state-conditional transitions"
    )

    gamma_raw_ghz = 3.8
    gamma_rc_ghz = 0.110
    gamma_hom_ghz = 0.032
    linewidth_gain = gamma_raw_ghz / gamma_rc_ghz
    eta_sd = gamma_hom_ghz / gamma_raw_ghz
    threshold_effective_detection = threshold_bisect(
        lambda eta: pair_speedup(eta_sd * eta, linewidth_gain), 0.0, 1.0
    )

    print("\nPUBLISHED RC-PLE PAIR MODEL (scoped reconstruction)")
    print(f"raw FWHM={gamma_raw_ghz:g} GHz; RC FWHM={gamma_rc_ghz:g} GHz")
    print(f"linewidth gain={linewidth_gain:.9f}; eta_SD={eta_sd:.9f}")
    print(
        "effective per-pulse detection factor eta_det*eta_exc needed for "
        f"pair speedup >= 1: {threshold_effective_detection:.6f}"
    )
    for eta in (0.05, 0.10, 0.15, 0.20, 0.50, 1.00):
        p = eta_sd * eta  # eta represents eta_det*eta_exc, not measured data
        attempts = pair_check_expected_attempts(p)
        speedup = pair_speedup(p, linewidth_gain)
        print(
            f"eta_det*eta_exc={eta:.2f}: p={p:.7g}, "
            f"E[max checks]={attempts:.3f}, model speedup={speedup:.3f}"
        )

    # Optical energy at the emitter, inferred from the reported pre-circulator
    # P_sat, measured 50% grating efficiency, and 100 ns RC excitation pulse.
    p_sat_w = 1.3e-6
    grating_eff = 0.5
    pulse_s = 100e-9
    p_check_at_device_w = 0.016 * p_sat_w * grating_eff
    e_check_j = p_check_at_device_w * pulse_s
    p_probe_at_device_w = 0.008 * p_sat_w * grating_eff
    e_probe_j = p_probe_at_device_w * pulse_s
    print("\nINCIDENT OPTICAL PULSE ENERGY AT DEVICE (not wall-plug energy)")
    print(f"check pulse: {e_check_j:.6g} J ({e_check_j/1e-15:.6g} fJ)")
    print(f"probe pulse: {e_probe_j:.6g} J ({e_probe_j/1e-15:.6g} fJ)")
    print("Detector, optical-source, refrigerator and electrical costs remain unmeasured.")


if __name__ == "__main__":
    main()
