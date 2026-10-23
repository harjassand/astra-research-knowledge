"""Native four-action recovery on chordless tw<=2, maximum-degree-four graphs.

The input is the ORIGINAL n/edge list. Bridges and modules are found here;
no supplied block tree, reduced-action oracle, or graph-dependent choice of
entries is used. Temporary subdivision in the degree-three atom adapter is
preparation only. All actions and the final least-squares plan use this input.

The theorem is sufficient on the advertised class. Accepted outputs on other
graphs are still independently checked color/component certificates; rejection
is not a chordlessness recognizer. Preparation costs O(n+m log m) arithmetic
plus one fixed certificate load. Exact bit work and action acquisition count
separately. The existing atom normalizer and Cycle10 utilities are unchanged.
"""
from collections import Counter
from itertools import permutations

from block_reset_recovery_legacy import (
    native_block_tree, actual_profile, certify_stars, certify_spiders)
from coordinate_decoder import prepare
from degree3_atom import Degree3AtomOracle


def native_bridge_forest(n, edges):
    """Iterative bridge deletion, retaining isolated vertices and original IDs."""
    if type(n) is not int or n < 1:
        raise ValueError('positive original vertex count required')
    es = []
    for e in edges:
        if (not isinstance(e, (list, tuple)) or len(e) != 2 or
                any(type(v) is not int for v in e)):
            raise ValueError('integer original edge pairs required')
        u, v = sorted(e)
        if not 0 <= u < v < n:
            raise ValueError('finite simple original support required')
        es.append((u, v))
    es.sort()
    if len(es) != len(set(es)):
        raise ValueError('duplicate original edge')
    adj = [[] for _ in range(n)]
    for u, v in es:
        adj[u].append(v); adj[v].append(u)
    if max(map(len, adj), default=0) > 4:
        raise ValueError('original maximum degree exceeds four')
    disc = [-1]*n; low = [-1]*n; par = [-1]*n
    clock = 0; bridges = []
    for root in range(n):
        if disc[root] >= 0:
            continue
        disc[root] = low[root] = clock; clock += 1
        walk = [(root, iter(adj[root]))]
        while walk:
            u, it = walk[-1]; v = next(it, None)
            if v is not None:
                if disc[v] < 0:
                    par[v] = u; disc[v] = low[v] = clock; clock += 1
                    walk.append((v, iter(adj[v])))
                elif v != par[u]:
                    low[u] = min(low[u], disc[v])
                continue
            walk.pop(); p = par[u]
            if p >= 0:
                low[p] = min(low[p], low[u])
                if low[u] > disc[p]:
                    bridges.append(tuple(sorted((p, u))))
    bridges.sort(); bridge_set = set(bridges)
    nonbridge_adj = [[] for _ in range(n)]
    for u, v in es:
        if (u, v) not in bridge_set:
            nonbridge_adj[u].append(v); nonbridge_adj[v].append(u)
    membership = [-1]*n; modules = []
    for root in range(n):
        if membership[root] >= 0:
            continue
        i = len(modules); vertices = [root]; membership[root] = i
        for u in vertices:
            for v in nonbridge_adj[u]:
                if membership[v] < 0:
                    membership[v] = i; vertices.append(v)
        vertices.sort(); loc = {v:j for j,v in enumerate(vertices)}
        modules.append(dict(vertices=vertices, local_ids=loc, edges=[], local_edges=[]))
    for u, v in es:
        if (u, v) not in bridge_set:
            i = membership[u]
            if membership[v] != i:
                raise ValueError('nonbridge module mismatch')
            modules[i]['edges'].append((u, v))
    for module in modules:
        loc = module['local_ids']
        module['local_edges'] = [(loc[u], loc[v]) for u,v in module['edges']]
        if module['edges'] and any(len(nonbridge_adj[v]) < 2 for v in module['vertices']):
            raise ValueError('nontrivial bridge-deleted component has a leaf')
    tree = [[] for _ in modules]
    for u, v in bridges:
        a, b = membership[u], membership[v]
        if a == b:
            raise ValueError('bridge inside one module')
        tree[a].append((b, u, v)); tree[b].append((a, v, u))
    parent = [-1]*len(modules); entry = [None]*len(modules)
    parent_vertex = [None]*len(modules); children = [[] for _ in modules]
    depth = [-1]*len(modules); order = []; roots = []
    for root in range(len(modules)):
        if depth[root] >= 0:
            continue
        roots.append(root); depth[root] = 0; queue = [root]
        for a in queue:
            order.append(a)
            for b,u,v in tree[a]:
                if b == parent[a]:
                    continue
                if depth[b] >= 0:
                    raise ValueError('bridge quotient is not a forest')
                parent[b] = a; entry[b] = v; parent_vertex[b] = u
                depth[b] = depth[a]+1; children[a].append((b,u,v)); queue.append(b)
    return dict(n=n, edges=es, bridges=bridges, modules=modules,
                vertex_module=membership, roots=roots, parent=parent,
                entry_vertex=entry, parent_vertex=parent_vertex,
                children=children, depth=depth, order=order,
                maximum_degree=max(map(len,adj),default=0))


