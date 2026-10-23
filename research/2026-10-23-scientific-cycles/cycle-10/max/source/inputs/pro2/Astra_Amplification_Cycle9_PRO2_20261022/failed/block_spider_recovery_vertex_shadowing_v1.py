"""Native, degree-free (p+2)-action recovery on trees of K_(p,k) blocks.

The common p is at least 2 and every k is greater than p. Cut vertices are middle vertices in exactly two
blocks. The original edge list, not a supplied decomposition, is the input.
No edge, observation, or coefficient is removed by preparation.

Canonical sorting is charged: O(n+m log m) comparison work, O(n+m) storage.
The inherited Fraction decoder counts arithmetic, not rational bit cost.
"""
from collections import defaultdict, deque
from coordinate_decoder import prepare, decode, action


def native_blocks(n, edges):
    """Iterative low-link block decomposition, with full class recognition."""
    if type(n) is not int or n < 5:
        raise ValueError('a connected Kp,k block graph needs n>=5')
    es = []
    for e in edges:
        if (not isinstance(e, (list, tuple)) or len(e) != 2 or
                any(type(x) is not int for x in e)):
            raise ValueError('edges must be pairs of integer original IDs')
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
        raise ValueError('connected nontrivial graph required')

    discovery = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    discovery[0] = low[0] = 0
    time = 1
    stack = [(0, iter(adj[0]))]
    edge_stack = []
    raw_blocks = []
    while stack:
        u, it = stack[-1]
        v = next(it, None)
        if v is not None:
            if discovery[v] == -1:
                parent[v] = u
                discovery[v] = low[v] = time; time += 1
                edge_stack.append((u, v))
                stack.append((v, iter(adj[v])))
            elif v != parent[u] and discovery[v] < discovery[u]:
                low[u] = min(low[u], discovery[v])
                edge_stack.append((u, v))
            continue
        stack.pop()
        p = parent[u]
        if p == -1:
            continue
        low[p] = min(low[p], low[u])
        if low[u] >= discovery[p]:
            block = []
            while True:
                e = edge_stack.pop()
                block.append(tuple(sorted(e)))
                if e == (p, u):
                    break
            raw_blocks.append(sorted(block))
    if time != n or edge_stack:
        raise ValueError('input must be connected')
    raw_blocks.sort(key=lambda b: b[0])

    blocks = []
    middle_sets = []
    common_p = None
    membership = [[] for _ in range(n)]
    for be in raw_blocks:
        ba = defaultdict(set)
        for u, v in be:
            ba[u].add(v); ba[v].add(u)
        p = min(map(len, ba.values()))
        hubs = sorted(v for v in ba if len(ba[v]) > p)
        middles = sorted(v for v in ba if len(ba[v]) == p)
        if p < 2 or len(hubs) != p or len(middles) <= p:
            raise ValueError('every maximal block must be Kp,k with k>p>=2')
        if common_p is None:
            common_p = p
        elif common_p != p:
            raise ValueError('the hub-side size p must be common to all blocks')
        hs, ms = set(hubs), set(middles)
        if any(ba[h] != ms for h in hubs) or any(ba[v] != hs for v in middles):
            raise ValueError('block is not complete bipartite Kp,k')
        i = len(blocks)
        blocks.append(dict(hubs=hubs, middles=middles, edges=[list(e) for e in be]))
        middle_sets.append(ms)
        for v in ba:
            membership[v].append(i)

    tree = [[] for _ in blocks]
    joins = []
    for v, ids in enumerate(membership):
        if not 1 <= len(ids) <= 2:
            raise ValueError('each original vertex must belong to at most two blocks')
        if len(ids) == 2:
            a, b = ids
            if any(v not in middle_sets[i] for i in ids):
                raise ValueError('only middle vertices may be shared')
            tree[a].append((b, v)); tree[b].append((a, v))
            joins.append(dict(vertex=v, blocks=ids))
    if len(joins) != len(blocks) - 1:
        raise ValueError('block adjacency must be a tree')
    par = [-1] * len(blocks)
    dep = [-1] * len(blocks)
    dep[0] = 0
    order = [0]
    for b in order:
        for c, v in tree[b]:
            if c == par[b]:
                continue
            if dep[c] != -1:
                raise ValueError('block adjacency cycle')
            par[c] = b; dep[c] = dep[b] + 1; order.append(c)
    if len(order) != len(blocks):
        raise ValueError('disconnected block adjacency')
    return dict(schema='astra-Kpk-native-block-form/v1', n=n, edges=es, p=common_p,
                blocks=blocks, membership=membership, joins=joins,
                root=0, parent=par, depth=dep, order=order,
                max_degree=max(map(len, adj)))


