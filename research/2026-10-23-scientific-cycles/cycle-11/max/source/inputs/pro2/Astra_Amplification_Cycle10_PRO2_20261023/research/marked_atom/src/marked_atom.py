"""Actual degree-two marked atom coloring from the unchanged Cycle8/9 proof.

No closure or coloring search runs here.  The input is the original atom edge
list and an actual specified degree-two vertex.  Protected-edge suppression
is only a preparation representation; every original edge is restored before
the resulting coloring is returned.  q=4, whole-row unit coordinate queries.

Promised coverage: two-connected chordless graphs of treewidth <=2 and maximum
degree <=4.  An accepted output additionally checks its ACTUAL full support,
star coloring, distinct marked-neighbor colors, and at most one marked flag.
The suppression failure on another support is not an all-input recognizer.

Canonical sorts cost O(n+m log m); native graph/expression traversal costs
O(n+m) under the degree cap, excluding one-time fixed-certificate loading.
"""
from collections import Counter, deque
from pathlib import Path
import hashlib
import json

from loaded_recovery import prepare_certificate, classify
from hazard_ports import canonical, transform, PERMS

CERTIFICATE_SHA256 = '63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525'
PROJECTION_SHA256 = '7a0bcde13cead849e1e828bbae564d1f3244f4dc65c9a37b0c173e0fb899fbfc'


def _input(n, edges, mark):
    if type(n) is not int or n < 3 or type(mark) is not int or not 0 <= mark < n:
        raise ValueError('original n>=3 and specified original mark required')
    es = []
    for e in edges:
        if not isinstance(e, (tuple, list)) or len(e) != 2 or any(type(v) is not int for v in e):
            raise ValueError('edges must be pairs of integer original IDs')
        u, v = sorted(e)
        if not 0 <= u < v < n:
            raise ValueError('original finite simple support required')
        es.append((u, v))
    es.sort()
    if len(set(es)) != len(es):
        raise ValueError('duplicate original edge')
    adj = [[] for _ in range(n)]
    for u, v in es:
        adj[u].append(v); adj[v].append(u)
    if any(not 2 <= len(ns) <= 4 for ns in adj) or len(adj[mark]) != 2:
        raise ValueError('atom degrees 2..4 and marked degree exactly two required')
    return es, adj


def prepare_marked_atom(n, edges, mark):
    """Exact H=G-mark native H8 form; its two ports are original neighbors.

    Unlike the old unmarked normalizer, ALL siblings of the formal protected
    edge are retained: suppressing the mark can produce a chorded auxiliary
    graph even when the original input is chordless.
    """
    es, original_adj = _input(n, edges, mark)
    a, b = sorted(original_adj[mark])
    if n == 3:
        if len(es) != 3:
            raise ValueError('three-vertex atom must be the original triangle')
        return dict(schema='astra-native-marked-atom/v1', n=n, original_edges=es,
                    mark=mark, ports=[a, b], triangle=True, nodes=[], root=None)
    if b in original_adj[a]:
        raise ValueError('nontriangle marked atom has adjacent mark neighbors')
    h_edges = [e for e in es if mark not in e]
    adj = [dict() for _ in range(n)]
    ordinary = []

    def add_edge(u, v):
        i = len(ordinary)
        ordinary.append(dict(kind='edge', s=u, t=v))
        adj[u][v] = adj[v][u] = i
        return i

    for u, v in h_edges:
        add_edge(u, v)
    protected = add_edge(a, b)  # FORMAL ONLY; never included in final support.

    def reverse(ref):
        return ref[0], not ref[1]

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
            return i, False
        if (node['s'], node['t']) == (t, s):
            return i, True
        raise ValueError('native orientation mismatch')

    def join(kind, left, right):
        _, s, mid, _ = view(left)
        _, start, t, _ = view(right)
        if kind == 'S':
            if mid != start:
                raise ValueError('native series endpoint mismatch')
        elif kind == 'P':
            if (s, mid) != (start, t):
                raise ValueError('native parallel endpoint mismatch')
            t = mid
        else:
            raise ValueError('ordinary production')
        if s == t:
            raise ValueError('coincident terminals')
        i = len(ordinary)
        ordinary.append(dict(kind=kind, s=s, t=t, children=[left, right]))
        return i, False

    contains_root = {protected}
    alive = [i != mark for i in range(n)]
    queue = deque(i for i in range(n) if i not in (a, b, mark) and len(adj[i]) == 2)
    suppressed = []
    while queue:
        w = queue.popleft()
        if not alive[w] or w in (a, b) or len(adj[w]) != 2:
            continue
        u, v = sorted(adj[w])
        path = join('S', orient(adj[w][u], u, w), orient(adj[w][v], w, v))
        old = adj[u].get(v)
        if old is not None:
            path = join('P', orient(old, u, v), path)
            if old in contains_root:
                contains_root.add(path[0])
        del adj[u][w]; del adj[v][w]
        adj[w].clear(); alive[w] = False
        adj[u][v] = adj[v][u] = path[0]
        suppressed.append([w, u, v, path[0]])
        for z in (u, v):
            if z not in (a, b) and len(adj[z]) == 2:
                queue.append(z)
    if sum(alive) != 2 or set(adj[a]) != {b} or set(adj[b]) != {a}:
        raise ValueError('marked protected-edge width-two suppression did not finish')

    cursor = orient(adj[a][b], a, b)
    siblings = []
    while cursor[0] != protected:
        kind, _, _, children = view(cursor)
        if kind != 'P':
            raise ValueError('formal edge has a non-parallel ancestor')
        hit = [j for j, ref in enumerate(children) if ref[0] in contains_root]
        if len(hit) != 1:
            raise ValueError('formal protected-edge ancestry not unique')
        siblings.append(children[1-hit[0]])
        cursor = children[hit[0]]
    if not siblings:
        raise ValueError('original marked vertex does not lie on a cycle')
    root = siblings[0]
    for other in siblings[1:]:
        root = join('P', root, other)

    nodes = []
    normal = {}
    stack = [(root, False)]
    while stack:
        ref, ready = stack.pop()
        if ref in normal:
            continue
        kind, s, t, children = view(ref)
        if kind == 'edge':
            if ref[0] == protected:
                raise ValueError('formal edge escaped into final H')
            normal[ref] = ('edge', s, t)
            continue
        if not ready:
            stack.append((ref, True))
            stack.extend((ch, False) for ch in reversed(children))
            continue
        left, right = [normal[ch] for ch in children]
        le, re = left[0] == 'edge', right[0] == 'edge'
        if kind == 'P':
            if le or re:
                raise ValueError('edge parallel branch violates induced H paths')
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
        i = len(nodes); nodes.append(node); normal[ref] = ('module', i)
    if normal[root][0] != 'module':
        raise ValueError('marked H is a single edge outside triangle case')
    form = dict(schema='astra-native-marked-atom/v1', n=n, original_edges=es,
                mark=mark, ports=[a, b], triangle=False, nodes=nodes,
                root=normal[root][1], h_edges=h_edges,
                preparation=dict(formal_edge=[a, b], parallel_siblings=len(siblings),
                                 suppressed_vertices=suppressed, ordinary_nodes=len(ordinary)))
    validate_marked_form(form)
    return form


