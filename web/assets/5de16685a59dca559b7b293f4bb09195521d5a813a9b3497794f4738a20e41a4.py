"""Exact rational BCS tree tensors with acquired structural decompositions.

Tree leaves are original site labels. A recursive leaf ordering makes every
subtree contiguous; the exact fermionic permutation is tracked on amplitudes.
Counts and samples return the original physical site ordering.
"""
from cutrank_bcs import *
from dataclasses import dataclass
from itertools import combinations


def leaves(tree):
    out, todo = [], [tree]
    while todo:
        t = todo.pop()
        if isinstance(t, int):
            out.append(t)
        else:
            if len(t) != 2:
                raise ValueError('binary site tree required')
            todo.extend((t[1],t[0]))
    return out


def balanced_join(parts):
    if not parts:
        raise ValueError('empty partition')
    if len(parts) == 1:
        return parts[0]
    k = len(parts)//2
    return balanced_join(parts[:k]), balanced_join(parts[k:])


def balanced_order_tree(n):
    return balanced_join(list(range(n)))


def support_graph(F):
    n = len(F)
    return [{j for j in range(n) if j != i and (F[i][j] or F[j][i])}
            for i in range(n)]


def components(adj, vertices):
    todo, out = set(vertices), []
    while todo:
        seed = min(todo)
        todo.remove(seed)
        todo_stack, comp = [seed], [seed]
        while todo_stack:
            v = todo_stack.pop()
            for u in sorted(adj[v] & todo):
                todo.remove(u)
                todo_stack.append(u)
                comp.append(u)
        out.append(sorted(comp))
    return out


def forest_tree(F):
    """Acquires a binary site partition of bidirectional cut rank <=2.

    Returns None exactly when the undirected off-diagonal support has a cycle.
    """
    adj = support_graph(F)
    seen, parent, child, traversal, roots = set(), {}, {}, [], []
    for root in range(len(F)):
        if root in seen:
            continue
        roots.append(root)
        seen.add(root)
        parent[root] = None
        todo = [root]
        while todo:
            v = todo.pop()
            traversal.append(v)
            child[v] = []
            for u in sorted(adj[v]):
                if u == parent[v]:
                    continue
                if u in seen:
                    return None
                seen.add(u)
                parent[u] = v
                child[v].append(u)
                todo.append(u)
    built = {}
    for v in reversed(traversal):
        parts = [built[u] for u in child[v]]
        built[v] = v if not parts else (v,balanced_join(parts))
    parts = [built[v] for v in roots]
    return balanced_join(parts)


def separator_tree(F, separator_bound):
    """Deterministic bounded-support-separator recognition and acquisition.

    Enumerates all candidate separators of size <= the fixed public bound.
    Rejects if a recursively encountered induced subgraph has no such balanced
    separator. Acceptance is broader than a treewidth certificate.
    """
    if separator_bound < 1:
        raise ValueError('positive fixed separator bound required')
    adj = support_graph(F)
    witness = []

    def build(S, depth):
        if len(S) == 1:
            return S[0]
        choice = None
        for size in range(min(separator_bound, len(S))+1):
            for sep in combinations(S, size):
                cs = components(adj, set(S)-set(sep))
                if all(2*len(c) <= len(S) for c in cs):
                    choice = list(sep), cs
                    break
            if choice is not None:
                break
        if choice is None:
            raise ValueError({'failed_induced_sites': S,
                              'separator_bound': separator_bound})
        sep, cs = choice
        witness.append({'sites': S, 'separator': sep, 'components': cs,
                        'recursive_depth': depth})
        parts = [build(c, depth+1) for c in cs] + sep
        return balanced_join(parts)

    return build(list(range(len(F))), 0), witness


def acquire_subset_basis(F, sites):
    n = len(F)
    outside = [i for i in range(n) if i not in set(sites)]
    U0 = [[F[i][j] for j in outside] for i in sites]
    D0 = [[F[j][i] for j in outside] for i in sites]
    uc, dc = pivot_cols(U0), pivot_cols(D0)
    Ur = [[row[j] for j in uc] for row in U0]
    Dr = [[row[j] for j in dc] for row in D0]
    up, down = zeros(n, len(uc)), zeros(n, len(dc))
    for i, site in enumerate(sites):
        up[site], down[site] = Ur[i], Dr[i]
    ur, dr = pivot_cols(transpose(Ur)), pivot_cols(transpose(Dr))
    pivots = sorted([2*sites[i] for i in ur]+[2*sites[i]+1 for i in dr])
    return CutBasis(len(sites), up, down, pivots)


def kron(a, b):
    out = zeros(len(a)*len(b), len(a[0])*len(b[0]))
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j]:
                for k in range(len(b)):
                    for l in range(len(b[0])):
                        if b[k][l]:
                            out[i*len(b)+k][j*len(b[0])+l] = a[i][j]*b[k][l]
    return out


@dataclass
class Node:
    sites: list
    basis: CutBasis
    left: object = None
    right: object = None
    tensor: object = None

    @property
    def is_leaf(self):
        return self.left is None


