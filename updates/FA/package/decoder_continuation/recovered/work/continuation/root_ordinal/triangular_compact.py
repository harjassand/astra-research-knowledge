"""Compact comparison-only triangular acquisition, expected D+6*binom(n,2).

D=sum_{h=0}^2 binom(n,h+1). Interpolate on the acquired-prefix complement,
not the whole raw cube. The source class and exact comparison access are supplied.
"""
import argparse
import json
import math
import random
import time
from pathlib import Path
from triangular_tournament import matching_cap
from triangular_translation import signature
from ordinal_flag_snapshot import (TriangularTeacher, Quadratic, coefficient_points,
                                   combine, interpolate, kernel)
from encoded_operations import inverse

HERE = Path(__file__).resolve().parent


class CompactDecoder:
    def __init__(self, basis, prefix_functions):
        self.n = len(basis)
        self.basis = basis
        self.coordinates = inverse(basis)
        self.prefix_functions = prefix_functions

    def rank(self, x):
        t = combine(self.coordinates, x)
        value = 0
        for j, h in enumerate(self.prefix_functions):
            value = (value << 1) | (((t >> j) & 1) ^ h(t & ((1 << j)-1)))
        return value

    def inverse_rank(self, target):
        t = 0
        for j, h in enumerate(self.prefix_functions):
            bit = (target >> (self.n-j-1)) & 1
            t |= (bit ^ h(t)) << j
        return combine(self.basis, t)

    def sample_prefix(self, bits, target, rng):
        t = rng.getrandbits(self.n-bits) << bits
        for j in range(bits):
            bit = (target >> (bits-j-1)) & 1
            h = self.prefix_functions[j](t & ((1 << j)-1))
            t |= (bit ^ h) << j
        return combine(self.basis, t)


def acquire(n, query, rng, beta=.01):
    pairs = n*(n-1)//2
    cap = matching_cap(pairs, beta)
    subspace = [1 << i for i in range(n)]
    basis, functions, stages = [], [], []
    interpolation_calls = response_calls = probe_calls = priority_calls = draws = 0
    for k in range(n):
        assert len(subspace) == n-k
        winner = subspace[0]
        trials = []
        for v in subspace[1:]:
            for attempt in range(cap):
                x = rng.getrandbits(n)
                draws += 1
                a = 1 ^ int(query(x, x ^ v))
                b = 1 ^ int(query(x, x ^ winner))
                probe_calls += 2
                if a == b:
                    break
            else:
                return None, {'status': 'UNKNOWN_MATCH_CAP', 'stage': k}
            if bool(query(x ^ v, x ^ winner)) == bool(a):
                winner = v
            priority_calls += 1
            trials.append(attempt+1)
        values = {}
        for a in coefficient_points(k):
            x = combine(basis, a)
            values[a] = 1 ^ int(query(x, x ^ winner))
        interpolation_calls += len(values)
        h = interpolate(values, k)
        constant = values[0]
        row = 0
        for i, v in enumerate(subspace):
            if v == winner:
                bit = 1
            else:
                bit = constant ^ (1 ^ int(query(v, v ^ winner)))
                response_calls += 1
            row |= bit << i
        assert row
        next_subspace = [combine(subspace, a) for a in kernel([row], len(subspace))]
        functions.append(h)
        basis.append(winner)
        subspace = next_subspace
        stages.append({'stage': k, 'prefix_variable_count': k,
                       'prefix_interpolation_queries': len(values),
                       'linear_response_queries': n-k-1,
                       'match_attempts_per_pair': trials})
    assert not subspace
    decoder = CompactDecoder(basis, functions)
    dimension = sum(math.comb(n, h+1) for h in range(min(2, n-1)+1))
    assert interpolation_calls == dimension and response_calls == pairs
    return decoder, {'status': 'EXACT_ON_COMPLETION_UNDER_SUPPLIED_CLASS',
        'stages': stages, 'prefix_interpolation_comparisons': interpolation_calls,
        'linear_response_comparisons': response_calls,
        'matching_probe_comparisons': probe_calls, 'priority_comparisons': priority_calls,
        'random_input_draws': draws, 'random_input_bits': n*draws,
        'cap_per_pair': cap, 'unknown_probability_upper_bound': pairs*2.0**(-cap),
        'semantic_error_probability_on_completion_under_promise': 0,
        'known_basis_exact_identification_information_lower_bound': dimension,
        'expected_comparison_upper_bound': dimension+6*pairs,
        'capped_comparison_upper_bound': dimension+(2*cap+2)*pairs,
        'compact_polynomial_coefficient_bits': dimension,
        'basis_bits': n*n,
        'inverse_basis_optional_cache_bits': n*n}


