"""Exact Q(omega) verification of the global binary kernel-sector coupling."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


ROOTS = ((F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(-1), F(-1)))


def rref(A):
    B = [[F(x) for x in row] for row in A]
    w, m = len(B), len(B[0])
    pivot_cols, r = [], 0
    for c in range(m):
        pivot = next((i for i in range(r, w) if B[i][c]), None)
        if pivot is None:
            continue
        B[r], B[pivot] = B[pivot], B[r]
        scale = B[r][c]
        B[r] = [x / scale for x in B[r]]
        for i in range(w):
            if i != r and B[i][c]:
                scale = B[i][c]
                B[i] = [x - scale*y for x, y in zip(B[i], B[r])]
        pivot_cols.append(c)
        r += 1
        if r == w:
            break
    return B, pivot_cols


def sector(z):
    a, b = z
    if not a and not b:
        return 0
    scores = (2*a-b, 2*b-a, -a-b)
    maximum = max(scores)
    assert maximum > 0
    return scores.index(maximum) + 1


def type_vectors(A):
    B, pivots = rref(A)
    m = len(A[0])
    free = [j for j in range(m) if j not in pivots]
    seen = set()
    for choices in product(range(4), repeat=len(free)):
        z = [ROOTS[0] for _ in range(m)]
        for j, choice in zip(free, choices):
            z[j] = ROOTS[choice]
        for i, j in enumerate(pivots):
            z[j] = tuple(-sum(B[i][k]*z[k][a] for k in free) for a in (0, 1))
        for row in A:
            assert all(sum(F(x)*zj[a] for x, zj in zip(row, z)) == 0 for a in (0, 1))
        types = tuple(map(sector, z))
        assert all(types[j] == choice for j, choice in zip(free, choices))
        assert types not in seen
        seen.add(types)
        for row in A:
            colors = {t for x, t in zip(row, types) if x and t}
            assert len(colors) != 1
        # Verify every base choice and every observed subtuple directly.
        for base in product(range(2), repeat=m):
            triple = [tuple(bit ^ (t == replica+1) for bit, t in zip(base, types))
                      for replica in range(3)]
            for row in A:
                observed = [tuple(bit for bit, include in zip(copy, row) if include)
                            for copy in triple]
                assert len(set(observed)) != 2
    return {"matrix": A, "rank": len(pivots), "free": len(free),
            "type_vectors": len(seen), "uniform_likelihood_ratio": 4**len(pivots)}


cases = [
    [[1,1,0], [0,1,1]],
    [[1,1,1,1]],
    [[1,1,1,1], [1,1,1,1], [1,1,1,1]],
    [[1,1,0], [1,0,1], [0,1,1]],
    [[1,0,1,0,1], [0,1,1,0,0], [0,0,0,1,1]],
    [[1,0,0,0], [0,1,0,0]],
]
result = {"cases": [type_vectors(A) for A in cases]}
Path(__file__).with_name("kernel_sector_verification.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
