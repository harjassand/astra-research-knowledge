"""Independent small-instance check of the capped random-match decoder.

The learner receives only the scalar comparator.  Target rank bits are used
only after acquisition to produce the finite-test receipt.  This file is an
audit executable, not a source of the mathematical proof.
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "work/continuation/sol03_learning/ordinal_flag.py"
spec = importlib.util.spec_from_file_location("ordinal_for_tournament", SOURCE)
ordinal = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ordinal
spec.loader.exec_module(ordinal)


def rank_rows(rows, n):
    a = [r for r in rows if r]
    pivots = []
    row = 0
    for col in range(n):
        p = next((i for i in range(row, len(a)) if (a[i] >> col) & 1), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        for i in range(len(a)):
            if i != row and ((a[i] >> col) & 1):
                a[i] ^= a[row]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a[:row], pivots


def nullspace(rows, n):
    reduced, pivots = rank_rows(rows, n)
    return [
        (1 << free) | sum(((reduced[i] >> free) & 1) << p
                          for i, p in enumerate(pivots))
        for free in range(n) if free not in pivots
    ]


def combine(basis, mask):
    value = 0
    for i, v in enumerate(basis):
        if (mask >> i) & 1:
            value ^= v
    return value


def preserving_subspace(quadratics, n):
    """Directions preserving all acquired bits for every input."""
    radical = nullspace([row for q in quadratics for row in q.polar()], n)
    rows = [sum((q(v) ^ q.constant) << i for i, v in enumerate(radical))
            for q in quadratics]
    return [combine(radical, mask) for mask in nullspace(rows, len(radical))]


def interpolate_translation(v, n, query, points):
    return ordinal.interpolate({x: 1 ^ int(query(x, x ^ v)) for x in points}, n)


def body(q):
    return q.constant, q.linear, tuple(q.upper)


def random_match_select(basis, n, query, rng, cap):
    """Tournament on directions without interpolating any candidate."""
    if not basis:
        return None, {"status": "UNKNOWN", "queries": 0, "attempts": 0}
    best = basis[0]
    queries = attempts = pairings = 0
    for candidate in basis[1:]:
        matched = False
        for _ in range(cap):
            x = rng.getrandbits(n)
            attempts += 1
            candidate_bit = 1 ^ int(query(x, x ^ candidate))
            best_bit = 1 ^ int(query(x, x ^ best))
            queries += 2
            if candidate_bit != best_bit:
                continue
            # At a match, the comparator chooses the earlier of the two
            # one-coordinate toggles; equal-coordinate ties may go either way.
            answer = int(query(x ^ candidate, x ^ best))
            queries += 1
            pairings += 1
            if answer == candidate_bit:
                best = candidate
            matched = True
            break
        if not matched:
            return None, {"status": "UNKNOWN", "queries": queries,
                          "attempts": attempts, "matched_pairs": pairings}
    return best, {"status": "selected", "queries": queries,
                  "attempts": attempts, "matched_pairs": pairings}


class CountedQuery:
    def __init__(self, oracle):
        self.oracle = oracle
        self.calls = 0

    def __call__(self, x, y):
        assert x != y
        self.calls += 1
        return self.oracle(x, y)


def acquire_random_match(n, query, seed, beta=0.01):
    """Capped complete-flag learner; cap makes failure explicit UNKNOWN."""
    pair_budget = n * (n - 1) // 2
    cap = max(1, math.ceil(math.log2(pair_budget / beta))) if pair_budget else 1
    rng = random.Random(seed)
    points = ordinal.coefficient_points(n)
    learned, toggles, stages = [], [], []
    for j in range(n):
        basis = preserving_subspace(learned, n)
        if len(basis) != n - j:
            return None, {"status": "UNKNOWN", "reason": "flag dimension check",
                          "stages": stages, "cap": cap}
        selected, tournament = random_match_select(basis, n, query, rng, cap)
        if selected is None:
            return None, {"status": "UNKNOWN", "reason": "matching cutoff",
                          "stages": stages, "cap": cap}
        q = interpolate_translation(selected, n, query, points)
        learned.append(q)
        toggles.append(selected)
        stages.append({"stage": j, "subspace_dimension": len(basis),
                       "interpolated_directions": 1,
                       "interpolation_comparisons": len(points),
                       **tournament})
    return (learned, toggles), {"status": "acquired", "stages": stages,
                               "cap": cap, "pair_budget": pair_budget}


def test_case(n, seed, beta=0.01):
    teacher = ordinal.TriangularTeacher(n, seed)
    query = CountedQuery(teacher.query)
    result, receipt = acquire_random_match(n, query, seed + 1000003, beta)
    assert result is not None and receipt["status"] == "acquired", receipt
    learned, toggles = result
    points = ordinal.coefficient_points(n)
    truth = [ordinal.interpolate(
        {x: (teacher.rank(x) >> (n - j - 1)) & 1 for x in points}, n)
        for j in range(n)]
    exact = [body(a) == body(b) for a, b in zip(learned, truth)]
    assert all(exact)
    decoder = lambda x: ordinal.learned_rank(learned, x)
    if n <= 9:
        checked = list(range(1 << n))
    else:
        check_rng = random.Random(seed + 3000001)
        checked = [check_rng.getrandbits(n) for _ in range(4096)]
    rank_errors = sum(decoder(x) != teacher.rank(x) for x in checked)
    inverse_errors = 0
    for x in checked:
        target = teacher.rank(x)
        y = 0
        for q, v, j in zip(learned, toggles, range(n)):
            desired = (target >> (n-j-1)) & 1
            if q(y) != desired:
                y ^= v
        inverse_errors += y != x
    assert rank_errors == 0 and inverse_errors == 0

    prefix_laws = []
    if n <= 8:
        for bits in range(n + 1):
            checked_targets = 0
            for target_prefix in range(1 << bits):
                counts = {}
                for original in range(1 << n):
                    x = original
                    for j in range(bits):
                        desired = (target_prefix >> (bits-j-1)) & 1
                        if learned[j](x) != desired:
                            x ^= toggles[j]
                    assert decoder(x) >> (n-bits) == target_prefix
                    counts[x] = counts.get(x, 0) + 1
                assert len(counts) == 1 << (n-bits)
                assert set(counts.values()) == {1 << bits}
                checked_targets += 1
            prefix_laws.append({"bits": bits, "targets_exhausted": checked_targets,
                                "distinct_outputs_per_target": 1 << (n-bits),
                                "preimages_each": 1 << bits})

    comparison_bound = (n * len(points)
                        + (2 * receipt["cap"] + 1) * receipt["pair_budget"])
    expected_pair_bound = n * len(points) + 5 * receipt["pair_budget"]
    actual = query.calls
    assert actual == sum(s["queries"] + s["interpolation_comparisons"]
                         for s in receipt["stages"])
    assert actual <= comparison_bound
    return {"n": n, "seed": seed, "status": receipt["status"],
            "coordinate_bodies_exact": exact, "rank_check_points": len(checked),
            "rank_errors": rank_errors, "inverse_errors": inverse_errors,
            "prefix_uniformity_exhausted": prefix_laws,
            "actual_comparisons": actual,
            "worst_case_comparison_bound": comparison_bound,
            "unbounded_expected_comparison_upper_bound": expected_pair_bound,
            "random_bits_drawn_for_matching": sum(s["attempts"] * n
                                                   for s in receipt["stages"]),
            "input_transmission_bits": 2 * n * actual,
            "stages": receipt["stages"], "cap": receipt["cap"],
            "failure_probability_bound": beta,
            "source_calls_during_acquisition": teacher.calls,
            "source_unique_rank_cache_entries": len(teacher.cache)}


class FixedRng:
    def __init__(self, value):
        self.value = value

    def getrandbits(self, n):
        return self.value


def cutoff_test():
    # Identity order: at x=1 the e0/e1 candidate bits differ. A fixed RNG
    # repeats that point, so a short cap must yield UNKNOWN, never a guess.
    n = 2
    rank = lambda x: x
    query = CountedQuery(lambda x, y: rank(x) < rank(y))
    selected, result = random_match_select([1, 2], n, query, FixedRng(1), cap=4)
    assert selected is None and result["status"] == "UNKNOWN"
    assert result["queries"] == 8 and result["attempts"] == 4
    return {"status": result["status"], "attempts": result["attempts"],
            "comparisons": result["queries"], "no_false_selection": selected is None}


def main():
    cases = [test_case(n, 992000 + 17*n + s)
             for n in range(2, 13) for s in range(3)]
    output = {"status": "FINITE_EXACT_AUDIT",
              "algorithm": "fresh global uniform match; one comparison resolves priority; interpolate winner only",
              "case_count": len(cases), "all_exact": all(
                  c["status"] == "acquired" and all(c["coordinate_bodies_exact"])
                  and c["rank_errors"] == 0 and c["inverse_errors"] == 0
                  for c in cases),
              "max_n": max(c["n"] for c in cases), "cases": cases,
              "explicit_cutoff_test": cutoff_test(),
              "proof_boundary": "Complete flag only; partial flag need not make every direction a coordinate toggle."}
    dest = HERE / "optimized_tournament_audit.json"
    dest.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": output["status"], "case_count": len(cases),
                      "all_exact": output["all_exact"], "max_n": output["max_n"],
                      "cutoff_test": output["explicit_cutoff_test"]}, indent=2))


if __name__ == "__main__":
    main()
