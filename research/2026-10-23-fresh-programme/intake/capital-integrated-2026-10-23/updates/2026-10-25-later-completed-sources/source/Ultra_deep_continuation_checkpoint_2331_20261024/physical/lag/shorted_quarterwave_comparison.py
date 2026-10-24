#!/usr/bin/env python3
"""Real-port finite TEM check for shorted quarter-wave shunt filters.

Uses only numpy and the exact lossless-line ABCD model.  Port reference planes
are at the first and last shunt planes, so N stubs have N-1 intervening
quarter-wave main sections.  The code charges every distributed line and stub
in the aggregate C/L/delay/length ledger and integrates all harmonic replicas.
"""
import json
import math
from pathlib import Path

import numpy as np

Z0 = 50.0
F0 = 6.0e9
TAU = 1.0 / (4.0 * F0)
TEMP = 0.100
KB = 1.380649e-23
H = 6.62607015e-34
C_LIGHT = 299792458.0
FUN = 2.0 * KB * TEMP / H


def line_abcd(freq, z, delay):
    phase = 2.0 * np.pi * freq * delay
    c, s = np.cos(phase), np.sin(phase)
    return c, 1j * z * s, 1j * s / z, c


def shunt_abcd(y):
    return (np.ones_like(y, dtype=complex), np.zeros_like(y, dtype=complex),
            y, np.ones_like(y, dtype=complex))


def cascade(a, b):
    aa, ab, ac, ad = a
    ba, bb, bc, bd = b
    return (aa * ba + ab * bc, aa * bb + ab * bd,
            ac * ba + ad * bc, ac * bb + ad * bd)


def sparams(abcd):
    a, b, c, d = abcd
    den = a + b / Z0 + c * Z0 + d
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        s21 = 2.0 / den
        s11 = (a + b / Z0 - c * Z0 - d) / den
    s21 = np.where(np.isfinite(s21), s21, 0j)
    s11 = np.where(np.isfinite(s11), s11, 1 + 0j)
    return s21, s11


def short_stub_filter(freq, n):
    """N shorted quarter-wave shunts, with N-1 matched quarter-wave links."""
    omega_tau = 2.0 * np.pi * freq * TAU
    sn, cs = np.sin(omega_tau), np.cos(omega_tau)
    # A shorted line has Y=-i*cot(omega*t)/Z.  At sin=0 its shunt is a
    # short circuit and the through amplitude is exactly zero.
    pole = np.abs(sn) < 2e-14
    y = np.zeros_like(freq, dtype=complex)
    safe = ~pole
    y[safe] = -1j * cs[safe] / (Z0 * sn[safe])
    stub = shunt_abcd(y)
    qline = line_abcd(freq, Z0, TAU)
    total = stub
    for _ in range(n - 1):
        total = cascade(cascade(total, qline), stub)
    s21, s11 = sparams(total)
    s21[pole] = 0j
    s11[pole] = 1 + 0j
    return s21, s11


def open_stub_winner(freq):
    """Prior matched-line/open-stub global-budget comparator, exact line model."""
    delay_main = 95.63015320e-12
    z_stub = 5.0
    c_stub = 3.825206128e-12
    omega = 2.0 * np.pi * freq
    phase = omega * z_stub * c_stub
    # Open-stub Y=i*tan(omega*Z*C)/Z.  Handle poles by their limiting S21=0.
    cos_phase = np.cos(phase)
    pole = np.abs(cos_phase) < 2e-14
    y = np.zeros_like(freq, dtype=complex)
    safe = ~pole
    y[safe] = 1j * np.sin(phase[safe]) / (z_stub * cos_phase[safe])
    stub = shunt_abcd(y)
    half = line_abcd(freq, Z0, delay_main / 2.0)
    total = cascade(cascade(half, stub), half)
    s21, s11 = sparams(total)
    s21[pole] = 0j
    s11[pole] = 1 + 0j
    return s21, s11


def bose_weight(u):
    out = np.ones_like(u)
    nz = u > 0
    # Equivalent to (u/sinh(u))^2, stable over the integration interval.
    out[nz] = (2.0 * u[nz] * np.exp(-u[nz]) /
               (-np.expm1(-2.0 * u[nz]))) ** 2
    return out


def simpson(y, h):
    return h / 3.0 * (y[0] + y[-1] + 4.0 * np.sum(y[1:-1:2]) +
                      2.0 * np.sum(y[2:-1:2]))


def integrate(transmission, cutoff=15.0, points=640001):
    u = np.linspace(0.0, cutoff, points)
    freq = u * FUN
    s21, s11 = transmission(freq)
    t = np.abs(s21) ** 2
    refl = np.abs(s11) ** 2
    tail = (math.exp(-2.0 * cutoff) *
            (2.0 * cutoff**2 + 2.0 * cutoff + 1.0) /
            (1.0 - math.exp(-2.0 * cutoff))**2)
    return float(simpson(bose_weight(u) * t, cutoff / (points - 1))), tail, float(np.max(np.abs(t + refl - 1.0)))


