#!/usr/bin/env python3
"""Exact, independent receiving check of coordinate_operations.json.

No producer module is imported. All mathematical input arithmetic is Fraction.
The decoder below forms and solves tiny incidence normal equations directly;
the 254-vertex cut witness is checked by direct sparse action evaluation.
This checks supplied concrete fixtures, not an all-size theorem or novelty.
"""
from collections import Counter, defaultdict, deque
from fractions import Fraction as F
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def graph(n, edges):
    result = []
    seen = set()
    for uv in edges:
        require(len(uv) == 2, "Edge arity")
        u, v = uv
        require(type(u) is int and type(v) is int and 0 <= u < v < n,
                "Canonical edge bounds")
        require((u, v) not in seen, "Duplicate edge")
        seen.add((u, v))
        result.append((u, v))
    return result


def coefficients(n, edges, diagonal, edge_values):
    require(len(diagonal) == n, "Diagonal length")
    diag = [F(v) for v in diagonal]
    values = {}
    for u, v, value in edge_values:
        require((u, v) in edges and (u, v) not in values,
                "Coefficient support or uniqueness")
        values[u, v] = F(value)
    require(set(values) == set(edges), "Complete off-diagonal coefficients")
    return diag, values


def matrix_data(n, q, rows):
    require(len(rows) == n and all(len(row) == q for row in rows),
            "Action/noise shape")
    return [[F(v) for v in row] for row in rows]


def coordinate_action(n, q, colors, diagonal, values):
    """Direct summation of all symmetric coefficients into action cells."""
    require(len(colors) == n and all(type(c) is int and 0 <= c < q for c in colors),
            "Color bounds")
    y = [[F(0) for _ in range(q)] for _ in range(n)]
    for i, value in enumerate(diagonal):
        y[i][colors[i]] += value
    for (u, v), value in values.items():
        y[u][colors[v]] += value
        y[v][colors[u]] += value
    return y


def norm_sq(rows):
    return sum((v*v for row in rows for v in row), F(0))


def matrix_frobenius_sq(diagonal, values):
    return sum((x*x for x in diagonal), F(0)) + 2*sum((x*x for x in values.values()), F(0))


def components(edges, colors):
    """Discover pair-color components independently by breadth-first search."""
    grouped = defaultdict(list)
    for u, v in edges:
        require(colors[u] != colors[v], "Improper coloring prevents free diagonal recovery")
        grouped[tuple(sorted((colors[u], colors[v])))].append((u, v))
    output = []
    for pair, pair_edges in sorted(grouped.items()):
        adj = defaultdict(list)
        for u, v in pair_edges:
            adj[u].append(v)
            adj[v].append(u)
        unseen = set(adj)
        while unseen:
            start = min(unseen)
            vertices = {start}
            queue = deque([start])
            unseen.remove(start)
            while queue:
                u = queue.popleft()
                for v in adj[u]:
                    if v not in vertices:
                        vertices.add(v)
                        unseen.remove(v)
                        queue.append(v)
            local_edges = sorted((u, v) for u, v in pair_edges if u in vertices)
            require(len(local_edges) == len(vertices)-1,
                    "Bichromatic component is not a tree")
            output.append((pair, sorted(vertices), local_edges))
    return output


def exact_solve(a, b):
    """Gauss-Jordan elimination, independent of the producer's decoder."""
    m = len(a)
    require(m == len(b) and all(len(row) == m for row in a), "Square system")
    augmented = [list(map(F, row)) + [F(rhs)] for row, rhs in zip(a, b)]
    for column in range(m):
        pivot = next((r for r in range(column, m) if augmented[r][column]), None)
        require(pivot is not None, "Singular incidence normal system")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        p = augmented[column][column]
        augmented[column] = [x/p for x in augmented[column]]
        for r in range(m):
            if r != column:
                factor = augmented[r][column]
                augmented[r] = [x-factor*y for x, y in zip(augmented[r], augmented[column])]
    return [row[-1] for row in augmented]


def gram(local_edges):
    return [[F(len(set(a).intersection(b))) for b in local_edges] for a in local_edges]


