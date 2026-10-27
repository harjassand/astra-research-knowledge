#!/usr/bin/env python3
"""Acquire hidden cubic blocks, align quadratic response orbits, reconstruct.

Centroid and metric k-median ingredients have prior ancestry. This program
implements their rank-metric interface and exact symmetric rounding, starting
from a raw cubic ANF. Finite sums are exhaustive; the asymptotic local
replacement-form engine is NOT implemented. No practical speed is claimed.
"""
from itertools import combinations, product
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_dense_cont'))
sys.path.insert(0, str(ROOT / 'work_mixed_root'))
from cubic_structure_compiler import (centroid_blocks, radical, substitute,
    random_invertible, compose, apply, indices, phase)
from acquired_block_phase_checks import truth_sum
from mixed_quadratic_compiler import independent, matrix_from_edges, edge_count
from diagonal_completion_compiler import (symmetric, off_diagonal,
    exact_compiled_symmetric)


def rank(A):
    return len(independent(A))


def xor(values):
    z = 0
    for v in values:
        z ^= v
    return z


def multiply(A, B):
    return [xor(B[j] for j in indices(row)) for row in A]


def transpose(A, width=None):
    if width is None:
        width = len(A)
    return [sum(((row >> j) & 1) << i for i, row in enumerate(A))
            for j in range(width)]


def general_linear(b):
    """Streaming enumeration uses polynomial space for variable b."""
    for rows in product(range(1 << b), repeat=b):
        if rank(rows) == b:
            yield tuple(rows)


def block_at(A, a, j, b):
    mask = (1 << b) - 1
    return [(A[a*b+i] >> (j*b)) & mask for i in range(b)]


def row_block(A, a, b):
    return A[a*b:(a+1)*b]


def row_distance(X, Y, b, blocks):
    mask = (1 << b) - 1
    difference = [x ^ y for x, y in zip(X, Y)]
    return sum(rank([(r >> (j*b)) & mask for r in difference])
               for j in range(blocks))


def orbit_distance(X, Y, b, blocks, group=None):
    """Return min_G d(G X,Y), and a minimizing left gauge."""
    best = None
    for G in group if group is not None else general_linear(b):
        value = row_distance(multiply(G, X), Y, b, blocks)
        if best is None or (value, tuple(G)) < best:
            best = (value, tuple(G))
    return best


def local_medians(distances, c):
    N = len(distances)
    if not 1 <= c <= N:
        raise ValueError('The center budget must be between 1 and N.')
    centers = list(range(c))
    sentinel = 1 + max(max(row) for row in distances)
    history = []
    proposed_swaps = 0
    while True:
        nearest = []
        for i in range(N):
            pairs = sorted((distances[i][j], j) for j in centers)
            nearest.append((pairs[0][0], pairs[0][1],
                            pairs[1][0] if len(pairs) > 1 else sentinel))
        value = sum(x[0] for x in nearest)
        history.append(value)
        winner = (value, None, None)
        for old in centers:
            for new in range(N):
                if new in centers:
                    continue
                candidate = sum(min(distances[i][new],
                                    second if assigned == old else first)
                                for i, (first, assigned, second) in enumerate(nearest))
                proposed_swaps += 1
                if candidate < winner[0]:
                    winner = (candidate, old, new)
        if winner[1] is None:
            break
        centers[centers.index(winner[1])] = winner[2]
        centers.sort()
    labels = [min(centers, key=lambda j: (distances[i][j], j))
              for i in range(N)]
    occupied = [j for j in centers if j in labels]
    classes = [[i for i in range(N) if labels[i] == j] for j in occupied]
    return dict(centers=occupied, classes=classes, assignments=labels,
                objective=history[-1], history=history,
                proposed_swaps=proposed_swaps)


def block_gauge_matrix(gauges, b):
    return [row << (a*b) for a, G in enumerate(gauges) for row in G]


def congruence(B, G):
    return multiply(multiply(G, B), transpose(G))


def round_symmetric(B, classes, b):
    """Entry-majority on cluster pairs; retain a free symmetric diagonal."""
    n = len(B)
    C = [0] * n
    quotient = [0] * (b*len(classes))
    for i, A in enumerate(classes):
        for j in range(i, len(classes)):
            T = classes[j]
            for u in range(b):
                for v in range(b):
                    if i == j and v < u:
                        continue
                    ones = sum((B[a*b+u] >> (t*b+v)) & 1 for a in A for t in T)
                    bit = int(2*ones > len(A)*len(T))
                    if bit:
                        quotient[i*b+u] |= 1 << (j*b+v)
                        quotient[j*b+v] |= 1 << (i*b+u)
                        for a in A:
                            for t in T:
                                C[a*b+u] |= 1 << (t*b+v)
                                C[t*b+v] |= 1 << (a*b+u)
    assert symmetric(C) and symmetric(quotient)
    return C, quotient


