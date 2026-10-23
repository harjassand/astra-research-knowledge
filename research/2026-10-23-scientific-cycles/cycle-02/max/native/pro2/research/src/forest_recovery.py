"""Three exact queries for symmetric matrices on a known forest.

This is the explicit depth-modulo-three star-coloring operation, not a claim
of a new coloring algorithm. Query rows have norm one. No actions on the
NIST matrix are taken here. Arithmetic is generic: Fraction inputs remain
exact. For arbitrary action error E, recovered coefficient error is at most
sqrt(2)*||E||_F in Frobenius norm, hence also in operator norm.
"""
from __future__ import annotations


def forest_design(parents):
    """Validate a rooted forest and return colors and its n-by-3 seed.

    parents[v] is -1 at a root and otherwise the index of v's parent.
    The validation does not require parents to precede their children.
    Construction costs O(n) time and storage, with three query columns.
    """
    n = len(parents)
    depth = [None] * n
    for v, p in enumerate(parents):
        if type(p) is not int or p < -1 or p >= n or p == v:
            raise ValueError('invalid parent')
    for start in range(n):
        if depth[start] is not None:
            continue
        trail, seen = [], set()
        v = start
        while v != -1 and depth[v] is None:
            if v in seen:
                raise ValueError('parent relation contains a cycle')
            seen.add(v)
            trail.append(v)
            v = parents[v]
        d = -1 if v == -1 else depth[v]
        for v in reversed(trail):
            d += 1
            depth[v] = d
    colors = [d % 3 for d in depth]
    seed = [[int(j == c) for j in range(3)] for c in colors]
    return colors, seed


def recover(parents, measured_action):
    """Return diagonal and edge-to-parent coefficients by direct reads.

    No subtraction, optimization, or matrix inversion is performed. Extra
    child-sum coordinates provide consistency information, but the bound
    needs only the directly read entries. Roots have edge coefficient zero.
    """
    colors, _ = forest_design(parents)
    if len(measured_action) != len(parents) or any(len(row) != 3 for row in measured_action):
        raise ValueError('action must have shape (n,3)')
    diagonal = [measured_action[v][colors[v]] for v in range(len(parents))]
    edges = [0 if p == -1 else measured_action[v][colors[p]]
             for v, p in enumerate(parents)]
    return diagonal, edges


def apply_supported(parents, diagonal, edges, seed):
    """Reference O(n*q) sparse action for testing and use with exact inputs."""
    n = len(parents)
    if len(diagonal) != n or len(edges) != n or len(seed) != n:
        raise ValueError('shape mismatch')
    q = len(seed[0]) if n else 0
    if any(len(row) != q for row in seed):
        raise ValueError('ragged seed')
    out = [[diagonal[v] * seed[v][j] for j in range(q)] for v in range(n)]
    for v, p in enumerate(parents):
        if p != -1:
            for j in range(q):
                out[v][j] += edges[v] * seed[p][j]
                out[p][j] += edges[v] * seed[v][j]
    return out
