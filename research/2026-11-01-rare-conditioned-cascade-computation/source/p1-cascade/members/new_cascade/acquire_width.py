"""Elementary complete bounded-width search; no decomposition oracle.

For each k, memoize states (S,C), with C a connected component whose entire
outside neighborhood is S.  Select a bag B=S union X of size <=k+1, and
recurse on the components left after X.  The running time is n**O(k), not
the much better bounds of advanced established treewidth algorithms.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import combinations


def graph_from_scopes(scopes, n):
    graph = [set() for _ in range(n)]
    for scope in scopes:
        for u, v in combinations(scope, 2):
            graph[u].add(v)
            graph[v].add(u)
    return tuple(frozenset(s) for s in graph)


def components(graph, vertices):
    remaining = set(vertices)
    out = []
    while remaining:
        v = min(remaining)
        remaining.remove(v)
        found, stack = {v}, [v]
        while stack:
            u = stack.pop()
            new = graph[u] & remaining
            remaining.difference_update(new)
            found.update(new)
            stack.extend(new)
        out.append(frozenset(found))
    return out


def order_width(graph, order):
    graph = [set(s) for s in graph]
    live = set(range(len(graph)))
    width = 0
    for v in order:
        neighbors = graph[v] & live
        width = max(width, len(neighbors))
        for u in neighbors:
            graph[u].update(neighbors - {u})
        live.remove(v)
    return width


def acquire_order(scopes, n, max_width=None):
    graph = graph_from_scopes(scopes, n)
    if max_width is None:
        max_width = n - 1
    root_components = components(graph, range(n))
    counts = []
    for width in range(max_width + 1):
        @lru_cache(None)
        def solve(separator, component):
            separator, component = frozenset(separator), frozenset(component)
            if not component:
                return ()
            capacity = width + 1 - len(separator)
            if capacity < 1:
                return None
            for count in range(1, min(capacity, len(component)) + 1):
                for introduced in combinations(sorted(component), count):
                    bag = separator | frozenset(introduced)
                    order = []
                    success = True
                    for child in components(graph, component - set(introduced)):
                        boundary = frozenset().union(*(graph[v] for v in child)) - child
                        if not boundary <= bag:
                            raise AssertionError("Invalid subproblem boundary")
                        sub = solve(tuple(sorted(boundary)), tuple(sorted(child)))
                        if sub is None:
                            success = False
                            break
                        order.extend(sub)
                    if success:
                        return tuple(order) + tuple(introduced)
            return None

        order = []
        feasible = True
        for comp in root_components:
            piece = solve((), tuple(sorted(comp)))
            if piece is None:
                feasible = False
                break
            order.extend(piece)
        counts.append({"tested_width": width, "states": solve.cache_info().currsize})
        if feasible:
            actual = order_width(graph, order)
            if sorted(order) != list(range(n)) or actual > width:
                raise AssertionError("Bad constructed order")
            return order, actual, counts
    raise ValueError("No decomposition within the charged width limit")
