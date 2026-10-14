#!/usr/bin/env python3
"""Fresh shared-code Monte Carlo reconstruction of the note's toy campaign.

Uses the pinned research runtime's NumPy. The original simulation script and
random seed were not supplied, so this does not replay or reproduce its exact
reported sample statistics.
"""

import json
import math
import numpy as np


SEED = 20261014
CAMPAIGNS = 100
N = 50_000
TAU = 1.0
RATE = 2.0
T = 2_000.0
C = 100.0
P_LOW = 0.01
P_HIGH = 0.99
A = P_HIGH - P_LOW
PREHISTORY = C + 4 * TAU

EVEN = np.asarray([x for x in range(16) if x.bit_count() % 2 == 0], dtype=np.uint8)
ODD = np.asarray([x for x in range(16) if x.bit_count() % 2 == 1], dtype=np.uint8)
PATTERN_BITS = np.asarray([[(x >> j) & 1 for j in range(4)] for x in range(16)], dtype=np.int8)


def telegraph_flips(rng, start, stop, rate):
    flips = []
    cursor = start
    while True:
        # Exponential interarrival times give a homogeneous Poisson process.
        cursor += float(rng.exponential(1.0 / rate))
        if cursor > stop:
            break
        flips.append(cursor)
    return np.asarray(flips, dtype=np.float64)


def one_model(rng, flips, start_sign, vectors):
    choice = rng.integers(0, len(vectors), size=N)
    x = PATTERN_BITS[vectors[choice]]
    output_time = rng.uniform(0.0, T, size=N)
    ages = C + TAU * (np.arange(4)[None, :] + x)
    entry_time = output_time[:, None] - ages
    flip_count = np.searchsorted(flips, entry_time, side="right")
    code_sign = start_sign * np.where(flip_count % 2 == 0, 1.0, -1.0)
    p_heavy = (1.0 + A * code_sign) / 2.0
    heavy = rng.random((N, 4)) < p_heavy
    k = np.sum(heavy, axis=1)
    weight = np.where(k % 2 == 0, 1.0, -1.0) / A**4
    return float(np.mean(weight))


def main():
    rng = np.random.default_rng(SEED)
    estimates_e, estimates_o = [], []
    for _ in range(CAMPAIGNS):
        start = -PREHISTORY
        stop = T
        start_sign = 1 if rng.integers(0, 2) else -1
        flips = telegraph_flips(rng, start, stop, RATE)
        estimates_e.append(one_model(rng, flips, start_sign, EVEN))
        estimates_o.append(one_model(rng, flips, start_sign, ODD))

    qe = (1 + 6 * math.exp(-4 * RATE * TAU) + math.exp(-8 * RATE * TAU)) / 8
    qo = (math.exp(-2 * RATE * TAU) + math.exp(-6 * RATE * TAU)) / 2
    e = np.asarray(estimates_e)
    o = np.asarray(estimates_o)
    report = {
        "provenance": "fresh simulation; shared telegraph path within each model pair; not a replay of the missing producer script",
        "numpy_version": np.__version__,
        "seed": SEED,
        "campaigns": CAMPAIGNS,
        "products_per_model_per_campaign": N,
        "tau": TAU,
        "r": RATE,
        "observation_duration_T": T,
        "common_delay_C": C,
        "simulated_prehistory": PREHISTORY,
        "p_low": P_LOW,
        "p_high": P_HIGH,
        "telegraph_mean_switches_per_campaign": RATE * (T + PREHISTORY),
        "exact_Q_E": qe,
        "exact_Q_O": qo,
        "mean_campaign_estimate_E": float(np.mean(e)),
        "mean_campaign_estimate_O": float(np.mean(o)),
        "between_campaign_sd_E": float(np.std(e, ddof=1)),
        "between_campaign_sd_O": float(np.std(o, ddof=1)),
        "standard_error_of_100_campaign_mean_E": float(np.std(e, ddof=1) / math.sqrt(CAMPAIGNS)),
        "standard_error_of_100_campaign_mean_O": float(np.std(o, ddof=1) / math.sqrt(CAMPAIGNS)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