def exact_psd(a):
    """Rational symmetric Schur-complement test, including zero pivots."""
    a = [list(map(F, row)) for row in a]
    m = len(a)
    require(all(len(row) == m for row in a), "PSD shape")
    require(all(a[i][j] == a[j][i] for i in range(m) for j in range(m)), "PSD symmetry")
    for k in range(m):
        pivot = a[k][k]
        require(pivot >= 0, "Negative Schur pivot")
        if not pivot:
            require(all(a[k][j] == 0 for j in range(k+1, m)), "Zero pivot with nonzero row")
            continue
        for i in range(k+1, m):
            for j in range(k+1, m):
                a[i][j] -= a[i][k]*a[k][j]/pivot
    return True


def decode(n, colors, blocks, action):
    diagonal = [action[i][colors[i]] for i in range(n)]
    values = {}
    for pair, vertices, local_edges in blocks:
        # Row u of the unsigned incidence equation is action[u, other color].
        target = {u: action[u][pair[1] if colors[u] == pair[0] else pair[0]]
                  for u in vertices}
        rhs = [target[u]+target[v] for u, v in local_edges]
        solution = exact_solve(gram(local_edges), rhs)
        values.update(zip(local_edges, solution))
    return diagonal, values


def check_case(case):
    n, q = case['n'], case['q']
    edges = graph(n, case['edges'])
    colors = case['colors']
    diagonal, values = coefficients(n, set(edges), case['diagonal'], case['edge_values'])
    action = coordinate_action(n, q, colors, diagonal, values)
    blocks = components(edges, colors)
    require(all(action[i][colors[i]] == diagonal[i] for i in range(n)),
            "Free diagonal action cells")
    require(decode(n, colors, blocks, action) == (diagonal, values), "Noiseless reconstruction")
    noise = matrix_data(n, q, case['noise'])
    noisy = [[a+e for a, e in zip(row, err)] for row, err in zip(action, noise)]
    out_d, out_e = decode(n, colors, blocks, noisy)
    saved_d, saved_e = coefficients(n, set(edges), case['decoded_diagonal'], case['decoded_edges'])
    require((out_d, out_e) == (saved_d, saved_e), "Saved noisy output differs")
    noise_sq = norm_sq(noise)
    error_sq = matrix_frobenius_sq([a-b for a, b in zip(out_d, diagonal)],
                                   {e: out_e[e]-values[e] for e in edges})
    c2 = F(case['verified_constant_sq'])
    require(noise_sq == F(case['noise_norm_sq']), "Saved noise squared norm")
    require(error_sq == F(case['error_frobenius_sq']), "Saved error squared norm")
    require(error_sq <= c2*noise_sq, "Exact fixture Frobenius inequality")
    # This also checks the global decoder bound for every noise on this fixed
    # graph/seed: 2||B^+||^2 <= c2 on each disjoint action block; diagonal norm 1.
    require(c2 >= 1, "Diagonal noise bound")
    for _, _, local_edges in blocks:
        g = gram(local_edges)
        exact_psd([[c2*g[i][j]/2 - F(i == j)
                    for j in range(len(g))] for i in range(len(g))])
    maximum = max((len(vs) for _, vs, _ in blocks), default=0)
    require(maximum == case['maximum_component_size'], "Saved maximum component size")
    name = case['name']
    if name.startswith('period9'):
        word = [0, 1, 2, 0, 3, 1, 0, 2, 3]
        require(q == 4 and colors == [word[i % 9] for i in range(n)], "Period-nine seed")
        require(all(v-u <= 2 for u, v in edges), "Bandwidth-two support")
        if name == 'period9_full':
            require(set(edges) == {(i,j) for i in range(n) for j in range(i+1,min(n,i+3))},
                    "Full squared path support")
        require(maximum <= 5, "Period-nine component size")
        for _, _, es in blocks:
            degree = Counter(v for e in es for v in e)
            require(max(degree.values()) <= 2, "Period-nine components must be paths")
    elif name == 'period5_comparator':
        require(q == 5 and colors == [i % 5 for i in range(n)], "Period-five seed")
        require(all(len(es) == 1 for _, _, es in blocks), "Comparator components must be matchings")
        require(norm_sq(action) == matrix_frobenius_sq(diagonal, values), "Exact matching isometry")
        # Symbolic isometry: each coefficient occupies its own cells; diagonals
        # appear once and every off-diagonal appears twice with no collisions.
        cells = [(i, colors[i]) for i in range(n)]
        cells += [(u, colors[v]) for u,v in edges] + [(v, colors[u]) for u,v in edges]
        require(len(cells) == len(set(cells)), "Symbolic isometry action-cell collision")
    elif name == 'prism_good':
        require(q == 4, "Prism query count")
        for _, _, es in blocks:
            degree = Counter(v for e in es for v in e)
            require(sum(d > 1 for d in degree.values()) <= 1, "Good prism component is not a star")
    else:
        raise AssertionError('Unexpected fixed operation name')
    return {'name': name, 'n': n, 'edges': len(edges), 'queries': q,
            'bichromatic_components': len(blocks), 'maximum_component_size': maximum,
            'maximum_exact_system_order': max((len(es) for _,_,es in blocks), default=0),
            'noise_norm_sq': str(noise_sq), 'error_frobenius_sq': str(error_sq),
            'constant_sq': str(c2), 'noiseless': 'PASS', 'saved_noisy_output': 'PASS',
            'all_noise_fixed_graph_block_inequality': 'PASS'}


