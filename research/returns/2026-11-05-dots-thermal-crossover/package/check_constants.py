"""Reproduce constants and small-box Ising checks; not a proof of the base theorem."""
from pathlib import Path
import itertools
import json
import math
from fractions import Fraction

ROOT = Path(__file__).resolve().parent
BASE_TITLE = "Exact accepting polymers and a fixed-temperature undecidable order parameter in two dimensions"
BASE_SHA256 = "42b57bfe3212e57db34803dc4f6af6875d5d8a6d3e38f9244958c38a31f0dc0c"


def tail_from_four(alpha):
    return 4 * alpha**4 * (4 / (1 - alpha) + alpha / (1 - alpha)**2)


def exact_plus_ising_box(side):
    sites = list(itertools.product(range(side), repeat=2))
    index = {v: i for i, v in enumerate(sites)}
    edges = []
    external_degrees = []
    for x, y in sites:
        for dx, dy in [(1, 0), (0, 1)]:
            w = (x + dx, y + dy)
            if w in index:
                edges.append((index[(x, y)], index[w]))
        external_degrees.append(sum((x + dx, y + dy) not in index
                                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]))
    partition = 0.0
    first_moment = [0.0] * len(sites)
    for bits in range(1 << len(sites)):
        spins = [1 if (bits >> i) & 1 else -1 for i in range(len(sites))]
        mismatches = sum(spins[i] != spins[j] for i, j in edges)
        mismatches += sum(d for d, spin in zip(external_degrees, spins) if spin == -1)
        weight = math.exp(-6 * mismatches)
        partition += weight
        for i, spin in enumerate(spins):
            first_moment[i] += spin * weight
    magnetizations = [m / partition for m in first_moment]
    return {"side": side, "configurations_enumerated": 1 << len(sites),
            "mean_magnetization": sum(magnetizations) / len(sites),
            "minimum_site_magnetization": min(magnetizations)}


def main():
    epsilon = tail_from_four(3 * math.exp(-6))
    q1 = math.tanh(3)
    delta = tail_from_four(3 * (1 - q1))
    small_boxes = [exact_plus_ising_box(side) for side in range(1, 5)]
    exp6_lower = sum((Fraction(6**k, math.factorial(k)) for k in range(25)), Fraction(0))
    epsilon_upper = tail_from_four(3 / exp6_lower)
    delta_upper = tail_from_four(6 / (1 + exp6_lower))
    result = {
        "base_manuscript_title": BASE_TITLE,
        "base_manuscript_sha256": BASE_SHA256,
        "exact_rational_certificates": {
            "method": "Use sum_{k=0}^{24}6^k/k! < exp(6) and monotonically increasing positive contour tails.",
            "epsilon_upper": str(epsilon_upper),
            "delta_upper": str(delta_upper),
        },
        "epsilon": epsilon,
        "pre_tableau_mean_lower": 1 - 2 * epsilon,
        "q1": q1,
        "delta_common_contour": delta,
        "common_mean_lower": 1 - 2 * delta,
        "common_pair_lower": 1 - 8 * delta,
        "pressure_crossing_constant": 26,
        "small_box_exact_enumeration": small_boxes,
        "checks": {
            "exact_epsilon_bound": epsilon_upper < Fraction(494, 10**10),
            "exact_delta_bound": delta_upper < Fraction(790, 10**9),
            "pre_tableau_mean_gt_0_9999999": 1 - 2 * epsilon > 0.9999999,
            "delta_lt_7_90e_minus7": delta < 7.90e-7,
            "robust_numeric_decision_separates": 1/4 + 1/16 < 1/2 < 1 - 2*epsilon - 1/16,
            "small_boxes_exceed_peierls_bound": all(
                box["minimum_site_magnetization"] >= 1 - 2 * epsilon for box in small_boxes),
        },
        "scope": "Exact rational contour bounds plus floating-point exhaustive finite Ising sums; no validation of halting, all-TI theorem, or asymptotic crossover is inferred."
    }
    assert all(result["checks"].values())
    (ROOT / "numerical_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
