#!/usr/bin/env python3
"""Exhaustive finite-state diagnostic for a dual-rail CRN ReLU module.

Formal CRN:
    Xp -> M + Yp
    M + Xn -> Yn

This is a diagnostic, not a physical DNA simulation. It enumerates every
reachable count vector for small integer inputs and confirms that every
terminal state has the rate-independent ReLU output. It then applies one
fuel-backed output leak F -> Yp to the zero-input terminal state.
"""
from collections import deque


def enabled(state):
    xp, xn, m, yp, yn = state
    out = []
    if xp >= 1:
        out.append((xp - 1, xn, m + 1, yp + 1, yn))
    if m >= 1 and xn >= 1:
        out.append((xp, xn - 1, m - 1, yp, yn + 1))
    return out


def explore(p, n):
    start = (p, n, 0, 0, 0)
    todo = deque([start])
    seen = {start}
    terminals = set()
    edges = 0
    while todo:
        state = todo.popleft()
        next_states = enabled(state)
        if not next_states:
            terminals.add(state)
            continue
        for nxt in next_states:
            edges += 1
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    return seen, terminals, edges


def main():
    checked_inputs = 0
    reachable_states = 0
    transition_edges = 0
    for p in range(9):
        for n in range(9):
            seen, terminals, edges = explore(p, n)
            checked_inputs += 1
            reachable_states += len(seen)
            transition_edges += edges
            expected = max(p - n, 0)
            assert len(terminals) == 1, (p, n, terminals)
            terminal = next(iter(terminals))
            xp, xn, m, yp, yn = terminal
            assert xp == 0
            assert yp - yn == expected, (p, n, terminal, expected)
            assert yp == p and yn == min(p, n)
            assert m == max(p - n, 0) and xn == max(n - p, 0)

    # One finite, fuel-backed spurious output event breaks the zero-input result.
    p = n = 0
    _, terminals, _ = explore(p, n)
    terminal = next(iter(terminals))
    xp, xn, m, yp, yn = terminal
    fuel_count = 1
    # Leak reaction F -> Yp, fired once.
    fuel_count -= 1
    yp += 1
    leaked_output = yp - yn
    assert leaked_output == 1 and fuel_count == 0

    print(f"input_pairs_checked={checked_inputs}")
    print(f"reachable_states_total={reachable_states}")
    print(f"transition_edges_total={transition_edges}")
    print("no_leak_terminal_output=ReLU(p-n) for every checked input")
    print("single_fuel_leak_on_(p,n)=(0,0): output=1 (incorrect)")


if __name__ == "__main__":
    main()
