#!/usr/bin/env python3
"""Exact countermodel scores and nominal Li-interface scales; no lab data.

The arithmetic does not certify material parameters, detector latency, hazardous
conductance, or experimental feasibility. Sources and assumptions are in REPORT.
"""
from fractions import Fraction as Fq
import json
import math
from pathlib import Path


def score(triple, r):
    ym, y0, yp = map(Fq, triple)
    return y0 * (ym - r) * (yp - r)


ring_words = [(0, 1, 1), (1, 1, 0), (1, 0, 1)]
canonical_words = [(0, 0, 1), (0, 1, 0), (1, 0, 0),
                   (0, 1, 1), (1, 0, 1), (1, 1, 0)]
scores = {}
for r in (Fq(1, 3), Fq(1, 2), Fq(9, 10)):
    scores[str(r)] = {
        "fixed_amplitude_threshold_minus_half": str(sum(score(w, r) for w in ring_words) / 3),
        "canonical_zero_threshold": str(sum(score(w, r) for w in canonical_words) / 6),
    }

# A genuine finite-friction, single-bath equilibrium oscillator. The stationary
# coordinate process is Gaussian. The orthant formula follows by expanding
# Y=(1+sign X)/2, using central symmetry and E[sign X sign Z]=2 asin(corr)/pi.
gamma, omega0, r = 0.1, 1.0, 1 / 3
omega_d = math.sqrt(omega0**2 - gamma**2 / 4)
gap = 2 * math.pi / (3 * omega_d)


def normalized_correlation(t):
    return math.exp(-gamma * t / 2) * (
        math.cos(omega_d * t) + gamma / (2 * omega_d) * math.sin(omega_d * t))


c1, c2 = normalized_correlation(gap), normalized_correlation(2 * gap)
p_all = 1 / 8 + (2 * math.asin(c1) + math.asin(c2)) / (4 * math.pi)
p_pair = 1 / 4 + math.asin(c1) / (2 * math.pi)
damped_score = p_all - 2 * r * p_pair + r * r / 2

# Source nominal values at approximately room temperature, not certified maxima.
electrical_resistivity = 9.28e-8  # ohm m, Chi 1979, Table 3, 293 K
density = 534.0                  # kg / m^3, NIST elemental composition
molar_mass = 0.006941            # kg / mol, NIST Chemistry WebBook
faraday = 96485.33212            # C / mol, rounded SI e*N_A
conductivity = 1 / electrical_resistivity
volume_per_coulomb = molar_mass / (faraday * density)

rod_scales = []
for d_um in (10, 20, 50, 100):
    d = d_um * 1e-6
    conductance = 1.0  # S; illustrative, not a universal hazard threshold
    volume = conductance * d * d / conductivity
    charge = volume / volume_per_coulomb
    area = conductance * d / conductivity
    rod_scales.append({
        "d_um": d_um, "G_S": conductance,
        "volume_m3": volume, "radius_um": math.sqrt(area / math.pi) * 1e6,
        "plating_charge_C": charge,
        "full_current_latency_ns_at_1A": charge * 1e9,
    })

latency_caps = []
for current, delay in ((1., 1e-6), (1., 10e-6), (0.1, 10e-6), (0.001, 100e-6)):
    d = 20e-6
    q = current * delay
    latency_caps.append({
        "I_A": current, "delay_s": delay, "Q_C": q,
        "nominal_G_volume_bound_S_at_d20um": conductivity * volume_per_coulomb * q / d**2,
    })

result = {
    "evidence_type": "calculation_on_declared_models_not_laboratory_evidence",
    "exact_oscillator_scores": scores,
    "finite_friction_equilibrium_oscillator_calculation": {
        "gamma": gamma, "omega0": omega0, "gap": gap, "r": r,
        "normalized_correlation_gap": c1, "normalized_correlation_twice_gap": c2,
        "EW": damped_score,
        "status": "analytic Gaussian formula evaluated in floating point; no simulated or laboratory trajectories",
    },
    "nominal_material_inputs": {
        "electrical_resistivity_ohm_m": electrical_resistivity,
        "density_kg_m3": density, "molar_mass_kg_mol": molar_mass,
        "faraday_C_mol": faraday,
        "volume_per_coulomb_m3_C": volume_per_coulomb,
    },
    "straight_Li_rod_scales": rod_scales,
    "full_current_latency_caps_no_initial_or_advected_metal": latency_caps,
    "guard_bias_example": {
        "contact_G_S": 1., "current_limit_A": 0.001,
        "max_guard_voltage_V": 0.001,
        "current_required_to_hold_50mV_A": 0.05,
        "interpretation": "Ohmic circuit calculation only; guard current is not necessarily Li stripping current",
    },
}
out = Path(__file__).with_name("CALCULATION_RESULTS.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
