"""Comparison-only acquisition of quadratic decoders with a polar toggle flag.

All target labels/ranks stay inside the source.  Its truth is read only after
acquisition.  Known-method components are not a novelty or comparator victory.
Stdlib only; cache hits, random draws, source work and checking are charged.
"""
import argparse
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path


def parity(x):
    return x.bit_count() & 1


def lin(rows, x):
    return sum(parity(row & x) << i for i, row in enumerate(rows))


def echelon(rows, n):
    rows = list(rows)
    pivots = []
    rank = 0
    for j in range(n):
        p = next((p for p in range(rank, len(rows)) if rows[p] >> j & 1), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i] >> j & 1:
                rows[i] ^= rows[rank]
        pivots.append(j)
        rank += 1
    return rows[:rank], pivots


def kernel(rows, n):
    reduced, pivots = echelon(rows, n)
    return [sum(((reduced[i] >> f) & 1) << p for i, p in enumerate(pivots))
            | (1 << f) for f in range(n) if f not in pivots]


def solve(rows, rhs, n):
    augmented = [row | (b << n) for row, b in zip(rows, rhs)]
    reduced, pivots = echelon(augmented, n)
    # echelon omits zero coefficient rows, so inspect a separate augmented pass.
    rank = 0
    for j in range(n):
        p = next((p for p in range(rank, len(augmented))
                  if augmented[p] >> j & 1), None)
        if p is None:
            continue
        augmented[rank], augmented[p] = augmented[p], augmented[rank]
        for i in range(len(augmented)):
            if i != rank and augmented[i] >> j & 1:
                augmented[i] ^= augmented[rank]
        rank += 1
    if any(row == 1 << n for row in augmented):
        return None
    return sum(((row >> n) & 1) << p for row, p in zip(reduced, pivots))


def complement(vectors, n):
    kept = list(vectors)
    result = []
    for i in range(n):
        candidate = 1 << i
        if len(echelon(kept + [candidate], n)[1]) > len(kept):
            kept.append(candidate)
            result.append(candidate)
    assert len(kept) == n
    return result


def combine(basis, coefficients):
    out = 0
    while coefficients:
        bit = coefficients & -coefficients
        out ^= basis[bit.bit_length() - 1]
        coefficients ^= bit
    return out


@dataclass
class Quadratic:
    constant: int
    linear: int
    upper: list

    def __call__(self, x):
        value = self.constant ^ parity(self.linear & x)
        active = x
        while active:
            bit = active & -active
            value ^= parity(self.upper[bit.bit_length() - 1] & x)
            active ^= bit
        return value

    def polar(self):
        rows = self.upper.copy()
        for i, upper in enumerate(self.upper):
            while upper:
                bit = upper & -upper
                rows[bit.bit_length() - 1] ^= 1 << i
                upper ^= bit
        return rows

    def body(self):
        return {'constant': self.constant, 'linear': self.linear, 'upper': self.upper}


def coefficient_points(n):
    return [0] + [1 << i for i in range(n)] + [
        (1 << i) | (1 << j) for i in range(n) for j in range(i + 1, n)]


def interpolate(values, n):
    c = values[0]
    linear = sum((values[1 << i] ^ c) << i for i in range(n))
    upper = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            upper[i] |= (values[(1 << i) | (1 << j)] ^ values[1 << i]
                         ^ values[1 << j] ^ c) << j
    return Quadratic(c, linear, upper)


class TriangularTeacher:
    def __init__(self, n, seed):
        start = time.perf_counter()
        rng = random.Random(seed)
        while True:
            rows = [rng.getrandbits(n) for _ in range(n)]
            if len(echelon(rows, n)[1]) == n:
                break
        self._rows, self._offset = rows, rng.getrandbits(n)
        self._g = []
        for j in range(n):
            upper = [rng.getrandbits(j) & ~((1 << (i + 1)) - 1)
                     if i < j else 0 for i in range(n)]
            self._g.append(Quadratic(rng.getrandbits(1), rng.getrandbits(j), upper))
        self.n = n
        self.calls = self.fresh_ranks = 0
        self.cache = {}
        self.setup_seconds = time.perf_counter() - start

    def rank(self, x):
        if x not in self.cache:
            self.fresh_ranks += 1
            u = lin(self._rows, x) ^ self._offset
            rank = 0
            for j, g in enumerate(self._g):
                rank = (rank << 1) | (((u >> j) & 1) ^ g(u))
            self.cache[x] = rank
        return self.cache[x]

    def query(self, x, y):
        self.calls += 1
        return self.rank(x) < self.rank(y)


