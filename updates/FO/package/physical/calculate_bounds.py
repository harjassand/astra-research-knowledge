#!/usr/bin/env python3
"""Reproduce a SCOPED impulsive selective-melting audit; not a device simulation.

Thermophysical source: Yamaguchi, Itagaki & Yazawa (1989),
DOI 10.2320/jinstmet1952.53.8_764, Table 1 and reported GaAs fusion heat.
The heat-content polynomial gives H(T)-H(298.15 K); it is not extrapolated
outside its published 800--1514 K interval. Room temperature is its reference.

Assumptions: equal molar amounts and initial temperature, equilibrium melting,
fixed composition, negligible cooling/heat exchange during energy partition,
net deposited energies Q*(1+C) and Q*(1-C), desired region stays below melt
onset while the other region melts completely. C is actual deposited-energy
contrast, NOT automatically the measured carrier-population contrast.

Not applicable as a universal limit to nonthermal transitions, interfacial
rearrangements, sustained heating with cooling, or partial melting/regrowth.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

T_REF_K = 298.15
T_M_K = 1514.0
L_FUSION_J_MOL = 106720.0


def heat_content_relative_to_298(t_k: float) -> float:
    """Published solid-state heat-content fit, J/mol relative to 298.15 K."""
    if not math.isfinite(t_k) or not 800.0 <= t_k <= T_M_K:
        raise ValueError("The published fit is valid only on 800--1514 K.")
    return 47.3*t_k + 3.99e-3*t_k*t_k + 2.40e5/t_k - 1.53e4


def sensible_heat_to_melting(t0_k: float) -> float:
    """Use the reference directly; otherwise stay within the published fit."""
    if t0_k == T_REF_K:
        initial = 0.0
    else:
        initial = heat_content_relative_to_298(t0_k)
    return heat_content_relative_to_298(T_M_K) - initial


def threshold_contrast(h_sensible: float, latent: float) -> float:
    """A nonempty full-melt/protected-solid dose window requires C > this."""
    if not (math.isfinite(h_sensible) and h_sensible >= 0):
        raise ValueError("Sensible heat must be finite and nonnegative.")
    if not (math.isfinite(latent) and latent > 0):
        raise ValueError("Latent heat must be finite and positive.")
    return latent/(2.0*h_sensible + latent)


def molten_fraction_supremum(contrast: float, h_sensible: float,
                            latent: float) -> float:
    """Supremum under strict protection, capped at 1; not a regrowth yield."""
    if not math.isfinite(contrast) or not 0 <= contrast < 1:
        raise ValueError("Contrast must be in [0, 1).")
    threshold_contrast(h_sensible, latent)  # validate the thermodynamic inputs
    return min(1.0, 2.0*contrast*h_sensible/((1.0-contrast)*latent))


def verify_window(h_sensible: float, latent: float) -> None:
    """Check the equivalent dose-window inequalities on each threshold side."""
    cstar = threshold_contrast(h_sensible, latent)
    for c in (0.5*cstar, 0.5*(1+cstar)):
        lower = (h_sensible+latent)/(1+c)
        upper = h_sensible/(1-c)
        assert (lower < upper) == (c > cstar)


def main() -> None:
    h_room = sensible_heat_to_melting(T_REF_K)
    temperatures = [T_REF_K, 800.0, 1000.0, 1200.0, 1400.0, 1500.0]
    rows = []
    for temperature in temperatures:
        h = sensible_heat_to_melting(temperature)
        verify_window(h, L_FUSION_J_MOL)
        rows.append({
            "initial_temperature_K": temperature,
            "sensible_heat_J_per_mol": h,
            "required_contrast_strictly_greater_than":
                threshold_contrast(h, L_FUSION_J_MOL),
        })
    result = {
        "status": "Conditional analytic-model arithmetic; no physical validation",
        "thermophysical_source_doi": "10.2320/jinstmet1952.53.8_764",
        "melting_temperature_K": T_M_K,
        "latent_heat_J_per_mol": L_FUSION_J_MOL,
        "room_temperature_complete_melting_J_per_mol": h_room+L_FUSION_J_MOL,
        "contrast_thresholds": rows,
        "hypothetical_heat_contrasts_not_measured_high_fluence_values": [
            {"contrast": c,
             "molten_fraction_supremum_room_temperature":
                 molten_fraction_supremum(c, h_room, L_FUSION_J_MOL)}
            for c in [0.02, 0.064, 0.14]
        ],
        "excluded_conclusions": [
            "No universal no-go for phase-selected retained rewriting",
            "No identification of carrier contrast with heat contrast",
            "No high-fluence optical constants or reaction kernel acquired",
            "No retained polarity rewriting demonstrated",
            "No industrial cost, throughput, or novelty established",
        ],
    }
    out = Path(__file__).resolve().with_name("results.json")
    out.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
