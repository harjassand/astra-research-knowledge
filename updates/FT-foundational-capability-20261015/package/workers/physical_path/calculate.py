#!/usr/bin/env python3
"""Conditional isotope-exchange arithmetic; no laboratory simulation or validation.

Source inputs are central experimental values transcribed and visually checked from
Susi et al., Nat Commun 7,13040 (2016), Supplementary Table 1, p.4.
The source's uncertainties are preserved in SOURCES.md, not propagated here.
All operations assume independent natural-feed replacements and fixed pristine
lattice cross sections; these are unacquired physical premises.
"""

from math import exp, expm1, log, sqrt
import json
from pathlib import Path

P = 0.01109
BARN_NM2 = 1e-10
SIGMA_L = 0.0566 * BARN_NM2
SIGMA_H = 0.0021 * BARN_NM2
ELECTRON_ENERGY_EV = 95_000.0
JOULE_PER_EV = 1.602176634e-19


def collateral_equilibrium(p, ratio, m):
    """Stable fixed point of the stated well-mixed collateral-loss model."""
    b = p * ratio + 1 - p
    if m == 0:
        return p * ratio / b
    a = m * (ratio - 1)
    big_b = b + m * (ratio + p * (ratio - 1))
    c = (1 + m) * p * ratio
    return 2 * c / (big_b + sqrt(big_b**2 - 4 * a * c))


def blind_target(q):
    b = P * SIGMA_L + (1 - P) * SIGMA_H
    q_star = P * SIGMA_L / b
    if not P <= q < q_star:
        raise ValueError("Target outside the ideal blind reachable interval")
    dose = -log((q_star - q) / (q_star - P)) / b
    exchanges = ((SIGMA_L - (SIGMA_L - SIGMA_H) * q_star) * dose
                 + (SIGMA_L - SIGMA_H) * (q - P) / b)
    r = SIGMA_L / SIGMA_H
    m_max = ((P * r * (1 - q) - (1 - P) * q)
             / ((r * (1 - q) + q) * (q - P)))
    return {
        "heavy_target": q,
        "dose_electrons_per_nm2": dose,
        "incident_kinetic_J_for_uniform_1nm2": dose * ELECTRON_ENERGY_EV * JOULE_PER_EV,
        "ideal_replacements_per_site": exchanges,
        "max_mean_unselected_collateral_per_primary_at_target": m_max,
    }


def renewal_target(q):
    """Root-proposed per-site exact-event renewal protocol, checked algebraically.

    An attempt starts with independent H probability P. Stop on an observed
    ejection and replace; accept/protect only after this attempt survives fluence d.
    Requires every ejection to be observed and accepted sites never exposed again.
    """
    if not P < q < 1:
        raise ValueError("Require P < q < 1")
    dose_cap = log(q * (1 - P) / (P * (1 - q))) / (SIGMA_L - SIGMA_H)
    survival_h = exp(-SIGMA_H * dose_cap)
    survival_l = exp(-SIGMA_L * dose_cap)
    accept = P * survival_h + (1 - P) * survival_l
    dose_per_attempt = (P * -expm1(-SIGMA_H * dose_cap) / SIGMA_H
                        + (1 - P) * -expm1(-SIGMA_L * dose_cap) / SIGMA_L)
    dose_total = dose_per_attempt / accept
    return {
        "accepted_heavy_posterior": q,
        "attempt_fluence_cap_electrons_per_nm2": dose_cap,
        "acceptance_probability_per_attempt": accept,
        "expected_attempts": 1 / accept,
        "expected_replacements_after_failed_attempts": 1 / accept - 1,
        "expected_total_fluence_electrons_per_nm2": dose_total,
        "incident_kinetic_J_for_uniform_1nm2": dose_total * ELECTRON_ENERGY_EV * JOULE_PER_EV,
        "initial_heavy_atom_survival_per_attempt": survival_h,
    }


def main():
    result = {
        "status": "CONDITIONAL_MODEL_ARITHMETIC_ONLY",
        "physical_validation": "NOT_PERFORMED",
        "novelty": "UNKNOWN",
        "inputs": {
            "heavy_feed_fraction": P,
            "sigma_L_barn": SIGMA_L / BARN_NM2,
            "sigma_H_barn": SIGMA_H / BARN_NM2,
            "sigma_ratio": SIGMA_L / SIGMA_H,
            "beam_energy_eV": ELECTRON_ENERGY_EV,
            "source": "Susi2016 Supplementary Table1 p4 experimental central values",
        },
        "blind_equilibrium_heavy_fraction": collateral_equilibrium(P, SIGMA_L / SIGMA_H, 0),
        "collateral_equilibria": [
            {"collateral_per_primary": m,
             "heavy_equilibrium": collateral_equilibrium(P, SIGMA_L / SIGMA_H, m)}
            for m in [0, .001, .01, .1, 1]
        ],
        "blind_targets": [blind_target(q) for q in [.02, .05, .1, .2]],
        "root_renewal_targets": [renewal_target(q) for q in [.5, .9, .99, .999]],
        "energy_boundary": (
            "Incident electron kinetic energy for uniformly exposed 1nm2. "
            "Not specimen heat, not wall-plug energy, not a per-site energy "
            "without an acquired atom-centred beam profile and effective area."
        ),
    }
    out = Path(__file__).with_name("calculations.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
