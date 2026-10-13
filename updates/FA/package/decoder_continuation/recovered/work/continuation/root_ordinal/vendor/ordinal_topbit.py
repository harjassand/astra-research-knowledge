"""Bounded nonlinear ordinal-to-executable-feature checkpoint.

Known degree-two top bit of an unknown bijective decoder, scalar comparisons only.
Near-median anchor + standard Reed-Muller self-correction, with all calls charged.
No novelty or advantage over the identical known-method composition is asserted.
"""
import argparse
import json
import math
import random
import time
from pathlib import Path
from encoded_operations import lin, random_invertible, parity, kernel_basis


class QuadraticOrderTeacher:
    """A nonlinear bijection: hidden affine map, then a top-bit quadratic shear.

    Memoization belongs to the synthetic source and is counted explicitly.  The
    learner sees only query(x,y); rank values and coefficients stay evaluator-only.
    """
    def __init__(self, n, seed):
        rng = random.Random(seed)
        _, self._decoder = random_invertible(rng, n)
        self._offset = rng.getrandbits(n)
        self._quadratic = [rng.getrandbits(n-1) & ~((1 << (i+1))-1)
                           for i in range(n-1)]
        self.n, self.queries, self.unique_rank_evaluations = n, 0, 0
        self._cache = {}

    def rank(self, x):
        if x not in self._cache:
            self.unique_rank_evaluations += 1
            u = lin(self._decoder, x) ^ self._offset
            q = 0
            for i, row in enumerate(self._quadratic):
                if (u >> i) & 1:
                    q ^= parity(row & u)
            self._cache[x] = u ^ (q << (self.n-1))
        return self._cache[x]

    def query(self, x, y):
        self.queries += 1
        return self.rank(x) < self.rank(y)


