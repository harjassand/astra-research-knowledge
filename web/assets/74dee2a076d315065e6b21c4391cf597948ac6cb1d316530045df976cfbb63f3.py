#!/usr/bin/env python3
"""Two-state detailed-balance counterexample for fixed-time state occupancy.

States are U (unfolded) and N (native), with U->N rate kf and N->U rate ku.
Multiplying both rates by s leaves the Boltzmann equilibrium occupancy fixed,
but changes native-state occupancy at any finite sampling time. This is not a
first-passage probability.
"""

from __future__ import annotations

import math


def native_occupancy(kf: float, ku: float, sample_time: float) -> float:
    """Native-state probability at sample_time, starting from unfolded U."""
    if kf < 0 or ku < 0 or sample_time < 0 or kf + ku == 0:
        raise ValueError("rates must be nonnegative, total rate positive, sample time nonnegative")
    pi_native = kf / (kf + ku)
    return pi_native * -math.expm1(-(kf + ku) * sample_time)


def minimum_relaxation_rate(pi_native: float, target_occupancy: float, sample_time: float) -> float:
    """Smallest total rate lambda needed for the occupancy from initial U."""
    if not (0 < pi_native <= 1 and 0 <= target_occupancy < pi_native and sample_time > 0):
        raise ValueError("require 0 < pi_native <= 1, 0 <= target < pi_native, sample time > 0")
    return -math.log1p(-target_occupancy / pi_native) / sample_time


def main() -> None:
    # Ratios set pi_N=0.95. Both pairs have exactly the same equilibrium law.
    fast = (0.95, 0.05)
    slow = (0.95e-8, 0.05e-8)
    sample_time = 1.0
    target_occupancy = 0.90
    print(f"equilibrium pi_N (fast, slow): {fast[0]/sum(fast):.6f}, {slow[0]/sum(slow):.6f}")
    print(f"native occupancy at t={sample_time:g} (fast, slow): "
          f"{native_occupancy(*fast, sample_time):.6f}, "
          f"{native_occupancy(*slow, sample_time):.10f}")
    print(f"minimum total relaxation rate for occupancy {target_occupancy:.2f} at t={sample_time:g}: "
          f"{minimum_relaxation_rate(0.95, target_occupancy, sample_time):.6f}")


if __name__ == "__main__":
    main()
