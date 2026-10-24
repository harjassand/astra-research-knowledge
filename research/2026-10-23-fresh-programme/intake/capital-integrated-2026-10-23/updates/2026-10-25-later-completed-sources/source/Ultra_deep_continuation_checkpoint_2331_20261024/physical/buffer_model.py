"""Finite-port temporal buffer and explicit transformer boundary checks.

NumPy/stdlib only.  This is a declared narrow-band passive input-output model,
not a whole-device calibration or a quantum-SQUID simulation.  The collision
check is an exactly unitary discretization, converging to the continuous-bin
input-output model; finite-bin emitted-mode noise is not asserted identical.
No fitted
experimental rates are invented by this script.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HBAR = 1.054571817e-34
PLANCK = 6.62607015e-34
KB = 1.380649e-23
PHI0 = 2.067833848e-15


def occupation(frequency_hz: float, temperature_k: float) -> float:
    return 1.0 / math.expm1(PLANCK * frequency_hz / (KB * temperature_k))


def release_weights(k_port: float, k_internal: float, duration: float) -> dict:
    """Exact selected emitted mode, constant rates, no second-port leak."""
    r = k_port + k_internal
    z = r * duration
    e = math.exp(-z)
    beta = k_port / r
    delta = k_internal / r
    z_e = z / math.expm1(z) if z < 700 else 0.0
    eta = beta * (-math.expm1(-z))
    port_noise = delta**2 + beta**2 * e + 2 * beta * delta * z_e
    internal_noise = beta * delta * (1 + e - 2 * z_e)
    assert abs(eta + port_noise + internal_noise - 1) < 2e-14
    return dict(memory=eta, port_noise=port_noise, internal_noise=internal_noise)


def periodic_two_bath(kh_integral: float, kc_integral: float,
                      n_hot: float, n_cold: float) -> dict:
    a, b = math.exp(-kh_integral), math.exp(-kc_integral)
    n0 = (n_cold * (1 - b) + b * n_hot * (1 - a)) / (1 - a * b)
    n1 = n_hot + (n0 - n_hot) * a
    n2 = n_cold + (n1 - n_cold) * b
    heat_quanta = (n_hot - n_cold) * (1 - a) * (1 - b) / (1 - a * b)
    assert abs(n2 - n0) < 2e-14
    assert abs((n1 - n0) - heat_quanta) < 2e-14
    return dict(n_before_hot=n0, n_after_hot=n1, heat_quanta=heat_quanta,
                eta_signal=(1 - a) * (1 - b),
                heat_factor=(1 - a) * (1 - b) / (1 - a * b))


def collision_dilation(k_port: float, k_internal: float, duration: float,
                        bins: int = 120) -> dict:
    """Exact two-stage dilation: three physical ports in each finite time bin.

    Port ordering is H,C,i. A bright-mode beam splitter of transmissivity
    exp(-sum(k)*dt) is used in each bin; all dark bath combinations are kept.
    These are a finite-bin realization, not a declaration of a thermal source's
    arbitrary-state preparation or a finite Maxwell environment.
    """
    steps = 2 * bins
    dim = 1 + 3 * steps
    u = np.eye(dim, dtype=float)
    groups = {f"{stage}_{port}": []
              for stage in ("capture", "release") for port in ("H", "C", "i")}
    capture_row = None
    release_memory_amplitudes = []
    release_c_rows = []
    # An independent release propagation column starts at one in the memory.
    release_column = np.zeros(dim)
    release_column[0] = 1.0
    dt = duration / bins
    for step in range(steps):
        stage = "capture" if step < bins else "release"
        rates = np.array([k_port, 0.0, k_internal] if step < bins
                         else [0.0, k_port, k_internal])
        total = float(sum(rates))
        weights = np.sqrt(rates / total)
        c = math.exp(-total * dt / 2)
        s = math.sqrt(-math.expm1(-total * dt))
        block = np.eye(4)
        block[0, 0] = c
        block[0, 1:] = s * weights
        block[1:, 0] = -s * weights
        block[1:, 1:] += (c - 1) * np.outer(weights, weights)
        idx = [0] + list(range(1 + 3 * step, 4 + 3 * step))
        u[idx, :] = block @ u[idx, :]
        for p, port in enumerate(("H", "C", "i")):
            groups[f"{stage}_{port}"].append(idx[p + 1])
        if step == bins - 1:
            capture_row = u[0].copy()
        if step >= bins:
            release_column[idx] = block @ release_column[idx]
            release_memory_amplitudes.append(release_column[idx[2]])
            release_c_rows.append(idx[2])
    assert capture_row is not None
    eta_c = float(sum(capture_row[groups["capture_H"]] ** 2))
    vr = np.asarray(release_memory_amplitudes)
    eta_r = float(vr @ vr)
    f_out = vr / math.sqrt(eta_r)
    out = f_out @ u[release_c_rows, :]
    eta = float(sum(out[groups["capture_H"]] ** 2))
    parts = {name: float(sum(out[idx] ** 2)) for name, idx in groups.items()}
    parts["initial_memory"] = float(out[0] ** 2)
    assert abs(sum(parts.values()) - 1) < 2e-13
    assert abs(eta - eta_c * eta_r) < 2e-13
    analytic = release_weights(k_port, k_internal, duration)
    assert abs(eta_r - analytic["memory"]) < 2e-13
    # Finite collision bins keep all port combinations and are unitary. Their
    # emitted temporal-mode noise weights converge to the continuous formula;
    # unlike final-memory loss, those weights are not identical at finite dt.
    release_noise_error = max(abs(parts["release_C"] - analytic["port_noise"]),
                              abs(parts["release_i"] - analytic["internal_noise"]))
    assert release_noise_error < 1e-6
    return dict(bins_per_stage=bins, eta_capture=eta_c, eta_release=eta_r,
                eta_signal=eta, output_noise_weights=parts,
                continuous_release_noise_error=release_noise_error,
                unitarity_error=float(np.max(np.abs(u @ u.T - np.eye(dim)))),
                selected_row_commutator_error=abs(float(out @ out) - 1))


def transformer(s: complex, ls: float) -> tuple[complex, complex]:
    l1 = l2 = 480e-12
    mutual = -138e-12
    resistance = 50.0
    lp, lsec, me = l1 + ls, l2 + ls, mutual + ls
    z = s * lp - s * s * me * me / (resistance + s * lsec)
    zp = lp - me * me * (2 * s * resistance + s * s * lsec) / (
        resistance + s * lsec) ** 2
    return z, zp


def two_port_poles() -> dict:
    """Static poles of the finite linear-SQUID / exact-TEM boundary model."""
    f0, zr = 6.57e9, 80.0
    w0 = 2 * math.pi * f0
    off = 138e-12
    lp_off = 618e-12
    # Same physical near-ground tap scale as the conventional resonator.
    theta_d = math.pi / 32
    td = theta_d / w0
    to = math.atan(1 / math.tan(theta_d) + 2 * zr / (w0 * lp_off)) / w0

    def admittance(s: complex, settings: tuple[float, float]):
        sh, ch = np.sinh(s * td), np.cosh(s * td)
        co = np.cosh(s * to)
        value = (np.tanh(s * to) + ch / sh) / zr
        deriv = (to / (co * co) - td / (sh * sh)) / zr
        for ls in settings:
            z, zp = transformer(s, ls)
            value += 1 / z
            deriv -= zp / (z * z)
        return value, deriv

    def pole(settings, guess):
        s = complex(guess)
        for _ in range(100):
            y, yp = admittance(s, settings)
            shift = y / yp
            s -= shift
            if abs(shift) < 1e-6:
                break
        assert abs(admittance(s, settings)[0]) < 1e-9
        return s

    rows = []
    guess = 1j * w0
    ic = 1.6e-6
    lmin = PHI0 / (4 * math.pi * ic)
    # Positive-inductance stable branch, with the second physical port off.
    for ls in (off, 160e-12, 200e-12, 300e-12, 500e-12, 1e-9):
        s = pole((ls, off), guess)
        guess = s
        det = (480e-12 + ls) ** 2 - (-138e-12 + ls) ** 2
        assert det > 0
        rows.append(dict(ls_pH=ls * 1e12, pole_real=s.real,
                         frequency_hz=s.imag / (2 * math.pi),
                         energy_decay_rate=-2 * s.real,
                         flux_phi0=math.acos(lmin / ls) / math.pi))
    return dict(model="two 480pH/-138pH transformer primaries at one tap; "
                      "independent real50ohm secondaries; no junction C or loss",
                off_target_hz=f0, short_segment_delay_s=td,
                open_segment_delay_s=to, total_delay_s=td + to,
                inferred_length_at_source_velocity_m=(td + to) * (4 * 4.8e-3 * f0),
                ls_min_pH=lmin * 1e12, static_poles=rows)


def main():
    frequency = 6.57e9
    nh, nc = occupation(frequency, .100), occupation(frequency, .010)
    eta0 = .99
    kmax = 1 / 5e-9
    min_time = -2 * math.log1p(-math.sqrt(eta0)) / kmax
    ideal_thermal = periodic_two_bath(-math.log1p(-math.sqrt(eta0)),
                                     -math.log1p(-math.sqrt(eta0)), nh, nc)
    k, ki = 1 / 20e-9, 1 / 3e-6
    duration = 6 / (k + ki)
    channel = collision_dilation(k, ki, duration)
    release = release_weights(k, ki, duration)
    rate_samples = []
    for ki_case, kmax_case, source in ((1 / 4.5e-6, 1 / 5e-9, "Yin2012 rates"),
                                      (1 / 3e-6, 1 / 20e-9, "Wenner2013 max rate"),
                                      (1 / 3e-6, 1 / 50e-9, "Wenner2013 chosen rate")):
        rate_samples.append(dict(source=source, eta_asymptotic_ceiling=(
            kmax_case / (kmax_case + ki_case)) ** 2))
    report = dict(
        carrier_hz=frequency, hot_temperature_k=.100, cold_temperature_k=.010,
        n_hot=nh, n_cold=nc, target_eta=eta0,
        ideal_minimum_capture_plus_release_time_s=min_time,
        ideal_periodic_thermal=ideal_thermal,
        ideal_heat_per_cycle_J=PLANCK * frequency * ideal_thermal["heat_quanta"],
        finite_loss_case=dict(kappa_on=k, kappa_intrinsic=ki,
                              duration_per_stage_s=duration,
                              branching_ceiling=(k / (k + ki)) ** 2,
                              release_weights=release, channel=channel),
        same_source_rate_checks=rate_samples,
        explicit_two_port_static_boundary=two_port_poles(),
        physical_limits=["two independently tunable ports not experimentally supplied here",
                         "no joint whole-circuit time-dependent Maxwell error certificate",
                         "no off-leakage or controller cold-dissipation certificate",
                         "carrier-energy heat ledger, not exact drive/source energy ledger",
                         "signal transmissivity is not arbitrary-state fidelity"])
    path = Path(__file__).with_name("buffer_model_results.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
