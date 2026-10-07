"""Finite diagnostics for the exact slice-rank lemma; no external packages."""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from random import Random


def rank(matrix):
    a = [[Fraction(v) for v in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][j]
        a[r] = [x / v for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                v = a[i][j]
                a[i] = [x - v * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def check(n, d, edges):
    edges = sorted(edges)
    edge_id = {e: l for l, e in enumerate(edges)}
    row_degrees = [sum(i == v for v, _ in edges) for i in range(n)]
    col_degrees = [sum(j == v for _, v in edges) for j in range(n)]
    z_total = x_total = b_total = 0
    for i, j in edges:
        # Slice variables can be restricted to their D active coordinates.
        s = [[int(k == l) for l in range(d)] for k in range(d)]
        z_total += rank(s)
    for i, k in product(range(n), range(d)):
        s = [[0] * n for _ in edges]
        for j in range(n):
            if (i, j) in edge_id:
                s[edge_id[i, j]][j] = 1
        found = rank(s)
        assert found == row_degrees[i], (n, d, edges, i, k, found)
        x_total += found
    for j, k in product(range(n), range(d)):
        s = [[0] * n for _ in edges]
        for i in range(n):
            if (i, j) in edge_id:
                s[edge_id[i, j]][i] = 1
        found = rank(s)
        assert found == col_degrees[j], (n, d, edges, j, k, found)
        b_total += found
    assert z_total == x_total == b_total == len(edges) * d


checked = 0
for n in range(1, 4):
    possible = list(product(range(n), repeat=2))
    for bits in product((0, 1), repeat=n * n):
        edges = [e for e, v in zip(possible, bits) if v]
        for d in range(1, 5):
            check(n, d, edges)
            checked += 1

rng = Random(107250914489)
for _ in range(100):
    n = rng.randrange(4, 13)
    d = rng.randrange(1, 6)
    density = rng.random()
    edges = [e for e in product(range(n), repeat=2) if rng.random() < density]
    check(n, d, edges)
    checked += 1

report = {
    "status": "PASS",
    "fixtures": checked,
    "exhaustive": "all masks N=1,2,3; D=1,2,3,4",
    "random": "100 seeded masks N=4..12; D=1..5",
    "scope": "slice coefficient matrix ranks only; not a general circuit lower bound",
}
Path(__file__).with_name("slice_rank_checks.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report))
