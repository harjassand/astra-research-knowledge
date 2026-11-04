"""Constructed two-bit collision example; no outside scientific inputs.

An ideal reciprocal pair collision exchanges |00,11> and |11,00>
with probability s. Each ancillary bit has independent probability p.
Known single-bit refresh rate is gamma. Failure is first register state 11.

This records a simulated reverse intervention, not a physical experiment.
All rare probabilities used in the Bernoulli sampler are exact Fractions.
"""

from fractions import Fraction
import json
import math
import random


def exact_bernoulli(rng, probability):
    return rng.randrange(probability.denominator) < probability.numerator


def mean_first_failure(p, gamma, pair_rate, s):
    return (1 + 2 * p) / (p * p * (2 * gamma + pair_rate * s))


def main():
    p = Fraction(1, 2**40)
    gamma = Fraction(1)
    pair_rate = Fraction(4)
    s = Fraction(1, 2)
    alpha = 0.05
    target_error_s = 0.01
    reverse_probability = (1 - p) ** 2 * s
    target_error_r = target_error_s * float((1 - p) ** 2)
    n = math.ceil(math.log(2 / alpha) / (2 * target_error_r**2))
    rng = random.Random(20261105)
    successes = sum(exact_bernoulli(rng, reverse_probability) for _ in range(n))
    observed = successes / n
    radius = math.sqrt(math.log(2 / alpha) / (2 * n))
    denominator = float((1 - p) ** 2)
    slo = max(0.0, (observed - radius) / denominator)
    shi = min(1.0, (observed + radius) / denominator)
    mtrue = mean_first_failure(p, gamma, pair_rate, s)
    mindependent = mean_first_failure(p, gamma, pair_rate, Fraction(0))
    mlower = mean_first_failure(float(p), float(gamma), float(pair_rate), shi)
    mupper = mean_first_failure(float(p), float(gamma), float(pair_rate), slo)
    result = {
        "model": "two-bit reciprocal pair collision plus independent refresh",
        "status": "simulation, not a physical experiment",
        "seed": 20261105,
        "p_exact": str(p),
        "gamma_per_second": float(gamma),
        "pair_attempt_rate_per_second": float(pair_rate),
        "true_pair_exchange_probability": float(s),
        "natural_pair_failure_rate_per_second": float(pair_rate * s * p * p),
        "reverse_intervention_probability": float(reverse_probability),
        "simulated_reverse_trials": n,
        "reverse_successes": successes,
        "confidence": 1 - alpha,
        "simultaneous_scope": "one scalar pair probability, Hoeffding interval",
        "s_interval": [slo, shi],
        "true_mean_seconds": float(mtrue),
        "mean_interval_seconds": [mlower, mupper],
        "mean_interval_ratio": mupper / mlower,
        "independent_only_mean_seconds": float(mindependent),
        "true_mean_over_independent_mean": float(mtrue / mindependent),
        "interval_contains_truth": mlower <= float(mtrue) <= mupper,
        "per_trial_cost_not_assumed": [
            "prepare register 11",
            "fresh product ancilla preparation",
            "one pair collision",
            "dephasing and output readout",
            "reset for next trial",
        ],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