class FlagCompiler:
    def __init__(self, n):
        self.n = n
        self.quadratics = []
        self.toggles = []
        self.complement = [1 << i for i in range(n)]
        self.sampler_cache = {}
        self.draws = self.random_bits = self.projections = 0
        self.projection_q_evaluations = self.cache_hits = self.enumerated_points = 0
        self.maximum_sampler_cache_entries = 0
        self.certificate_checks = []

    def prefix(self, x):
        return sum(q(x) << j for j, q in enumerate(self.quadratics))

    def project(self, x, target):
        self.projections += 1
        for j, (q, v) in enumerate(zip(self.quadratics, self.toggles)):
            self.projection_q_evaluations += 1
            if q(x) != ((target >> j) & 1):
                x ^= v
        return x

    def sample(self, target, rng):
        r = len(self.complement)
        seed = rng.getrandbits(r)
        self.draws += 1
        self.random_bits += r
        key = (target << r) | seed
        if key not in self.sampler_cache:
            self.sampler_cache[key] = self.project(combine(self.complement, seed), target)
            self.maximum_sampler_cache_entries = max(
                self.maximum_sampler_cache_entries, len(self.sampler_cache))
        else:
            self.cache_hits += 1
        return self.sampler_cache[key]

    def fiber(self, target):
        for seed in range(1 << len(self.complement)):
            self.enumerated_points += 1
            yield self.project(combine(self.complement, seed), target)

    def add(self, q):
        quadratics = self.quadratics + [q]
        radical = kernel([row for p in quadratics for row in p.polar()], self.n)
        response_rows = [sum((p(v) ^ p.constant) << a for a, v in enumerate(radical))
                         for p in quadratics]
        a = solve(response_rows, [0] * len(self.quadratics) + [1], len(radical))
        if a is None:
            return False
        v = combine(radical, a)
        certificate = all(
            all(parity(row & v) == 0 for row in p.polar())
            and (p(v) ^ p.constant) == int(i == len(quadratics) - 1)
            for i, p in enumerate(quadratics))
        assert certificate
        self.quadratics.append(q)
        self.toggles.append(v)
        self.complement = complement(self.toggles, self.n)
        self.sampler_cache = {}
        self.certificate_checks.append(certificate)
        return True


