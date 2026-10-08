#!/usr/bin/env python3
"""Finite synthetic check of the tagwise cancellation algebra.

This is an implementation check, not biological evidence or a proof beyond the
algebra in proof/COPY_INVARIANT_TAGWISE_CONTRAST.md.
"""
from __future__ import annotations

import json
import math
import random


def contrast(y_phase, y_ref, d1, d2):
    return (
        sum(math.log2(y_phase[i] / y_ref[i]) for i in d1) / len(d1)
        - sum(math.log2(y_phase[i] / y_ref[i]) for i in d2) / len(d2)
    )


def pooled(y, d1, d2):
    return math.log2(sum(y[i] for i in d1) / sum(y[i] for i in d2))


def run(seed=260108, trials=10000):
    rng = random.Random(seed)
    d1, d2 = [0, 1, 2, 3], [4, 5, 6]
    codes = d1 + d2
    max_tagwise_error = 0.0
    pooled_bias_examples = []
    for _ in range(trials):
        copy = [2 ** rng.uniform(-3, 3) for _ in codes]
        bias = [2 ** rng.uniform(-2, 2) for _ in codes]
        theta0 = [[2 ** rng.uniform(-2, 1) for _ in codes] for _ in range(2)]
        theta1 = [[theta0[m][i] * 2 ** rng.uniform(-1, 1) for i in codes] for m in range(2)]
        scale0 = [2 ** rng.uniform(-4, 4) for _ in range(2)]
        scale1 = [2 ** rng.uniform(-4, 4) for _ in range(2)]
        observed0 = [[scale0[m] * bias[i] * copy[i] * theta0[m][i] for i in codes] for m in range(2)]
        observed1 = [[scale1[m] * bias[i] * copy[i] * theta1[m][i] for i in codes] for m in range(2)]
        for m in range(2):
            true = contrast(theta1[m], theta0[m], d1, d2)
            got = contrast(observed1[m], observed0[m], d1, d2)
            max_tagwise_error = max(max_tagwise_error, abs(true - got))
        # A cross-marker H/C pooled contrast is not invariant: its weights
        # depend on the arbitrary copy vector and tagwise occupancies.
        pooled_observed = (pooled(observed1[1], d1, d2) - pooled(observed0[1], d1, d2)) - (
            pooled(observed1[0], d1, d2) - pooled(observed0[0], d1, d2)
        )
        pooled_true = (pooled(theta1[1], d1, d2) - pooled(theta0[1], d1, d2)) - (
            pooled(theta1[0], d1, d2) - pooled(theta0[0], d1, d2)
        )
        if abs(pooled_observed - pooled_true) > 1.0 and len(pooled_bias_examples) < 3:
            pooled_bias_examples.append({
                "copy_weights": copy,
                "pooled_observed_log2_interaction": pooled_observed,
                "per_copy_pooled_log2_interaction": pooled_true,
            })
    result = {
        "seed": seed,
        "trials": trials,
        "max_tagwise_error_under_fixed_copy_and_bias": max_tagwise_error,
        "pooled_noninvariance_examples_over_1_log2_unit": pooled_bias_examples,
        "interpretation": "synthetic algebra/implementation check only; no biological inference",
    }
    assert max_tagwise_error < 1e-12
    assert len(pooled_bias_examples) == 3
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
