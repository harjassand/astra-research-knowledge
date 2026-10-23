"""Native-support preparation for two-connected chordless width-two atoms.

Every vertex/edge in the returned normal form is an ORIGINAL input vertex/edge.
The all-size guarantee uses the hypotheses in research/structural_scope/
ALL_CHORDLESS_ATOMS.md. On other supports this routine may reject; it is not
advertised as a full recognizer of the promised class. No matrix action occurs
in preparation. All stacks and graph traversals are iterative.
"""
from collections import deque, Counter
from loaded_recovery import prepare_certificate, classify
from hazard_ports import canonical, transform, PERMS


def prepare_atom(n, edges):
    if type(n) is not int or n < 3:
        raise ValueError('atom needs at least three vertices')
    edges = [tuple(sorted(e)) for e in edges]
    if len(set(edges)) != len(edges) or any(
        len(e) != 2 or not 0 <= e[0] < e[1] < n for e in edges
    ):
        raise ValueError('finite simple native support required')
    edges.sort()
    adj = [dict() for _ in range(n)]
    ordinary = []
    edge_ids = {}

    def add_edge(u, v):
        i = len(ordinary)
        ordinary.append(dict(kind='edge', s=u, t=v, contains_parallel=False))
        return i

    for u, v in edges:
        i = add_edge(u, v)
        edge_ids[u, v] = i
        adj[u][v] = adj[v][u] = i
    if any(not a or len(a) > 4 for a in adj):
        raise ValueError('positive degree at most four required')
    if n == 3:
        if len(edges) != 3:
            raise ValueError('the three-vertex atom must be C3')
        return dict(schema='astra-native-atom-normal-form/v1', n=n,
                    original_edges=edges, triangle=True, nodes=[], root=None,
                    preparation=dict(suppressed_vertices=[], ordinary_nodes=3))

    def reverse(ref):
        return (ref[0], not ref[1])

    def view(ref):
        node = ordinary[ref[0]]
        if not ref[1]:
            return node['kind'], node['s'], node['t'], node.get('children', [])
        ch = [reverse(r) for r in node.get('children', [])]
        if node['kind'] == 'S':
            ch.reverse()
        return node['kind'], node['t'], node['s'], ch

    def orient(i, s, t):
        node = ordinary[i]
        if (node['s'], node['t']) == (s, t):
            return (i, False)
        if (node['s'], node['t']) == (t, s):
            return (i, True)
        raise ValueError('orientation does not match native endpoints')

    def join(kind, left, right):
        _, s, mid, _ = view(left)
        _, start, t, _ = view(right)
        if kind == 'S':
            if mid != start:
                raise ValueError('series native endpoint mismatch')
        elif (s, mid) != (start, t):
            raise ValueError('parallel native endpoint mismatch')
        else:
            t = mid
        if s == t:
            raise ValueError('coincident terminals')
        i = len(ordinary)
        ordinary.append(dict(kind=kind, s=s, t=t, children=[left, right],
                             contains_parallel=kind == 'P' or any(
                                 ordinary[r[0]]['contains_parallel'] for r in (left, right))))
        return (i, False)

    u, v = edges[0]
    protected = edge_ids[u, v]
    contains_root = {protected}
    alive = [True] * n
    queue = deque(i for i in range(n) if i not in (u, v) and len(adj[i]) == 2)
    suppressed = []
    while queue:
        w = queue.popleft()
        if not alive[w] or w in (u, v) or len(adj[w]) != 2:
            continue
        a, b = sorted(adj[w])
        left, right = orient(adj[w][a], a, w), orient(adj[w][b], w, b)
        path = join('S', left, right)
        old = adj[a].get(b)
        if old is not None:
            path = join('P', orient(old, a, b), path)
            if old in contains_root:
                contains_root.add(path[0])
        del adj[a][w]
        del adj[b][w]
        adj[w].clear()
        alive[w] = False
        adj[a][b] = adj[b][a] = path[0]
        suppressed.append([w, a, b, path[0]])
        for z in (a, b):
            if z not in (u, v) and len(adj[z]) == 2:
                queue.append(z)
    if sum(alive) != 2 or set(adj[u]) != {v} or set(adj[v]) != {u}:
        raise ValueError('protected-edge width-two suppression did not finish')
    root = orient(adj[u][v], u, v)

    # The protected original edge has only parallel ancestors. Removing this
    # one edge leaves exact TTSP siblings with the same original terminals.
    siblings = []
    cursor = root
    while cursor[0] != protected:
        kind, _, _, ch = view(cursor)
        if kind != 'P':
            raise ValueError('protected edge has a non-parallel ancestor')
        hit = [j for j, r in enumerate(ch) if r[0] in contains_root]
        if len(hit) != 1:
            raise ValueError('protected-edge ancestry not unique')
        siblings.append(ch[1 - hit[0]])
        cursor = ch[hit[0]]
    if len(siblings) != 1:
        raise ValueError('root edge chords two other parallel branches')
    h = siblings[0]
    complement = orient(protected, u, v)

    if not ordinary[h[0]]['contains_parallel']:
        # G is a cycle. Two nonadjacent native vertices give two arcs >=2.
        original_adj = [[] for _ in range(n)]
        for a, b in edges:
            original_adj[a].append(b)
            original_adj[b].append(a)
        if any(len(a) != 2 for a in original_adj):
            raise ValueError('edge-rooted path does not bind to a cycle')
        s = 0
        first = min(original_adj[s])
        t = next(z for z in original_adj[first] if z != s)
        branches = []
        for nxt in sorted(original_adj[s]):
            path = [s, nxt]
            seen = set(path)
            while path[-1] != t:
                following = next(z for z in original_adj[path[-1]] if z != path[-2])
                if following in seen:
                    raise ValueError('cycle walk repeated a vertex')
                path.append(following)
                seen.add(following)
            refs = [orient(edge_ids[tuple(sorted((a, b)))], a, b)
                    for a, b in zip(path, path[1:])]
            branch = refs[0]
            for r in refs[1:]:
                branch = join('S', branch, r)
            branches.append(branch)
        root = join('P', branches[0], branches[1])
        selected_split = 'cycle_arcs'
    else:
        # Reach the first internal P through S contexts. The complement uses
        # each off-path child once, with its actual orientation reversed.
        cursor = h
        while True:
            kind, s, t, ch = view(cursor)
            if kind == 'P':
                root = join('P', join('P', ch[0], ch[1]), complement)
                break
            if kind != 'S':
                raise ValueError('parallel descendant disappeared')
            if ordinary[ch[0][0]]['contains_parallel']:
                complement = join('S', complement, reverse(ch[1]))
                cursor = ch[0]
            else:
                complement = join('S', reverse(ch[0]), complement)
                cursor = ch[1]
        selected_split = 'internal_parallel_and_complement'

    # Convert edge/S/P labels to loaded modules, preserving original IDs.
    nodes = []
    normal = {}
    stack = [(root, False)]
    while stack:
        ref, ready = stack.pop()
        if ref in normal:
            continue
        kind, s, t, ch = view(ref)
        if kind == 'edge':
            normal[ref] = ('edge', s, t)
            continue
        if not ready:
            stack.append((ref, True))
            stack.extend((r, False) for r in reversed(ch))
            continue
        left, right = [normal[r] for r in ch]
        le, re = left[0] == 'edge', right[0] == 'edge'
        if kind == 'P':
            if le or re:
                raise ValueError('parallel edge child violates induced terminal paths')
            node = dict(kind='P', children=[left[1], right[1]], terminals=[s, t])
        elif le and re:
            if left[2] != right[1]:
                raise ValueError('path2 midpoint mismatch')
            node = dict(kind='path', length=2, middle=left[2], terminals=[s, t])
        elif le:
            node = dict(kind='L', children=[right[1]], terminals=[s, t])
        elif re:
            node = dict(kind='R', children=[left[1]], terminals=[s, t])
        else:
            node = dict(kind='S', children=[left[1], right[1]], terminals=[s, t])
        idx = len(nodes)
        nodes.append(node)
        normal[ref] = ('module', idx)
    if normal[root][0] != 'module':
        raise ValueError('normal root is a single edge')
    result = dict(schema='astra-native-atom-normal-form/v1', n=n,
                  original_edges=edges, triangle=False, nodes=nodes,
                  root=normal[root][1], preparation=dict(
                      protected_edge=[u, v], selected_split=selected_split,
                      suppressed_vertices=suppressed, ordinary_nodes=len(ordinary)))
    validate_native_form(result)
    return result


