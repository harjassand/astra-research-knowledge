#!/usr/bin/env python3
"""Exact finite primal/dual checks for positive rectangle covers of L^tensor t."""

from fractions import Fraction as F
from itertools import permutations


def labels(t):
    return [format(i, f"0{t}b") for i in range(1 << t)]


def subset(a, b):
    return all(x == "0" or y == "1" for x, y in zip(a, b))


def permute_label(a, p):
    out = ["0"] * len(a)
    for i, j in enumerate(p):
        out[j] = a[i]
    return "".join(out)


def rectangle_orbit(A, B, t):
    orbit = set()
    for p in permutations(range(t)):
        orbit.add((tuple(sorted(permute_label(a, p) for a in A)),
                   tuple(sorted(permute_label(b, p) for b in B))))
    return sorted(orbit)


# Each entry is (coefficient on every distinct coordinate-permutation image,
# row subset, column subset). Labels name subsets of [t], in binary order.
PRIMAL = {
    2: [
        (F(1, 4), ("00",), ("00",)),
        (F(1, 2), ("00",), ("00", "01", "10")),
        (F(1, 4), ("00",), ("00", "01", "10", "11")),
        (F(3, 4), ("01",), ("01",)),
        (F(1, 4), ("00", "01"), ("01", "11")),
        (F(1, 8), ("01", "11"), ("11",)),
        (F(1, 8), ("00", "01", "11"), ("11",)),
        (F(1, 2), ("01", "10", "11"), ("11",)),
    ],
    3: [
        (F(1, 5), ("000",), ("000", "001", "010", "011", "100")),
        (F(1, 20), ("000",), ("000", "001", "010", "011", "101")),
        (F(1, 30), ("000",), ("000", "001", "010", "011", "100", "101")),
        (F(4, 15), ("001",), ("001",)),
        (F(19, 60), ("001",), ("001", "011")),
        (F(1, 10), ("000", "001"), ("001", "011", "101")),
        (F(4, 15), ("011",), ("011",)),
        (F(3, 20), ("001", "011"), ("011",)),
        (F(1, 10), ("001", "010", "011"), ("011", "111")),
        (F(1, 3), ("000", "001", "010", "011"), ("011", "111")),
        (F(1, 30), ("001", "010", "111"), ("111",)),
        (F(1, 30), ("001", "010", "011", "111"), ("111",)),
        (F(4, 15), ("011", "101", "111"), ("111",)),
    ],
}


def y_weight(t, k, ell):
    if t == 2:
        return F(0) if (k, ell) == (1, 2) else F(1, 4)
    return {
        (0, 0): F(1, 5),
        (0, 1): F(0),
        (0, 2): F(1, 10),
        (0, 3): F(1, 10),
        (1, 1): F(1, 10),
        (1, 2): F(1, 10),
        (1, 3): F(1, 10),
        (2, 2): F(1, 10),
        (2, 3): F(0),
        (3, 3): F(1, 5),
    }[(k, ell)]


def row_dual(t, a):
    if t == 2:
        return F(1, 4) if len(a.replace("0", "")) == 0 else F(0)
    return {0: F(1, 5), 1: F(1, 10)}.get(len(a.replace("0", "")), F(0))


def col_dual(t, b):
    rank = len(b.replace("0", ""))
    if t == 2:
        return F(1, 4) if rank in (1, 2) else F(0)
    return {2: F(1, 10), 3: F(1, 5)}.get(rank, F(0))


def verify(t):
    states = labels(t)
    coverage = {(a, b): F(0) for a in states for b in states if subset(a, b)}
    row_load = {a: F(0) for a in states}
    col_load = {b: F(0) for b in states}
    primal_rectangles = set()

    for weight, A, B in PRIMAL[t]:
        orbit = rectangle_orbit(A, B, t)
        for AA, BB in orbit:
            assert all(subset(a, b) for a in AA for b in BB)
            primal_rectangles.add((AA, BB))
            for a in AA:
                row_load[a] += weight
            for b in BB:
                col_load[b] += weight
            for a in AA:
                for b in BB:
                    coverage[(a, b)] += weight

    assert all(value == 1 for value in coverage.values())
    cap = max(max(row_load.values()), max(col_load.values()))

    # Full, unsymmetrized dual certificate. For every allowed rectangle,
    # sum_{(a,b) in R} y_ab <= sum_{a in A} u_a + sum_{b in B} v_b.
    all_rectangles = []
    for bitsA in range(1, 1 << len(states)):
        A = tuple(states[i] for i in range(len(states)) if bitsA >> i & 1)
        for bitsB in range(1, 1 << len(states)):
            B = tuple(states[i] for i in range(len(states)) if bitsB >> i & 1)
            if all(subset(a, b) for a in A for b in B):
                all_rectangles.append((A, B))
    for A, B in all_rectangles:
        lhs = sum((y_weight(t, len(a.replace("0", "")),
                            len(b.replace("0", "")))
                   for a in A for b in B), F(0))
        rhs = sum((row_dual(t, a) for a in A), F(0)) + \
              sum((col_dual(t, b) for b in B), F(0))
        assert lhs <= rhs, (A, B, lhs, rhs)

    budget = sum((row_dual(t, a) for a in states), F(0)) + \
             sum((col_dual(t, b) for b in states), F(0))
    dual_value = sum((y_weight(t, len(a.replace("0", "")),
                               len(b.replace("0", "")))
                      for a, b in coverage), F(0))
    assert budget == 1
    assert dual_value == cap

    print(f"t={t}: allowed_rectangles={len(all_rectangles)}, "
          f"primal_rectangles={len(primal_rectangles)}, cap={cap}, "
          f"dual={dual_value}, budget={budget}")
    for side, loads in (("row", row_load), ("col", col_load)):
        by_rank = [sorted({v for a, v in loads.items()
                           if len(a.replace("0", "")) == k})[0]
                   for k in range(t + 1)]
        print(f"  {side} loads by Hamming rank: {by_rank}")


if __name__ == "__main__":
    verify(2)
    verify(3)
