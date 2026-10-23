"""Native four-color short-arm recovery design for theta-block trees.

The original simple graph is recognized. All selected hubs and deletions are
internal coloring devices: this file returns the original graph and four-row
coordinate colors. No original edge is discarded from recovery.

Iterative block decomposition follows the standard low-link procedure also
used in Cycle9; the theta recognizer, hub choice and sparse color correction
are the new construction. Canonical sorting costs O(n+m log m).
"""
from collections import defaultdict, deque


def theta_form(n, edges):
    if type(n) is not int or n < 5:
        raise ValueError('nontrivial theta-block tree required')
    es = []
    for e in edges:
        if (not isinstance(e, (list, tuple)) or len(e) != 2 or
                any(type(v) is not int for v in e)):
            raise ValueError('integer edge pair required')
        u, v = sorted(e)
        if not 0 <= u < v < n:
            raise ValueError('original simple support required')
        es.append((u, v))
    es.sort()
    if len(set(es)) != len(es):
        raise ValueError('duplicate edge')
    adj = [[] for _ in range(n)]
    for u, v in es:
        adj[u].append(v); adj[v].append(u)
    if any(not a for a in adj):
        raise ValueError('connected support required')
    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    disc[0] = low[0] = 0
    timer = 1
    stack = [(0, iter(adj[0]))]
    edge_stack, raw = [], []
    while stack:
        u, it = stack[-1]
        v = next(it, None)
        if v is not None:
            if disc[v] == -1:
                parent[v] = u
                disc[v] = low[v] = timer; timer += 1
                edge_stack.append((u, v))
                stack.append((v, iter(adj[v])))
            elif v != parent[u] and disc[v] < disc[u]:
                low[u] = min(low[u], disc[v])
                edge_stack.append((u, v))
            continue
        stack.pop()
        pv = parent[u]
        if pv == -1:
            continue
        low[pv] = min(low[pv], low[u])
        if low[u] >= disc[pv]:
            be = []
            while True:
                e = edge_stack.pop()
                be.append(tuple(sorted(e)))
                if e == (pv, u):
                    break
            raw.append(sorted(be))
    if timer != n or edge_stack:
        raise ValueError('connected support required')
    raw.sort(key=lambda b: b[0])
    blocks = []
    memberships = [[] for _ in range(n)]
    for be in raw:
        ba = defaultdict(list)
        for u, v in be:
            ba[u].append(v); ba[v].append(u)
        hubs = sorted(v for v in ba if len(ba[v]) != 2)
        if (len(hubs) != 2 or len(ba[hubs[0]]) < 3 or
                len(ba[hubs[0]]) != len(ba[hubs[1]])):
            raise ValueError('each block must have two equal-degree hubs and degree-two interiors')
        a, b = hubs
        paths, seen_interior, used_edges = [], set(), set()
        for start in sorted(ba[a]):
            path = [a, start]
            prev, cur = a, start
            while cur != b:
                if cur == a or cur in seen_interior or len(ba[cur]) != 2:
                    raise ValueError('paths are not internally disjoint theta branches')
                seen_interior.add(cur)
                nxt = ba[cur][0] if ba[cur][1] == prev else ba[cur][1]
                path.append(nxt)
                prev, cur = cur, nxt
            if len(path) < 3:
                raise ValueError('all theta branches must have length at least two')
            for u, v in zip(path, path[1:]):
                used_edges.add(tuple(sorted((u, v))))
            paths.append(path)
        if used_edges != set(be) or len(paths) != len(ba[a]):
            raise ValueError('theta edge coverage failure')
        i = len(blocks)
        for v in ba:
            memberships[v].append(i)
        blocks.append(dict(hubs=hubs, paths=paths, edges=be,
                           adjacency={v: sorted(ns) for v, ns in ba.items()}))
    tree = [[] for _ in blocks]
    for v, ids in enumerate(memberships):
        if not 1 <= len(ids) <= 2:
            raise ValueError('each original vertex belongs to one or two blocks')
        if len(ids) == 2:
            a, b = ids
            if v in blocks[a]['hubs'] or v in blocks[b]['hubs']:
                raise ValueError('hubs must remain unshared')
            tree[a].append((b, v)); tree[b].append((a, v))
    par = [-1] * len(blocks)
    incoming = [None] * len(blocks)
    depth = [-1] * len(blocks)
    order = [0]; depth[0] = 0
    for i in order:
        for j, v in tree[i]:
            if j == par[i]:
                continue
            if depth[j] != -1:
                raise ValueError('block adjacency is not a tree')
            par[j], incoming[j], depth[j] = i, v, depth[i] + 1
            order.append(j)
    if len(order) != len(blocks):
        raise ValueError('disconnected block tree')
    return dict(n=n, edges=es, blocks=blocks, memberships=memberships,
                parent=par, incoming=incoming, depth=depth, order=order,
                max_degree=max(map(len, adj)))


