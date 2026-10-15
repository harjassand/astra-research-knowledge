#!/usr/bin/env python3
"""Exact finite-statistic clock obstruction, with independent generator checks.

All model parameters and equality assertions use fractions/SymPy rationals.
Only displayed probabilities and timings use mpmath transcendental arithmetic.
The certified ratio lower bound is rational and is checked independently.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import sympy as sp

HERE = Path(__file__).resolve().parent
mp.mp.dps = 90


def rat(v):
    v = F(v)
    return sp.Rational(v.numerator, v.denominator)


def mpr(v):
    v = F(v)
    return mp.mpf(v.numerator) / v.denominator


def lagrange_weights(nodes, value, probes):
    """Rational interpolation in {p(x)/D(x): deg p <= n-1}."""
    def denominator(x):
        result = F(1)
        for shift, multiplicity in probes:
            result *= (1 + shift * x) ** multiplicity
        return result

    result = []
    for i, xi in enumerate(nodes):
        li = F(1)
        for j, xj in enumerate(nodes):
            if i != j:
                li *= (value - xj) / (xi - xj)
        result.append(li * denominator(xi) / denominator(value))
    return result


def construct(order, probes, deadline):
    n = order + 1 + sum(m for _, m in probes)
    assert order >= 2 and deadline > n + 1
    nodes = [F(i + 2) for i in range(n)]
    c = lagrange_weights(nodes, F(deadline), probes)
    assert sum(c) == 1
    assert max(abs(v) for v in c) <= F(deadline) ** (n - 1)
    ceiling = max([F(1)] + [abs(v) for v in c])
    epsilon = 1 / (2 * n * ceiling)
    q = F(1, deadline**3)
    baseline = [F(1, n)] * n
    perturbed = [w - epsilon * ci for w, ci in zip(baseline, c)]
    assert all(w >= F(1, 2 * n) for w in perturbed)
    perturbed.append(epsilon)
    alternative_nodes = nodes + [F(deadline)]
    # Split one baseline phase into two identical positive phases. The two
    # chains then have the same number of states, all reachable from the source.
    baseline[0] /= 2
    baseline.append(F(1, 2 * n))
    baseline_nodes = nodes + [nodes[0]]
    assert sum(baseline) == sum(perturbed) == 1
    return n, q, epsilon, c, baseline_nodes, baseline, alternative_nodes, perturbed


def make_generator(nodes, weights, q):
    count = len(nodes)
    Q = sp.zeros(count + 2)
    Q[0, 0] = -1
    Q[0, -1] = rat(1 - q)
    for i, (x, w) in enumerate(zip(nodes, weights), start=1):
        Q[0, i] = rat(q * w)
        Q[i, i] = -rat(1 / x)
        Q[i, -1] = rat(1 / x)
    assert Q * sp.ones(count + 2, 1) == sp.zeros(count + 2, 1)
    assert all(Q[i, j] >= 0 for i in range(count + 2)
               for j in range(count + 2) if i != j)
    return Q


def generator_statistics(Q, order, probes):
    hidden = list(range(1, Q.rows - 1))
    retained = [0, Q.rows - 1]
    II = Q.extract(hidden, hidden)
    RI = Q.extract(retained, hidden)
    IR = Q.extract(hidden, retained)
    RR = Q.extract(retained, retained)
    G = (-II).inv()
    m = G * sp.ones(len(hidden), 1)
    K = RR + RI * G * IR
    alpha = sp.ones(2, 1) + RI * m
    killed = Q[:-1, :-1]
    N = (-killed).inv()
    mu = sp.zeros(1, N.rows)
    mu[0, 0] = 1
    occupations = mu * N
    V = 2 * sum(occupations[0, i + 1] * m[i, 0]
                for i in range(len(hidden)))
    moments = []
    vector = sp.ones(N.rows, 1)
    for k in range(1, order + 1):
        vector = N * vector
        moments.append(sp.factorial(k) * (mu * vector)[0])
    kernel_probes = []
    for shift, multiplicity in probes:
        resolvent = (rat(shift) * sp.eye(II.rows) - II).inv()
        for k in range(multiplicity):
            derivative = (-1)**k * sp.factorial(k) * RI * resolvent**(k + 1) * IR
            kernel_probes.append((str(shift), k, derivative))
    return K, alpha, V, moments, kernel_probes


def survival(nodes, weights, q, t):
    # Exact analytic law of Exp(1) plus either zero or Exp(mean=x).
    t = mp.mpf(t)
    fast = mp.exp(-t)
    answer = (1 - mpr(q)) * fast
    for x, w in zip(nodes, weights):
        xx = mpr(x)
        answer += mpr(q * w) * (xx * mp.exp(-t / xx) - fast) / (xx - 1)
    return answer


def certified_decade(bound):
    """Largest integer k for which a positive rational bound is strictly >10^k."""
    k = math.floor((bound.numerator.bit_length() - bound.denominator.bit_length())
                   * math.log10(2))
    while bound <= F(10) ** k:
        k -= 1
    while bound > F(10) ** (k + 1):
        k += 1
    assert bound > F(10) ** k
    return k


def serialize_matrix(matrix):
    return [[str(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def run_case(name, order, probes, deadline, semigroup_check=False, slow_mean=None):
    start = time.perf_counter()
    bounded_rates = slow_mean is not None
    slow_mean = deadline if slow_mean is None else slow_mean
    n, _, epsilon, c, x0, w0, x1, w1 = construct(order, probes, slow_mean)
    q = F(1, deadline**3)
    Q0 = make_generator(x0, w0, q)
    Q1 = make_generator(x1, w1, q)
    assert Q0.shape == Q1.shape
    stats0 = generator_statistics(Q0, order, probes)
    stats1 = generator_statistics(Q1, order, probes)
    assert stats0 == stats1
    K, alpha, V, moments, kernel_probes = stats0
    assert K == sp.Matrix([[-1, 1], [0, 0]])
    mean = moments[0]
    assert mean == alpha[0]
    Vformula = 2 * q * sum(w * x*x for x, w in zip(x0, w0))
    assert V == rat(Vformula)
    # Check excursion moments directly as well as through full-generator moments.
    for k in range(order + 1):
        assert sum(w * x**k for x, w in zip(x0, w0)) == sum(w * x**k for x, w in zip(x1, w1))
    for shift, multiplicity in probes:
        for k in range(multiplicity):
            left = sum(w * x**k / (1 + shift*x)**(k + 1) for x, w in zip(x0, w0))
            right = sum(w * x**k / (1 + shift*x)**(k + 1) for x, w in zip(x1, w1))
            assert left == right
    s0 = survival(x0, w0, q, deadline)
    s1 = survival(x1, w1, q, deadline)
    if bounded_rates:
        exponent = F(deadline) * (F(1, n + 1) - F(1, slow_mean))
        bound = q * epsilon * F(2) ** math.floor(exponent) / 3
        bound_formula = 'q*epsilon*2**floor(t*(1/(n+1)-1/slow_mean))/3'
    else:
        bound = q * epsilon * F(2) ** (deadline // (n + 1)) / 9
        bound_formula = 'q*epsilon*2**floor(M/(n+1))/9'
    assert s1 / s0 > mpr(bound)
    semigroup_relative = None
    if semigroup_check:
        errors = []
        for Q, nodes, weights in [(Q0, x0, w0), (Q1, x1, w1)]:
            A = mp.matrix([[mpr(F(Q[i, j])) for j in range(Q.rows - 1)]
                           for i in range(Q.rows - 1)])
            value = sum(mp.expm(deadline * A)[0, j] for j in range(A.cols))
            closed = survival(nodes, weights, q, deadline)
            relative = abs(value / closed - 1)
            assert relative < mp.mpf('1e-70')
            errors.append(mp.nstr(relative, 8))
        semigroup_relative = errors
    max_bits = max(max(F(a).numerator.bit_length(), F(a).denominator.bit_length())
                   for Q in (Q0, Q1) for a in Q)
    return {
        'name': name,
        'status': 'PASS_EXACT_RATIONAL_EQUALITIES',
        'order': order,
        'probes': [{'s': str(s), 'derivative_orders': list(range(m))} for s, m in probes],
        'fast_distinct_phases': n,
        'states_each_chain': Q0.rows,
        'deadline': deadline,
        'slow_mean': slow_mean,
        'bounded_rate_corollary': bounded_rates,
        'q': str(q), 'epsilon': str(epsilon),
        'slow_branch_probability': str(q * epsilon),
        'interpolation_weights': [str(v) for v in c],
        'baseline': {'means': [str(x) for x in x0], 'weights': [str(w) for w in w0], 'Q': serialize_matrix(Q0)},
        'alternative': {'means': [str(x) for x in x1], 'weights': [str(w) for w in w1], 'Q': serialize_matrix(Q1)},
        'K': serialize_matrix(K), 'alpha': serialize_matrix(alpha),
        'V': str(V), 'mean_T': str(mean),
        'normalized_W2_bound': mp.nstr(mp.sqrt(mpr(F(V))) / mpr(F(mean)), 14),
        'matched_T_moments': [str(v) for v in moments],
        'matched_kernel_probes': [{'s': s, 'derivative': k, 'matrix': serialize_matrix(v)} for s, k, v in kernel_probes],
        'survival_baseline': mp.nstr(s0, 18),
        'survival_alternative': mp.nstr(s1, 18),
        'log10_survival_ratio': mp.nstr(mp.log10(s1 / s0), 16),
        'certified_ratio_gt_10_power': certified_decade(bound),
        'ratio_bound_formula': bound_formula,
        'max_input_rational_bits': max_bits,
        'semigroup_relative_errors_90dps': semigroup_relative,
        'check_seconds': time.perf_counter() - start,
    }


def main():
    configs = [
        ('moments_2_M100', 2, [], 100, True),
        ('moments_2_M1000', 2, [], 1000, False),
        ('moments_2_M10000', 2, [], 10000, False),
        ('moments_4_fixed_probes_M1000', 4, [(F(1, 7), 2), (F(2), 1)], 1000, False),
        ('moments_4_fixed_probes_M10000', 4, [(F(1, 7), 2), (F(2), 1)], 10000, False),
        ('moments_6_moving_probes_M1000', 6, [(F(1, 1000), 2), (F(1, 1000000), 1), (F(2), 1)], 1000, False),
        ('moments_6_moving_probes_M10000', 6, [(F(1, 10000), 2), (F(1, 100000000), 1), (F(2), 1)], 10000, False),
        ('moments_8_fixed_probes_M10000', 8, [(F(1, 5), 2), (F(3), 2)], 10000, False),
        ('moments_2_rates_in_one_eighth_to_one_t1000', 2, [], 1000, False, 8),
    ]
    cases = [run_case(*config) for config in configs]
    result = {
        'status': 'ALL_NINE_EXACT_CASES_PASSED',
        'claim_scope': 'Finite replay validates fixtures; the general result is the proof in REPORT.md.',
        'python': sys.version, 'platform': platform.platform(),
        'sympy': sp.__version__, 'mpmath': mp.__version__, 'mpmath_dps': mp.mp.dps,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'cases': cases,
    }
    (HERE / 'REPLAY.json').write_text(json.dumps(result, indent=2) + '\n')
    for case in cases:
        print(f"{case['name']}: exact PASS; W2/mean <= {case['normalized_W2_bound']}; "
              f"log10 tail ratio = {case['log10_survival_ratio']}; "
              f"rationally certified ratio > 10^{case['certified_ratio_gt_10_power']}")


if __name__ == '__main__':
    main()
