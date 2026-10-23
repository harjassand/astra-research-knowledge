"""Four original actions on rooted-qualifiable block trees.

Native n/edge-list input. In the advertised class G is connected, bridgeless,
chordless, tw<=2 and Delta<=4. The code checks actual block incidence, obtains
one marked star coloring per block from the inherited constructive theorem,
then certifies the actual global spider components. It does not claim that
every rejected/accepted support is classified by chordlessness recognition.

Preparation O(n+m log m), fixed certificate loading additionally charged.
Color/LS/output O(nq+m) arithmetic; rational bit work is extra.
"""
from collections import defaultdict, Counter
from itertools import permutations
from coordinate_decoder import prepare, decode, action
from marked_atom import prepare_marked_certificate, color_marked_atom


def native_block_tree(n, edges):
    if type(n) is not int or n < 3:
        raise ValueError('at least one nontrivial bridgeless block required')
    es = []
    for edge in edges:
        if (not isinstance(edge, (list, tuple)) or len(edge) != 2 or
                any(type(v) is not int for v in edge)):
            raise ValueError('integer original edge pairs required')
        u, v = sorted(edge)
        if not 0 <= u < v < n:
            raise ValueError('original finite simple support required')
        es.append((u, v))
    es.sort()
    if len(set(es)) != len(es):
        raise ValueError('duplicate edge')
    adj = [[] for _ in range(n)]
    for u, v in es:
        adj[u].append(v); adj[v].append(u)
    if any(not ns or len(ns) > 4 for ns in adj):
        raise ValueError('connected positive degree at most four required')

    disc = [-1] * n; low = [-1] * n; par = [-1] * n
    disc[0] = low[0] = 0
    timer = 1
    walk = [(0, iter(adj[0]))]; stack = []; raw = []
    while walk:
        u, it = walk[-1]
        v = next(it, None)
        if v is not None:
            if disc[v] < 0:
                par[v] = u; disc[v] = low[v] = timer; timer += 1
                stack.append((u, v)); walk.append((v, iter(adj[v])))
            elif v != par[u] and disc[v] < disc[u]:
                low[u] = min(low[u], disc[v]); stack.append((u, v))
            continue
        walk.pop(); p = par[u]
        if p < 0:
            continue
        low[p] = min(low[p], low[u])
        if low[u] >= disc[p]:
            block = []
            while True:
                e = stack.pop(); block.append(tuple(sorted(e)))
                if e == (p, u):
                    break
            if len(block) < 3:
                raise ValueError('bridges are outside this theorem')
            raw.append(sorted(block))
    if timer != n or stack:
        raise ValueError('graph must be connected')
    raw.sort(key=lambda b: b[0])
    membership = [[] for _ in range(n)]; blocks = []
    for i, be in enumerate(raw):
        vertices = sorted({v for e in be for v in e})
        loc = {v: j for j, v in enumerate(vertices)}
        ba = defaultdict(list)
        for u, v in be:
            ba[u].append(v); ba[v].append(u)
        if any(len(ns) < 2 for ns in ba.values()):
            raise ValueError('nontrivial biconnected block required')
        blocks.append(dict(vertices=vertices, edges=be, adjacency=dict(ba),
                           local_ids=loc,
                           local_edges=[(loc[u], loc[v]) for u, v in be]))
        for v in vertices:
            membership[v].append(i)
    tree = [[] for _ in blocks]; joins = []
    for v, ids in enumerate(membership):
        if not 1 <= len(ids) <= 2:
            raise ValueError('each cut must meet exactly two nontrivial blocks')
        if len(ids) == 2:
            a, b = ids
            if any(len(blocks[i]['adjacency'][v]) != 2 for i in ids):
                raise ValueError('actual cut load must be two on both sides')
            tree[a].append((b, v)); tree[b].append((a, v))
            joins.append(dict(vertex=v, blocks=ids))
    if len(joins) != len(blocks)-1:
        raise ValueError('block adjacency must be a tree')
    parent = [-1] * len(blocks); depth = [-1] * len(blocks)
    incoming = [None] * len(blocks); children = [[] for _ in blocks]
    depth[0] = 0; order = [0]
    for b in order:
        for c, v in tree[b]:
            if c == parent[b]:
                continue
            if depth[c] >= 0:
                raise ValueError('block adjacency cycle')
            parent[c] = b; depth[c] = depth[b]+1; incoming[c] = v
            children[b].append((c, v)); order.append(c)
    if len(order) != len(blocks):
        raise ValueError('disconnected block tree')
    return dict(n=n, edges=es, blocks=blocks, membership=membership,
                joins=joins, root=0, parent=parent, depth=depth,
                incoming=incoming, children=children, order=order,
                maximum_degree=max(map(len, adj)))


def actual_profile(block, colors, vertex):
    adj = block['adjacency']; root_color = colors[vertex]
    ns = {colors[u] for u in adj[vertex]}
    flags = {colors[u] for u in adj[vertex]
             if any(w != vertex and colors[w] == root_color for w in adj[u])}
    return dict(color=root_color, neighbors=sorted(ns), flags=sorted(flags))


def certify_stars(vertices, edges, colors):
    mult = {v: Counter() for v in vertices}
    for u, v in edges:
        if colors[u] == colors[v]:
            raise ValueError('local atom coloring is not proper')
        mult[u][colors[v]] += 1; mult[v][colors[u]] += 1
    for u, v in edges:
        if mult[u][colors[v]] >= 2 and mult[v][colors[u]] >= 2:
            raise ValueError('local bichromatic P4')


