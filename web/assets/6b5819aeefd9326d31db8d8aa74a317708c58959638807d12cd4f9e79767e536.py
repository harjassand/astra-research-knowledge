#!/usr/bin/env python3
"""Exact finite checks of support and bounded-multiplicity reductions; no FPRAS."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
import random


def hafnian_table(B):
    n = len(B)

    @lru_cache(None)
    def h(mask):
        if mask == 0:
            return 1
        if mask.bit_count() % 2:
            return 0
        low = mask & -mask
        i = low.bit_length() - 1
        rest = mask ^ low
        return sum(B[i][j] * h(rest ^ (1 << j))
                   for j in range(i + 1, n) if rest & (1 << j))

    return h


def cycle_rank(B):
    n = len(B)
    edges = sum(B[i][j] != 0 for i in range(n) for j in range(i + 1, n))
    unseen = set(range(n))
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            i = stack.pop()
            for j in list(unseen):
                if B[i][j]:
                    unseen.remove(j)
                    stack.append(j)
    return edges - n + components


def dummy_matrix(B, q, required):
    n = len(B)
    ndummy = n - q
    A = [row + [0] * ndummy for row in B]
    A.extend([[0] * (n + ndummy) for _ in range(ndummy)])
    for d in range(n, n + ndummy):
        for i in range(n):
            if i not in required:
                A[d][i] = A[i][d] = 1
    return A


def run():
    summary = {"unweighted_graphs": 0, "induced_multiplicity_checks": 0,
               "weighted_instances": 0, "pinned_dummy_checks": 0,
               "status": "PASS", "scope": "finite exact diagnostics, not FPRAS implementation"}
    # Exhaustive small support graphs: matching multiplicity injects into cycle space.
    for n in (4, 5, 6):
        E = list(combinations(range(n), 2))
        for edge_mask in range(1 << len(E)):
            B = [[0] * n for _ in range(n)]
            for j, (u, v) in enumerate(E):
                if edge_mask & (1 << j):
                    B[u][v] = B[v][u] = 1
            h = hafnian_table(B)
            R = 1 << cycle_rank(B)
            for mask in range(1 << n):
                if mask.bit_count() % 2 == 0:
                    assert h(mask) <= R
                    summary["induced_multiplicity_checks"] += 1
            summary["unweighted_graphs"] += 1

    rng = random.Random(20261007)
    for _ in range(250):
        n = 6
        B = [[0] * n for _ in range(n)]
        for u, v in combinations(range(n), 2):
            B[u][v] = B[v][u] = rng.choice((0, 0, 1, 2, 5, 9))
        h = hafnian_table(B)
        d = hafnian_table([[v * v for v in row] for row in B])
        r = hafnian_table([[int(v != 0) for v in row] for row in B])
        for mask in range(1 << n):
            if mask.bit_count() % 2 == 0:
                assert d(mask) <= h(mask) ** 2 <= r(mask) * d(mask)
        # Include/exclude pins are varied before the dummy construction.
        forbidden = {i for i in range(n) if rng.randrange(4) == 0}
        allowed = [i for i in range(n) if i not in forbidden]
        C = [[B[u][v] for v in allowed] for u in allowed]
        N = len(C)
        ch = hafnian_table(C)
        cd = hafnian_table([[v * v for v in row] for row in C])
        required = {i for i in range(N) if rng.randrange(3) == 0}
        H = sum(1 << i for i in required)
        for q in range(0, N + 1, 2):
            masks = [m for m in range(1 << N) if m.bit_count() == q and m & H == H]
            target = sum(ch(m) ** 2 for m in masks)
            single = sum(ch(m) for m in masks)
            squared_edge = sum(cd(m) for m in masks)
            A = dummy_matrix(C, q, required)
            pm = hafnian_table(A)((1 << len(A)) - 1)
            A2 = dummy_matrix([[v * v for v in row] for row in C], q, required)
            pm2 = hafnian_table(A2)((1 << len(A2)) - 1)
            factor = 1
            for j in range(1, N - q + 1):
                factor *= j
            assert pm == factor * single
            assert pm2 == factor * squared_edge
            assert (target > 0) == (pm > 0)
            # Rejection unnormalized output mass is exactly desired h_S^2/R.
            R = 1 << cycle_rank(C)
            for m in masks:
                if cd(m):
                    assert cd(m) <= ch(m) ** 2 <= R * cd(m)
            summary["pinned_dummy_checks"] += 1
        summary["weighted_instances"] += 1
    path = Path(__file__).with_name("verification_results.json")
    path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run()