def acquire_orbits(B, b, c):
    """Raw block-matrix acquisition; no labels, gauges or error witness used."""
    n = len(B)
    if (n <= 0 or b <= 0 or n % b or any(not isinstance(row, int) or row < 0 or row >= (1 << n) for row in B)
            or not symmetric(B) or any(row >> i & 1 for i, row in enumerate(B))):
        raise ValueError('Require an alternating matrix and uniform full blocks.')
    N = n // b
    group = list(general_linear(b)) if b <= 3 else None
    distances = [[0]*N for _ in range(N)]
    aligning = [[None]*N for _ in range(N)]
    for a in range(N):
        for j in range(N):
            value, G = orbit_distance(row_block(B, a, b), row_block(B, j, b),
                                      b, N, group)
            distances[a][j] = value
            aligning[a][j] = G
    assert all(distances[a][j] == distances[j][a]
               for a in range(N) for j in range(N))
    medians = local_medians(distances, c)
    gauges = [aligning[a][medians['assignments'][a]] for a in range(N)]
    G = block_gauge_matrix(gauges, b)
    transformed = congruence(B, G)
    GT = transpose(G)
    approximation = []
    for a in range(N):
        center = medians['assignments'][a]
        approximation.extend(multiply(row_block(B, center, b), GT))
    rank_cost = sum(row_distance(row_block(transformed, a, b),
                                row_block(approximation, a, b), b, N)
                    for a in range(N))
    bit_cost = sum((x ^ y).bit_count() for x, y in zip(transformed, approximation))
    assert rank_cost == medians['objective']
    assert bit_cost <= b*b*rank_cost
    C, quotient = round_symmetric(transformed, medians['classes'], b)
    directed_rounding_cost = sum((x ^ y).bit_count() for x, y in zip(transformed, C))
    assert directed_rounding_cost <= 3*bit_cost
    sparse = [x ^ y for x, y in zip(transformed, off_diagonal(C))]
    assert edge_count(sparse)*2 <= directed_rounding_cost
    assert symmetric(sparse) and rank(C) <= b*len(medians['classes'])
    U = [sum(1 << (a*b+u) for a in A)
         for A in medians['classes'] for u in range(b)]
    assert multiply(multiply(transpose(U, n), quotient), U) == C
    return dict(block_size=b, block_count=N, classes=medians['classes'],
                centers=medians['centers'], objective=rank_cost,
                objective_history=medians['history'], proposed_swaps=medians['proposed_swaps'],
                gauges=[list(g) for g in gauges], gauge_rows=G,
                transformed_matrix=transformed, low_rank_matrix=C, quotient=quotient,
                sparse_matrix=sparse, code_generators=U, retained=list(range(n)), removed=[],
                low_rank=rank(C), rank_budget=b*len(medians['classes']),
                residual_edges=edge_count(sparse), row_bit_cost=bit_cost,
                directed_rounding_cost=directed_rounding_cost)


def quadratic_matrix(poly, n):
    return matrix_from_edges(n, [tuple(indices(t)) for t in poly if t.bit_count() == 2])


def matrix_polynomial(B):
    return {(1 << i) | (1 << j) for i in range(len(B)) for j in range(i+1, len(B))
            if B[i] >> j & 1}