def color_block_tree(form, certificate_bundle):
    """One actual marked root per atom; only children respond to messages."""
    colors = [-1] * form['n']; records = []; blocked = {}
    local_colors = [None] * len(form['blocks'])
    for b in form['order']:
        block = form['blocks'][b]
        root = form['incoming'][b]
        if root is None:
            root = next(v for v in block['vertices'] if len(block['adjacency'][v]) == 2)
        mark = block['local_ids'][root]
        ans = color_marked_atom(len(block['vertices']), block['local_edges'], mark,
                               certificate_bundle=certificate_bundle)
        original = {v: ans['colors'][i] for i, v in enumerate(block['vertices'])}
        certify_stars(block['vertices'], block['edges'], original)
        raw = actual_profile(block, original, root)
        if len(raw['neighbors']) != 2 or len(raw['flags']) > 1:
            raise ValueError('one-mark guarantee not realized')
        parent_support = []; forced = None; common = []
        if form['parent'][b] < 0:
            permutation = tuple(range(4))
        else:
            pb = form['parent'][b]
            pp = actual_profile(form['blocks'][pb], local_colors[pb], root)
            parent_support = pp['neighbors']
            forced = blocked.get(root)
            if forced is not None and forced not in parent_support:
                raise ValueError('message is not a real parent channel')
            # Only 24 permutations: fixed work, no graph-size optimization.
            valid = []
            for p in permutations(range(4)):
                if p[raw['color']] != colors[root]:
                    continue
                child_n = {p[x] for x in raw['neighbors']}
                child_f = {p[x] for x in raw['flags']}
                intersection = child_n.intersection(parent_support)
                if (len(intersection) <= 1 and not intersection.intersection(child_f)
                        and (forced is None or forced not in child_n)):
                    valid.append(p)
            if not valid:
                raise ValueError('nonempty one-message transition failed')
            permutation = min(valid)
        cs = {v: permutation[c] for v, c in original.items()}
        for v, c in cs.items():
            if colors[v] not in (-1, c):
                raise ValueError('shared original vertex color changed')
            colors[v] = c
        local_colors[b] = cs
        profile = actual_profile(block, cs, root)
        common = sorted(set(profile['neighbors']).intersection(parent_support))
        stop_message = None
        if common:
            channel = common[0]
            ns = [u for u in block['adjacency'][root] if cs[u] == channel]
            if len(ns) != 1 or channel in profile['flags']:
                raise ValueError('common child component is not an isolated edge')
            endpoint = ns[0]
            downstream = [c for c, v in form['children'][b] if v == endpoint]
            if len(downstream) > 1:
                raise ValueError('cut multiplicity exceeds two')
            if downstream:
                if endpoint in blocked:
                    raise ValueError('two messages collide')
                blocked[endpoint] = colors[root]
                stop_message = dict(vertex=endpoint, forbidden=colors[root],
                                    child=downstream[0], incoming_edge=[root, endpoint])
        records.append(dict(block=b, actual_mark=root, local_mark=mark,
                            parent=form['parent'][b], permutation=list(permutation),
                            parent_neighbor_colors=parent_support,
                            forbidden_incoming_color=forced,
                            root_profile=profile, shared_channel=common,
                            outgoing_stop_message=stop_message,
                            vertex_ids=block['vertices'], colors=[cs[v] for v in block['vertices']],
                            atom_certificate=ans))
    if any(c < 0 for c in colors):
        raise ValueError('uncolored original vertex')
    return dict(colors=colors, q=4, blocks=records,
                messages=[dict(vertex=v, forbidden=c) for v, c in sorted(blocked.items())])


def certify_spiders(plan):
    """Actual finite shape check, supporting but not replacing the all-depth proof."""
    out = []
    for comp in plan['components']:
        order = comp['order']; parent = comp['parent']
        adj = {v: [] for v in order}
        for v in order[1:]:
            p = parent[v]; adj[v].append(p); adj[p].append(v)
        branch = [v for v in order if len(adj[v]) > 2]
        if len(branch) > 1:
            raise ValueError('two branch centers in a color component')
        if branch:
            candidates = branch
        else:
            # A nonbranching component must be a path of at most five vertices.
            if len(order) > 5:
                raise ValueError('bichromatic path exceeds two short arms')
            candidates = sorted(order)
        witness = None
        for center in candidates:
            arms = []; seen = {center}; ok = True
            for u in adj[center]:
                arm = [u]; seen.add(u)
                tail = [v for v in adj[u] if v != center]
                if len(tail) > 1:
                    ok = False; break
                if tail:
                    v = tail[0]
                    if len(adj[v]) != 1 or v in seen:
                        ok = False; break
                    seen.add(v); arm.append(v)
                arms.append(arm)
            if ok and seen == set(order):
                witness = dict(pair=list(comp['pair']), center=center, arms=arms,
                               vertices=len(order)); break
        if witness is None:
            raise ValueError('component is not an arm-two spider')
        out.append(witness)
    return out


def prepare_recovery(n, edges, certificate_bundle):
    form = native_block_tree(n, edges)
    design = color_block_tree(form, certificate_bundle)
    plan = prepare(n, form['edges'], design['colors'], 4)
    design['components'] = certify_spiders(plan)
    design['guarantee'] = dict(operator_constant_sq='3+sqrt(5)',
                               frobenius_constant_sq='3+sqrt(5)',
                               row_norm_sq=1,
                               theorem='one-message-block-reset-and-arm-Poincare')
    return form, design, plan
