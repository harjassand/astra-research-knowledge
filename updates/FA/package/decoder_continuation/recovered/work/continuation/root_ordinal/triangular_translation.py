"""Exact comparison-only acquisition of hidden triangular quadratic order.

Supplied promise: in hidden affine input coordinates u, the most-to-least
significant bits are q_j=u_j+g_j(u_0,...,u_{j-1}), deg(g_j)<=2.
This is equivalent to a complete independent quadratic polar-toggle flag.
No ranks, labels, target code, input transform, toggles or fibers are supplied.
The comparator is queried only on chosen pairs and returns a single bit.
"""
import argparse
import hashlib
import json
import random
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'sol03_learning/ordinal_flag.py'
VENDOR = HERE/'vendor'
VENDOR.mkdir(exist_ok=True)
SNAPSHOT = VENDOR/'ordinal_flag_snapshot.py'
if not SNAPSHOT.exists():
    shutil.copy2(SOURCE, SNAPSHOT)
sys.path.insert(0, str(VENDOR))
from ordinal_flag_snapshot import (Quadratic, TriangularTeacher, coefficient_points,
    combine, interpolate, kernel, parity)


def signature(q):
    return (q.constant, q.linear, tuple(q.upper))


def xor_polynomial(a, b):
    return Quadratic(a.constant ^ b.constant, a.linear ^ b.linear,
                     [x ^ y for x, y in zip(a.upper, b.upper)])


def preserving_subspace(quadratics, n):
    radical = kernel([row for q in quadratics for row in q.polar()], n)
    rows = [sum((q(v) ^ q.constant) << i for i, v in enumerate(radical))
            for q in quadratics]
    return [combine(radical, w) for w in kernel(rows, len(radical))]


def equal_value_point(a, b, n):
    """a+b is a balanced quadratic because a,b are distinct actual rank bits."""
    difference = xor_polynomial(a, b)
    if difference.constant == 0:
        return 0
    radical = kernel(difference.polar(), n)
    point = next((v for v in radical if difference(v) ^ difference.constant), None)
    if point is None:
        raise ValueError('UNKNOWN: candidates fail the balanced quadratic criterion')
    assert a(point) == b(point)
    return point


class Decoder:
    def __init__(self, n, quadratics, toggles):
        self.n, self.quadratics, self.toggles = n, quadratics, toggles

    def rank(self, x):
        word = 0
        for q in self.quadratics:
            word = (word << 1) | q(x)
        return word

    def project_prefix(self, x, bits, target):
        for j in range(bits):
            desired = (target >> (bits-j-1)) & 1
            if self.quadratics[j](x) != desired:
                x ^= self.toggles[j]
        return x

    def inverse_rank(self, target):
        return self.project_prefix(0, self.n, target)

    def sample_prefix(self, bits, target, rng):
        return self.project_prefix(rng.getrandbits(self.n), bits, target)


