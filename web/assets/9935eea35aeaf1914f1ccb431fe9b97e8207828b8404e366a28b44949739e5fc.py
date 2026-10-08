"""Exact-model calculations for paired-sister damage partition/repair separation.

This is an algebraic demonstration under the assumptions in FINAL_REPORT.md.
It does not fit or validate the biological model.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


def logistic(x: float) -> float:
    if x >= 0:
        e = math.exp(-x)
        return 1.0 / (1.0 + e)
    e = math.exp(x)
    return e / (1.0 + e)


def signal_pair(
    p: float,
    k1: float,
    k2: float,
    t: float,
    common_gain: float = 1.0,
    eta1: float = 1.0,
    eta2: float = 1.0,
) -> tuple[float, float]:
    """Return positive sister-channel signals for unit total post-division load."""
    return (
        common_gain * eta1 * p * math.exp(-k1 * t),
        common_gain * eta2 * (1.0 - p) * math.exp(-k2 * t),
    )


def recover_from_two_times(
    t1: float, y11: float, y21: float, t2: float, y12: float, y22: float
) -> dict[str, float]:
    """Recover p and k2-k1 from two physical-channel sister ratios."""
    if not (0.0 < t1 < t2 and min(y11, y21, y12, y22) > 0):
        raise ValueError("times must be positive and ordered; signals must be positive")
    ell1 = math.log(y11 / y21)
    ell2 = math.log(y12 / y22)
    dk = (ell2 - ell1) / (t2 - t1)
    theta = ell1 - dk * t1
    return {"p": logistic(theta), "logit_p": theta, "k2_minus_k1": dk}


def main() -> None:
    # Same one-time sister ratio from partition or repair.
    t_obs = 1.0
    target_ratio = 2.0
    partition_only = signal_pair(p=2 / 3, k1=0.0, k2=0.0, t=t_obs)
    repair_only = signal_pair(p=0.5, k1=0.0, k2=math.log(2.0), t=t_obs)

    # At two times, the ideal common-gain physical channel recovers both terms.
    p_true, k1_true, k2_true = 0.73, 0.12, 0.48
    t1, t2 = 0.04, 0.18
    pair1 = signal_pair(p_true, k1_true, k2_true, t1, common_gain=3.2)
    pair2 = signal_pair(p_true, k1_true, k2_true, t2, common_gain=0.7)
    recovered = recover_from_two_times(t1, *pair1, t2, *pair2)

    # A sister-specific reporter factor alone can create a focus ratio.
    sensor_physical = signal_pair(0.5, 0.0, 0.0, t_obs)
    sensor_focus = signal_pair(0.5, 0.0, 0.0, t_obs, eta1=2.0, eta2=1.0)

    # Delayed-first-read partition error if |k2-k1| <= K.
    K, delay = 0.08, 0.5
    delay_error_bound = math.tanh(K * delay / 4.0)

    # Hoeffding sign-test budget for independent pair scores in [-1,1].
    alpha, target_effect = 0.05, 0.20
    n_pairs_per_arm = math.ceil(4.0 * math.log(2.0 / alpha) / target_effect**2)
    illustrative_q_div = 0.006

    result = {
        "status": "finite algebraic/model check only",
        "one_time_alias": {
            "time": t_obs,
            "target_ratio": target_ratio,
            "partition_model": {
                "p": 2 / 3,
                "k1": 0.0,
                "k2": 0.0,
                "observed_ratio": partition_only[0] / partition_only[1],
            },
            "repair_model": {
                "p": 0.5,
                "k1": 0.0,
                "k2": math.log(2.0),
                "observed_ratio": repair_only[0] / repair_only[1],
            },
        },
        "two_time_recovery": {
            "true": {"p": p_true, "k2_minus_k1": k2_true - k1_true},
            "recovered": recovered,
            "physical_pairs": [list(pair1), list(pair2)],
            "common_gains": [3.2, 0.7],
        },
        "sensor_confounding": {
            "physical_ratio": sensor_physical[0] / sensor_physical[1],
            "focus_ratio_if_eta1_eta2_is_2": sensor_focus[0] / sensor_focus[1],
        },
        "delayed_read": {
            "differential_repair_bound_per_time": K,
            "delay": delay,
            "absolute_partition_fraction_error_bound": delay_error_bound,
        },
        "sample_budget": {
            "alpha": alpha,
            "minimum_mean_difference": target_effect,
            "informative_pairs_per_arm": n_pairs_per_arm,
            "conditional_event_yield_per_random_division": illustrative_q_div,
            "random_divisions_per_arm_in_expectation": math.ceil(
                n_pairs_per_arm / illustrative_q_div
            ),
            "yield_note": (
                "q_div is an explicitly assumed event yield, not inferred from "
                "the reported instantaneous 2C-like cell prevalence."
            ),
        },
        "limitations": [
            "constant exponential repair over the fitted window",
            "positive background-subtracted signals",
            "shared multiplicative gain within a sister pair",
            "no unmodeled sister-specific lesion creation",
            "informative death/tracking loss requires a joint competing-risk model",
            "physical lesion assay and pair identity must be acquired",
        ],
    }
    out = Path(__file__).with_name("CHECK_RUN.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
