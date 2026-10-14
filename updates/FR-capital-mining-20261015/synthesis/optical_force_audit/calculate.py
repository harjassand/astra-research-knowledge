#!/usr/bin/env python3
"""Conditional optical/APB audit. Stdlib only; no material fit is fabricated.

Published input provenance is in REFERENCES.md. Numbers labeled normalization
or cold_DFT must not be combined into acquired hot-GaAs performance.
"""
from __future__ import annotations

import cmath
import hashlib
import json
import math
from pathlib import Path
import random

OUT = Path(__file__).resolve().parent
EPS0 = 8.8541878128e-12
C = 299792458.0
EV = 1.602176634e-19
HC_EV_UM = 1.2398419843320026
PIN = "00631610750c708263d5cf6d812ebbb8edc77335"
REPO = Path("/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-compensation-exchange")
SOURCE = Path("/Users/harjas/.codex/attachments/70979206-4b3f-415e-9ff1-e22869ba8372/Pasted text.txt")


def gap_panish_casey(T: float) -> float:
    """GaAs direct gap; published absorption data cover 300 <= T <= 973 K."""
    if not 300.0 <= T <= 973.0:
        raise ValueError("Panish-Casey measured temperature range exceeded")
    return 1.522 - 5.8e-4 * T * T / (T + 300.0)


def index_skauli_22C(wavelength_um: float) -> float:
    """Original paper Eq.13/Table II, at 22 C ONLY; 0.97--17 um."""
    if not 0.97 <= wavelength_um <= 17.0:
        raise ValueError("Skauli wavelength range exceeded")
    poles = (0.4431307, 0.8746453, 36.9166)
    strengths = (27.83972, 0.031764, 0.00143636)
    inv_l2 = 1.0 / wavelength_um**2
    n2 = 5.372514 + sum(g / (1.0 / pole**2 - inv_l2)
                              for pole, g in zip(poles, strengths))
    return math.sqrt(n2)


def sinc(x: float) -> float:
    return 1.0 if x == 0.0 else math.sin(x) / x


def overlap(q: float, d: float, attenuation: float = 0.0) -> complex:
    r = complex(-attenuation, q) * d
    return 1.0 + 0j if abs(r) < 1e-12 else (cmath.exp(r) - 1.0) / r


def simpson(f, lo: float, hi: float, n: int = 4000):
    assert n % 2 == 0
    h = (hi - lo) / n
    result = f(lo) + f(hi)
    result += 4 * sum(f(lo + i * h) for i in range(1, n, 2))
    result += 2 * sum(f(lo + i * h) for i in range(2, n, 2))
    return result * h / 3


