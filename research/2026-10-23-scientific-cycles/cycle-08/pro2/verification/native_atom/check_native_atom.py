"""Independent exact gate for the new native Cycle8 atom receiver.

Imports only standard-library modules and the earlier independent receiving
checker's pure arithmetic helpers. It imports no producer, performs no search
for a new coloring, and does not rerun the earlier two receiving records.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import argparse
import hashlib
import importlib.util
import json
import resource
import time

F = Fraction
PINS = {
    'inputs/native_atom_9.json':
        (458, '0c0feabd40a60b8a64be468fbb62ed33d7622d51b80077c75674a21ea271c4aa'),
    'results/native_atom_9_four_action.json':
        (12259, 'b296faff62ea21aca02f21dc36d2402557e5c534d4971cd6000e1c90a8cd4316'),
    'results/native_atom_branch_checks.json':
        (3014, 'f839dea60eb556a37e12c605d08c878ec3fd9d50a33cc1c9ca1401643d6d9751'),
    'verification/receiving/verify_receiving.py':
        (18670, '05ef4fef5ebdc2affea5e042449653723f62bc202e7bfedf72a67d42d82bc3b5')
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_bound(root, relative):
    raw = (root / relative).read_bytes()
    size, sha = PINS[relative]
    need(len(raw) == size and hashlib.sha256(raw).hexdigest() == sha,
         'pinned source mismatch: ' + relative)
    return raw


def canonical_edges(n, raw_edges):
    result = set()
    for edge in raw_edges:
        need(len(edge) == 2, 'edge arity')
        u, v = edge
        need(type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n and u != v,
             'edge outside simple original support')
        edge = tuple(sorted((u, v)))
        need(edge not in result, 'duplicate edge')
        result.add(edge)
    return result


def adjacency_of(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        need(u in adjacency and v in adjacency, 'edge endpoint outside vertices')
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def connected(adjacency, deleted=None):
    vertices = set(adjacency) - {deleted}
    if not vertices:
        return False
    todo, seen = [min(vertices)], set()
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(adjacency[v] - seen - {deleted})
    return seen == vertices


def all_cycles(adjacency):
    """Exact finite diagnostic, exponential in general; not production prep."""
    cycles = set()
    for start in sorted(adjacency):
        def visit(path):
            here = path[-1]
            for nxt in sorted(adjacency[here]):
                if nxt == start and len(path) >= 3:
                    forward = tuple(path)
                    reverse = (start,) + tuple(reversed(path[1:]))
                    cycles.add(min(forward, reverse))
                elif nxt > start and nxt not in path:
                    visit(path + [nxt])
        visit([start])
    return sorted(cycles)


def width_two_elimination(adjacency):
    """Finite independent backtracking, with an explicitly verified fill trace."""
    def search(current):
        if not current:
            return []
        for v in sorted(current):
            neighbors = sorted(current[v])
            if len(neighbors) > 2:
                continue
            copied = {u: nbrs - {v} for u, nbrs in current.items() if u != v}
            added = []
            if len(neighbors) == 2:
                a, b = neighbors
                if b not in copied[a]:
                    copied[a].add(b)
                    copied[b].add(a)
                    added = [[a, b]]
            rest = search(copied)
            if rest is not None:
                return [{'vertex': v, 'later_neighbors': neighbors,
                         'bag': [v] + neighbors, 'fill_edges': added}] + rest
        return None

    trace = search(adjacency)
    need(trace is not None, 'no width-two elimination certificate found')
    current = {v: set(nbrs) for v, nbrs in adjacency.items()}
    for row in trace:
        v = row['vertex']
        need(v in current and sorted(current[v]) == row['later_neighbors'], 'fill trace mismatch')
        need(len(current[v]) <= 2, 'elimination width exceeds two')
        neighbors = sorted(current[v])
        for u in neighbors:
            current[u].remove(v)
        del current[v]
        for a, b in combinations(neighbors, 2):
            current[a].add(b)
            current[b].add(a)
    need(not current, 'elimination trace incomplete')
    return trace


def graph_class(n, edges):
    need(type(n) is int and n >= 3, 'two-connected graph size')
    adjacency = adjacency_of(range(n), edges)
    need(connected(adjacency), 'original graph disconnected')
    need(all(connected(adjacency, v) for v in adjacency), 'original graph has cut vertex')
    need(max(map(len, adjacency.values())) <= 4, 'original maximum degree')
    cycles = all_cycles(adjacency)
    need(cycles, 'two-connected input has no cycle')
    for cycle in cycles:
        length = len(cycle)
        cycle_edges = {tuple(sorted((cycle[i], cycle[(i + 1) % length]))) for i in range(length)}
        induced_edges = {e for e in edges if e[0] in cycle and e[1] in cycle}
        need(induced_edges == cycle_edges, 'original graph has a chorded cycle')
    return {
        'simple': True, 'two_connected': True, 'maximum_degree': max(map(len, adjacency.values())),
        'chordless_all_cycles_enumerated': True,
        'cycles': [list(c) for c in cycles],
        'triangle_free': all(len(c) != 3 for c in cycles),
        'width_two_elimination_trace': width_two_elimination(adjacency),
        'diagnostic_scope': 'Finite exact graph checks; exhaustive cycle enumeration and elimination backtracking are not the production preparation algorithm.'
    }


def validate_suppression(form, edges):
    """Check the original-vertex meaning of the producer's recorded reductions."""
    prep = form['preparation']
    if form['triangle']:
        need(prep['suppressed_vertices'] == [], 'triangle suppression should be empty')
        return []
    protected = tuple(sorted(prep['protected_edge']))
    need(protected in edges, 'protected edge absent from original graph')
    current = adjacency_of(range(form['n']), edges)
    trace = []
    for row in prep['suppressed_vertices']:
        need(len(row) == 4, 'suppression record arity')
        w, a, b, opaque_expression_id = row
        need(w in current and w not in protected and current[w] == {a, b},
             'suppression is not actual degree two away from protected edge')
        need(type(opaque_expression_id) is int and opaque_expression_id >= 0,
             'malformed expression identifier')
        merged = b in current[a]
        current[a].remove(w)
        current[b].remove(w)
        del current[w]
        current[a].add(b)
        current[b].add(a)
        need(max(map(len, current.values())) <= 4, 'suppression exceeded degree cap')
        trace.append({'vertex': w, 'neighbors': [a, b], 'parallel_merge': merged})
    need(set(current) == set(protected), 'suppression did not reach protected endpoints')
    need(current[protected[0]] == {protected[1]} and current[protected[1]] == {protected[0]},
         'suppression final edge mismatch')
    return trace


