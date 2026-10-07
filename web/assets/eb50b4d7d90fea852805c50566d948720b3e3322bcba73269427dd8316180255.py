#!/usr/bin/env python3
"""Small exact diagnostics for the source-swap boundary lemma.

Network format: each edge is (source_complex, product_complex, rational_rate),
and a complex is a tuple of nonnegative integers. This is a diagnostic, not a
generic reachability or recurrence solver.
"""

from collections import deque
from fractions import Fraction
from math import prod


def support(x):
    return frozenset(i for i, a in enumerate(x) if a > 0)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def enabled(x, y):
    return all(a >= b for a, b in zip(x, y))


def falling(x, y):
    if not enabled(x, y):
        return 0
    out = 1
    for a, b in zip(x, y):
        for k in range(b):
            out *= a - k
    return out


def path_edges(edges, start, finish):
    """Return a shortest directed complex path, including its edge indices."""
    adjacency = {}
    for i, (y, yp, _rate) in enumerate(edges):
        adjacency.setdefault(y, []).append((yp, i))
    todo = deque([start])
    parent = {start: None}
    while todo:
        y = todo.popleft()
        if y == finish:
            break
        for yp, i in adjacency.get(y, ()):
            if yp not in parent:
                parent[yp] = (y, i)
                todo.append(yp)
    if finish not in parent:
        return None
    out = []
    node = finish
    while parent[node] is not None:
        prev, edge_i = parent[node]
        out.append(edge_i)
        node = prev
    return tuple(reversed(out))


def apply_word(edges, x, edge_ids):
    """Apply enabled reaction edges and check the spectator identity."""
    states = [tuple(x)]
    for edge_i in edge_ids:
        y, yp, _rate = edges[edge_i]
        cur = states[-1]
        assert enabled(cur, y), (cur, y, edge_i)
        nxt = add(cur, sub(yp, y))
        assert all(a >= 0 for a in nxt)
        states.append(nxt)
    return tuple(states)


def face_escape(edges, I):
    """Return a source-supported-in-I edge that creates a species outside I."""
    for i, (y, yp, _rate) in enumerate(edges):
        if support(y) <= I and support(yp) - I:
            return i
    return None


def face_invariant(edges, I):
    return face_escape(edges, I) is None


def exact_path_probability_lower_bound(edges, x, edge_ids):
    """Uniform rational lower bound for the prescribed next-jump word.

    Assumes every complex has molecularity at most two and all listed rates
    are positive rationals. Uses q(state) <= R*kappa_max*(1+|state|+M)^2.
    """
    if not edges:
        return Fraction(1)
    rates = [rate for _y, _yp, rate in edges]
    assert all(isinstance(rate, Fraction) and rate > 0 for rate in rates)
    assert all(sum(y) <= 2 and sum(yp) <= 2 for y, yp, _ in edges)
    kmin, kmax = min(rates), max(rates)
    M = max(sum(y) for y, yp, _ in edges for y in (y, yp))
    N = sum(x)
    states = apply_word(edges, x, edge_ids)
    q_upper = len(edges) * kmax * (1 + N + M) ** 2
    one_step = min(Fraction(1), kmin / q_upper)
    assert all(falling(states[j], edges[edge_i][0]) >= 1
               for j, edge_i in enumerate(edge_ids))
    return one_step ** len(edge_ids)


def check_network(name, edges, states):
    d = len(edges[0][0])
    complexes = sorted({z for y, yp, _ in edges for z in (y, yp)})
    M = tuple(max(z[i] for z in complexes) for i in range(d))
    checks = 0
    for x in states:
        I = support(x)
        if all(x[i] >= M[i] + 1 for i in I) and not face_invariant(edges, I):
            edge_i = face_escape(edges, I)
            y, yp, _rate = edges[edge_i]
            assert enabled(x, y)
            nxt = add(x, sub(yp, y))
            assert I <= support(nxt)
            assert support(yp) - I
            checks += 1
    print(f"{name}: complexes={len(complexes)}, M={M}, thick-face checks={checks}")


def main():
    # A+B <-> 2A: deterministic B=0 face points outward, but the lattice
    # state (A,B)=(1,0) is an absorbing class because the dimer source is not
    # enabled. At (2,0), the outward reaction is enabled and stays in the same
    # weakly reversible communicating class.
    ab_2a = [
        ((1, 1), (2, 0), Fraction(1)),
        ((2, 0), (1, 1), Fraction(1)),
    ]
    assert not face_invariant(ab_2a, frozenset({0}))
    assert all(not enabled((1, 0), y) for y, _yp, _r in ab_2a)
    edge_i = face_escape(ab_2a, frozenset({0}))
    path = (edge_i,)
    states = apply_word(ab_2a, (2, 0), path)
    assert states == ((2, 0), (1, 1))
    assert path_edges(ab_2a, (1, 1), (2, 0)) is not None
    p_lower = exact_path_probability_lower_bound(ab_2a, (2, 0), path)
    assert p_lower > 0
    print(f"A+B<->2A: (1,0) absorbing; (2,0)->(1,1), path probability >= {p_lower}")

    # A <-> 2A: the empty face is invariant and the positive lattice states
    # form a separate weakly reversible class. This catches the need for a
    # component/face restriction in any recovery theorem.
    a_2a = [
        ((1,), (2,), Fraction(2)),
        ((2,), (1,), Fraction(3)),
    ]
    assert face_invariant(a_2a, frozenset())
    assert face_invariant(a_2a, frozenset({0}))
    assert all(not enabled((0,), y) for y, _yp, _r in a_2a)
    assert path_edges(a_2a, (1,), (2,)) is not None
    check_network("A+B<->2A", ab_2a, [(a, b) for a in range(8) for b in range(8)])
    check_network("A<->2A", a_2a, [(a,) for a in range(12)])
    print("diagnostics: all exact assertions passed; this does not prove recurrence or a global Foster bound")


if __name__ == "__main__":
    main()
