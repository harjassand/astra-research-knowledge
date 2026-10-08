#!/usr/bin/env python3
"""Finite arithmetic and conservative full-protocol cost audit.

Run from the workspace root:
  python3 work/agents/c4_hidden_acquisition/slow_readout/slow_readout_witness.py

Checks the three-state CTMC endpoint alias, a finite-probe orbit gap, the
exact two-read-law contrast and its kappa^4 KL limit. It then instantiates the
repaired Euclidean-concentration / confidence-spent doubling bound for a
uniform p_*=1/3 witness, charging calibration and probe founders, all read
blocks, elapsed read time, and the per-block slow-action floor. The q_ramp=0
column is only an optimistic mathematical illustration; no physical action
or ramp has been calibrated. This is finite floating-point arithmetic, not a
proof about nature or a practical assay estimate.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CELL_OBS = HERE.parents[1] / "cell_control" / "cell_observation_design"
sys.path.insert(0, str(CELL_OBS))
from cycle3_hidden_word import cycle_for_d, expm  # noqa: E402


def kl(p: np.ndarray, q: np.ndarray) -> float:
    return float(np.sum(p * np.log(p / q)))


def main() -> None:
    k = 3
    total_rate = 10.0
    alias_lag = 1.0
    d = 4.0 * math.pi / (math.sqrt(3.0) * alias_lag)
    q0 = cycle_for_d(total_rate, 0.0, alias_lag)
    q1 = cycle_for_d(total_rate, d, alias_lag)
    p0_alias = expm(q0 * alias_lag)
    p1_alias = expm(q1 * alias_lag)

    pulse_duration = 0.05
    p0 = expm(q0 * pulse_duration)
    p1 = expm(q1 * pulse_duration)
    import itertools

    orbit_gap = math.inf
    for perm in itertools.permutations(range(k)):
        s = np.eye(k)[:, perm]
        orbit_gap = min(orbit_gap, float(np.linalg.norm(p0 - s.T @ p1 @ s, ord="fro")))

    delta_p = p0 - p1
    asymptotic_kl_coefficient = 0.5 * float(np.linalg.norm(delta_p, ord="fro") ** 2)
    alpha = 0.05
    p_star = 1.0 / 3.0
    lambda_max = max(float(np.max(-np.diag(q0))), float(np.max(-np.diag(q1))))
    read_duration = 0.01

    # Sufficient per-row sample count from the vector norm McDiarmid bound:
    # 1/sqrt(m)+sqrt(log(4K/alpha)/m) <= gamma/(8 sqrt(K)).
    m_row = math.ceil(
        (64.0 * k / orbit_gap**2)
        * (1.0 + math.sqrt(math.log(4.0 * k / alpha))) ** 2
    )
    n_cal = math.ceil(math.log(8.0 * k / alpha) / p_star)
    n_probe = math.ceil(
        (2.0 * m_row + 8.0 * math.log(8.0 * k / alpha)) / p_star
    )
    n_blocks = n_cal + 2 * n_probe
    per_block_ramp_gate = alpha / (4.0 * n_blocks)

    rows = []
    for kappa in (0.4, 0.2, 0.1, 0.05):
        emission = kappa * np.eye(k) + (1.0 - kappa) * np.ones((k, k)) / k
        sigma_min = float(np.linalg.svd(emission, compute_uv=False)[-1])
        pair0 = emission @ p0.T @ emission.T / k
        pair1 = emission @ p1.T @ emission.T / k
        passive_kl = kl(pair0, pair1)
        pair_gap = float(np.linalg.norm(pair0 - pair1, ord="fro"))

        j = 0
        while True:
            r_j = (
                1.0
                + math.sqrt(
                    math.log(
                        4.0
                        * n_blocks
                        * (j + 1)
                        * (j + 2)
                        / alpha
                    )
                )
            ) / math.sqrt(2**j)
            if r_j <= math.sqrt(2.0) * kappa / 16.0:
                break
            j += 1
        max_frames_per_block = 2**j
        q_ramp_optimistic = 0.0
        rho = (
            per_block_ramp_gate - q_ramp_optimistic
        ) / (lambda_max * max_frames_per_block * read_duration)
        reads_total = n_blocks * max_frames_per_block
        wall_seconds_held = reads_total * read_duration
        rows.append(
            {
                "kappa": kappa,
                "sigma_min_emission": sigma_min,
                "passive_pair_law_frobenius_gap": pair_gap,
                "passive_pair_kl": passive_kl,
                "passive_kl_over_kappa4": passive_kl / kappa**4,
                "confidence_spent_max_epoch": j,
                "max_frames_per_block": max_frames_per_block,
                "euclidean_frequency_radius_at_max_epoch": r_j,
                "strictly_positive_rho_if_q_ramp_were_zero": rho,
                "per_block_ramp_gate": per_block_ramp_gate,
                "all_blocks_maximum_frame_budget": reads_total,
                "all_blocks_maximum_held_read_walltime_seconds": wall_seconds_held,
                "all_blocks_maximum_held_read_walltime_years": wall_seconds_held / (365.25 * 24 * 3600),
                "warning": "Excludes every physical ramp, preparation, device, culture, detector and recovery cost; q_ramp=0 is not experimentally established.",
            }
        )

    out = {
        "status": "finite numerical check of a conditional model theorem and its conservative resource bound",
        "hypothesis_generators": {
            "Q0_clockwise_counterclockwise_rates": [5.0, 5.0],
            "Q1_clockwise_counterclockwise_rates": [
                5.0 + 2.0 * math.pi / math.sqrt(3.0),
                5.0 - 2.0 * math.pi / math.sqrt(3.0),
            ],
            "maximum_exit_rate": lambda_max,
        },
        "passive_endpoint_alias": {
            "lag": alias_lag,
            "max_abs_transition_matrix_gap": float(np.max(np.abs(p0_alias - p1_alias))),
        },
        "finite_probe": {
            "duration": pulse_duration,
            "permutation_quotiented_frobenius_gap": orbit_gap,
        },
        "fixed_pair_passive_law": {
            "identity": "J0-J1 = kappa^2/3 * (P0-P1)^T",
            "limit_D_over_kappa4": asymptotic_kl_coefficient,
            "rows": rows,
            "scope": "independent passive two-read pairs only; no lower bound for passive multi-time likelihoods",
        },
        "corrected_full_protocol_cost": {
            "K": k,
            "alpha": alpha,
            "p_star": p_star,
            "row_samples_m": m_row,
            "calibration_founders": n_cal,
            "probe_founders": n_probe,
            "total_blocks": n_blocks,
            "per_block_ramp_probability_gate": per_block_ramp_gate,
            "read_duration_seconds": read_duration,
            "rows": rows,
            "status": "The very large number of founders/frames and tiny positive rho are conservative consequences of this proof bound, not measured device requirements or assay recommendations.",
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
