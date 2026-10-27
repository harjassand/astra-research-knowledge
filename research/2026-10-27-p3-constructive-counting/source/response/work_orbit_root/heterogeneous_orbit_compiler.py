#!/usr/bin/env python3
"""Unequal block sizes and acquired rank-budget allocation.

Orbit profiles are not inputs. A dynamic program allocates centers among
block dimensions. Exact finite validators only; no asymptotic phase backend.
"""
from itertools import combinations
from pathlib import Path
import json
import random

from orbit_phase_compiler import (rank, multiply, transpose, general_linear,
    local_medians, congruence, symmetric, off_diagonal, edge_count, independent,
    centroid_blocks, radical, substitute, compose, indices, phase, apply,
    random_invertible, matrix_polynomial, quadratic_matrix, truth_sum,
    exact_reconstruct)


def offsets(sizes):
    result = [0]
    for size in sizes:
        result.append(result[-1]+size)
    return result


def distance(X, Y, sizes, starts):
    difference = [x ^ y for x, y in zip(X, Y)]
    return sum(rank([(v >> starts[j]) & ((1 << size)-1) for v in difference])
               for j, size in enumerate(sizes))


def orbit(X, Y, sizes, starts, group=None):
    d = len(X)
    best = None
    for G in group if group is not None else general_linear(d):
        val = distance(multiply(G, X), Y, sizes, starts)
        if best is None or (val, tuple(G)) < best:
            best = val, tuple(G)
    return best


def scalar_round(B, classes):
    n = len(B)
    C = [0]*n
    K = [0]*len(classes)
    for i, A in enumerate(classes):
        for j in range(i, len(classes)):
            T = classes[j]
            ones = sum((B[a] >> t) & 1 for a in A for t in T)
            if 2*ones > len(A)*len(T):
                K[i] |= 1 << j
                K[j] |= 1 << i
                for a in A:
                    for t in T:
                        C[a] |= 1 << t
                        C[t] |= 1 << a
    return C, K


def acquire_budget(B, sizes, budget):
    n = len(B)
    if (n <= 0 or not sizes or any(d <= 0 for d in sizes) or sum(sizes) != n
            or any(v < 0 or v >= (1 << n) for v in B) or not symmetric(B)
            or any(v >> i & 1 for i, v in enumerate(B))):
        raise ValueError('Require an alternating matrix with a valid block partition.')
    dimensions = sorted(set(sizes))
    if not sum(dimensions) <= budget <= n:
        raise ValueError('Budget must permit at least one center per occurring dimension.')
    starts = offsets(sizes)
    by_size = {d: [a for a, z in enumerate(sizes) if z == d] for d in dimensions}
    choices = {}
    alignments = {}
    for d in dimensions:
        ids = by_size[d]
        N = len(ids)
        group = list(general_linear(d)) if d <= 3 and N > 1 else None
        distances = [[0]*N for _ in range(N)]
        aligning = [[None]*N for _ in range(N)]
        for i, a in enumerate(ids):
            X = B[starts[a]:starts[a+1]]
            for j, t in enumerate(ids):
                if i == j:
                    aligning[i][j] = tuple(1 << u for u in range(d))
                else:
                    value, G = orbit(X, B[starts[t]:starts[t+1]], sizes, starts, group)
                    distances[i][j] = value
                    aligning[i][j] = G
        assert all(distances[i][j] == distances[j][i]
                   for i in range(N) for j in range(N))
        choices[d] = {c: local_medians(distances, c) for c in range(1, N+1)}
        alignments[d] = aligning
    states = {0: (0, {})}
    for d in dimensions:
        new = {}
        for previous_rank, (previous_cost, profile) in states.items():
            for c, medians in choices[d].items():
                weight = previous_rank+d*c
                if weight > budget:
                    continue
                candidate = (previous_cost+medians['objective'], dict(profile, **{str(d): c}))
                if weight not in new or candidate[0] < new[weight][0]:
                    new[weight] = candidate
        states = new
    selected_weight = min(states, key=lambda r: (states[r][0], r))
    objective, string_profile = states[selected_weight]
    profile = {int(d): c for d, c in string_profile.items()}
    gauges = [None]*len(sizes)
    centers = [None]*len(sizes)
    scalar_classes = []
    chosen_classes = []
    histories = {}
    for d in dimensions:
        ids = by_size[d]
        medians = choices[d][profile[d]]
        histories[d] = medians['history']
        for i, a in enumerate(ids):
            j = medians['assignments'][i]
            centers[a] = ids[j]
            gauges[a] = alignments[d][i][j]
        for local_class in medians['classes']:
            A = [ids[j] for j in local_class]
            chosen_classes.append(A)
            scalar_classes.extend([[starts[a]+u for a in A] for u in range(d)])
    G = [row << starts[a] for a, gauge in enumerate(gauges) for row in gauge]
    Bp = congruence(B, G)
    GT = transpose(G)
    X = []
    for a, t in enumerate(centers):
        assert sizes[a] == sizes[t]
        X.extend(multiply(B[starts[t]:starts[t+1]], GT))
    actual_cost = sum(distance(Bp[starts[a]:starts[a+1]], X[starts[a]:starts[a+1]],
                               sizes, starts) for a in range(len(sizes)))
    bit_cost = sum((a ^ b).bit_count() for a, b in zip(Bp, X))
    assert actual_cost == objective and bit_cost <= max(sizes)**2*objective
    C, K = scalar_round(Bp, scalar_classes)
    directed = sum((a ^ b).bit_count() for a, b in zip(Bp, C))
    assert directed <= 3*bit_cost
    S = [a ^ b for a, b in zip(Bp, off_diagonal(C))]
    U = [sum(1 << a for a in A) for A in scalar_classes]
    assert multiply(multiply(transpose(U, n), K), U) == C
    assert symmetric(C) and symmetric(S)
    assert rank(C) <= len(U) <= selected_weight <= budget
    return dict(block_sizes=list(sizes), requested_rank_budget=budget,
                acquired_profile=profile, selected_profile_weight=selected_weight,
                scalar_classes=scalar_classes, block_classes=chosen_classes,
                objective=objective, objective_histories=histories,
                profile_costs={str(d): {str(c): rec['objective'] for c, rec in options.items()}
                               for d, options in choices.items()},
                gauge_rows=G, gauges=[list(g) for g in gauges],
                transformed_matrix=Bp, low_rank_matrix=C, sparse_matrix=S,
                quotient=K, code_generators=U, retained=list(range(n)), removed=[],
                low_rank=rank(C), rank_budget=len(U), residual_edges=edge_count(S),
                row_bit_cost=bit_cost, directed_rounding_cost=directed)


