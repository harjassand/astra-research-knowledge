#!/usr/bin/env python3
"""Reproduce an ASTRA candidate's kinematic audit; NOT a defect-yield simulator.

Run: python recoil_audit.py
Uses only Python's standard library. Output is JSON on stdout.
The assertions check algebra and numerical consistency, not material feasibility,
retention, novelty, or scientific correctness of imported experimental estimates.

Source inputs:
- Kamaraju et al., arXiv:1011.0090v1 (2010), especially pp. 4-7:
  https://arxiv.org/abs/1011.0090
- Te mass and density: Royal Society of Chemistry periodic table:
  https://periodic-table.rsc.org/element/52/tellurium

Important: 0.24 angstrom is an optical-model displacement estimate. Its literal
per-atom harmonic interpretation is deliberately audited, NOT endorsed.
The coherent-energy ceiling assumes the same sampled volume, uniform equal-
amplitude A1 motion, no imported energy and no other released energy reservoir.
A 100% coherent conversion ceiling is NOT a realizable pump-efficiency estimate.
No CdTe displacement threshold is used for elemental Te.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math

EV_J = 1.602176634e-19
C_M_S = 299792458.0
U_KG = 1.66053906892e-27
MEC2_EV = 510998.95069


def positive(value: float, name: str) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return value


@dataclass(frozen=True)
class Inputs:
    te_mass_u: float = 127.60
    density_kg_m3: float = 6232.0
    mode_frequency_hz: float = 3.24e12
    inferred_amplitude_m: float = 0.24e-10
    photoexcited_density_m3: float = 1.4e27
    pump_photon_ev: float = 1.57

    def validate(self) -> None:
        for key, value in asdict(self).items():
            positive(value, key)


def momentum_transfer_max(beam_ev: float) -> float:
    """2p for near-backscattering, neglecting small electron recoil corrections."""
    positive(beam_ev, "beam_ev")
    pc_ev = math.sqrt(beam_ev * (beam_ev + 2.0 * MEC2_EV))
    return 2.0 * pc_ev * EV_J / C_M_S


def stationary_transfer_ev(beam_ev: float, mass_kg: float) -> float:
    positive(mass_kg, "mass_kg")
    q = momentum_transfer_max(beam_ev)
    return q * q / (2.0 * mass_kg * EV_J)


def transfer_derivative(beam_ev: float, mass_kg: float) -> float:
    """dT0/dE, with both energies in eV."""
    positive(beam_ev, "beam_ev")
    positive(mass_kg, "mass_kg")
    mass_rest_ev = mass_kg * C_M_S**2 / EV_J
    return 4.0 * (beam_ev + MEC2_EV) / mass_rest_ev


def timing_attenuation(frequency_hz: float, fwhm_fs: float, jitter_rms_fs: float = 0.0) -> float:
    """Gaussian convolution of a LINEAR sinusoidal signal, not nonlinear yield."""
    positive(frequency_hz, "frequency_hz")
    if not all(math.isfinite(x) and x >= 0 for x in (fwhm_fs, jitter_rms_fs)):
        raise ValueError("Pulse width and jitter must be finite and nonnegative")
    sigma_pulse = fwhm_fs * 1e-15 / math.sqrt(8.0 * math.log(2.0))
    sigma_jitter = jitter_rms_fs * 1e-15
    sigma2 = sigma_pulse**2 + sigma_jitter**2
    return math.exp(-0.5 * (2.0 * math.pi * frequency_hz)**2 * sigma2)


def hazard_ratio_required(target_fraction: float, undesired_fraction: float) -> float:
    """Independent irreversible-hit model only; no healing or changing cross sections."""
    if not (0 < target_fraction < 1 and 0 < undesired_fraction < 1):
        raise ValueError("Fractions must lie strictly between zero and one")
    return math.log1p(-target_fraction) / math.log1p(-undesired_fraction)


def algebra_checks() -> dict[str, bool]:
    mass = 127.60 * U_KG
    q = momentum_transfer_max(300e3)
    for velocity in (-500.0, -20.0, 0.0, 20.0, 500.0):
        p = mass * velocity
        direct = ((p + q)**2 - p**2) / (2.0 * mass)
        identity = q*q/(2.0*mass) + q*velocity
        assert math.isclose(direct, identity, rel_tol=1e-12, abs_tol=1e-30)
    for k in range(61):
        theta = 2.0 * math.pi * k / 61.0
        a = [math.cos(theta - 2.0*math.pi*j/3.0) for j in range(3)]
        assert abs(sum(a)) < 1e-13
        assert math.isclose(sum(x*x for x in a), 1.5, abs_tol=1e-13)
        assert math.isclose(sum(x**3 for x in a), 0.75*math.cos(3*theta), abs_tol=1e-13)
    for beam in (100e3, 200e3, 300e3, 500e3):
        d_numeric = (stationary_transfer_ev(beam+1, mass)-stationary_transfer_ev(beam-1, mass))/2
        assert math.isclose(d_numeric, transfer_derivative(beam, mass), rel_tol=1e-9)
    return {"impulse_identity": True, "three_site_moments": True, "energy_derivative": True}


def main() -> None:
    inp = Inputs()
    inp.validate()
    mass = inp.te_mass_u * U_KG
    nat = inp.density_kg_m3 / mass
    omega = 2.0 * math.pi * inp.mode_frequency_hz
    inferred_speed = omega * inp.inferred_amplitude_m
    literal_coherent_ev = 0.5 * mass * inferred_speed**2 / EV_J
    absorbed_ev = inp.photoexcited_density_m3 * inp.pump_photon_ev / nat
    speed_ceiling = math.sqrt(2.0 * absorbed_ev * EV_J / mass)
    speed_per_pm = omega * 1e-12

    recoil_table = []
    for beam_kev in (100, 200, 300, 500):
        beam_ev = beam_kev * 1000.0
        q = momentum_transfer_max(beam_ev)
        t0 = stationary_transfer_ev(beam_ev, mass)
        shift_ceiling = q * speed_ceiling / EV_J
        shift_per_pm = q * speed_per_pm / EV_J
        assert math.isclose(shift_ceiling, 2.0*math.sqrt(t0*absorbed_ev), rel_tol=1e-12)
        recoil_table.append({
            "beam_kev": beam_kev,
            "stationary_max_transfer_ev": t0,
            "conditional_100pct_coherent_shift_ceiling_ev": shift_ceiling,
            "shift_ev_per_measured_pm": shift_per_pm,
            "one_vs_other_splitting_ev_per_measured_pm": 1.5*shift_per_pm,
            "equivalent_beam_shift_kev_per_measured_pm": shift_per_pm/transfer_derivative(beam_ev, mass)/1000.0,
        })

    output = {
        "status": "Kinematic candidate audit; no retained-yield, throughput, or novelty validation",
        "inputs": asdict(inp),
        "atom_density_cm3": nat / 1e6,
        "literal_undamped_per_atom_amplitude_interpretation": {
            "speed_m_s": inferred_speed,
            "coherent_energy_ev_atom": literal_coherent_ev,
            "absorbed_energy_estimate_ev_atom": absorbed_ev,
            "coherent_over_absorbed_ratio": literal_coherent_ev / absorbed_ev,
            "interpretation": "Requires reconciliation of mode normalization, sampling volume, damping and optical inference; not a refutation of the source paper",
        },
        "conditional_all_absorbed_energy_in_equal_amplitude_mode_ceiling": {
            "speed_m_s": speed_ceiling,
            "amplitude_angstrom": speed_ceiling / omega / 1e-10,
            "is_demonstrated_operating_point": False,
        },
        "recoil_table": recoil_table,
        "linear_sinusoid_timing_attenuation_no_jitter": {
            str(fwhm): timing_attenuation(inp.mode_frequency_hz, fwhm)
            for fwhm in (20, 28, 50, 100, 200)
        },
        "99pct_target_1pct_undesired_integrated_hazard_ratio": hazard_ratio_required(.99, .01),
        "checks": algebra_checks(),
        "unknowns": [
            "Calibrated Q(t), atomic momentum covariance and electronic state in actual Te lamella",
            "Directional, phase-conditioned retained-event cross sections for elemental Te",
            "Neighbour-motion effects and competing electronic damage",
            "Post-pulse retention, readout damage, sample stability and repeated-dose evolution",
            "Joint electron pulse duration, energy, current, timing and wall-plug cost",
            "Historical priority and advantage over actual alternatives",
        ],
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
