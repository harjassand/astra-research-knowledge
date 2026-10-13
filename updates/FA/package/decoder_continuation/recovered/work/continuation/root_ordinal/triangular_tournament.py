"""Faster exact comparison-only triangular decoder acquisition.

Expected comparisons <= n*M + 5*n*(n-1)/2, M=1+n+binom(n,2).
The only randomized failure is an explicit UNKNOWN at the matching-probe cap.
Every completed result is exact under the supplied complete triangular promise.
"""
import argparse
import json
import math
import random
import time
from pathlib import Path
from triangular_translation import Decoder, signature, outside_class_counterexample
from ordinal_flag_snapshot import (TriangularTeacher, coefficient_points, combine,
                                   interpolate, kernel, parity)

HERE = Path(__file__).resolve().parent


def matching_cap(pairs, beta):
    """Exact integer choice for the supplied binary-rational float beta."""
    if not 0 < beta < 1:
        raise ValueError('beta must lie strictly between zero and one')
    numerator, denominator = beta.as_integer_ratio()
    target = pairs*denominator
    cap = max(0, target.bit_length()-numerator.bit_length())
    while (numerator << cap) < target:
        cap += 1
    while cap and (numerator << (cap-1)) >= target:
        cap -= 1
    return cap


def acquire(n, query, rng, beta=.01):
    points = coefficient_points(n)
    pairs = n*(n-1)//2
    cap = matching_cap(pairs, beta)
    subspace = [1 << j for j in range(n)]
    quadratics, toggles, stages = [], [], []
    probe_calls = priority_calls = interpolation_calls = draws = 0
    for stage in range(n):
        assert len(subspace) == n-stage
        winner = subspace[0]
        stage_trials = []
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
                return None, {'status': 'UNKNOWN_MATCH_CAP', 'stage': stage,
                    'cap_per_pair': cap, 'random_draws': draws,
                    'comparisons_so_far': probe_calls+priority_calls+interpolation_calls}
            response = bool(query(x ^ v, x ^ winner))
            priority_calls += 1
            if response == bool(a):
                winner = v
            stage_trials.append(attempt+1)
        values = {x: 1 ^ int(query(x, x ^ winner)) for x in points}
        interpolation_calls += len(points)
        q = interpolate(values, n)
        response_row = sum((q(v) ^ q.constant) << j for j, v in enumerate(subspace))
        if not response_row or (q(winner) ^ q.constant) != 1:
            return None, {'status': 'UNKNOWN_CLASS_CONSISTENCY', 'stage': stage}
        # Complete triangular promise makes this restriction a linear functional.
        subspace = [combine(subspace, coordinates)
                    for coordinates in kernel([response_row], len(subspace))]
        quadratics.append(q)
        toggles.append(winner)
        stages.append({'stage': stage, 'match_attempts_per_pair': stage_trials})
    certificate = all(
        all(parity(row & v) == 0 for row in q.polar()) and
        (q(v) ^ q.constant) == int(i == j)
        for j, v in enumerate(toggles) for i, q in enumerate(quadratics[:j+1]))
    if not certificate:
        return None, {'status': 'UNKNOWN_FLAG_CHECK'}
    return Decoder(n, quadratics, toggles), {
        'status': 'EXACT_ON_COMPLETION_UNDER_SUPPLIED_CLASS',
        'stages': stages, 'interpolation_comparisons': interpolation_calls,
        'match_probe_comparisons': probe_calls, 'priority_comparisons': priority_calls,
        'random_input_draws': draws, 'random_input_bits': n*draws,
        'tournament_pair_count': priority_calls, 'cap_per_pair': cap,
        'expected_comparison_upper_bound': n*len(points)+5*pairs,
        'bounded_comparison_upper_bound': n*len(points)+(2*cap+1)*pairs,
        'unknown_probability_upper_bound': pairs*2.0**(-cap),
        'semantic_error_probability_on_completion_under_promise': 0,
        'polar_toggle_flag_certificate': certificate,
        'known_basis_subclass_decision_tree_query_lower_bound':
            sum(math.comb(n, j+1) for j in range(min(2, n-1)+1)),
    }