def color_form(form, corrected=True):
    n, blocks = form['n'], form['blocks']
    special = []
    constraints = {}
    for bi, block in enumerate(blocks):
        a, b = block['hubs']
        r = form['incoming'][bi]
        if r is None:
            h = a
        else:
            neighbors = block['adjacency'][r]
            constrained = a in neighbors and b in neighbors
            h = a if constrained or a not in neighbors else b
            if constrained:
                for z in block['adjacency'][h]:
                    if z != r:
                        if z in constraints:
                            raise AssertionError('conflicting rooted constraint')
                        constraints[z] = r
        special.append(h)
    hs = set(special)
    adj = [[] for _ in range(n)]
    for u, v in form['edges']:
        if u not in hs and v not in hs:
            adj[u].append(v); adj[v].append(u)
    root = next(h for h in blocks[0]['hubs'] if h != special[0])
    par = [-2] * n; par[root] = -1
    order = [root]
    for v in order:
        for w in adj[v]:
            if w == par[v]:
                continue
            if par[w] != -2:
                raise AssertionError('deleting selected hubs did not leave a tree')
            par[w] = v; order.append(w)
    if len(order) != n - len(hs):
        raise AssertionError('deleted-hub forest disconnected')
    colors = [-1] * n
    for h in hs:
        colors[h] = 3
    colors[root] = 0
    flips = []
    for v in order[1:]:
        pv = par[v]
        gv = par[pv]
        default = 1 if gv == -1 else 3 - colors[pv] - colors[gv]
        if corrected and v in constraints and default == colors[constraints[v]]:
            if gv < 0 or colors[gv] < 0:
                raise AssertionError('constraint lacks a colored grandparent')
            colors[v] = colors[gv]
            flips.append(v)
        else:
            colors[v] = default
    if any(colors[u] == colors[v] for u, v in form['edges']):
        raise AssertionError('coloring is improper')
    if corrected:
        if any(colors[v] == colors[r] for v, r in constraints.items()):
            raise AssertionError('root transmission constraint failed')
        flipset = set(flips)
        if any(par[v] in flipset for v in flips):
            raise AssertionError('adjacent flips')
        counts = defaultdict(int)
        for v in flips:
            counts[par[v]] += 1
        if any(k > 1 for k in counts.values()):
            raise AssertionError('two flipped children')
    return dict(colors=colors, q=4, special_hubs=special, forest_root=root,
                forest_parent=par, forest_order=order, flips=flips,
                constraints=constraints, corrected=corrected)


def pair_components(n, edges, colors):
    groups = defaultdict(list)
    for u, v in edges:
        if colors[u] == colors[v]:
            raise ValueError('improper coloring')
        groups[tuple(sorted((colors[u], colors[v])))].append((u, v))
    out = []
    for pair, es in sorted(groups.items()):
        adj = defaultdict(list)
        for u, v in es:
            adj[u].append(v); adj[v].append(u)
        seen = set()
        for v in sorted(adj):
            if v in seen:
                continue
            par, order = {v: None}, [v]; seen.add(v)
            for u in order:
                for w in adj[u]:
                    if w == par[u]:
                        continue
                    if w in seen:
                        raise ValueError('bichromatic cycle')
                    seen.add(w); par[w] = u; order.append(w)
            out.append(dict(pair=pair, vertices=order, parent=par,
                            adjacency={u: adj[u] for u in order}))
    return out


def short_arm_witness(component):
    adj = component['adjacency']
    def farthest(start):
        par = {start: None}; order = [start]
        for v in order:
            for w in adj[v]:
                if w != par[v]:
                    par[w] = v; order.append(w)
        return order[-1], par
    a, _ = farthest(component['vertices'][0])
    b, par = farthest(a)
    diameter_path = [b]
    while diameter_path[-1] != a:
        diameter_path.append(par[diameter_path[-1]])
    # A diameter-three spider can have two graph centers; only its unique
    # degree>=3 vertex is an admissible arm center. For path components the
    # middle of a diameter path is the correct choice.
    branching = [v for v in adj if len(adj[v]) >= 3]
    if len(branching) > 1:
        raise ValueError('two intermediate branch vertices')
    center = branching[0] if branching else diameter_path[len(diameter_path) // 2]
    seen, arms = {center}, []
    for v in adj[center]:
        arm = [v]; seen.add(v)
        nxt = [w for w in adj[v] if w != center]
        if len(nxt) > 1:
            raise ValueError('intermediate branch')
        if nxt:
            w = nxt[0]
            if len(adj[w]) != 1 or w in seen:
                raise ValueError('arm longer than two')
            arm.append(w); seen.add(w)
        arms.append(arm)
    if seen != set(adj):
        raise ValueError('not a short-arm spider')
    return dict(pair=component['pair'], center=center, arms=arms)


def prepare(n, edges):
    form = theta_form(n, edges)
    design = color_form(form)
    design['spiders'] = [short_arm_witness(c) for c in
                         pair_components(n, form['edges'], design['colors'])]
    design['guarantee'] = dict(operator_constant_sq='3+sqrt(5)',
                              frobenius_constant_sq='3+sqrt(5)')
    return form, design