def validate_marked_form(form):
    """Bind expression occurrence edges to exactly the ORIGINAL G-mark."""
    if form['triangle']:
        return
    nodes = form['nodes']; used = set(); edges = []
    stack = [form['root']]
    while stack:
        i = stack.pop()
        if i in used:
            raise ValueError('module occurrence duplicated')
        used.add(i); node = nodes[i]; s, t = node['terminals']; kind = node['kind']
        if s == t or form['mark'] in (s, t):
            raise ValueError('invalid marked-H ports')
        if kind == 'path':
            edges.extend([(s, node['middle']), (node['middle'], t)])
            continue
        ch = node['children']
        if any(type(j) is not int or not 0 <= j < i for j in ch):
            raise ValueError('normal form topology')
        ports = [nodes[j]['terminals'] for j in ch]
        if kind == 'P':
            if any(p != [s, t] for p in ports):
                raise ValueError('parallel native ports')
        elif kind == 'S':
            if ports[0][0] != s or ports[0][1] != ports[1][0] or ports[1][1] != t:
                raise ValueError('series native ports')
        elif kind == 'L':
            if ports[0][1] != t:
                raise ValueError('left-extension native ports')
            edges.append((s, ports[0][0]))
        elif kind == 'R':
            if ports[0][0] != s:
                raise ValueError('right-extension native ports')
            edges.append((ports[0][1], t))
        else:
            raise ValueError('unknown normal production')
        stack.extend(ch)
    if len(used) != len(nodes):
        raise ValueError('unreachable H module')
    expanded = sorted(tuple(sorted(e)) for e in edges)
    if expanded != form['h_edges'] or any(form['mark'] in e for e in expanded):
        raise ValueError('marked H changed original support')
    a, b = form['ports']
    restored = sorted(expanded + [tuple(sorted((a, form['mark']))), tuple(sorted((b, form['mark'])))])
    if restored != form['original_edges']:
        raise ValueError('restored marked atom changed original support')
    if nodes[form['root']]['terminals'] != [a, b]:
        raise ValueError('marked H has wrong actual ports')


