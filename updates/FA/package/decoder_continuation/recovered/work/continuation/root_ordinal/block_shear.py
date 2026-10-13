"""Comparison-only full decoder acquisition for an explicit quadratic block class.

The class and exact comparison access are supplied. Only the initial quadratic
top-bit acquisition is probabilistic. This combines standard code correction,
quadratic radicals and affine-order learning; novelty and best-prior advantage
are not asserted. Ground truth is read exclusively after learner termination.
"""
import argparse
import functools
import hashlib
import json
import random
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery/work/phase6/learning_invention')
VENDOR = HERE / 'vendor'
VENDOR.mkdir(exist_ok=True)
receipts = []
for name in ('encoded_operations.py', 'ordinal_topbit.py'):
    source = SOURCE / name
    dest = VENDOR / name
    if not dest.exists():
        shutil.copy2(source, dest)
    assert source.read_bytes() == dest.read_bytes()
    receipts.append({'source': str(source), 'copy': str(dest),
                     'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
sys.path.insert(0, str(VENDOR))
from encoded_operations import (acquire_comparator, inverse, kernel_basis, lin,
                                parity, random_invertible, transpose)
from ordinal_topbit import (acquire_topbit, interpolate_two, points_degree_two,
                           poly_eval)


def polar_rows(terms, n):
    rows = [0] * n
    for term in terms:
        if term.bit_count() == 2:
            first = term & -term
            second = term ^ first
            rows[first.bit_length()-1] ^= second
            rows[second.bit_length()-1] ^= first
    return rows


def independent(columns):
    pivots = {}
    for value in columns:
        while value:
            pivot = value.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def complement(radical, n):
    columns = list(radical)
    out = []
    for i in range(n):
        value = 1 << i
        if independent(columns + [value]) > len(columns):
            out.append(value)
            columns.append(value)
    assert len(columns) == n
    return out


class BlockShearTeacher:
    """Hidden affine input; Q=(y xor g(z),z), top g nondegenerate on z."""
    def __init__(self, n, r, seed):
        assert n >= 8 and 2 <= r < n and r % 2 == 0
        rng = random.Random(seed)
        _, self._decoder = random_invertible(rng, n)
        self._offset = rng.getrandbits(n)
        self.n, self.r, self.k = n, r, n-r
        self._shears = []
        for _ in range(self.k):
            terms = [x for x in points_degree_two(r) if rng.getrandbits(1)]
            self._shears.append(terms)
        # Exact rank-r alternating polar form; any linear/constant coefficients.
        self._shears[-1] = ([0] if rng.getrandbits(1) else []) + [
            1 << i for i in range(r) if rng.getrandbits(1)] + [
            (1 << i) | (1 << (i+1)) for i in range(0, r, 2)]
        self.queries = 0
        self.source_evaluations = 0
        self.cache = {}

    def rank(self, x):
        if x not in self.cache:
            self.source_evaluations += 1
            u = lin(self._decoder, x) ^ self._offset
            z = u & ((1 << self.r)-1)
            value = u
            for i, terms in enumerate(self._shears):
                value ^= poly_eval(terms, z) << (self.r+i)
            self.cache[x] = value
        return self.cache[x]

    def query(self, x, y):
        self.queries += 1
        return self.rank(x) < self.rank(y)


class CompiledDecoder:
    def __init__(self, n, top_terms, duals, transversal, low_decoder, low_offset):
        self.n = n
        self.top_terms = top_terms  # actual significance: low-to-high
        self.duals = duals
        self.transversal = transversal
        self.r = len(transversal)
        self.low_decoder, self.low_offset = low_decoder, low_offset
        basis = duals + transversal
        self.coordinates = inverse(basis)

    def rank(self, x):
        top = sum(poly_eval(q, x) << j for j, q in enumerate(self.top_terms))
        # Quotient coordinates ignore translations in the acquired radical.
        z = lin(self.coordinates, x) >> len(self.duals)
        low = lin(self.low_decoder, z) ^ self.low_offset
        return (top << self.r) | low

    def normalize_top(self, x):
        word = sum(poly_eval(q, x) << j for j, q in enumerate(self.top_terms))
        return x ^ lin(self.duals, word)

    def sample_prefix(self, bits, prefix, rng):
        """Uniform among the actual top `bits` values equal to prefix.

        Normalize requested top bits by their independent radical translations;
        remaining bits retain their uniform distribution. No source queries.
        """
        k = len(self.top_terms)
        if not 0 <= bits <= k:
            raise ValueError('This sampler currently exposes top-block prefixes.')
        x = rng.getrandbits(self.n)
        for i in range(bits):
            j = k-1-i
            desired = (prefix >> (bits-1-i)) & 1
            if poly_eval(self.top_terms[j], x) != desired:
                x ^= self.duals[j]
        return x


def acquire_block(n, query, rng, beta=.01):
    start_queries = 0  # generic oracle exposes no metadata
    top, _, evidence = acquire_topbit(n, query, rng, beta=beta)
    radical = kernel_basis(polar_rows(top, n), n)
    k, r = len(radical), n-len(radical)
    if not (1 <= k < n and r % 2 == 0):
        raise ValueError('UNKNOWN: polar rank inconsistent with supplied block class')
    terms = [top]
    restricted = [sum((poly_eval(top, v) ^ poly_eval(top, 0)) << i
                      for i, v in enumerate(radical))]
    points = points_degree_two(n)
    exact_probes = 0
    while len(terms) < k:
        null = kernel_basis(restricted, k)
        if not null:
            raise ValueError('UNKNOWN: translation restrictions lost rank')
        v = lin(radical, null[0])
        values = {x: 1 ^ int(query(x, x ^ v)) for x in points}
        exact_probes += len(points)
        q = interpolate_two(values, n)
        row = sum((poly_eval(q, w) ^ poly_eval(q, 0)) << i
                  for i, w in enumerate(radical))
        if not parity(row & null[0]) or independent(restricted+[row]) <= len(restricted):
            raise ValueError('UNKNOWN: new quadratic translation feature invalid')
        if any(parity(b & w) for b in polar_rows(q, n) for w in radical):
            raise ValueError('UNKNOWN: acquired feature violates common-radical promise')
        restricted.append(row)
        terms.append(q)
    matrix = transpose(restricted, k)
    duals = [lin(radical, c) for c in inverse(matrix)]
    zero = lin(duals, sum(poly_eval(q, 0) << i for i, q in enumerate(terms)))

    def priority(i, j):
        if i == j:
            return 0
        return -1 if query(zero ^ duals[j], zero ^ duals[i]) else 1

    high_to_low = sorted(range(k), key=functools.cmp_to_key(priority))
    low_to_high = list(reversed(high_to_low))
    terms = [terms[i] for i in low_to_high]
    duals = [duals[i] for i in low_to_high]
    transversal = complement(radical, n)

    def normalize(x):
        word = sum(poly_eval(q, x) << i for i, q in enumerate(terms))
        return x ^ lin(duals, word)

    def low_query(a, b):
        return query(normalize(lin(transversal, a)), normalize(lin(transversal, b)))

    low_decoder, low_offset, low_probes = acquire_comparator(r, low_query)
    compiled = CompiledDecoder(n, terms, duals, transversal, low_decoder, low_offset)
    evidence.update({'acquired_top_block_dimension': k, 'acquired_affine_quotient_dimension': r,
                     'exact_quadratic_translation_probes': exact_probes,
                     'affine_quotient_row_probes': low_probes,
                     'quadratic_feature_count': len(terms),
                     'comparison_access_only': True})
    return compiled, evidence


def run(n, r, seed):
    total = time.perf_counter()
    teacher = BlockShearTeacher(n, r, seed)
    setup = time.perf_counter()-total
    rng = random.Random(seed+1000000)
    start = time.perf_counter()
    compiled, evidence = acquire_block(n, teacher.query, rng)
    acquisition_seconds = time.perf_counter()-start
    queries = teacher.queries
    source_evaluations = teacher.source_evaluations
    source_cache_entries = len(teacher.cache)
    validation_start = time.perf_counter()
    # Read truth only now, after the learner has fully compiled.
    body_points = points_degree_two(n)
    true_bodies = [interpolate_two({x: (teacher.rank(x) >> j) & 1 for x in body_points}, n)
                   for j in range(n)]
    compiled_bodies = [interpolate_two({x: (compiled.rank(x) >> j) & 1 for x in body_points}, n)
                       for j in range(n)]
    assert true_bodies == compiled_bodies
    tested = list(range(1 << n)) if n <= 12 else [rng.getrandbits(n) for _ in range(4096)]
    for x in tested:
        assert compiled.rank(x) == teacher.rank(x)
    exact_fiber = None
    if n <= 12:
        exact_fiber = []
        for bits in range(min(compiled.n-compiled.r, 5)+1):
            prefix = (1 << bits)-1
            counts = Counter()
            for x in range(1 << n):
                z = x
                for i in range(bits):
                    j = len(compiled.top_terms)-1-i
                    wanted = (prefix >> (bits-1-i)) & 1
                    if poly_eval(compiled.top_terms[j], z) != wanted:
                        z ^= compiled.duals[j]
                assert compiled.rank(z) >> (n-bits) == prefix
                counts[z] += 1
            assert len(counts) == 1 << (n-bits) and set(counts.values()) == {1 << bits}
            exact_fiber.append({'bits': bits, 'fiber_size': len(counts), 'seed_preimages': 1 << bits})
    else:
        for bits in (1, (n-r)//2, n-r):
            prefix = rng.getrandbits(bits)
            for _ in range(256):
                x = compiled.sample_prefix(bits, prefix, rng)
                assert compiled.rank(x) >> (n-bits) == prefix
    assert teacher.queries == queries
    validation_seconds = time.perf_counter()-validation_start
    # Explicit arithmetic counters; dictionary/allocator costs not included.
    monomials = sum(len(q) for q in teacher._shears)
    evidence.update({'n': n, 'residual_dimension': r, 'top_block_dimension': n-r, 'seed': seed,
        'total_one_bit_comparisons': queries, 'transmitted_input_bits': 2*n*queries,
        'source_unique_rank_evaluations_acquisition': source_evaluations,
        'source_cache_logical_payload_bits': 2*n*source_cache_entries,
        'source_rank_bitwork_conservative_upper': source_evaluations*(n*n+n+n*monomials),
        'source_setup_seconds': setup, 'acquisition_seconds_including_source': acquisition_seconds,
        'validation_seconds': validation_seconds, 'overall_seconds': time.perf_counter()-total,
        'all_n_coordinate_polynomials_match_exactly': True, 'validated_points': len(tested),
        'source_queries_during_compiled_execution': 0, 'exhaustive_prefix_distribution': exact_fiber,
        'initial_feature_failure_bound': evidence['median_failure_bound']+evidence['coefficient_failure_union_bound'],
        'compact_top_coefficient_bits_upper': (n-r)*len(points_degree_two(n)),
        'closest_composition_status': 'Known algebra/correction/affine mechanisms; tailored prior and comparative advantage UNKNOWN.',
        'scope': 'Supplied hidden-affine block shear with nondegenerate top polar form; not arbitrary quadratic permutations.'})
    return evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(HERE/'BLOCK_SHEAR_RESULTS.json'))
    args = parser.parse_args()
    cases = [(8, 4, 610041), (12, 4, 610042), (16, 6, 610043),
             (24, 8, 610044), (32, 12, 610045)]
    results = []
    for case in cases:
        result = run(*case)
        results.append(result)
        print(json.dumps({key: result[key] for key in ['n', 'residual_dimension',
            'total_one_bit_comparisons', 'all_n_coordinate_polynomials_match_exactly',
            'acquisition_seconds_including_source']}), flush=True)
    Path(args.output).write_text(json.dumps({'cases': results, 'source_copies': receipts,
        'mission_status': 'NOT_ACHIEVED', 'novelty': 'UNKNOWN',
        'status': 'RESTRICTED_CLASS_COMPARATOR_ONLY_FULL_DECODER_CONSTRUCTION'}, indent=2)+'\n')


if __name__ == '__main__':
    main()
