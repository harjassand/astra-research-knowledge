"""Comparison-only robust partial-flag learner for quadratic bijections.

All labels, directions, coefficients and samplers are acquired from `query`.
The degree, flag-existence, item-error bound and beta are supplied promises.
Fixed persistent comparisons may be arbitrary on pairs incident to bad items.
No exhaustive input-domain data enters this learner. Stdlib only.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'p_s01_partial_flag'))
from partial_flag import Compiler, Quadratic, combine
from shifted_ball_decoder import ShiftedBallDecoder
import math
import random
import time


class StopUnknown(Exception):
    pass


def binary_kl(x, y):
    if x == 0:
        return -math.log1p(-y)
    if x == 1:
        return -math.log(y)
    return x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))


def threshold_equal_kl(a, b):
    # D(t||a)-D(t||b) is an affine function of t.
    A = math.log(b / a)
    B = math.log((1 - b) / (1 - a))
    return -B / (A - B)


def validator_config(epsilon, delta):
    a = 2 * epsilon
    gap0 = .25 - 4 * epsilon
    if not 0 < epsilon < 1 / 16 or not 0 < delta < 1 / 3:
        raise ValueError("this implementation requires positive noise bound <1/16")
    # Optimize a fully specified finite cap, not an empirical post-selection.
    choices = []
    for m in range(1, math.ceil(2 / gap0 ** 2) + 1):
        c = math.comb(2 * m, m) / (2 * 4 ** m)
        b = .25 - 2 * epsilon - c
        if b <= a:
            continue
        tau = threshold_equal_kl(a, b)
        exponent = min(binary_kl(tau, a), binary_kl(tau, b))
        cap = math.ceil(math.log(2 / delta) / exponent)
        choices.append((m * m * cap, m, c, b, tau, cap, exponent))
    _, m, c, b, tau, cap, exponent = min(choices)
    return dict(m=m, c_m=c, true_mean_upper=a, false_mean_lower=b,
                threshold=tau, batch_cap=cap, fixed_horizon_kl_exponent=exponent,
                llr_positive_slope=math.log(b / a),
                llr_negative_slope=math.log((1 - b) / (1 - a)),
                llr_boundary=math.log(2 / delta), failure_budget=delta,
                maximum_comparison_requests=cap * m * m)


def config(n, r, epsilon, beta):
    if not 1 <= n or not 0 <= r <= n or not 0 < beta <= .5:
        raise ValueError("invalid dimension/confidence contract")
    h = n - r
    p = 2 ** (-r - 1)
    Rcap = math.ceil((2 / p) * math.log(4 * h / beta)) if h else 0
    delta = beta / (4 * h * Rcap ** 2) if h else beta / 4
    validator = validator_config(epsilon, delta)
    return dict(n=n, r=r, degree=2, h=h, epsilon=epsilon, beta=beta,
                genuine_direction_probability_lower=p, candidate_cap=Rcap,
                per_candidate_validation_failure_budget=delta,
                body_failure_budget=.25,
                suffix_body_failure_budget=beta / (2 * r) if r else 0,
                validator=validator,
                first_wrong_prefix_acceptance_probability_upper=h * Rcap * delta,
                prefix_candidate_exhaustion_probability_upper=beta / 4,
                suffix_failure_probability_upper=beta / 2 if r else 0,
                total_wrong_or_unknown_probability_upper=(beta / 4 + h * Rcap * delta
                                                           + (beta / 2 if r else 0)))


def as_quadratic(terms, n):
    upper = [0] * n
    linear = 0
    for s in terms:
        if s.bit_count() == 1:
            linear |= s
        elif s.bit_count() == 2:
            low = s & -s
            upper[low.bit_length() - 1] |= s ^ low
        elif s:
            raise ValueError("nonquadratic decoder result")
    return Quadratic(int(0 in terms), linear, upper)


def matching_batch(f, v, comp, query, rng, m):
    pref = rng.getrandbits(len(comp.q))
    left, right = [], []
    for bit, target in ((0, left), (1, right)):
        for _ in range(m):
            x = comp.sample(pref, rng)
            target.append(x if f(x) == bit else x ^ v)
    unmatched = list(range(m))
    size = requests = 0
    # The greedy matching is maximal; repeated sampled positions remain vertices.
    for x in left:
        for j in unmatched:
            requests += 1
            if not query(x, right[j]):
                unmatched.remove(j)
                size += 1
                break
    return size / m, requests


def validate(f, v, comp, query, rng, cfg, sequential=True):
    score = llr = 0.0
    requests = 0
    for t in range(1, cfg['batch_cap'] + 1):
        z, used = matching_batch(f, v, comp, query, rng, cfg['m'])
        requests += used
        score += z
        llr += z * cfg['llr_positive_slope'] + (1 - z) * cfg['llr_negative_slope']
        if sequential and llr >= cfg['llr_boundary']:
            return False, dict(batches=t, mean_score=score / t, llr=llr,
                               stopping_rule='llr_reject', comparison_requests=requests)
        if sequential and llr <= -cfg['llr_boundary']:
            return True, dict(batches=t, mean_score=score / t, llr=llr,
                              stopping_rule='llr_accept', comparison_requests=requests)
    passed = score / cfg['batch_cap'] <= cfg['threshold']
    return passed, dict(batches=cfg['batch_cap'], mean_score=score / cfg['batch_cap'],
                       llr=llr, stopping_rule='fixed_horizon_kl',
                       comparison_requests=requests)


def current_fiber(x, comp, suffix, k, n):
    fiber = list(comp.fiber(comp.prefix(x)))
    values = [p(x) for p in suffix]
    fiber = [y for y in fiber if all(p(y) == b for p, b in zip(suffix, values))]
    if len(fiber) != (1 << (n - k)) or len(set(fiber)) != len(fiber) or x not in fiber:
        raise StopUnknown('filtered_fiber_cardinality_check_failed')
    return fiber


def acquire(n, r, epsilon, beta, query, seed, *, sequential=True,
            max_logical_requests=None, force_zero_directions=False,
            decoder_factory=None):
    """Acquire the complete model from the single counted comparison callback.

    Optional request budget is a fail-closed compute limit: no confidence penalty
    is spent on UNKNOWN. force_zero_directions is a test-only exhaustion fixture.
    A decoder_factory can replace only the body/tail decoder for matched controls.
    """
    begin = time.perf_counter()
    cfg = config(n, r, epsilon, beta)
    rng = random.Random(seed)
    comp = Compiler(n, True)
    body = (decoder_factory or ShiftedBallDecoder)(n, 2, 2 * epsilon, .25, rng)
    tail = (decoder_factory or ShiftedBallDecoder)(n, 2, 2 * epsilon,
                                                 beta / (2 * r) if r else .25, rng)
    suffix = []
    attempts = []
    logical = raw_cache_max = validation_requests = validation_batches = 0
    preprocessing_seconds = time.perf_counter() - begin

    def ask(x, y):
        nonlocal logical
        if max_logical_requests is not None and logical >= max_logical_requests:
            raise StopUnknown('comparison_request_budget_exhausted')
        logical += 1
        return int(query(x, y))

    def result(status, reason=None):
        ans = dict(status=status, parameters=cfg, attempts=attempts,
                   body_decoder=body.ledger(), suffix_decoder=tail.ledger(),
                   comparison_requests=logical,
                   validation_comparison_requests=validation_requests,
                   validation_batches=validation_batches,
                   deterministic_raw_cache_max_entries=raw_cache_max,
                   sampler_cache_enabled=True,
                   sampler_cache_max_entries=comp.sampler_cache_max_entries,
                   sampler_fiber_draws=comp.fiber_draws,
                   sampler_projections=comp.projections,
                   sampler_polynomial_evaluations=comp.projection_q_evaluations,
                   tail_enumerated_seed_positions=comp.enumerated_points,
                   direction_random_bits=comp.direction_random_bits,
                   fiber_seed_random_bits=comp.random_bits,
                   seconds=time.perf_counter() - begin,
                   preprocessing_seconds=preprocessing_seconds,
                   sequential_validation_enabled=sequential,
                   all_source_calls_pass_only_through_query=True)
        if reason:
            ans['reason'] = reason
        return ans

    try:
        for k in range(n - r):
            accepted = False
            for trial in range(cfg['candidate_cap']):
                a = 0 if force_zero_directions else rng.getrandbits(len(comp.stabilizer))
                comp.direction_random_bits += 0 if force_zero_directions else len(comp.stabilizer)
                v = combine(comp.stabilizer, a)
                if not v:
                    attempts.append(dict(stage=k, trial=trial, status='zero_direction_skipped'))
                    continue
                cache = {}

                def raw(x):
                    if x not in cache:
                        cache[x] = 1 ^ ask(x, x ^ v)
                    return cache[x]

                body_started = time.perf_counter()
                f = as_quadratic(body.decode(raw), n)
                body_seconds = time.perf_counter() - body_started
                raw_cache_max = max(raw_cache_max, len(cache))
                if not f.toggles(v):
                    attempts.append(dict(stage=k, trial=trial, status='own_toggle_rejected',
                                         direction=v, raw_cache_entries=len(cache),
                                         body_seconds=body_seconds))
                    continue
                validation_started = time.perf_counter()
                passed, receipt = validate(f, v, comp, ask, rng, cfg['validator'], sequential)
                receipt['seconds'] = time.perf_counter() - validation_started
                validation_requests += receipt['comparison_requests']
                validation_batches += receipt['batches']
                attempts.append(dict(stage=k, trial=trial,
                                     status='accepted' if passed else 'matching_rejected',
                                     direction=v, raw_cache_entries=len(cache),
                                     body_seconds=body_seconds, validation=receipt))
                if passed:
                    comp.add(f, v)
                    accepted = True
                    break
            if not accepted:
                raise StopUnknown('candidate_cap_exhausted')
        for k in range(n - r, n):
            cache = {}

            def raw(x):
                if x not in cache:
                    fiber = current_fiber(x, comp, suffix, k, n)
                    count = sum(ask(y, x) for y in fiber if y != x)
                    cache[x] = int(2 * count >= len(fiber))
                return cache[x]

            suffix.append(as_quadratic(tail.decode(raw), n))
            raw_cache_max = max(raw_cache_max, len(cache))
    except StopUnknown as exc:
        return result('UNKNOWN', str(exc)), None, comp
    return result('returned_model'), comp.q + suffix, comp
