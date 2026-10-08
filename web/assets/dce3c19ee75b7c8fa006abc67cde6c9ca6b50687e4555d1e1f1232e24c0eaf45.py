#!/usr/bin/env python3
"""Finite exact transcription check for REPORT.txt's sparse WR network.

This checks formulas and finite-state connectivity only. The report's
all-state drift, localization, and recurrence arguments are analytic.
"""

from collections import deque
from fractions import Fraction


def transitions(a: int, b: int, m: int):
    c = m - b
    assert 0 <= b <= m
    out = []
    # A+B <-> 2A+B, forward rate 2 and reverse rate 1.
    if a >= 1 and b >= 1:
        out.append(((a + 1, b), 2 * a * b, 1))
    if a >= 2 and b >= 1:
        out.append(((a - 1, b), a * (a - 1) * b, -1))
    # A+C <-> 2A+C, both rates 1.
    if a >= 1 and c >= 1:
        out.append(((a + 1, b), a * c, 1))
    if a >= 2 and c >= 1:
        out.append(((a - 1, b), a * (a - 1) * c, -1))
    # A+B <-> A+C, both rates 1.
    if a >= 1 and b >= 1:
        out.append(((a, b - 1), a * b, 0))
    if a >= 1 and c >= 1:
        out.append(((a, b + 1), a * c, 0))
    return out


def check_formulas():
    for m in range(1, 9):
        for a in range(0, 41):
            for b in range(m + 1):
                c = m - b
                tr = transitions(a, b, m)
                assert all(rate > 0 and 0 <= nb <= m for (_, nb), rate, _ in tr)
                q = sum(rate for _, rate, _ in tr)
                lv = sum(rate * da for _, rate, da in tr)
                expected_lv = a * (b + (2 - a) * m)
                expected_q = a * a * m + a * (m + b)
                assert lv == expected_lv, (m, a, b, lv, expected_lv)
                assert q == expected_q, (m, a, b, q, expected_q)
                assert lv <= 2 * m, (m, a, b, lv)
                if a >= 4:
                    assert lv <= -a * m, (m, a, b, lv)
                if a >= 8:
                    assert Fraction(lv, q) <= Fraction(-1, 2)


def check_active_class_connectivity(m: int, a_max: int):
    vertices = {(a, b) for a in range(1, a_max + 1) for b in range(m + 1)}
    start = (1, 0)
    seen = {start}
    queue = deque([start])
    while queue:
        a, b = queue.popleft()
        for (na, nb), _, _ in transitions(a, b, m):
            nxt = (na, nb)
            if nxt in vertices and nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    assert seen == vertices, (m, a_max, len(seen), len(vertices))


def main():
    # Edge-balance conditions on the tree would require both values below to
    # equal c_A; this rate choice gives 2 and 1.
    assert Fraction(2, 1) != Fraction(1, 1)
    check_formulas()
    for m in range(1, 7):
        check_active_class_connectivity(m, 12)
    print("PASS: generator, total-rate, drift, and finite active-class checks")
    print("Scope: finite diagnostics only; see the analytic report proof.")


if __name__ == "__main__":
    main()