def check_analytic_identities() -> dict:
    checks = {}
    # Independent cycle integration checks the cubic prefactor.
    e1, e2, phase = 1.7, 0.8, 0.46
    avg_cubic = simpson(lambda t: (e1 * math.cos(t) +
                         e2 * math.cos(2 * t + phase))**3,
                         0, 2 * math.pi) / (2 * math.pi)
    cubic_exact = 0.75 * e1**2 * e2 * math.cos(phase)
    assert abs(avg_cubic - cubic_exact) < 1e-12
    checks["cycle_average_E_cubed_abs_error"] = abs(avg_cubic-cubic_exact)

    rng = random.Random(821)
    overlap_err = 0.0
    invariant_err = 0.0
    parity_err = 0.0
    for _ in range(30):
        qd = rng.uniform(-12, 12)
        ad = rng.uniform(0, 4)
        direct = simpson(lambda z: cmath.exp(complex(-ad, qd) * z), 0, 1)
        overlap_err = max(overlap_err, abs(direct - overlap(qd, 1, ad)))
        a = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        b = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        g = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
        gp = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
        adot = -2j * g.conjugate() * a.conjugate() * b
        bdot = -1j * g * a**2
        dna = 2 * (a.conjugate() * adot).real
        dnb = 2 * (b.conjugate() * bdot).real
        invariant_err = max(invariant_err, abs(dna + 2 * dnb))
        K, delta = 0.4, 0.6
        bself = -1j * g * a**2 / complex(K, -delta)
        bself_inv = -1j * (-g) * a**2 / complex(K, -delta)
        force = -2 * (gp * bself.conjugate() * a**2).real
        force_inv = -2 * ((-gp) * bself_inv.conjugate() * a**2).real
        parity_err = max(parity_err, abs(force-force_inv))
    assert overlap_err < 1e-10
    assert invariant_err < 1e-12
    assert parity_err < 1e-12
    checks["complex_overlap_quadrature_max_abs_error"] = overlap_err
    checks["Manley_Rowe_max_abs_residual"] = invariant_err
    checks["unseeded_global_inversion_force_max_abs_residual"] = parity_err

    q, p0, phi, x = 2.3, 1.7, 0.9, 0.43
    dx = 1e-5
    potential = lambda z: -p0 * math.sin(q*z + phi) / q
    fd_force = -(potential(x+dx)-potential(x-dx))/(2*dx)
    assert abs(fd_force-p0*math.cos(q*x+phi)) < 1e-9
    cycle_work = simpson(lambda z: p0*math.cos(q*z+phi), 0, 2*math.pi/q)
    assert abs(cycle_work) < 1e-12
    checks["force_potential_finite_difference_abs_error"] = abs(fd_force-p0*math.cos(q*x+phi))
    checks["static_pressure_work_per_beat_abs_residual"] = abs(cycle_work)

    # Elastica equation and free-tip condition tested without a small-slope approximation.
    gamma, thickness, pressure = 1.3, 0.7, 0.8
    a = pressure / gamma
    slope = lambda z: a*(thickness-z) / math.sqrt(1-(a*(thickness-z))**2)
    top_numeric = simpson(slope, 0, thickness)
    r = pressure*thickness/gamma
    top_exact = (pressure*thickness**2/gamma)/(1+math.sqrt(1-r*r))
    assert abs(top_numeric-top_exact) < 1e-12
    assert slope(thickness) == 0
    checks["pinned_elastica_top_quadrature_abs_error"] = abs(top_numeric-top_exact)
    checks["status"] = "passed_internal_conditional_identity_checks_only"
    return checks