def check_witness(witness, prism_case):
    n, q = witness['n'], witness['q']
    require((n,q) == (254,4), "Pinned prism dimensions")
    edges = graph(n, witness['edges'])
    diag, values = coefficients(n, set(edges), witness['diagonal'], witness['edge_values'])
    parents = witness['parents']
    require(n == 2*len(parents) and parents[0] is None, "Prism base dimensions")
    expected = {(2*i,2*i+1) for i in range(len(parents))}
    for i, p in enumerate(parents[1:],1):
        require(type(p) is int and 0 <= p < i, "Rooted-tree parent")
        expected.update(((2*p,2*i),(2*p+1,2*i+1)))
    require(set(edges) == expected, "Two tree layers and matching rungs")
    require(set(edges) == set(map(tuple,prism_case['edges']))
            and witness['good_colors'] == prism_case['colors'], "Same support and good seed")
    degree = Counter(v for e in edges for v in e)
    require(max(degree.values()) == 4, "Prism maximum degree four")
    action = {}
    action_norms = {}
    component_sizes = {}
    for seed in ('bad','good'):
        colors = witness[seed+'_colors']
        blocks = components(edges, colors)
        component_sizes[seed] = max(len(vs) for _,vs,_ in blocks)
        action[seed] = coordinate_action(n,q,colors,diag,values)
        require(action[seed] == matrix_data(n,q,witness[seed+'_action']), "Saved witness action")
        action_norms[seed] = norm_sq(action[seed])
        require(action_norms[seed] == F(witness[seed+'_action_norm_sq']), "Saved witness action norm")
    require(action_norms['bad'] == F(127,4032), "Pinned bad action squared norm")
    require(action_norms['good'] == F(3167639,451584), "Pinned good action squared norm")
    cut = tuple(witness['cut_edge'])
    require(cut in values and abs(values[cut]) == 1, "Unit cut entry operator witness")
    require(F(witness['operator_norm_lower']) == 1, "Pinned operator lower bound")
    require(F(witness['inverse_lower_sq']) == 1/action_norms['bad'] == F(4032,127),
            "Inverse lower squared ratio")
    require(all(d == 0 for d in diag), "Witness diagonal zero")
    require(all(value == 0 for (u,v),value in values.items() if u%2 or v%2),
            "Witness supported on one tree layer")
    # Independently split that tree at the cut, and check the action magnitude
    # 1/a or 1/b on every vertex on its respective side.
    adj = defaultdict(list)
    for u,v in edges:
        if u%2 == v%2 == 0 and (u,v) != cut:
            adj[u].append(v)
            adj[v].append(u)
    reached = {cut[1]}
    queue = deque([cut[1]])
    while queue:
        for v in adj[queue.popleft()]:
            if v not in reached:
                reached.add(v)
                queue.append(v)
    other = set(range(0,n,2))-reached
    a,b = len(reached),len(other)
    require((a,b) == (witness['a'],witness['b']) == (63,64), "Independent cut sizes")
    for vertices,size in ((reached,a),(other,b)):
        for v in vertices:
            nonzero = [abs(x) for x in action['bad'][v] if x]
            require(nonzero == [F(1,size)], "Exact cut-load magnitudes")
    require(all(all(x == 0 for x in action['bad'][v]) for v in range(1,n,2)),
            "Unloaded layer action")
    require(action_norms['bad'] == F(1,a)+F(1,b), "Cut norm identity")
    return {'n':n,'edges':len(edges),'maximum_degree':max(degree.values()),
            'cut_edge':list(cut),'cut_sizes':[a,b],'absolute_cut_entry':'1',
            'bad_action_norm_sq':str(action_norms['bad']),
            'good_action_norm_sq':str(action_norms['good']),
            'inverse_lower_sq':str(1/action_norms['bad']),
            'maximum_bichromatic_component_sizes':component_sizes,
            'scope':'A bad seed on a graph with a verified good seed; no all-design lower bound.',
            'status':'PASS'}


