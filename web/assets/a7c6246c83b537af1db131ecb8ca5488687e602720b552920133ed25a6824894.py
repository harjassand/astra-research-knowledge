#!/usr/bin/env python3
"""Exact semantic checks of the two quotient phases; not FO-syntax verification."""
from itertools import product
from pathlib import Path
import json


def quotient(vertices, equalities, unary, edges):
    parent = {x: x for x in vertices}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for x, y in equalities:
        x, y = find(x), find(y)
        if x != y:
            parent[y] = x
    image = {x: find(x) for x in vertices}
    out = set(image.values())
    return (out, {p: {image[x] for x in xs} for p, xs in unary.items()},
            {p: {(image[x], image[y]) for x, y in es} for p, es in edges.items()}, image)


def run_case(n, seed, relation):
    # Raw representatives V, binary relation candidates J, and two permanent controls.
    vs = [('v', i) for i in range(n)]
    js = [('j', i, j) for i, j in relation]
    controls = [('control', 0), ('control', 1)]
    vertices = set(vs + js + controls)
    unary = {'D': set(vs), 'J': set(js), 'M0': {controls[0]}, 'M1': {controls[1]}}
    edges = {'P0': {(('j', i, j), ('v', i)) for i, j in relation},
             'P1': {(('j', i, j), ('v', j)) for i, j in relation}}
    c_nodes, c_unary, c_edges, c_map = quotient(vertices,
        [(('v', i), ('v', j)) for i, j in seed], unary, edges)
    target = {p: {} for p in c_edges}
    for p, es in c_edges.items():
        for j, d in es:
            target[p].setdefault(j, set()).add(d)
    for j in c_unary['J']:
        assert len(target['P0'][j]) == len(target['P1'][j]) == 1
    dedup = [(j, k) for j in c_unary['J'] for k in c_unary['J']
             if all(target[p][j] == target[p][k] for p in target)]
    d_nodes, d_unary, d_edges, d_map = quotient(c_nodes, dedup, c_unary, c_edges)
    # Independently calculate undirected reachability of the arbitrary seed.
    reach = [[i == j or (i, j) in seed or (j, i) in seed for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] |= reach[i][k] and reach[k][j]
    cls = {i: min(j for j in range(n) if reach[i][j]) for i in range(n)}
    logical_names = {d_map[c_map[('v', i)]]: cls[i] for i in range(n)}
    dtarget = {p: {j: d for j, d in es} for p, es in d_edges.items()}
    actual = {(logical_names[dtarget['P0'][j]], logical_names[dtarget['P1'][j]]) for j in d_unary['J']}
    expected = {(cls[i], cls[j]) for i, j in relation}
    assert actual == expected
    assert len(d_unary['J']) == len(expected), 'duplicate incidences survived'
    assert len(d_unary['D']) == len(set(cls.values()))
    assert len(d_nodes) == len(set(cls.values())) + len(expected) + 2
    assert len(d_unary['M0']) == len(d_unary['M1']) == 1
    assert not (d_unary['D'] & (d_unary['M0'] | d_unary['M1']))
    return len(c_nodes), len(d_nodes), len(set(cls.values()))


def subsets(xs):
    return [tuple(x for i, x in enumerate(xs) if bits & (1 << i)) for bits in range(1 << len(xs))]


def main():
    cases = 0
    logical_counts = set()
    max_shrink = 0
    for n in range(4):
        pairs = list(product(range(n), repeat=2))
        all_subsets = subsets(pairs)
        for seed in all_subsets:
            for relation in all_subsets:
                c, d, logical = run_case(n, seed, relation)
                cases += 1
                logical_counts.add(logical)
                max_shrink = max(max_shrink, c-d)
    # Specific all-nine-candidates-to-one case, with nonsymmetric/nontransitive seed.
    c, d, logical = run_case(3, ((0, 1), (1, 2)), tuple(product(range(3), repeat=2)))
    assert (c, d, logical) == (12, 4, 1)
    # Two tags first make the complete repeated-coordinate product disjoint from old diagonals.
    tuple_cases = 0
    for n in range(6):
        marker = ('marker', 0)
        domain = [('atom', i) for i in range(n)]
        old = set(domain + [marker, ('marker', 1)])
        first = {(x, marker) for x in domain}
        diagonals = {(x, x) for x in old}
        assert not first & diagonals
        assert len(first) == n
        # Treat the new tagged vertices as distinct objects in the next state.
        t1 = [('T1', i) for i in range(n)]
        next_old = set(domain + t1 + [marker, ('marker', 1)])
        second = {(t1[i], domain[j]) for i in range(n) for j in range(n)}
        assert not second & {(x, x) for x in next_old}
        assert len(second) == n*n
        tuple_cases += 1
    results = {
        'status': 'passed',
        'exhaustive_cases': cases,
        'representative_domain_sizes': [0, 1, 2, 3],
        'logical_output_domain_sizes_tested': sorted(logical_counts),
        'all_directed_equality_seeds_including_loops': True,
        'all_noncongruent_binary_relation_candidate_subsets': True,
        'permanent_control_vertices_per_case': 2,
        'maximum_incidence_dedup_shrink': max_shrink,
        'nine_candidates_to_one_incidence': {'phase_c_size': c, 'phase_d_size': d},
        'tagged_product_cases': tuple_cases,
        'qualification': 'Semantic finite checks only; not formal proof or generated FO syntax verification.'
    }
    path = Path(__file__).with_name('dimension_binary_compiler_test_results.json')
    path.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