def validate_normal_form(form, n, original_edges):
    need(form['schema'] == 'astra-native-atom-normal-form/v1', 'native form schema')
    need(form['n'] == n and canonical_edges(n, form['original_edges']) == original_edges,
         'normal form original support binding')
    suppression = validate_suppression(form, original_edges)
    nodes = form['nodes']
    if form['triangle']:
        need(n == 3 and len(original_edges) == 3 and nodes == [] and form['root'] is None,
             'triangle exception is not exactly C3')
        return {'triangle_exception': True, 'loaded_nodes': 0,
                'suppression_trace': suppression, 'node_trace': []}

    root = form['root']
    need(type(root) is int and 0 <= root < len(nodes), 'loaded root index')
    used_as_child = Counter()
    sets, trace = [], []
    for index, node in enumerate(nodes):
        kind = node['kind']
        ports = node['terminals']
        need(len(ports) == 2 and all(type(v) is int and 0 <= v < n for v in ports)
             and ports[0] != ports[1], 'node terminals')
        s, t = ports
        children = node.get('children', [])
        need(all(type(c) is int and 0 <= c < index for c in children), 'loaded node topology')
        used_as_child.update(children)
        shared = []
        if kind == 'path':
            need(not children and node['length'] == 2, 'native path leaf is not path2')
            middle = node['middle']
            need(type(middle) is int and 0 <= middle < n and middle not in {s, t}, 'path midpoint')
            vertices = {s, middle, t}
            edges = {tuple(sorted((s, middle))), tuple(sorted((middle, t)))}
        elif kind in ('L', 'R'):
            need(len(children) == 1, 'extension child count')
            c = children[0]
            child_vertices, child_edges, child_ports = sets[c]
            a, b = child_ports
            if kind == 'L':
                need(t == b and s not in child_vertices, 'left extension actual fresh endpoint')
                old, new = a, s
            else:
                need(s == a and t not in child_vertices, 'right extension actual fresh endpoint')
                old, new = b, t
            child_adj = adjacency_of(child_vertices, child_edges)
            need(len(child_adj[old]) <= 3, 'actual extension load budget')
            vertices = child_vertices | {new}
            edges = child_edges | {tuple(sorted((old, new)))}
        elif kind in ('S', 'P'):
            need(len(children) == 2, 'binary native join arity')
            left_v, left_e, left_p = sets[children[0]]
            right_v, right_e, right_p = sets[children[1]]
            need(not left_e & right_e, 'child edge overlap')
            if kind == 'S':
                need(left_p[0] == s and right_p[1] == t and left_p[1] == right_p[0],
                     'series port identification')
                junction = left_p[1]
                need(left_v & right_v == {junction}, 'series child interiors are not disjoint')
                shared = [junction]
            else:
                need(left_p == ports and right_p == ports, 'parallel port identification')
                need(left_v & right_v == {s, t}, 'parallel child interiors are not disjoint')
                shared = [s, t]
            left_adj = adjacency_of(left_v, left_e)
            right_adj = adjacency_of(right_v, right_e)
            need(all(len(left_adj[v]) + len(right_adj[v]) <= 4 for v in shared),
                 'actual combined join load exceeds four')
            vertices = left_v | right_v
            edges = left_e | right_e
        else:
            raise ValueError('unknown loaded production')

        need(edges <= original_edges, 'normalization invented a support edge')
        need(s in vertices and t in vertices and tuple(sorted((s, t))) not in edges,
             'module ports not genuinely nonadjacent')
        adjacency = adjacency_of(vertices, edges)
        need(connected(adjacency), 'loaded module disconnected')
        need(all(1 <= len(nbrs) <= 4 for nbrs in adjacency.values()), 'actual module degree range')
        sets.append((vertices, edges, ports))
        trace.append({'node': index, 'kind': kind, 'children': children,
                      'ports': ports, 'port_degrees': [len(adjacency[s]), len(adjacency[t])],
                      'vertices': sorted(vertices), 'edges': [list(e) for e in sorted(edges)],
                      'actual_shared_vertices': shared, 'maximum_degree': max(map(len, adjacency.values()))})

    need(used_as_child[root] == 0 and all(used_as_child[i] == 1 for i in range(len(nodes)) if i != root),
         'native expression is not one rooted tree using each node once')
    root_v, root_e, root_ports = sets[root]
    need(root_v == set(range(n)) and root_e == original_edges, 'root does not preserve complete original support')
    return {'triangle_exception': False, 'loaded_nodes': len(nodes),
            'root_ports': root_ports, 'root_degrees': trace[root]['port_degrees'],
            'each_node_used_once': True, 'all_child_interiors_disjoint': True,
            'all_ports_nonadjacent': True, 'all_actual_degree_budgets_checked': True,
            'root_original_support_exact': True,
            'suppression_trace': suppression, 'node_trace': trace,
            'opaque_metadata_scope': 'Recorded ordinary-node IDs/counts are not used as proof; their original vertex suppression meaning and the complete loaded result are checked independently.'}


