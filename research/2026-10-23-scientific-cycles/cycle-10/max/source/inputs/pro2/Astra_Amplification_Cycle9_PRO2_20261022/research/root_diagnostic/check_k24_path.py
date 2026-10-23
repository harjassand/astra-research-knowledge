"""Independent exhaustive star-four check for a three-K2,4 block path.

No scientific producer imports. The fixed graph is constructed before any
coloring. Canonical first-occurrence color labels give one representative of
every coloring orbit, including fewer than four colors. Partial rejection
uses only a monochromatic edge or a fully colored bichromatic simple P4.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations, permutations, product
import argparse
import hashlib
import json
import math
import resource
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def make_graph(block_count):
    require(block_count in (1, 2, 3), 'bounded candidate count')
    blocks = [{'hubs': [0, 1], 'middles': [2, 3, 4, 5]}]
    if block_count >= 2:
        blocks.append({'hubs': [6, 7], 'middles': [2, 8, 9, 10]})
    if block_count == 3:
        blocks.append({'hubs': [11, 12], 'middles': [3, 13, 14, 15]})
    edges = []
    for block in blocks:
        edges.extend(tuple(sorted((h, m))) for h in block['hubs'] for m in block['middles'])
    require(len(set(edges)) == len(edges), 'block union duplicated edge')
    n = (6, 11, 16)[block_count - 1]
    # A star of four bags per block, joined through the actual cut vertices.
    bags, tree_edges = [], []
    for b, block in enumerate(blocks):
        base = len(bags)
        bags.extend(block['hubs'] + [m] for m in block['middles'])
        tree_edges.extend([base, base + j] for j in range(1, 4))
    if block_count >= 2:
        tree_edges.append([0, 4])  # Original vertex 2 occurs in both bags.
    if block_count == 3:
        tree_edges.append([1, 8])  # Original vertex 3 occurs in both bags.
    return {'name': f'K24_block_path_{block_count}', 'n': n,
            'edges': [list(e) for e in sorted(edges)], 'blocks': blocks,
            'width_two_decomposition': {'bags': bags, 'tree_edges': tree_edges}}


def adjacency(graph):
    n = graph['n']
    result = [set() for _ in range(n)]
    seen = set()
    for u, v in graph['edges']:
        require(type(u) is int and type(v) is int and 0 <= u < v < n, 'simple labeled edge')
        require((u, v) not in seen, 'duplicate original edge')
        seen.add((u, v))
        result[u].add(v)
        result[v].add(u)
    require(all(result), 'unused original vertex')
    return result


def reached(adj, start, allowed):
    seen, todo = set(), [start]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend((adj[v] & allowed) - seen)
    return seen


def graph_certificate(graph):
    n = graph['n']
    adj = adjacency(graph)
    require(reached(adj, 0, set(range(n))) == set(range(n)), 'graph disconnected')
    require(max(map(len, adj)) <= 4, 'degree cap fails')
    cycles = set()
    for s in range(n):
        def visit(path):
            for v in adj[path[-1]]:
                if v == s and len(path) >= 3:
                    p = tuple(path)
                    cycles.add(min(p, (s,) + tuple(reversed(path[1:]))))
                elif v > s and v not in path:
                    visit(path + [v])
        visit([s])
    require(len(cycles) == 6 * len(graph['blocks']), 'unexpected simple cycle count')
    for cycle in cycles:
        require(len(cycle) == 4, 'non-four-cycle found')
        induced = sum(1 for u, v in graph['edges'] if u in cycle and v in cycle)
        require(induced == 4, 'chorded cycle found')

    bags = graph['width_two_decomposition']['bags']
    tree_edges = graph['width_two_decomposition']['tree_edges']
    require(all(1 <= len(b) <= 3 and len(set(b)) == len(b) for b in bags), 'bag size')
    tadj = [set() for _ in bags]
    require(len(tree_edges) == len(bags) - 1, 'decomposition tree edge count')
    for a, b in tree_edges:
        require(0 <= a < b < len(bags), 'decomposition tree edge')
        tadj[a].add(b)
        tadj[b].add(a)
    require(reached(tadj, 0, set(range(len(bags)))) == set(range(len(bags))), 'bag tree disconnected')
    for u, v in graph['edges']:
        require(any(u in bag and v in bag for bag in bags), 'uncovered original edge')
    for v in range(n):
        containing = {i for i, bag in enumerate(bags) if v in bag}
        require(containing and reached(tadj, min(containing), containing) == containing, 'running intersection')
    cuts = []
    for v in range(n):
        allowed = set(range(n)) - {v}
        if reached(adj, min(allowed), allowed) != allowed:
            cuts.append(v)
    return {'connected': True, 'simple': True, 'maximum_degree': max(map(len, adj)),
            'degree_sequence': list(map(len, adj)), 'triangle_free': True,
            'chordless': True, 'all_simple_cycles': [list(c) for c in sorted(cycles)],
            'width_two_decomposition_verified': True, 'cut_vertices': cuts}


def paths_four(adj):
    paths = set()
    for b in range(len(adj)):
        for c in adj[b]:
            if c < b:
                continue
            for a in adj[b] - {c}:
                for d in adj[c] - {b, a}:
                    p = (a, b, c, d)
                    paths.add(min(p, tuple(reversed(p))))
    return sorted(paths)


def is_star(colors, edges, p4s):
    if any(colors[u] == colors[v] for u, v in edges):
        return False
    return not any(colors[a] == colors[c] and colors[b] == colors[d] for a, b, c, d in p4s)


def root_signature(adj, colors, v):
    own = colors[v]
    counts = Counter(colors[u] for u in adj[v])
    flags = {colors[u] for u in adj[v]
             if any(w != v and colors[w] == own for w in adj[u])}
    require(not any(counts[c] >= 2 and c in flags for c in counts), 'invalid root profile')
    if len(adj[v]) == 2:
        if len(counts) == 1:
            require(not flags, 'monochromatic-neighbor root has far flag')
            kind = 'A'
        else:
            kind = 'B' + str(len(flags))
    else:
        kind = 'degree_' + str(len(adj[v]))
    return {'type': kind, 'root_color': own,
            'neighbor_color_counts': [counts.get(c, 0) for c in range(4)],
            'far_flags': sorted(flags)}


def enumerate_canonical(graph):
    """Complete exact DFS; at most 4 colors, no timeout or solver status."""
    start, cpu = time.perf_counter(), time.process_time()
    n = graph['n']
    adj = adjacency(graph)
    edges = [tuple(e) for e in graph['edges']]
    p4s = paths_four(adj)
    # Fixed original-ID order. Canonical first-occurrence labels quotient only
    # global color permutations, not vertex permutations or root hypotheses.
    order = list(range(n))
    containing = [[] for _ in range(n)]
    for path in p4s:
        for v in path:
            containing[v].append(path)
    colors = [-1] * n
    stats = Counter()
    first = None
    profile_counts = {v: Counter() for v in range(n) if len(adj[v]) == 2}
    profile_witnesses = {v: {} for v in profile_counts}
    weighted_count = 0

    def walk(position, highest):
        nonlocal first, weighted_count
        stats['search_nodes'] += 1
        if position == n:
            require(is_star(colors, edges, p4s), 'accepted complete coloring invalid')
            stats['complete_canonical_star_colorings'] += 1
            used = highest + 1
            weighted_count += math.factorial(4) // math.factorial(4 - used)
            if first is None:
                first = list(colors)
            for v in profile_counts:
                profile = root_signature(adj, colors, v)
                kind = profile['type']
                profile_counts[v][kind] += 1
                profile_witnesses[v].setdefault(kind, {'colors': list(colors), 'profile': profile})
            return
        v = order[position]
        for color in range(min(3, highest + 1) + 1):
            stats['proposed_assignments'] += 1
            if any(colors[u] == color for u in adj[v]):
                stats['properness_rejections'] += 1
                continue
            colors[v] = color
            bad = False
            for a, b, c, d in containing[v]:
                if min(colors[a], colors[b], colors[c], colors[d]) >= 0:
                    if colors[a] == colors[c] and colors[b] == colors[d]:
                        bad = True
                        break
            if bad:
                stats['completed_P4_rejections'] += 1
            else:
                walk(position + 1, max(highest, color))
            colors[v] = -1

    walk(0, -1)
    return {'complete': True, 'color_budget': 4, 'fixed_vertex_order': order,
            'quotient': 'global first-occurrence color relabeling only',
            'simple_P4_constraints': len(p4s), 'statistics': dict(stats),
            'canonical_star_colorings': stats['complete_canonical_star_colorings'],
            'labeled_star_colorings': weighted_count, 'first_coloring': first,
            'degree_two_profiles': {str(v): dict(counts) for v, counts in profile_counts.items()},
            'degree_two_profile_witnesses': {str(v): w for v, w in profile_witnesses.items()},
            'body_wall_seconds': time.perf_counter() - start,
            'body_cpu_seconds': time.process_time() - cpu}


def raw_single_block_check(graph, canonical_result):
    """Different enumeration for the load-bearing local profile lemma."""
    adj = adjacency(graph)
    edges = [tuple(e) for e in graph['edges']]
    p4s = paths_four(adj)
    count = 0
    profiles = Counter()
    witness = {}
    for colors in product(range(4), repeat=6):
        if not is_star(colors, edges, p4s):
            continue
        count += 1
        require(colors[0] != colors[1], 'equal K2,4 hub colors survived')
        mids = [2, 3, 4, 5]
        unique = [v for v in mids if sum(colors[w] == colors[v] for w in mids) == 1]
        require(len(unique) <= 1, 'K2,4 has two singleton-color middles')
        for v in mids:
            profile = root_signature(adj, colors, v)
            expected = 'B0' if v in unique else 'B2'
            require(profile['type'] == expected, 'K2,4 far-flag characterization fails')
        profile = root_signature(adj, colors, 2)
        profiles[profile['type']] += 1
        witness.setdefault(profile['type'], {'colors': list(colors), 'profile': profile})
    require(count == canonical_result['labeled_star_colorings'], 'independent local enumeration mismatch')
    require(set(profiles) == {'B0', 'B2'}, 'unexpected K2,4 root type set')
    return {'all_assignments_tested': 4 ** 6, 'labeled_star_colorings': count,
            'marked_middle_vertex': 2, 'exact_profile_counts': dict(profiles),
            'witnesses': witness, 'equal_hub_star_colorings': 0,
            'max_singleton_color_middles': 1,
            'all_four_middle_profiles_checked_in_every_star_coloring': True}


def gluing_truth_table():
    # Root color 0. Profiles realize neighbor supports in {1,2,3}.
    types = {'A': [({c}, set()) for c in (1, 2, 3)]}
    for flags in range(3):
        rows = []
        for support in combinations((1, 2, 3), 2):
            for marked in combinations(support, flags):
                rows.append((set(support), set(marked)))
        types['B' + str(flags)] = rows
    answer = {}
    for left, right in product(types, repeat=2):
        witnesses = []
        for (nl, fl), (nr, fr) in product(types[left], types[right]):
            if not nl & nr & (fl | fr):
                witnesses.append({'left_N': sorted(nl), 'left_F': sorted(fl),
                                  'right_N': sorted(nr), 'right_F': sorted(fr)})
        answer[left + '+' + right] = {'admitted': bool(witnesses),
                                     'witness': witnesses[0] if witnesses else None}
    require(all(not answer['B2+' + t]['admitted'] for t in ('B0', 'B1', 'B2')),
            'B2 compatibility conclusion fails')
    return answer


def run(outdir):
    start, cpu = time.perf_counter(), time.process_time()
    graphs = [make_graph(k) for k in (1, 2, 3)]
    inputs = {'schema': 'astra-cycle9-K24-root-diagnostic-input/v1', 'graphs': graphs}
    encoded = (json.dumps(inputs, indent=2) + '\n').encode()
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / 'INPUTS.json').write_bytes(encoded)
    records = []
    for graph in graphs:
        structure = graph_certificate(graph)
        coloring = enumerate_canonical(graph)
        expected = len(graph['blocks']) < 3
        require(bool(coloring['canonical_star_colorings']) == expected, 'unexpected star-four verdict')
        records.append({'name': graph['name'], 'vertices': graph['n'], 'edges': len(graph['edges']),
                        'structure': structure, 'coloring': coloring})
    local = raw_single_block_check(graphs[0], records[0]['coloring'])
    truth = gluing_truth_table()
    result = {'schema': 'astra-cycle9-independent-root-diagnostic/v1', 'status': 'PASS',
              'input': {'filename': 'INPUTS.json', 'bytes': len(encoded),
                        'sha256': hashlib.sha256(encoded).hexdigest()},
              'producer_imports': False, 'old_suite_rerun': False,
              'records': records, 'single_block_independent_raw_enumeration': local,
              'root_gluing_truth_table': truth,
              'conclusion': 'The fixed 16-vertex three-K2,4 block path is connected, simple, chordless, treewidth<=2, maximum degree4, and is not star-four-colorable. This excludes star-coordinate four queries only; bounded-component or arbitrary-real four-query recovery is not excluded.',
              'cost': {'body_wall_seconds': time.perf_counter() - start,
                       'body_cpu_seconds': time.process_time() - cpu,
                       'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                       'scope': 'Three actual graph certificates, complete canonical star-four enumerations, independent 4096-assignment local enumeration, root gluing table, and input serialization; excludes startup and final result serialization.'}}
    (outdir / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'input': result['input'],
                      'records': [{'name': r['name'],
                                   'canonical_star_colorings': r['coloring']['canonical_star_colorings'],
                                   'labeled_star_colorings': r['coloring']['labeled_star_colorings'],
                                   'statistics': r['coloring']['statistics']} for r in records],
                      'local': local, 'cost': result['cost']}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    run(args.output_dir)