def _reroot_atoms(form, entry):
    """The ACTUAL bridge entry selects the one root atom; it is not a cut."""
    if entry is None:
        return
    ids = form['membership'][entry]
    if len(ids) != 1:
        raise ValueError('a bridge entry cannot already meet two nontrivial atoms')
    root = ids[0]; tree = [[] for _ in form['blocks']]
    for join in form['joins']:
        a,b = join['blocks']; v = join['vertex']
        tree[a].append((b,v)); tree[b].append((a,v))
    parent = [-1]*len(tree); depth = [-1]*len(tree); incoming = [None]*len(tree)
    children = [[] for _ in tree]; order = [root]; depth[root] = 0
    for a in order:
        for b,v in tree[a]:
            if b == parent[a]:
                continue
            if depth[b] >= 0:
                raise ValueError('atom adjacency cycle')
            parent[b]=a; depth[b]=depth[a]+1; incoming[b]=v
            children[a].append((b,v)); order.append(b)
    form.update(root=root,parent=parent,depth=depth,incoming=incoming,
                children=children,order=order)


def color_rooted_module(n, edges, marked_bundle, degree3_bundle,
                        entry=None, entry_color=None, incoming_color=None):
    """One real root qualification, then the inherited one-message atom rule."""
    form = native_block_tree(n, edges)
    _reroot_atoms(form, entry)
    if entry is not None and (entry_color == incoming_color or
            entry_color not in range(4) or incoming_color not in range(4)):
        raise ValueError('two prescribed DISTINCT entry colors required')
    colors = [-1]*n; records = []; blocked = {}
    local_colors = [None]*len(form['blocks'])
    for b in form['order']:
        block = form['blocks'][b]; is_root = form['parent'][b] < 0
        root = entry if is_root else form['incoming'][b]
        if root is None:
            root = next(v for v in block['vertices'] if len(block['adjacency'][v]) == 2)
        mark = block['local_ids'][root]; degree = len(block['adjacency'][root])
        if is_root and entry is not None and degree == 3:
            ans = degree3_bundle.color(len(block['vertices']), block['local_edges'], mark)
        elif degree == 2:
            ans = marked_bundle.color(len(block['vertices']), block['local_edges'], mark)
        else:
            raise ValueError('actual entry load must be two or three')
        original = {v:ans['colors'][j] for j,v in enumerate(block['vertices'])}
        certify_stars(block['vertices'], block['edges'], original)
        raw = actual_profile(block, original, root)
        if degree == 2 and (len(raw['neighbors']) != 2 or len(raw['flags']) > 1):
            raise ValueError('inherited degree-two qualification failed')
        parent_support = []; forced = None
        if is_root:
            if entry is None:
                permutation = tuple(range(4))
            else:
                missing = set(range(4))-{raw['color']}-set(raw['neighbors'])
                if not missing:
                    raise ValueError('actual root has no missing neighbor color')
                valid = [p for p in permutations(range(4))
                         if p[raw['color']] == entry_color
                         and incoming_color not in {p[c] for c in raw['neighbors']}]
                permutation = min(valid)
        else:
            pb = form['parent'][b]
            parent_support = actual_profile(form['blocks'][pb],local_colors[pb],root)['neighbors']
            forced = blocked.get(root)
            if forced is not None and forced not in parent_support:
                raise ValueError('stop request is not a real parent channel')
            valid = []
            for p in permutations(range(4)):
                if p[raw['color']] != colors[root]:
                    continue
                cn = {p[c] for c in raw['neighbors']}
                cf = {p[c] for c in raw['flags']}
                common = cn.intersection(parent_support)
                if (len(common) <= 1 and not common.intersection(cf)
                        and (forced is None or forced not in cn)):
                    valid.append(p)
            if not valid:
                raise ValueError('inherited one-message transition failed')
            permutation = min(valid)
        cs = {v:permutation[c] for v,c in original.items()}
        for v,c in cs.items():
            if colors[v] not in (-1,c):
                raise ValueError('previously fixed actual vertex changed')
            colors[v]=c
        local_colors[b]=cs
        profile = actual_profile(block,cs,root)
        common = sorted(set(profile['neighbors']).intersection(parent_support))
        stop = None
        if common:
            channel = common[0]
            ns = [v for v in block['adjacency'][root] if cs[v] == channel]
            if len(ns) != 1 or channel in profile['flags']:
                raise ValueError('common child component is not an isolated edge')
            endpoint = ns[0]
            downstream = [c for c,v in form['children'][b] if v == endpoint]
            if len(downstream)>1:
                raise ValueError('internal cut multiplicity exceeds two')
            if downstream:
                if endpoint in blocked:
                    raise ValueError('internal requests collided')
                blocked[endpoint]=colors[root]
                stop=dict(vertex=endpoint,forbidden=colors[root],child=downstream[0],
                          incoming_edge=[root,endpoint])
        records.append(dict(block=b,actual_mark=root,local_mark=mark,actual_degree=degree,
            parent=form['parent'][b],permutation=list(permutation),
            parent_neighbor_colors=parent_support,forbidden_incoming_color=forced,
            root_profile=profile,shared_channel=common,outgoing_stop_message=stop,
            vertex_ids=block['vertices'],colors=[cs[v] for v in block['vertices']],
            atom_certificate=ans))
    if any(c < 0 for c in colors):
        raise ValueError('uncolored module vertex')
    plan=prepare(n,form['edges'],colors,4)
    components=certify_spiders(plan)
    qualification=None
    if entry is not None:
        ns=[v if u==entry else u for u,v in form['edges'] if entry in (u,v)]
        mult=Counter(colors[v] for v in ns)
        if colors[entry]!=entry_color or incoming_color in mult:
            raise ValueError('missing entry channel destroyed by internal gluing')
        qualification=dict(vertex=entry,color=entry_color,incoming_color=incoming_color,
            actual_degree=len(ns),neighbor_color_multiplicities=[mult.get(c,0) for c in range(4)])
    return dict(colors=colors,blocks=records,atom_form=form,components=components,
                entry_qualification=qualification,
                messages=[dict(vertex=v,forbidden=c) for v,c in sorted(blocked.items())])


