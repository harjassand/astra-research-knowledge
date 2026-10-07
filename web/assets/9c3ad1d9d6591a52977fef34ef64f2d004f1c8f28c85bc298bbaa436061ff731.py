#!/usr/bin/env python3
"""Exact output-only learner using FULL responses on the short scalar grid.

Only eval_oracle,n,m enter the learner.  A hidden fixture is accessible only
to its oracle and all-word checker.  Prefix extraction uses width-d identity
chains, never the old scalar-prefix/first-row feature.  The comparison-safe
mode takes detector promise M=2m; residuals sharing hidden transitions need
only M=m.  This replay is finite implementation evidence, not a theorem proof.
"""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
from itertools import product
import json
import time

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("reconstruction", BASE / "reconstruct_abp.py")
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)


def scalar_grid(n, state_bound):
    d = 2 * n * state_bound
    base = []
    for i in range(1, n + 1):
        a = lib.zeros(d)
        for r in range(1, d):
            for q in range(r):
                a[q][r] = Q((-1) ** (r - q - 1), r * i ** (r - q))
        base.append(a)
    # Upper transposes; reversal stays in the same promised realization class.
    return [[[[point * value for value in row] for row in a] for a in base]
            for point in range(1, state_bound + 1)]


def reconstruct(eval_oracle, n, m, comparison_safe=False):
    detector_bound = 2 * m if comparison_safe else m
    grid = scalar_grid(n, detector_bound)
    d = len(grid[0][0])
    feature_cache = {}
    calls = 0
    max_dimension = 0
    response_entries = 0
    description_entries = 0
    response_max_bit_height = 0
    response_payload_bits = 0
    description_payload_bits = 0

    def feature(w):
        nonlocal calls, max_dimension, response_entries, description_entries
        nonlocal response_max_bit_height
        nonlocal response_payload_bits, description_payload_bits
        if w in feature_cache:
            return feature_cache[w]
        k = len(w)
        qdim = (k + 1) * d
        result = []
        for suffix in grid:
            if k == 0:
                x = suffix
            else:
                x = [lib.zeros(qdim) for _ in range(n)]
                for i in range(n):
                    for a in range(d):
                        for b in range(d):
                            x[i][k * d + a][k * d + b] = suffix[i][a][b]
                for j, letter in enumerate(w):
                    for a in range(d):
                        x[letter][j * d + a][(j + 1) * d + a] = Q(1)
            value = eval_oracle(x)
            calls += 1
            max_dimension = max(max_dimension, qdim)
            description_entries += n * qdim * qdim
            response_entries += qdim * qdim
            description_payload_bits += sum(
                1 + max(1, abs(entry.numerator).bit_length()) + entry.denominator.bit_length()
                for matrix in x for row in matrix for entry in row)
            response_payload_bits += sum(
                1 + max(1, abs(entry.numerator).bit_length()) + entry.denominator.bit_length()
                for row in value for entry in row)
            response_max_bit_height = max(
                response_max_bit_height,
                max((max(abs(entry.numerator).bit_length(), entry.denominator.bit_length())
                     for row in value for entry in row), default=0))
            result.extend(value[a][k * d + b] for a in range(d) for b in range(d))
        feature_cache[w] = result
        return result

    basis, basis_words, echelon = [], [], []
    queue = [()]
    pos = 0
    while pos < len(queue):
        w = queue[pos]
        pos += 1
        y = feature(w)
        remainder = y[:]
        for pivot, row in echelon:
            c = remainder[pivot]
            if c:
                remainder = [a - c * b for a, b in zip(remainder, row)]
        pivot = next((j for j, entry in enumerate(remainder) if entry), None)
        if pivot is None:
            continue
        c = remainder[pivot]
        echelon.append((pivot, [entry / c for entry in remainder]))
        basis.append(y)
        basis_words.append(w)
        if len(basis) > m:
            raise ValueError("supplied hidden-state promise is false")
        queue.extend(w + (i,) for i in range(n))

    r = len(basis)
    alpha = lib.coordinates(basis, feature(()))
    beta = [y[0] for y in basis]
    transitions = [lib.zeros(r) for _ in range(n)]
    for a, w in enumerate(basis_words):
        for i in range(n):
            transitions[i][a] = lib.coordinates(basis, feature(w + (i,)))
    assert calls == detector_bound * len(feature_cache)
    assert calls <= detector_bound * (1 + n * r)
    assert max_dimension <= (r + 1) * d
    return {"alpha": alpha, "transitions": transitions, "beta": beta,
            "rank": r, "basis_words": basis_words, "calls": calls,
            "max_dimension": max_dimension, "hitting_dimension": d,
            "features": feature_cache, "detector_state_bound": detector_bound,
            "grid_size": detector_bound, "feature_length": detector_bound * d * d,
            "full_returned_entries": response_entries,
            "full_description_entries": description_entries,
            "full_returned_rational_payload_bits": response_payload_bits,
            "full_description_rational_payload_bits": description_payload_bits,
            "response_max_bit_height": response_max_bit_height}


