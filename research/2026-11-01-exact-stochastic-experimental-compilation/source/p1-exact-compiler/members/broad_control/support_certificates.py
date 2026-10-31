"""Support-only stochastic reachability certificates, using exact rationals.

This is a constructive comparator, not a claim of new qualitative model checking.
No transition probabilities enter certificate synthesis after support recovery.
"""
from collections import deque
from fractions import Fraction
import json
import math
import random
from pathlib import Path


def acquire_support(rows, p_min, delta, rng):
    """Every row is an executable local generative source returning a state.

    This API charges every invocation. It does not earn the physical ability
    to reset to an arbitrary row. The source caller must separately price it.
    """
    n = len(rows)
    m = math.ceil(math.log(n * n / delta) / float(p_min))
    support = [set() for _ in rows]
    for i, source in enumerate(rows):
        for _ in range(m):
            support[i].add(source(rng))
    return support, n*m, m


def certificate(support, target, p_min):
    n = len(support)
    pred = [[] for _ in range(n)]
    for u, successors in enumerate(support):
        for v in successors:
            pred[v].append(u)
    dist = [None]*n
    q = deque(target)
    for t in target:
        dist[t] = 0
    while q:
        v = q.popleft()
        for u in pred[v]:
            if dist[u] is None:
                dist[u] = dist[v]+1
                q.append(u)
    if any(d is None for d in dist):
        return None
    D = max(dist)
    if p_min == 1:
        values = [Fraction(d) for d in dist]
    else:
        values = [(1-p_min**d)/((1-p_min)*p_min**D) for d in dist]
    return dist, values


def worst_drift(support, values, p_min, target):
    """Exact maximum row expectation over positive support masses >= p_min."""
    drifts = []
    for s, post in enumerate(support):
        if s in target:
            continue
        if len(post)*p_min > 1:
            raise ValueError("Support incompatible with p_min")
        expectation = p_min*sum(values[t] for t in post)
        expectation += (1-len(post)*p_min)*max(values[t] for t in post)
        drifts.append(values[s]-expectation)
    return min(drifts, default=Fraction(0))


def run():
    rng = random.Random(20261101)
    D = 30
    p = Fraction(1, 10)
    # Source advances one site with probability p; otherwise all progress lost.
    rows = []
    for s in range(D):
        rows.append(lambda r, s=s: s+1 if r.randrange(10)==0 else 0)
    rows.append(lambda r: D)
    support, actions, per_row = acquire_support(rows, p, .01, rng)
    expected_support = [{0, s+1} for s in range(D)] + [{D}]
    assert support == expected_support
    dist, V = certificate(support, {D}, p)
    drift = worst_drift(support, V, p, {D})
    assert drift == 1
    # Here the upper-bound certificate is the exact expected hitting time.
    for s in range(D):
        assert V[s] == 1 + p*V[s+1] + (1-p)*V[0]
    assert V[D] == 0
    # The same acquired support is reused for every target containing D.
    reuses = 0
    for _ in range(200):
        target = {D} | {s for s in range(D) if rng.random()<.1}
        result = certificate(support, target, p)
        assert result is not None
        _, W = result
        assert worst_drift(support, W, p, target) >= 1
        reuses += 1
    # Random supports with a guaranteed path to a target; every row has <= 5
    # edges and p=1/8. Check exact worst compatible rows, not sampled kernels.
    random_checks = 0
    for n in range(2, 41):
        for _ in range(20):
            g = []
            for s in range(n-1):
                post = {s+1}
                post.update(rng.randrange(n) for _ in range(4))
                g.append(post)
            g.append({n-1})
            _, W = certificate(g, {n-1}, Fraction(1,8))
            assert worst_drift(g, W, Fraction(1,8), {n-1}) >= 1
            random_checks += 1
    result = {
        'construction': 'support-only exact rational RSM',
        'states': D+1,
        'p_min': str(p),
        'confidence_delta': .01,
        'sampled_source_invocations': actions,
        'samples_per_row': per_row,
        'recovered_support_exactly_in_fixture': True,
        'certificate_minimum_worst_compatible_row_drift': str(drift),
        'certificate_max_numerator_bits': max(v.numerator.bit_length() for v in V),
        'certificate_max_denominator_bits': max(v.denominator.bit_length() for v in V),
        'exact_expected_physical_steps_to_reset_from_zero': str(V[0]),
        'expected_steps_float': float(V[0]),
        'additional_adaptive_target_queries_without_source_calls': reuses,
        'exact_random_support_checks': random_checks,
        'scope': 'Generative row access only; arbitrary physical resets are NOT acquired.',
    }
    Path(__file__).with_name('support_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