def color_form(form, mode='stable'):
    """Depth-parity design, or matched (2p+1)-action star control."""
    if mode not in ('stable', 'star'):
        raise ValueError('only the proved stable and star designs')
    p = form['p']
    colors = [-1] * form['n']
    for b, block in enumerate(form['blocks']):
        offset = 0 if mode == 'stable' else p * (form['depth'][b] % 2)
        for i, h in enumerate(block['hubs']):
            if colors[h] != -1:
                raise ValueError('hub reused across blocks')
            colors[h] = offset + i
    for v, ids in enumerate(form['membership']):
        if colors[v] != -1:
            continue
        if mode == 'star':
            colors[v] = 2 * p
        else:
            b = min(ids, key=lambda i: form['depth'][i])
            colors[v] = p + form['depth'][b] % 2
    return colors


def certify_spiders(form, colors, plan, mode):
    """Check actual component shapes; no claim from a local rank test."""
    witnesses = []
    p = form['p']
    hubs = {h: b for b, block in enumerate(form['blocks']) for h in block['hubs']}
    for comp in plan['components']:
        pair, order, parent = comp['pair'], comp['order'], comp['parent']
        adj = {v: [] for v in order}
        for v in order[1:]:
            p = parent[v]
            adj[v].append(p); adj[p].append(v)
        if mode == 'stable':
            c = next(x for x in pair if x >= p)
            candidates = [v for v in order if v in hubs and
                          form['depth'][hubs[v]] % 2 == c - p]
        else:
            candidates = [v for v in order if colors[v] != 2 * p]
        if len(candidates) != 1:
            raise ValueError('component lacks its proved unique center')
        center = candidates[0]
        arms = []
        seen = {center}
        for v in adj[center]:
            arm = [v]
            seen.add(v)
            following = [w for w in adj[v] if w != center]
            if len(following) > (1 if mode == 'stable' else 0):
                raise ValueError('an intermediate arm vertex branches')
            if following:
                w = following[0]
                if len(adj[w]) != 1 or w in seen:
                    raise ValueError('arm has length greater than two')
                seen.add(w); arm.append(w)
            arms.append(arm)
        if seen != set(order):
            raise ValueError('component is not the claimed spider')
        witnesses.append(dict(pair=list(pair), center=center, arms=arms,
                              vertices=len(order)))
    return witnesses


def prepare_design(form, mode='stable'):
    p = form['p']
    q = p + 2 if mode == 'stable' else 2 * p + 1
    colors = color_form(form, mode)
    plan = prepare(form['n'], form['edges'], colors, q)
    shapes = certify_spiders(form, colors, plan, mode)
    # Older plan fields remain conservative generic estimates. This theorem
    # supplies the stronger, degree-independent certificate used here.
    bound = (dict(operator_constant_sq='3+sqrt(5)',
                  frobenius_constant_sq='3+sqrt(5)', theorem='spider-arm-Poincare')
             if mode == 'stable' else
             dict(operator_constant_sq='3/2', frobenius_constant_sq='2',
                  theorem='star-LS-and-triangle-free-dual'))
    return plan, dict(colors=colors, q=q, mode=mode, component_witnesses=shapes, guarantee=bound)
