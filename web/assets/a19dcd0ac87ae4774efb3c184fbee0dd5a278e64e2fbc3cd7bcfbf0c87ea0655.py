#!/usr/bin/env python3
"""Exact tiny-state check for a bimolecular strongly endotactic network.

Network: 2A -> A+B and 2B -> A+B, with integer-count propensity
k * n(n-1), omitting the common factorial convention (which only rescales
rates). This checks reachable transitions, communication distinctions, and
source-direction witnesses for totals 1 and 2. It is a finite diagnostic;
the all-direction endotactic proof is given analytically in INITIAL.txt.
"""
from fractions import Fraction
from collections import deque

# State is (A,B); each transition is (source complex, jump, label).
REACTIONS = [
    ((2, 0), (-1, 1), "2A -> A+B"),
    ((0, 2), (1, -1), "2B -> A+B"),
]


def enabled(state, source):
    return all(state[i] >= source[i] for i in range(2))


def successors(state):
    out = []
    for source, jump, label in REACTIONS:
        if enabled(state, source):
            nxt = tuple(state[i] + jump[i] for i in range(2))
            # Exact positive propensity up to a positive rate constant.
            propensity = 1
            for i in range(2):
                for r in range(source[i]):
                    propensity *= state[i] - r
            assert propensity > 0
            out.append((nxt, label, propensity))
    return out


def reachable(start):
    todo, seen = deque([start]), {start}
    while todo:
        x = todo.popleft()
        for y, _, _ in successors(x):
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def main():
    # For every non-normal w, the maximizing source's edge points strictly
    # inward: if w_A>w_B, 2A is maximal and w.(-1,1)<0; conversely for 2B.
    # Use rational witness vectors on both sides as a compact arithmetic check.
    for w in ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)),
              (Fraction(2), Fraction(1)), (Fraction(1), Fraction(2))):
        wa, wb = w
        if wa > wb:
            assert wa * (-1) + wb * 1 < 0
        elif wb > wa:
            assert wa * 1 + wb * (-1) < 0

    total1 = {(1, 0), (0, 1)}
    assert all(successors(x) == [] for x in total1)

    total2 = {(2, 0), (1, 1), (0, 2)}
    assert reachable((2, 0)) == {(2, 0), (1, 1)}
    assert reachable((0, 2)) == {(0, 2), (1, 1)}
    assert successors((1, 1)) == []
    # Every state has the same total and lies in the integer stoichiometric
    # coset, while the count-space communicating structure is not one class.
    assert all(a + b == 2 for a, b in total2)
    assert (1, 1) in reachable((2, 0)) and (2, 0) not in reachable((1, 1))

    print({
        "network": "2A->A+B; 2B->A+B",
        "total_1_absorbing_states": sorted(total1),
        "total_2_reach_from_2A": sorted(reachable((2, 0))),
        "total_2_reach_from_2B": sorted(reachable((0, 2))),
        "total_2_center_successors": successors((1, 1)),
        "diagnostic_scope": "exact finite enabledness/reachability only",
    })


if __name__ == "__main__":
    main()
