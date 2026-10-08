#!/usr/bin/env python3
"""Exact scoped fixtures for the independently reconstructed gap lemma.

No spectral claims are inferred from floating-point diagonalization. The sharp
fixture checks an exact local covariance witness and resampling eigenfunction;
the upper bound and exact-gap inference are supplied by INDEPENDENT_PROOF.md.
"""

from collections import defaultdict, deque
from fractions import Fraction as F
from pathlib import Path
import json


def pair_from_product_channels(seed_law, channel):
    pair = defaultdict(F)
    marginal = defaultdict(F)
    for seed, weight in seed_law.items():
        outputs = {q: p for q, p in channel(seed).items() if p}
        assert sum(outputs.values()) == 1
        for q, p in outputs.items():
            marginal[q] += weight * p
            for r, t in outputs.items():
                pair[q, r] += weight * p * t
    assert sum(pair.values()) == 1
    return dict(pair), dict(marginal)


def support_components(pair):
    graph = defaultdict(set)
    for (q, r), weight in pair.items():
        if weight:
            a, b = (0, q), (1, r)
            graph[a].add(b)
            graph[b].add(a)
    pending = set(graph)
    count = 0
    while pending:
        count += 1
        seen = {next(iter(pending))}
        queue = deque(seen)
        while queue:
            for neighbor in graph[queue.popleft()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        pending.difference_update(seen)
    return count


def witness_statistics(pair, marginal, g):
    mean = sum(weight * g[q] for q, weight in marginal.items())
    assert mean == 0
    var = sum(weight * g[q] ** 2 for q, weight in marginal.items())
    cov = sum(weight * g[q] * g[r] for (q, r), weight in pair.items())
    assert var > 0
    return var, cov, cov / var


def sign_law(rho):
    return {(x, y): (1 + rho * x * y) / 4
            for x in (-1, 1) for y in (-1, 1)}


def branch_channel(eta):
    def channel(seed):
        x, y = seed
        return {('A', x): eta, ('B', y): eta,
                ('F', x, y): 1 - 2 * eta}
    return channel


def sharp_fixture(name, rho, eta):
    seed_law = sign_law(rho)
    channel = branch_channel(eta)
    pair, marginal = pair_from_product_channels(seed_law, channel)
    g_num = defaultdict(F)
    for seed, weight in seed_law.items():
        f = sum(seed)
        for q, p in channel(seed).items():
            if p:
                g_num[q] += weight * p * f
    g = {q: g_num[q] / weight for q, weight in marginal.items()}
    var, cov, witness_corr = witness_statistics(pair, marginal, g)
    expected = 1 - eta * (1 - rho)
    assert witness_corr == expected
    cond_partner = defaultdict(F)
    for (q, r), weight in pair.items():
        cond_partner[q] += weight * g[r]
    assert all(cond_partner[q] / marginal[q] == expected * g[q]
               for q in marginal)
    eigenvalue = (1 + expected) / 2
    for q, r in pair:
        h = g[q] + g[r]
        eq0 = g[q] + cond_partner[q] / marginal[q]
        eq1 = g[r] + cond_partner[r] / marginal[r]
        assert (eq0 + eq1) / 2 == eigenvalue * h
    assert support_components(pair) == 1
    return {
        'name': name,
        'rho': str(rho), 'eta': str(eta),
        'witness_variance': str(var), 'witness_covariance': str(cov),
        'witness_correlation': str(witness_corr),
        'resampling_eigenvalue': str(eigenvalue),
        'gap_from_general_bound_and_eigenvalue': str(1 - eigenvalue),
        'support_components': 1,
        'status': 'exact fixture passed'
    }


def common_register_failure():
    seed_law = {(x, y, r): F(1, 8) for x in (-1, 1)
                for y in (-1, 1) for r in (-1, 1)}
    eta = F(1, 9)
    def channel(seed):
        x, y, r = seed
        return {('A', x, r): eta, ('B', y, r): eta,
                ('F', x, y, r): 1 - 2 * eta}
    pair, marginal = pair_from_product_channels(seed_law, channel)
    g = {q: F(q[-1]) for q in marginal}
    var, cov, corr = witness_statistics(pair, marginal, g)
    assert (var, cov, corr) == (1, 1, 1)
    assert support_components(pair) == 2
    return {'name': 'forbidden extra shared register on clear branches',
            'witness_correlation': str(corr),
            'support_components': 2, 'removed_premise': 'clear-view restriction',
            'status': 'exact counterexample to dropping premise'}


def selector_failure():
    def channel(seed):
        x, y = seed
        return {('A', x) if x == 1 else ('B', y): F(1)}
    pair, marginal = pair_from_product_channels(sign_law(F(0)), channel)
    g = {q: F(1 if q[0] == 'A' else -1) for q in marginal}
    _, _, corr = witness_statistics(pair, marginal, g)
    assert corr == 1
    mass_a = sum(p for q, p in marginal.items() if q[0] == 'A')
    assert mass_a == F(1, 2)
    return {'name': 'seed-dependent selectors reveal base X in the tag',
            'input_rho': '0', 'A_branch_mass': str(mass_a),
            'B_branch_mass': str(1 - mass_a),
            'witness_correlation': str(corr),
            'removed_premise': 'selector independent of S',
            'status': 'exact counterexample to dropping premise'}


def postselection_failure():
    # Independent signs conditioned on X=Y have this exact conditional law.
    seed_law = {(-1, -1): F(1, 2), (1, 1): F(1, 2)}
    pair, marginal = pair_from_product_channels(seed_law, branch_channel(F(1, 9)))
    g = {q: F(q[1]) for q in marginal}
    _, _, corr = witness_statistics(pair, marginal, g)
    assert corr == 1
    return {'name': 'success event X=Y changes an initially independent law',
            'original_input_rho': '0', 'conditional_input_rho': '1',
            'success_probability': '1/2', 'output_witness_correlation': str(corr),
            'status': 'exact postselection warning fixture'}


def pairwise_independence_failure():
    seed_law = {(x, y, u, u ^ x ^ y): F(1, 8)
                for x in (0, 1) for y in (0, 1) for u in (0, 1)}
    for x in (0, 1):
        for y in (0, 1):
            for bit in (0, 1):
                assert sum(p for (a, b, u, v), p in seed_law.items()
                           if a == x and b == y and u == bit) == F(1, 8)
                assert sum(p for (a, b, u, v), p in seed_law.items()
                           if a == x and b == y and v == bit) == F(1, 8)
    for u in (0, 1):
        for v in (0, 1):
            assert sum(p for (a, b, c, d), p in seed_law.items()
                       if c == u and d == v) == F(1, 4)
    eta = F(1, 9)
    def channel(seed):
        x, y, u, v = seed
        return {('A', x, u): eta, ('B', y, v): eta,
                ('F', x, y, u, v): 1 - 2 * eta}
    pair, marginal = pair_from_product_channels(seed_law, channel)
    g = {q: F(1 - 2 * (q[1] ^ (q[3] if q[0] == 'F' else q[2])))
         for q in marginal}
    _, _, corr = witness_statistics(pair, marginal, g)
    assert corr == 1
    return {'name': 'pairwise auxiliary independence hides XOR common bit',
            'input_rho': '0', 'witness_correlation': str(corr),
            'pairwise_objects': ['(X,Y)', 'U', 'V'],
            'mutually_independent': False,
            'removed_premise': 'joint auxiliary marginal factorization',
            'status': 'exact counterexample to weaker independence reading'}


def loose_certificate_failure():
    law = sign_law(F(0))
    bases = [lambda x, y: F(x), lambda x, y: F(y),
             lambda x, y: F(x * y)]
    expected_eigenvalues = [F(1, 2), F(1, 2), F(0)]
    for f, eigenvalue in zip(bases, expected_eigenvalues):
        for x, y in law:
            p_x = sum(p for (a, b), p in law.items() if a == x)
            p_y = sum(p for (a, b), p in law.items() if b == y)
            cx = sum(p * f(a, b) for (a, b), p in law.items() if a == x) / p_x
            cy = sum(p * f(a, b) for (a, b), p in law.items() if b == y) / p_y
            assert (cx + cy) / 2 == eigenvalue * f(x, y)
    actual_gap = 1 - max(expected_eigenvalues)
    loose_rho = F(1, 2)
    false_identity = (1 - loose_rho) / 2
    assert actual_gap == F(1, 2) and false_identity == F(1, 4)
    return {'name': 'upper correlation certificate substituted into equality',
            'actual_rho': '0', 'permitted_upper_certificate': str(loose_rho),
            'actual_gap': str(actual_gap), 'false_formula_value': str(false_identity),
            'status': 'exact counterexample to frozen line 23 equality'}


def main():
    sharp = [sharp_fixture('independent signs, Figure eta', F(0), F(1, 9)),
             sharp_fixture('correlated signs', F(1, 3), F(1, 9)),
             sharp_fixture('eta endpoint, no full branch', F(1, 2), F(1, 2))]
    degenerate = sharp_fixture('constant original pair, auxiliary independent signs',
                               F(0), F(1, 9))
    degenerate.update({'original_pair_gap_by_singleton_convention': '1',
                       'naive_eta_times_original_gap': '1/9',
                       'actual_output_gap': '1/18',
                       'capped_eta_times_min_gap_half': '1/18',
                       'status': 'exact fixture proves cap necessary'})
    # Event denominators of a fixed finite binary seed are powers of two.
    nondyadic = []
    for role_mass in (F(1, 3), F(1, 9)):
        d = role_mass.denominator
        is_power_two = d > 0 and (d & (d - 1)) == 0
        assert not is_power_two
        nondyadic.append({'event_mass': str(role_mass),
                         'reduced_denominator': d, 'is_dyadic': is_power_two})
    old_coefficient = F(2**32, 117649)
    universal_coefficient, t2_coefficient = F(36864), F(24576)
    data = {
        'status': 'all rational fixture assertions passed',
        'scope': 'finite fixtures and arithmetic, not external or formal validation',
        'sharpness': sharp, 'singleton_cap': degenerate,
        'premise_failures': [common_register_failure(), selector_failure(),
                             pairwise_independence_failure(),
                             postselection_failure(), loose_certificate_failure()],
        'CL_label_obstruction': nondyadic,
        'conditional_comparator_arithmetic': {
            'old_coefficient': str(old_coefficient),
            'old_coefficient_decimal': f'{float(old_coefficient):.9f}',
            'universal_coefficient': str(universal_coefficient),
            'universal_relative_increase': str(universal_coefficient / old_coefficient - 1),
            'universal_relative_increase_percent': f'{float(100 * (universal_coefficient / old_coefficient - 1)):.9f}',
            't2_coefficient': str(t2_coefficient),
            't2_relative_copy_reduction': str(1 - t2_coefficient / old_coefficient),
            't2_relative_copy_reduction_percent': f'{float(100 * (1 - t2_coefficient / old_coefficient)):.9f}',
            'premises': 'the old/new sufficient bounds are assumed here, not proved'
        }
    }
    path = Path(__file__).with_name('exact_checks.json')
    path.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({'status': data['status'], 'output': str(path),
                      'sharp_fixture_count': len(sharp),
                      'premise_failure_count': len(data['premise_failures'])}, indent=2))


if __name__ == '__main__':
    main()
