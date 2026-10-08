#!/usr/bin/env python3
"""Independent exact diagnostic for the observed-mark row-urn code.

The reference explicitly enumerates colored count pools and every row-urn
path, allowing unused pools. The compiler independently sums product weights
over total span and row totals. Neither imports a root or other-worker checker.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path
import json
import time


def colored_partitions(N, q):
    p = [0] * N
    p[0] = 1
    for j in range(1, N):
        for _ in range(q * q):
            for s in range(j, N):
                p[s] += p[s - j]
    return p


def pools(N, q):
    cells = [(i, d, j) for j in range(1, N) for i in range(q) for d in range(q)]
    C = {}

    def visit(k, span):
        if k == len(cells):
            yield dict(C), span
            return
        cell = cells[k]
        j = cell[2]
        for u in range((N - 1 - span) // j + 1):
            if u:
                C[cell] = u
            else:
                C.pop(cell, None)
            yield from visit(k + 1, span + j * u)
        C.pop(cell, None)

    yield from visit(0, 0)


def reference_block(N, q):
    all_pools = list(pools(N, q))
    K = 1 + len(all_pools)
    assert len(all_pools) == sum(colored_partitions(N, q))
    law = defaultdict(F)
    law[(0,) * N] = F(1, K)
    unused_terminal_paths = 0

    def walk(C, events, probability):
        nonlocal unused_terminal_paths
        position, current = events[-1]
        outgoing = [(cell, u) for cell, u in C.items() if cell[0] == current]
        row_total = sum(u for _, u in outgoing)
        if not row_total:
            unused_terminal_paths += bool(C)
            symbols = [0] * N
            for at, mark in events:
                assert 1 <= at <= N
                symbols[at - 1] = mark + 1
            law[tuple(symbols)] += probability
            return
        for cell, u in outgoing:
            changed = dict(C)
            if u == 1:
                del changed[cell]
            else:
                changed[cell] = u - 1
            _, destination, gap = cell
            walk(changed, events + [(position + gap, destination)], probability * F(u, row_total))

    for C, S in all_pools:
        for anchor in range(1, N - S + 1):
            for start_mark in range(q):
                walk(C, [(anchor, start_mark)], F(1, q * K * (N - S)))
    assert sum(law.values()) == 1
    assert len(law) == (q + 1) ** N
    return dict(law), K, unused_terminal_paths


def prefix_stats(y, q):
    events = [(i + 1, mark - 1) for i, mark in enumerate(y) if mark]
    assert events
    c = defaultdict(int)
    row_uses = [0] * q
    for (a, origin), (b, destination) in zip(events, events[1:]):
        c[(origin, destination, b - a)] += 1
        row_uses[origin] += 1
    return events[0][0], events[-1][1], len(y) - events[-1][0], c, tuple(row_uses)


def falling(u, r):
    if r > u:
        return 0
    return factorial(u) // factorial(u - r)


@lru_cache(maxsize=None)
def integer_prefix(y, N, q):
    assert 0 <= len(y) <= N
    assert all(0 <= a <= q for a in y)
    parts = colored_partitions(N, q)
    K = 1 + sum(parts)
    fac = factorial(N)
    if not any(y):
        h = q * fac
        for S, count in enumerate(parts):
            allowed = max(0, N - S - len(y))
            assert fac % (N - S) == 0
            h += q * count * allowed * (fac // (N - S))
        return h
    anchor, last_mark, age, c, used = prefix_stats(y, q)
    cap = N - anchor
    table = {(0, (0,) * q): (1, 0)}
    for j in range(1, N):
        for origin in range(q):
            for destination in range(q):
                lower = c[(origin, destination, j)]
                new = defaultdict(lambda: [0, 0])
                for (S, totals), (A, B) in table.items():
                    for u in range(lower, (cap - S) // j + 1):
                        rows = list(totals)
                        rows[origin] += u
                        weight = falling(u, lower)
                        tail = u - lower if origin == last_mark and j > age else 0
                        key = (S + j * u, tuple(rows))
                        new[key][0] += weight * A
                        new[key][1] += weight * (B + tail * A)
                table = {key: tuple(value) for key, value in new.items()}
    h = 0
    for (S, totals), (A, B) in table.items():
        denom = N - S
        for R, r in zip(totals, used):
            denom *= falling(R, r)
        if totals[last_mark] == used[last_mark]:
            numerator = A
        else:
            denom *= totals[last_mark] - used[last_mark]
            numerator = B
        assert denom > 0 and fac % denom == 0
        h += numerator * (fac // denom)
    assert 0 < h <= q * K * fac
    return h


def true_block_probability(x, kernel, pi):
    q = len(kernel)
    N = len(x)
    means = [sum(gap * p for (gap, _), p in row.items()) for row in kernel]
    mean = sum(p * m for p, m in zip(pi, means))
    if not any(x):
        return sum(pi[i] * max(0, gap - N) * p
                   for i, row in enumerate(kernel) for (gap, _), p in row.items()) / mean
    events = [(i + 1, mark - 1) for i, mark in enumerate(x) if mark]
    anchor, first_mark = events[0]
    value = sum(pi[i] * p for i, row in enumerate(kernel)
                for (gap, destination), p in row.items()
                if gap >= anchor and destination == first_mark) / mean
    for (a, origin), (b, destination) in zip(events, events[1:]):
        value *= kernel[origin].get((b - a, destination), F(0))
    age = N - events[-1][0]
    value *= sum(p for (gap, _), p in kernel[events[-1][1]].items() if gap > age)
    return value


def fixtures(q):
    if q == 1:
        return [
            ([{(1, 0): F(1)}], [F(1)]),
            ([{(200, 0): F(1)}], [F(1)]),
            ([{(1, 0): F(1, 2), (4, 0): F(1, 2)}], [F(1)]),
        ]
    if q == 2:
        return [
            ([{(1, 1): F(1)}, {(1, 0): F(1)}], [F(1, 2), F(1, 2)]),
            ([{(5, 0): F(1)}, {(7, 1): F(1)}], [F(1, 3), F(2, 3)]),
            ([{(1, 0): F(1, 4), (3, 1): F(3, 4)},
              {(2, 0): F(1, 2), (5, 1): F(1, 2)}], [F(2, 5), F(3, 5)]),
            ([{(200, 1): F(1)}, {(1, 0): F(1, 1000), (200, 1): F(999, 1000)}],
             [F(1, 1001), F(1000, 1001)]),
        ]
    if q == 3:
        return [
            ([{(2, (i + 1) % 3): F(1)} for i in range(3)], [F(1, 3)] * 3),
            ([{(g, d): F(1, 6) for g in (1, 4) for d in range(3)} for _ in range(3)],
             [F(1, 3)] * 3),
        ]
    raise ValueError(q)


def main():
    start = time.perf_counter()
    checks = []
    for q, maximum in [(1, 8), (2, 6), (3, 4)]:
        for N in range(1, maximum + 1):
            law, K, unused = reference_block(N, q)
            scale = q * K * factorial(N)
            reference_prefix = defaultdict(F)
            for x, mass in law.items():
                for t in range(N + 1):
                    reference_prefix[x[:t]] += mass
            prefix_checks = normalizations = regrets = 0
            for t in range(N + 1):
                for y in product(range(q + 1), repeat=t):
                    h = integer_prefix(tuple(y), N, q)
                    assert F(h, scale) == reference_prefix[y]
                    prefix_checks += 1
                    if t < N:
                        assert h == sum(integer_prefix(y + (a,), N, q) for a in range(q + 1))
                        normalizations += 1
            for kernel, pi in fixtures(q):
                assert sum(pi) == 1
                assert all(sum(row.values()) == 1 for row in kernel)
                for d in range(q):
                    assert pi[d] == sum(pi[i] * p for i, row in enumerate(kernel)
                                        for (_, target), p in row.items() if target == d)
                total = F(0)
                for x, code_mass in law.items():
                    true_mass = true_block_probability(x, kernel, pi)
                    total += true_mass
                    assert true_mass <= q * K * N * code_mass
                    regrets += 1
                assert total == 1
            checks.append({
                "q": q, "N": N, "pool_options_plus_allzero": K,
                "prefix_equalities": prefix_checks, "normalizations": normalizations,
                "stationary_regret_checks": regrets, "unused_terminal_paths": unused,
                "scale_bits": scale.bit_length(),
            })
            print(json.dumps(checks[-1]), flush=True)
    assert any(c["unused_terminal_paths"] for c in checks if c["q"] > 1 and c["N"] > 1)
    result = {
        "status": "PASS", "arithmetic": "exact Fraction and integers",
        "cases": checks,
        "total_prefix_equalities": sum(c["prefix_equalities"] for c in checks),
        "total_normalizations": sum(c["normalizations"] for c in checks),
        "total_stationary_regret_checks": sum(c["stationary_regret_checks"] for c in checks),
        "elapsed_seconds": time.perf_counter() - start,
        "scope": "Independent finite diagnostic; not all-N proof, external validation, or priority evidence.",
    }
    (Path(__file__).with_name("CHECKS.json")).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "cases"}, indent=2))


if __name__ == "__main__":
    main()
