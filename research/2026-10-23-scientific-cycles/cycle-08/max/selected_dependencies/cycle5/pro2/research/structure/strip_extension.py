"""Exact four-color reset extension for long squared-path triangle strips.

This does not color an arbitrary partial 2-tree.  It extends any supplied proper
colors on the two end edges of P_n^2, n >= 30.  No optimizer or floating point.
"""
from itertools import permutations

PERIOD = (0, 1, 2, 0, 3, 1, 0, 2, 3)
PAIRS = tuple(permutations(range(4), 2))


def six_step_table():
    """All 144 ordered-pair transitions; appended tuple has exactly 6 colors."""
    table = {}
    for start in PAIRS:
        frontier = {start: ()}
        for _ in range(6):
            following = {}
            for (a, b), word in sorted(frontier.items()):
                for c in range(4):
                    if c != a and c != b:
                        following.setdefault((b, c), word + (c,))
            frontier = following
        if set(frontier) != set(PAIRS):
            raise AssertionError("six-step transition closure failed")
        for end, word in frontier.items():
            table[(start, end)] = word
    return table


TRANSITIONS = six_step_table()


def extend_strip(n, left, right):
    """Return colors on ordered P_n^2 with specified end pairs, n >= 30."""
    left, right = tuple(left), tuple(right)
    if n < 30 or left not in PAIRS or right not in PAIRS:
        raise ValueError("need n >= 30 and ordered distinct color pairs in 0..3")
    prefix = left + TRANSITIONS[(left, (0, 1))]
    core = tuple(PERIOD[i % 9] for i in range(n - 12))
    suffix = TRANSITIONS[(core[-2:], right)]
    word = prefix[:-2] + core + suffix
    assert len(word) == n and word[:2] == left and word[-2:] == right
    return word


def square_edges(n):
    return [(i, j) for i in range(n) for j in range(i + 1, min(n, i + 3))]


def triangle_components(vertices, edges):
    """Maximal unions of triangles connected by shared edges; Δ is not assumed.

    For bounded Δ, triangle listing and incidence traversal cost O(n).
    The full support is materialized exactly once.
    """
    vertices, edges = list(vertices), [tuple(sorted(e)) for e in edges]
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    triangles = [(u, v, w) for u in vertices for v in adjacency[u] if u < v
                 for w in adjacency[u] & adjacency[v] if v < w]
    by_edge = {}
    for i, (a, b, c) in enumerate(triangles):
        for e in ((a, b), (a, c), (b, c)):
            by_edge.setdefault(e, []).append(i)
    seen, groups = set(), []
    for i in range(len(triangles)):
        if i in seen:
            continue
        seen.add(i); stack = [i]; vertices_here = set()
        while stack:
            a, b, c = triangles[stack.pop()]
            vertices_here.update((a, b, c))
            for e in ((a, b), (a, c), (b, c)):
                for j in by_edge[e]:
                    if j not in seen:
                        seen.add(j); stack.append(j)
        groups.append(tuple(vertices_here))
    return groups


def long_strip_orders(vertices, edges, threshold=30):
    """Extract and validate long triangle strips, conditional on TW<=2, Δ<=4.

    The procedure validates the strip and saturation assertions actually used.
    It does not independently certify the graph's treewidth.
    """
    vertices, edges = list(vertices), [tuple(sorted(e)) for e in edges]
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if max(map(len, adjacency.values()), default=0) > 4:
        raise ValueError("maximum degree exceeds four")
    orders = []
    for component in triangle_components(vertices, edges):
        if len(component) < threshold:
            continue
        vs = set(component)
        local = {v: adjacency[v] & vs for v in vs}
        ends = sorted(v for v in vs if len(local[v]) == 2)
        if len(ends) != 2:
            raise ValueError("long triangle component is not a squared path")
        first = ends[0]
        seconds = [v for v in local[first] if len(local[v]) == 3]
        if len(seconds) != 1:
            raise ValueError("cannot identify second strip vertex")
        order = [first, seconds[0]]
        seen = set(order)
        while len(order) < len(component):
            following = (local[order[-2]] & local[order[-1]]) - seen
            if len(following) != 1:
                raise ValueError("ambiguous squared-path continuation")
            nxt = next(iter(following))
            order.append(nxt)
            seen.add(nxt)
        expected = {tuple(sorted((order[i], order[j]))) for i, j in square_edges(len(order))}
        actual = {(u, v) for u in vs for v in local[u] if u < v}
        if expected != actual:
            raise ValueError("strip has wrong edge pattern")
        if any(adjacency[v] - vs for v in order[2:-2]):
            raise ValueError("internal strip vertex has an outside edge")
        orders.append(tuple(order))
    return orders


def reduce_long_strips(vertices, edges):
    vertices, edges = list(vertices), [tuple(sorted(e)) for e in edges]
    orders = long_strip_orders(vertices, edges)
    deleted = {v for order in orders for v in order[2:-2]}
    kept = [v for v in vertices if v not in deleted]
    reduced_edges = [(u, v) for u, v in edges if u not in deleted and v not in deleted]
    return kept, reduced_edges, orders


def extend_reduced_coloring(colors, orders):
    """Caller supplies a proper reduced coloring; no hidden coloring solver."""
    answer = dict(colors)
    for order in orders:
        word = extend_strip(len(order), tuple(answer[v] for v in order[:2]),
                            tuple(answer[v] for v in order[-2:]))
        for v, c in zip(order, word):
            if v in answer and answer[v] != c:
                raise ValueError("inconsistent shared port color")
            answer[v] = c
    return answer
