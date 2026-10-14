"""Counted persistent-comparator experiment; truth becomes available after return.

The learner is passed only a callback, n,r,epsilon,beta and PRNG seed. Source
construction, planted bad membership, source ranks and coefficients are kept in
this separate harness. No claim of process isolation or physical acquisition.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'p_s01_partial_flag'))
from partial_flag import PartialTeacher, coefficient_points, interpolate, rank_from_model, linear
from robust_learner import acquire
import argparse
import json
import random
import resource
import time
import tracemalloc


class PersistentSource:
    def __init__(self, n, r, seed, bad_count, mode):
        started = time.perf_counter()
        self.ideal = PartialTeacher(n, r, seed)
        self.n, self.r, self.mode = n, r, mode
        self.bad = set(random.Random(seed + 700000).sample(range(1 << n), bad_count))
        self.calls = 0
        self.setup_seconds = time.perf_counter() - started

    def query(self, x, y):
        self.calls += 1
        if x == y:
            return 0
        incident = x in self.bad or y in self.bad
        if self.mode == 'bad_first_total_order':
            return int((int(x not in self.bad), self.ideal.rank(x)) <
                       (int(y not in self.bad), self.ideal.rank(y)))
        ideal = int(self.ideal.rank(x) < self.ideal.rank(y))
        if self.mode == 'flip_incident':
            return ideal ^ int(incident)
        if self.mode == 'asymmetric_hash' and incident:
            return (((x + 3) * (y + 5)).bit_count()) & 1
        if self.mode == 'ideal':
            return ideal
        if self.mode not in ('asymmetric_hash',):
            raise ValueError('unknown fault mode')
        return ideal


class MeteredMemo:
    """Persistent ordered-pair cache; original direction is retained by default.

    The optional canonicalize=True mode reproduces the preserved restricted C*
    experiments. The primary run never infers a reverse answer from a forward
    answer. Source calls, logical requests and entries are reported separately.
    """
    def __init__(self, n, source_query, memoize=True, max_entries=250000,
                 canonicalize=False):
        self.n, self.source_query, self.memoize = n, source_query, memoize
        self.max_entries = max_entries
        self.canonicalize = canonicalize
        self.cache = {}
        self.requests = self.cache_hits = self.equal_requests = self.source_calls = 0

    def __call__(self, x, y):
        self.requests += 1
        if x == y:
            self.equal_requests += 1
            return 0
        reverse = self.canonicalize and x > y
        a, b = (y, x) if reverse else (x, y)
        key = a | (b << self.n)
        if self.memoize and key in self.cache:
            self.cache_hits += 1
            ans = self.cache[key]
        else:
            self.source_calls += 1
            ans = int(self.source_query(a, b))
            if self.memoize and (self.max_entries is None or len(self.cache) < self.max_entries):
                self.cache[key] = ans
        return ans ^ int(reverse)

    def ledger(self):
        return dict(logical_requests=self.requests, source_calls=self.source_calls,
                    effective_oracle=('Cstar_canonical_forward_and_complemented_reverse'
                                      if self.canonicalize else 'original_directed_C'),
                    effective_oracle_equals_original_on_all_clean_pairs=True,
                    original_reverse_answer_equality_assumed=False,
                    canonical_pair_cache_enabled=self.memoize and self.canonicalize,
                    ordered_pair_cache_enabled=self.memoize and not self.canonicalize,
                    canonical_pair_cache_entries=len(self.cache),
                    canonical_pair_cache_entry_cap=self.max_entries,
                    cache_hits=self.cache_hits, equal_requests=self.equal_requests,
                    cache_logical_bits_upper=(2 * self.n + 1) * len(self.cache),
                    transmitted_query_argument_bits=2 * self.n * self.source_calls,
                    transmitted_answer_bits=self.source_calls)


def inverse_columns(rows, n):
    aug = [row | (1 << (n + i)) for i, row in enumerate(rows)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if (aug[i] >> j) & 1)
        aug[j], aug[pivot] = aug[pivot], aug[j]
        for i in range(n):
            if i != j and (aug[i] >> j) & 1:
                aug[i] ^= aug[j]
    inverse_rows = [row >> n for row in aug]
    return [sum(((inverse_rows[i] >> j) & 1) << i for i in range(n)) for j in range(n)]


def check_after_return(source, model, comp, exhaustive=True):
    started = time.perf_counter()
    n, r = source.n, source.r
    calls_before, fresh_before = source.calls, source.ideal.fresh_ranks
    points = coefficient_points(n)
    truth = [interpolate({x: (source.ideal.rank(x) >> (n - 1 - j)) & 1 for x in points}, n)
             for j in range(n)]
    equal = [a.body() == b.body() for a, b in zip(model, truth)]
    directions = inverse_columns(source.ideal._rows, n)
    flag_valid = all(truth[i].toggles(directions[i]) and
                     all(truth[j](directions[i]) == truth[j].constant and
                         all((row & directions[i]).bit_count() % 2 == 0 for row in truth[j].polar())
                         for j in range(i))
                     for i in range(n - r))
    assert flag_valid
    rank_errors = degree_errors = 0
    ranks = set()
    check_points = range(1 << n) if exhaustive else random.Random(771).sample(range(1 << n), 1024)
    count = 0
    for x in check_points:
        expected = source.ideal.rank(x)
        ranks.add(expected)
        rank_errors += rank_from_model(model, x) != expected
        degree_errors += rank_from_model(truth, x) != expected
        count += 1
    # The acquired sampler has a unique seed representative in each toggle orbit.
    # Exhausting it at n16 charges 2^16 additional local checks after acquisition.
    sampler_points = 0
    if exhaustive:
        seen = set()
        for target in range(1 << (n - r)):
            fiber = list(comp.fiber(target))
            assert len(fiber) == 1 << r and len(set(fiber)) == len(fiber)
            assert all(comp.prefix(x) == target for x in fiber)
            seen.update(fiber)
            sampler_points += len(fiber)
        assert len(seen) == 1 << n
    inverse_targets = 0
    for target in random.Random(772).sample(range(1 << n), min(64, 1 << n)):
        pref = sum(((target >> (n - 1 - j)) & 1) << j for j in range(n - r))
        xs = [x for x in comp.fiber(pref) if rank_from_model(model, x) == target]
        assert len(xs) == 1 and source.ideal.rank(xs[0]) == target
        inverse_targets += 1
    assert source.calls == calls_before
    return dict(coefficients_exact=all(equal), coordinate_equalities=equal,
                rank_check_points=count, rank_errors=rank_errors,
                exhaustive_degree_check_points=count, degree_errors=degree_errors,
                source_rank_bijection_checked=exhaustive and len(ranks) == 1 << n,
                promised_partial_flag_checked=flag_valid,
                acquired_sampler_points_checked=sampler_points,
                inverse_targets_checked=inverse_targets,
                checking_fresh_source_rank_evaluations=source.ideal.fresh_ranks - fresh_before,
                checking_comparison_calls=source.calls - calls_before,
                seconds=time.perf_counter() - started)


def run_case(n=16, r=2, seed=960162, epsilon=1/32, beta=.05,
             mode='asymmetric_hash', bad_count=None, sequential=True,
             decoder_factory=None, max_requests=None, check=True,
             memory_profile=False, pair_cache_cap=250000, canonicalize=False):
    if bad_count is None:
        bad_count = max(1, int(epsilon * (1 << n)))
    if bad_count / (1 << n) > epsilon:
        raise ValueError('fixture exceeds supplied noise upper bound')
    source = PersistentSource(n, r, seed, bad_count, mode)
    memo = MeteredMemo(n, source.query, max_entries=pair_cache_cap,
                       canonicalize=canonicalize)
    if memory_profile:
        tracemalloc.start()
    receipt, model, comp = acquire(n, r, epsilon, beta, memo, seed + 100000,
                                 sequential=sequential, decoder_factory=decoder_factory,
                                 max_logical_requests=max_requests)
    if memory_profile:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        receipt['tracemalloc_peak_bytes_acquisition'] = peak
    acquisition_fresh = source.ideal.fresh_ranks
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    receipt.update(source=dict(n=n, r=r, fixture_seed=seed, learner_seed=seed+100000,
                               actual_bad_count=bad_count, actual_bad_density=bad_count/(1<<n),
                               supplied_epsilon_upper_bound=epsilon, fault_mode=mode,
                               fixed_bad_items_hidden_from_learner=True,
                               source_setup_seconds=source.setup_seconds,
                               fresh_rank_evaluations_acquisition=acquisition_fresh,
                               cached_rank_payload_logical_bits=2*n*len(source.ideal.cache)),
                   oracle=memo.ledger(), truth_access_only_after_return=True,
                   process_peak_rss_acquisition_bytes=rss if sys.platform=='darwin' else 1024*rss)
    assert source.calls == memo.source_calls
    assert receipt['comparison_requests'] == memo.requests
    if model is not None:
        receipt['returned_model'] = [p.body() for p in model]
        receipt['acquired_toggles'] = comp.toggles
        if check:
            receipt['post_return_checks'] = check_after_return(source, model, comp,
                                                             exhaustive=n<=16)
            if receipt['post_return_checks']['rank_errors'] or not receipt['post_return_checks']['coefficients_exact']:
                receipt['finite_result'] = 'RETURNED_WRONG_MODEL'
            else:
                receipt['finite_result'] = 'EXACT_MODEL_CHECKED_AFTER_RETURN'
    else:
        receipt['finite_result'] = 'UNKNOWN'
    return receipt


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--n', type=int, default=16)
    p.add_argument('--r', type=int, default=2)
    p.add_argument('--seed', type=int, default=960162)
    p.add_argument('--epsilon', type=float, default=1/32)
    p.add_argument('--beta', type=float, default=.05)
    p.add_argument('--bad-count', type=int)
    p.add_argument('--mode', choices=['bad_first_total_order','flip_incident','asymmetric_hash','ideal'],
                   default='asymmetric_hash')
    p.add_argument('--fixed-horizon', action='store_true')
    p.add_argument('--max-requests', type=int)
    p.add_argument('--memory-profile', action='store_true')
    p.add_argument('--no-check', action='store_true')
    p.add_argument('--original-directed', action='store_true')
    p.add_argument('--canonicalize', action='store_true',
                   help='restricted Cstar experiment; primary default keeps original directed C')
    p.add_argument('--output', default='receipt_n16_r2_hash.json')
    a = p.parse_args()
    receipt = run_case(a.n, a.r, a.seed, a.epsilon, a.beta, a.mode, a.bad_count,
                       not a.fixed_horizon, max_requests=a.max_requests,
                       memory_profile=a.memory_profile, check=not a.no_check,
                       canonicalize=a.canonicalize and not a.original_directed)
    output = HERE / a.output
    output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(output=str(output), status=receipt['status'],
                         finite_result=receipt['finite_result'],
                         seconds=receipt['seconds'],
                         oracle=receipt['oracle'],
                         body_decoder=receipt['body_decoder'],
                         validation_batches=receipt['validation_batches']), indent=2))


if __name__ == '__main__':
    main()
