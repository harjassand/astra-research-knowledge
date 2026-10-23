"""Independent bounded diagnostics of the new spider proof, without producer imports.

The all-depth/all-p theorem is analytic in REVIEW.md. This checks its exact
quadratic identity, one branching graph, and one lost-hypothesis witness.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
from collections import defaultdict
import json
import time
import resource


def add(u, v):
    return u[0]+v[0], u[1]+v[1]


def mul(u, v):
    return u[0]*v[0]+5*u[1]*v[1], u[0]*v[1]+u[1]*v[0]


def scale(a, u):
    return a*u[0], a*u[1]


def graph_blocks(p, sizes, parents, parent_middle_indices):
    blocks, edges, membership = [], [], defaultdict(list)
    next_vertex = 0
    for i, k in enumerate(sizes):
        assert p >= 2 and k >= p+1
        hubs = list(range(next_vertex, next_vertex+p))
        next_vertex += p
        if parents[i] is None:
            mids = []
            depth = 0
        else:
            parent = parents[i]
            mids = [blocks[parent]['middles'][parent_middle_indices[i]]]
            depth = blocks[parent]['depth']+1
        while len(mids) < k:
            mids.append(next_vertex)
            next_vertex += 1
        blocks.append(dict(hubs=hubs, middles=mids, depth=depth))
        for v in hubs+mids:
            membership[v].append(i)
        edges.extend(tuple(sorted((h, v))) for h in hubs for v in mids)
    assert len(set(edges)) == len(edges)
    return next_vertex, sorted(edges), blocks, membership


def color(p, n, blocks, membership, star=False):
    colors = [-1]*n
    for block in blocks:
        start = p*(block['depth'] % 2) if star else 0
        for j, h in enumerate(block['hubs']):
            assert colors[h] == -1
            colors[h] = start+j
    for v, ids in membership.items():
        if colors[v] != -1:
            continue
        colors[v] = 2*p if star else p+min(blocks[i]['depth'] for i in ids) % 2
    assert min(colors) >= 0
    return colors


def components(n, edges, colors):
    groups = defaultdict(list)
    for u, v in edges:
        assert colors[u] != colors[v]
        groups[tuple(sorted((colors[u], colors[v])))].append((u, v))
    result = []
    for pair, es in sorted(groups.items()):
        adj = defaultdict(set)
        for u, v in es:
            adj[u].add(v); adj[v].add(u)
        seen = set()
        for start in sorted(adj):
            if start in seen:
                continue
            order = [start]; seen.add(start)
            for u in order:
                for v in sorted(adj[u]):
                    if v not in seen:
                        seen.add(v); order.append(v)
            assert sum(len(adj[v]) for v in order) == 2*(len(order)-1)
            result.append((pair, order, adj))
    return result


def check_shapes(p, n, edges, blocks, membership, star=False):
    colors = color(p, n, blocks, membership, star)
    hb = {v: i for i, block in enumerate(blocks) for v in block['hubs']}
    records = []
    for pair, order, adj in components(n, edges, colors):
        c = next(z for z in pair if z >= p) if not star else 2*p
        eligible = [v for v in order if v in hb and
                    (star or blocks[hb[v]]['depth'] % 2 == c-p)]
        assert len(eligible) == 1
        center = eligible[0]
        used = {center}; lengths = []
        for neighbor in sorted(adj[center]):
            used.add(neighbor)
            following = adj[neighbor]-{center}
            assert len(following) <= (0 if star else 1)
            if following:
                leaf = next(iter(following))
                assert adj[leaf] == {neighbor} and leaf not in used
                used.add(leaf)
            lengths.append(1+len(following))
        assert used == set(order)
        records.append({'pair': list(pair), 'center': center,
                        'vertices': len(order), 'arm_lengths': lengths})
    return colors, records


def main():
    started = time.perf_counter()
    # Q(sqrt5) arithmetic: t=(3+sqrt5)/2 and exact PSD determinant.
    t = (F(3,2), F(1,2))
    zero = add(add(mul(t, t), scale(-3, t)), (F(1), F(0)))
    determinant = add(mul(add(scale(2, t), (F(-1), F(0))),
                          add(t, (F(-1), F(0)))), scale(-1, mul(t, t)))
    assert zero == determinant == (0, 0)

    # One branching receiving-class graph; no depth or parameter sweep.
    n, es, blocks, membership = graph_blocks(2, [4,3,3], [None,0,0], [None,0,1])
    assert all(len(ids) <= 2 for ids in membership.values())
    c4, shape4 = check_shapes(2, n, es, blocks, membership)
    c5, shape5 = check_shapes(2, n, es, blocks, membership, True)

    # The natural extension without the at-most-two-block condition fails.
    parameter = 4
    nn, ee, bb, mm = graph_blocks(2, [parameter]+[3]*(parameter-1),
                                 [None]+[0]*(parameter-1),
                                 [None]+[0]*(parameter-1))
    cc = color(2, nn, bb, mm)
    center_hub = bb[0]['hubs'][0]
    cut_middle = bb[0]['middles'][0]
    target = next((pair, order, adj) for pair, order, adj in components(nn, ee, cc)
                  if pair == (0,2) and center_hub in order)
    pair, order, adj = target
    assert len(order) == 2*parameter
    central = tuple(sorted((center_hub, cut_middle)))
    coeff = {tuple(sorted((u,v))): (F(1) if tuple(sorted((u,v))) == central else F(-1,parameter))
             for u in order for v in adj[u] if u < v}
    y = [[F(0) for _ in range(4)] for _ in range(nn)]
    for (u,v), w in coeff.items():
        y[u][cc[v]] += w; y[v][cc[u]] += w
    norm2 = sum(x*x for row in y for x in row)
    assert norm2 == F(2, parameter) and coeff[central] == 1
    result = {
        'schema': 'astra-cycle9-independent-spider-review/v1',
        'exact_quadratic_identity': {'t': ['3/2','1/2'],
            'field': 'Q(sqrt5)', 't_squared_minus_3t_plus_1': ['0','0'],
            'PSD_determinant': ['0','0']},
        'branching_graph': {'p': 2, 'n': n, 'edges': es, 'blocks': blocks,
            'four_colors': c4, 'four_components': shape4,
            'five_colors': c5, 'five_components': shape5},
        'lost_membership_hypothesis': {'parameter_t': parameter, 'n': nn,
            'edges': ee, 'blocks': bb, 'colors': cc,
            'shared_vertex': cut_middle, 'shared_block_count': len(mm[cut_middle]),
            'component_vertices': order, 'central_edge': central,
            'coefficients': [[u,v,str(w)] for (u,v),w in sorted(coeff.items())],
            'full_action_norm_sq': str(norm2), 'operator_inverse_lower_sq': str(F(parameter,2))},
        'all_size_proof': 'REVIEW.md', 'no_size_or_parameter_sweep': True,
        'passed': True, 'wall_seconds_body': time.perf_counter()-started,
        'process_max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['passed','wall_seconds_body','process_max_rss_kib']}))


if __name__ == '__main__':
    main()