def main() -> None:
    chi = 100e-12
    n = 3.3
    normalization = []
    gamma_DFT = 28e-3 * EV / 1e-20
    d = 400e-9
    for E in (1e7, 1e8, 3e8):
        p = EPS0 * chi * E**3 / 2
        intensity = n * EPS0 * C * E**2 / 2
        r = p * d / gamma_DFT
        bow = (p*d*d/gamma_DFT)/(1+math.sqrt(1-r*r)) if r < 1 else None
        normalization.append({
            "peak_internal_E_each_color_V_m": E,
            "scalar_on_pressure_Pa": p,
            "traveling_intensity_each_color_GW_cm2": intensity / 1e13,
            "D_1e_minus_7_average_pressure_Pa": 1e-7 * p,
            "cold_DFT_elastica_pd_over_gamma": r,
            "cold_DFT_pinned_top_bow_nm": None if bow is None else bow*1e9,
            "cold_DFT_cylindrical_growth_critical_radius_um": gamma_DFT/p*1e6,
            "fixed_temperature_M_for_1um_in_600s_m4_J_s": 1e-6/(600*p),
            "same_linear_M_with_D_1e_minus_7_m4_J_s": 1e-6/(600*p*1e-7),
        })

    temperatures = []
    for T in (300.0, 823.15, 923.15, 973.0):
        Eg = gap_panish_casey(T)
        temperatures.append({"T_K": T, "T_C": T-273.15, "gap_eV": Eg,
            "lambda_fundamental_above_which_2omega_1PA_below_gap_um": 2*HC_EV_UM/Eg,
            "lambda_fundamental_above_which_mixed_2PA_below_gap_um": 3*HC_EV_UM/Eg,
            "lambda_fundamental_above_which_all_1PA_2PA_below_gap_um": 4*HC_EV_UM/Eg,
            "lambda_fundamental_above_which_2omega_3PA_below_gap_um": 6*HC_EV_UM/Eg})
    Eg_hot = gap_panish_casey(923.15)
    spectral_cases = []
    channel_multiples = {"omega_1PA": 1, "2omega_1PA_and_omega_2PA": 2,
                         "mixed_2PA_and_omega_3PA": 3, "2omega_2PA": 4,
                         "2omega_3PA": 6}
    for lam in (1.55, 1.8, 2.3, 3.4, 4.6, 6.8):
        photon = HC_EV_UM/lam
        spectral_cases.append({"fundamental_um": lam, "harmonic_um": lam/2,
            "fundamental_photon_eV": photon,
            "harmonic_photon_eV": 2*photon,
            "hot_channels_above_direct_gap_energetically_open_only":
                [name for name, multiple in channel_multiples.items() if multiple*photon > Eg_hot]})
    cold_cavity_harmonic = 2*HC_EV_UM/1.8
    delta = 1.522-cold_cavity_harmonic
    crossover = (delta+math.sqrt(delta*delta+4*5.8e-4*delta*300))/(2*5.8e-4)
    assert 300 <= crossover <= 973
    assert abs(gap_panish_casey(crossover)-cold_cavity_harmonic) < 1e-12

    dispersion = []
    for lam in (2.3, 3.4, 4.6, 6.8):
        n1, n2 = index_skauli_22C(lam), index_skauli_22C(lam/2)
        # Same convention as DERIVATIONS: q = 2 k_omega - k_2omega.
        q = 4*math.pi*(n1-n2)/(lam*1e-6)
        dispersion.append({"temperature_C": 22, "fundamental_um": lam,
            "n_omega": n1, "n_2omega": n2, "q_m_inverse": q,
            "coherence_length_pi_over_q_um": math.pi/abs(q)*1e6,
            "beat_length_2pi_over_q_um": 2*math.pi/abs(q)*1e6,
            "400nm_uniform_forward_overlap_magnitude": abs(overlap(q, d)),
            "hot_650C_extrapolation": "NOT_PERFORMED"})

    cancellation = []
    for beat_fraction in (0.1, 0.25, 0.5, 1, 2, 5):
        qd = 2*math.pi*beat_fraction
        cancellation.append({"thickness_over_beat_length": beat_fraction,
                             "uniform_lossless_overlap_abs": abs(overlap(qd, 1))})
    attenuation_cases = [{"amplitude_product_attenuation_ad": ad,
                          "overlap_abs_at_qd_2pi": abs(overlap(2*math.pi, 1, ad))}
                         for ad in (0, 0.1, 1, 3)]

    results = {
        "status": "conditional_internal_audit_no_hardware_validation",
        "historical_originality": "UNKNOWN",
        "source_repository_pin": PIN,
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "parameter_warning": "100 pm/V, n=3.3 and equal fields are source normalizations; 28 meV/A^2 is static DFT, not hot measured wall stiffness; no favorable hot mobility, absorption, coupling, or yield was assigned.",
        "published_cold_DFT_gamma110_J_m2": gamma_DFT,
        "source_normalization": normalization,
        "Panish_Casey_gap_and_kinematic_thresholds": temperatures,
        "hot_650C_spectral_cases": spectral_cases,
        "cold_1800nm_cavity_harmonic_crosses_gap_at_C": crossover-273.15,
        "Skauli_22C_propagation_examples": dispersion,
        "controlled_phase_cancellation_cases": cancellation,
        "attenuation_breaks_exact_sinc_zero_but_not_overlap_bound": attenuation_cases,
        "checks": check_analytic_identities(),
    }
    (OUT / "results.json").write_text(json.dumps(results, indent=2)+"\n")
    selected = {"hot_gap_eV": Eg_hot,
        "all_one_two_photon_closed_necessary_lambda_um": 4*HC_EV_UM/Eg_hot,
        "cold_1800nm_cavity_crossover_C": crossover-273.15,
        "middle_field_conditional_bow_nm": normalization[1]["cold_DFT_pinned_top_bow_nm"],
        "identity_checks": results["checks"]}
    print(json.dumps(selected, indent=2))


if __name__ == "__main__":
    main()