def acquire(n, query):
    points = coefficient_points(n)
    quadratics, toggles, stages = [], [], []
    candidate_cache = {}
    comparison_count, priority_comparisons = 0, 0
    for j in range(n):
        subspace = preserving_subspace(quadratics, n)
        if len(subspace) != n-j:
            raise ValueError('UNKNOWN: preservation dimension violates complete triangular promise')
        best = None
        distinct = set()
        fresh = 0
        for v in subspace:
            if v not in candidate_cache:
                values = {x: 1 ^ int(query(x, x ^ v)) for x in points}
                comparison_count += len(points)
                candidate_cache[v] = interpolate(values, n)
                fresh += 1
            q = candidate_cache[v]
            key = signature(q)
            if key in distinct:
                continue
            distinct.add(key)
            if any(parity(row & v) for row in q.polar()) or (q(v) ^ q.constant) != 1:
                raise ValueError('UNKNOWN: extracted bit fails its translation certificate')
            if best is None:
                best = (q, v)
                continue
            b, w = best
            point = equal_value_point(q, b, n)
            response = bool(query(point ^ v, point ^ w))
            priority_comparisons += 1
            # q is earlier iff it flips a shared bit value a to 1-a first.
            if response == bool(q(point)):
                best = (q, v)
        if best is None:
            raise ValueError('UNKNOWN: no next decoder coordinate')
        q, v = best
        for i, old in enumerate(quadratics):
            assert all(parity(row & v) == 0 for row in old.polar())
            assert (old(v) ^ old.constant) == 0
        quadratics.append(q)
        toggles.append(v)
        stages.append({'stage': j, 'preserving_dimension': len(subspace),
                       'distinct_candidate_bits': len(distinct), 'fresh_translation_bodies': fresh})
    assert not preserving_subspace(quadratics, n)
    result = Decoder(n, quadratics, toggles)
    certificate = all(
        all(parity(row & v) == 0 for row in q.polar()) and
        (q(v) ^ q.constant) == int(i == j)
        for j, v in enumerate(toggles) for i, q in enumerate(quadratics[:j+1]))
    assert certificate
    return result, {'stages': stages, 'translation_body_comparisons': comparison_count,
                    'priority_comparisons': priority_comparisons,
                    'cached_translation_bodies': len(candidate_cache),
                    'polar_toggle_flag_certificate': certificate,
                    'comparison_bound': len(points)*n*(n+1)//2+n*(n-1)//2,
                    'failure_probability_under_supplied_class': 0}


def full_sort_control(n, query):
    """Context only; full enumeration is not a strongest tailored-method claim."""
    from functools import cmp_to_key
    values = list(range(1 << n))
    values.sort(key=cmp_to_key(lambda a, b: -1 if query(a, b) else 1))
    return values


