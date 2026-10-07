#!/usr/bin/env python3
"""Broader small exact checks on non-path sparse bases.

Uses the independent original-minor enumerator and both Grassmann contractions
from augmented_grassmann_dp.py. This is a finite algebra check, not a generic
treewidth-DP proof or performance benchmark.
"""

import json
import random

from augmented_grassmann_dp import (
    ZERO, ONE, gadd, gmul, make_case, direct_coefficients,
    exact_augmented_elimination, exact_chiral_elimination, elimination_width,
)


def case_from_edges(rng, n, r, edges):
    s = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        s[i][i] = (rng.randrange(-1, 2), rng.randrange(-1, 2))
    for i, j in edges:
        s[i][j] = (rng.randrange(-2, 3), rng.randrange(-1, 2))
        s[j][i] = (rng.randrange(-2, 3), rng.randrange(-1, 2))
    u = [[(rng.randrange(-2, 3), rng.randrange(-1, 2)) for _ in range(r)]
         for _ in range(n)]
    v = [[(rng.randrange(-2, 3), rng.randrange(-1, 2)) for _ in range(r)]
         for _ in range(n)]
    uv = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for ell in range(r):
                uv[i][j] = gadd(uv[i][j], gmul(u[i][ell], v[j][ell]))
    f = [[gadd(s[i][j], uv[i][j]) for j in range(n)] for i in range(n)]

    m = [[ZERO for _ in range(n + r)] for _ in range(n + r)]
    for i in range(n):
        for j in range(n):
            m[i][j] = s[i][j]
        for ell in range(r):
            m[i][n + ell] = u[i][ell]
    for ell in range(r):
        for j in range(n):
            m[n + ell][j] = (-v[j][ell][0], -v[j][ell][1])
        m[n + ell][n + ell] = ONE
    return f, m, s


def main():
    rng = random.Random(710305)
    n = 6
    supports = {
        "star": {(0, i) for i in range(1, n)},
        "cycle": {(i, (i + 1) % n) for i in range(n)},
        "2x3_grid": {(0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (1, 4), (2, 5)},
        "K2_4": {(i, j) for i in (0, 1) for j in (2, 3, 4, 5)},
    }
    orders = {
        "star": list(range(1, n)) + [0],
        "cycle": list(range(n)),
        "2x3_grid": list(range(n)),
        "K2_4": [2, 3, 4, 5, 0, 1],
    }
    rows = []
    for name, edges in supports.items():
        base_order = orders[name]
        for r in (0, 1, 2):
            f, m, s = case_from_edges(rng, n, r, edges)
            order = base_order + list(range(n, n + r))
            base_w = elimination_width(s, base_order)
            aug_w = elimination_width(m, order)
            got1 = [x[0] for x in exact_augmented_elimination(m, n, order)]
            got2 = [x[0] for x in exact_chiral_elimination(m, n, order)]
            want = direct_coefficients(f)
            assert got1 == want, (name, r, "paired", got1, want)
            assert got2 == want, (name, r, "chiral", got2, want)
            assert aug_w <= base_w + r, (name, r, base_w, aug_w)
            rows.append({"base": name, "n": n, "rank_bound": r,
                         "base_order_width": base_w,
                         "augmented_order_width": aug_w,
                         "coefficients": want})
    print(json.dumps({"status": "PASS", "seed": 710305, "cases": rows,
                      "scope": "Twelve exact Gaussian-integer comparisons on star, cycle, 2x3-grid, and K2,4 sparse bases; both contractions match direct original-minor enumeration.",
                      "not_established": ["generic theorem proof by experiment", "treewidth recognition", "decomposition discovery", "runtime scaling", "sampler", "novelty"]}, indent=2))


if __name__ == "__main__":
    main()