def certify_bridge_components(form, colors, plan):
    """Exact original-edge check of the all-depth theorem's resulting geometry."""
    oriented={}
    for a in form['order']:
        for b,u,v in form['children'][a]:
            oriented[tuple(sorted((u,v)))]=(u,v,a,b)
    out=[]
    for comp in plan['components']:
        vertices=comp['order']; parent=comp['parent']
        es=[tuple(sorted((v,parent[v]))) for v in vertices[1:]]
        adj={v:[] for v in vertices}
        for u,v in es:adj[u].append(v);adj[v].append(u)
        bridge_edges=[]; core_edges=[]
        for e in es:
            if e in oriented:
                u,v,a,b=oriented[e]
                if len(adj[v])!=1:
                    raise ValueError('a bridge child endpoint is not a global pair leaf')
                bridge_edges.append(e)
            else:core_edges.append(e)
        record=dict(pair=list(comp['pair']),vertices=list(vertices),
                    bridges=bridge_edges,core_edges=core_edges)
        if not core_edges:
            centers=[v for v in vertices if len(adj[v])==len(vertices)-1]
            if not centers or len(vertices)>5:
                raise ValueError('bridge-only component is not a degree-four star')
            record.update(kind='bridge_star',center=min(centers))
        else:
            mids={form['vertex_module'][u] for e in core_edges for u in e}
            if len(mids)!=1:
                raise ValueError('nonbridge core crosses two modules')
            core=sorted({v for e in core_edges for v in e}); core_set=set(core)
            loc={v:i for i,v in enumerate(core)}
            core_plan=prepare(len(core),[(loc[u],loc[v]) for u,v in core_edges],
                              [colors[v] for v in core],4)
            if len(core_plan['components'])!=1:
                raise ValueError('disconnected core')
            shape=certify_spiders(core_plan)[0]
            attached=Counter()
            for u,v in bridge_edges:
                hits=[w for w in (u,v) if w in core_set]
                if len(hits)!=1 or len(adj[v if u in core_set else u])!=1:
                    raise ValueError('bridge is not one pendant core leaf')
                attached[hits[0]]+=1
            if max(attached.values(),default=0)>2 or len(vertices)>25:
                raise ValueError('actual pendant budget or component order exceeds theorem')
            record.update(kind='one_spider_plus_pendants',module=next(iter(mids)),
                core_vertices=core,core_shape=shape,
                pendant_counts=[[v,k] for v,k in sorted(attached.items())])
        out.append(record)
    return out