def run(n, seed):
    total = time.perf_counter()
    teacher = TriangularTeacher(n, seed)
    setup = time.perf_counter()-total
    begin = time.perf_counter()
    decoder, evidence = acquire(n, teacher.query, random.Random(seed+4000000))
    acquisition_seconds = time.perf_counter()-begin
    if decoder is None:
        return {'n': n, 'seed': seed, **evidence, 'one_bit_comparisons': teacher.calls}
    calls, ranks, cache_size = teacher.calls, teacher.fresh_ranks, len(teacher.cache)
    assert calls == sum(evidence[key] for key in ('interpolation_comparisons',
            'match_probe_comparisons', 'priority_comparisons'))
    assert calls <= evidence['bounded_comparison_upper_bound']
    begin = time.perf_counter()
    points = coefficient_points(n)
    # Ground truth is isolated from the learner and read only after its return.
    truth = [interpolate({x: (teacher.rank(x) >> (n-1-j)) & 1 for x in points}, n)
             for j in range(n)]
    assert [signature(q) for q in decoder.quadratics] == [signature(q) for q in truth]
    rng = random.Random(seed+5000000)
    inputs = range(1 << n) if n <= 12 else [rng.getrandbits(n) for _ in range(4096)]
    checked = 0
    for x in inputs:
        r = decoder.rank(x)
        assert r == teacher.rank(x)
        assert decoder.inverse_rank(r) == x
        checked += 1
    for bits in (0, 1, n//2, n-1, n):
        target = rng.getrandbits(bits)
        for _ in range(128):
            x = decoder.sample_prefix(bits, target, rng)
            assert decoder.rank(x) >> (n-bits) == target
    assert teacher.calls == calls
    validation_seconds = time.perf_counter()-begin
    model = {'n': n, 'source': 'acquired scalar-comparison transcript only',
             'promise': 'complete hidden affine triangular quadratic order',
             'quadratics_high_to_low': [q.body() for q in decoder.quadratics],
             'prefix_toggles': decoder.toggles,
             'inductive_algebraic_flag_certificate': evidence['polar_toggle_flag_certificate']}
    model_path = HERE/f'acquired_tournament_n{n}_seed{seed}.json'
    model_path.write_text(json.dumps(model, indent=2)+'\n')
    evidence.update({'n': n, 'seed': seed, 'one_bit_comparisons': calls,
        'query_input_transmission_bits': 2*n*calls,
        'source_unique_rank_evaluations_acquisition': ranks,
        'source_cache_logical_payload_bits': 2*n*cache_size,
        'source_uncached_rank_bitwork_conservative_upper': ranks*(8*n**3+8*n**2),
        'source_setup_seconds': setup, 'acquisition_seconds_including_source': acquisition_seconds,
        'ground_truth_and_execution_validation_seconds': validation_seconds,
        'all_coordinate_polynomials_exact': True,
        'rank_and_inverse_validation_points': checked,
        'source_queries_during_compiled_execution': 0,
        'compact_acquired_polynomial_coefficient_bits': n*len(points),
        'acquired_toggle_bits': n*n, 'acquired_model_path': str(model_path),
        'accounting_scope': 'Dense bitwork bound, logical cache payload only; Python allocator/lookup overhead not profiled. Setup, acquisition and checking separated.',
        'novelty': 'UNKNOWN', 'advantage_over_strongest_tailored_prior': 'UNKNOWN'})
    return evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(HERE/'TRIANGULAR_TOURNAMENT_RESULTS.json'))
    parser.add_argument('--quick', action='store_true',
                        help='Bounded replay of n=8 and n=12; full receipt includes n=64.')
    args = parser.parse_args()
    cases = [(4, 610061), (6, 610062), (8, 610063), (10, 610064),
             (12, 610065), (16, 610066), (24, 610067), (32, 610068), (64, 610069)]
    if args.quick:
        cases = [case for case in cases if case[0] in (8, 12)]
    results = []
    for case in cases:
        result = run(*case)
        results.append(result)
        print(json.dumps({key: result.get(key) for key in ('n', 'status',
            'one_bit_comparisons', 'all_coordinate_polynomials_exact',
            'acquisition_seconds_including_source')}), flush=True)
    Path(args.output).write_text(json.dumps({'cases': results,
        'mission_status': 'NOT_ACHIEVED', 'novelty': 'UNKNOWN',
        'outside_class_counterexample': outside_class_counterexample(),
        'scope': 'Exact completion under supplied complete triangular class; randomized resource cap can return UNKNOWN. Not arbitrary quadratic bijections or partial flags.'}, indent=2)+'\n')


if __name__ == '__main__':
    main()
