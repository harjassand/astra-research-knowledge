#!/usr/bin/env python3
"""Exact compiler/reference test for unknown deterministic-transition leaf."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path
import json


def parts(N, colors):
    p = [1] + [0] * (N - 1)
    for gap in range(1, N):
        for _ in range(colors):
            for S in range(gap, N):
                p[S] += p[S - gap]
    return p


def pools(N, ell):
    cells = [(i, g) for g in range(1, N) for i in range(ell)]
    C = {}

    def visit(k, S):
        if k == len(cells):
            yield dict(C), S
            return
        i, g = cells[k]
        for u in range((N - 1 - S) // g + 1):
            if u:
                C[(i, g)] = u
            else:
                C.pop((i, g), None)
            yield from visit(k + 1, S + g * u)
        C.pop((i, g), None)

    yield from visit(0, 0)


def reference(N, ell):
    K = 1 + sum(parts(N, ell))
    law = defaultdict(F)
    law[(0,) * N] = F(1, K)

    def walk(C, phase, events, probability):
        outgoing = [(g, u) for (i, g), u in C.items() if i == phase]
        total = sum(u for _, u in outgoing)
        if not total:
            x = [0] * N
            for at in events:
                x[at - 1] = 1
            law[tuple(x)] += probability
            return
        for gap, u in outgoing:
            changed = dict(C)
            if u == 1:
                del changed[(phase, gap)]
            else:
                changed[(phase, gap)] = u - 1
            walk(changed, (phase + 1) % ell, events + [events[-1] + gap], probability * F(u, total))

    for C, S in pools(N, ell):
        for anchor in range(1, N - S + 1):
            for phase in range(ell):
                walk(C, phase, [anchor], F(1, ell * K * (N - S)))
    assert sum(law.values()) == 1 and len(law) == 2 ** N
    return law


def fall(u, r):
    return factorial(u) // factorial(u - r)


@lru_cache(maxsize=None)
def compiled(y, N, ell):
    K = 1 + sum(parts(N, ell))
    fac = factorial(N)
    scale = ell * K * fac
    events = [t + 1 for t, bit in enumerate(y) if bit]
    if not events:
        h = ell * fac
        for S, count in enumerate(parts(N, ell)):
            h += ell * count * max(0, N - S - len(y)) * (fac // (N - S))
        return F(h, scale)
    anchor, age = events[0], len(y) - events[-1]
    r = len(events) - 1
    H = 0
    for phase in range(ell):
        c = defaultdict(int)
        used = [0] * ell
        for t, (a, b) in enumerate(zip(events, events[1:])):
            origin = (phase + t) % ell
            c[(origin, b - a)] += 1
            used[origin] += 1
        last = (phase + r) % ell
        table = {(0, (0,) * ell): (1, 0)}
        for gap in range(1, N):
            for origin in range(ell):
                lower = c[(origin, gap)]
                new = defaultdict(lambda: [0, 0])
                for (S, rows), (A, B) in table.items():
                    for u in range(lower, (N - anchor - S) // gap + 1):
                        rv = list(rows)
                        rv[origin] += u
                        w = fall(u, lower)
                        tail = u - lower if origin == last and gap > age else 0
                        key = (S + gap * u, tuple(rv))
                        new[key][0] += w * A
                        new[key][1] += w * (B + tail * A)
                table = {key: tuple(v) for key, v in new.items()}
        for (S, rows), (A, B) in table.items():
            denom = N - S
            for R, used_count in zip(rows, used):
                denom *= fall(R, used_count)
            if rows[last] == used[last]:
                numerator = A
            else:
                numerator = B
                denom *= rows[last] - used[last]
            assert fac % denom == 0
            H += numerator * (fac // denom)
    return F(H, scale)


def true_probability(x, T, mu, pi):
    N = len(x)
    mean = sum(pi[i] * gap * p for i, row in enumerate(mu) for gap, p in row.items())
    events = [t + 1 for t, bit in enumerate(x) if bit]
    if not events:
        return sum(pi[i] * max(0, gap - N) * p for i, row in enumerate(mu) for gap, p in row.items()) / mean
    value = F(0)
    for first in range(len(T)):
        at = first
        term = sum(pi[i] * p for i, row in enumerate(mu) for gap, p in row.items()
                   if T[i] == first and gap >= events[0]) / mean
        for a, b in zip(events, events[1:]):
            term *= mu[at].get(b - a, F(0))
            at = T[at]
        term *= sum(p for gap, p in mu[at].items() if gap > N - events[-1])
        value += term
    return value


def main():
    cases = []
    for N in range(1, 7):
        references = [reference(N, ell) for ell in range(1, 4)]
        for q in range(1, 4):
            law = {x: sum(row[x] for row in references[:q]) / q for x in references[0]}
            prefix = defaultdict(F)
            for x, probability in law.items():
                for t in range(N + 1):
                    prefix[x[:t]] += probability
            equalities = normalizations = regret_checks = 0
            for t in range(N + 1):
                for y in product((0, 1), repeat=t):
                    p = sum(compiled(y, N, ell) for ell in range(1, q + 1)) / q
                    assert p == prefix[y]
                    equalities += 1
                    if t < N:
                        assert p == sum(sum(compiled(y + (bit,), N, ell) for ell in range(1, q + 1)) / q
                                        for bit in (0, 1))
                        normalizations += 1
            fixtures = [([0], [{1:F(1,2),5:F(1,2)}], [F(1)])]
            if q >= 2:
                fixtures.append(([1,0],[{1:F(1)},{2:F(1)}],[F(1,2),F(1,2)]))
            if q >= 3:
                fixtures.extend([
                    ([1,0,2],[{1:F(1)},{3:F(1)},{200:F(1)}],[F(1,4),F(1,4),F(1,2)]),
                    ([1,2,0],[{1:F(1,2),4:F(1,2)},{2:F(1)},{3:F(1)}],[F(1,3)]*3),
                    ([1,1,1],[{2:F(1)},{7:F(1)},{3:F(1)}],[F(0),F(1),F(0)]),
                ])
            K = 1 + sum(parts(N, q))
            for T, mu, pi in fixtures:
                total = F(0)
                for x, code_probability in law.items():
                    p = true_probability(x, T, mu, pi)
                    total += p
                    assert p <= q * q * K * N * code_probability
                    regret_checks += 1
                assert total == 1
            cases.append({"N":N,"state_bound":q,"prefix_equalities":equalities,
                          "normalizations":normalizations,"regret_checks":regret_checks})
    result={"status":"PASS","arithmetic":"exact integers/Fraction","cases":cases,
            "prefix_equalities":sum(c["prefix_equalities"] for c in cases),
            "normalizations":sum(c["normalizations"] for c in cases),
            "regret_checks":sum(c["regret_checks"] for c in cases),
            "scope":"Unknown-period cycle-code finite diagnostic, not external proof or generic hidden-state algorithm."}
    Path(__file__).with_name("PERIODIC_CHECKS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k != "cases"},indent=2))


if __name__ == "__main__":
    main()