def prepare_recovery(n, edges, marked_bundle, degree3_bundle):
    form=native_bridge_forest(n,edges)
    colors=[-1]*n; assigned={}; module_records=[]; bridge_records=[]
    for a in form['order']:
        module=form['modules'][a]; entry=form['entry_vertex'][a]
        incoming=form['parent_vertex'][a]
        entry_color=assigned.get(a)
        if module['edges']:
            loc=module['local_ids']
            ans=color_rooted_module(len(module['vertices']),module['local_edges'],
                marked_bundle,degree3_bundle,entry=None if entry is None else loc[entry],
                entry_color=entry_color,incoming_color=None if incoming is None else colors[incoming])
            for i,v in enumerate(module['vertices']):colors[v]=ans['colors'][i]
        else:
            if len(module['vertices'])!=1:raise ValueError('empty non-singleton module')
            colors[module['vertices'][0]]=0 if entry is None else entry_color
            ans=dict(colors=[colors[module['vertices'][0]]],blocks=[],components=[],
                     entry_qualification=None,messages=[])
        module_records.append(dict(module=a,original_vertex_ids=module['vertices'],
            original_entry=entry,original_parent_endpoint=incoming,certificate=ans))
        for b,u,v in form['children'][a]:
            forbidden={colors[u]}
            if entry is not None and u==entry:
                forbidden.add(colors[incoming])
            c=min(set(range(4))-forbidden);assigned[b]=c
            bridge_records.append(dict(parent_module=a,child_module=b,edge=[u,v],
                parent_color=colors[u],child_color=c,forbidden_colors=sorted(forbidden),
                entry_vertex_reset=(entry is not None and u==entry)))
    if any(c<0 for c in colors):raise ValueError('uncolored original graph')
    plan=prepare(n,form['edges'],colors,4)
    components=certify_bridge_components(form,colors,plan)
    design=dict(colors=colors,q=4,modules=module_records,bridges=bridge_records,
        components=components,guarantee=dict(row_norm_sq=1,
            operator_constant_sq=18,frobenius_constant_sq=18,
            sharper_constant_sq='3*beta+1+sqrt((3*beta-1)^2+8*beta), beta=(3+sqrt(5))/2',
            theorem='one-qualified-module-root-plus-entry-bridge-reset-and-pendant-Poincare',
            finite_operator_constant_sq=str(min(18,plan['certified_operator_constant_sq'])),
            finite_frobenius_constant_sq=str(min(18,plan['certified_frobenius_constant_sq']))))
    return form,design,plan
