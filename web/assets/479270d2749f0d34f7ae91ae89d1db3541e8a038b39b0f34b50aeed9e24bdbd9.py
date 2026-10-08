#!/usr/bin/env python3
"""Exact toy checks for the Paneth-renewal / crypt-repair identifiability note.

All values in the counterexample section are deliberately synthetic. They are
not estimates from Andersson et al. (2025), and the functional Notum threshold
is a model parameter, not a measured biological threshold.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


def functional_crypt_fraction(renewal: list[float], new_notum: float,
                              old_notum: float, threshold: float) -> float:
    """Fraction passing an illustrative per-crypt mean-Notum threshold."""
    passed = 0
    for r in renewal:
        local_notum = (1.0 - r) * old_notum + r * new_notum
        passed += local_notum <= threshold + 1e-12
    return passed / len(renewal)


def support_bounds(qbar: float, tau: float) -> tuple[float, float]:
    """Sharp bounds on P(R >= tau) given R in [0,1], E[R] = qbar."""
    if not (0.0 <= qbar <= 1.0 and 0.0 < tau <= 1.0):
        raise ValueError("require qbar in [0,1] and tau in (0,1]")
    lower = max(0.0, (qbar - tau) / (1.0 - tau)) if tau < 1 else float(qbar == 1)
    upper = min(1.0, qbar / tau)
    return lower, upper


def renewal_rate_alias(window_days: float, mean_labeled_fraction: float,
                       renewed_crypt_share: float) -> dict[str, float]:
    """Two rate distributions with the same pooled EdU fraction.

    Under a homogeneous Poisson replacement model, f=1-exp(-lambda*T).
    The heterogeneous model has a fraction `renewed_crypt_share` of crypts
    with a common positive rate and the rest at zero. The high rate is chosen
    so the pooled EdU+ fraction is identical.
    """
    T, fbar, p = window_days, mean_labeled_fraction, renewed_crypt_share
    if T <= 0 or not (0.0 < fbar < 1.0) or not (fbar < p <= 1.0):
        raise ValueError("require T>0, fbar in (0,1), and p>fbar")
    homogeneous = -math.log1p(-fbar) / T
    high_f = fbar / p
    high_rate = -math.log1p(-high_f) / T
    heterogeneous_mean = p * high_rate
    return {
        "window_days": T,
        "pooled_EdU_fraction": fbar,
        "active_crypt_share": p,
        "homogeneous_mean_rate_per_day": homogeneous,
        "active_crypt_label_fraction": high_f,
        "heterogeneous_mean_rate_per_day": heterogeneous_mean,
        "rate_ratio_heterogeneous_to_homogeneous": heterogeneous_mean / homogeneous,
    }


def main() -> None:
    # Equal-sized crypts; 8 Paneth cells each; normalized Notum units.
    n_crypts = 100
    paneth_per_crypt = 8
    old_notum = 1.0
    new_notum = 0.1
    notum_threshold = 0.55

    homogeneous = [0.5] * n_crypts
    clustered = [1.0] * (n_crypts // 2) + [0.0] * (n_crypts // 2)

    def summaries(renewal: list[float]) -> dict[str, float | int]:
        per_crypt_notum = [
            (1.0 - r) * old_notum + r * new_notum for r in renewal
        ]
        return {
            "crypt_count": n_crypts,
            "Paneth_cells_per_crypt": paneth_per_crypt,
            "pooled_EdU_positive_fraction": sum(renewal) / len(renewal),
            "mean_normalized_Notum_per_cell": sum(per_crypt_notum) / len(per_crypt_notum),
            "mean_Notum_in_EdU_positive_cells": new_notum,
            "mean_Notum_in_EdU_negative_cells": old_notum,
            "fraction_crypts_passing_functional_threshold": functional_crypt_fraction(
                renewal, new_notum, old_notum, notum_threshold
            ),
        }

    homogeneous_summary = summaries(homogeneous)
    clustered_summary = summaries(clustered)
    assert homogeneous_summary["pooled_EdU_positive_fraction"] == clustered_summary["pooled_EdU_positive_fraction"]
    assert homogeneous_summary["mean_normalized_Notum_per_cell"] == clustered_summary["mean_normalized_Notum_per_cell"]
    assert homogeneous_summary["mean_Notum_in_EdU_positive_cells"] == clustered_summary["mean_Notum_in_EdU_positive_cells"]
    assert homogeneous_summary["mean_Notum_in_EdU_negative_cells"] == clustered_summary["mean_Notum_in_EdU_negative_cells"]
    assert homogeneous_summary["fraction_crypts_passing_functional_threshold"] == 1.0
    assert clustered_summary["fraction_crypts_passing_functional_threshold"] == 0.5

    qbar = 0.5
    tau = round((old_notum - notum_threshold) / (old_notum - new_notum), 12)
    bounds = support_bounds(qbar, tau)

    rate_alias = renewal_rate_alias(
        window_days=21.0,
        mean_labeled_fraction=0.5,
        renewed_crypt_share=0.6,
    )
    assert abs(rate_alias["pooled_EdU_fraction"] - 0.5) < 1e-12

    result = {
        "status": "synthetic exact arithmetic; not biological data or a fitted model",
        "model": {
            "new_cell_Notum_ratio_to_old": new_notum,
            "functional_threshold_normalized_Notum": notum_threshold,
            "equivalent_renewal_threshold": tau,
        },
        "same_aggregate_observables_different_crypt_coverage": {
            "homogeneous_renewal": homogeneous_summary,
            "clustered_renewal": clustered_summary,
        },
        "sharp_coverage_bounds_given_only_mean_renewal": {
            "mean_renewal": qbar,
            "local_renewal_threshold": tau,
            "minimum_functional_crypt_fraction": bounds[0],
            "maximum_functional_crypt_fraction": bounds[1],
        },
        "same_21_day_EdU_mean_different_mean_replacement_rates": rate_alias,
        "interpretation": [
            "Pooled EdU and pooled Notum summaries do not determine the fraction of crypts crossing a local functional threshold.",
            "Even under constant-hazard replacement, a pooled EdU fraction identifies one Laplace-transform value, not the mean rate or its distribution.",
        ],
    }

    out = Path(__file__).with_name("crypt_repair_identifiability_run.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