def acquire_raw_cubic(poly, n, c):
    """Read only a raw degree-three ANF and a response-center budget."""
    if n <= 0 or any(not isinstance(t, int) or t < 0 or t.bit_count() > 3 or t >= (1 << n) for t in poly):
        raise ValueError('Require a degree-at-most-three Boolean ANF.')
    if radical(poly, n):
        raise ValueError('This entry point requires a radical-free third tensor.')
    blocks, metadata = centroid_blocks(poly, n)
    sizes = list(map(len, blocks))
    if len(set(sizes)) != 1:
        raise ValueError('This entry point requires uniform primitive block sizes.')
    b = sizes[0]
    columns = [v for block in blocks for v in block]
    acquired = substitute(poly, n, columns)
    assert all(t.bit_count() < 3 or len({i//b for i in indices(t)}) == 1
               for t in acquired)
    B = quadratic_matrix(acquired, n)
    representation = acquire_orbits(B, b, c)
    final = substitute(acquired, n, representation['gauge_rows'])
    foreground = final ^ matrix_polynomial(representation['transformed_matrix'])
    assert all(len({i//b for i in indices(t)}) <= 1 for t in foreground)
    total_columns = compose(columns, representation['gauge_rows'])
    assert len(independent(total_columns)) == n
    representation.update(original_variables=n, raw_polynomial=sorted(poly),
                          raw_cubic_terms=sum(t.bit_count() == 3 for t in poly),
                          centroid_columns=columns, full_coordinate_columns=total_columns,
                          block_sizes=sizes, final_polynomial=sorted(final),
                          foreground_polynomial=sorted(foreground),
                          foreground_terms=len(foreground-{0}), centroid=metadata)
    return representation


def exact_reconstruct(record):
    terms = [(t, 1) for t in record['foreground_polynomial'] if t]
    answer, stats = exact_compiled_symmetric(record['transformed_matrix'], terms, 1, record)
    value = int(answer[0])
    if 0 in record['foreground_polynomial']:
        value = -value
    return value, stats


def hidden_instance(N, c, errors, rng, b=3, affine_disguise=True):
    n = N*b
    labels = [a % c for a in range(N)]
    rng.shuffle(labels)
    latent = b*c
    K = [0]*latent
    for i in range(latent):
        for j in range(i, latent):
            if rng.randrange(2):
                K[i] |= 1 << j
                K[j] |= 1 << i
    D = [sum(((K[labels[a]*b+u] >> (labels[t]*b+v)) & 1) << (t*b+v)
             for t in range(N) for v in range(b)) for a in range(N) for u in range(b)]
    possible = [(i, j) for i in range(n) for j in range(i+1, n) if i//b != j//b]
    chosen = rng.sample(possible, errors)
    S = matrix_from_edges(n, chosen)
    B = [x ^ y for x, y in zip(off_diagonal(D), S)]
    base = matrix_polynomial(B)
    assert b == 3
    base.symmetric_difference_update({7 << (3*a) for a in range(N)})
    for a in range(N):
        for u in range(3):
            if rng.randrange(2):
                base.symmetric_difference_update({1 << (3*a+u)})
    if rng.randrange(2):
        base.symmetric_difference_update({0})
    hidden = random_invertible(n, rng) if affine_disguise else [1 << i for i in range(n)]
    offset = rng.randrange(1 << n) if affine_disguise else 0
    raw = substitute(base, n, hidden, offset)
    E = sum(rank(block_at(S, a, j, b)) for a in range(N) for j in range(a+1, N))
    return dict(raw=raw, base=base, hidden=hidden, offset=offset, labels=labels,
                D=D, S=S, B=B, errors=errors, error_rank_sum=E, n=n, b=b, c=c)


def run_checks():
    rng = random.Random(2026102707)
    records = []
    pointwise = 0
    reconstructed = 0
    for N, c, errors in [(2, 1, 0), (3, 1, 2), (4, 1, 3), (4, 2, 6),
                         (5, 1, 8), (6, 2, 12), (8, 2, 24)]:
        fixture = hidden_instance(N, c, errors, rng)
        rec = acquire_raw_cubic(fixture['raw'], fixture['n'], c)
        n = fixture['n']; b = 3; E = fixture['error_rank_sum']
        assert rec['objective'] <= 10*(2*E+n)
        assert 2*rec['residual_edges'] <= 30*b*b*(2*E+n)
        assert rec['rank_budget'] <= b*c
        final = set(rec['final_polynomial'])
        assignments = range(1 << n) if n <= 12 else [rng.randrange(1 << n) for _ in range(2048)]
        for y in assignments:
            assert phase(fixture['raw'], apply(rec['full_coordinate_columns'], y)) == phase(final, y)
            pointwise += 1
        value = truth_sum(fixture['raw'], n)
        assert value == truth_sum(fixture['base'], n) == truth_sum(final, n)
        rec['exact_phase_sum'] = value
        rec['zero_count'] = ((1 << n)+value)//2
        if n <= 18:
            reconstructed_value, stats = exact_reconstruct(rec)
            assert reconstructed_value == value
            reconstructed += 1
            rec['reconstruction_stats'] = stats
        rec.update(hidden_error_edges=errors, hidden_error_rank_sum=E,
                   hidden_rank=rank(fixture['D']), hidden_types=c,
                   original_error_product=rank(fixture['D'])*errors,
                   original_n_squared=n*n,
                   raw_rank=rank(quadratic_matrix(fixture['raw'], n)),
                   count_backend='exhaustive truth vectors and exact Gaussian-Walsh reconstruction')
        records.append(rec)
    return dict(status='all exact assertions passed', raw_anf_fixtures=len(records),
                full_polynomial_pointwise_checks=pointwise,
                exact_original_hidden_acquired_counts=len(records),
                exact_gaussian_walsh_reconstructions=reconstructed,
                asymptotic_phase_engine_executed=False, practical_speed_claim=False,
                records=records)


if __name__ == '__main__':
    result = run_checks()
    Path(__file__).with_name('orbit_phase_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, indent=2))
    for r in result['records']:
        print(json.dumps({k: r[k] for k in ['original_variables', 'raw_cubic_terms', 'block_sizes',
              'hidden_error_edges', 'hidden_error_rank_sum', 'objective', 'rank_budget',
              'low_rank', 'residual_edges', 'foreground_terms', 'exact_phase_sum']}))
