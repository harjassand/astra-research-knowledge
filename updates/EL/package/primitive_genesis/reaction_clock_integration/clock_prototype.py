"""Numerical sanity checks for the exact mathematical sparse clock construction.

This is a double-precision reference prototype, not a bit-exact sampler.
All write paths remain in the reaction_clock_integration directory.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
from pathlib import Path
import random
import statistics


def open_uniform(rng):
    u = rng.random()
    while u == 0.0:
        u = rng.random()
    return u


def geom0(continuation, rng):
    """P(G=m) = (1-continuation) continuation**m, m >= 0."""
    if continuation == 0.0:
        return 0
    return math.floor(math.log(open_uniform(rng)) / math.log(continuation))


def sparse_clock(n, k, order, growth, rng, scale=1.0):
    """Return duration, sorted sparse stage extras, candidate count, and total extras."""
    if k == 0:
        return 0.0, [], 0, 0
    low = math.comb(n, order)
    high = math.comb(n + (k - 1) * growth, order)
    if low <= 0 or high < low:
        raise ValueError('Requires positive nondecreasing rates.')
    if high == low:
        return rng.gammavariate(k, 1.0 / (scale * high)), [], 0, 0
    difference = high - low
    qstar = difference / high
    marks, total, candidates = [], 0, 0
    index = -1
    while True:
        gap = 1 + math.floor(math.log(open_uniform(rng)) / math.log1p(-qstar))
        index += gap
        if index >= k:
            break
        candidates += 1
        local_difference = high - math.comb(n + index * growth, order)
        if rng.random() < local_difference / difference:
            q = local_difference / high
            extra = 1 + geom0(q, rng)
            marks.append((index, extra))
            total += extra
    return rng.gammavariate(k + total, 1.0 / (scale * high)), marks, candidates, total


def cutoff_count(duration, marks, k, horizon, rng):
    """Locate the horizon through a lazy conditional gamma/Dirichlet tree."""
    if horizon >= duration:
        return k, 0
    if horizon <= 0.0:
        return 0, 0
    lo, hi, current_time, residual, splits = 0, k, duration, horizon, 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        left_shape = mid - lo + sum(v for i, v in marks if lo <= i < mid)
        right_shape = hi - mid + sum(v for i, v in marks if mid <= i < hi)
        left_time = rng.betavariate(left_shape, right_shape) * current_time
        splits += 1
        if residual < left_time:
            hi, current_time = mid, left_time
        else:
            lo, current_time = mid, current_time - left_time
            residual -= left_time
    return lo, splits


def decode_microcount(marks, microcount):
    """Map unit-gamma phases completed to original stages completed."""
    completed = microcount
    for index, extra in marks:
        if index >= completed:
            break
        completed = max(index, completed - extra)
    return completed


def cutoff_binomial(duration, marks, k, horizon, rng):
    """One binomial plus one sparse scan; requires Python 3.12+ random API."""
    if horizon >= duration:
        return k, 0
    if horizon <= 0.0:
        return 0, 0
    total_shape = k + sum(extra for _, extra in marks)
    microcount = rng.binomialvariate(total_shape - 1, horizon / duration)
    completed = decode_microcount(marks, microcount)
    assert 0 <= completed < k
    return completed, 1


def sparse_decoder_check():
    """Exhaustive finite inverse-CDF-index check, independent of random sampling."""
    cases = 0
    for k in range(1, 6):
        for extras in itertools.product(range(4), repeat=k):
            marks = [(i, value) for i, value in enumerate(extras) if value]
            boundaries, cumulative = [], 0
            for value in extras:
                cumulative += 1 + value
                boundaries.append(cumulative)
            for microcount in range(cumulative):
                expected = sum(boundary <= microcount for boundary in boundaries)
                assert decode_microcount(marks, microcount) == expected
                cases += 1
    return {'status': 'FINITE_EXHAUSTIVE_ONLY', 'checked_microcounts': cases,
            'stage_counts': [1, 2, 3, 4, 5], 'extras_each': [0, 1, 2, 3], 'passed': True}


def nb_pmf(n, j, time):
    """Number of births by time in a unit-rate Yule process with n ancestors."""
    p = math.exp(-time)
    return math.comb(n + j - 1, j) * p ** n * (-math.expm1(-time)) ** j


def hitting_cdf(n, k, time):
    if time <= 0.0:
        return 0.0
    return max(0.0, min(1.0, 1.0 - sum(nb_pmf(n, j, time) for j in range(k))))


def standardized_max(observed, expected, trials):
    return max(abs(o / trials - p) / math.sqrt(max(p * (1 - p), 1 / trials) / trials)
               for o, p in zip(observed, expected))


def yule_joint_check(trials, cutoff=cutoff_count):
    rng = random.Random(10212026)
    n, k, time = 3, 7, 0.45
    thresholds = [0.70, 1.10]
    counts = [0] * (k + 1)
    joints = [[0] * (k + 1) for _ in thresholds]
    candidates, extras, splits, durations = [], [], [], []
    for _ in range(trials):
        duration, marks, candidate_count, total_extra = sparse_clock(n, k, 1, 1, rng)
        j, split_count = cutoff(duration, marks, k, time, rng)
        counts[j] += 1
        for h, row in zip(thresholds, joints):
            if duration <= h:
                row[j] += 1
        candidates.append(candidate_count)
        extras.append(total_extra)
        splits.append(split_count)
        durations.append(duration)
    exact_count = [nb_pmf(n, j, time) for j in range(k)] + [hitting_cdf(n, k, time)]
    count_z = standardized_max(counts, exact_count, trials)
    joint_z = []
    for h, row in zip(thresholds, joints):
        expected = [nb_pmf(n, j, time) * hitting_cdf(n + j, k - j, h - time)
                    for j in range(k)] + [hitting_cdf(n, k, time)]
        joint_z.append(standardized_max(row, expected, trials))
    mean_exact = sum(1 / (n + i) for i in range(k))
    variance_exact = sum(1 / (n + i) ** 2 for i in range(k))
    mean_z = abs(statistics.mean(durations) - mean_exact) / math.sqrt(variance_exact / trials)
    assert count_z < 6.0 and max(joint_z) < 6.0 and mean_z < 6.0
    return {'trials': trials, 'cutoff': cutoff.__name__, 'n': n, 'k': k, 'time': time,
            'max_count_z': count_z, 'max_joint_z_by_endpoint_threshold': dict(zip(thresholds, joint_z)),
            'duration_mean_z': mean_z, 'mean_candidates': statistics.mean(candidates),
            'exact_mean_candidates': k * (1 - n / (n + k - 1)),
            'mean_extras': statistics.mean(extras),
            'exact_mean_extras': sum((n + k - 1) / (n + i) - 1 for i in range(k)),
            'mean_terminal_steps': statistics.mean(splits), 'passed': True}


def changing_population_check(trials, cutoff=cutoff_count):
    """A -> 2A and B -> 2B, both unit rate: two independent Yule processes."""
    rng = random.Random(120102026)
    a0, b0, time = 3, 4, 0.6
    values_a, values_b, no_a, no_b, no_both = [], [], 0, 0, 0
    for _ in range(trials):
        a, b, now = a0, b0, 0.0
        while now < time:
            n = a + b
            k = max(1, math.isqrt(n))
            duration, marks, _, _ = sparse_clock(n, k, 1, 1, rng)
            if now + duration > time:
                j, _ = cutoff(duration, marks, k, time - now, rng)
                for _ in range(j):
                    if rng.random() < a / (a + b):
                        a += 1
                    else:
                        b += 1
                break
            for _ in range(k):
                if rng.random() < a / (a + b):
                    a += 1
                else:
                    b += 1
            now += duration
        values_a.append(a)
        values_b.append(b)
        no_a += a == a0
        no_b += b == b0
        no_both += a == a0 and b == b0
    factor = math.exp(time)
    mean_a, mean_b = a0 * factor, b0 * factor
    var_a, var_b = a0 * factor * (factor - 1), b0 * factor * (factor - 1)
    z_a = abs(statistics.mean(values_a) - mean_a) / math.sqrt(var_a / trials)
    z_b = abs(statistics.mean(values_b) - mean_b) / math.sqrt(var_b / trials)
    observed_events = [no_a, no_b, no_both]
    expected_events = [math.exp(-a0 * time), math.exp(-b0 * time), math.exp(-(a0 + b0) * time)]
    event_z = standardized_max(observed_events, expected_events, trials)
    covariance = sum((a - mean_a) * (b - mean_b) for a, b in zip(values_a, values_b)) / trials
    covariance_z = abs(covariance) / math.sqrt(var_a * var_b / trials)
    assert max(z_a, z_b, event_z, covariance_z) < 6.0
    return {'trials': trials, 'cutoff': cutoff.__name__, 'network': ['A -> 2A at rate 1', 'B -> 2B at rate 1'],
            'start': {'A': a0, 'B': b0}, 'time': time,
            'A_mean_z': z_a, 'B_mean_z': z_b, 'unchanged_event_max_z': event_z,
            'covariance_z': covariance_z, 'passed': True}


def resource_check(trials):
    rng = random.Random(20261012)
    rows = []
    for n in [100, 10000, 1000000, 100000000]:
        k = math.isqrt(n)
        candidates, extras = [], []
        for _ in range(trials):
            _, _, c, e = sparse_clock(n, k, 2, 1, rng)
            candidates.append(c)
            extras.append(e)
        low, high = math.comb(n, 2), math.comb(n + k - 1, 2)
        exact_candidates = k * (high - low) / high
        rows.append({'n': n, 'k': k, 'mean_candidates': statistics.mean(candidates),
                     'exact_mean_candidates': exact_candidates, 'mean_extras': statistics.mean(extras)})
    return {'trials_each': trials, 'order': 2, 'growth': 1, 'rows': rows,
            'interpretation': 'Bounded expected queried rates; no runtime or bit-exactness claim.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trials', type=int, default=100000)
    args = parser.parse_args()
    results = {'status': 'NUMERICAL_SANITY_ONLY',
               'arithmetic': 'Python double precision and pseudorandom variates; mathematical proof separate',
               'joint_clock_cutoff': yule_joint_check(args.trials),
               'joint_clock_binomial_cutoff': yule_joint_check(args.trials, cutoff_binomial),
               'two_type_changing_population': changing_population_check(args.trials),
               'two_type_binomial_cutoff': changing_population_check(args.trials, cutoff_binomial),
               'sparse_decoder': sparse_decoder_check(),
               'query_scaling': resource_check(max(10000, args.trials // 5))}
    Path('validation_results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
