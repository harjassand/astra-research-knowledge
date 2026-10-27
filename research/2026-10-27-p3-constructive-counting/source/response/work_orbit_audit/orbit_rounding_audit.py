#!/usr/bin/env python3
"""Adversarial exact audit of the actual root orbit compiler.

Finite reconstruction tests use the root's exhaustive backend; no asymptotic
phase engine or practical speed improvement is claimed.
"""
from itertools import combinations, product
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_orbit_root'))
import orbit_phase_compiler as oc


def hamming(a, b):
    return sum((x ^ y).bit_count() for x, y in zip(a, b))


def direct_projection(rows, labels):
    """Independent unrestricted blockconstant majority; symmetry follows."""
    classes = {label: [i for i, v in enumerate(labels) if v == label] for label in set(labels)}
    quotient = {}
    for a, aa in classes.items():
        for b, bb in classes.items():
            ones = sum((rows[i] >> j) & 1 for i in aa for j in bb)
            quotient[a, b] = int(2 * ones > len(aa) * len(bb))
    return [sum(quotient[labels[i], labels[j]] << j for j in range(len(rows)))
            for i in range(len(rows))]


def project_columns(rows, labels):
    classes = {label: [i for i, v in enumerate(labels) if v == label] for label in set(labels)}
    return [sum((int(2 * sum((row >> j) & 1 for j in jj) > len(jj)) << j)
                for jj in classes.values() for j in jj) for row in rows]


def input_optimum(dist, c):
    return min(sum(min(dist[i][j] for j in centers) for i in range(len(dist)))
               for centers in combinations(range(len(dist)), c))


def random_model(b, N, c, errors, rng):
    group = list(oc.general_linear(b))
    labels = [a % c for a in range(N)]
    rng.shuffle(labels)
    K = [0] * (b*c)
    for i in range(b*c):
        for j in range(i, b*c):
            if rng.randrange(2):
                K[i] |= 1 << j
                K[j] |= 1 << i
    D = [sum(((K[labels[a]*b+u] >> (labels[z]*b+v)) & 1) << (z*b+v)
             for z in range(N) for v in range(b)) for a in range(N) for u in range(b)]
    S = [0] * (b*N)
    pairs = list(combinations(range(N), 2))
    rng.shuffle(pairs)
    for a, z in pairs[:errors]:
        noise = [rng.randrange(1 << b) for _ in range(b)]
        if not any(noise):
            noise[0] = 1
        for u in range(b):
            for v in range(b):
                if noise[u] >> v & 1:
                    S[a*b+u] ^= 1 << (z*b+v)
                    S[z*b+v] ^= 1 << (a*b+u)
    B = [x ^ y for x, y in zip(D, S)]
    # Every diagonal block is overwritten by arbitrary local quadratic data.
    for a in range(N):
        for u in range(b):
            B[a*b+u] &= ~(((1 << b)-1) << (a*b))
        for u in range(b):
            for v in range(u+1, b):
                if rng.randrange(2):
                    B[a*b+u] ^= 1 << (a*b+v)
                    B[a*b+v] ^= 1 << (a*b+u)
    gs = [rng.choice(group) for _ in range(N)]
    G = oc.block_gauge_matrix(gs, b)
    raw = oc.congruence(B, G)
    ideal = oc.congruence(D, G)
    E = sum(oc.rank(oc.block_at(S, a, z, b)) for a in range(N) for z in range(a+1, N))
    T = sum(oc.row_distance(oc.row_block(raw, a, b), oc.row_block(ideal, a, b), b, N)
            for a in range(N))
    assert T <= 2*E+b*N
    return raw, T, E, group


