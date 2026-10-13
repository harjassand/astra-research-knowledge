"""Conditional qualification arithmetic, not an atomistic simulation.

All hBN numerical inputs come from ONE theoretical study:
Hamdi et al., npj Computational Materials 6, 178 (2020),
DOI: 10.1038/s41524-020-00451-y.
The inputs are predictions, not measured Stone-Wales defect parameters.

The optical branching calculation applies to the reported relaxed singlet
cycle. It does not bound alternative excitation or charge-injection pathways.
No repair barrier, repair probability, transfer rate, or gain is assumed.

Run: python qualification_calculations.py
"""
from __future__ import annotations
import json
import math
from pathlib import Path

EV_J = 1.602176634e-19  # Exact SI conversion.

def branching_probability(isc_s: float, radiative_lifetime_s: float,
                          additional_loss_s: float = 0.0) -> float:
    if not all(math.isfinite(x) for x in
               (isc_s, radiative_lifetime_s, additional_loss_s)):
        raise ValueError("Inputs must be finite")
    if isc_s < 0 or radiative_lifetime_s <= 0 or additional_loss_s < 0:
        raise ValueError("Rates must be nonnegative and lifetime positive")
    return isc_s / (isc_s + 1.0 / radiative_lifetime_s + additional_loss_s)

def zero_success_upper_bound(trials: int, confidence: float = 0.95) -> float:
    """Exact one-sided binomial bound: independent, verified trials only."""
    if trials <= 0 or not 0 < confidence < 1:
        raise ValueError("Positive trials and confidence in (0,1) required")
    return -math.expm1(math.log1p(-confidence) / trials)

def outcome_probabilities(exposure: float, useful: float, damage: float):
    """Poisson exposure; terminal useful/damage hazards; no reverse reaction.

    'useful' and 'damage' are mutually exclusive per-event probabilities.
    This is an analytical diagnostic, not a fit to experimental observations.
    """
    if exposure < 0 or useful < 0 or damage < 0 or useful + damage > 1:
        raise ValueError("Invalid exposure or event probabilities")
    total = useful + damage
    if total == 0:
        return (1.0, 0.0, 0.0)
    changed = -math.expm1(-exposure * total)
    return (1.0 - changed, useful / total * changed,
            damage / total * changed)

def main() -> None:
    isc = 100.0
    tau = 2.4e-9
    photon_ev = 4.53
    eta = branching_probability(isc, tau)
    photon_j = photon_ev * EV_J
    target_yield = 0.99
    # Unknown triplet-to-repair probability y remains symbolic. y=1 below
    # defines an optimistic ceiling, not an inferred physical parameter.
    result = {
        "status": "Conditional arithmetic only; no qualified physical operation",
        "source_doi": "10.1038/s41524-020-00451-y",
        "inputs_are_theoretical_predictions": True,
        "inputs": {"isc_rate_s^-1": isc, "radiative_lifetime_s": tau,
                   "vertical_excitation_eV": photon_ev},
        "relaxed_cycle_triplet_branching_probability": eta,
        "mean_absorbed_photons_per_triplet": 1 / eta,
        "absorbed_optical_energy_per_triplet_J": photon_j / eta,
        "G_threshold_for_more_than_one_retained_repair_per_absorbed_photon": 1 / eta,
        "optimistic_damage_probability_ceiling_for_99_percent_terminal_yield":
            eta * (1 - target_yield) / target_yield,
        "damage_ceiling_qualification":
            "No chain, y=1, no extra optical loss, no later damage or reversal. "
            "For general triplet repair probability y, multiply by y.",
        "no_damage_unsaturated_99_percent_fluence_coefficient_J":
            photon_j * (-math.log1p(-target_yield)) / eta,
        "fluence_formula":
            "incident_fluence[J/cm^2] = coefficient_J / "
            "(defect_absorption_cross_section[cm^2] * triplet_repair_probability). "
            "Requires constant cross section, independent sites, no recycling, "
            "no saturation, no damage, no reverse reaction.",
        "zero_success_95_percent_upper_bounds": {
            str(n): zero_success_upper_bound(n) for n in (30, 300, 3000)
        },
        "unacquired": ["Structural identity of addressed optical centre",
                       "Excited-state repair path and nonadiabatic branching",
                       "Mobile outgoing excitation after repair",
                       "Same-specimen capture and transfer kinetics",
                       "Defect absorption cross section and parasitic absorption",
                       "Damage probability and retained lifetime",
                       "Matched competing repair process and wall energy"],
    }
    # Numerical integrity checks, NOT scientific/physical validation.
    assert abs(eta - 2.4e-7) / 2.4e-7 < 3e-7
    assert 3e-12 < photon_j / eta < 3.1e-12
    for a in (0.0, 1.0, 1e5, 1e8):
        probs = outcome_probabilities(a, eta, eta / 99)
        assert abs(sum(probs) - 1.0) < 1e-12
        assert all(0 <= p <= 1 for p in probs)
    for n in (30, 300, 3000):
        p = zero_success_upper_bound(n)
        assert math.isclose((1 - p) ** n, 0.05, rel_tol=1e-10)
    output = Path(__file__).with_name("qualification_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
