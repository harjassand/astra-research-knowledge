#!/usr/bin/env python3
"""Bounded-fair-bit sampler for the certified conditional count receiver.

The error theorem assumes independent fair bits. The CLI uses secrets.randbits
only as a software diagnostic. The certificate accounts for the bounded-rejection
fallback explicitly; it does not assume a floating probability generator.
"""
from pathlib import Path
import argparse
import json
import secrets


def sample_integer_weights(weights, randbits, attempts=32):
    """Sample integer weights, with fallback 0 and failure probability <=2^-attempts."""
    if any(not isinstance(w, int) or w < 0 for w in weights):
        raise ValueError("nonnegative integer weights required")
    total = sum(weights)
    if total <= 0 or attempts < 1:
        raise ValueError("positive total weight and positive attempt cap required")
    width = (total - 1).bit_length()
    for trial in range(1, attempts + 1):
        u = randbits(width) if width else 0
        if not 0 <= u < (1 << width):
            raise ValueError("randbits source returned an out-of-range integer")
        if u >= total:
            continue
        for j, weight in enumerate(weights):
            if u < weight:
                return {"count": j, "attempts": trial, "fair_bits": trial * width,
                        "fallback": False}
            u -= weight
        raise AssertionError("unreachable cumulative selector")
    return {"count": 0, "attempts": attempts, "fair_bits": attempts * width,
            "fallback": True}


def sample_sorted_endpoints(n, k, prefix_mass, randbits, attempts=32):
    """Receive common-denominator integer prefix masses, then sample k sites.

    prefix_mass(F, a) is the signed mass of endpoint sets whose first sites
    are exactly F and whose remaining sites all lie in {a,...,n-1}.
    Its denominator is shared across every query. The caller must provide
    the error and survival certificate from PROOF.md for probabilistic use.
    """
    if not 1 <= k <= n:
        raise ValueError("1 <= k <= n required")
    prefix, decisions, fair_bits, fallbacks, zero_nodes, queries = [], 0, 0, 0, 0, 0
    cache = {}

    def mass(fixed, lower):
        nonlocal queries
        key = (tuple(fixed), lower)
        if key not in cache:
            cache[key] = prefix_mass(tuple(fixed), lower)
            queries += 1
        return cache[key]

    while len(prefix) < k:
        lo = prefix[-1] + 1 if prefix else 0
        hi = n - (k - len(prefix))
        while lo < hi:
            mid = (lo + hi) // 2
            left = mass(prefix, lo) - mass(prefix, mid + 1)
            right = mass(prefix, mid + 1) - mass(prefix, hi + 1)
            weights = [max(0, left), max(0, right)]
            if sum(weights):
                draw = sample_integer_weights(weights, randbits, attempts)
                side = draw["count"]
                fair_bits += draw["fair_bits"]
                fallbacks += draw["fallback"]
            else:
                side = 0
                zero_nodes += 1
            decisions += 1
            if side == 0:
                hi = mid
            else:
                lo = mid + 1
        prefix.append(lo)
    return {"endpoint": prefix, "decisions": decisions, "fair_bits": fair_bits,
            "rejection_fallbacks": fallbacks, "zero_mass_fallbacks": zero_nodes,
            "distinct_prefix_mass_queries": queries}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=3)
    parser.add_argument("--samples", type=int, default=10)
    args = parser.parse_args()
    receipt = json.loads((Path(__file__).parent / "checks_receipt.json").read_text())
    case = receipt["finite_bit_count_cases"][args.case]
    if not case["survival_lower_bound"]["numerator"] or int(case["survival_lower_bound"]["numerator"]) <= 0:
        raise ValueError("a positive certified survival lower bound is required")
    weights = [max(0, int(x)) for x in case["coefficient_integer_numerators"]]
    weights += [0] * (case["k"] + 1 - len(weights))
    draws = [sample_integer_weights(weights, secrets.randbits) for _ in range(args.samples)]
    print(json.dumps({"case": case["name"], "counts": [x["count"] for x in draws],
                      "fair_bits_consumed": sum(x["fair_bits"] for x in draws),
                      "fallbacks": sum(x["fallback"] for x in draws),
                      "scope": "software diagnostic; proof assumes independent fair bits"}, indent=2))


if __name__ == "__main__":
    main()
