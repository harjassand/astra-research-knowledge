"""Self-contained exact tests of the translation tournament at degree 3 and 4.

The oracle exposes only strict comparisons.  Hidden ranks are inspected only
after acquisition for exact finite verification.  No quadratic/polar-form
machinery or Sol03 code is imported.
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


def masks_of_degree_at_most(n: int, degree: int) -> list[int]:
    return [sum(1 << i for i in subset)
            for h in range(min(n, degree) + 1)
            for subset in combinations(range(n), h)]


def gf2_rank(rows: list[int], n: int) -> int:
    a = [r for r in rows if r]
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, len(a))
                      if (a[i] >> col) & 1), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for i in range(len(a)):
            if i != rank and ((a[i] >> col) & 1):
                a[i] ^= a[rank]
        rank += 1
        if rank == len(a):
            break
    return rank


def kernel_one_row(basis: list[int], response: list[int]) -> list[int]:
    """Return a basis for the kernel of response on span(basis)."""
    assert len(basis) == len(response)
    pivot = next((i for i, bit in enumerate(response) if bit), None)
    if pivot is None:
        raise ValueError("UNKNOWN: next-bit response vanishes on the suffix basis")
    result = [basis[i] ^ (basis[pivot] if response[i] else 0)
              for i in range(len(basis)) if i != pivot]
    assert len(result) == len(basis) - 1
    assert gf2_rank(result, max((v.bit_length() for v in basis), default=0)) == len(result)
    return result


class ANF:
    def __init__(self, n: int, degree: int, coefficients: dict[int, int]):
        self.n = n
        self.degree = degree
        self.coefficients = {mask: int(bit) & 1 for mask, bit in coefficients.items()}
        self.coefficients = {mask: bit for mask, bit in self.coefficients.items() if bit}
        assert all(mask.bit_count() <= degree for mask in self.coefficients)

    def __call__(self, x: int) -> int:
        value = 0
        for monomial in self.coefficients:
            if x & monomial == monomial:
                value ^= 1
        return value

    def body(self) -> tuple[int, ...]:
        return tuple(sorted(mask for mask, bit in self.coefficients.items() if bit))

    def degree_actual(self) -> int:
        return max((mask.bit_count() for mask in self.coefficients), default=0)


def interpolate_low_weight(values: dict[int, int], n: int, degree: int) -> ANF:
    """Möbius inversion on all input vectors of Hamming weight <= degree."""
    points = masks_of_degree_at_most(n, degree)
    assert set(values) == set(points)
    points.sort(key=lambda mask: (mask.bit_count(), mask))
    coeff: dict[int, int] = {}
    for monomial in points:
        value = values[monomial]
        sub = (monomial - 1) & monomial
        while True:
            if sub in coeff:
                value ^= coeff[sub]
            if sub == 0:
                break
            sub = (sub - 1) & monomial
        coeff[monomial] = value
    out = ANF(n, degree, coeff)
    assert all(out(x) == values[x] for x in points)
    return out


class TriangularTeacher:
    """Random hidden-affine triangular bijection with total degree <= d."""
    def __init__(self, n: int, degree: int, seed: int):
        self.n, self.degree = n, degree
        rng = random.Random(seed)
        while True:
            rows = [rng.getrandbits(n) for _ in range(n)]
            if gf2_rank(rows, n) == n:
                break
        self.rows = rows
        self.offset = rng.getrandbits(n)
        self.g = []
        for i in range(n):
            monomials = masks_of_degree_at_most(i, degree)
            self.g.append({monomial: rng.getrandbits(1) for monomial in monomials})
        self.cache: dict[int, int] = {}
        self.comparisons = 0

    def hidden_input(self, x: int) -> int:
        return sum((parity(row & x) ^ ((self.offset >> i) & 1)) << i
                   for i, row in enumerate(self.rows))

    def rank(self, x: int) -> int:
        if x not in self.cache:
            u = self.hidden_input(x)
            rank = 0
            for i in range(self.n):
                bit = (u >> i) & 1
                for monomial, coefficient in self.g[i].items():
                    if coefficient and (u & monomial) == monomial:
                        bit ^= 1
                rank = (rank << 1) | bit
            self.cache[x] = rank
        return self.cache[x]

    def query(self, x: int, y: int) -> bool:
        self.comparisons += 1
        assert x != y
        return self.rank(x) < self.rank(y)


class CountedQuery:
    def __init__(self, oracle):
        self.oracle = oracle
        self.calls = 0
        self.points: set[int] = set()

    def __call__(self, x: int, y: int) -> bool:
        assert x != y
        self.calls += 1
        self.points.add(x)
        self.points.add(y)
        return self.oracle(x, y)


def random_match_select(basis: list[int], n: int, query, rng,
                        cap: int) -> tuple[int | None, dict]:
    if not basis:
        return None, {"status": "UNKNOWN", "queries": 0,
                      "attempts": 0, "matched_pairs": 0}
    best = basis[0]
    queries = attempts = matched_pairs = 0
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
            answer = int(query(x ^ candidate, x ^ best))
            queries += 1
            matched_pairs += 1
            # Equal labels at x: the response equals the common label exactly
            # when candidate's coordinate is the earlier one.  Same-coordinate
            # ties can safely select either witness.
            if answer == candidate_bit:
                best = candidate
            matched = True
            break
        if not matched:
            return None, {"status": "UNKNOWN", "queries": queries,
                          "attempts": attempts, "matched_pairs": matched_pairs}
    return best, {"status": "selected", "queries": queries,
                  "attempts": attempts, "matched_pairs": matched_pairs}


def prefix_projection(x: int, bits: int, target: int,
                      polynomials: list[ANF], toggles: list[int]) -> int:
    for j in range(bits):
        desired = (target >> (bits - j - 1)) & 1
        if polynomials[j](x) != desired:
            x ^= toggles[j]
    return x


def rank_from_polynomials(polynomials: list[ANF], x: int) -> int:
    out = 0
    for q in polynomials:
        out = (out << 1) | q(x)
    return out


def acquire(n: int, degree: int, query, seed: int, beta: float = 0.01):
    m_d = len(masks_of_degree_at_most(n, degree))
    pair_budget = n * (n - 1) // 2
    cap = max(1, math.ceil(math.log2(pair_budget / beta))) if pair_budget else 1
    rng = random.Random(seed)
    points = masks_of_degree_at_most(n, degree)
    suffix_basis = [1 << i for i in range(n)]
    polynomials, toggles, stages = [], [], []
    for j in range(n):
        if len(suffix_basis) != n - j:
            return None, {"status": "UNKNOWN", "reason": "suffix dimension",
                          "stages": stages, "cap": cap}
        selected, tournament = random_match_select(suffix_basis, n, query, rng, cap)
        if selected is None:
            return None, {"status": "UNKNOWN", "reason": "matching cutoff",
                          "stages": stages, "cap": cap}
        values = {x: 1 ^ int(query(x, x ^ selected)) for x in points}
        q = interpolate_low_weight(values, n, degree)
        if (q(selected) ^ q(0)) != 1:
            return None, {"status": "UNKNOWN", "reason": "selected translation certificate",
                          "stages": stages, "cap": cap}
        response = [q(v) ^ q(0) for v in suffix_basis]
        new_basis = kernel_one_row(suffix_basis, response)
        stages.append({"stage": j, "suffix_dimension": len(suffix_basis),
                       "tournament_queries": tournament["queries"],
                       "tournament_attempts": tournament["attempts"],
                       "interpolation_queries": m_d,
                       "response_row_rank": 1,
                       "selected_translation": selected})
        polynomials.append(q)
        toggles.append(selected)
        suffix_basis = new_basis
    return (polynomials, toggles), {"status": "acquired", "stages": stages,
                                    "M_d": m_d, "pair_budget": pair_budget,
                                    "cap": cap}


def lower_bound_terms(n: int, degree: int) -> int:
    # Number of independent g_i ANF coefficients when hidden input basis is
    # fixed and known: sum_i sum_h C(i-1,h) = sum_h C(n,h+1).
    return sum(math.comb(n, h + 1) for h in range(degree + 1)
               if h + 1 <= n)


def test_case(n: int, degree: int, seed: int, beta: float = 0.01) -> dict:
    teacher = TriangularTeacher(n, degree, seed)
    query = CountedQuery(teacher.query)
    result, receipt = acquire(n, degree, query, seed + 1000001, beta)
    assert result is not None and receipt["status"] == "acquired", receipt
    polynomials, toggles = result
    points = masks_of_degree_at_most(n, degree)
    truth = [interpolate_low_weight(
        {x: (teacher.rank(x) >> (n - j - 1)) & 1 for x in points}, n, degree)
        for j in range(n)]
    exact_bodies = [q.body() == actual.body()
                    for q, actual in zip(polynomials, truth)]
    assert all(exact_bodies)

    rank_errors = 0
    inverse_errors = 0
    seen = set()
    for x in range(1 << n):
        learned_rank = rank_from_polynomials(polynomials, x)
        true_rank = teacher.rank(x)
        rank_errors += learned_rank != true_rank
        y = 0
        for j, (q, v) in enumerate(zip(polynomials, toggles)):
            target_bit = (true_rank >> (n - j - 1)) & 1
            if q(y) != target_bit:
                y ^= v
        inverse_errors += y != x
        seen.add(y)
    assert rank_errors == 0 and inverse_errors == 0 and len(seen) == (1 << n)

    prefix_laws = []
    if n <= 8:
        for bits in range(n + 1):
            targets = 0
            for target in range(1 << bits):
                counts = Counter(prefix_projection(x, bits, target, polynomials, toggles)
                                 for x in range(1 << n))
                assert len(counts) == 1 << (n - bits)
                assert set(counts.values()) == {1 << bits}
                assert all(rank_from_polynomials(polynomials, y) >> (n-bits) == target
                           for y in counts)
                targets += 1
            prefix_laws.append({"prefix_bits": bits, "targets_exhausted": targets,
                                "fiber_points_each": 1 << (n-bits),
                                "preimages_per_fiber_point": 1 << bits})

    p = receipt["pair_budget"]
    cap = receipt["cap"]
    m_d = receipt["M_d"]
    expected_upper = n * m_d + 5 * p
    max_comparisons = n * m_d + (2 * cap + 1) * p
    assert query.calls == sum(s["interpolation_queries"] + s["tournament_queries"]
                              for s in receipt["stages"])
    assert query.calls <= max_comparisons
    l = lower_bound_terms(n, degree)
    return {"n": n, "degree": degree, "seed": seed,
            "status": receipt["status"], "exact_coordinate_bodies": exact_bodies,
            "all_rank_points_checked": 1 << n, "rank_errors": rank_errors,
            "inverse_targets_checked": 1 << n, "inverse_errors": inverse_errors,
            "prefix_projection_laws": prefix_laws,
            "comparison_count": query.calls, "interpolation_comparison_count": n * m_d,
            "tournament_comparison_count": query.calls - n * m_d,
            "uncapped_expected_comparison_upper": expected_upper,
            "capped_worst_case_comparison_upper": max_comparisons,
            "pair_budget": p, "matching_cap": cap,
            "fresh_random_bits_for_matching": sum(s["tournament_attempts"] * n
                                                  for s in receipt["stages"]),
            "query_argument_bits": 2 * n * query.calls,
            "response_bits": query.calls,
            "M_d": m_d, "known_basis_information_lower_bound_L": l,
            "finite_expected_upper_to_L_ratio": expected_upper / l,
            "source_unique_rank_cache_entries_including_postcheck": len(teacher.cache),
            "distinct_source_rank_inputs_during_acquisition": len(query.points),
            "logical_source_rank_cache_payload_bits_during_acquisition": 2 * n * len(query.points),
            # The actual teacher uses n-bit integer masks. Charge each dense
            # mask membership test O(n) elementary bit work, plus O(n^2) for
            # the affine transform. A scalar-gate evaluator can tighten this
            # to O(n^2 + dL), but that is a different implementation model.
            "source_dense_rank_elementary_bitwork_upper_per_distinct_input": n * n + n * l,
            "stages": receipt["stages"]}


class FixedRng:
    def __init__(self, value: int):
        self.value = value

    def getrandbits(self, n: int) -> int:
        return self.value


def cutoff_test() -> dict:
    """Cutoff behavior is independent of degree; exercise it on a cubic map."""
    n, degree = 4, 3
    teacher = TriangularTeacher(n, degree, 812341)
    query = CountedQuery(teacher.query)
    basis = [1, 2]
    x = next(z for z in range(1 << n)
             if (int(teacher.rank(z) < teacher.rank(z ^ basis[0]))) !=
                (int(teacher.rank(z) < teacher.rank(z ^ basis[1]))))
    selected, result = random_match_select(basis, n, query, FixedRng(x), cap=5)
    assert selected is None and result["status"] == "UNKNOWN"
    assert result["attempts"] == 5 and result["queries"] == 10
    return {"degree": degree, "status": result["status"],
            "attempts": result["attempts"], "comparisons": result["queries"],
            "returns_no_guess": selected is None,
            "test_fixture_uses_hidden_ranks": True}


def main() -> None:
    cases = []
    for degree, ns in ((3, range(4, 10)), (4, range(5, 10))):
        for n in ns:
            for seed_offset in range(3):
                cases.append(test_case(n, degree,
                                       740000 + 101 * degree + 19 * n + seed_offset))
    result = {"status": "EXACT_FINITE_DEGREE3_4_AUDIT",
              "case_count": len(cases), "cases": cases,
              "all_exact": all(c["status"] == "acquired"
                               and all(c["exact_coordinate_bodies"])
                               and c["rank_errors"] == 0
                               and c["inverse_errors"] == 0 for c in cases),
              "max_n": max(c["n"] for c in cases),
              "cutoff_test": cutoff_test(),
              "scope": "Hidden-affine triangular q_i=u_i+g_i(u_<i), total degree <= d, exact strict comparison oracle; degree 3 and 4.",
              "randomness": "Seeded standard-library PRNG for finite reproducibility; theorem uses independent uniform global points."}
    (HERE / "degree3_4_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "cases": len(cases),
                      "all_exact": result["all_exact"], "max_n": result["max_n"],
                      "cutoff_test": result["cutoff_test"]}, indent=2))


if __name__ == "__main__":
    main()
