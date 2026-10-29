#!/usr/bin/env python3
"""Exact finite checks of the signed witness and an addressed Ising consumer.

These are population-model calculations, not acquired physical observations.
The continuous-time analytic theorem is proved in the accompanying document;
the floating CT entries below are only independent sanity checks.
"""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = (F(1, 10), F(3, 10), F(1, 4), F(7, 20))
B = (F(1, 20), F(3, 20), F(1, 10), F(1, 10))
VA = (B[0], -B[1], B[2], -B[3])
P = tuple((u, b) for u, b in zip(U, B))
ZERO, ONE = (F(0),), (F(1),)


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return tuple(p)


def add(a, b):
    c = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return trim(c)


def scale(a, z):
    return trim([x * z for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def ev(p, h):
    z = F(0)
    for x in reversed(p):
        z = z * h + x
    return z


def derivative(p):
    return trim([F(i) * p[i] for i in range(1, len(p))] or [F(0)])


def frac(x):
    return str(x.numerator) + '/' + str(x.denominator)


def all_total_trees(depth):
    """Full policy enumeration, including early stopping, no deduplication."""
    if depth == 0:
        return [ZERO]
    prev = all_total_trees(depth - 1)
    out = [ZERO]
    for p in P:
        for left in prev:
            noflip_part = mul(sub(ONE, p), left)
            for right in prev:
                out.append(add(noflip_part, mul(p, sub(ONE, right))))
    return out


def all_herald_trees(depth):
    """Pair (opposite-success, same-success), relative to each subtree input."""
    if depth == 0:
        return [(ZERO, ONE), (ZERO, ZERO)]
    prev = all_herald_trees(depth - 1)
    out = [(ZERO, ONE), (ZERO, ZERO)]
    for p in P:
        no = sub(ONE, p)
        for f0, e0 in prev:
            for f1, e1 in prev:
                out.append((add(mul(no, f0), mul(p, e1)),
                            add(mul(no, e0), mul(p, f1))))
    return out


def check_tree_cone():
    total = all_total_trees(3)
    nonzero = 0
    degrees = {}
    witness_max = None
    for f in total:
        if f == ZERO:
            continue
        nonzero += 1
        d = len(f) - 1
        degrees[d] = degrees.get(d, 0) + 1
        assert d >= 1 and f[-1] * ((-1) ** (d - 1)) > 0
        value = ev(f, F(-4))
        assert value < 0
        witness_max = value if witness_max is None else max(witness_max, value)
        assert F(0) < ev(f, F(0)) < 1

    herald = all_herald_trees(2)
    successful = 0
    checks = 0
    for f, e in herald:
        if ev(add(f, e), F(0)) == 0:
            assert f == ZERO and e == ZERO
            continue
        successful += 1
        assert ev(f, F(-4)) <= 0 and ev(e, F(-4)) >= 0
        for c in (F(3, 20), F(3, 10), F(1, 2)):
            g = sub(scale(f, 1 - c), scale(e, c))
            assert ev(g, F(-4)) < 0
            checks += 1
    return {'total_depth3_trees': len(total),
            'nonzero_flip_trees': nonzero,
            'nonzero_polynomial_degrees': degrees,
            'largest_negative_witness_value': frac(witness_max),
            'herald_depth2_trees': len(herald),
            'herald_positive_success_trees': successful,
            'herald_target_sign_checks': checks}


def check_monotonicity_failure():
    # Fast mode3 while 0, slow mode0 while 1: a legal state-feedback policy.
    p_fast, p_slow = P[3], P[0]
    f = ZERO
    outputs = []
    for n in range(1, 13):
        f = add(p_fast, mul(sub(sub(ONE, p_fast), p_slow), f))
        outputs.append({'calls': n, 'derivative_at_zero': frac(ev(derivative(f), F(0))),
                        'flip_at_minus1': frac(ev(f, F(-1))),
                        'flip_at_plus1': frac(ev(f, F(1)))})
    negative = [r['calls'] for r in outputs
                if F(r['derivative_at_zero']) < 0]
    assert negative
    assert ev(f, F(-4)) < 0
    return {'first_negative_derivative_call_count': negative[0],
            'fixed_policy_values': outputs,
            'last_polynomial': [frac(x) for x in f]}


def check_ring():
    d = 4
    states = list(product((0, 1), repeat=d))
    index = {x: i for i, x in enumerate(states)}
    weights = []
    for x in states:
        equal = sum(x[i] == x[(i + 1) % d] for i in range(d))
        assert equal % 2 == 0
        weights.append(F(5, 3) ** (equal // 2))
    z = sum(weights)
    pi = [w / z for w in weights]
    transition = [[F(0) for _ in states] for _ in states]
    locals_checked = 0
    key_counts_seen = set()
    for row, x in enumerate(states):
        for site in range(d):
            neigh = x[(site - 1) % d] + x[(site + 1) % d]
            conditional_one = (F(3, 8), F(1, 2), F(5, 8))[neigh]
            target_flip = F(9, 20) * (conditional_one if x[site] == 0
                                      else 1 - conditional_one)
            r = (target_flip - F(3, 20)) / F(3, 20)
            assert r in (F(1, 8), F(1, 2), F(7, 8))
            counts = [0, 0, 0, 0]
            # Enumerate 3 selector bits and 2 raw-mode bits: exactly32 keys.
            for selector, raw in product(range(8), range(4)):
                if selector < 8 * r:
                    j = 2 + (raw % 2)
                else:
                    j = 0 if raw < 3 else 1
                counts[j] += 1
            pkeys = [F(c, 32) for c in counts]
            assert sum(pkeys) == 1
            assert sum(p * u for p, u in zip(pkeys, U)) == target_flip
            assert sum(p * v for p, v in zip(pkeys, VA)) == 0
            key_counts_seen.add(tuple(counts))
            for h in (F(-1), F(-2, 7), F(0), F(3, 11), F(1)):
                actual = sum(p * (u + v * h)
                             for p, u, v in zip(pkeys, U, VA))
                assert actual == target_flip
            y = list(x)
            y[site] = 1 - y[site]
            col = index[tuple(y)]
            transition[row][col] += target_flip / d
            transition[row][row] += (1 - target_flip) / d
            # Direct conditional Gibbs probability from the global target.
            y0, y1 = list(x), list(x)
            y0[site], y1[site] = 0, 1
            w0, w1 = weights[index[tuple(y0)]], weights[index[tuple(y1)]]
            assert w1 / (w0 + w1) == conditional_one
            locals_checked += 1
    assert all(sum(row) == 1 and min(row) >= 0 for row in transition)
    detailed_checks = 0
    for a in range(len(states)):
        for b in range(len(states)):
            assert pi[a] * transition[a][b] == pi[b] * transition[b][a]
            detailed_checks += 1
    stationary = [sum(pi[a] * transition[a][b] for a in range(len(states)))
                  for b in range(len(states))]
    assert stationary == pi
    mean_ones = sum(p * sum(x) for p, x in zip(pi, states))
    nearest_corr = sum(p * (2 * x[0] - 1) * (2 * x[1] - 1)
                       for p, x in zip(pi, states))
    assert mean_ones == 2
    return {'states': len(states), 'local_context_checks': locals_checked,
            'native_key_counts_out_of_32': sorted(key_counts_seen),
            'pointwise_hidden_value_checks': 5 * locals_checked,
            'detailed_balance_pairs': detailed_checks,
            'stationary_law': [frac(p) for p in pi],
            'mean_number_of_ones': frac(mean_ones),
            'nearest_neighbor_spin_correlation': frac(nearest_corr),
            'ideal_native_calls_per_site_update': 1,
            'private_fair_bits_per_site_update': 5,
            'random_scan_extra_bits_for_four_sites': 2}


def chebyshev(n, x):
    if n == 0:
        return F(1)
    a, b = F(1), x
    for _ in range(1, n):
        a, b = b, 2 * x * b - a
    return b


def ct_sanity():
    rows = []
    for h in (-4.0, -1.0, 0.0, 1.0):
        rates = [-math.log(1 - 2 * (float(u) + float(b) * h)) / 2
                 for u, b in zip(U, B)]
        if h == -4:
            assert max(rates) < 0
        else:
            assert min(rates) > 0
        # Actual feedback: mode3 from0, mode0 from1.
        a, b = rates[3], rates[0]
        for t in (0.125, 1.0, 8.0):
            flip = a / (a + b) * (-math.expm1(-(a + b) * t))
            assert (flip < 0) if h == -4 else (0 < flip < 1)
            rows.append({'h': h, 'time_in_t0_units': t,
                         'feedback_flip_probability_or_continuation': flip})
    return {'scope': 'Floating sanity calculation, not a numerical proof or experiment',
            'state_feedback_checks': rows}


def main():
    out = {'scope': 'Exact population-model finite checks except explicitly marked CT floats',
           'signed_tree_cone': check_tree_cone(),
           'failed_monotonicity_attack': check_monotonicity_failure(),
           'addressed_Ising_ring': check_ring(),
           'uniform_fixed_call_lower_bounds': [
               {'maximum_calls': n, 'c': '3/10',
                'bound': frac(F(3, 10) / chebyshev(n, F(7, 2)))}
               for n in (1, 2, 3, 4, 8, 16)],
           'continuous_time_sanity': ct_sanity()}
    out['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ROOT / 'SIGNED_CONTROL_CHECKS.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items()
                      if k in ('signed_tree_cone', 'addressed_Ising_ring', 'script_sha256')},
                     indent=2))


if __name__ == '__main__':
    main()