def merge_sort(values, query):
    if len(values) <= 1:
        return list(values)
    mid = len(values)//2
    left, right = merge_sort(values[:mid], query), merge_sort(values[mid:], query)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if query(left[i], right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out+left[i:]+right[j:]


def points_degree_two(n):
    return [0]+[1 << i for i in range(n)]+[
        (1 << i) | (1 << j) for i in range(n) for j in range(i+1, n)]


def interpolate_two(values, n):
    terms = {}
    constant = values[0]
    if constant:
        terms[0] = 1
    for i in range(n):
        if values[1 << i] ^ constant:
            terms[1 << i] = 1
    for i in range(n):
        for j in range(i+1, n):
            key = (1 << i) | (1 << j)
            if values[key] ^ values[1 << i] ^ values[1 << j] ^ constant:
                terms[key] = 1
    return sorted(terms)


def poly_eval(terms, x):
    return sum((x & term) == term for term in terms) & 1


def single_fiber_sampler_check(terms, n, rng):
    """Compile a toggle for one balanced quadratic's fiber, not joint fibers.

    B(v,x)=q(v+x)+q(v)+q(x)+q(0) is the polar form.  A radical vector
    with q(v)+q(0)=1 toggles q everywhere.  Balanced quadratics have one.
    This is ordinary quadratic-form algebra; no novelty claim is made.
    """
    start = time.perf_counter()
    polar_rows = [0]*n
    for term in terms:
        if term.bit_count() == 2:
            first = term & -term
            other = term ^ first
            i, j = first.bit_length()-1, other.bit_length()-1
            polar_rows[i] ^= other
            polar_rows[j] ^= first
    radical = kernel_basis(polar_rows, n)
    constant = poly_eval(terms, 0)
    toggle = next((v for v in radical if poly_eval(terms, v) ^ constant), None)
    preparation_seconds = time.perf_counter()-start
    if toggle is None:
        return {'single_fiber_toggle_found': False,
                'single_fiber_preparation_seconds': preparation_seconds}
    # These two algebraic equalities certify q(x+v)=q(x)+1 for all x.
    algebraic = all(parity(row & toggle) == 0 for row in polar_rows)
    algebraic &= bool(poly_eval(terms, toggle) ^ constant)
    checked = 0
    distribution_exact = None
    if n <= 12:
        counts = [{}, {}]
        for x in range(1 << n):
            value = poly_eval(terms, x)
            for bit in (0, 1):
                z = x if value == bit else x ^ toggle
                assert poly_eval(terms, z) == bit
                counts[bit][z] = counts[bit].get(z, 0)+1
                checked += 1
        distribution_exact = all(
            len(count) == 1 << (n-1) and set(count.values()) == {2}
            for count in counts)
        assert distribution_exact
    else:
        for _ in range(4096):
            x = rng.getrandbits(n)
            assert poly_eval(terms, x ^ toggle) == (poly_eval(terms, x) ^ 1)
            checked += 1
    assert algebraic
    return {'single_fiber_toggle_found': True,
            'single_fiber_toggle': toggle,
            'single_fiber_toggle_algebraically_verified': algebraic,
            'single_fiber_exhaustive_distribution_verified': distribution_exact,
            'single_fiber_checked_points': checked,
            'single_fiber_preparation_seconds': preparation_seconds,
            'single_fiber_total_check_seconds': time.perf_counter()-start,
            'single_fiber_extra_source_queries': 0}


def self_correct(point, threshold, n, repetitions, rng):
    votes = 0
    for _ in range(repetitions):
        a, b, c = (rng.getrandbits(n) for _ in range(3))
        value = 0
        for shift in (a, b, a ^ b, c, a ^ c, b ^ c, a ^ b ^ c):
            value ^= int(threshold(point ^ shift))
        votes += value
    return int(votes > repetitions//2)


def acquire_topbit(n, query, rng, beta=0.01, epsilon=1/32, sample_count=4095):
    if n < 8 or epsilon <= 2**(-n):
        raise ValueError('This bounded confidence calculation uses n>=8.')
    points = points_degree_two(n)
    gap = 0.5-7*epsilon
    repetitions = math.ceil(math.log(2*len(points)/beta)/(2*gap*gap))
    if repetitions % 2 == 0:
        repetitions += 1
    samples = [rng.getrandbits(n) for _ in range(sample_count)]
    ordered = merge_sort(samples, query)
    anchor = ordered[sample_count//2]
    threshold = lambda x: query(x, anchor)
    # Direct threshold interpolation is only a diagnostic, not a strong comparator.
    direct_values = {x: int(threshold(x)) ^ 1 for x in points}
    corrected_values = {x: self_correct(x, threshold, n, repetitions, rng) ^ 1
                        for x in points}
    return interpolate_two(corrected_values, n), interpolate_two(direct_values, n), {
        'sample_count': sample_count, 'anchor': anchor, 'epsilon': epsilon,
        'beta_target': beta, 'coefficient_points': len(points),
        'self_correction_repetitions': repetitions,
        'median_failure_bound': 2*math.exp(-2*sample_count*(epsilon-2**(-n))**2),
        'coefficient_failure_union_bound': len(points)*math.exp(-2*repetitions*gap*gap),
        'comparison_upper_bound_including_diagnostic':
            sample_count*math.ceil(math.log2(sample_count)) +
            len(points)*(7*repetitions+1),
    }


def run(n, seed):
    total_start = time.perf_counter()
    teacher = QuadraticOrderTeacher(n, seed)
    source_preparation_seconds = time.perf_counter()-total_start
    rng = random.Random(seed+900000)
    start = time.perf_counter()
    terms, direct_terms, evidence = acquire_topbit(n, teacher.query, rng)
    seconds = time.perf_counter()-start
    acquisition_queries = teacher.queries
    source_evaluations = teacher.unique_rank_evaluations
    source_cache_entries = len(teacher._cache)
    validation_start = time.perf_counter()
    # Evaluator-only ground truth, read AFTER the learner returns.
    truth_values = {x: (teacher.rank(x) >> (n-1)) & 1 for x in points_degree_two(n)}
    truth_terms = interpolate_two(truth_values, n)
    exact_body = terms == truth_terms
    direct_exact = direct_terms == truth_terms
    heldout = range(1 << n) if n <= 12 else [rng.getrandbits(n) for _ in range(4096)]
    errors = direct_errors = tested = 0
    for x in heldout:
        actual = (teacher.rank(x) >> (n-1)) & 1
        errors += poly_eval(terms, x) != actual
        direct_errors += poly_eval(direct_terms, x) != actual
        tested += 1
    validation_seconds = time.perf_counter()-validation_start
    evidence.update({
        'n': n, 'seed': seed, 'acquisition_seconds_including_source': seconds,
        'source_preparation_seconds': source_preparation_seconds,
        'validation_seconds_including_source': validation_seconds,
        'acquisition_comparisons': acquisition_queries,
        'acquisition_returned_bits': acquisition_queries,
        'acquisition_query_input_bits': acquisition_queries*2*n,
        'source_unique_rank_evaluations': source_evaluations,
        'source_rank_bitwork_upper': source_evaluations*(3*n*n+n),
        'source_cache_entries_during_acquisition': source_cache_entries,
        'source_cache_payload_bits_upper': source_cache_entries*2*n,
        'exact_polynomial_body_matches_truth': exact_body,
        'direct_interpolation_exact_diagnostic': direct_exact,
        'heldout_points': tested, 'corrected_heldout_errors': errors,
        'direct_heldout_errors_diagnostic': direct_errors,
        'source_queries_during_learned_execution': teacher.queries-acquisition_queries,
        'anchor_rank_evaluator_only': teacher.rank(evidence['anchor']),
        'anchor_hamming_error_fraction_evaluator_only':
            abs(teacher.rank(evidence['anchor'])-(1 << (n-1)))/(1 << n),
        'acquired_anf_monomial_masks': terms,
        'acquired_body_coefficient_bits_upper': 1+n+n*(n-1)//2,
        'actual_nonzero_monomial_mask_payload_bits_upper': n*len(terms),
        'known_method_boundary': 'quantile concentration and Reed-Muller self-correction are standard; no advantage over their identical same-interface composition is claimed',
    })
    evidence.update(single_fiber_sampler_check(terms, n, rng))
    evidence['overall_seconds_including_source_preparation_validation_and_fiber'] = (
        time.perf_counter()-total_start)
    assert acquisition_queries <= evidence['comparison_upper_bound_including_diagnostic']
    assert evidence['median_failure_bound'] + evidence['coefficient_failure_union_bound'] <= 0.01
    return evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='ordinal_topbit_evidence.json')
    args = parser.parse_args()
    cases = []
    for n, seed in [(8,610031),(12,610032),(16,610031),(16,610032),(32,610033)]:
        result = run(n, seed)
        cases.append(result)
        print(json.dumps({k: v for k, v in result.items() if k != 'acquired_anf_monomial_masks'}), flush=True)
    Path(args.output).write_text(json.dumps({
        'status': 'bounded_exact_nonlinear_feature_checkpoint_prior_art_not_cleared',
        'cases': cases,
        'interface': 'Only one-bit comparisons under a hidden quadratic bijective decoder. No target ranks, bits or intermediate traces given to learner.',
        'boundary': 'Only top bit is acquired here. One known balanced quadratic fiber has an exact compiled toggle sampler. Full decoder/order recovery and efficient joint deep-fiber acquisition/sampling are not solved.'
    }, indent=2)+'\n')


if __name__ == '__main__':
    main()
