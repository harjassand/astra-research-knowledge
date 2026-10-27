#!/usr/bin/env python3
"""Generic top-polar block acquisition and degree-four orbit reconstruction.

This is an extension validator. It reuses the root's exact finite
reconstruction, not its unimplemented asymptotic phase engine. The multilinear
centroid and clustering ingredients are established prior machinery.
"""
from itertools import combinations
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_dense_cont'))
sys.path.insert(0, str(ROOT / 'work_orbit_root'))
from cubic_structure_compiler import (nullspace, independent, compose, mat_xor,
    flat, unflat, xor_all, indices, substitute, random_invertible, phase,
    apply, brute)
from orbit_phase_compiler import (acquire_orbits, quadratic_matrix,
    matrix_polynomial, exact_reconstruct, matrix_from_edges, off_diagonal,
    rank, block_at)


def top_contractions(poly, n, degree):
    top = {term for term in poly if term.bit_count() == degree}
    rows = {}
    for tail in combinations(range(n), degree-1):
        mask = sum(1 << i for i in tail)
        rows[mask] = sum(1 << j for j in range(n)
                         if not (mask >> j & 1) and (mask | (1 << j)) in top)
    return rows


def top_polar_blocks(poly, n, degree):
    if degree < 3 or any(t.bit_count() > degree for t in poly):
        raise ValueError('Require a degree-at-most-d ANF with d >= 3.')
    contraction = top_contractions(poly, n, degree)
    if nullspace(contraction.values(), n):
        raise ValueError('Top derivative has nonzero radical.')
    constraints = []
    for tail in combinations(range(n), degree-2):
        tail_mask = sum(1 << k for k in tail)
        for i in range(n):
            for j in range(n):
                left = 0 if tail_mask >> j & 1 else contraction[tail_mask | (1 << j)]
                right = 0 if tail_mask >> i & 1 else contraction[tail_mask | (1 << i)]
                constraints.append((left << (n*i)) ^ (right << (n*j)))
    center = nullspace(constraints, n*n)
    matrices = [unflat(vector, n) for vector in center]
    assert all(compose(A, B) == compose(B, A)
               for A in matrices for B in matrices)
    frobenius_minus_identity = [flat(mat_xor(compose(A, A), A), n)
                               for A in matrices]
    equations = [0]*(n*n)
    for j, vector in enumerate(frobenius_minus_identity):
        for i in indices(vector):
            equations[i] ^= 1 << j
    idempotent_coefficients = nullspace(equations, len(center))
    idempotents = [unflat(xor_all(center[j] for j in indices(v)), n)
                   for v in idempotent_coefficients]
    projectors = [[1 << i for i in range(n)]]
    for A in idempotents:
        assert compose(A, A) == A
        refined = []
        for P in projectors:
            PA = compose(P, A)
            PB = mat_xor(P, PA)
            if any(PA):
                refined.append(PA)
            if any(PB):
                refined.append(PB)
        projectors = refined
    blocks = [independent(P) for P in projectors]
    assert len(blocks) == len(idempotents)
    assert sum(map(len, blocks)) == n
    return blocks, dict(degree=degree, centroid_equations=len(constraints),
                        centroid_dimension=len(center),
                        primitive_blocks=len(blocks))