def audit_compiler(rng):
    fixtures = triangles = isometries = median_checks = 0
    examples = []
    for b in (1, 2, 3):
        for repeat in range(9):
            N, c, errors = 4 + repeat % 3, 1 + repeat % 3, repeat % 5
            B, T, E, group = random_model(b, N, c, errors, rng)
            distances = [[oc.orbit_distance(oc.row_block(B, a, b), oc.row_block(B, z, b), b, N, group)[0]
                          for z in range(N)] for a in range(N)]
            for a, z, t in product(range(N), repeat=3):
                assert distances[a][z] == distances[z][a]
                assert distances[a][z] <= distances[a][t] + distances[t][z]
                triangles += 1
            gauge = oc.block_gauge_matrix([rng.choice(group) for _ in range(N)], b)
            changed = oc.congruence(B, gauge)
            for a, z in product(range(N), repeat=2):
                value = oc.orbit_distance(oc.row_block(changed, a, b), oc.row_block(changed, z, b), b, N, group)[0]
                assert value == distances[a][z]
                isometries += 1
            rec = oc.acquire_orbits(B, b, c)
            optimum = input_optimum(distances, c)
            assert optimum <= 2*T
            assert rec['objective'] <= 5*optimum <= 10*T
            assert all(x > y for x, y in zip(rec['objective_history'], rec['objective_history'][1:]))
            assert rec['rank_budget'] <= b*c
            assert rec['residual_edges'] <= 15*b*b*(2*E+b*N)
            scalar_labels = [None] * (b*N)
            for a, cls in enumerate(rec['classes']):
                for block in cls:
                    for u in range(b):
                        scalar_labels[block*b+u] = (a, u)
            expected = direct_projection(rec['transformed_matrix'], scalar_labels)
            assert expected == rec['low_rank_matrix']
            assert all(x == (y & ~(1 << i)) ^ z for i, (x, y, z) in
                       enumerate(zip(rec['transformed_matrix'], rec['low_rank_matrix'], rec['sparse_matrix'])))
            median_checks += 1
            fixtures += 1
            examples.append(dict(b=b, blocks=N, center_budget=c, block_pair_errors=errors,
                                 error_rank_sum=E, hidden_row_error=T, optimum=optimum,
                                 objective=rec['objective'], acquired_rank=rec['low_rank'],
                                 residual_edges=rec['residual_edges'], classes=len(rec['classes'])))
    # Exact zero distances deliberately leave requested facilities unoccupied.
    empty_cases = []
    for b, N, c in ((1, 5, 5), (2, 4, 3), (3, 4, 4)):
        rec = oc.acquire_orbits([0]*(b*N), b, c)
        assert len(rec['classes']) == 1 and rec['classes'][0] == list(range(N))
        assert rec['low_rank'] == rec['residual_edges'] == rec['objective'] == 0
        empty_cases.append(dict(b=b, blocks=N, requested_centers=c, occupied_centers=1))
    return dict(fixtures=fixtures, triangle_checks=triangles, gauge_isometry_checks=isometries,
                median_checks=median_checks, empty_class_cases=empty_cases, examples=examples)


def audit_rounding():
    checks = 0
    largest = (0, 1)
    example = None
    for n, labels in ((2, [0,0]), (3, [0,0,0]), (4, [0,0,0,0]),
                      (5, [0,0,0,0,0]), (4, [0,0,1,1])):
        c = max(labels)+1
        edges = list(combinations(range(n), 2))
        classes = [[i for i, label in enumerate(labels) if label == a] for a in range(c)]
        for edge_bits in range(1 << len(edges)):
            B = oc.matrix_from_edges(n, [edge for i, edge in enumerate(edges) if edge_bits >> i & 1])
            rounded, _ = oc.round_symmetric(B, classes, 1)
            assert rounded == direct_projection(B, labels)
            error = hamming(B, rounded)
            for row_types in product(range(1 << n), repeat=c):
                C = [row_types[label] for label in labels]
                A = hamming(B, C)
                projected = project_columns(C, labels)
                assert hamming(C, projected) <= hamming(C, oc.transpose(C)) <= 2*A
                assert error <= hamming(B, projected) <= 3*A
                if A and error * largest[1] > largest[0] * A:
                    largest = error, A
                    example = dict(n=n, labels=labels, B=B, C=C, error=error, initial=A)
                checks += 1
    return dict(checks=checks, largest_observed_ratio=list(largest), example=example)


def audit_raw(rng):
    fixtures = []
    pointwise = 0
    for N, c, errors in ((2, 1, 0), (3, 2, 4), (4, 2, 8)):
        hidden = oc.hidden_instance(N, c, errors, rng)
        rec = oc.acquire_raw_cubic(hidden['raw'], hidden['n'], c)
        final = set(rec['final_polynomial'])
        for x in range(1 << hidden['n']):
            assert oc.phase(hidden['raw'], oc.apply(rec['full_coordinate_columns'], x)) == oc.phase(final, x)
            pointwise += 1
        actual = oc.truth_sum(hidden['raw'], hidden['n'])
        rebuilt, stats = oc.exact_reconstruct(rec)
        assert rebuilt == actual
        fixtures.append(dict(n=hidden['n'], raw_cubics=rec['raw_cubic_terms'],
                             rank=rec['low_rank'], residual_edges=rec['residual_edges'],
                             foreground_terms=rec['foreground_terms'], exact_sum=actual))
    return dict(fixtures=fixtures, pointwise_checks=pointwise, gaussian_reconstructions=len(fixtures))


def main():
    rng = random.Random(2026102711)
    results = {"compiler": audit_compiler(rng), "rounding": audit_rounding(),
               "raw_cubic": audit_raw(rng),
               "status": "All exact assertions passed. Exhaustive finite count backend only."}
    Path(__file__).with_name('orbit_rounding_audit_results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps({k: ({a:b for a,b in v.items() if a != 'examples'} if isinstance(v,dict) else v)
                      for k,v in results.items()}, indent=2))


if __name__ == '__main__':
    main()
