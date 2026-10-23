"""Degree-free operator certificate for a proper acyclic coordinate design.

The incidence least-squares decoder is inherited unchanged from Cycle4.
This module computes new centroid/cut information and reroots its plan.
All reported bounds are exact rational/integer, valid for arbitrary real noise.
"""
from fractions import Fraction as F
from collections import defaultdict
from coordinate_decoder import prepare as original_prepare, decode, action, norm_sq


def prepare(n, edges, colors, q=4):
    if type(n) is not int or n < 1:
        raise ValueError('the matrix dimension must be a positive integer')
    plan = original_prepare(n, edges, colors, q)
    neighbour_colors = [set() for _ in range(n)]
    for u, v in plan['edges']:
        neighbour_colors[u].add(colors[v])
        neighbour_colors[v].add(colors[u])
    r = max(map(len, neighbour_colors), default=0)
    maximum_branch = 0
    maximum_incoming = [0]*n
    for comp in plan['components']:
        order, parent, size = comp['order'], comp['parent'], comp['size']
        N = len(order)
        adj = defaultdict(list)
        for v in order[1:]:
            adj[v].append(parent[v]); adj[parent[v]].append(v)
        # Sizes at every possible root follow from one rooted traversal.
        balance = {v: max([N-size[v]] + [size[w] for w in adj[v]
                                        if parent.get(w) == v]) for v in order}
        root = min(order, key=lambda v: (balance[v], v))
        assert 2*balance[root] <= N
        order, parent = [root], {root: None}
        for u in order:
            for v in adj[u]:
                if v != parent[u]:
                    parent[v] = u; order.append(v)
        size = {v: 1 for v in order}
        for v in reversed(order[1:]):
            size[parent[v]] += size[v]
        M = max(size[v] for v in order[1:])
        cuts = {v: F(size[v]*(N-size[v]),N) for v in order[1:]}
        gamma = max(cuts.values())
        assert gamma <= M <= 2*gamma
        for v in order[1:]:
            maximum_incoming[v] += 1
        comp.update(order=order, parent=parent, size=size, cut_norm_sq=cuts,
                    centroid=root, maximum_child_subtree=M, gamma=gamma)
        maximum_branch = max(maximum_branch, M)
    incoming = max(maximum_incoming, default=0)
    assert incoming <= r
    plan.update(neighbour_color_count=r, maximum_incoming=incoming,
                centroid_branch_maximum=maximum_branch,
                gamma=plan['kappa2'],
                cut_operator_constant_sq=F(1+4*incoming*maximum_branch))
    plan['certified_operator_constant_sq'] = min(
        plan['certified_operator_constant_sq'], plan['cut_operator_constant_sq'])
    return plan


def subdivided_star(arm_lengths):
    """Supplied positive integer arm lengths; no graph recognition is hidden."""
    edges, colors, arms = [], [0], []
    for length in arm_lengths:
        if type(length) is not int or length < 1:
            raise ValueError('arm lengths must be positive integers')
        previous = 0; arm=[]
        for depth in range(1,length+1):
            v = len(colors); colors.append(depth % 2)
            edges.append((previous,v)); previous=v; arm.append(v)
        arms.append(arm)
    return len(colors), edges, colors, arms


def double_star(leaves_each):
    if type(leaves_each) is not int or leaves_each < 1:
        raise ValueError('positive leaf count')
    t = leaves_each
    n = 2+2*t
    edges = [(0,1)] + [(0,2+i) for i in range(t)] + [(1,2+t+i) for i in range(t)]
    colors = [0,1]+[1]*t+[0]*t
    return n, edges, colors


def summary(plan):
    return {'n': plan['n'], 'q': plan['q'], 'edges':len(plan['edges']),
            'maximum_degree':plan['max_degree'],
            'maximum_component_size':max((len(c['order']) for c in plan['components']),default=1),
            'gamma':str(plan['gamma']),
            'centroid_branch_maximum':plan['centroid_branch_maximum'],
            'maximum_incoming':plan['maximum_incoming'],
            'neighbour_color_count':plan['neighbour_color_count'],
            'cut_operator_constant_sq':str(plan['cut_operator_constant_sq']),
            'best_supplied_operator_constant_sq':str(plan['certified_operator_constant_sq'])}