def resources(n):
    # Every quarter-wave 50-ohm TEM segment has these integrated resources.
    c_seg = TAU / Z0
    l_seg = Z0 * TAU
    n_main = n - 1
    n_all = 2 * n - 1
    return {
        "stubs": n,
        "main_sections": n_main,
        "quarter_wave_segments_total": n_all,
        "C_total_F": n_all * c_seg,
        "L_total_H": n_all * l_seg,
        "C_stub_total_F": n * c_seg,
        "L_stub_total_H": n * l_seg,
        "C_main_total_F": n_main * c_seg,
        "L_main_total_H": n_main * l_seg,
        "main_delay_s": n_main * TAU,
        "summed_delay_s": n_all * TAU,
        "summed_length_m_vacuum_velocity": n_all * C_LIGHT * TAU,
        "one_segment_delay_s": TAU,
        "one_segment_length_m_vacuum_velocity": C_LIGHT * TAU,
    }


def window_metrics(transmission, points=20001):
    f = np.linspace(5.9e9, 6.1e9, points)
    s21, _ = transmission(f)
    t = np.abs(s21) ** 2
    return {
        "T_min": float(np.min(t)),
        "T_max": float(np.max(t)),
        "T_5p9GHz": float(t[0]),
        "T_6GHz": float(t[points // 2]),
        "T_6p1GHz": float(t[-1]),
        "S21_5p9GHz": [float(s21[0].real), float(s21[0].imag)],
        "S21_6GHz": [float(s21[points // 2].real), float(s21[points // 2].imag)],
        "S21_6p1GHz": [float(s21[-1].real), float(s21[-1].imag)],
    }


def main():
    rows = []
    for n in range(1, 5):
        fn = lambda f, n=n: short_stub_filter(f, n)
        j, tail, passivity = integrate(fn)
        rows.append({
            "N": n,
            "J_dimensionless": j,
            "integral_tail_upper_after_u15": tail,
            "window_5p9_to_6p1GHz": window_metrics(fn),
            "max_abs_power_balance_error_on_u_grid": passivity,
            "resources": resources(n),
        })

    open_j, open_tail, open_passivity = integrate(open_stub_winner)
    open_resources = {
        "main_delay_s": 95.63015320e-12,
        "main_C_F": 95.63015320e-12 / Z0,
        "main_L_H": Z0 * 95.63015320e-12,
        "stub_C_F": 3.825206128e-12,
        "stub_L_H": 5.0**2 * 3.825206128e-12,
        "stub_delay_s": 5.0 * 3.825206128e-12,
        "C_total_F": 95.63015320e-12 / Z0 + 3.825206128e-12,
        "L_total_H": Z0 * 95.63015320e-12 + 5.0**2 * 3.825206128e-12,
    }
    open_result = {
        "J_dimensionless": open_j,
        "integral_tail_upper_after_u15": open_tail,
        "window_5p9_to_6p1GHz": window_metrics(open_stub_winner),
        "max_abs_power_balance_error_on_u_grid": open_passivity,
        "resources": open_resources,
    }
    budgets = {"C_max_F": 5.73781e-12, "L_max_H": 33.8362e-9,
               "main_delay_max_s": 95.6302e-12}
    for row in rows:
        r = row["resources"]
        row["within_aggregate_budgets"] = {
            "C": r["C_total_F"] <= budgets["C_max_F"],
            "L": r["L_total_H"] <= budgets["L_max_H"],
            "main_delay": r["main_delay_s"] <= budgets["main_delay_max_s"],
        }
    out = {
        "model": "lossless uniform 50-ohm TEM, real 50-ohm resistor ports",
        "port_plane_convention": "first/last shunt planes; N stubs, N-1 intervening quarter-wave main lines",
        "temperature_K": TEMP,
        "carrier_Hz": F0,
        "window_Hz": [5.9e9, 6.1e9],
        "Bose_frequency_unit_Hz": FUN,
        "quarter_wave_delay_s": TAU,
        "quarter_wave_C_F": TAU / Z0,
        "quarter_wave_L_H": Z0 * TAU,
        "quarter_wave_length_m_vacuum_velocity": C_LIGHT * TAU,
        "aggregate_caps": budgets,
        "shorted_stub_filters": rows,
        "prior_open_stub_winner": open_result,
        "integration": {
            "dimensionless_variable": "u=f/(2 k_B T/h)",
            "range": [0.0, 15.0],
            "even_simpson_points": 640001,
            "tail_bound_using_T_le_1": open_tail,
        },
        "scope": "finite ideal TEM circuit comparison only; no junction, footprint, loss, or experimental claim",
    }
    path = Path(__file__).with_name("shorted_quarterwave_results.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
