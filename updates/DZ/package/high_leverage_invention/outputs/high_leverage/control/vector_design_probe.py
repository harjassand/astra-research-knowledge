#!/usr/bin/env python3
"""Explicit transit-compensated phase-sphere control; numerical model checks.

Construction was proposed by root; this independently reconstructs its
quadrature, positivity, waveform and finite-bandwidth spectrum. NumPy is used
for polynomial cubature and FFTs. No molecular parameters or experiments.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss, legval


def polynomial_kernel(dot, degree):
    coefficients = np.arange(degree + 1, dtype=float) * 2 + 1
    return legval(dot, coefficients)


def construction(degree, samples=32768):
    zs, zws = leggauss(degree + 1)
    zs, zws = zs[::-1], zws[::-1]
    theta = np.arccos(zs)
    azimuth = np.arange(2 * degree + 1) * 2 * np.pi / (2 * degree + 1)
    nodes = np.array([
        [np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)]
        for th in theta for ph in azimuth
    ])
    weights = np.repeat(zws / (2 * (2 * degree + 1)), 2 * degree + 1)
    ring_lengths = 2 * np.pi * np.sin(theta)
    meridian_range = theta[-1] - theta[0]
    length = float(sum(ring_lengths) + 2 * meridian_range)
    delta = 1 / (2 * (degree + 1) ** 2)

    # Exact for polynomial ring integrands, high-order quadrature on meridians.
    qp, qw = [], []
    qphi = np.arange(max(64, 2 * degree + 3)) * 2 * np.pi / max(64, 2 * degree + 3)
    for th, circumference in zip(theta, ring_lengths):
        for ph in qphi:
            qp.append([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
            qw.append(circumference / (length * len(qphi)))
    g, gw = leggauss(64)
    for th, w in zip(theta[0] + (g + 1) * meridian_range / 2, gw):
        qp.append([np.sin(th), 0, np.cos(th)])
        qw.append(w * meridian_range / length)
    qp, qw = np.array(qp), np.array(qw)
    assert abs(sum(qw) - 1) < 1e-13
    h = polynomial_kernel(nodes @ qp.T, degree) @ qw
    dwell = weights * (1 - delta * h)
    assert min(dwell / weights) >= 0.5 - 1e-12
    assert abs(sum(dwell) - (1 - delta)) < 1e-12

    moment_errors = []
    for a in range(degree + 1):
        for b in range(degree + 1 - a):
            for c in range(degree + 1 - a - b):
                pnodes = nodes[:, 0] ** a * nodes[:, 1] ** b * nodes[:, 2] ** c
                ppath = qp[:, 0] ** a * qp[:, 1] ** b * qp[:, 2] ** c
                obtained = float(dwell @ pnodes + delta * (qw @ ppath))
                if any(power % 2 for power in (a, b, c)):
                    expected = 0.0
                else:
                    expected = math.exp(
                        sum(math.lgamma((power + 1) / 2) for power in (a, b, c))
                        - math.lgamma((a + b + c + 3) / 2) - math.log(2 * np.pi)
                    )
                moment_errors.append(abs(obtained - expected))
    assert max(moment_errors) < 2e-12

    # Every segment is (duration, type, starting theta, starting phi, amount).
    segments = []
    mphi = len(azimuth)
    for row, th in enumerate(theta):
        for col, ph in enumerate(azimuth):
            segments.append((float(dwell[row * mphi + col]), "hold", th, ph, 0.0))
            amount = 2 * np.pi / mphi
            segments.append((delta * np.sin(th) * amount / length, "phi", th, ph, amount))
        if row < len(theta) - 1:
            amount = theta[row + 1] - th
            segments.append((delta * amount / length, "theta", th, 0.0, amount))
    segments.append((delta * meridian_range / length, "theta", theta[-1], 0.0, -meridian_range))
    durations = np.array([seg[0] for seg in segments])
    assert abs(sum(durations) - 1) < 1e-12
    ends = np.cumsum(durations)
    starts = np.r_[0.0, ends[:-1]]
    times = np.arange(samples) / samples
    indices = np.searchsorted(ends, times, side="right")
    path = np.empty((samples, 3))
    for i, (duration, kind, th, ph, amount) in enumerate(segments):
        selected = indices == i
        frac = (times[selected] - starts[i]) / duration
        this_th = th + amount * frac if kind == "theta" else np.full(len(frac), th)
        this_ph = ph + amount * frac if kind == "phi" else np.full(len(frac), ph)
        path[selected] = np.column_stack((
            np.sin(this_th) * np.cos(this_ph),
            np.sin(this_th) * np.sin(this_ph), np.cos(this_th)))
    # Physical phase is pi * path, with |d|=1. Total period normalized to1.
    phase = np.pi * path
    a_norm = np.pi * length / np.sqrt(delta)
    summary = {
        "degree": degree,
        "nodes": len(nodes),
        "unit_sphere_path_length": length,
        "transit_fraction": delta,
        "minimum_dwell_over_cubature_weight": float(min(dwell / weights)),
        "maximum_monomial_error": float(max(moment_errors)),
        "normalized_RMS_phase_velocity": float(a_norm),
        "Omega_over_A": float(2 * np.pi / a_norm),
        "peak_field_over_RMS": float(1 / np.sqrt(delta)),
    }
    return phase, a_norm, summary


def orientation_nodes(m=10):
    z, w = leggauss(m)
    phi = np.arange(2 * m) * np.pi / m
    nodes = np.array([[np.sqrt(1 - a * a) * np.cos(p),
                       np.sqrt(1 - a * a) * np.sin(p), a] for a in z for p in phi])
    weights = np.repeat(w / (4 * m), 2 * m)
    return nodes, weights


def spectral_probe(phase, a_norm, cutoff):
    count = len(phase)
    harmonics = np.fft.fftfreq(count, 1 / count)
    if cutoff is not None:
        coeff = np.fft.fft(phase, axis=0) / count
        fejer = np.maximum(1 - abs(harmonics) / (cutoff + 1), 0)
        phase_filtered = np.fft.ifft(coeff * fejer[:, None], axis=0).real * count
        field_rms = float(np.sqrt(np.sum((2 * np.pi * harmonics[:, None]) ** 2 * abs(coeff * fejer[:, None]) ** 2)))
        field = np.fft.ifft(2j * np.pi * harmonics[:, None] * coeff * fejer[:, None], axis=0).real * count
        field_peak = float(np.max(np.linalg.norm(field, axis=1)))
        assert field_rms <= a_norm * 1.001
    else:
        phase_filtered = phase
        field_rms = a_norm
        field_peak = None
    directions, direction_weights = orientation_nodes()
    average_spectrum = np.zeros(count)
    maximum_carrier_amplitude = 0.0
    for start in range(0, len(directions), 8):
        ds = directions[start:start + 8]
        ws = direction_weights[start:start + 8]
        u = np.exp(-1j * (phase_filtered @ ds.T))
        coeffs = np.fft.fft(u, axis=0) / count
        average_spectrum += abs(coeffs) ** 2 @ ws
        maximum_carrier_amplitude = max(maximum_carrier_amplitude, float(max(abs(coeffs[0]))))
    assert abs(sum(average_spectrum) - 1) < 1e-11
    def relative_rate(x):
        return float(sum(average_spectrum / (1 + (harmonics * 2 * np.pi * x / field_rms) ** 2)))

    thresholds = []
    for gain in (10, 100):
        target = 1 / gain
        if average_spectrum[0] >= target:
            thresholds.append({"ensemble_initial_rate_reduction": gain, "reachable": False,
                               "reason": "carrier floor exceeds target rate"})
            continue
        lo, hi = 0.0, 1.0
        while relative_rate(hi) > target:
            hi *= 2
        for _ in range(55):
            mid = (lo + hi) / 2
            if relative_rate(mid) > target:
                lo = mid
            else:
                hi = mid
        thresholds.append({"ensemble_initial_rate_reduction": gain, "reachable": True,
                           "A_over_kappa": hi,
                           "Omega_over_kappa": 2 * np.pi * hi / field_rms,
                           "bandwidth_over_kappa": None if cutoff is None else cutoff * 2 * np.pi * hi / field_rms,
                           "peak_A_over_kappa": None if field_peak is None else hi * field_peak / field_rms})
    xs = (10, 15.0442331186, 30, 50, 100, 156.4401, 300, 1000, 3000)
    rates = []
    for x in xs:
        frequencies_over_kappa = harmonics * 2 * np.pi * x / field_rms
        relative = relative_rate(x)
        rates.append({
            "A_over_kappa": x,
            "ensemble_rate_relative_to_no_control": relative,
            "static_ensemble_rate": math.atan(x) / x,
            "bandwidth_over_kappa": None if cutoff is None else cutoff * 2 * np.pi * x / field_rms,
        })
    return {
        "fejer_cutoff": cutoff,
        "RMS_phase_velocity_after_filter": field_rms,
        "peak_field_over_RMS_on_time_grid": None if field_peak is None else field_peak / field_rms,
        "maximum_carrier_amplitude_on_orientation_grid": maximum_carrier_amplitude,
        "ensemble_carrier_weight": float(average_spectrum[0]),
        "gain_thresholds": thresholds,
        "rate_grid": rates,
    }


def main():
    out = []
    for degree in (2, 3, 4, 6):
        phase, a_norm, summary = construction(degree)
        summary["spectral_probes"] = [spectral_probe(phase, a_norm, k) for k in (None, 64, 256)]
        out.append(summary)
        print(json.dumps({"degree": degree,
                          "moment_error": summary["maximum_monomial_error"],
                          "Omega_over_A": summary["Omega_over_A"],
                          "carrier": summary["spectral_probes"][0]["ensemble_carrier_weight"]}))
    dest = Path(__file__).with_name("vector_design_results.json")
    dest.write_text(json.dumps({
        "scope": "Model-only numerical cubature and Fourier checks; not physical validation or uniform proof.",
        "orientation_grid_size": 200,
        "time_samples": 32768,
        "constructions": out,
    }, indent=2) + "\n")
    print(str(dest))


if __name__ == "__main__":
    main()
