#!/usr/bin/env python3
"""Paid scalar Walsh acquisition and retained classical code-trellis inference.

Standard-library-only constructive verifier, not an optimized sparse WHT package.
Integers encode vectors over GF(2). Acquisition never reads the oracle support.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import ceil, log, log2
from pathlib import Path
import json
import itertools
import random
import time


def parity(x: int) -> int:
    return x.bit_count() & 1


def linear_combination(vectors: list[int], mask: int) -> int:
    out = 0
    while mask:
        low = mask & -mask
        out ^= vectors[low.bit_length() - 1]
        mask ^= low
    return out


def basis_and_relations(vectors: list[int]) -> tuple[list[int], list[int]]:
    """An echelon basis and a basis of all dependencies of input columns."""
    pivots: dict[int, tuple[int, int]] = {}
    relations = []
    for j, original in enumerate(vectors):
        v, relation = original, 1 << j
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                w, combination = pivots[p]
                v ^= w
                relation ^= combination
            else:
                pivots[p] = (v, relation)
                break
        if not v:
            relations.append(relation)
    return [pivots[p][0] for p in sorted(pivots)], relations


def basis(vectors: list[int]) -> list[int]:
    return basis_and_relations(vectors)[0]


def intersection_basis(left: list[int], right: list[int]) -> list[int]:
    _, relations = basis_and_relations(left + right)
    mask = (1 << len(left)) - 1
    return [linear_combination(left, r & mask) for r in relations]


def span(vectors: list[int]) -> list[int]:
    out = [0]
    for v in vectors:
        out += [x ^ v for x in out]
    return out


def solve_rows(rows: list[int], rhs: list[int]) -> int:
    """Return one solution to row_j dot x = rhs_j; free bits are zero."""
    pivots: dict[int, tuple[int, int]] = {}
    for row, value in zip(rows, rhs):
        while row:
            p = row.bit_length() - 1
            if p in pivots:
                v, b = pivots[p]
                row ^= v
                value ^= b
            else:
                pivots[p] = (row, value)
                break
        if not row and value:
            raise ValueError("Inconsistent binary equations")
    x = 0
    for p in sorted(pivots):
        row, value = pivots[p]
        if value ^ parity(row & x):
            x |= 1 << p
    assert all(parity(row & x) == b for row, b in zip(rows, rhs))
    return x


def fwht(values: list) -> list:
    """Unnormalized exact Walsh-Hadamard transform."""
    out = list(values)
    step = 1
    while step < len(out):
        for start in range(0, len(out), step * 2):
            for j in range(start, start + step):
                a, b = out[j], out[j + step]
                out[j], out[j + step] = a + b, a - b
        step *= 2
    return out


@dataclass
class ScalarOracle:
    n: int
    support: list[int]
    coefficients: list[int]
    constant: int = 0
    calls: int = 0

    def __call__(self, x: int):
        self.calls += 1
        return self.constant + sum(c if not parity(a & x) else -c
                                   for a, c in zip(self.support, self.coefficients))


def hash_candidate(n: int, sparsity_bound: int, oracle,
                   random_columns: list[int]) -> tuple[dict | None, str]:
    """Construct a candidate, including a possible constant at mask zero.

    The consistency tests are necessary, not sufficient. A collision can
    produce a false candidate; independent validation remains necessary.
    """
    buckets = 1 << len(random_columns)
    inputs = span(random_columns)
    transforms = [fwht([oracle(x ^ shift) for x in inputs])
                  for shift in [0] + [1 << i for i in range(n)]]
    recovered = {}
    for bucket, value in enumerate(transforms[0]):
        if value == 0:
            if any(t[bucket] != 0 for t in transforms[1:]):
                return None, "zero_base_nonzero_shift"
            continue
        if any(abs(t[bucket]) != abs(value) for t in transforms[1:]):
            return None, "non_singleton_magnitude"
        a = sum((1 << i) for i in range(n)
                if (transforms[i + 1][bucket] < 0) != (value < 0))
        hashed = sum(parity(a & col) << i for i, col in enumerate(random_columns))
        if hashed != bucket:
            return None, "inconsistent_hash"
        recovered[a] = Fraction(value, buckets)
        if len(recovered) > sparsity_bound:
            return None, "candidate_exceeds_sparsity_cap"
    return recovered, "candidate_constructed"


def evaluate_sparse(coefficients: dict[int, Fraction], x: int):
    return sum(c if not parity(a & x) else -c for a, c in coefficients.items())


def acquire_certified(n: int, sparsity_bound: int, delta: float,
                      oracle, rng: random.Random) -> dict:
    """Finite-budget exact rational acquisition from scalar queries.

    sparsity_bound S counts ALL nonzero Walsh coefficients, including mask
    zero when the constant is nonzero. Return an exact representation with
    probability >= 1-delta, or an explicitly reported failure. The sum of
    wrong acceptance and reported failure probabilities is <= delta.
    """
    if not (n >= 1 and sparsity_bound >= 1 and 0 < delta < 1):
        raise ValueError("Require n>=1, S>=1, and delta in (0,1)")
    start = time.perf_counter()
    calls = 0
    def query(x):
        nonlocal calls
        calls += 1
        return oracle(x)
    b = (2 * sparsity_bound * sparsity_bound - 1).bit_length()
    attempts_cap = max(1, ceil(log(2 / delta) / log(4)))
    delta_exact = Fraction(str(delta))
    # Audit the confidence bounds with exact rational arithmetic, so a
    # floating logarithm at a ceiling boundary cannot weaken the guarantee.
    while Fraction(1, 4 ** attempts_cap) > delta_exact / 2:
        attempts_cap += 1
    validation_cap = ceil(2 * sparsity_bound * log(2 * attempts_cap / delta))
    while Fraction(2 * sparsity_bound - 1, 2 * sparsity_bound) ** validation_cap > delta_exact / (2 * attempts_cap):
        validation_cap += 1
    attempts = []
    if b >= n:
        size = 1 << n
        transform = fwht([query(x) for x in range(size)])
        recovered = {a: Fraction(value, size) for a, value in enumerate(transform) if value}
        if len(recovered) > sparsity_bound:
            raise ValueError("Observed full table violates the supplied sparsity promise")
        mode, bound = "full_wht", size
    else:
        size = 1 << b
        bound = attempts_cap * ((n + 1) * size + validation_cap)
        mode, recovered = "validated_subspace_hash", None
        for attempt in range(attempts_cap):
            before = calls
            columns = [rng.getrandbits(n) for _ in range(b)]
            candidate, status = hash_candidate(n, sparsity_bound, query, columns)
            record = {"attempt": attempt + 1, "training_queries": calls - before,
                      "construction_status": status, "validation_queries": 0,
                      "candidate_terms": None if candidate is None else len(candidate)}
            if candidate is not None:
                valid = True
                for _ in range(validation_cap):
                    x = rng.getrandbits(n)
                    record["validation_queries"] += 1
                    if query(x) != evaluate_sparse(candidate, x):
                        valid = False
                        break
                record["accepted"] = valid
                if valid:
                    recovered = candidate
                    attempts.append(record)
                    break
            attempts.append(record)
    common = {"success": recovered is not None, "mode": mode, "b": min(b, n),
              "query_count": calls, "query_bound": bound,
              "attempts_cap": attempts_cap, "validation_cap": validation_cap,
              "attempts": attempts, "seconds": time.perf_counter() - start,
              "sparsity_bound_including_constant": sparsity_bound,
              "delta": delta, "prepared_configuration_bits": calls * n}
    if recovered is None:
        return {**common, "reason": "finite_attempt_cap_exhausted"}
    nonconstant = {a: c for a, c in recovered.items() if a}
    return {**common, "support": sorted(nonconstant), "coefficients": nonconstant,
            "constant": recovered.get(0, Fraction(0)),
            "all_coefficients": recovered}


@dataclass
class CompiledTrellis:
    support: list[int]
    n: int
    rank: int
    checks: list[int]
    columns: list[int]
    layers: list[list[int]]
    transitions: list[list[tuple[int, int, int]]]

    @classmethod
    def compile(cls, n: int, support: list[int]):
        primal_basis, checks = basis_and_relations(support)
        m = len(support)
        columns = [sum(((row >> j) & 1) << i for i, row in enumerate(checks))
                   for j in range(m)]
        prefix = [basis(columns[:j]) for j in range(m + 1)]
        suffix = [basis(columns[j:]) for j in range(m + 1)]
        layers = [span(intersection_basis(prefix[j], suffix[j]))
                  for j in range(m + 1)]
        transitions = []
        for j in range(m):
            targets = {s: k for k, s in enumerate(layers[j + 1])}
            edges = []
            for source_index, state in enumerate(layers[j]):
                for bit in (0, 1):
                    target = state ^ (columns[j] if bit else 0)
                    if target in targets:
                        edges.append((source_index, targets[target], bit))
            transitions.append(edges)
        return cls(support, n, len(primal_basis), checks, columns, layers, transitions)

    def partition(self, weights: list[tuple[int, int]]) -> int:
        values = [1]
        for layer, edges, weight in zip(self.layers[1:], self.transitions, weights):
            nxt = [0] * len(layer)
            for source, target, bit in edges:
                nxt[target] += values[source] * weight[bit]
            values = nxt
        return (1 << (self.n - self.rank)) * values[0]

    def minimum(self, costs: list[tuple[int, int]]) -> tuple[int, int, list[int]]:
        values = [0]
        parents = []
        for layer, edges, cost in zip(self.layers[1:], self.transitions, costs):
            nxt = [None] * len(layer)
            parent = [None] * len(layer)
            for source, target, bit in edges:
                if values[source] is None:
                    continue
                candidate = values[source] + cost[bit]
                if nxt[target] is None or candidate < nxt[target]:
                    nxt[target] = candidate
                    parent[target] = (source, bit)
            values = nxt
            parents.append(parent)
        index, bits = 0, []
        for parent in reversed(parents):
            index, bit = parent[index]
            bits.append(bit)
        bits.reverse()
        x = solve_rows(self.support, bits)
        return values[0], x, bits

    @property
    def edge_count(self):
        return sum(map(len, self.transitions))

    @property
    def width(self):
        return max(len(layer).bit_length() - 1 for layer in self.layers)


def dual_partition(n: int, support: list[int], weights: list[tuple[int, int]]) -> int:
    """Independent exact dual-code character-sum implementation."""
    bs, checks = basis_and_relations(support)
    total = 0
    for codeword in span(checks):
        product = 1
        for j, (w0, w1) in enumerate(weights):
            product *= w0 - w1 if (codeword >> j) & 1 else w0 + w1
        total += product
    assert total % (1 << len(checks)) == 0
    return (1 << (n - len(bs))) * (total // (1 << len(checks)))


def make_support(n: int, rank: int, m: int, rng: random.Random) -> list[int]:
    independent = []
    while len(independent) < rank:
        trial = rng.getrandbits(n)
        if len(basis(independent + [trial])) > len(independent):
            independent.append(trial)
    result = list(independent)
    while len(result) < m:
        v = linear_combination(independent, rng.randrange(1, 1 << rank))
        if v not in result:
            result.append(v)
    return sorted(result)


def brute_force(n: int, support: list[int], weights, costs):
    z, best, witness = 0, None, None
    for x in range(1 << n):
        bits = [parity(a & x) for a in support]
        product = 1
        for j, bit in enumerate(bits):
            product *= weights[j][bit]
        z += product
        value = sum(costs[j][bit] for j, bit in enumerate(bits))
        if best is None or value < best:
            best, witness = value, x
    return z, best, witness


def verify_small(rng: random.Random):
    cases = 0
    for n in range(3, 9):
        for trial in range(10):
            rank = rng.randrange(1, n + 1)
            m = min((1 << rank) - 1, rank + rng.randrange(4))
            support = make_support(n, rank, m, rng)
            trellis = CompiledTrellis.compile(n, support)
            weights = [(rng.randrange(1, 6), rng.randrange(1, 6)) for _ in support]
            costs = [(rng.randrange(-5, 6), rng.randrange(-5, 6)) for _ in support]
            direct_z, direct_min, _ = brute_force(n, support, weights, costs)
            optimum, x, bits = trellis.minimum(costs)
            assert direct_z == trellis.partition(weights) == dual_partition(n, support, weights)
            assert direct_min == optimum == sum(costs[j][parity(a & x)]
                                               for j, a in enumerate(support))
            assert all(parity(row & sum(b << j for j, b in enumerate(bits))) == 0
                       for row in trellis.checks)
            d = m - rank
            for j, layer in enumerate(trellis.layers):
                expected_dim = (len(basis(trellis.columns[:j]))
                                + len(basis(trellis.columns[j:])) - d)
                assert len(layer) == 1 << expected_dim
            cases += 1
    return cases


def verify_evidence_obstruction(rng: random.Random):
    """Finite check of the decoding reduction, not evidence of NP-hardness."""
    m, k = 8, 4
    rows = make_support(m, m, m, rng)
    h = rows[:k]
    b = [rng.randrange(2) for _ in range(k)]
    best_y = min(y.bit_count() for y in range(1 << m)
                 if all(parity(row & y) == bit for row, bit in zip(h, b)))
    # T is rows; columns of T^{-1} give y=T^{-1}x. We need its rows as parities.
    inverse_cols = [solve_rows(rows, [(i == j) for i in range(m)]) for j in range(m)]
    inverse_rows = [sum(((col >> i) & 1) << j for j, col in enumerate(inverse_cols))
                    for i in range(m)]
    feasible_x = [x for x in range(1 << m)
                  if all(((x >> i) & 1) == b[i] for i in range(k))]
    best_x = min(sum(parity(a & x) for a in inverse_rows) for x in feasible_x)
    assert len(basis(inverse_rows)) == m
    assert best_x == best_y
    return {"m": m, "k": k, "unconditioned_dependency_count": 0,
            "conditioned_optimum": best_x,
            "decoding_optimum": best_y,
            "evidence": b, "checks": h}


def verify_uncertainty():
    cases, minimum_product = 0, 64
    # Every nonzero spectrum in {-1,0,1}^8: an exact finite check, not a proof.
    for coefficients in itertools.product((-1, 0, 1), repeat=8):
        spectral_support = sum(c != 0 for c in coefficients)
        if not spectral_support:
            continue
        values = fwht(list(coefficients))
        value_support = sum(v != 0 for v in values)
        product = spectral_support * value_support
        assert product >= 8
        minimum_product = min(minimum_product, product)
        cases += 1
    return {"n": 3, "nonzero_spectra_checked": cases,
            "minimum_support_product": minimum_product, "domain_size": 8}


def verify_false_candidate_rejection():
    # f=(1-chi_e0)(1-chi_e1), with four Walsh terms, is zero on every
    # Rz and Rz+e_i for this legal but unlucky R. Structural tests pass.
    n, support = 8, [0, 1, 2, 3]
    oracle = ScalarOracle(n, support, [1, -1, -1, 1])
    columns = [4, 8, 16, 32, 64]
    candidate, status = hash_candidate(n, 4, oracle, columns)
    assert candidate == {} and status == "candidate_constructed"
    training_queries = oracle.calls
    rng = random.Random(20261101)
    count = 0
    for _ in range(32):
        x = rng.getrandbits(n)
        count += 1
        if oracle(x) != evaluate_sparse(candidate, x):
            break
    else:
        raise AssertionError("Fixed finite validation sample missed the collision witness")
    return {"n": n, "true_sparsity_including_constant": 4,
            "training_queries": training_queries,
            "false_candidate_passed_all_hash_consistency_tests": True,
            "validation_queries_before_rejection": count,
            "true_disagreement_fraction": "1/4"}


def main():
    rng = random.Random(20261031)
    start = time.perf_counter()
    small_cases = verify_small(rng)
    n, r, m = 32, 24, 28
    support = make_support(n, r, m, rng)
    coefficients = [rng.choice((-1, 1)) * rng.randrange(1, 6) for _ in support]
    oracle = ScalarOracle(n, support, coefficients, constant=7)
    learned = acquire_certified(n, m + 1, 0.01, oracle, rng)
    assert learned["success"]
    assert learned["support"] == support
    assert learned["constant"] == 7
    assert learned["coefficients"] == dict(zip(support, coefficients))
    compilation_start = time.perf_counter()
    acquired_trellis = CompiledTrellis.compile(n, learned["support"])
    compile_seconds = time.perf_counter() - compilation_start
    # Equally informed retaining classical baseline: same acquired support,
    # standard minimal code trellis. No artificial forgetting baseline.
    retained_classical = CompiledTrellis.compile(n, support)
    assert acquired_trellis.transitions == retained_classical.transitions
    future_tasks = 100
    future_start = time.perf_counter()
    for _ in range(future_tasks):
        weights = [(rng.randrange(1, 10), rng.randrange(1, 10)) for _ in support]
        costs = [(rng.randrange(-9, 10), rng.randrange(-9, 10)) for _ in support]
        z = acquired_trellis.partition(weights)
        assert z == retained_classical.partition(weights) == dual_partition(n, support, weights)
        best, x, bits = acquired_trellis.minimum(costs)
        assert best == retained_classical.minimum(costs)[0]
        assert best == sum(costs[j][parity(a & x)] for j, a in enumerate(support))
    future_seconds = time.perf_counter() - future_start
    noise_support = make_support(17, 5, 7, rng)
    noise_coefs = [rng.choice((-2, -1, 1, 2)) for _ in noise_support]
    noisy_oracle = ScalarOracle(17, noise_support, noise_coefs, constant=3)
    def rounded_noisy(x):
        measurement = noisy_oracle(x) + Fraction(((x * 1103515245 + 12345) % 9) - 4, 32)
        # Known coefficient lattice is Z; every scalar energy is integral.
        return round(measurement)
    noisy_learned = acquire_certified(17, 8, 0.01, rounded_noisy, rng)
    assert noisy_learned["success"]
    assert noisy_learned["support"] == noise_support
    assert noisy_learned["coefficients"] == dict(zip(noise_support, noise_coefs))
    report = {
        "seed": 20261031,
        "small_exhaustive_cases": small_cases,
        "acquisition": {
            "n": n, "m": m, "rank": r, "d": m - r,
            "mode": learned["mode"], "hash_bits": learned["b"],
            "S_including_constant": m + 1, "delta": learned["delta"],
            "charged_scalar_queries": oracle.calls,
            "query_bound": learned["query_bound"],
            "attempts_cap": learned["attempts_cap"],
            "validation_cap": learned["validation_cap"],
            "attempts": learned["attempts"],
            "prepared_configuration_bits": learned["prepared_configuration_bits"],
            "support_exact": True, "coefficient_exact": True,
            "seconds": learned["seconds"],
            "maximum_absolute_possible_training_energy": 7 + sum(map(abs, coefficients)),
        },
        "compiled_operation": {
            "trellis_width": acquired_trellis.width,
            "layer_states": list(map(len, acquired_trellis.layers)),
            "total_edges": acquired_trellis.edge_count,
            "raw_syndrome_transition_upper_bound": 2 * m * (1 << (m - r)),
            "native_configuration_count": 1 << n,
            "compile_seconds": compile_seconds,
            "future_task_pairs": future_tasks,
            "verification_inclusive_seconds": future_seconds,
            "retained_classical_same_transitions": True,
            "all_partition_values_match_independent_dual_formula": True,
            "all_minima_match_retained_classical_and_lift": True,
        },
        "bounded_noise_check": {
            "n": 17, "m": 7, "S_including_constant": 8,
            "known_coefficient_lattice_spacing": 1, "epsilon": "1/8",
            "mode": noisy_learned["mode"], "queries": noisy_oracle.calls,
            "exact_support": True, "exact_coefficients_after_rounding": True,
        },
        "uncertainty_check": verify_uncertainty(),
        "false_candidate_check": verify_false_candidate_rejection(),
        "coordinate_evidence_reduction": verify_evidence_obstruction(rng),
        "total_seconds": time.perf_counter() - start,
        "scope": "Finite synthetic verification; no empirical advantage over retained classical compilation."
    }
    destination = Path(__file__).resolve().parent.parent / "results" / "acquisition.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