def run(n, seed):
    total = time.perf_counter()
    teacher = TriangularTeacher(n, seed)
    setup = time.perf_counter()-total
    begin = time.perf_counter()
    decoder, evidence = acquire(n, teacher.query, random.Random(seed+4000000))
    seconds = time.perf_counter()-begin
    if decoder is None:
        return {'n': n, 'seed': seed, **evidence}
    calls, ranks, cache = teacher.calls, teacher.fresh_ranks, len(teacher.cache)
    assert calls == sum(evidence[k] for k in ('prefix_interpolation_comparisons',
        'linear_response_comparisons', 'matching_probe_comparisons', 'priority_comparisons'))
    assert calls <= evidence['capped_comparison_upper_bound']
    begin = time.perf_counter()
    # Ground truth only after learner termination. Both complete bodies are
    # interpolated in raw coordinates for comparison, without learner labels.
    points = coefficient_points(n)
    actual_values = {x: teacher.rank(x) for x in points}
    learned_values = {x: decoder.rank(x) for x in points}
    actual = [interpolate({x: (actual_values[x] >> j) & 1 for x in points}, n)
              for j in range(n)]
    learned = [interpolate({x: (learned_values[x] >> j) & 1 for x in points}, n)
               for j in range(n)]
    assert [signature(q) for q in actual] == [signature(q) for q in learned]
    rng = random.Random(seed+5000000)
    inputs = range(1 << n) if n <= 12 else [rng.getrandbits(n) for _ in range(4096)]
    checked = 0
    for x in inputs:
        r = decoder.rank(x)
        assert r == teacher.rank(x) and decoder.inverse_rank(r) == x
        checked += 1
    for bits in (0, 1, n//2, n-1, n):
        target = rng.getrandbits(bits)
        for _ in range(128):
            x = decoder.sample_prefix(bits, target, rng)
            assert decoder.rank(x) >> (n-bits) == target
    assert teacher.calls == calls
    validation_seconds = time.perf_counter()-begin
    path = HERE/f'acquired_compact_n{n}_seed{seed}.json'
    path.write_text(json.dumps({'n': n,
        'basis_columns': decoder.basis,
        'prefix_polynomials_high_to_low': [h.body() for h in decoder.prefix_functions],
        'promise': 'hidden affine triangular quadratic order; exact comparisons',
        'source': 'learned comparison answers only'}, indent=2)+'\n')
    evidence.update({'n': n, 'seed': seed, 'one_bit_comparisons': calls,
        'query_input_transmission_bits': 2*n*calls,
        'source_unique_rank_evaluations_acquisition': ranks,
        'source_cache_logical_payload_bits': 2*n*cache,
        'source_rank_elementary_bitwork_conservative_upper': ranks*(8*n**3+8*n**2),
        'source_setup_seconds': setup, 'acquisition_seconds_including_source': seconds,
        'post_acquisition_ground_truth_validation_seconds': validation_seconds,
        'all_raw_coordinate_polynomials_exact': True,
        'rank_and_inverse_validation_points': checked,
        'source_queries_during_compiled_execution': 0,
        'prefix_sampler_random_bits_per_sample': 'n-prefix_length',
        'acquired_model_path': str(path),
        'novelty': 'UNKNOWN', 'practical_advantage_over_tailored_prior': 'UNKNOWN'})
    return evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--output', default=str(HERE/'TRIANGULAR_COMPACT_RESULTS.json'))
    args = parser.parse_args()
    cases = [(8, 610063), (12, 610065), (16, 610066),
             (24, 610067), (32, 610068), (64, 610069)]
    if args.quick:
        cases = cases[:2]
    results = []
    for case in cases:
        result = run(*case)
        results.append(result)
        print(json.dumps({k: result.get(k) for k in ('n', 'one_bit_comparisons',
            'all_raw_coordinate_polynomials_exact', 'acquisition_seconds_including_source')}), flush=True)
    Path(args.output).write_text(json.dumps({'cases': results,
        'mission_status': 'NOT_ACHIEVED',
        'scope': 'Complete hidden affine triangular quadratic class; expected leading query coefficient matches known-basis counting lower bound. No class recognition, noisy access, priority clearance or external validation.'}, indent=2)+'\n')


if __name__ == '__main__':
    main()
