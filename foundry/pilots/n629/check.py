"""Finite adversarial comparisons, exact probabilities, and fault sensitivity."""
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations_with_replacement
import json
from random import Random
import sys

from common import dump, source_sampler
from reference import (enumerate_pairs, image, joint_kernel,
                       kernel_representatives, prefix_counts, valid, validate)


def compare(sampler, m, blocks, detailed=False):
    pairs = enumerate_pairs(m, blocks)
    assert sampler.total == len(pairs), ("total", m, blocks, sampler.total, len(pairs))
    assert len(pairs) * 4**(2*len(blocks)) >= 4**m
    kernel = joint_kernel(m, blocks)
    if kernel == [0]:
        assert (len(pairs)-1) % 6 == 0
        if len(blocks) and m >= 2*len(blocks):
            assert len(pairs) >= 7
    result = {"m": m, "blocks": blocks, "count": len(pairs),
              "joint_kernel_size": len(kernel), "prefix_checks": 0,
              "unranking_checks": 0, "status": "passed"}
    if not detailed:
        return result
    for bits, count in prefix_counts(m, pairs).items():
        assert sampler.count(bits) == count, ("prefix", m, blocks, bits, count)
        result["prefix_checks"] += 1
    outputs = [sampler.unrank(i) for i in range(sampler.total)]
    assert len(set(outputs)) == len(outputs), "unranking collision"
    assert set(outputs) == set(pairs), "unranking support"
    # Force every rank through draw(): the RNG contract is one uniform integer.
    class ForcedRank:
        def __init__(self, rank):
            self.rank = rank
        def randrange(self, stop):
            assert stop == len(pairs)
            return self.rank
    assert [sampler.draw(ForcedRank(i)) for i in range(len(pairs))] == outputs
    assert all(sampler.valid(u, v) == valid(blocks, u, v)
               for u in range(2**m) for v in range(2**m))
    # Exact rational output mass from a uniform rank, not a frequency estimate.
    masses = Counter(outputs)
    assert all(Fraction(n, len(outputs)) == Fraction(1, len(pairs))
               for n in masses.values())
    marginals = [Counter() for _ in range(3)]
    observed_diagonal = 0
    for u, v in pairs:
        for a in range(2**m):
            triple = (a, a ^ u, a ^ v)
            for i, x in enumerate(triple):
                marginals[i][x] += 1
            observed = [tuple(image(rows, x) for rows in blocks) for x in triple]
            for j in range(len(blocks)):
                assert len({obs[j] for obs in observed}) in (1, 3)
            observed_diagonal += len(set(observed)) == 1
    assert all(len(row) == 2**m and set(row.values()) == {len(pairs)}
               for row in marginals)
    assert observed_diagonal == 2**m * len(kernel)**2
    result.update(unranking_checks=len(outputs), pair_probability=str(Fraction(1, len(pairs))),
                  latent_diagonal_probability=str(Fraction(1, len(pairs))),
                  observed_diagonal_probability=str(Fraction(len(kernel)**2, len(pairs))),
                  exact_kl_log_argument=str(Fraction(4**m, len(pairs))),
                  coupling_triples_checked=2**m*len(pairs),
                  unranking_sha256=hashlib.sha256(json.dumps(outputs).encode()).hexdigest())
    return result