class MarkedAtomOracle:
    """Load the accepted fixed evidence once; realize one true marked coloring."""

    def __init__(self, certificate_path, projection_path):
        certificate_path, projection_path = Path(certificate_path), Path(projection_path)
        if hashlib.sha256(certificate_path.read_bytes()).hexdigest() != CERTIFICATE_SHA256:
            raise ValueError('wrong inherited Cycle8 certificate bytes')
        projection_bytes = projection_path.read_bytes()
        if hashlib.sha256(projection_bytes).hexdigest() != PROJECTION_SHA256:
            raise ValueError('wrong inherited Cycle9 projection bytes')
        self.cert, self.table, self.indices = prepare_certificate(certificate_path)
        projection = json.loads(projection_bytes)
        self.rows = {row['family']: row for row in projection['rows']}
        if len(self.rows) != 66:
            raise ValueError('saved one-mark family map has wrong size')

    def color(self, n, edges, mark):
        form = prepare_marked_atom(n, edges, mark)
        a, b = form['ports']; colors = [None] * n
        if form['triangle']:
            colors[mark] = 0; colors[a] = 1; colors[b] = 2
            family, target_index, target = None, None, None
        else:
            labels, ds = classify(form, self.cert, self.table)
            root = form['root']; family = labels[root]
            if max(ds[root]) > 3:
                raise ValueError('marked H ports must both stay active')
            row = self.rows[family]
            target_index = row['target_index']
            target = tuple(self.cert['families'][family]['targets'][target_index])
            if list(target) != row['inherited_target'] or list(ds[root]) != row['degree']:
                raise ValueError('saved one-mark witness mismatch')
            colors[mark] = row['root_color']
            stack = [(root, target)]

            def assign(v, c):
                if c < 0:
                    return
                if colors[v] is not None and colors[v] != c:
                    raise ValueError('inconsistent actual vertex color')
                colors[v] = c

            while stack:
                i, st = stack.pop(); node = form['nodes'][i]
                s, t = node['terminals']; assign(s, st[0]); assign(t, st[1])
                canon = canonical(st); ti = self.indices[labels[i]][canon]
                perm = next(p for p in PERMS if transform(canon, p) == st)
                kind = node['kind']
                if kind == 'path':
                    w = self.cert['leaf']['witnesses'][ti]
                    if w['target'] != ti:
                        raise ValueError('inherited leaf witness order')
                    left, middle, right = [perm[x] for x in w['colors']]
                    assign(s, left); assign(node['middle'], middle); assign(t, right)
                    continue
                children = node['children']; order = list(range(len(children)))
                if kind == 'P':
                    order.sort(key=lambda j: (labels[children[j]], j))
                transition = self.table[kind, tuple(labels[children[j]] for j in order)]
                witness = transition['witnesses'][ti]
                if witness['target'] != ti:
                    raise ValueError('inherited transition witness order')
                assigned = [None] * len(children)
                for j, sig in zip(order, witness['child_signatures']):
                    assigned[j] = transform(tuple(sig), perm)
                if kind == 'L':
                    assign(s, perm[witness['new_color']])
                elif kind == 'R':
                    assign(t, perm[witness['new_color']])
                stack.extend((children[j], assigned[j]) for j in reversed(range(len(children))))
        profile = check_marked_coloring(n, form['original_edges'], mark, colors)
        return dict(schema='astra-native-marked-coloring/v1', n=n,
                    edges=form['original_edges'], colors=colors, q=4, mark=mark,
                    profile=profile, root_family=family, root_target_index=target_index,
                    root_target=target, native_normal_form=form)


def check_marked_coloring(n, edges, mark, colors):
    """Actual degree/multiplicity/star/profile check, independent of target masks."""
    if len(colors) != n or any(type(c) is not int or c not in range(4) for c in colors):
        raise ValueError('unresolved or invalid actual color')
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if colors[u] == colors[v]:
            raise ValueError('actual coloring not proper')
        adj[u].append(v); adj[v].append(u)
    mult = [Counter(colors[v] for v in ns) for ns in adj]
    for u, v in edges:
        if mult[u][colors[v]] >= 2 and mult[v][colors[u]] >= 2:
            raise ValueError('actual coloring has a bichromatic P4')
    if len(adj[mark]) != 2:
        raise ValueError('actual marked degree is not two')
    neighbor_colors = sorted(mult[mark])
    if len(neighbor_colors) != 2:
        raise ValueError('marked neighbors do not have distinct colors')
    flags = sorted({colors[v] for v in adj[mark] if mult[v][colors[mark]] >= 2})
    if len(flags) > 1:
        raise ValueError('marked coloring has two actual far flags')
    return dict(color=colors[mark], degree=2, neighbor_colors=neighbor_colors,
                far_flags=flags,
                neighbor_color_multiplicities=[mult[mark].get(c, 0) for c in range(4)])


def prepare_marked_certificate(certificate_path, projection_path):
    """One-time fixed source loading, hash binding, and transition indexing."""
    return MarkedAtomOracle(certificate_path, projection_path)


def color_marked_atom(n, edges, mark, certificate_bundle=None):
    """Public block adapter; reuse an explicit bundle across every block.

    If omitted, default source locations are ../data/loaded_star_certificate.json
    and ../data/marked_root_projection.json.  Loading is charged and callers
    processing many blocks should ALWAYS prepare and supply one bundle.
    """
    if certificate_bundle is None:
        data = Path(__file__).resolve().parents[1] / 'data'
        certificate_bundle = prepare_marked_certificate(
            data / 'loaded_star_certificate.json', data / 'marked_root_projection.json')
    result = certificate_bundle.color(n, edges, mark)
    result['root_neighbors'] = result['profile']['neighbor_colors']
    result['root_flags'] = result['profile']['far_flags']
    return result