def validate_native_form(form):
    """Linear output/support binding; this is not a full TTSP recognizer."""
    if form['triangle']:
        return
    nodes = form['nodes']
    actual_edges = []
    occurrences = Counter()
    stack = [form['root']]
    while stack:
        i = stack.pop()
        occurrences[i] += 1
        if occurrences[i] != 1:
            raise ValueError('native module occurrence duplicated')
        node = nodes[i]
        s, t = node['terminals']
        k = node['kind']
        if k == 'path':
            actual_edges.extend([(s, node['middle']), (node['middle'], t)])
            continue
        ch = node['children']
        if any(j >= i or j < 0 for j in ch):
            raise ValueError('normal form topology')
        ports = [nodes[j]['terminals'] for j in ch]
        if k == 'P':
            if any(p != [s, t] for p in ports):
                raise ValueError('parallel native ports')
        elif k == 'S':
            if ports[0][0] != s or ports[0][1] != ports[1][0] or ports[1][1] != t:
                raise ValueError('series native ports')
        elif k == 'L':
            if ports[0][1] != t:
                raise ValueError('left-extension native ports')
            actual_edges.append((s, ports[0][0]))
        elif k == 'R':
            if ports[0][0] != s:
                raise ValueError('right-extension native ports')
            actual_edges.append((ports[0][1], t))
        else:
            raise ValueError('normal production')
        stack.extend(ch)
    if sorted(tuple(sorted(e)) for e in actual_edges) != form['original_edges']:
        raise ValueError('normal form changed original support')
    if len(occurrences) != len(nodes):
        raise ValueError('unreachable native module')