def c5_three_color_obstruction():
    """All 3^5 coordinate assignments; scope is star coloring on C5 only."""
    edges = [(i, (i + 1) % 5) for i in range(5)]
    proper = 0
    for colors in product(range(3), repeat=5):
        if any(colors[u] == colors[v] for u, v in edges):
            continue
        proper += 1
        need(any(len({colors[(start + j) % 5] for j in range(4)}) <= 2 for start in range(5)),
             'unexpected star-three coloring of C5')
    return {'assignments': 3 ** 5, 'proper_assignments': proper, 'star_three_assignments': 0,
            'scope': 'Star-coordinate coloring only; no arbitrary-real three-query lower bound.'}


def check_numerical(record, helper):
    graph, q = record['graph'], record['query_count']
    n, colors = graph['n'], graph['colors']
    edges, adjacency, counts = helper.validate_graph(graph, q)
    actual_counts = [[counts[v].get(c, 0) for c in range(4)] for v in range(n)]
    need(actual_counts == graph['actual_neighbor_color_multiplicities']
         == record['graph_check']['actual_neighbor_color_multiplicities'], 'actual color multiplicities')
    need(record['actual_design'] == {'type': 'coordinate', 'colors': colors, 'row_energy_sq': 1},
         'actual full-action row budget')
    need(graph['query_count'] == q == 4, 'native action count')
    need(record['graph_check']['maximum_degree'] == max(map(len, adjacency)), 'saved maximum degree')
    need(record['graph_check']['star'] is True and record['graph_check']['row_energy_sq'] == 1,
         'saved star/row metadata')
    diagonal, values = helper.matrix_source(record['matrix'], n, edges)
    need(all(diagonal) and all(values.values()), 'native fixture must exercise all free coefficients')
    noise = helper.fraction_array(record['noise'], n, q)
    noise_sq = helper.squared_norm(noise)
    need(noise_sq > 0, 'native noise vanished')
    action = helper.full_action(n, q, colors, diagonal, values)
    need(action == helper.fraction_array(record['full_action'], n, q), 'original full action mismatch')
    observed = [[action[v][c] + noise[v][c] for c in range(q)] for v in range(n)]
    need(observed == helper.fraction_array(record['observed_action'], n, q), 'observed original action mismatch')
    clean_d, clean_e, _ = helper.analytic_star_inverse(n, q, colors, edges, action)
    need((clean_d, clean_e) == (diagonal, values), 'native noiseless recovery mismatch')
    recovered_d, recovered_e, components = helper.analytic_star_inverse(n, q, colors, edges, observed)
    saved_d, saved_e = helper.matrix_source(record['output'], n, edges)
    need((recovered_d, recovered_e) == (saved_d, saved_e), 'independent analytic LS output mismatch')
    projected = helper.full_action(n, q, colors, recovered_d, recovered_e)
    need(projected == helper.fraction_array(record['projected_action'], n, q), 'saved projection mismatch')
    residual = [[observed[v][c] - projected[v][c] for c in range(q)] for v in range(n)]
    need(all(residual[v][colors[v]] == 0 for v in range(n)), 'diagonal LS normal equation')
    need(all(residual[u][colors[v]] + residual[v][colors[u]] == 0 for u, v in edges),
         'edge LS normal equation')
    delta = [[F(0) for _ in range(n)] for _ in range(n)]
    for v in range(n):
        delta[v][v] = recovered_d[v] - diagonal[v]
    for (u, v), value in recovered_e.items():
        delta[u][v] = delta[v][u] = value - values[u, v]
    error_sq = helper.squared_norm(delta)
    need(error_sq <= 2 * noise_sq, 'native Frobenius bound')
    psd = [[(F(3, 2) * noise_sq if i == j else F(0))
            - sum((delta[i][k] * delta[k][j] for k in range(n)), F(0))
            for j in range(n)] for i in range(n)]
    pivots = helper.ldl_certificate(psd)
    checks = record['exact_checks']
    need(checks['noiseless_equality'] is True and F(checks['projected_action_residual_sq']) == 0,
         'saved native equality/residual')
    need(F(checks['noise_norm_sq']) == noise_sq and F(checks['error_frobenius_sq']) == error_sq,
         'saved native norm')
    need(F(checks['operator_constant_sq']) == F(3, 2) and F(checks['frobenius_constant_sq']) == 2,
         'saved native bound constants')
    need(list(map(F, checks['operator_psd_pivots'])) == pivots, 'saved native exact PSD pivots')
    need(checks['operator_psd_matrix'] == '(3/2)*||E||F^2*I - (Dhat-D)^2', 'saved native PSD label')
    need(record['graph_check']['all_noise_operator_constant_sq'] == '3/2'
         and record['graph_check']['all_noise_frobenius_constant_sq'] == '2', 'graph-check bound constants')
    return {'full_original_action_noise_and_observation_matched': True,
            'all_free_diagonals_and_edges_exercised': True,
            'independent_analytic_star_LS_matched': True, 'noiseless_recovery_exact': True,
            'projected_action_and_normal_equations_exact': True,
            'coordinate_row_energy_sq': 1, 'queries': q,
            'noise_norm_sq': str(noise_sq), 'error_frobenius_sq': str(error_sq),
            'raw_observation_residual_sq': str(helper.squared_norm(residual)),
            'projected_action_residual_sq': '0',
            'PSD_matrix': '(3/2)*||E||F^2*I - (Dhat-D)^2',
            'PSD_pivots': list(map(str, pivots)),
            'PSD_LDL_full_reconstruction_checked': True,
            'PSD_all_pivots_strictly_positive': all(p > 0 for p in pivots),
            'bichromatic_star_components': components}


