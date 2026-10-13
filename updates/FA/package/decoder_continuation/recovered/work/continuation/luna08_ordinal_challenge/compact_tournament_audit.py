"""Independent exact finite audit of the compact winner-coordinate learner.

The acquisition code sees only strict comparisons. Ground truth is used only
by post-acquisition finite checks and to construct the forced-cutoff fixture.
This deliberately does not import the v2 audit implementation.
"""
from __future__ import annotations

import json
import math
import random
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent


def parity(x: int) -> int:
    return x.bit_count() & 1


def low_weight_masks(nvars: int, degree: int) -> list[int]:
    return [sum(1 << i for i in subset)
            for weight in range(min(nvars, degree) + 1)
            for subset in combinations(range(nvars), weight)]


def gf2_rank(vectors: list[int], ambient: int) -> int:
    rows = [v for v in vectors if v]
    rank = 0
    for col in range(ambient):
        pivot = next((i for i in range(rank, len(rows))
                      if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
        if rank == len(rows):
            break
    return rank


def xor_span(vectors: list[int], coefficient_mask: int) -> int:
    out = 0
    for i, vector in enumerate(vectors):
        if (coefficient_mask >> i) & 1:
            out ^= vector
    return out


def interpolate_low_weight(values: dict[int, int], nvars: int,
                           degree: int) -> dict[int, int]:
    points = low_weight_masks(nvars, degree)
    assert set(values) == set(points)
    coefficients: dict[int, int] = {}
    for mask in sorted(points, key=lambda x: (x.bit_count(), x)):
        value = values[mask]
        proper = (mask - 1) & mask
        while True:
            value ^= coefficients.get(proper, 0)
            if proper == 0:
                break
            proper = (proper - 1) & mask
        coefficients[mask] = value
    return coefficients


def evaluate_anf(coefficients: dict[int, int], point: int) -> int:
    value = 0
    for monomial, bit in coefficients.items():
        if bit and (point & monomial) == monomial:
            value ^= 1
    return value


class Teacher:
    """Random hidden-affine triangular map of total degree at most d."""
    def __init__(self, n: int, degree: int, seed: int):
        self.n, self.degree = n, degree
        rng = random.Random(seed)
        while True:
            rows = [rng.getrandbits(n) for _ in range(n)]
            if gf2_rank(rows, n) == n:
                break
        self.rows = rows
        self.offset = rng.getrandbits(n)
        self.g: list[dict[int, int]] = []
        for i in range(n):
            self.g.append({mask: rng.getrandbits(1)
                           for mask in low_weight_masks(i, degree)})
        self.cache: dict[int, int] = {}
        self.comparisons = 0

    def hidden_coordinates(self, x: int) -> list[int]:
        return [parity(row & x) ^ ((self.offset >> i) & 1)
                for i, row in enumerate(self.rows)]

    def output_bits(self, x: int) -> list[int]:
        u = self.hidden_coordinates(x)
        u_mask = sum(bit << i for i, bit in enumerate(u))
        out = []
        for i in range(self.n):
            bit = u[i]
            for monomial, coefficient in self.g[i].items():
                if coefficient and (u_mask & monomial) == monomial:
                    bit ^= 1
            out.append(bit)
        return out

    def rank(self, x: int) -> int:
        if x not in self.cache:
            rank = 0
            for bit in self.output_bits(x):
                rank = (rank << 1) | bit
            self.cache[x] = rank
        return self.cache[x]

    def query(self, x: int, y: int) -> bool:
        assert x != y
        self.comparisons += 1
        return self.rank(x) < self.rank(y)


class CountedQuery:
    def __init__(self, oracle):
        self.oracle = oracle
        self.calls = 0
        self.endpoints: set[int] = set()

    def __call__(self, x: int, y: int) -> bool:
        assert x != y
        self.calls += 1
        self.endpoints.add(x)
        self.endpoints.add(y)
        return self.oracle(x, y)


def select_earliest(basis: list[int], n: int, query, rng,
                    cap: int) -> tuple[int | None, int | None, dict]:
    if not basis:
        return None, None, {"status": "UNKNOWN", "queries": 0,
                            "attempts": 0, "matched_pairs": 0}
    best = basis[0]
    best_index = 0
    queries = attempts = matched_pairs = 0
    for candidate_index, candidate in enumerate(basis[1:], start=1):
        matched = False
        for _ in range(cap):
            x = rng.getrandbits(n)
            attempts += 1
            candidate_bit = 1 ^ int(query(x, x ^ candidate))
            best_bit = 1 ^ int(query(x, x ^ best))
            queries += 2
            if candidate_bit != best_bit:
                continue
            answer = int(query(x ^ candidate, x ^ best))
            queries += 1
            matched_pairs += 1
            if answer == candidate_bit:
                best = candidate
                best_index = candidate_index
            matched = True
            break
        if not matched:
            return None, None, {"status": "UNKNOWN", "queries": queries,
                                "attempts": attempts,
                                "matched_pairs": matched_pairs}
    return best, best_index, {"status": "selected", "queries": queries,
                              "attempts": attempts,
                              "matched_pairs": matched_pairs}


def acquire_compact(n: int, degree: int, query, seed: int,
                    beta: float = 0.01):
    pair_budget = n * (n - 1) // 2
    cap = max(1, math.ceil(math.log2(pair_budget / beta))) if pair_budget else 1
    rng = random.Random(seed)
    winners: list[int] = []
    suffix: list[int] = [1 << i for i in range(n)]
    restricted: list[dict[int, int]] = []
    stages = []
    interpolation_total = response_total = 0

    for k in range(n):
        if len(suffix) != n - k:
            return None, {"status": "UNKNOWN", "reason": "suffix dimension",
                          "stages": stages, "cap": cap}
        if gf2_rank(winners + suffix, n) != n:
            return None, {"status": "UNKNOWN", "reason": "complement rank",
                          "stages": stages, "cap": cap}

        winner, winner_index, tournament = select_earliest(
            suffix, n, query, rng, cap)
        if winner is None:
            return None, {"status": "UNKNOWN", "reason": "matching cutoff",
                          "stages": stages, "cap": cap}

        points = low_weight_masks(k, degree)
        values = {a: 1 ^ int(query(xor_span(winners, a),
                                   xor_span(winners, a) ^ winner))
                  for a in points}
        h = interpolate_low_weight(values, k, degree)
        h0 = evaluate_anf(h, 0)

        # The winner is a suffix-basis vector and already has response one.
        row = []
        for i, vector in enumerate(suffix):
            if i == winner_index:
                row.append(1)
            else:
                q_at_vector = 1 ^ int(query(vector, vector ^ winner))
                row.append(q_at_vector ^ h0)
                response_total += 1
        assert row[winner_index] == 1
        new_suffix = [suffix[i] ^ (winner if row[i] else 0)
                      for i in range(len(suffix)) if i != winner_index]
        assert len(new_suffix) == n - k - 1
        assert gf2_rank(new_suffix, n) == len(new_suffix)

        interpolation_total += len(points)
        stages.append({"stage": k, "suffix_dimension": len(suffix),
                       "winner_basis_index": winner_index,
                       "tournament_queries": tournament["queries"],
                       "tournament_attempts": tournament["attempts"],
                       "interpolation_queries": len(points),
                       "response_queries": len(suffix) - 1,
                       "suffix_after": len(new_suffix)})
        winners.append(winner)
        restricted.append(h)
        suffix = new_suffix

    total_dimension = sum(len(low_weight_masks(k, degree)) for k in range(n))
    lower_bound = sum(math.comb(n, h + 1) for h in range(degree + 1)
                      if h + 1 <= n)
    assert interpolation_total == total_dimension == lower_bound
    assert response_total == pair_budget
    assert not suffix and gf2_rank(winners, n) == n
    return (winners, restricted), {
        "status": "acquired", "stages": stages, "D": total_dimension,
        "known_basis_lower_bound_L": lower_bound,
        "pair_budget": pair_budget, "cap": cap,
        "interpolation_queries": interpolation_total,
        "response_queries": response_total,
        "tournament_queries": sum(s["tournament_queries"] for s in stages),
        "expected_comparison_upper": total_dimension + 6 * pair_budget,
        "unknown_probability_union_bound": pair_budget * (2.0 ** -cap),
        "fresh_matching_random_bits": n * sum(s["tournament_attempts"]
                                               for s in stages),
        "query_argument_bits": 2 * n * query.calls,
        "response_bits": query.calls,
        "output_coefficient_bits": total_dimension,
        "output_winner_vector_bits": n * n,
        "source_distinct_query_endpoints": len(query.endpoints),
        "worst_case_comparison_bound": total_dimension + (2 * cap + 2) * pair_budget,
    }


def basis_coordinates(vectors: list[int], point: int, n: int) -> int:
    echelon: dict[int, tuple[int, int]] = {}
    for i, vector in enumerate(vectors):
        row, coordinates = vector, 1 << i
        while row:
            pivot = row.bit_length() - 1
            if pivot in echelon:
                old_row, old_coordinates = echelon[pivot]
                row ^= old_row
                coordinates ^= old_coordinates
            else:
                echelon[pivot] = (row, coordinates)
                break
    assert len(echelon) == n
    remainder, coordinates = point, 0
    for pivot in sorted(echelon, reverse=True):
        if (remainder >> pivot) & 1:
            row, row_coordinates = echelon[pivot]
            remainder ^= row
            coordinates ^= row_coordinates
    assert remainder == 0
    return coordinates


def compact_rank(point: int, winners: list[int],
                 restricted: list[dict[int, int]], n: int) -> int:
    t = basis_coordinates(winners, point, n)
    out = 0
    for j, h in enumerate(restricted):
        prefix = t & ((1 << j) - 1)
        bit = ((t >> j) & 1) ^ evaluate_anf(h, prefix)
        out = (out << 1) | bit
    return out


def compact_inverse(rank: int, winners: list[int],
                    restricted: list[dict[int, int]], n: int) -> int:
    t = 0
    for j, h in enumerate(restricted):
        output_bit = (rank >> (n - j - 1)) & 1
        t_bit = output_bit ^ evaluate_anf(h, t & ((1 << j) - 1))
        t |= t_bit << j
    return xor_span(winners, t)


def sample_prefix_fiber(winners: list[int],
                        restricted: list[dict[int, int]], n: int,
                        prefix_bits: int, target: int,
                        free_suffix: int) -> int:
    t = 0
    for j in range(prefix_bits):
        output_bit = (target >> (prefix_bits - j - 1)) & 1
        t_bit = output_bit ^ evaluate_anf(restricted[j], t & ((1 << j) - 1))
        t |= t_bit << j
    for j in range(prefix_bits, n):
        t_bit = (free_suffix >> (n - j - 1)) & 1
        t |= t_bit << j
    return xor_span(winners, t)


def test_case(n: int, degree: int, seed: int) -> dict:
    teacher = Teacher(n, degree, seed)
    query = CountedQuery(teacher.query)
    result, receipt = acquire_compact(n, degree, query, seed + 880001)
    assert result is not None and receipt["status"] == "acquired", receipt
    winners, restricted = result
    assert query.calls == (receipt["interpolation_queries"] +
                           receipt["response_queries"] +
                           receipt["tournament_queries"])
    assert query.calls <= receipt["worst_case_comparison_bound"]

    rank_errors = inverse_errors = 0
    seen_ranks = set()
    for x in range(1 << n):
        predicted = compact_rank(x, winners, restricted, n)
        actual = teacher.rank(x)
        rank_errors += predicted != actual
        inverse_errors += compact_inverse(actual, winners, restricted, n) != x
        seen_ranks.add(predicted)
    assert rank_errors == inverse_errors == 0 and len(seen_ranks) == (1 << n)

    fiber_checks = []
    for k in range(n + 1):
        targets = 0
        for target in range(1 << k):
            sampled = [sample_prefix_fiber(winners, restricted, n, k,
                                           target, free)
                       for free in range(1 << (n - k))]
            assert len(set(sampled)) == 1 << (n - k)
            assert all((teacher.rank(x) >> (n - k)) == target for x in sampled)
            targets += 1
        fiber_checks.append({"prefix_bits": k, "targets_exhausted": targets,
                             "points_per_fiber": 1 << (n - k)})

    return {"n": n, "degree": degree, "seed": seed,
            "status": receipt["status"], "rank_inputs_checked": 1 << n,
            "rank_errors": rank_errors, "inverse_targets_checked": 1 << n,
            "inverse_errors": inverse_errors,
            "prefix_fiber_checks": fiber_checks,
            "actual_comparisons": query.calls,
            "D_equals_known_basis_L": receipt["D"] == receipt["known_basis_lower_bound_L"],
            "D": receipt["D"], "known_basis_lower_bound_L": receipt["known_basis_lower_bound_L"],
            "response_queries": receipt["response_queries"],
            "tournament_queries": receipt["tournament_queries"],
            "matching_random_bits": receipt["fresh_matching_random_bits"],
            "query_argument_bits": receipt["query_argument_bits"],
            "response_bits": receipt["response_bits"],
            "compact_output_bits": (receipt["output_coefficient_bits"] +
                                    receipt["output_winner_vector_bits"]),
            "distinct_source_query_endpoints": receipt["source_distinct_query_endpoints"],
            "capped_worst_case_bound": receipt["worst_case_comparison_bound"],
            "stages": receipt["stages"]}


class FixedRng:
    def __init__(self, value: int):
        self.value = value

    def getrandbits(self, n: int) -> int:
        return self.value


def cutoff_test() -> dict:
    n, degree = 4, 3
    teacher = Teacher(n, degree, 778239)
    query = CountedQuery(teacher.query)
    basis = [1, 2]
    x = next(z for z in range(1 << n)
             if (int(teacher.rank(z) < teacher.rank(z ^ basis[0]))) !=
                (int(teacher.rank(z) < teacher.rank(z ^ basis[1]))))
    winner, index, receipt = select_earliest(basis, n, query,
                                             FixedRng(x), cap=5)
    assert winner is None and index is None and receipt["status"] == "UNKNOWN"
    assert query.calls == receipt["queries"] == 10
    return {"degree": degree, "status": receipt["status"],
            "attempts": receipt["attempts"], "comparisons": query.calls,
            "returns_no_guess": winner is None}


def main() -> None:
    cases = []
    for degree, ns in ((3, range(4, 9)), (4, range(5, 9))):
        for n in ns:
            for seed_offset in range(2):
                cases.append(test_case(n, degree,
                                       918000 + 1009 * degree + 31 * n + seed_offset))
    result = {"status": "EXACT_FINITE_COMPACT_TOURNAMENT_AUDIT",
              "case_count": len(cases), "cases": cases,
              "all_exact": all(c["status"] == "acquired" and
                               c["rank_errors"] == 0 and
                               c["inverse_errors"] == 0 and
                               c["D_equals_known_basis_L"] for c in cases),
              "degree_3_case_count": sum(c["degree"] == 3 for c in cases),
              "degree_4_case_count": sum(c["degree"] == 4 for c in cases),
              "max_n": max(c["n"] for c in cases),
              "cutoff_test": cutoff_test(),
              "scope": "Complete hidden-affine triangular F2 bijection, total degree <= d; compact winner-basis representation; exact strict comparator.",
              "randomness": "Seeded PRNG for reproducibility; theorem requires fresh independent uniform global points."}
    (HERE / "compact_tournament_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "cases": len(cases),
                      "all_exact": result["all_exact"], "max_n": result["max_n"],
                      "cutoff_test": result["cutoff_test"]}, indent=2))


if __name__ == "__main__":
    main()