@dataclass
class BCSTree:
    original_F: list
    F: list
    order: list
    root: Node
    nodes: list

    @property
    def max_cutrank(self):
        return max(v.basis.rank for v in self.nodes)

    def amplitude(self, states):
        x = [states[i] for i in self.order]
        amplitudes = {}
        for node in self.nodes:
            if node.is_leaf:
                value = [node.tensor[x[node.sites[0]]]]
            else:
                a, b = amplitudes[id(node.left)], amplitudes[id(node.right)]
                row = [[u*v for u in a[0] for v in b[0]]]
                value = mm(row,node.tensor)
            amplitudes[id(node)] = value
        z = amplitudes[id(self.root)][0][0]
        parity = sum(x[i].bit_count()*x[j].bit_count()
                     for i in range(len(x)) for j in range(i+1, len(x))
                     if self.order[i] > self.order[j]) & 1
        return -z if parity else z


def acquire_tree(F, tree, max_dimension=256):
    original = [[C.of(x) for x in row] for row in F]
    n = len(F)
    if not n or not all(len(row) == n for row in F):
        raise ValueError('nonempty square F required')
    order = leaves(tree)
    if sorted(order) != list(range(n)):
        raise ValueError('tree leaves must partition all physical sites')
    position = {site: i for i, site in enumerate(order)}
    F = [[original[i][j] for j in order] for i in order]
    nodes = []

    node_map, todo = {}, [(tree,False)]
    key = lambda t: ('leaf',t) if isinstance(t,int) else ('node',id(t))
    while todo:
        t, visited = todo.pop()
        if not isinstance(t,int) and not visited:
            todo.extend(((t,True),(t[1],False),(t[0],False)))
            continue
        if isinstance(t,int):
            sites = [position[t]]
            node = Node(sites, acquire_subset_basis(F, sites))
        else:
            a, b = node_map[key(t[0])], node_map[key(t[1])]
            sites = a.sites+b.sites
            node = Node(sites, acquire_subset_basis(F, sites), a, b)
        nodes.append(node)
        node_map[key(t)] = node
    root = node_map[key(tree)]
    if max(v.basis.dim for v in nodes) > max_dimension:
        raise ValueError('explicit resource cap exceeded; no approximation made')
    for node in nodes:
        basis = node.basis
        if node.is_leaf:
            s = node.sites[0]
            node.tensor = []
            for x in range(4):
                occ = ([2*s] if x & 1 else [])+([2*s+1] if x & 2 else [])
                node.tensor.append([basis_amplitude(F, basis, occ, z)
                                    for z in range(basis.dim)])
        else:
            a, b = node.left.basis, node.right.basis
            H = []
            for y in range(a.dim):
                for z in range(b.dim):
                    occ = occupation_of_pivots(a.pivots, y)+ \
                          occupation_of_pivots(b.pivots, z)
                    H.append([basis_amplitude(F, basis, occ, label)
                              for label in range(basis.dim)])
            Kinv = kron(inverse(pivot_matrix(F, a)), inverse(pivot_matrix(F, b)))
            node.tensor = mm(Kinv, H)
    return BCSTree(original, F, order, root, nodes)


def tree_counts(compiled, t=None, allowed=None):
    n = len(compiled.F)
    original_weights = local_weights(n, t, allowed)
    weights = [original_weights[i] for i in compiled.order]

    contracted = {}
    for node in compiled.nodes:
        d = node.basis.dim
        out = {}
        if node.is_leaf:
            site = node.sites[0]
            for x in range(4):
                w = weights[site][x]
                if not w:
                    continue
                k = x & 1
                if k not in out:
                    out[k] = zeros(d, d)
                row = node.tensor[x]
                add_scaled(out[k], [[a.conj()*b for b in row] for a in row], w)
        else:
            left, right = contracted[id(node.left)], contracted[id(node.right)]
            Td = dagger(node.tensor)
            for i, A in left.items():
                for j, B in right.items():
                    k = i+j
                    if k not in out:
                        out[k] = zeros(d, d)
                    value = mm(mm(Td, kron(A, B)), node.tensor)
                    add_scaled(out[k], value, 1)
        contracted[id(node)] = out
    E = contracted[id(compiled.root)]
    return [real_nonnegative(E.get(k, [[ZERO]])[0][0]) for k in range(n+1)]


def tree_sample(compiled, k, t=None, rng=None, allowed=None):
    rng = random.SystemRandom() if rng is None else rng
    n = len(compiled.F)
    if not isinstance(k, int) or not 0 <= k <= n:
        raise ValueError('pair count must be an integer in [0,n]')
    allowed = [set(range(4)) for _ in range(n)] if allowed is None else [set(s) for s in allowed]
    if not tree_counts(compiled, t, allowed)[k]:
        raise ValueError('zero requested sector')
    states = []
    for i in range(n):
        qs = []
        permitted = set(allowed[i])
        for x in range(4):
            if x not in permitted:
                qs.append(Q(0))
                continue
            allowed[i] = {x}
            qs.append(tree_counts(compiled, t, allowed)[k])
        x = integer_choice(qs, rng)
        states.append(x)
        allowed[i] = {x}
    return states
