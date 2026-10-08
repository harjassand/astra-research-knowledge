#!/usr/bin/env python3
"""Exact checks for the c12 driven-chemistry Floquet boundary audit.

No kinetic simulation is performed. Fraction arithmetic verifies the source
parameter volume consequence and the clamped-precursor periodic-response
counterexample. Trigonometric terms are evaluated only at a phase where they
are exactly 0 or +/-1.
"""
from fractions import Fraction as F
from math import log


def bulk_exchange_coefficient(area: F, diffusivity: F, volume: F, layer: F) -> F:
    """Published code's bulk concentration exchange coefficient, in s^-1."""
    return area * diffusivity / ((volume - area * layer) * layer)


def periodic_product_at_trough(q: F, x_mean: F, amplitude: F,
                                reverse_rate: F, omega: F) -> F:
    """Exact periodic P at the trough for x=x_mean+amplitude*cos(omega*t)."""
    return q * x_mean - q * amplitude * reverse_rate**2 / (reverse_rate**2 + omega**2)


def derivative_at_trough(q: F, amplitude: F, reverse_rate: F,
                         omega: F) -> F:
    """dP/dt at phase omega*t=pi for the same driven precursor."""
    return -q * amplitude * reverse_rate * omega**2 / (reverse_rate**2 + omega**2)


def main() -> None:
    area = F(2, 10_000)             # 2e-4 m^2
    diffusivity = F(1, 1_000_000_000)  # 1e-9 m^2/s
    layer = F(1, 100_000)           # 1e-5 m
    volume_table = F(4, 1_000)      # 4e-3 m^3 as printed in 2026 Table 2
    volume_methods = F(4, 1_000_000)  # 4 mL = 4e-6 m^3 from Methods

    k_table = bulk_exchange_coefficient(area, diffusivity, volume_table, layer)
    k_methods = bulk_exchange_coefficient(area, diffusivity, volume_methods, layer)
    tau_table = 1 / k_table
    tau_methods = 1 / k_methods
    assert k_table < k_methods

    # Same chemical equilibrium ratio q=100, with the source's two chemical
    # relaxation rates: (100, 1)/s and (10,000, 100)/s.
    q = F(100)
    x_mean = F(51, 100)
    amplitude = F(1, 2)
    omega = F(1)
    x_trough = x_mean - amplitude
    assert x_trough == F(1, 100)

    v_slow = F(1)
    v_fast = F(100)
    p_slow = periodic_product_at_trough(q, x_mean, amplitude, v_slow, omega)
    p_fast = periodic_product_at_trough(q, x_mean, amplitude, v_fast, omega)
    branch_slow = x_trough + p_slow
    branch_fast = x_trough + p_fast
    trough_ratio = branch_fast / branch_slow

    # The period averages are q * mean(x) for both first-order reversible
    # products, so average branch inventories coincide exactly.
    pbar_slow = q * x_mean
    pbar_fast = q * x_mean
    branchbar = x_mean + q * x_mean
    assert p_slow == F(26)
    assert p_fast == F(10051, 10001)
    assert branch_fast == F(1015101, 1000100)
    assert branch_slow == F(2601, 100)
    assert trough_ratio == F(112789, 2890289)
    assert pbar_slow == pbar_fast == F(51)
    assert branchbar == F(5151, 100)

    # At the trough, x'=0. Compute the local log-slope of the branch ratio
    # and the linear timing window for 10% relative-ratio error.
    dslow = derivative_at_trough(q, amplitude, v_slow, omega)
    dfast = derivative_at_trough(q, amplitude, v_fast, omega)
    log_slope = dfast / branch_fast - dslow / branch_slow
    assert dslow == F(-25)
    assert dfast == F(-5000, 10001)

    print("bulk exchange coefficients from public source formula")
    print(f"table V=4e-3 m^3: k={float(k_table):.10g} s^-1, tau={float(tau_table):.6g} s")
    print(f"Methods V=4e-6 m^3: k={float(k_methods):.10g} s^-1, tau={float(tau_methods):.6g} s")
    print(f"tau ratio (table/Methods): {float(tau_table / tau_methods):.9g}")
    print("\nclamped-precursor illustration (not full paper model)")
    print(f"trough x={x_trough} M; P_slow={p_slow} M; P_fast={p_fast} M")
    print(f"instantaneous fast/slow branch ratio={trough_ratio}={float(trough_ratio):.9f}")
    print(f"period-mean branch inventories both={branchbar} M; ratio=1 exactly")
    print(f"trough log-ratio slope={float(log_slope):.9f} s^-1")
    print(f"linear 10% timing window={0.1 / abs(float(log_slope)):.6f} s")
    print(f"90% no-quench retention delay: P_slow={-log(0.9) / float(v_slow):.6f} s, P_fast={-log(0.9) / float(v_fast):.6f} s")


if __name__ == "__main__":
    main()