def check_cycle(case):
    n,q = case['n'],case['q']
    edges = graph(n,case['edges'])
    diagonal,values = coefficients(n,set(edges),case['diagonal'],case['edge_values'])
    require(n == 4 and len(edges) == 4 and len(set(case['colors'])) == 2,
            "Pinned bichromatic C4")
    require(all(case['colors'][u] != case['colors'][v] for u,v in edges), "C4 proper coloring")
    action = coordinate_action(n,q,case['colors'],diagonal,values)
    require(norm_sq(action) == 0 and matrix_frobenius_sq(diagonal,values) == 8,
            "Exact nonzero C4 kernel")
    rejected = False
    try:
        components(edges,case['colors'])
    except AssertionError as error:
        require(str(error) == 'Bichromatic component is not a tree', "Unexpected C4 rejection")
        rejected = True
    require(rejected, "Decoder must reject bicolored cycle")
    return {'nonzero_matrix_frobenius_sq':'8','action_norm_sq':'0',
            'forest_decoder_rejection':'PASS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1]/'results'/'coordinate_operations.json')
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('independent_coordinate_result.json'))
    arguments = parser.parse_args()
    source, target = arguments.input, arguments.output
    wall = time.perf_counter()
    cpu = time.process_time()
    raw = source.read_bytes()
    data = json.loads(raw)
    require(data['counts']['fixed_operation_cases'] == len(data['cases']) == 4, "Fixed case count")
    require({c['name'] for c in data['cases']} == {'period9_full','period9_subsupport','period5_comparator','prism_good'},
            "Pinned fixture names")
    case_results = [check_case(case) for case in data['cases']]
    prism_case = next(case for case in data['cases'] if case['name'] == 'prism_good')
    witness_result = check_witness(data['same_graph_witness'],prism_case)
    cycle_result = check_cycle(data['cycle_kernel'])
    result = {'status':'PASS','checker':'independent_coordinate_check.py',
              'producer_code_imported':False,'mathematical_arithmetic':'fractions.Fraction only',
              'input_filename':source.name,'input_bytes':len(raw),
              'input_sha256':hashlib.sha256(raw).hexdigest(),
              'cases':case_results,'same_graph_witness':witness_result,'cycle_kernel':cycle_result,
              'costs':{'body_wall_seconds':time.perf_counter()-wall,
                       'body_cpu_seconds':time.process_time()-cpu,
                       'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                       'actual_verification_runs':1,
                       'exclusions':'Process startup, initial JSON inspection, checker authoring, prior literature research, parent integration and delivery are additional.'},
              'scope':'Independent exact concrete-data and block-norm verification. This is not a historical-novelty or universal-graph theorem check.'}
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