def median_abs_deviation(m):
    assert m % 2 == 1
    return math.comb(m + 1, (m + 1) // 2) / (2 ** (m + 2))


def noisy_bit(point, query, compiler, m, rng):
    prefix = compiler.prefix(point)
    votes = sum(query(point, compiler.sample(prefix, rng)) for _ in range(m))
    return int(votes <= m // 2)


def corrected_bit(point, query, compiler, m, repetitions, rng):
    votes = 0
    for _ in range(repetitions):
        a, b, c = (rng.getrandbits(compiler.n) for _ in range(3))
        value = 0
        for shift in (a, b, a ^ b, c, a ^ c, b ^ c, a ^ b ^ c):
            value ^= noisy_bit(point ^ shift, query, compiler, m, rng)
        votes += value
    return int(votes > repetitions // 2)


def acquire(n, query, seed, beta=0.01, m=127, tail_dimension=7):
    rng = random.Random(seed)
    compiler = FlagCompiler(n)
    points = coefficient_points(n)
    learned = []
    stages = []
    total_start = time.perf_counter()
    while n - len(learned) > tail_dimension:
        k = len(learned)
        residual_size = 1 << (n - k)
        eta = median_abs_deviation(m) + 1 / residual_size
        gap = 0.5 - 7 * eta
        if gap <= 0:
            raise ValueError('Choose larger m or residual tail bound.')
        repetitions = math.ceil(math.log(n * len(points) / beta) / (2 * gap * gap))
        repetitions += 1 - repetitions % 2
        start = time.perf_counter()
        values = {x: corrected_bit(x, query, compiler, m, repetitions, rng) for x in points}
        q = interpolate(values, n)
        certificate_start = time.perf_counter()
        added = compiler.add(q)
        certificate_seconds = time.perf_counter() - certificate_start
        stages.append({'stage': k, 'residual_size': residual_size,
                       'median_samples_per_label': m, 'average_label_error_bound': eta,
                       'rm_trial_error_bound': 7 * eta, 'correction_repetitions': repetitions,
                       'comparison_charge': 7 * m * repetitions * len(points),
                       'stage_failure_bound': len(points) * math.exp(-2 * repetitions * gap * gap),
                       'flag_certificate_acquired': added,
                       'certificate_seconds': certificate_seconds,
                       'stage_seconds_including_source': time.perf_counter() - start})
        if not added:
            return {'status': 'flag_gate_failed', 'stages': stages}, None, compiler
        learned.append(q)
    # This is the only enumeration. Its size is <= 2^tail_dimension, independent
    # of the number of prefixes. Each coefficient point's own prefix is handled.
    start = time.perf_counter()
    remaining = n - len(learned)
    tail_values = [dict() for _ in range(remaining)]
    for x in points:
        prefix = compiler.prefix(x)
        rank = sum(query(y, x) for y in compiler.fiber(prefix) if y != x)
        for j in range(remaining):
            tail_values[j][x] = (rank >> (remaining - j - 1)) & 1
    learned.extend(interpolate(values, n) for values in tail_values)
    receipt = {'status': 'acquired', 'stages': stages, 'n': n,
               'coefficient_points': len(points), 'beta_target': beta,
               'total_failure_bound': sum(s['stage_failure_bound'] for s in stages),
               'tail_dimension_bound': tail_dimension, 'enumerated_residual_dimension': remaining,
               'tail_comparison_upper_bound': len(points) * ((1 << remaining) - 1),
               'tail_seconds_including_source': time.perf_counter() - start,
               'acquisition_seconds_including_source': time.perf_counter() - total_start}
    return receipt, learned, compiler


def learned_rank(quadratics, x):
    out = 0
    for q in quadratics:
        out = (out << 1) | q(x)
    return out


def invert_rank(quadratics, compiler, target_rank):
    k = len(compiler.quadratics)
    n = compiler.n
    target_prefix = sum(((target_rank >> (n - j - 1)) & 1) << j for j in range(k))
    return next(x for x in compiler.fiber(target_prefix)
                if learned_rank(quadratics, x) == target_rank)


def merge_sort(values, query):
    if len(values) <= 1:
        return values
    m = len(values) // 2
    left, right = merge_sort(values[:m], query), merge_sort(values[m:], query)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if query(left[i], right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


def run(n, seed, beta, m, tail_dimension):
    start = time.perf_counter()
    teacher = TriangularTeacher(n, seed)
    receipt, quadratics, compiler = acquire(n, teacher.query, seed + 1000000,
                                           beta=beta, m=m, tail_dimension=tail_dimension)
    receipt.update({'seed': seed, 'source_setup_seconds': teacher.setup_seconds,
                    'source_calls_acquisition': teacher.calls,
                    'source_fresh_ranks_acquisition': teacher.fresh_ranks,
                    'source_rank_bitwork_upper_acquisition': teacher.fresh_ranks * (3 * n ** 3 + 3 * n ** 2),
                    'source_cache_payload_bits_acquisition': len(teacher.cache) * 2 * n,
                    'source_cache_entries_acquisition': len(teacher.cache),
                    'query_input_bits_acquisition': teacher.calls * 2 * n,
                    'returned_bits_acquisition': teacher.calls,
                    'uniform_fiber_draws': compiler.draws,
                    'fiber_random_bits': compiler.random_bits,
                    'random_cube_direction_bits': sum(s['correction_repetitions'] * 3 * n
                                                      for s in receipt['stages']) * len(coefficient_points(n)),
                    'fiber_projection_calls_acquisition': compiler.projections,
                    'fiber_projection_q_evaluations_acquisition': compiler.projection_q_evaluations,
                    'fiber_sampler_cache_hits': compiler.cache_hits,
                    'fiber_sampler_maximum_cache_entries': compiler.maximum_sampler_cache_entries,
                    'fiber_sampler_cache_payload_bits_upper': compiler.maximum_sampler_cache_entries * 2 * n,
                    'tail_enumerated_points_acquisition': compiler.enumerated_points})
    if quadratics is None:
        return receipt
    assert teacher.calls == (sum(s['comparison_charge'] for s in receipt['stages'])
                             + receipt['tail_comparison_upper_bound'])
    source_calls_before_check = teacher.calls
    fresh_before_check = teacher.fresh_ranks
    check_start = time.perf_counter()
    # Evaluator-only truth is accessed strictly after the learner has returned.
    points = coefficient_points(n)
    truth = [interpolate({x: (teacher.rank(x) >> (n - j - 1)) & 1 for x in points}, n)
             for j in range(n)]
    exact_bodies = [q.body() == p.body() for q, p in zip(quadratics, truth)]
    errors = sum(learned_rank(quadratics, x) != teacher.rank(x) for x in range(1 << n))
    prefix_checks = 0
    for target_prefix in range(1 << len(compiler.quadratics)):
        fiber = list(compiler.fiber(target_prefix))
        assert len(fiber) == len(set(fiber)) == (1 << len(compiler.complement))
        assert all(compiler.prefix(x) == target_prefix for x in fiber)
        prefix_checks += len(fiber)
    future_targets = random.Random(seed + 2000000).sample(range(1 << n), min(32, 1 << n))
    assert all(teacher.rank(invert_rank(quadratics, compiler, target)) == target
               for target in future_targets)
    receipt.update({'exact_all_coordinate_bodies': exact_bodies,
                    'exhaustive_rank_points': 1 << n, 'exhaustive_rank_errors': errors,
                    'exhaustive_prefix_fiber_points_checked': prefix_checks,
                    'future_inverse_targets_checked': len(future_targets),
                    'checking_seconds_including_source': time.perf_counter() - check_start,
                    'checking_fresh_source_ranks': teacher.fresh_ranks - fresh_before_check,
                    'source_queries_during_learned_execution': teacher.calls - source_calls_before_check,
                    'compact_coefficient_payload_bits': n * len(points),
                    'toggle_payload_bits': n * len(compiler.toggles),
                    'acquired_coordinate_bodies': [q.body() for q in quadratics],
                    'acquired_toggle_vectors': compiler.toggles,
                    'overall_seconds_before_baseline': time.perf_counter() - start})
    assert all(exact_bodies) and errors == 0
    baseline = TriangularTeacher(n, seed)
    baseline_start = time.perf_counter()
    sorted_points = merge_sort(list(range(1 << n)), baseline.query)
    baseline_seconds = time.perf_counter() - baseline_start
    baseline_correct = all(baseline.rank(x) == rank for rank, x in enumerate(sorted_points))
    receipt['enumeration_baseline'] = {'status': 'exact', 'comparisons': baseline.calls,
                                      'fresh_source_ranks': baseline.fresh_ranks,
                                      'seconds_including_source': baseline_seconds,
                                      'source_setup_seconds': baseline.setup_seconds,
                                      'full_table_points': len(sorted_points),
                                      'correct': baseline_correct}
    receipt['known_method_control'] = 'An equally informed composition using these same sampler/median/RM components ties exactly; no superiority claimed.'
    return receipt


def boundary_witness():
    n = 4
    q = [Quadratic(0, 1, [0, 0, 8, 0]),
         Quadratic(0, 2, [0, 0, 8, 0]),
         Quadratic(0, 4, [0] * n), Quadratic(0, 8, [0] * n)]
    compiler = FlagCompiler(n)
    certs = [compiler.add(p) for p in q[:3]]
    assert certs == [True, True, False]
    ranks = [learned_rank(q, x) for x in range(1 << n)]
    assert len(set(ranks)) == 1 << n
    return {'quadratics': [p.body() for p in q], 'first_three_flag_gates': certs,
            'exact_bijective': True, 'exhaustive_points': 1 << n,
            'boundary': 'A quadratic bijection need not have the sequential polar flag.'}


def analytic_scaling(beta=0.01, m=127, tail_dimension=7):
    cases = []
    for n in (8, 12, 16, 24, 32, 64, 128):
        M = len(coefficient_points(n))
        calls = 0
        for k in range(max(0, n - tail_dimension)):
            eta = median_abs_deviation(m) + 2 ** (-(n - k))
            gap = 0.5 - 7 * eta
            t = math.ceil(math.log(n * M / beta) / (2 * gap * gap))
            t += 1 - t % 2
            calls += 7 * m * t * M
        calls += M * ((1 << min(n, tail_dimension)) - 1)
        cases.append({'n': n, 'comparison_bound': calls,
                      'enumeration_sort_upper_bound': n * (1 << n),
                      'executed': False})
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sizes', default='4,6,8,10,12')
    parser.add_argument('--output', default='ordinal_flag_evidence.json')
    parser.add_argument('--beta', type=float, default=0.01)
    parser.add_argument('--median-samples', type=int, default=127)
    parser.add_argument('--tail-dimension', type=int, default=7)
    args = parser.parse_args()
    cases = []
    result = {'status': 'internally_reconstructed_restricted_compiler_no_novelty_claim',
              'interface': 'n and supplied quadratic-bijection/flag promise; chosen raw-input one-bit comparisons only',
              'cases': cases, 'boundary_witness': boundary_witness(),
              'analytic_unexecuted_scaling': analytic_scaling(args.beta, args.median_samples,
                                                            args.tail_dimension)}
    for n in map(int, args.sizes.split(',')):
        case = run(n, 613003 + n, args.beta, args.median_samples, args.tail_dimension)
        cases.append(case)
        Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({k: v for k, v in case.items() if k != 'acquired_coordinate_bodies'}), flush=True)
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