def run(root):
    start, cpu = time.perf_counter(), time.process_time()
    native = json.loads(read_bound(root, 'inputs/native_atom_9.json'))
    record = json.loads(read_bound(root, 'results/native_atom_9_four_action.json'))
    branches = json.loads(read_bound(root, 'results/native_atom_branch_checks.json'))
    read_bound(root, 'verification/receiving/verify_receiving.py')
    spec = importlib.util.spec_from_file_location('independent_receiving_helpers',
        root / 'verification/receiving/verify_receiving.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    need(record['schema'] == 'astra-loaded-star-full-action-receiving/v1', 'native receiving schema')
    graph = record['graph']
    need(graph['original_native_input'] == native, 'native source object binding')
    need(not any(k in native for k in ('nodes', 'root', 'spec', 'expression')),
         'native original unexpectedly contains an expression')
    n = native['n']
    edges = canonical_edges(n, native['edges'])
    need(graph['n'] == n and graph['edges'] == [list(e) for e in sorted(edges)], 'original IDs/support changed')
    original_class = graph_class(n, edges)
    need(original_class['triangle_free'], 'native receiving support not triangle-free')
    normal = validate_normal_form(graph['native_normal_form'], n, edges)
    need(graph['terminals'] == normal['root_ports'] and graph['terminal_degrees'] == normal['root_degrees'],
         'normal-form root/receiving port binding')
    need([0, 2, 8, 6, 5] in original_class['cycles'], 'specified native C5 not in actual support')
    numerical = check_numerical(record, helper)

    branch_rows = {}
    need(set(branches) == {'cycle', 'triangle'}, 'branch record cases')
    for name in ('cycle', 'triangle'):
        item = branches[name]
        bn = item['n']
        be = canonical_edges(bn, item['edges'])
        if name == 'cycle':
            need(bn == 5 and be == {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}, 'cycle branch source')
        else:
            need(bn == 3 and be == set(combinations(range(3), 2)), 'triangle branch source')
        bclass = graph_class(bn, be)
        bnormal = validate_normal_form(item['native_normal_form'], bn, be)
        if name == 'cycle':
            _, badj, counts = helper.validate_graph(item, item['query_count'])
            need(item['query_count'] == 4, 'cycle branch action count')
            need(item['terminals'] == bnormal['root_ports'] and item['terminal_degrees'] == bnormal['root_degrees'],
                 'cycle branch port binding')
            actual = [[counts[v].get(c, 0) for c in range(4)] for v in range(bn)]
            need(actual == item['actual_neighbor_color_multiplicities'], 'cycle branch multiplicities')
            scope = 'Exact C5 support, native loaded normalization and star-four coloring; no new matrix/noise receiving record.'
        else:
            need(item['query_count'] == 3 and item['colors'] == [0, 1, 2], 'triangle identity design')
            scope = 'Exact C3 special branch with X=I3. Symmetrization gives error <=||E||F. No triangle-free sqrt(3/2) argument is used, and no saved matrix/noise receiver is claimed.'
        branch_rows[name] = {'vertices': bn, 'edges': len(be), 'graph_class': bclass,
                             'normalization': bnormal, 'scope': scope}

    obstruction = c5_three_color_obstruction()
    return {'schema': 'astra-cycle8-independent-native-atom-gate/v1', 'status': 'PASS',
            'producer_imports': False, 'previous_receivers_rerun': False, 'finite_gate_rerun': False,
            'source_pins': [{'path': p, 'bytes': size, 'sha256': sha} for p, (size, sha) in PINS.items()],
            'native_source_has_no_expression': True,
            'native_original_vertex_and_edge_identity_exact': True,
            'native_vertices': n, 'native_edges': len(edges),
            'native_graph_class': original_class, 'native_normalization': normal,
            'native_full_action_receiver': numerical, 'distinct_code_branches': branch_rows,
            'C5_star_three_obstruction': obstruction,
            'scope': 'One new native full-action receiver and two structural branch records. All-depth theorem and general algorithm correctness are separate proof obligations; finite diagnostics do not replace them.',
            'cost': {'body_wall_seconds': time.perf_counter() - start,
                     'body_cpu_seconds': time.process_time() - cpu,
                     'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                     'scope': 'Pinned reads, independent helper import, actual normal-form/class checks, one exact full-action receiver, cycle/C3 structural checks, and the 243-assignment C5 test; excludes startup and final receipt serialization.'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'native_vertices': result['native_vertices'],
                      'native_edges': result['native_edges'],
                      'normalization_nodes': result['native_normalization']['loaded_nodes'],
                      'native_cycles': result['native_graph_class']['cycles'],
                      'receiver': {k: v for k, v in result['native_full_action_receiver'].items()
                                   if k not in {'PSD_pivots', 'bichromatic_star_components'}},
                      'cost': result['cost']}, indent=2))
