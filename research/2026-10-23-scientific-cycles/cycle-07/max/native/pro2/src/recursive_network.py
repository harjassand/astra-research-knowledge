"""Cycle6 three-color construction, with an explicit admitted graph grammar.

Nodes are topologically ordered. Repeated child IDs denote disjoint copies,
sharing only the terminals specified by the production. This is an algorithm
for a supplied expression, not a recognition oracle for all partial two-trees.
No external dependencies. All profile counts are exact integers.
"""
from collections import defaultdict


def validate_spec(spec, allow_even_failure=False):
    nodes = spec['nodes']
    if not nodes or not 0 <= spec['root'] < len(nodes):
        raise ValueError('nonempty topologically ordered specification required')
    for i, node in enumerate(nodes):
        kind = node['kind']
        if kind == 'path':
            if type(node['length']) is not int or node['length'] < 2:
                raise ValueError('leaf paths have at least two edges')
            continue
        children = node.get('children', [])
        if any(type(j) is not int or not 0 <= j < i for j in children):
            raise ValueError('children must precede their parent')
        if kind == 'parallel':
            if len(children) not in (2, 3):
                raise ValueError('degree-four operation permits two or three branches')
        elif kind == 'series':
            if len(children) < 3 or len(children) % 2 == 0:
                raise ValueError('positive construction permits only odd series >=3')
        elif kind == 'series_even_failure' and allow_even_failure:
            if len(children) != 2:
                raise ValueError('only the explicitly failed two-child rule is implemented')
        else:
            raise ValueError('unadmitted production: '+str(kind))
    return nodes


def path_word(length, a=0, b=1):
    if length < 2 or a == b or a not in range(3) or b not in range(3):
        raise ValueError('distinct three-color endpoints and length>=2 required')
    if length == 2:
        word = [0, 2, 1]
    elif length == 3:
        word = [0, 2, 0, 1]
    else:
        word = [i % 3 for i in range(length-1)]
        word.append(next(c for c in range(3) if c not in (word[-1], 1)))
        word.append(1)
    c = 3-a-b
    return [[a, b, c][v] for v in word]


def graph_profile(n, edges, colors, terminals):
    """Exact actual-graph audit; does not use recursive mass formulas."""
    s, t = terminals
    a, b = colors[s], colors[t]
    if a == b:
        raise ValueError('this interface requires distinct terminal colors')
    c = 3-a-b
    slots = [(s, frozenset((a,b))), (s, frozenset((a,c))),
             (t, frozenset((a,b))), (t, frozenset((b,c)))]
    masses = [None]*4
    maximum = 1
    for pair in (frozenset((0,1)), frozenset((0,2)), frozenset((1,2))):
        adj = {v:[] for v in range(n) if colors[v] in pair}
        for u,v in edges:
            if colors[u] == colors[v]:
                raise ValueError('improper coloring')
            if u in adj and v in adj:
                adj[u].append(v); adj[v].append(u)
        seen = set()
        for start in adj:
            if start in seen:
                continue
            order, seen_now = [start], {start}
            edge_twice = 0
            for u in order:
                edge_twice += len(adj[u])
                for v in adj[u]:
                    if v not in seen_now:
                        seen_now.add(v); order.append(v)
            if edge_twice != 2*(len(order)-1):
                raise ValueError('bichromatic cycle')
            if s in seen_now and t in seen_now:
                raise ValueError('a bichromatic component transmits between terminals')
            seen.update(seen_now)
            maximum = max(maximum, len(order))
            for j,(endpoint, p) in enumerate(slots):
                if p == pair and endpoint in seen_now:
                    masses[j] = len(order)
    assert all(type(x) is int for x in masses)
    return {'boundary':masses, 'K':maximum}