def color_native_atom(form, certificate_path=None):
    """Apply the already-verified finite witnesses to unchanged native vertices."""
    validate_native_form(form)
    if form['triangle']:
        return dict(n=3, edges=form['original_edges'], colors=[0, 1, 2],
                    query_count=3, native_normal_form=form)
    cert, table, indices = prepare_certificate(certificate_path)
    labels, ds = classify(form, cert, table)
    root = form['root']
    target = tuple(cert['families'][labels[root]]['targets'][0])
    colors = [None] * form['n']
    stack = [(root, target)]

    def assign(v, c):
        if c < 0:
            return
        if colors[v] is not None and colors[v] != c:
            raise ValueError('inconsistent native vertex color')
        colors[v] = c

    while stack:
        i, st = stack.pop()
        node = form['nodes'][i]
        s, t = node['terminals']
        assign(s, st[0])
        assign(t, st[1])
        canon = canonical(st)
        ti = indices[labels[i]][canon]
        p = next(p for p in PERMS if transform(canon, p) == st)
        k = node['kind']
        if k == 'path':
            w = cert['leaf']['witnesses'][ti]
            a, c, b = [p[x] for x in w['colors']]
            assign(s, a)
            assign(node['middle'], c)
            assign(t, b)
            continue
        children = node['children']
        order = list(range(len(children)))
        if k == 'P':
            order.sort(key=lambda j: (labels[children[j]], j))
        row = table[k, tuple(labels[children[j]] for j in order)]
        w = row['witnesses'][ti]
        assigned = [None] * len(children)
        for j, ch in zip(order, w['child_signatures']):
            assigned[j] = transform(tuple(ch), p)
        if k == 'L':
            assign(s, p[w['new_color']])
        elif k == 'R':
            assign(t, p[w['new_color']])
        stack.extend((children[j], assigned[j]) for j in reversed(range(len(children))))
    if any(c is None for c in colors):
        raise ValueError('native saturation color remained unresolved')
    mult = [Counter() for _ in colors]
    for a, b in form['original_edges']:
        if colors[a] == colors[b]:
            raise ValueError('native coloring not proper')
        mult[a][colors[b]] += 1
        mult[b][colors[a]] += 1
    for a, b in form['original_edges']:
        if mult[a][colors[b]] >= 2 and mult[b][colors[a]] >= 2:
            raise ValueError('native coloring contains a bichromatic P4')
    return dict(n=form['n'], edges=form['original_edges'], colors=colors,
                query_count=4, terminals=form['nodes'][root]['terminals'],
                terminal_degrees=ds[root], root_family=labels[root],
                actual_neighbor_color_multiplicities=[
                    [m.get(c, 0) for c in range(4)] for m in mult],
                native_normal_form=form)
