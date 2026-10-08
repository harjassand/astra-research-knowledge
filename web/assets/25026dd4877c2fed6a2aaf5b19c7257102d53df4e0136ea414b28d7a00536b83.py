"""Synthetic end-to-end assay-to-certificate arithmetic fixture (not material data)."""

from __future__ import annotations

import json
import math

from certificate_checker import (
    effective_face_margin,
    poisson_rate_confidence_interval,
    reaction_face_margin,
)


def main() -> None:
    # Synthetic pilot summaries: four adsorption/removal channels and one
    # reciprocal-hop channel. The values are chosen for arithmetic checking;
    # no trajectory or physical assay generated them.
    delta, channel_delta = 0.05, 0.01  # P=5, Bonferroni allocation
    reaction_ci = poisson_rate_confidence_interval(10_000, 10_000, channel_delta, 2.0)
    hop_ci = poisson_rate_confidence_interval(10_000, 200_000, channel_delta, 0.2)
    assert reaction_ci is not None and hop_ci is not None
    rlo, rhi = reaction_ci
    _, chi = hop_ci

    lower, upper, collar = (0.5,), (1.5,), 0.25
    reactions = [
        {"y": (0,), "nu": (1,), "k_lo": rlo, "k_hi": rhi},
        {"y": (1,), "nu": (-1,), "k_lo": rlo, "k_hi": rhi},
    ]
    alpha, face_data = (1.0, 3.0), []
    for site_alpha in alpha:
        low_rxn = reaction_face_margin(reactions, lower, upper, 0, collar, "lower")
        high_rxn = reaction_face_margin(reactions, lower, upper, 0, collar, "upper")
        low_eff = effective_face_margin(low_rxn, site_alpha, (chi,), collar)
        high_eff = effective_face_margin(high_rxn, site_alpha, (chi,), collar)
        face_data.append({
            "reaction_lower_margin": low_rxn,
            "reaction_upper_margin": high_rxn,
            "effective_lower_margin": low_eff,
            "effective_upper_margin": high_eff,
        })

    # PROOF.md constants for two sites, one species, birth/death reactions,
    # one reciprocal edge, b=1.5, and gaps g=0.5 from x0=1.
    effective = [z[k] for z in face_data for k in
                 ("effective_lower_margin", "effective_upper_margin")]
    face_gamma = [
        min(face_data[i]["effective_lower_margin"], face_data[i]["effective_upper_margin"])
        for i in range(2)
    ]
    bmax = 1.5
    B_by_site = [
        (rhi + rhi * bmax) / alpha[i] + 2 * bmax * chi / alpha[i] ** 2
        for i in range(2)
    ]
    theta_by_site = [min(alpha[i], face_gamma[i] / (6 * B_by_site[i])) for i in range(2)]
    c_star = min(theta_by_site[i] * collar for i in range(2))
    c_zero = min(theta * 0.5 for theta in theta_by_site)
    Lambda = sum(a * (rhi + rhi * bmax) for a in alpha) + 2 * chi * bmax
    M, V = 4, 25_000
    T = math.exp(c_star * V / 2)
    initial_term = 2 * sum(math.exp(-theta * V * 0.5) for theta in theta_by_site)
    jump_term = 2 * M * V * Lambda * T * math.exp(-c_star * V)
    assert min(effective) > 0
    assert initial_term + jump_term < 1e-4

    out = {
        "synthetic_only": True,
        "calibration_delta": delta,
        "channel_delta": channel_delta,
        "reaction_ci": list(reaction_ci),
        "hop_ci": list(hop_ci),
        "pilot_counts": {"four_reaction_channels": 40_000, "hop_channel": 10_000},
        "integrated_exposures": {"four_reaction_channels": 40_000, "hop_channel": 200_000},
        "effective_face_data": face_data,
        "all_effective_margins_positive": min(effective) > 0,
        "site_face_margin_minima": face_gamma,
        "theta_by_site": theta_by_site,
        "c_star": c_star,
        "c_zero": c_zero,
        "Lambda": Lambda,
        "V": V,
        "horizon": T,
        "operational_exit_bound": initial_term + jump_term,
        "operational_bound_terms": {"initial": initial_term, "jump": jump_term},
        "event_activity_envelope": V * Lambda * T,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