def evaluate_profiles(spec, allow_even_failure=False):
    """Exact compositional profiles and graph sizes, without materializing graphs.

    This computes specified expressions; the all-depth proof is PROOF.md §4,
    not finite profile enumeration.
    """
    nodes = validate_spec(spec, allow_even_failure)
    out = []
    for node in nodes:
        if node['kind'] == 'path':
            word = path_word(node['length'])
            n = len(word)
            prof = graph_profile(n, [(i,i+1) for i in range(n-1)], word, (0,n-1))
            prof.update(n=n, m=n-1, applications=1, depth=0)
            out.append(prof)
            continue
        ch = [out[j] for j in node['children']]
        boundary = [p['boundary'] for p in ch]
        kind = node['kind']
        K = max(p['K'] for p in ch)
        if kind == 'parallel':
            x = 2+sum(p[1]-1 for p in boundary)
            y = 2+sum(p[2]-1 for p in boundary)
            xy = [x,1,1,y]
            K = max(K,x,y,1+sum(p[0]-1 for p in boundary),
                    1+sum(p[3]-1 for p in boundary))
            n = sum(p['n'] for p in ch)-2*len(ch)+4
            m = sum(p['m'] for p in ch)+2
        elif kind == 'series':
            xy = boundary[0][:2]+boundary[-1][2:]
            K = max([K]+[max(p[2]+q[0]-1, p[3]+q[1]-1)
                          for p,q in zip(boundary,boundary[1:])])
            n = sum(p['n'] for p in ch)-len(ch)+1
            m = sum(p['m'] for p in ch)
        else:
            p,q = boundary
            xy = [p[1],p[0],q[3],q[2]]
            K = max(K,p[2]+q[1]-1,p[3]+q[0]-1)
            n = ch[0]['n']+ch[1]['n']-1
            m = ch[0]['m']+ch[1]['m']
        out.append({'boundary':xy, 'K':K, 'n':n, 'm':m,
                    'applications':1+sum(p['applications'] for p in ch),
                    'depth':1+max(p['depth'] for p in ch)})
    return out


def build(spec, allow_even_failure=False):
    """Iterative full graph/color construction. No matrix entries are omitted."""
    nodes = validate_spec(spec, allow_even_failure)
    colors, edges = [0,1], []
    stack = [(spec['root'],0,1,0,1)]
    applications = 0
    def vertex(color):
        i = len(colors); colors.append(color); return i
    while stack:
        idx,s,t,a,b = stack.pop()
        applications += 1
        assert colors[s] == a and colors[t] == b and a != b
        node = nodes[idx]
        c = 3-a-b
        if node['kind'] == 'path':
            word = path_word(node['length'],a,b)
            path = [s]+[vertex(color) for color in word[1:-1]]+[t]
            edges.extend(zip(path,path[1:]))
        elif node['kind'] == 'parallel':
            u,v = vertex(b),vertex(c)
            edges.extend(((s,u),(v,t)))
            stack.extend((j,u,v,b,c) for j in reversed(node['children']))
        else:
            children = node['children']
            if node['kind'] == 'series':
                chain_colors = [a if i%2 == 0 else b for i in range(len(children)+1)]
            else:
                chain_colors = [a,c,b]
            chain = [s]+[vertex(color) for color in chain_colors[1:-1]]+[t]
            stack.extend((j,chain[i],chain[i+1],chain_colors[i],chain_colors[i+1])
                         for i,j in reversed(list(enumerate(children))))
    edges = [tuple(sorted(e)) for e in edges]
    if len(set(edges)) != len(edges):
        raise AssertionError('repeated edge contradicts grammar')
    degree = [0]*len(colors)
    for u,v in edges:
        if u == v:
            raise AssertionError('loop')
        degree[u] += 1; degree[v] += 1
    assert degree[0] == degree[1] == 1 and max(degree) <= 4
    return {'n':len(colors), 'edges':edges, 'colors':colors, 'terminals':[0,1],
            'maximum_degree':max(degree), 'applications':applications}


def standard_spec():
    """Uneven, branching, odd-series receiving input, all leaves length two."""
    nodes = [
        {'kind':'path','length':2},
        {'kind':'parallel','children':[0,0,0]},
        {'kind':'series','children':[1,0,1]},
        {'kind':'parallel','children':[2,1,0]},
        {'kind':'series','children':[3,1,2,0,3]},
        {'kind':'parallel','children':[4,3,2]},
        {'kind':'series','children':[5,3,4]},
        {'kind':'parallel','children':[6,5,4]},
    ]
    return {'nodes':nodes, 'root':len(nodes)-1}


def path_extension_spec():
    return {'nodes':[
        {'kind':'path','length':2}, {'kind':'path','length':3},
        {'kind':'path','length':8}, {'kind':'path','length':17},
        {'kind':'parallel','children':[0,1,2]},
        {'kind':'series','children':[4,3,4]},
        {'kind':'parallel','children':[5,4,1]},
        {'kind':'series','children':[6,5,4]},
        {'kind':'parallel','children':[7,6,5]},
    ], 'root':8}


def failed_spec(depth):
    if type(depth) is not int or depth < 0:
        raise ValueError('nonnegative depth')
    nodes = [{'kind':'path','length':2}]
    last = 0
    for _ in range(depth):
        nodes.append({'kind':'series_even_failure','children':[last,0]})
        j = len(nodes)-1
        nodes.append({'kind':'parallel','children':[j,j]})
        last = len(nodes)-1
    return {'nodes':nodes,'root':last}