def acquire_raw(poly, n, budget):
    if n <= 0 or any(t < 0 or t >= (1 << n) or t.bit_count() > 3 for t in poly):
        raise ValueError('Require a nonempty cubic Boolean ANF.')
    if radical(poly, n):
        raise ValueError('The third tensor must have zero radical.')
    blocks, metadata = centroid_blocks(poly, n)
    sizes = list(map(len, blocks))
    V = [v for block in blocks for v in block]
    p = substitute(poly, n, V)
    starts = offsets(sizes)
    owner = {i: a for a in range(len(sizes)) for i in range(starts[a], starts[a+1])}
    assert all(t.bit_count() < 3 or len({owner[i] for i in indices(t)}) == 1 for t in p)
    rec = acquire_budget(quadratic_matrix(p, n), sizes, budget)
    final = substitute(p, n, rec['gauge_rows'])
    foreground = final ^ matrix_polynomial(rec['transformed_matrix'])
    assert all(len({owner[i] for i in indices(t)}) <= 1 for t in foreground)
    rec.update(original_variables=n, raw_polynomial=sorted(poly),
               raw_cubic_terms=sum(t.bit_count() == 3 for t in poly),
               centroid_columns=V, centroid=metadata,
               full_coordinate_columns=compose(V, rec['gauge_rows']),
               final_polynomial=sorted(final), foreground_polynomial=sorted(foreground),
               foreground_terms=len(foreground-{0}))
    return rec


def test():
    rng = random.Random(2026102711)
    matrix_cases = []
    for sizes, budget in [([1, 2, 1, 2], 3), ([2, 3, 2, 3], 5),
                          ([1, 1, 2, 2, 3], 6), ([3, 3, 3, 6], 9)]:
        n = sum(sizes)
        B = [0]*n
        for i, j in combinations(range(n), 2):
            if rng.randrange(2):
                B[i] |= 1 << j
                B[j] |= 1 << i
        got = acquire_budget(B, sizes, budget)
        possibilities = [(0, 0)]
        for d_text, options in got['profile_costs'].items():
            d = int(d_text)
            possibilities = [(r+d*int(c), z+cost) for r, z in possibilities
                             for c, cost in options.items() if r+d*int(c) <= budget]
        assert got['objective'] == min(z for r, z in possibilities)
        matrix_cases.append({k: got[k] for k in ['block_sizes', 'requested_rank_budget',
                            'acquired_profile', 'objective', 'low_rank', 'residual_edges']})
    indecomposable5 = {7, (1 << 0) | (1 << 3) | (1 << 4)}
    indecomposable6 = {(1 << 0) | (1 << 1) | (1 << 5),
                      (1 << 0) | (1 << 2) | (1 << 4),
                      (1 << 1) | (1 << 2) | (1 << 3)}
    raw_cases = []
    pointwise = 0
    for sizes, polys, budget in [([3, 3, 5], [{7}, {7}, indecomposable5], 8),
                                 ([3, 3, 6], [{7}, {7}, indecomposable6], 9)]:
        n = sum(sizes)
        starts = offsets(sizes)
        base = {t << starts[a] for a, local in enumerate(polys) for t in local}
        for i, j in combinations(range(n), 2):
            if rng.randrange(2):
                base.symmetric_difference_update({(1 << i) | (1 << j)})
        V = random_invertible(n, rng)
        raw = substitute(base, n, V, rng.randrange(1 << n))
        got = acquire_raw(raw, n, budget)
        assert sorted(got['block_sizes']) == sorted(sizes)
        final = set(got['final_polynomial'])
        for y in range(1 << n):
            assert phase(raw, apply(got['full_coordinate_columns'], y)) == phase(final, y)
            pointwise += 1
        value, stats = exact_reconstruct(got)
        assert value == truth_sum(raw, n) == truth_sum(base, n) == truth_sum(final, n)
        got.update(exact_phase_sum=value, reconstruction_stats=stats)
        raw_cases.append(got)
    return dict(status='all exact assertions passed', matrix_fixtures=matrix_cases,
                full_polynomial_pointwise_checks=pointwise,
                exact_raw_mixed_block_reconstructions=len(raw_cases), raw_fixtures=raw_cases,
                asymptotic_phase_engine_executed=False)


if __name__ == '__main__':
    out = test()
    Path(__file__).with_name('heterogeneous_orbit_results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'raw_fixtures'}, indent=2))
    for r in out['raw_fixtures']:
        print(json.dumps({k: r[k] for k in ['original_variables', 'block_sizes', 'acquired_profile',
                          'low_rank', 'residual_edges', 'exact_phase_sum']}))
