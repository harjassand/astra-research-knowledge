#!/usr/bin/env python3
"""A small exact rational column sampler with an explicit random-bit budget.

This is ordinary inverse-CDF interval sampling, not a new sampling method.
The role is to make the expected-vs-worst-case cost in a frame compiler exact.
"""
from fractions import Fraction as F
from itertools import accumulate
from pathlib import Path
import json


def bounds(weights):
    assert weights and min(weights) > 0 and sum(weights) == 1
    return [F(0)] + list(accumulate(weights))


def cell_owner(prefix, depth, edges):
    lo = F(prefix, 1 << depth)
    hi = F(prefix + 1, 1 << depth)
    for j in range(len(edges) - 1):
        if edges[j] <= lo and hi <= edges[j + 1]:
            return j
    return None


def exact_sample(weights, fair_bit):
    """Return a categorical sample; fair_bit is a fresh unbiased bit oracle.

    Almost-sure finite termination. A non-dyadic weight precludes a finite
    worst-case fair-bit bound for every exact algorithm, not only this one.
    """
    edges = bounds(weights)
    prefix = depth = 0
    while True:
        owner = cell_owner(prefix, depth, edges)
        if owner is not None:
            return owner, depth
        bit = fair_bit()
        assert bit in (0, 1)
        prefix = 2 * prefix + bit
        depth += 1


def unresolved_prefixes(depth, edges):
    out = set()
    for b in edges[1:-1]:
        scaled = b * (1 << depth)
        if scaled.denominator != 1:
            out.add(scaled.numerator // scaled.denominator)
    return out


def analyze(weights, cutoff=64):
    edges = bounds(weights)
    support = len(weights)
    expected_lower = F(0)
    levels = []
    for k in range(cutoff):
        unresolved = unresolved_prefixes(k, edges)
        prob = F(len(unresolved), 1 << k)
        assert prob <= min(F(1), F(support - 1, 1 << k))
        expected_lower += prob
        if k < 12:
            levels.append({"bits": k, "tail_probability": str(prob)})
    tail_bound = F(2 * (support - 1), 1 << cutoff)
    # Exact finite tree propagation: track only unresolved prefixes. This
    # counts every already-terminated leaf without 2^cutoff enumeration.
    active = {0}
    masses = [F(0)] * support
    for k in range(cutoff + 1):
        nxt = set()
        for prefix in active:
            owner = cell_owner(prefix, k, edges)
            if owner is None:
                nxt.update((2 * prefix, 2 * prefix + 1))
            else:
                masses[owner] += F(1, 1 << k)
        if k == cutoff:
            remaining = F(len(nxt), 1 << (k + 1))
            assert sum(masses) + remaining == 1
            for mass, target in zip(masses, weights):
                assert mass <= target and target - mass <= remaining
        active = nxt
    return {"weights": [str(w) for w in weights], "support": support,
            "fair_bit_expected_lower": str(expected_lower),
            "fair_bit_expected_upper": str(expected_lower + tail_bound),
            "finite_tree_depth": cutoff,
            "finite_tree_unresolved_mass": str(remaining),
            "finite_tree_assigned_masses": [str(x) for x in masses],
            "tail_examples": levels,
            "exact_probability_mass_checks": True}


def main():
    examples = [analyze(w) for w in
                ([F(1,3), F(2,3)], [F(1,3), F(1,7), F(11,21)],
                 [F(1,16)] * 16)]
    result = {"method": "ordinary exact inverse-CDF binary interval refinement",
              "expected_bits_bound_r_gt_1": "ceil(log2(r-1))+2",
              "tail_bound": "Pr[B>k] <= min(1,(r-1)*2^-k)",
              "finite_circuit_G_union_tail_bound": "G*(r-1)*2^-k",
              "non_dyadic_weights_have_no_finite_worst_bit_bound": True,
              "examples": examples}
    target = Path(__file__).resolve().parent / "SAMPLER_RESULTS.json"
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
