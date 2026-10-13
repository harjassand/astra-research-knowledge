"""Exact, finite checks for the Astra contact/critical-core investigation.

No floating-point optimization and no external theorem prover are used.
The small-graph tests are falsification tests, not proofs for arbitrary graphs.
"""
from __future__ import annotations
import itertools
import json
from functools import lru_cache
from pathlib import Path
import networkx as nx


def masks_from_graph(G: nx.Graph) -> tuple[int, ...]:
    G = nx.convert_node_labels_to_integers(G)
    return tuple(sum(1 << u for u in G.neighbors(v)) for v in G)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def chromatic(adj: tuple[int, ...], mask: int | None = None) -> int:
    if mask is None:
        mask = (1 << len(adj)) - 1
    if not mask:
        return 0
    ids = tuple(vertices(mask))
    # DSATUR branch and bound, with exact integer adjacency.
    colours: dict[int, int] = {}
    best = len(ids)
    def solve(used: int) -> None:
        nonlocal best
        if len(colours) == len(ids):
            best = min(best, used)
            return
        if used >= best:
            return
        uncol = [v for v in ids if v not in colours]
        forbidden = {v: {colours[u] for u in colours if adj[v] & (1 << u)}
                     for v in uncol}
        v = max(uncol, key=lambda u: (len(forbidden[u]), (adj[u] & mask).bit_count()))
        for c in range(min(used + 1, best)):
            if c not in forbidden[v]:
                colours[v] = c
                solve(max(used, c + 1))
                del colours[v]
    solve(0)
    return best


def connected_bipartite(adj: tuple[int, ...], mask: int) -> bool:
    if not mask:
        return False
    root = (mask & -mask).bit_length() - 1
    side = {root: 0}
    stack = [root]
    while stack:
        v = stack.pop()
        for u in vertices(adj[v] & mask):
            if u in side:
                if side[u] == side[v]:
                    return False
            else:
                side[u] = 1 - side[v]
                stack.append(u)
    return len(side) == mask.bit_count()


def is_perfect(adj: tuple[int, ...]) -> bool:
    # Exact strong-perfect-graph criterion: no induced odd hole or antihole.
    n = len(adj)
    for k in range(5, n + 1, 2):
        for ids in itertools.combinations(range(n), k):
            mask = sum(1 << u for u in ids)
            for complement in (False, True):
                nei = {v: ((mask & ~(1 << v) & ~adj[v]) if complement else adj[v] & mask)
                       for v in ids}
                if not all(nei[v].bit_count() == 2 for v in ids):
                    continue
                reached = {ids[0]}
                stack = [ids[0]]
                while stack:
                    v = stack.pop()
                    for u in vertices(nei[v]):
                        if u not in reached:
                            reached.add(u)
                            stack.append(u)
                if len(reached) == k:
                    return False
    return True


def quotient(adj: tuple[int, ...], parts: tuple[int, ...]) -> tuple[int, ...]:
    touch = []
    for part in parts:
        union = 0
        for v in vertices(part):
            union |= adj[v]
        touch.append(union)
    return tuple(sum(1 << j for j, p in enumerate(parts)
                     if j != i and touch[i] & p) for i in range(len(parts)))


def perfect_bipartite_partition(adj: tuple[int, ...]) -> tuple[int, ...] | None:
    n = len(adj)
    full = (1 << n) - 1
    by_vertex: list[list[int]] = [[] for _ in range(n)]
    for mask in range(1, full + 1):
        if connected_bipartite(adj, mask):
            for v in vertices(mask):
                by_vertex[v].append(mask)
    for options in by_vertex:
        options.sort(key=int.bit_count, reverse=True)
    def recurse(left: int, parts: tuple[int, ...]):
        if not left:
            return parts if is_perfect(quotient(adj, parts)) else None
        v = (left & -left).bit_length() - 1
        for part in by_vertex[v]:
            if part & left == part:
                result = recurse(left ^ part, parts + (part,))
                if result is not None:
                    return result
        return None
    return recurse(full, ())


def matchings(vs: tuple[int, ...]):
    if not vs:
        yield ()
        return
    a = vs[0]
    for i in range(1, len(vs)):
        b = vs[i]
        for rest in matchings(vs[1:i] + vs[i+1:]):
            yield ((a,b),) + rest


def matching_check(G: nx.Graph):
    G = nx.convert_node_labels_to_integers(G)
    total = legal = touching = 0
    for matching in matchings(tuple(G)):
        total += 1
        if not all(G.has_edge(*e) for e in matching):
            continue
        legal += 1
        if all(any(G.has_edge(u, v) for u in a for v in b)
               for a, b in itertools.combinations(matching, 2)):
            touching += 1
    return dict(total_complete_graph_matchings=total,
                legal_perfect_matchings=legal,
                pairwise_touching_perfect_matchings=touching)


def run():
    bridge = nx.disjoint_union(nx.complete_graph(4), nx.complete_graph(4))
    bridge.add_edge(3,4)
    bridge_result = matching_check(bridge)
    assert bridge_result == dict(total_complete_graph_matchings=105,
                                 legal_perfect_matchings=9,
                                 pairwise_touching_perfect_matchings=0)
    assert chromatic(masks_from_graph(bridge)) == 4
    # Independent cross-check of the chromatic solver on every atlas graph.
    # A simple exhaustive partition into independent sets is used as reference.
    @lru_cache(None)
    def reference_chi(adj: tuple[int, ...], mask: int) -> int:
        if not mask:
            return 0
        bit = mask & -mask
        best = mask.bit_count()
        sub = mask
        while sub:
            if sub & bit and all(not (adj[v] & sub) for v in vertices(sub)):
                best = min(best, 1 + reference_chi(adj, mask ^ sub))
            sub = (sub - 1) & mask
        return best
    atlas = nx.graph_atlas_g()
    critical = []
    for index, G in enumerate(atlas):
        adj = masks_from_graph(G)
        n = len(adj)
        full = (1 << n) - 1
        chi = chromatic(adj)
        assert chi == reference_chi(adj, full), (index, chi)
        if n and all(chromatic(adj, full ^ (1 << v)) < chi for v in range(n)):
            parts = perfect_bipartite_partition(adj)
            assert parts is not None, ('critical counterexample', index)
            assert all(connected_bipartite(adj, p) for p in parts)
            assert is_perfect(quotient(adj, parts))
            critical.append(dict(atlas_index=index, n=n, edges=G.number_of_edges(), chi=chi,
                                 bags=[list(vertices(p)) for p in parts]))
    result = dict(bridge_example=bridge_result,
                  atlas_graphs_tested=len(atlas),
                  atlas_max_order=7,
                  critical_graphs_tested=len(critical),
                  critical_failures=0, critical_witnesses=critical,
                  warning='Small finite tests do not establish the general structural conjecture.')
    out = Path(__file__).with_name('finite_checks.json')
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps({k:v for k,v in result.items() if k != 'critical_witnesses'}, indent=2))

if __name__ == '__main__':
    run()