def run():
    Sampler = source_sampler()
    exhaustive = []
    kernel_counts = []
    for m in range(4):
        representatives = kernel_representatives(m)
        kernel_counts.append(len(representatives))
        for w in range(4):
            for blocks in combinations_with_replacement(representatives, w):
                blocks = list(blocks)
                exhaustive.append(compare(Sampler(m, blocks), m, blocks))
    assert kernel_counts == [1, 2, 5, 16]
    cases = [
        ("empty_ambient_empty_family", 0, []),
        ("empty_ambient_zero_maps", 0, [[], [0], [0, 0]]),
        ("empty_family", 4, []),
        ("all_zero_maps", 4, [[], [0], [0, 0]]),
        ("rank_one_only_diagonal_observed", 3, [[1]]),
        ("noninjective_rank_two", 4, [[1, 2]]),
        ("dependent_duplicate_rows_blocks", 4, [[1, 2, 3, 0, 1], [1, 2], []]),
        ("injective_m1", 1, [[1]]),
        ("m_equals_2w", 2, [[1, 2]]),
        ("m_below_2w", 3, [[1, 2], [2, 4]]),
        ("m_above_2w", 5, [[1, 2, 4, 8, 16]]),
        ("w_equals_m_no_plane", 4, [[1], [2], [4], [8]]),
        ("joint_injective_disjoint_blocks", 4, [[1, 2], [4, 8]]),
        ("coordinate_permutation", 4, [[8, 4], [2, 1]]),
    ]
    rng = Random(62920261010)
    for i in range(48):
        m = rng.randrange(1, 5)
        blocks = [[rng.randrange(2**m) for _ in range(rng.randrange(m+3))]
                  for _ in range(rng.randrange(5))]
        cases.append((f"seeded_{i:02}", m, blocks))
    detailed = []
    for name, m, blocks in cases:
        row = compare(Sampler(m, blocks), m, blocks, detailed=True)
        row["case_id"] = name
        detailed.append(row)
    sharp = []
    for i in range(32):
        m, w = (6, 5) if i < 24 else (7, 6)
        blocks = [[rng.randrange(1, 2**m) for _ in range(rng.randrange(1, m+1))]
                  for _ in range(w)]
        row = compare(Sampler(m, blocks), m, blocks)
        row["case_id"] = f"sharp_threshold_{i:02}"
        row["jointly_injective"] = row["joint_kernel_size"] == 1
        row["sharp_counterexample"] = row["jointly_injective"] and row["count"] == 1
        sharp.append(row)
    # Representation invariance, including output basis changes and repeats.
    assert Sampler(4, [[1, 2]]).total == Sampler(4, [[3, 2, 0, 3]]).total
    assert Sampler(4, [[1, 2], [4, 8]]).total == Sampler(4, [[4, 8], [1, 2]]).total
    # Zero/inconsistent prefixes actually occur; tests above compare both.
    assert Sampler(1, [[1]]).count([1]) == 0
    for bad_m, blocks in [(-1, []), (2, [[4]]), (2, [[-1]]), (2, [[1.0]])]:
        try:
            validate(bad_m, blocks)
        except ValueError:
            pass
        else:
            raise AssertionError("oracle failed to reject malformed input")
    detected = []
    for fault in ("total", "prefix", "unrank"):
        honest = Sampler(2, [[1, 2]])
        class Fault:
            total = honest.total + (fault == "total")
            def count(self, p):
                return honest.count(p) + (fault == "prefix")
            def unrank(self, i):
                return honest.unrank(0 if fault == "unrank" else i)
        try:
            compare(Fault(), 2, [[1, 2]], detailed=True)
        except AssertionError:
            detected.append(fault)
        else:
            raise AssertionError(("synthetic fault escaped", fault))
    return {"kind": "finite_diagnostic", "status": "passed", "seed": 62920261010,
            "independent_scientific_verification": False,
            "exhaustive_scope": "All kernel multisets with m<=3,w<=3; output row bases represented once per kernel; repeated kernels included",
            "kernel_counts_by_m": kernel_counts,
            "exhaustive_cases": exhaustive, "detailed_cases": detailed,
            "sharp_threshold_exploration": sharp,
            "summary": {"exhaustive_cases": len(exhaustive), "detailed_cases": len(detailed),
                        "prefix_checks": sum(x["prefix_checks"] for x in detailed),
                        "unranking_checks": sum(x["unranking_checks"] for x in detailed),
                        "coupling_triples_checked": sum(x["coupling_triples_checked"] for x in detailed),
                        "synthetic_faults_detected": detected,
                        "sharp_threshold_cases": len(sharp),
                        "sharp_threshold_jointly_injective": sum(r["jointly_injective"] for r in sharp),
                        "sharp_counterexamples": sum(r["sharp_counterexample"] for r in sharp)},
            "scope": "Independent implementation from definitions, operated by the same exposed audit agent; no expert or formal-kernel certification"}


if __name__ == "__main__":
    result = run()
    dump(sys.argv[1], result)
    print(json.dumps(result["summary"], indent=2))