def run(n, seed, compare_sort=True):
    start = time.perf_counter()
    teacher = TriangularTeacher(n, seed)
    setup = time.perf_counter()-start
    begin = time.perf_counter()
    decoder, evidence = acquire(n, teacher.query)
    acquisition = time.perf_counter()-begin
    calls, ranks, cache_size = teacher.calls, teacher.fresh_ranks, len(teacher.cache)
    assert calls == evidence['translation_body_comparisons']+evidence['priority_comparisons']
    assert calls <= evidence['comparison_bound']
    begin = time.perf_counter()
    # Evaluator-only truth, read after the algorithm has returned.
    points = coefficient_points(n)
    true_bodies = [interpolate({x: (teacher.rank(x) >> (n-1-j)) & 1 for x in points}, n)
                   for j in range(n)]
    assert [signature(q) for q in decoder.quadratics] == [signature(q) for q in true_bodies]
    rng = random.Random(seed+900000)
    inputs = range(1 << n) if n <= 12 else [rng.getrandbits(n) for _ in range(4096)]
    checked = 0
    for x in inputs:
        y = decoder.rank(x)
        assert y == teacher.rank(x)
        assert decoder.inverse_rank(y) == x
        checked += 1
    exact_distributions = []
    if n <= 10:
        for bits in range(n+1):
            target = (1 << bits)-1
            counts = Counter(decoder.project_prefix(x, bits, target) for x in range(1 << n))
            assert len(counts) == 1 << (n-bits)
            assert set(counts.values()) == {1 << bits}
            assert all(decoder.rank(x) >> (n-bits) == target for x in counts)
            exact_distributions.append({'prefix_bits': bits, 'fiber_size': len(counts),
                                        'seed_preimages_each': 1 << bits})
    else:
        for bits in (1, n//2, n-1, n):
            target = rng.getrandbits(bits)
            for _ in range(256):
                x = decoder.sample_prefix(bits, target, rng)
                assert decoder.rank(x) >> (n-bits) == target
    fresh_values = [rng.getrandbits(n) for _ in range(128)]
    ordered = sorted(fresh_values, key=decoder.rank)
    assert [teacher.rank(x) for x in ordered] == sorted(teacher.rank(x) for x in fresh_values)
    assert teacher.calls == calls
    validation = time.perf_counter()-begin
    sort_control = None
    if compare_sort and n <= 12:
        control = TriangularTeacher(n, seed)
        begin = time.perf_counter()
        sorted_values = full_sort_control(n, control.query)
        wall = time.perf_counter()-begin
        assert [control.rank(x) for x in sorted_values] == list(range(1 << n))
        sort_control = {'comparisons': control.calls, 'wall_seconds': wall,
            'fresh_source_ranks': control.fresh_ranks,
            'scope': 'Exact full-domain sort context, not strongest tailored comparator.'}
    evidence.update({'n': n, 'seed': seed, 'one_bit_comparisons': calls,
        'input_transmission_bits': 2*n*calls, 'source_unique_ranks_acquisition': ranks,
        'source_cache_logical_payload_bits': 2*n*cache_size,
        'source_rank_bitwork_upper_without_object_overhead': ranks*(3*n*n+n),
        'source_setup_seconds': setup, 'acquisition_seconds_including_source': acquisition,
        'validation_seconds': validation, 'all_coordinate_polynomials_exact': True,
        'rank_and_inverse_validation_points': checked,
        'source_queries_during_execution': 0, 'all_prefix_sizes_exhaustive_seed_laws': exact_distributions,
        'full_domain_sort_context': sort_control, 'novelty': 'UNKNOWN',
        'tailored_prior_advantage': 'UNKNOWN',
        'scope': 'Supplied complete quadratic polar-toggle flag / hidden affine triangular order; exact chosen-input comparisons only.'})
    return evidence


def outside_class_counterexample():
    # q_top=x2+x0*x1, q_mid=x0, q_low=x1: a quadratic bijection with no complete flag.
    n = 3
    def rank(x):
        a, b, c = ((x >> i) & 1 for i in range(3))
        return ((c ^ (a & b)) << 2) | (a << 1) | b
    v = 1
    values = {x: 1 ^ int(rank(x) < rank(x ^ v)) for x in coefficient_points(n)}
    extracted = interpolate(values, n)
    actual = [interpolate({x: (rank(x) >> j) & 1 for x in coefficient_points(n)}, n)
              for j in range(n)]
    assert all(extracted(x) == (1 ^ int(rank(x) < rank(x ^ v))) for x in range(1 << n))
    assert all(signature(extracted) != signature(q) for q in actual)
    return {'n': n, 'translation': v, 'all_outputs_are_quadratic': True,
            'rank_is_bijective': len({rank(x) for x in range(1 << n)}) == 1 << n,
            'comparison_extracted_quadratic_not_an_actual_bit': extracted.body(),
            'scope': 'Polynomial interpolation and local translation checks alone cannot recognize the complete-flag promise.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(HERE/'TRIANGULAR_TRANSLATION_RESULTS.json'))
    args = parser.parse_args()
    cases = [(4, 610051), (6, 610052), (8, 610053), (10, 610054),
             (12, 610055), (16, 610056), (24, 610057), (32, 610058)]
    results = []
    for case in cases:
        result = run(*case)
        results.append(result)
        print(json.dumps({k: result[k] for k in ['n', 'one_bit_comparisons',
            'all_coordinate_polynomials_exact', 'acquisition_seconds_including_source']}), flush=True)
    Path(args.output).write_text(json.dumps({'status': 'EXACT_RESTRICTED_COMPARISON_ONLY_FULL_DECODER',
        'mission_status': 'NOT_ACHIEVED', 'cases': results,
        'outside_class_failure': outside_class_counterexample(),
        'source_snapshot': {'source': str(SOURCE), 'snapshot': str(SNAPSHOT),
                            'sha256': hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest()}}, indent=2)+'\n')


if __name__ == '__main__':
    main()
