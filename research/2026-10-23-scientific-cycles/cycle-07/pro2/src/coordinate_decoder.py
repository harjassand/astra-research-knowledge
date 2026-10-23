"""Exact coordinate-query recovery on an acyclic coloring.

All queries have unit total row energy. Arithmetic is Fraction-based; the
O(n+m+nq) claim counts arithmetic operations, not rational bit operations.
The preparation validates the ACTUAL graph/coloring, not merely its name.
"""
from fractions import Fraction as F
from collections import defaultdict


def prepare(n, edges, colors, q=4):
    if len(colors) != n or any(not 0 <= c < q for c in colors):
        raise ValueError("invalid colors")
    edges = [tuple(sorted(e)) for e in edges]
    if len(set(edges)) != len(edges):
        raise ValueError("repeated edges")
    groups = defaultdict(list)
    degree = [0] * n
    for u, v in edges:
        if not (0 <= u < v < n) or colors[u] == colors[v]:
            raise ValueError("not a simple graph with a proper coloring")
        degree[u] += 1
        degree[v] += 1
        groups[tuple(sorted((colors[u], colors[v])))].append((u, v))
    components = []
    for pair, es in groups.items():
        adj = defaultdict(list)
        for u, v in es:
            adj[u].append(v)
            adj[v].append(u)
        seen = set()
        for root in adj:
            if root in seen:
                continue
            order, parent = [root], {root: None}
            seen.add(root)
            for u in order:
                for v in adj[u]:
                    if v == parent[u]:
                        continue
                    if v in seen:
                        raise ValueError("bichromatic cycle: exact recovery impossible")
                    seen.add(v)
                    parent[v] = u
                    order.append(v)
            size = {v: 1 for v in order}
            for v in reversed(order[1:]):
                size[parent[v]] += size[v]
            N = len(order)
            cuts = {v: F(size[v] * (N - size[v]), N) for v in order[1:]}
            comp = dict(pair=pair, order=order, parent=parent, size=size,
                        cut_norm_sq=cuts, trace_inverse=sum(cuts.values(), F(0)),
                        max_degree=max(len(adj[v]) for v in order))
            components.append(comp)
    kappa2 = max((v for c in components for v in c['cut_norm_sq'].values()), default=F(0))
    # Finite exact certificates, valid for all real inputs, not fitted data.
    frobenius2 = max([F(1)] + [2 * c['trace_inverse'] for c in components])
    # Sharp-order operator certificate: disjoint branches within a tree,
    # disjoint selected action cells across neighbor colors (PROOF.md §5).
    local_component_sizes = [0] * n
    for c in components:
        for v in c['order']:
            local_component_sizes[v] += len(c['order']) - 1
    operator2 = F(1 + max(local_component_sizes, default=0))
    return dict(n=n, q=q, edges=edges, colors=list(colors), components=components,
                max_degree=max(degree, default=0), kappa2=kappa2,
                certified_frobenius_constant_sq=frobenius2,
                certified_operator_constant_sq=min(frobenius2, operator2))


def decode(plan, Y):
    """Least-squares each unsigned-incidence tree; free diagonals read directly."""
    n, q, colors = plan['n'], plan['q'], plan['colors']
    if len(Y) != n or any(len(row) != q for row in Y):
        raise ValueError("action shape")
    diagonal = [F(Y[i][colors[i]]) for i in range(n)]
    edge_values = {}
    for comp in plan['components']:
        a, b = comp['pair']
        order, parent, size = comp['order'], comp['parent'], comp['size']
        signed = {v: (1 if colors[v] == a else -1) * F(Y[v][b if colors[v] == a else a])
                  for v in order}
        total = sum(signed.values(), F(0))
        subtotal = signed.copy()
        N = len(order)
        for v in reversed(order[1:]):
            value = (1 if colors[v] == a else -1) * (subtotal[v] - F(size[v], N) * total)
            edge_values[tuple(sorted((v, parent[v])))] = value
            subtotal[parent[v]] += subtotal[v]
    return diagonal, edge_values


def action(n, q, colors, diagonal, edge_values):
    Y = [[F(0) for _ in range(q)] for _ in range(n)]
    for i, v in enumerate(diagonal):
        Y[i][colors[i]] += v
    for (u, v), w in edge_values.items():
        Y[u][colors[v]] += w
        Y[v][colors[u]] += w
    return Y


def matrix_frobenius_sq(diagonal, edge_values):
    return sum((v*v for v in diagonal), F(0)) + 2*sum((v*v for v in edge_values.values()), F(0))


def norm_sq(Y):
    return sum((v*v for row in Y for v in row), F(0))


def squared_path(n, deleted=None):
    deleted = set(deleted or [])
    es = [(u, v) for u in range(n) for v in (u+1, u+2) if v < n and (u, v) not in deleted]
    word = [0, 1, 2, 0, 3, 1, 0, 2, 3]
    return es, [word[i % 9] for i in range(n)]


def forest_prism(parents, bad=False):
    """Supplied rooted forest, parent index < child or None. No graph search hidden."""
    N = len(parents)
    depths = [0] * N
    edges = [(2*v, 2*v+1) for v in range(N)]
    for v, p in enumerate(parents):
        if p is not None:
            if not 0 <= p < v:
                raise ValueError("parents must precede children")
            depths[v] = depths[p] + 1
            edges.extend([(2*p, 2*v), (2*p+1, 2*v+1)])
    word = [0, 2, 1, 3]
    colors = []
    for d in depths:
        colors.extend([d % 2, 2+d % 2] if bad else [word[d % 4], word[(d+2) % 4]])
    return edges, colors


def cut_witness(plan, component_index=None, child=None):
    """D_e=1, ||DX||^2=1/a+1/b, exact adversarial witness for THIS seed only."""
    if not plan['components']:
        raise ValueError("no edges")
    if component_index is None:
        component_index = max(range(len(plan['components'])),
                              key=lambda i: max(plan['components'][i]['cut_norm_sq'].values()))
    comp = plan['components'][component_index]
    if child is None:
        child = max(comp['cut_norm_sq'], key=comp['cut_norm_sq'].get)
    order, parent, N = comp['order'], comp['parent'], len(comp['order'])
    if child not in comp['cut_norm_sq']:
        raise ValueError("cut edge")
    inside = {child}
    for v in order:
        if parent[v] in inside:
            inside.add(v)
    a, b = len(inside), N-len(inside)
    signed = {v: F(1, a) if v in inside else -F(1, b) for v in order}
    Y = [[F(0) for _ in range(plan['q'])] for _ in range(plan['n'])]
    ca, cb = comp['pair']
    for v in order:
        Y[v][cb if plan['colors'][v] == ca else ca] = (1 if plan['colors'][v] == ca else -1)*signed[v]
    diag, values = decode(plan, Y)
    actual = action(plan['n'], plan['q'], plan['colors'], diag, values)
    if actual != Y:
        raise ArithmeticError("exact cut witness failed")
    edge = tuple(sorted((child, parent[child])))
    assert abs(values[edge]) == 1 and norm_sq(Y) == F(1,a)+F(1,b)
    return dict(component_index=component_index, edge=edge, a=a, b=b,
                diagonal=diag, edge_values=values, action=Y,
                action_norm_sq=norm_sq(Y), inverse_lower_sq=F(a*b,N))
