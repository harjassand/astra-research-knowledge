#!/usr/bin/env python3
"""Finite analytic audits; this is not a physical experiment or full sampler.

Uses exact rational arithmetic for finite generator/return/permutation checks.
High-precision decimal calculations are diagnostics of proved inequalities,
not interval-arithmetic replacements for the proofs.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib
import json
import math
import platform
import sys

import mpmath as mp

ROOT = Path(__file__).resolve().parent
mp.mp.dps = 100


def mpf(x):
    return mp.mpf(x.numerator) / x.denominator if isinstance(x, F) else mp.mpf(x)


def out(x, digits=25):
    return mp.nstr(mpf(x), digits)


def weighted_s(q, r):
    """Exact weighted Bernoulli convolution for positive integer rates."""
    pmf = [F(1)]
    for qi, ri in zip(q, r):
        ri = int(ri)
        nxt = [F(0)] * (len(pmf) + ri)
        for j, p in enumerate(pmf):
            nxt[j] += p * qi
            nxt[j + ri] += p * (1 - qi)
        pmf = nxt
    return sum((p / j for j, p in enumerate(pmf) if j), F(0))


def solve(a, b):
    a = [list(row) + [v] for row, v in zip(a, b)]
    n = len(b)
    for col in range(n):
        pivot = next(j for j in range(col, n) if a[j][col])
        a[col], a[pivot] = a[pivot], a[col]
        p = a[col][col]
        a[col] = [v / p for v in a[col]]
        for j in range(n):
            if j != col and a[j][col]:
                z = a[j][col]
                a[j] = [v - z * w for v, w in zip(a[j], a[col])]
    return [row[-1] for row in a]


def mean_by_generator(q, r):
    n = len(q)
    ns = 1 << n
    target = ns - 1
    qmat = [[F(0)] * ns for _ in range(ns)]
    pi = []
    for x in range(ns):
        mass = F(1)
        for i, (qi, ri) in enumerate(zip(q, r)):
            xi = (x >> i) & 1
            mass *= qi if xi else 1 - qi
            rate = ri * ((1 - qi) if xi else qi)
            qmat[x][x ^ (1 << i)] = rate
            qmat[x][x] -= rate
        pi.append(mass)
    amat = [[-qmat[x][y] for y in range(target)] for x in range(target)]
    h = solve(amat, [F(1)] * target)
    return sum((pi[x] * h[x] for x in range(target)), F(0)) / (1 - pi[target])


def homogeneous_s(n, q):
    mass = q ** n
    total = mp.mpf(0)
    for k in range(1, n + 1):
        mass *= (mp.mpf(n - k + 1) / k) * ((1 - q) / q)
        total += mass / k
    return total


def lower_case(n, eps=mp.mpf('0.1'), delta=mp.mpf('0.05')):
    theta = -mp.log(3)
    d = 32 * eps / n
    q0 = mp.mpf(1) / 4
    q1 = 1 / (1 + mp.exp(-theta - d))
    s0, s1 = homogeneous_s(n, q0), homogeneous_s(n, q1)
    p0, p1 = q0 ** n, q1 ** n
    lm0 = mp.log(s0) - mp.log(p0) - mp.log1p(-p0)
    lm1 = mp.log(s1) - mp.log(p1) - mp.log1p(-p1)
    gap = lm0 - lm1
    assert gap >= 4 * eps
    kl = (1 - 2 * delta) * mp.log((1 - delta) / delta)
    bound = n * n * kl / (512 * mp.e * eps * eps)
    return {
        'n': n,
        'epsilon': out(eps),
        'delta': out(delta),
        'logit_shift': out(d),
        'log_mean_separation': out(gap),
        'proved_minimum_log_separation': out(4 * eps),
        'log10_target_probability_at_h0': out(mp.log10(p0)),
        'log10_mean_at_h0': out(lm0 / mp.log(10)),
        'proved_expected_normalized_evidence_lower_bound': out(bound),
    }


def killed_moment(L):
    # States 0,1 are retained; state 2 is the absorbing cemetery.
    p = [[F(3, 4), F(1, 8), F(1, 8)],
         [F(1, 4), F(3, 4), F(0)],
         [F(0), F(0), F(1)]]
    dist = {(0, 0): F(1)}
    for j in range(L):
        nxt = {}
        for (x, count), mass in dist.items():
            count += int(x == 0)
            if j == L - 1:
                nxt[(x, count)] = nxt.get((x, count), F(0)) + mass
            else:
                for y in range(3):
                    if p[x][y]:
                        key = (y, count)
                        nxt[key] = nxt.get(key, F(0)) + mass * p[x][y]
        dist = nxt
    mu = sum((mass * count for (_, count), mass in dist.items()), F(0))
    second = sum((mass * count * count for (_, count), mass in dist.items()), F(0))
    assert second <= 2 * mu * mu - mu
    assert sum(dist.values()) == 1
    return {'L': L, 'mean': out(mu), 'second_moment': out(second),
            'proved_second_moment_bound': out(2 * mu * mu - mu),
            'variance_over_mean_squared': out((second - mu * mu) / (mu * mu)),
            'exact_rational_check': True}


def main():
    results = {
        'scope': 'Analytic and synthetic mathematical audits only; no hardware, no complete experimental service executed.',
        'environment': {'python': sys.version, 'platform': platform.platform(),
                        'mpmath': mp.__version__, 'decimal_precision': mp.mp.dps},
    }

    generator_checks = []
    for n in (2, 3, 4):
        q = [F(i + 1, 2 * n + 3) for i in range(n)]
        r = list(range(1, n + 1))
        p = math.prod(q)
        from_sum = weighted_s(q, r) / (p * (1 - p))
        from_generator = mean_by_generator(q, r)
        assert from_sum == from_generator
        generator_checks.append({'n': n, 'mean': out(from_sum), 'exact_agreement': True})
    results['independent_killed_generator_checks'] = generator_checks

    perm_checks = []
    for n in (2, 4, 6):
        q = [F(i + 2, 2 * (n + 2)) for i in range(n)]
        rates = tuple(range(1, n + 1))
        ss = [(weighted_s(q, perm), perm) for perm in permutations(rates)]
        min_s, min_perm = min(ss)
        max_s, max_perm = max(ss)
        s_sorted = weighted_s(q, rates)
        s_reverse = weighted_s(q, rates[::-1])
        assert max_s == s_sorted and min_s == s_reverse
        perm_checks.append({'n': n, 'assignments_enumerated': math.factorial(n),
                            'maximum_s': out(max_s), 'minimum_s': out(min_s),
                            'maximizing_assignment': max_perm, 'minimizing_assignment': min_perm,
                            'exact_rational_check': True})
    results['all_assignment_checks'] = perm_checks

    large_cases = []
    for n in (16, 64, 256):
        q = [F(1, 8) + F((17 * i) % n, 4 * (n - 1)) for i in range(n)]
        rates = [1] * (n // 2) + [2] * (n - n // 2)
        eta, rho = F(1, 1000), F(1, 200)
        # Deliberately make a near-tied pair and perturb against its true
        # order; the approximate-order audit must include actual mistakes.
        qi_order = sorted(range(n), key=lambda i: q[i])
        q[qi_order[n // 2 - 1]] = F(1, 4) - eta / 4
        q[qi_order[n // 2]] = F(1, 4) + eta / 4
        qhat = [qi + (eta if qi <= F(1, 4) else -eta) for qi in q]
        order_true = sorted(range(n), key=lambda i: q[i])
        order_hat = sorted(range(n), key=lambda i: qhat[i])
        r_true, r_hat_assignment = [0] * n, [0] * n
        for j, i in enumerate(order_true): r_true[i] = rates[j]
        for j, i in enumerate(order_hat): r_hat_assignment[i] = rates[j]
        sbest = weighted_s(q, r_true)
        sselected = weighted_s(q, r_hat_assignment)
        qbar, kappa = F(1, 2), F(2)
        cn = (3 * kappa * kappa * F(n, n + 1) / ((1 - qbar) ** 2)
              + kappa * n * n * qbar ** (n - 1)) / ((1 - qbar ** n) ** 2)
        certified = mp.exp(-2 * (mpf(cn * eta) + mpf(rho)))
        ratio = sselected / sbest
        assert mpf(ratio) >= certified
        assert ratio < 1
        p = math.prod(q)
        large_cases.append({'n': n, 'candidate_assignments': str(math.factorial(n)),
                            'actual_ratio_selected_to_optimal_mean': out(ratio),
                            'proved_ratio_with_probability_and_rate_allowances': out(certified),
                            'log10_global_failure_probability': out(mp.log10(mpf(p))),
                            'q_infinity_allowance': str(eta), 'log_rate_allowance': str(rho),
                            'C_n': out(cn),
                            'components_with_nonoptimal_module': sum(a != b for a, b in zip(r_true, r_hat_assignment)),
                            'actual_assignment_computed_without_path_sampling': True,
                            'data_status': 'admissible deterministic perturbation, not acquired experimental data'})
    results['growing_assignment_family'] = large_cases
    results['prediction_lower_bound_family'] = [lower_case(n) for n in (4, 16, 64, 256, 1024)]
    results['killed_return_moment_checks'] = [killed_moment(L) for L in (1, 2, 8, 32)]

    max_eq, max_path = mp.mpf(0), mp.mpf(0)
    d = mp.mpf('0.8')
    for j in range(-200, 201):
        z = mp.mpf(j) / 2
        q0 = 1 / (1 + mp.exp(-z))
        q1 = 1 / (1 + mp.exp(-z - d))
        kl = q0 * mp.log(q0 / q1) + (1 - q0) * mp.log((1 - q0) / (1 - q1))
        assert kl <= d * d / 8
        max_eq = max(max_eq, kl / (d * d))
        for a, b in ((q0, q1), (1 - q0, 1 - q1)):
            rate = a * mp.log(a / b) - a + b
            assert rate <= mp.e * d * d / 2
            max_path = max(max_path, rate / (d * d))
    results['field_uniform_information_diagnostics'] = {
        'fields': 401, 'range': [-100, 100], 'logit_shift': out(d),
        'maximum_equilibrium_kl_over_shift_squared': out(max_eq),
        'proved_uniform_equilibrium_bound': '1/8',
        'maximum_instantaneous_path_kl_over_shift_squared': out(max_path),
        'proved_uniform_path_bound': out(mp.e / 2),
        'status': 'high-precision grid diagnostic; universal bounds proved analytically'}
    results['all_assertions_passed'] = True
    raw = json.dumps(results, indent=2, sort_keys=True) + '\n'
    (ROOT / 'audit_results.json').write_text(raw)
    receipt = {'script': Path(__file__).name,
               'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'results_sha256': hashlib.sha256(raw.encode()).hexdigest(),
               'all_assertions_passed': True}
    (ROOT / 'execution_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'all_assertions_passed': True,
                      'generator_cases': len(generator_checks),
                      'enumerated_assignments': sum(x['assignments_enumerated'] for x in perm_checks),
                      'growing_family_sizes': [x['n'] for x in large_cases],
                      'forecast_family_sizes': [x['n'] for x in results['prediction_lower_bound_family']],
                      'killed_moment_cases': 4}, indent=2))


if __name__ == '__main__':
    main()