def acquire_fixed_degree(poly, n, degree, c, execute_orbits=True):
    blocks, metadata = top_polar_blocks(poly, n, degree)
    sizes = list(map(len, blocks))
    if len(set(sizes)) != 1:
        raise ValueError('Finite orbit backend here uses uniform blocks.')
    b = sizes[0]
    columns = [v for block in blocks for v in block]
    acquired = substitute(poly, n, columns)
    if any(t.bit_count() >= 3 and len({i//b for i in indices(t)}) > 1
           for t in acquired):
        raise ValueError('A lower-degree nonlinear term crosses primitive blocks.')
    if not execute_orbits:
        return dict(block_sizes=sizes, full_coordinate_columns=columns,
                    final_polynomial=sorted(acquired), centroid=metadata)
    B = quadratic_matrix(acquired, n)
    record = acquire_orbits(B, b, c)
    final = substitute(acquired, n, record['gauge_rows'])
    foreground = final ^ matrix_polynomial(record['transformed_matrix'])
    assert all(len({i//b for i in indices(t)}) <= 1 for t in foreground)
    record.update(block_sizes=sizes, centroid=metadata,
                  full_coordinate_columns=compose(columns, record['gauge_rows']),
                  final_polynomial=sorted(final),
                  foreground_polynomial=sorted(foreground))
    return record


def fixture(blocks, degree, c, errors, rng):
    n = blocks*degree
    labels = [i % c for i in range(blocks)]
    latent = degree*c
    K = [0]*latent
    for i in range(latent):
        for j in range(i, latent):
            if rng.randrange(2):
                K[i] |= 1 << j
                K[j] |= 1 << i
    D = [sum(((K[labels[a]*degree+u] >> (labels[z]*degree+v)) & 1)
             << (z*degree+v) for z in range(blocks) for v in range(degree))
         for a in range(blocks) for u in range(degree)]
    possibilities = [(i, j) for i in range(n) for j in range(i+1, n)
                     if i//degree != j//degree]
    S = matrix_from_edges(n, rng.sample(possibilities, errors))
    B = [x ^ y for x, y in zip(off_diagonal(D), S)]
    poly = matrix_polynomial(B)
    poly.symmetric_difference_update({((1 << degree)-1) << (a*degree)
                                       for a in range(blocks)})
    for a in range(blocks):
        for support in range(1, 1 << degree):
            if support.bit_count() < degree and rng.randrange(3) == 0:
                poly.symmetric_difference_update({support << (a*degree)})
    if rng.randrange(2):
        poly.symmetric_difference_update({0})
    hidden = random_invertible(n, rng)
    offset = rng.randrange(1 << n)
    raw = substitute(poly, n, hidden, offset)
    E = sum(rank(block_at(S, a, j, degree))
            for a in range(blocks) for j in range(a+1, blocks))
    return dict(n=n, degree=degree, c=c, errors=errors, E=E,
                base=poly, raw=raw, hidden=hidden, offset=offset)


def run_checks():
    rng = random.Random(2026102715)
    records = []
    pointwise = 0
    for blocks, degree, c, errors, use_orbit in [
            (2, 4, 1, 0, True), (2, 4, 1, 3, True),
            (3, 4, 1, 5, True), (2, 5, 1, 2, False),
            (2, 6, 1, 3, False)]:
        data = fixture(blocks, degree, c, errors, rng)
        n = data['n']
        rec = acquire_fixed_degree(data['raw'], n, degree, c, use_orbit)
        assert rec['block_sizes'] == [degree]*blocks
        transformed = set(rec['final_polynomial'])
        for y in range(1 << n):
            assert phase(data['raw'], apply(rec['full_coordinate_columns'], y)) == phase(transformed, y)
            pointwise += 1
        value = brute(data['raw'], n)
        assert value == brute(data['base'], n) == brute(transformed, n)
        summary = dict(n=n, degree=degree, input_terms=len(data['raw']),
                       block_sizes=rec['block_sizes'], exact_phase_sum=value,
                       centroid=rec['centroid'], orbit_backend_executed=use_orbit)
        if use_orbit:
            assert rec['objective'] <= 10*(2*data['E']+n)
            assert rec['residual_edges'] <= 15*degree*degree*(2*data['E']+n)
            reconstructed, statistics = exact_reconstruct(rec)
            assert reconstructed == value
            summary.update(rank_budget=rec['rank_budget'],
                           residual_edges=rec['residual_edges'],
                           reconstruction=statistics)
        records.append(summary)
        print(json.dumps(summary), flush=True)
    # The high-degree block promise must be checked, not inferred from top degree.
    negative = fixture(2, 4, 1, 0, rng)
    bad_base = negative['base'] ^ {(1 << 0) | (1 << 1) | (1 << 4)}
    bad_raw = substitute(bad_base, 8, negative['hidden'], negative['offset'])
    rejected = False
    try:
        acquire_fixed_degree(bad_raw, 8, 4, 1, False)
    except ValueError as error:
        rejected = 'crosses primitive blocks' in str(error)
    assert rejected
    return dict(status='all exact assertions passed', fixtures=len(records),
                exact_pointwise_identities=pointwise,
                complete_orbit_reconstructions=sum(r['orbit_backend_executed'] for r in records),
                crossed_lower_degree_negative_rejected=rejected,
                asymptotic_phase_engine_executed=False,
                practical_speed_claim=False, records=records)


if __name__ == '__main__':
    result = run_checks()
    Path(__file__).with_name('fixed_degree_orbit_results.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'records'}, indent=2))
