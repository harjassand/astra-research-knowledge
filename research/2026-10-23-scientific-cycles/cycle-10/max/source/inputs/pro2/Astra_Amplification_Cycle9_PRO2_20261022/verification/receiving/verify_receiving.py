"""Independent Cycle9 full-action receiving and new midpoint-witness check.

Standard library only; no producer imports. Uses original edge sets and
Fraction Gaussian elimination on unsigned-incidence normal equations,
not the producer's projected divergence/subtree algorithm. Does not execute
the accepted star-color obstruction suite or inherited closure gate.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter, defaultdict, deque
from itertools import combinations
import argparse
import hashlib
import json
import resource
import time

F = Fraction
PINS = {
    'inputs/native_K24_obstruction_16.json':
        (1118, '6e14c9ccd31a7bcc111a3ab8376c6bc32f40876be3a730d6c451052ae5f4e5a2'),
    'inputs/native_p3_unequal_branch_27.json':
        (2012, 'b426d10920f003f33242fd6187dd3d5074c8dc8b7b553bcf165e037a0ab53896'),
    'results/native_K24_obstruction_16_receiving.json':
        (30597, '8bed093c685e37380f794445e1b5f7dc89439148c734b0054cf0f1a67544be0c'),
    'results/native_p3_unequal_branch_27_receiving.json':
        (61023, '238e17ba51b64883e7f6a9d35da2eea21b0c5dea1b8ad2b2014d9b24055c761a'),
    'research/root_diagnostic/INPUTS.json':
        (6828, 'da7cdf7f5a83558cb09843efabfe5dddc67fa49827ca56c3e561781eaa457f0b'),
    'results/marked_root_projection.json':
        (26859, '7a0bcde13cead849e1e828bbae564d1f3244f4dc65c9a37b0c173e0fb899fbfc'),
    'sources/cycle8_selected/loaded_star_certificate.json':
        (982625, '63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525'),
    'failed/RECEIVER_ATTEMPT_01.json':
        (763, '2985de5289b4963d2f4e2a222a9d332c936232d8c6513c4ae92a63ff6a859d2b'),
    'failed/block_spider_recovery_vertex_shadowing_v1.py':
        (8337, '28795e7c60ee47938c5d38a59f2d790b01d75261b9ce7acfe5d69f50bc8f595f')
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_bound(root, relative):
    raw = (root / relative).read_bytes()
    size, sha = PINS[relative]
    need(len(raw) == size and hashlib.sha256(raw).hexdigest() == sha, 'source mismatch: ' + relative)
    return raw


def edges_checked(n, raw):
    result = set()
    for edge in raw:
        need(len(edge) == 2, 'edge arity')
        u, v = edge
        need(type(u) is int and type(v) is int and 0 <= u < v < n, 'canonical simple original edge')
        need((u, v) not in result, 'duplicate support edge')
        result.add((u, v))
    return result


def adjacency(n, edges):
    result = [set() for _ in range(n)]
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return result


def reach(adj, allowed):
    need(allowed, 'empty connectivity request')
    seen, todo = set(), [min(allowed)]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend((adj[v] & allowed) - seen)
    return seen


def recipe_p3():
    """Independent original-ID expansion of the stated four-block input recipe."""
    p = 3
    sizes, parents, slots = [4, 5, 4, 5], [None, 0, 0, 1], [None, 0, 1, 1]
    blocks, edges, fresh = [], set(), 0
    for i, size in enumerate(sizes):
        hubs = list(range(fresh, fresh + p))
        fresh += p
        if parents[i] is None:
            middles = list(range(fresh, fresh + size))
            fresh += size
        else:
            shared = blocks[parents[i]]['middles'][slots[i]]
            middles = [shared] + list(range(fresh, fresh + size - 1))
            fresh += size - 1
        blocks.append({'hubs': hubs, 'middles': middles})
        edges.update(tuple(sorted((h, m))) for h in hubs for m in middles)
    return fresh, edges


def verify_block_form(native, form):
    n = native['n']
    need(type(n) is int and n >= 5, 'native size')
    original = edges_checked(n, native['edges'])
    need(form['schema'] == 'astra-Kpk-native-block-form/v1', 'native form schema')
    need(form['n'] == n and edges_checked(n, form['edges']) == original, 'native form support binding')
    p, blocks = form['p'], form['blocks']
    need(type(p) is int and p >= 2 and blocks, 'common p or empty block family')
    count = len(blocks)
    membership = [[] for _ in range(n)]
    edge_uses = Counter()
    all_hubs, all_middles, block_sets = set(), set(), []
    for b, block in enumerate(blocks):
        hubs, mids = block['hubs'], block['middles']
        need(hubs == sorted(set(hubs)) and mids == sorted(set(mids)), 'canonical roles')
        need(len(hubs) == p and len(mids) > p and not set(hubs) & set(mids), 'Kpk role sizes')
        vertices = set(hubs) | set(mids)
        need(all(type(v) is int and 0 <= v < n for v in vertices), 'block vertex identity')
        expected = {tuple(sorted((h, m))) for h in hubs for m in mids}
        actual = edges_checked(n, block['edges'])
        need(actual == expected, 'actual block not complete bipartite Kpk')
        need(actual <= original, 'block invented support')
        edge_uses.update(actual)
        for v in vertices:
            membership[v].append(b)
        all_hubs.update(hubs)
        all_middles.update(mids)
        block_sets.append(vertices)
    need(set(edge_uses) == original and set(edge_uses.values()) == {1}, 'native block edge partition')
    need(not all_hubs & all_middles and all_hubs | all_middles == set(range(n)), 'global role partition')
    need(membership == form['membership'] and all(1 <= len(ids) <= 2 for ids in membership),
         'actual block memberships')
    expected_joins, block_adj = [], [set() for _ in blocks]
    for v, ids in enumerate(membership):
        if len(ids) == 2:
            need(all(v in set(blocks[b]['middles']) for b in ids), 'shared vertex not middle on both sides')
            left, right = ids
            need(right not in block_adj[left], 'blocks meet at more than one vertex')
            block_adj[left].add(right)
            block_adj[right].add(left)
            expected_joins.append({'vertex': v, 'blocks': ids})
    need(expected_joins == form['joins'], 'native join list differs')
    for left, right in combinations(range(count), 2):
        shared = block_sets[left] & block_sets[right]
        need(len(shared) <= 1, 'child block interiors overlap')
        need(bool(shared) == (right in block_adj[left]), 'block intersection omitted')
    need(sum(map(len, block_adj)) == 2 * (count - 1), 'block intersection not a tree')
    need(reach(block_adj, set(range(count))) == set(range(count)), 'block tree disconnected')
    root = form['root']
    need(type(root) is int and 0 <= root < count, 'native block root')
    parent, depth = [-2] * count, [-1] * count
    parent[root], depth[root] = -1, 0
    queue = deque([root])
    while queue:
        b = queue.popleft()
        for child in sorted(block_adj[b]):
            if depth[child] < 0:
                parent[child], depth[child] = b, depth[b] + 1
                queue.append(child)
    need(parent == form['parent'] and depth == form['depth'], 'rooted parent/depth mismatch')
    order = form['order']
    need(sorted(order) == list(range(count)) and order[0] == root, 'native traversal order')
    position = {v: i for i, v in enumerate(order)}
    need(all(parent[b] < 0 or position[parent[b]] < position[b] for b in range(count)), 'child precedes parent')
    adj = adjacency(n, original)
    need(reach(adj, set(range(n))) == set(range(n)), 'native graph disconnected')
    need(form['max_degree'] == max(map(len, adj)), 'native maximum degree metadata')
    cuts = []
    for v in range(n):
        remaining = set(range(n)) - {v}
        if reach(adj, remaining) != remaining:
            cuts.append(v)
    need(cuts == [v for v in range(n) if len(membership[v]) == 2], 'actual cut vertices differ from block joins')

    # Each complete Kpk is two-connected. The verified intersection tree and
    # cut vertices make these the actual maximal two-connected blocks.
    # Build and verify a separate original-vertex width-p bag tree.
    bags, bag_edges, lookup = [], [], {}
    for b, block in enumerate(blocks):
        first = len(bags)
        for m in block['middles']:
            index = len(bags)
            bags.append(block['hubs'] + [m])
            lookup[b, m] = index
            if index != first:
                bag_edges.append((first, index))
    for join in expected_joins:
        a, b = join['blocks']
        bag_edges.append(tuple(sorted((lookup[a, join['vertex']], lookup[b, join['vertex']]))))
    badj = adjacency(len(bags), bag_edges)
    need(len(bag_edges) == len(bags) - 1 and reach(badj, set(range(len(bags)))) == set(range(len(bags))),
         'width-p bag graph not a tree')
    need(all(len(b) == p + 1 for b in bags), 'width-p bag size')
    need(all(any(u in bag and v in bag for bag in bags) for u, v in original), 'bag edge coverage')
    for v in range(n):
        ids = {i for i, bag in enumerate(bags) if v in bag}
        need(ids and reach(badj, ids) == ids, 'bag running intersection')

    chorded_cycle = None
    if p >= 3:
        h = blocks[0]['hubs'][:3]
        m = blocks[0]['middles'][:3]
        cycle = [h[0], m[0], h[1], m[1], h[2], m[2]]
        cyc_edges = {tuple(sorted((cycle[i], cycle[(i + 1) % 6]))) for i in range(6)}
        chord = tuple(sorted((h[0], m[1])))
        need(cyc_edges <= original and chord in original - cyc_edges, 'p>=3 chorded cycle witness')
        chorded_cycle = {'cycle': cycle, 'chord': list(chord)}
    return original, {'p': p, 'blocks': count, 'block_sizes': [len(b['middles']) for b in blocks],
        'maximal_block_partition_exact': True, 'all_original_edges_once': True,
        'middle_only_cut_vertices': cuts, 'at_most_two_blocks_per_vertex': True,
        'root': root, 'parent': parent, 'depth': depth,
        'triangle_free_global_hub_middle_bipartition': True,
        'maximum_degree': max(map(len, adj)),
        'width_p_bags': bags, 'width_p_bag_edges': [list(e) for e in bag_edges],
        'p_ge_3_chorded_cycle_witness': chorded_cycle}


def color_components(n, edges, colors, q):
    need(len(colors) == n and all(type(c) is int and 0 <= c < q for c in colors), 'query dimensions/palette')
    need(set(colors) == set(range(q)), 'unused claimed query in actual fixture')
    need(all(colors[u] != colors[v] for u, v in edges), 'improper coordinate design')
    result = []
    for pair in combinations(range(q), 2):
        pe = {e for e in edges if tuple(sorted((colors[e[0]], colors[e[1]]))) == pair}
        if not pe:
            continue
        adj = adjacency(n, pe)
        unseen = {v for edge in pe for v in edge}
        while unseen:
            todo, vertices = [min(unseen)], set()
            while todo:
                v = todo.pop()
                if v not in vertices:
                    vertices.add(v)
                    todo.extend(adj[v] - vertices)
            ce = {e for e in pe if e[0] in vertices}
            need(len(ce) == len(vertices) - 1, 'bichromatic component not a tree')
            unseen -= vertices
            result.append({'pair': pair, 'vertices': vertices, 'edges': ce})
    need(set().union(*(c['edges'] for c in result)) == edges, 'color components omit edge')
    return result


def verify_design(form, design, edges):
    n, p = form['n'], form['p']
    mode, q, colors = design['mode'], design['q'], design['colors']
    need(mode in ('stable', 'star'), 'unknown design mode')
    expected_q = p + 2 if mode == 'stable' else 2 * p + 1
    need(q == expected_q, 'actual action count differs from parameter')
    expected = [-1] * n
    for b, block in enumerate(form['blocks']):
        parity = form['depth'][b] % 2
        for h, v in enumerate(block['hubs']):
            expected[v] = h if mode == 'stable' else h + p * parity
    for v, ids in enumerate(form['membership']):
        if expected[v] >= 0:
            continue
        closest = min(ids, key=lambda b: form['depth'][b])
        expected[v] = p + form['depth'][closest] % 2 if mode == 'stable' else 2 * p
    need(expected == colors, 'actual original-ID parity design mismatch')
    components = color_components(n, edges, colors, q)
    remaining = {(c['pair'], tuple(sorted(c['vertices']))): c for c in components}
    arms_summary = []
    for witness in design['component_witnesses']:
        pair, center, arms = tuple(witness['pair']), witness['center'], witness['arms']
        need(len(pair) == 2 and pair[0] < pair[1], 'component witness pair')
        need(type(center) is int and 0 <= center < n, 'component center')
        used = {center}
        expected_edges = set()
        for arm in arms:
            need(1 <= len(arm) <= (2 if mode == 'stable' else 1), 'arm too long for claimed mode')
            need(len(set(arm)) == len(arm) and not set(arm) & used, 'spider arms overlap')
            need(all(type(v) is int and 0 <= v < n for v in arm), 'arm vertex identity')
            walk = [center] + arm
            expected_edges.update(tuple(sorted((walk[i], walk[i + 1]))) for i in range(len(arm)))
            used.update(arm)
        key = pair, tuple(sorted(used))
        need(key in remaining, 'component witness is missing, duplicate, or has invented vertices')
        actual = remaining.pop(key)
        need(actual['edges'] == expected_edges and witness['vertices'] == len(used), 'component arm support mismatch')
        arms_summary.append({'pair': list(pair), 'center': center, 'arm_lengths': list(map(len, arms)),
                             'vertices': len(used), 'edges': len(expected_edges)})
    need(not remaining, 'actual color component lacks shape witness')
    guarantee = design['guarantee']
    if mode == 'stable':
        need(guarantee == {'operator_constant_sq': '3+sqrt(5)', 'frobenius_constant_sq': '3+sqrt(5)',
                           'theorem': 'spider-arm-Poincare'}, 'stable guarantee metadata')
    else:
        need(guarantee == {'operator_constant_sq': '3/2', 'frobenius_constant_sq': '2',
                           'theorem': 'star-LS-and-triangle-free-dual'}, 'star guarantee metadata')
    return components, {'mode': mode, 'queries': q, 'coordinate_row_energy_sq': 1,
                        'original_ID_parity_rule_exact': True, 'all_components_verified': True,
                        'components': arms_summary,
                        'maximum_component_vertices': max(len(c['vertices']) for c in components)}


def fraction_grid(data, n, q):
    need(len(data) == n and all(len(row) == q for row in data), 'action/noise array shape')
    return [[F(x) for x in row] for row in data]


def matrix_values(diagonal, raw_edges, n, edges):
    result_d = list(map(F, diagonal))
    need(len(result_d) == n, 'diagonal shape')
    result_e = {}
    for u, v, value in raw_edges:
        need((u, v) in edges and (u, v) not in result_e, 'matrix edge support')
        result_e[u, v] = F(value)
    need(set(result_e) == edges, 'matrix omits original coefficient')
    return result_d, result_e


def full_action(n, q, colors, diagonal, values):
    result = [[F(0) for _ in range(q)] for _ in range(n)]
    for v in range(n):
        result[v][colors[v]] += diagonal[v]
    for (u, v), value in values.items():
        result[u][colors[v]] += value
        result[v][colors[u]] += value
    return result


def normal_solve(gram, rhs):
    """Exact elimination of an independent incidence normal system."""
    k = len(rhs)
    rows = [[F(x) for x in gram[i]] + [F(rhs[i])] for i in range(k)]
    for col in range(k):
        pivot = rows[col][col]
        need(pivot > 0, 'nonpositive incidence Gram pivot')
        rows[col] = [x / pivot for x in rows[col]]
        for row in range(col + 1, k):
            scale = rows[row][col]
            if scale:
                rows[row] = [rows[row][j] - scale * rows[col][j] for j in range(k + 1)]
    solution = [F(0)] * k
    for row in reversed(range(k)):
        solution[row] = rows[row][-1] - sum((rows[row][j] * solution[j] for j in range(row + 1, k)), F(0))
    need(all(sum((F(gram[i][j]) * solution[j] for j in range(k)), F(0)) == rhs[i] for i in range(k)),
         'independent normal-equation solution failed substitution')
    return solution


def least_squares(n, colors, components, action):
    diagonal = [action[v][colors[v]] for v in range(n)]
    values = {}
    for component in components:
        edges = sorted(component['edges'])
        endpoints = list(map(set, edges))
        gram = [[len(a & b) for b in endpoints] for a in endpoints]
        rhs = [action[u][colors[v]] + action[v][colors[u]] for u, v in edges]
        solution = normal_solve(gram, rhs)
        for edge, value in zip(edges, solution):
            need(edge not in values, 'inverse assigns edge twice')
            values[edge] = value
    return diagonal, values


def square_sum(rows):
    return sum((v * v for row in rows for v in row), F(0))


def below_three_plus_sqrt5(rational):
    difference = rational - 3
    return difference <= 0 or difference * difference <= 5


def verify_operation(record, operation, original_edges, d, values):
    start, cpu = time.perf_counter(), time.process_time()
    form, design = record['native_form'], operation['design']
    n, q, colors = form['n'], design['q'], design['colors']
    components, structural = verify_design(form, design, original_edges)
    clean = full_action(n, q, colors, d, values)
    need(clean == fraction_grid(operation['original_action'], n, q), 'full original DX mismatch')
    noise = fraction_grid(operation['noise'], n, q)
    observed = [[clean[v][c] + noise[v][c] for c in range(q)] for v in range(n)]
    need(observed == fraction_grid(operation['observed'], n, q), 'original DX+E mismatch')
    clean_d, clean_e = least_squares(n, colors, components, clean)
    need((clean_d, clean_e) == (d, values), 'independent exact noiseless reconstruction')
    found_d, found_e = least_squares(n, colors, components, observed)
    saved_d, saved_e = matrix_values(operation['recovered_diagonal'], operation['recovered_edges'],
                                     n, original_edges)
    need((found_d, found_e) == (saved_d, saved_e), 'independent incidence-LS differs from saved output')
    projection = full_action(n, q, colors, found_d, found_e)
    need(projection == fraction_grid(operation['projected_action'], n, q), 'saved full-action projection mismatch')
    residual = [[observed[v][c] - projection[v][c] for c in range(q)] for v in range(n)]
    need(all(residual[v][colors[v]] == 0 for v in range(n)), 'diagonal projection normal equation')
    need(all(residual[u][colors[v]] + residual[v][colors[u]] == 0 for u, v in original_edges),
         'edge projection normal equation')
    noise_sq, raw_residual_sq = square_sum(noise), square_sum(residual)
    need(noise_sq > 0, 'zero receiving noise')
    error_sq = sum(((a - b) ** 2 for a, b in zip(found_d, d)), F(0))
    error_sq += 2 * sum(((found_e[e] - values[e]) ** 2 for e in original_edges), F(0))
    ratio = error_sq / noise_sq
    if design['mode'] == 'stable':
        need(below_three_plus_sqrt5(ratio), 'stable exact Frobenius bound fails')
        bound = '3+sqrt(5)'
        exact_bound_reason = 'For rational r=error_sq/noise_sq, r<=3 or (r-3)^2<=5 with r>3; no floating sqrt.'
    else:
        need(ratio <= 2, 'star exact Frobenius bound fails')
        # These specific records satisfy the stronger F bound already, so
        # their claimed operator inequality needs no dense floating solve.
        need(ratio <= F(3, 2), 'actual star operator check via Frobenius insufficient')
        bound = '2'
        exact_bound_reason = 'Exact rational Frobenius ratio<=2; in this saved case ratio<=3/2 also certifies the operator bound by op<=F.'
    need(operation['normal_equations_exact'] is True and operation['noiseless_reconstruction_exact'] is True,
         'saved equality metadata')
    need(F(operation['projected_action_residual_sq']) == 0, 'saved projected residual')
    need(F(operation['raw_observation_residual_sq']) == raw_residual_sq, 'saved raw residual norm')
    need(F(operation['noise_frobenius_sq']) == noise_sq, 'saved noise norm')
    need(F(operation['error_frobenius_sq']) == error_sq, 'saved error norm')
    need(F(operation['error_to_noise_frobenius_sq']) == ratio, 'saved error ratio')
    return {'status': 'PASS', 'design_check': structural,
            'full_original_DX_and_DX_plus_E_exact': True,
            'independent_Fraction_incidence_normal_solve': True,
            'noiseless_coefficients_exact': True, 'saved_noisy_coefficients_exact': True,
            'all_projection_normal_equations_exact': True,
            'noise_frobenius_sq': str(noise_sq), 'error_frobenius_sq': str(error_sq),
            'error_to_noise_frobenius_sq': str(ratio),
            'raw_observation_residual_sq': str(raw_residual_sq), 'projected_action_residual_sq': '0',
            'uniform_Frobenius_bound_sq': bound, 'actual_bound_checked_exactly': exact_bound_reason,
            'body_wall_seconds': time.perf_counter() - start,
            'body_cpu_seconds': time.process_time() - cpu}, noise


def verify_receiver(root, stem, diagnostic_input):
    start, cpu = time.perf_counter(), time.process_time()
    input_rel = 'inputs/' + stem + '.json'
    output_rel = 'results/' + stem + '_receiving.json'
    native = json.loads(read_bound(root, input_rel))
    record = json.loads(read_bound(root, output_rel))
    need(record['schema'] == 'astra-block-spider-full-action-receiver/v1', 'receiver schema')
    need(record['input_filename'] == stem + '.json', 'native filename binding')
    need((record['input_bytes'], record['input_sha256']) == PINS[input_rel], 'native byte/hash binding')
    need(native['name'] == record['name'] == stem, 'native name binding')
    need(not any(k in native for k in ('blocks', 'root', 'parent', 'depth', 'colors', 'expression')),
         'native input unexpectedly includes prepared structure')
    original_edges, graph_check = verify_block_form(native, record['native_form'])
    if stem == 'native_K24_obstruction_16':
        old = diagnostic_input['graphs'][2]
        need(native['n'] == old['n'] and native['edges'] == old['edges'], 'same obstruction original support binding')
        need(native['provenance']['sha256'] == PINS['research/root_diagnostic/INPUTS.json'][1]
             and native['provenance']['graph_index'] == 2, 'obstruction source identity')
        need(record['native_form']['p'] == 2, 'p=2 receiver changed')
        source_binding = 'Exact original edge list from pinned accepted obstruction INPUTS, read without rerunning its suite.'
    else:
        expected_n, expected_edges = recipe_p3()
        need(native['n'] == expected_n and original_edges == expected_edges, 'independent p3 recipe binding')
        need(native['provenance']['recipe'] == 'p=3;k=(4,5,4,5);parents=(None,0,0,1);parent_slots=(None,0,1,1)',
             'p3 recipe string changed')
        need(record['native_form']['p'] == 3, 'p=3 receiver changed')
        source_binding = 'Independent original-ID expansion of p=3, unequal k=(4,5,4,5), parents=(None,0,0,1).'
    n = native['n']
    d, values = matrix_values(record['original_diagonal'], record['original_edge_values'], n, original_edges)
    need(len(record['operations']) == 2, 'matched receiver operation count')
    need([op['design']['mode'] for op in record['operations']] == ['stable', 'star'], 'operation modes/order')
    rows, noises = [], []
    for op in record['operations']:
        row, noise = verify_operation(record, op, original_edges, d, values)
        rows.append(row)
        noises.append(noise)
    q_stable, q_star = [op['design']['q'] for op in record['operations']]
    need(q_stable < q_star, 'control does not pay its extra query')
    need(all(noises[1][v] == noises[0][v] + [F(0)] * (q_star - q_stable) for v in range(n)),
         'control noise is not the same array padded by zero columns')
    need(square_sum(noises[0]) == square_sum(noises[1]), 'absolute Frobenius noise differs')
    need(record['same_D_and_absolute_noise_norm'] is True, 'saved matched-control metadata')
    return {'status': 'PASS', 'name': stem,
            'native_input': {'path': input_rel, 'bytes': PINS[input_rel][0], 'sha256': PINS[input_rel][1]},
            'receiving_record': {'path': output_rel, 'bytes': PINS[output_rel][0], 'sha256': PINS[output_rel][1]},
            'vertices': n, 'edges': len(original_edges), 'source_binding': source_binding,
            'native_input_has_no_decomposition_or_coloring': True, 'graph_check': graph_check,
            'same_D_in_both_operations': True, 'same_absolute_Frobenius_noise_entrywise_zero_padding': True,
            'operations': rows,
            'body_wall_seconds': time.perf_counter() - start,
            'body_cpu_seconds': time.process_time() - cpu}


def check_marked_projection(root):
    start, cpu = time.perf_counter(), time.process_time()
    cert_rel = 'sources/cycle8_selected/loaded_star_certificate.json'
    source = json.loads(read_bound(root, cert_rel))
    result = json.loads(read_bound(root, 'results/marked_root_projection.json'))
    need(result['schema'] == 'astra-marked-midpoint-projection/v1', 'new midpoint schema')
    need(result['predecessor_certificate_sha256'] == PINS[cert_rel][1], 'midpoint predecessor binding')
    families = {f['id']: f for f in source['families']}
    active = {i for i, family in families.items() if max(family['degree']) <= 3}
    rows = result['rows']
    need(len(rows) == 66 == result['cases'] == len(active), 'new midpoint case count')
    need(len({r['family'] for r in rows}) == len(rows) and {r['family'] for r in rows} == active,
         'midpoint cases omit or duplicate active family')
    flag_counts = Counter()
    for row in rows:
        family = families[row['family']]
        index = row['target_index']
        need(type(index) is int and 0 <= index < len(family['targets']), 'midpoint target index')
        target = family['targets'][index]
        need(row['inherited_target'] == target and row['degree'] == family['degree'], 'literal inherited target mismatch')
        a, b, dl, nl, fl, dr, nr, fr = target
        need([dl, dr] == family['degree'] and 1 <= dl <= 3 and 1 <= dr <= 3, 'actual insertion degree budgets')
        z = row['root_color']
        need(a != b and type(z) is int and z in set(range(4)) - {a, b}, 'real midpoint path coloring')
        need(not ((fl | fr) & (1 << z)), 'new neighbor color hits an inherited far-repeat hazard')
        flags = ((1 << a) if nl & (1 << z) else 0) | ((1 << b) if nr & (1 << z) else 0)
        need(flags.bit_count() <= 1, 'midpoint has two possible far-repeat flags')
        need(row['root_degree'] == 2 and row['root_neighbor_colors'] == [a, b], 'new midpoint exact root profile')
        need(row['root_flag_upper_mask'] == flags and row['flag_count_upper'] == flags.bit_count(), 'midpoint flag upper bound')
        flag_counts[flags.bit_count()] += 1
    need(result['all_nonempty'] is True, 'midpoint nonempty metadata')
    return {'status': 'PASS', 'new_literal_witnesses_checked': len(rows),
            'active_families_covered_once': True, 'flag_count_upper_histogram': dict(flag_counts),
            'predecessor_hash': PINS[cert_rel][1], 'old_11142_witness_gate_executed': False,
            'scope': 'Conditional on the accepted inherited family guarantees and the proved marked-midpoint structural representation. Checks only the 66 new literal insertions; does not promise simultaneous marks or a new native marked-atom receiver.',
            'body_wall_seconds': time.perf_counter() - start,
            'body_cpu_seconds': time.process_time() - cpu}


def run(root):
    start, cpu = time.perf_counter(), time.process_time()
    diagnostic_input = json.loads(read_bound(root, 'research/root_diagnostic/INPUTS.json'))
    receivers = [verify_receiver(root, stem, diagnostic_input) for stem in
                 ('native_K24_obstruction_16', 'native_p3_unequal_branch_27')]
    projection = check_marked_projection(root)
    failure_raw = read_bound(root, 'failed/RECEIVER_ATTEMPT_01.json')
    failed_source = read_bound(root, 'failed/block_spider_recovery_vertex_shadowing_v1.py')
    failure = json.loads(failure_raw)
    need(failure['status'] == 'failed' and failure['result_written'] is False, 'failed attempt misreported')
    need(failure['source_sha256'] == hashlib.sha256(failed_source).hexdigest(), 'failed source binding')
    need(failure['body_wall_seconds'] is None and failure['body_cpu_seconds'] is None,
         'unknown failed-attempt costs silently replaced')
    return {'schema': 'astra-cycle9-independent-full-action-receiving-check/v1', 'status': 'PASS',
            'producer_imports': False, 'star_obstruction_suite_rerun': False,
            'old_finite_closure_gate_rerun': False, 'receivers': receivers,
            'new_marked_midpoint_projection': projection,
            'preserved_failed_attempt': {'receipt': 'failed/RECEIVER_ATTEMPT_01.json',
                'source': failure['source_file'], 'source_sha256': failure['source_sha256'],
                'cause': failure['cause'], 'cost_status': 'Uninstrumented failed body cost is unknown, not zero.',
                'failed_source_reexecuted': False},
            'cost': {'body_wall_seconds': time.perf_counter() - start,
                     'body_cpu_seconds': time.process_time() - cpu,
                     'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                     'scope': 'Pinned source reads, two native graph/recipe/block checks, four independent exact normal-equation receiver operations, paired noise comparison, 66 new marked insertions, and failed-source binding. Excludes startup and final receipt serialization.'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'],
        'receivers': [{'name': r['name'], 'p': r['graph_check']['p'],
                      'operations': [{'q': o['design_check']['queries'],
                                      'error_to_noise_frobenius_sq': o['error_to_noise_frobenius_sq'],
                                      'raw_observation_residual_sq': o['raw_observation_residual_sq'],
                                      'projected_action_residual_sq': o['projected_action_residual_sq']}
                                     for o in r['operations']]} for r in result['receivers']],
        'projection': result['new_marked_midpoint_projection'], 'cost': result['cost']}, indent=2))