def fixture_two_state_cycle():
    a = [[Q(1), Q(1)], [Q(0), Q(0)]]
    b = [[Q(0), Q(0)], [Q(1), Q(0)]]
    return lib.ProperSeriesOracle([a, b], [1, 0], [0, 1])


def fixture_five_state_alias():
    a, b = lib.zeros(5), lib.zeros(5)
    a[0][1] = Q(1)
    b[1][3] = Q(1)
    b[0][2] = Q(1)
    a[2][4] = Q(-1)
    a[4][4] = Q(-1)
    b[4][3] = Q(1)
    # Reverse the lower-tuple alias to make it an alias on our upper tuple.
    return lib.ProperSeriesOracle([lib.transpose(a), lib.transpose(b)],
                                  [0, 0, 0, 1, 1], [1, 0, 0, 0, 0])


def finite_hankel_minimality(oracle, prefix_words):
    """Independent finite minor lower bound; source parameters are checker-only."""
    r = len(prefix_words)
    columns, suffix_words, echelon = [], [], []
    for length in range(oracle.m):
        for word in product(range(oracle.n), repeat=length):
            column = [oracle.coefficient(prefix + word) for prefix in prefix_words]
            remainder = column[:]
            for pivot, row in echelon:
                c = remainder[pivot]
                if c:
                    remainder = [a - c * b for a, b in zip(remainder, row)]
            pivot = next((j for j, value in enumerate(remainder) if value), None)
            if pivot is None:
                continue
            c = remainder[pivot]
            echelon.append((pivot, [value / c for value in remainder]))
            columns.append(column)
            suffix_words.append(word)
            if len(columns) == r:
                break
        if len(columns) == r:
            break
    assert len(columns) == r
    a = lib.transpose(columns)
    determinant = Q(1)
    for j in range(r):
        p = next(k for k in range(j, r) if a[k][j])
        if p != j:
            a[p], a[j] = a[j], a[p]
            determinant = -determinant
        pivot = a[j][j]
        determinant *= pivot
        for k in range(j + 1, r):
            c = a[k][j] / pivot
            a[k] = [b - c * e for b, e in zip(a[k], a[j])]
    assert determinant
    return {"rank_lower_bound": r, "prefixes": [list(w) for w in prefix_words],
            "suffixes": [list(w) for w in suffix_words], "minor_determinant": str(determinant),
            "upper_bound": "learned r-state realization and separately certified all-word equality"}


def run_fixture(name, oracle, comparison_safe):
    start = time.perf_counter()
    model = reconstruct(oracle, oracle.n, oracle.m, comparison_safe)
    certificate = lib.equivalence_certificate(oracle, model)
    assert certificate["valid"]
    for w in model["basis_words"]:
        assert len(w) < oracle.m
    result = {key: model[key] for key in (
        "rank", "calls", "max_dimension", "hitting_dimension", "detector_state_bound",
        "grid_size", "feature_length", "full_returned_entries", "full_description_entries",
        "response_max_bit_height", "full_returned_rational_payload_bits",
        "full_description_rational_payload_bits")}
    result.update({"name": name, "hidden_states": oracle.m,
                   "comparison_safe": comparison_safe,
                   "basis_words": [list(w) for w in model["basis_words"]],
                   "all_word_equality_certificate": certificate,
                   "finite_hankel_minimality_certificate": finite_hankel_minimality(oracle, model["basis_words"]),
                   "elapsed_seconds": time.perf_counter() - start})
    return result


def main():
    start = time.perf_counter()
    cases = [
        ("two_state_cycle_native", fixture_two_state_cycle(), False),
        ("two_state_cycle_comparison_2m", fixture_two_state_cycle(), True),
        ("five_state_full_operator_alias_native", fixture_five_state_alias(), False),
    ]
    records = []
    for name, oracle, comparison_safe in cases:
        record = run_fixture(name, oracle, comparison_safe)
        records.append(record)
        print(json.dumps({"case": name, "rank": record["rank"],
                          "calls": record["calls"],
                          "maximum_query_dimension": record["max_dimension"],
                          "elapsed_seconds": record["elapsed_seconds"]}), flush=True)
    result = {"status": "PASS", "interface": "Exact output-only matrix oracle, proper recognizable series; learner sees n,m and callable only.",
              "feature": "All d-by-d residual entries at each of M distinct positive scalar grid points.",
              "prefix_extraction": "Width-d identity chains; no scalar-seed replacement.",
              "fixtures": records, "elapsed_seconds": time.perf_counter() - start,
              "payload_bit_convention": "Per rational: one sign bit, at least one numerator-magnitude bit, denominator bit length; no wire-format framing, and dense structural zeros are charged.",
              "harness_correction": "Draft replay looked for the wrong key in the reused equality-checker result; changed equal_on_every_word lookup to the actual valid status key before the reported run.",
              "scope": "Finite implementation replay with separate reachable-space all-word equality certificates; not a proof of the universal generator or learner.",
              "external_validation": False}
    out = BASE.parents[2] / "results" / "frontier_check_hitting" / "cycle19" / "SCALAR_GRID_RECONSTRUCTION_CHECK.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"],
                      "result_path": str(out)}, indent=2))


if __name__ == "__main__":
    main()
