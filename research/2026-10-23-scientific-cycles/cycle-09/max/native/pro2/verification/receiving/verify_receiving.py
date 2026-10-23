"""Independent exact receiving check for Cycle8's two new operations.

No producer imports. Rebuilds original supports, forms complete coordinate
actions, uses analytic star-block least squares, and checks rational LDL^T.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter, defaultdict
from itertools import combinations
import argparse
import hashlib
import json
import resource
import time

F = Fraction
PINNED = {
    'A5_three_action_control.json': (8482, '3fb018f3f8d7d0acd9a8a6f4c5df3570cbe024fd54bcce69f50379ec2f196188'),
    'mixed_loaded_16_four_action.json': (14889, 'b6396938e76b2b2adb199e103a48bf4087222a78e62e9a45387d790e5acee9df')
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def fraction_array(data, n, q):
    need(len(data) == n and all(len(row) == q for row in data), 'action/noise dimensions')
    return [[F(v) for v in row] for row in data]


def a_l_graph(length):
    need(type(length) is int and length >= 2, 'A_L length')
    base_length = 2 + (length - 2) % 3
    bases = {2: [1, 0, 1], 3: [1, 0, 2, 1], 4: [1, 0, 2, 0, 1]}
    word = bases[base_length] + [2, 0, 1] * ((length - base_length) // 3)
    path = [1] + list(range(7, length + 6)) + [2]
    colors = [0, 1, 1, 2, 2, 2, 2] + word[1:-1]
    edges = [(0, 3), (1, 3), (0, 4), (1, 4),
             (0, 5), (2, 5), (0, 6), (2, 6)]
    edges += list(zip(path, path[1:]))
    return len(colors), sorted(tuple(sorted(e)) for e in edges), colors, word


def expand_original(spec):
    """Independent uncolored expansion, preserving the documented vertex IDs.

    Uses recursive original productions. Paths allocate their actual internal
    vertices from left to right. Multi-series is left-associated; parallel
    children are traversed left to right. No coloring/certificate import.
    """
    nodes, root = spec['nodes'], spec['root']
    need(type(root) is int and 0 <= root < len(nodes), 'expression root')
    loads = []
    for i, node in enumerate(nodes):
        kind = node['kind']
        if kind == 'path':
            need(type(node['length']) is int and node['length'] >= 2, 'path length')
            loads.append((1, 1))
            continue
        children = node['children']
        need(all(type(j) is int and 0 <= j < i for j in children), 'expression topology')
        if kind in ('L', 'R'):
            need(len(children) == 1, 'extension arity')
            degree = loads[children[0]]
            affected = 0 if kind == 'L' else 1
            need(degree[affected] <= 3, 'extension degree budget')
            loads.append((1, degree[1]) if kind == 'L' else (degree[0], 1))
        else:
            need(kind in ('S', 'P') and len(children) >= 2, 'join arity/kind')
            child_loads = [loads[j] for j in children]
            if kind == 'P':
                degree = tuple(sum(d[k] for d in child_loads) for k in (0, 1))
                need(max(degree) <= 4, 'parallel degree budget')
            else:
                need(all(child_loads[k][1] + child_loads[k + 1][0] <= 4
                         for k in range(len(children) - 1)), 'series degree budget')
                degree = (child_loads[0][0], child_loads[-1][1])
            loads.append(degree)

    next_vertex, edges = 2, []
    original_occurrences = 0

    def fresh():
        nonlocal next_vertex
        v = next_vertex
        next_vertex += 1
        return v

    def expand_series(children, s, t):
        if len(children) == 1:
            expand(children[0], s, t)
        else:
            junction = fresh()
            expand_series(children[:-1], s, junction)
            expand(children[-1], junction, t)

    def expand(index, s, t):
        nonlocal original_occurrences
        original_occurrences += 1
        node = nodes[index]
        kind = node['kind']
        if kind == 'path':
            chain = [s] + [fresh() for _ in range(node['length'] - 1)] + [t]
            edges.extend(zip(chain, chain[1:]))
        elif kind == 'P':
            for child in node['children']:
                expand(child, s, t)
        elif kind == 'S':
            expand_series(node['children'], s, t)
        elif kind == 'L':
            old_terminal = fresh()
            edges.append((s, old_terminal))
            expand(node['children'][0], old_terminal, t)
        else:
            old_terminal = fresh()
            edges.append((old_terminal, t))
            expand(node['children'][0], s, old_terminal)

    expand(root, 0, 1)
    return next_vertex, sorted(tuple(sorted(e)) for e in edges), loads[root], original_occurrences


def validate_graph(graph, q):
    n, colors = graph['n'], graph['colors']
    need(type(n) is int and n > 0 and len(colors) == n, 'vertex count')
    need(all(type(c) is int and 0 <= c < q for c in colors), 'actual query palette')
    need(set(colors) == set(range(q)), 'unused claimed action')
    edges = [tuple(e) for e in graph['edges']]
    need(len(set(edges)) == len(edges), 'duplicate support edge')
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        need(0 <= u < v < n, 'simple support edge')
        need(colors[u] != colors[v], 'improper coordinate coloring')
        adjacency[u].add(v)
        adjacency[v].add(u)
    counts = [Counter(colors[u] for u in neighbors) for neighbors in adjacency]
    need(max(map(len, adjacency)) <= 4, 'maximum degree')
    for u, v in edges:
        need(not adjacency[u] & adjacency[v], 'triangle in actual support')
        need(not (counts[u][colors[v]] >= 2 and counts[v][colors[u]] >= 2),
             'actual multiplicity test finds a bichromatic P4')
    s, t = graph['terminals']
    need(s != t and t not in adjacency[s], 'nonadjacent distinct terminals')
    need([len(adjacency[s]), len(adjacency[t])] == list(graph['terminal_degrees']),
         'actual terminal degrees')
    return edges, adjacency, counts


def matrix_source(data, n, edges):
    diagonal = list(map(F, data['diagonal']))
    need(len(diagonal) == n, 'free diagonal dimensions')
    edge_values = {}
    for u, v, value in data['edges']:
        need((u, v) not in edge_values, 'duplicate matrix edge')
        edge_values[u, v] = F(value)
    need(set(edge_values) == set(edges), 'matrix support differs from actual graph')
    return diagonal, edge_values


def full_action(n, q, colors, diagonal, edge_values):
    result = [[F(0) for _ in range(q)] for _ in range(n)]
    for i in range(n):
        result[i][colors[i]] = diagonal[i]
    for (u, v), value in edge_values.items():
        result[u][colors[v]] += value
        result[v][colors[u]] += value
    return result


def analytic_star_inverse(n, q, colors, edges, observations):
    diagonal = [observations[i][colors[i]] for i in range(n)]
    recovered = {}
    components = []
    for a, b in combinations(range(q), 2):
        adjacency = defaultdict(set)
        for u, v in edges:
            if {colors[u], colors[v]} == {a, b}:
                adjacency[u].add(v)
                adjacency[v].add(u)
        unseen = set(adjacency)
        while unseen:
            first = min(unseen)
            todo, vertices = [first], set()
            while todo:
                v = todo.pop()
                if v in vertices:
                    continue
                vertices.add(v)
                todo.extend(adjacency[v] - vertices)
            unseen -= vertices
            center = min(vertices, key=lambda v: (-len(adjacency[v]), v))
            leaves = sorted(vertices - {center})
            need(adjacency[center] == set(leaves), 'bichromatic block not a star')
            need(all(adjacency[v] == {center} for v in leaves), 'nonleaf in star block')
            k = len(leaves)
            need(k >= 1, 'empty edge component')
            center_color = colors[center]
            leaf_color = colors[leaves[0]]
            leaf_data = [observations[v][center_color] for v in leaves]
            correction = (observations[center][leaf_color] - sum(leaf_data, F(0))) / (k + 1)
            for v, value in zip(leaves, leaf_data):
                edge = tuple(sorted((center, v)))
                need(edge not in recovered, 'edge assigned twice')
                recovered[edge] = value + correction
            components.append({'colors': [a, b], 'center': center, 'leaves': leaves})
    need(set(recovered) == set(edges), 'edge omitted by analytic inverse')
    return diagonal, recovered, components


def squared_norm(array):
    return sum((x * x for row in array for x in row), F(0))


def ldl_certificate(matrix):
    """Independent exact LDL recurrence and full factor reconstruction."""
    n = len(matrix)
    lower = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = []
    for j in range(n):
        pivot = matrix[j][j] - sum((lower[j][k] ** 2 * diagonal[k] for k in range(j)), F(0))
        need(pivot >= 0, 'negative PSD pivot')
        diagonal.append(pivot)
        for i in range(j + 1, n):
            numerator = matrix[i][j] - sum((lower[i][k] * lower[j][k] * diagonal[k]
                                           for k in range(j)), F(0))
            if pivot == 0:
                need(numerator == 0, 'zero PSD pivot with nonzero column')
                lower[i][j] = F(0)
            else:
                lower[i][j] = numerator / pivot
    for i in range(n):
        for j in range(n):
            reconstructed = sum((lower[i][k] * diagonal[k] * lower[j][k]
                                 for k in range(min(i, j) + 1)), F(0))
            need(reconstructed == matrix[i][j], 'LDL factor does not reconstruct matrix')
    return diagonal


def check_one(path):
    start, cpu = time.perf_counter(), time.process_time()
    raw = path.read_bytes()
    size, sha = PINNED[path.name]
    need(len(raw) == size and hashlib.sha256(raw).hexdigest() == sha, 'receiving source identity')
    record = json.loads(raw)
    need(record['schema'] == 'astra-loaded-star-full-action-receiving/v1', 'receiving schema')
    graph, q = record['graph'], record['query_count']
    n, colors = graph['n'], graph['colors']
    edges, adjacency, counts = validate_graph(graph, q)
    if path.name == 'A5_three_action_control.json':
        expected_n, expected_edges, expected_colors, word = a_l_graph(graph['length'])
        need((n, edges, colors) == (expected_n, expected_edges, expected_colors), 'A_L source recipe binding')
        need(word == graph['path_word'] and graph['branch_vertices'] == {'a': 0, 'b': 1, 'c': 2}, 'A_L word/branches')
        need(q == 3 and len(edges) == n + 2, 'A_L query/dimension control')
        source_binding = 'Exact A_L edge recipe and explicit all-length star-three word; L=5.'
    else:
        expected_n, expected_edges, terminal_loads, original_count = expand_original(graph['original_spec'])
        need((n, edges) == (expected_n, expected_edges), 'original expression/support binding')
        need(tuple(graph['terminal_degrees']) == terminal_loads, 'original expression port loads')
        normalized_n, normalized_edges, normalized_loads, normalized_count = expand_original(graph['normalized_spec'])
        need((n, edges, terminal_loads) == (normalized_n, normalized_edges, normalized_loads),
             'saved normalized expression changes original support')
        need(normalized_count == graph['expanded_occurrences'], 'expanded occurrence count')
        need(q == 4, 'mixed operation query count')
        # Actual data, including per-color multiplicities, bind the projected root target.
        target = graph['root_target']
        for index, vertex in enumerate(graph['terminals']):
            degree_index, support_index, flag_index = (2, 3, 4) if index == 0 else (5, 6, 7)
            need(len(adjacency[vertex]) == target[degree_index], 'root target actual degree')
            if target[degree_index] == 4:
                need(target[index] == -1 and target[support_index] == 0 and target[flag_index] == 0,
                     'root saturation marker')
                continue
            need(colors[vertex] == target[index], 'root target visible color')
            support = sum(1 << c for c in counts[vertex])
            flags = 0
            for neighbor in adjacency[vertex]:
                if any(other != vertex and colors[other] == colors[vertex] for other in adjacency[neighbor]):
                    flags |= 1 << colors[neighbor]
            need(support & target[support_index] == support and flags & target[flag_index] == flags,
                 'actual root support/flags exceed target')
        source_binding = 'Independent uncolored expansion of original and normalized supplied expressions; exact vertex IDs and edges.'

    actual_multiplicities = [[counts[i].get(c, 0) for c in range(4)] for i in range(n)]
    need(actual_multiplicities == record['graph_check']['actual_neighbor_color_multiplicities'], 'saved neighbor multiplicities')
    need(record['graph_check']['maximum_degree'] == max(map(len, adjacency)), 'saved maximum degree')
    need(record['graph_check']['star'] is True, 'saved star check')
    need(record['actual_design'] == {'type': 'coordinate', 'colors': colors, 'row_energy_sq': 1}, 'actual design/row budget')
    need(record['graph_check']['row_energy_sq'] == 1, 'graph-check row budget')

    diagonal, values = matrix_source(record['matrix'], n, edges)
    need(all(diagonal) and all(values.values()), 'fixture should exercise free diagonal and every edge')
    noise = fraction_array(record['noise'], n, q)
    noise_sq = squared_norm(noise)
    need(noise_sq > 0, 'zero receiving noise')
    exact_action = full_action(n, q, colors, diagonal, values)
    need(exact_action == fraction_array(record['full_action'], n, q), 'full original action mismatch')
    observed = [[exact_action[i][c] + noise[i][c] for c in range(q)] for i in range(n)]
    need(observed == fraction_array(record['observed_action'], n, q), 'observed action mismatch')

    clean_diagonal, clean_values, _ = analytic_star_inverse(n, q, colors, edges, exact_action)
    need((clean_diagonal, clean_values) == (diagonal, values), 'independent noiseless recovery')
    recovered_diagonal, recovered_values, components = analytic_star_inverse(n, q, colors, edges, observed)
    saved_diagonal, saved_values = matrix_source(record['output'], n, edges)
    need((recovered_diagonal, recovered_values) == (saved_diagonal, saved_values), 'analytic LS output mismatch')
    projected = full_action(n, q, colors, recovered_diagonal, recovered_values)
    need(projected == fraction_array(record['projected_action'], n, q), 'projected full action mismatch')
    residual = [[observed[i][c] - projected[i][c] for c in range(q)] for i in range(n)]
    need(all(residual[i][colors[i]] == 0 for i in range(n)), 'diagonal projection normal equation')
    need(all(residual[u][colors[v]] + residual[v][colors[u]] == 0 for u, v in edges),
         'edge projection normal equation')

    delta = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        delta[i][i] = recovered_diagonal[i] - diagonal[i]
    for (u, v), value in recovered_values.items():
        delta[u][v] = delta[v][u] = value - values[u, v]
    error_sq = squared_norm(delta)
    need(error_sq <= 2 * noise_sq, 'actual Frobenius bound fails')
    psd = [[(F(3, 2) * noise_sq if i == j else F(0))
            - sum((delta[i][k] * delta[k][j] for k in range(n)), F(0))
            for j in range(n)] for i in range(n)]
    pivots = ldl_certificate(psd)
    checks = record['exact_checks']
    need(checks['noiseless_equality'] is True, 'saved noiseless result')
    need(F(checks['projected_action_residual_sq']) == 0, 'saved projected residual')
    need(F(checks['noise_norm_sq']) == noise_sq, 'saved noise norm')
    need(F(checks['error_frobenius_sq']) == error_sq, 'saved error norm')
    need(F(checks['operator_constant_sq']) == F(3, 2) and F(checks['frobenius_constant_sq']) == 2,
         'saved constants')
    need(list(map(F, checks['operator_psd_pivots'])) == pivots, 'saved exact PSD pivots')
    need(checks['operator_psd_matrix'] == '(3/2)*||E||F^2*I - (Dhat-D)^2', 'PSD matrix label')
    need(record['graph_check']['all_noise_operator_constant_sq'] == '3/2'
         and record['graph_check']['all_noise_frobenius_constant_sq'] == '2', 'graph-check constants')

    return {'name': record['name'], 'status': 'PASS',
            'input': {'filename': path.name, 'bytes': len(raw), 'sha256': sha},
            'vertices': n, 'edges': len(edges), 'queries': q,
            'source_binding': source_binding,
            'simple_triangle_free_star_degree_four': True,
            'actual_neighbor_color_multiplicities_matched': True,
            'coordinate_row_energy_sq': 1,
            'full_original_action_and_noise_matched': True,
            'independent_analytic_star_LS_matched': True,
            'noiseless_reconstruction_exact': True,
            'projection_normal_equations_exact': True,
            'projected_action_residual_sq': '0',
            'raw_observation_residual_sq': str(squared_norm(residual)),
            'noise_norm_sq': str(noise_sq), 'error_frobenius_sq': str(error_sq),
            'exact_PSD_LDL_reconstruction_matched': True,
            'PSD_pivots': len(pivots), 'PSD_strictly_positive_pivots': all(p > 0 for p in pivots),
            'bichromatic_star_components': components,
            'body_wall_seconds': time.perf_counter() - start,
            'body_cpu_seconds': time.process_time() - cpu}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--results-dir', type=Path,
                        default=Path(__file__).resolve().parents[2] / 'results')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    start, cpu = time.perf_counter(), time.process_time()
    rows = [check_one(args.results_dir / name) for name in PINNED]
    result = {'schema': 'astra-cycle8-independent-receiving-gate/v1',
              'status': 'PASS', 'producer_imports': False, 'operations': rows,
              'cost': {'body_wall_seconds': time.perf_counter() - start,
                       'body_cpu_seconds': time.process_time() - cpu,
                       'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                       'scope': 'Both source reads/hash binding, graph and full-action reconstruction, exact analytic LS, projection and LDL checks; excludes startup and final receipt serialization.'}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
