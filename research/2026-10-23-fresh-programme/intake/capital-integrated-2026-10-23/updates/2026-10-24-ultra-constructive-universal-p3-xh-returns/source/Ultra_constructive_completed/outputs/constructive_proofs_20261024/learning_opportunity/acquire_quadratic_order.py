#!/usr/bin/env python3
"""Comparator-only acquisition of quadratic permutations, with paid fibre preparation.

The learner receives n, the quadratic-permutation class promise and a comparator.
Its optional core-rank cap is a resource limit, not a supplied hidden rank.
Teacher truth is opened only
after it returns, for finite validation. Random experiments use Python's PRNG:
these runs validate an implementation, not ideal independent entropy.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from functools import cmp_to_key
import json
import math
from pathlib import Path
import random
import resource
import platform
import time


def parity(x: int) -> int:
    return x.bit_count() & 1


def xor_combination(basis: list[int], mask: int) -> int:
    out = 0
    while mask:
        low = mask & -mask
        out ^= basis[low.bit_length() - 1]
        mask ^= low
    return out


def independent_basis(vectors: list[int]) -> list[int]:
    pivots: dict[int, int] = {}
    answer = []
    for original in vectors:
        x = original
        while x:
            p = x.bit_length() - 1
            if p not in pivots:
                pivots[p] = x
                answer.append(original)
                break
            x ^= pivots[p]
    return answer


def nullspace(rows: list[int], n: int) -> list[int]:
    pivots: dict[int, int] = {}
    for original in rows:
        x = original
        while x:
            p = x.bit_length() - 1
            if p not in pivots:
                pivots[p] = x
                break
            x ^= pivots[p]
    free = [j for j in range(n) if j not in pivots]
    answer = []
    for j in free:
        x = 1 << j
        for p in sorted(pivots):
            if parity(pivots[p] & x):
                x ^= 1 << p
        assert all(parity(row & x) == 0 for row in rows)
        answer.append(x)
    return answer


@dataclass(frozen=True)
class Quadratic:
    n: int
    constant: int
    linear: int
    pairs: tuple[tuple[int, int], ...]

    def __call__(self, x: int) -> int:
        out = self.constant ^ parity(self.linear & x)
        for i, j in self.pairs:
            out ^= ((x >> i) & (x >> j) & 1)
        return out

    def polar_rows(self) -> list[int]:
        rows = [0] * self.n
        for i, j in self.pairs:
            rows[i] ^= 1 << j
            rows[j] ^= 1 << i
        return rows

    def as_dict(self) -> dict:
        return {"constant": self.constant, "linear": self.linear,
                "pairs": [list(pair) for pair in self.pairs]}


def interpolate(values: dict[int, int], n: int) -> Quadratic:
    c = values[0]
    linear = sum((values[1 << i] ^ c) << i for i in range(n))
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            a = values[(1 << i) ^ (1 << j)] ^ values[1 << i] ^ values[1 << j] ^ c
            if a:
                pairs.append((i, j))
    return Quadratic(n, c, linear, tuple(pairs))


class AccountingComparator:
    """A retaining comparator cache is allowed to candidate and baseline alike."""
    def __init__(self, rank, n: int):
        self._rank = rank
        self.n = n
        self.ranks: dict[int, int] = {}
        self.answers: dict[tuple[int, int], bool] = {}
        self.requests = self.physical = self.cache_hits = self.equal_inputs = 0
        self.teacher_seconds = 0.0

    def __call__(self, x: int, y: int) -> bool:
        self.requests += 1
        if x == y:
            self.equal_inputs += 1
            return False
        a, b = (x, y) if x < y else (y, x)
        key = (a, b)
        if key in self.answers:
            self.cache_hits += 1
            answer = self.answers[key]
        else:
            start = time.perf_counter()
            for z in (a, b):
                if z not in self.ranks:
                    self.ranks[z] = self._rank(z)
            self.teacher_seconds += time.perf_counter() - start
            answer = self.ranks[a] < self.ranks[b]
            self.answers[key] = answer
            self.physical += 1
        return answer if x < y else not answer

    def cmp(self, x: int, y: int) -> int:
        if x == y:
            return 0
        return -1 if self(x, y) else 1

    def record(self) -> dict:
        return {"logical_comparison_requests": self.requests,
                "physical_comparisons_after_retention": self.physical,
                "comparison_cache_hits": self.cache_hits,
                "local_equal_input_answers": self.equal_inputs,
                "teacher_unique_rank_evaluations": len(self.ranks),
                "teacher_seconds_in_comparator": self.teacher_seconds,
                "oracle_transmitted_input_bits": 2 * self.n * self.physical,
                "oracle_returned_bits": self.physical,
                "learner_comparison_cache_logical_bits": (2 * self.n + 1) * len(self.answers),
                "teacher_rank_cache_logical_bits": 2 * self.n * len(self.ranks)}


class PrefixSampler:
    """Constructed only from acquired prefix polynomials, never teacher state."""
    def __init__(self, functions: list[Quadratic], n: int, b_bound: int):
        self.functions = tuple(functions)
        self.n, self.t = n, len(functions)
        rows = [row for fn in functions for row in fn.polar_rows()]
        self.radical = nullspace(rows, n)
        self.r = n - len(self.radical)
        if self.r > b_bound:
            raise ValueError("UNKNOWN: acquired joint polar rank exceeds resource cap")
        full = independent_basis(self.radical + [1 << i for i in range(n)])
        self.complement = full[len(self.radical):]
        assert len(self.complement) == self.r
        self.constant = self.prefix(0)
        self.image: dict[int, tuple[int, int]] = {}
        self.kernel: list[int] = []
        for original in self.radical:
            column = self.prefix(original) ^ self.constant
            preimage = original
            while column:
                p = column.bit_length() - 1
                if p not in self.image:
                    self.image[p] = (column, preimage)
                    break
                old_col, old_pre = self.image[p]
                column ^= old_col
                preimage ^= old_pre
            if column == 0:
                self.kernel.append(preimage)
        self.rank_a = len(self.image)
        self.cores: dict[int, list[tuple[int, int]]] = {}
        for z in range(1 << self.r):
            x = xor_combination(self.complement, z)
            value = self.prefix(x)
            syndrome, _ = self.reduce(value)
            self.cores.setdefault(syndrome, []).append((x, value))
        expected_log = self.r + self.rank_a - self.t
        if expected_log < 0 or len(self.cores) != (1 << (self.t - self.rank_a)):
            raise ValueError("UNKNOWN: malformed acquired prefix balance")
        if any(len(bucket) != 1 << expected_log for bucket in self.cores.values()):
            raise ValueError("UNKNOWN: acquired core bucket is unbalanced")
        self.core_choice_bits = expected_log
        assert self.core_choice_bits + len(self.kernel) == n - self.t
        self.samples = self.random_bits = self.enumerated_points = 0

    def prefix(self, x: int) -> int:
        return sum(fn(x) << i for i, fn in enumerate(self.functions))

    def reduce(self, value: int) -> tuple[int, int]:
        preimage = 0
        for p in sorted(self.image, reverse=True):
            if (value >> p) & 1:
                col, pre = self.image[p]
                value ^= col
                preimage ^= pre
        return value, preimage

    def bucket(self, y: int) -> list[tuple[int, int]]:
        syndrome, _ = self.reduce(y)
        return self.cores[syndrome]

    def sample(self, y: int, rng: random.Random) -> int:
        bucket = self.bucket(y)
        core_x, core_value = bucket[rng.getrandbits(self.core_choice_bits)]
        remainder, v = self.reduce(y ^ core_value)
        assert remainder == 0
        v ^= xor_combination(self.kernel, rng.getrandbits(len(self.kernel)))
        x = core_x ^ v
        self.samples += 1
        self.random_bits += self.n - self.t
        return x

    def enumerate(self, y: int) -> list[int]:
        answer = []
        for core_x, core_value in self.bucket(y):
            remainder, particular = self.reduce(y ^ core_value)
            assert remainder == 0
            for mask in range(1 << len(self.kernel)):
                answer.append(core_x ^ particular ^ xor_combination(self.kernel, mask))
        self.enumerated_points += len(answer)
        return answer

    def record(self) -> dict:
        return {"prefix_bits": self.t, "acquired_polar_rank": self.r,
                "radical_dimension": len(self.radical), "image_rank": self.rank_a,
                "core_buckets": len(self.cores), "core_entries": 1 << self.r,
                "core_choice_bits": self.core_choice_bits,
                "kernel_seed_bits": len(self.kernel),
                "fresh_bits_per_sample": self.n - self.t,
                "conditional_samples": self.samples, "conditional_random_bits": self.random_bits,
                "exactly_enumerated_points": self.enumerated_points}


class CompiledAffineCore:
    """Source-free full decoder/inverse after acquisition, with a 2^r core table."""
    def __init__(self, functions: list[Quadratic], n: int):
        final = PrefixSampler(functions, n, n)
        self.n, self.r = n, final.r
        self.radical, self.complement = final.radical, final.complement
        self.l = len(self.radical)

        def acquired_rank(x):
            value = 0
            for fn in functions:
                value = (value << 1) | fn(x)
            return value

        zero = acquired_rank(0)
        self.responses = [acquired_rank(v) ^ zero for v in self.radical]
        self.core = [acquired_rank(xor_combination(self.complement, z)) for z in range(1 << self.r)]
        self.input_coordinates = {}
        for i, original in enumerate(self.radical + self.complement):
            value, coordinate = original, 1 << i
            while value:
                p = value.bit_length() - 1
                if p not in self.input_coordinates:
                    self.input_coordinates[p] = (value, coordinate)
                    break
                old, old_coordinate = self.input_coordinates[p]
                value ^= old
                coordinate ^= old_coordinate
            assert value
        self.output_image = {}
        for raw, original in zip(self.radical, self.responses):
            value, preimage = original, raw
            while value:
                p = value.bit_length() - 1
                if p not in self.output_image:
                    self.output_image[p] = (value, preimage)
                    break
                old, old_preimage = self.output_image[p]
                value ^= old
                preimage ^= old_preimage
            assert value, "bijection forces injective affine response on the radical"
        self.inverse_core = {}
        for z, rank in enumerate(self.core):
            syndrome, _ = self._reduce(self.output_image, rank)
            assert syndrome not in self.inverse_core
            self.inverse_core[syndrome] = z

    @staticmethod
    def _reduce(basis, value):
        output = 0
        for p in sorted(basis, reverse=True):
            if (value >> p) & 1:
                row, item = basis[p]
                value ^= row
                output ^= item
        return value, output

    def rank(self, x: int) -> int:
        remainder, coordinates = self._reduce(self.input_coordinates, x)
        assert remainder == 0
        return self.core[coordinates >> self.l] ^ xor_combination(self.responses, coordinates & ((1 << self.l) - 1))

    def inverse(self, rank: int) -> int:
        syndrome, _ = self._reduce(self.output_image, rank)
        z = self.inverse_core[syndrome]
        remainder, v = self._reduce(self.output_image, rank ^ self.core[z])
        assert remainder == 0
        return xor_combination(self.complement, z) ^ v

    def payload_record(self) -> dict:
        # Logical numeric payload, excluding Python/dictionary overhead.
        return {"core_rank_discovered": self.r, "core_entries": len(self.core),
                "input_basis_bits": self.n * self.n,
                "linear_response_bits": self.n * self.l,
                "core_output_table_bits": self.n * (1 << self.r),
                "numeric_decoder_payload_bits": self.n * self.n + self.n * self.l + self.n * (1 << self.r),
                "inverse_preprocessing_is_additional": True}


def odd_ceiling(x: float) -> int:
    k = math.ceil(x)
    return k if k & 1 else k + 1


class Acquire:
    """Fresh/cached median implementations of the proved acquisition bootstrap."""
    def __init__(self, n: int, b_bound: int, comparator: AccountingComparator,
                 seed: int, delta: float, median_mode: str = "cached"):
        self.n, self.b_bound, self.oracle = n, b_bound, comparator
        self.rng = random.Random(seed)
        self.delta = delta
        self.median_mode = median_mode
        self.functions: list[Quadratic] = []
        self.stages: list[dict] = []
        self.offset_random_bits = 0
        self.support = [0] + [1 << i for i in range(n)]
        self.support += [(1 << i) ^ (1 << j) for i in range(n) for j in range(i + 1, n)]
        epsilon = 1 / 64
        self.k = odd_ceiling(((n + 1) * math.log(2) + math.log(2 / delta)) / (2 * epsilon**2))
        margin = 43 / 128
        self.repeats = odd_ceiling(math.log(2 * n * len(self.support) / delta) / (2 * margin**2))
        self.median_failure_bound = 2 ** (n + 1) * math.exp(-2 * self.k * epsilon**2)
        self.correction_failure_bound = n * len(self.support) * math.exp(-2 * self.repeats * margin**2)
        if median_mode == "fresh":
            self.k = 511
            self.repeats = odd_ceiling(8 * math.log(n * len(self.support) / delta))
            self.median_failure_bound = 0.0
            self.correction_failure_bound = n * len(self.support) * math.exp(-self.repeats / 8)

    def run(self) -> list[Quadratic]:
        for t in range(self.n):
            start = time.perf_counter()
            sampler = PrefixSampler(self.functions, self.n, self.b_bound)
            medians: dict[int, int] = {}
            labels: dict[int, int] = {}
            label_requests = 0
            median_unique_points = 0
            exact_fibres = 0
            median_experiments = 0
            encountered_prefixes = set()
            before = self.oracle.record()

            def weak_label(x: int) -> int:
                nonlocal label_requests, median_unique_points, exact_fibres, median_experiments
                label_requests += 1
                large_fresh = self.median_mode == "fresh" and self.n - t > 6
                if not large_fresh and x in labels:
                    return labels[x]
                prefix = sampler.prefix(x)
                if large_fresh or prefix not in medians:
                    median_experiments += 1
                    encountered_prefixes.add(prefix)
                    if self.n - t <= 6:
                        fibre = sampler.enumerate(prefix)
                        fibre.sort(key=cmp_to_key(self.oracle.cmp))
                        median = fibre[len(fibre) // 2 - 1]
                        exact_fibres += 1
                        median_unique_points += len(fibre)
                    else:
                        counts = Counter(sampler.sample(prefix, self.rng) for _ in range(self.k))
                        values = sorted(counts, key=cmp_to_key(self.oracle.cmp))
                        median_unique_points += len(values)
                        cumulative = 0
                        median = values[-1]
                        for value in values:
                            cumulative += counts[value]
                            if cumulative > self.k // 2:
                                median = value
                                break
                    if not large_fresh:
                        medians[prefix] = median
                else:
                    median = medians[prefix]
                label = int(self.oracle(median, x))
                if not large_fresh:
                    labels[x] = label
                return label

            values = {}
            for x in self.support:
                ones = 0
                for _ in range(self.repeats):
                    a, b, c = (self.rng.getrandbits(self.n) for _ in range(3))
                    self.offset_random_bits += 3 * self.n
                    correction = 0
                    for offset in (a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c):
                        correction ^= weak_label(x ^ offset)
                    ones += correction
                values[x] = int(2 * ones > self.repeats)
            function = interpolate(values, self.n)
            self.functions.append(function)
            after = self.oracle.record()
            self.stages.append({**sampler.record(), "learned_coordinate": t + 1,
                                "median_prefixes_materialised": len(medians),
                                "distinct_prefixes_requiring_median": len(encountered_prefixes),
                                "median_preparation_experiments": median_experiments,
                                "exact_fibres": exact_fibres,
                                "unique_points_sorted_for_medians": median_unique_points,
                                "weak_label_requests": label_requests,
                                "weak_label_cache_entries": len(labels),
                                "physical_comparisons": after["physical_comparisons_after_retention"] - before["physical_comparisons_after_retention"],
                                "logical_comparison_requests": after["logical_comparison_requests"] - before["logical_comparison_requests"],
                                "seconds": time.perf_counter() - start})
        self.final_sampler = PrefixSampler(self.functions, self.n, self.b_bound)
        return self.functions

    def rank(self, x: int) -> int:
        value = 0
        for fn in self.functions:
            value = (value << 1) | fn(x)
        return value

    def inverse(self, rank: int) -> int:
        prefix = sum(((rank >> (self.n - 1 - i)) & 1) << i for i in range(self.n))
        # All random-bit budgets are zero for a full permutation fibre.
        return self.final_sampler.sample(prefix, self.rng)


def gf8_mul(x: int, y: int) -> int:
    value = 0
    while y:
        if y & 1:
            value ^= x
        y >>= 1
        x <<= 1
        if x & 8:
            x ^= 0b1011
    return value


def cube(x: int) -> int:
    return gf8_mul(gf8_mul(x, x), x)


def random_invertible_rows(n: int, rng: random.Random) -> list[int]:
    rows = []
    while len(rows) < n:
        trial = rng.getrandbits(n)
        if len(independent_basis(rows + [trial])) > len(rows):
            rows.append(trial)
    return rows


def affine(rows: list[int], offset: int, x: int) -> int:
    return sum(parity(row & x) << i for i, row in enumerate(rows)) ^ offset


def teacher(n: int, seed: int, family: str):
    rng = random.Random(seed)
    left, right = random_invertible_rows(n, rng), random_invertible_rows(n, rng)
    c, d = rng.getrandbits(n), rng.getrandbits(n)

    def rank(x: int) -> int:
        u = affine(left, c, x)
        if family == "cube":
            z = (u & ~7) | cube(u & 7)
        elif family == "cube_blocks":
            z = u
            for shift in range(0, n - 2, 3):
                z = (z & ~(7 << shift)) | (cube((u >> shift) & 7) << shift)
        elif family == "partial_flag_counterexample":
            common = ((u >> 2) & (u >> 3) & 1)
            z = u ^ (3 if common else 0)
        elif family == "affine":
            z = u
        else:
            raise ValueError(family)
        return affine(right, d, z)
    return rank


def run_case(n: int, family: str, seed: int, delta: float, median_mode: str = "cached") -> dict:
    setup_start = time.perf_counter()
    rank_truth = teacher(n, seed, family)
    teacher_setup_seconds = time.perf_counter() - setup_start
    oracle = AccountingComparator(rank_truth, n)
    # No hidden core bound is supplied: the algorithm discovers every r_t.
    # An implementation may separately impose a user-chosen resource cap.
    acquisition = Acquire(n, n, oracle, seed + 110000, delta, median_mode)
    start = time.perf_counter()
    functions = acquisition.run()
    acquisition_seconds = time.perf_counter() - start
    candidate_peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    acquired_record = oracle.record()

    # Teacher truth enters only in this post-return validation region.
    start = time.perf_counter()
    all_ranks = [acquisition.rank(x) == rank_truth(x) for x in range(1 << n)]
    all_inverse = [acquisition.inverse(y) == x for x, y in ((x, rank_truth(x)) for x in range(1 << n))]
    compiled = CompiledAffineCore(functions, n)
    assert all(compiled.rank(x) == rank_truth(x) for x in range(1 << n))
    assert all(compiled.inverse(rank_truth(x)) == x for x in range(1 << n))
    fibre_checks = 0
    for t in range(n + 1):
        sampler = PrefixSampler(functions[:t], n, acquisition.b_bound)
        expected: dict[int, list[int]] = {}
        for x in range(1 << n):
            expected.setdefault(sampler.prefix(x), []).append(x)
        for y, objects in expected.items():
            actual = sampler.enumerate(y)
            assert sorted(actual) == objects
            assert sampler.core_choice_bits + len(sampler.kernel) == n - t
            fibre_checks += 1
    validation_seconds = time.perf_counter() - start
    assert all(all_ranks) and all(all_inverse)
    assert oracle.record() == acquired_record, "validation must not use comparator"

    baseline_oracle = AccountingComparator(rank_truth, n)
    start = time.perf_counter()
    ordered = sorted(range(1 << n), key=cmp_to_key(baseline_oracle.cmp))
    baseline_table = {x: i for i, x in enumerate(ordered)}
    baseline_seconds = time.perf_counter() - start
    assert all(baseline_table[x] == rank_truth(x) for x in range(1 << n))
    return {"n": n, "family": family, "seed": seed, "delta_requested": delta,
            "median_mode": median_mode, "teacher_setup_seconds": teacher_setup_seconds,
            "median_sample_size": acquisition.k, "correction_repetitions": acquisition.repeats,
            "proved_median_failure_bound": acquisition.median_failure_bound,
            "proved_correction_failure_bound": acquisition.correction_failure_bound,
            "acquisition_seconds": acquisition_seconds, "validation_seconds": validation_seconds,
            "candidate": acquired_record, "offset_random_bits": acquisition.offset_random_bits,
            "candidate_checkpoint_process_peak_rss": candidate_peak_rss,
            "process_peak_rss_unit": "bytes" if platform.system() == "Darwin" else "KiB",
            "peak_rss_scope": "cumulative process peak through acquisition; includes any earlier cases in this process",
            "conditional_random_bits": sum(s["conditional_random_bits"] for s in acquisition.stages),
            "stages": acquisition.stages,
            "learned_polynomials": [fn.as_dict() for fn in functions],
            "supplied_core_rank": None,
            "learned_full_polar_rank": acquisition.final_sampler.r,
            "compiled_affine_core": compiled.payload_record(),
            "validation": {"all_input_ranks": len(all_ranks), "all_input_ranks_correct": all(all_ranks),
                           "all_inverse_targets": len(all_inverse), "all_inverse_correct": all(all_inverse),
                           "every_prefix_fibre_checked": fibre_checks,
                           "source_free_compiled_rank_and_inverse_correct": True,
                           "additional_comparator_calls": 0},
            "equal_information_full_sort_baseline": {**baseline_oracle.record(),
                                                     "seconds": baseline_seconds,
                                                     "rank_table_payload_bits": 2 * n * (1 << n)}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, nargs="+", default=[3, 8, 12])
    parser.add_argument("--family", choices=["cube", "cube_blocks", "partial_flag_counterexample", "affine"], default="cube")
    parser.add_argument("--seed", type=int, default=20261024)
    parser.add_argument("--delta", type=float, default=0.01)
    parser.add_argument("--median-mode", choices=["cached", "fresh"], default="cached")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = []
    for n in args.n:
        record = run_case(n, args.family, args.seed + n, args.delta, args.median_mode)
        records.append(record)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({"status": "FINITE_IMPLEMENTATION_DIAGNOSTIC",
                                           "records": records}, indent=2) + "\n")
        print(json.dumps({"n": n, "family": args.family,
                          "candidate_physical_comparisons": record["candidate"]["physical_comparisons_after_retention"],
                          "sort_physical_comparisons": record["equal_information_full_sort_baseline"]["physical_comparisons_after_retention"],
                          "acquisition_seconds": record["acquisition_seconds"],
                          "all_checks_passed": True}), flush=True)


if __name__ == "__main__":
    main()
