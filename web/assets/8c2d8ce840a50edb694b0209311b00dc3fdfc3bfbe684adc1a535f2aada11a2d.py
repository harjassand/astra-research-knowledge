#!/usr/bin/env python3
"""Finite exact check for sparse-plus-low-rank Schur/Grassmann transfer.

All arithmetic is Gaussian integer. The implementation is intentionally a
small width-order prototype for verification, not an optimized production DP.
"""

from itertools import combinations, permutations
import json
import random

GI = tuple[int, int]
ZERO: GI = (0, 0)
ONE: GI = (1, 0)
EP = dict  # exterior bitmask -> z-polynomial dict


def gadd(a: GI, b: GI) -> GI:
    return a[0] + b[0], a[1] + b[1]


def gneg(a: GI) -> GI:
    return -a[0], -a[1]


def gmul(a: GI, b: GI) -> GI:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gconj(a: GI) -> GI:
    return a[0], -a[1]


def ptrim(p: dict[int, GI]) -> dict[int, GI]:
    return {d: c for d, c in p.items() if c != ZERO}


def padd(a: dict[int, GI], b: dict[int, GI]) -> dict[int, GI]:
    out = dict(a)
    for d, c in b.items():
        out[d] = gadd(out.get(d, ZERO), c)
    return ptrim(out)


def pneg(a: dict[int, GI]) -> dict[int, GI]:
    return {d: gneg(c) for d, c in a.items()}


def pmul(a: dict[int, GI], b: dict[int, GI]) -> dict[int, GI]:
    out: dict[int, GI] = {}
    for da, ca in a.items():
        for db, cb in b.items():
            d = da + db
            out[d] = gadd(out.get(d, ZERO), gmul(ca, cb))
    return ptrim(out)


def pshift(a: dict[int, GI]) -> dict[int, GI]:
    return {d + 1: c for d, c in a.items()}


def ext_sign(a: int, b: int) -> int:
    inv = 0
    bits = a
    while bits:
        low = bits & -bits
        inv += (b & (low - 1)).bit_count()
        bits ^= low
    return -1 if inv & 1 else 1


def ep_add(a: EP, b: EP) -> EP:
    out = {m: dict(p) for m, p in a.items()}
    for m, p in b.items():
        out[m] = padd(out.get(m, {}), p)
        if not out[m]:
            del out[m]
    return out


def ep_mul(a: EP, b: EP) -> EP:
    out: EP = {}
    for ma, pa in a.items():
        for mb, pb in b.items():
            if ma & mb:
                continue
            p = pmul(pa, pb)
            if ext_sign(ma, mb) < 0:
                p = pneg(p)
            m = ma | mb
            out[m] = padd(out.get(m, {}), p)
            if not out[m]:
                del out[m]
    return out


def linear_edge(a: int, b: int, c: GI) -> EP:
    if c == ZERO:
        return {0: {0: ONE}}
    if a > b:
        c = gneg(c)
    return {0: {0: ONE}, (1 << a) | (1 << b): {0: c}}


def matrix_edge(i: int, j: int, value: GI) -> EP:
    # Two determinant replicas, with the second amplitude conjugated.
    e1 = linear_edge(4 * i, 4 * j + 1, value)
    e2 = linear_edge(4 * i + 2, 4 * j + 3, gconj(value))
    return ep_mul(e1, e2)


def contract_site(poly: EP, site: int, kind: str) -> EP:
    row = (1 << (4 * site)) | (1 << (4 * site + 2))
    col = (1 << (4 * site + 1)) | (1 << (4 * site + 3))
    local_mask = 15 << (4 * site)
    out: EP = {}
    for mask, p in poly.items():
        local = mask & local_mask
        if kind == "physical":
            if local == 0 or local == col:
                q = p
            elif local == row:
                q = pneg(pshift(p))  # row selected: z and replica-order sign
            else:  # both selected or an unmatched replica state
                continue
        elif kind == "auxiliary":
            if local != row | col:
                continue
            q = p  # both selected; the row/column Koszul signs cancel
        else:
            raise ValueError(kind)
        reduced = mask ^ local
        out[reduced] = padd(out.get(reduced, {}), q)
        if not out[reduced]:
            del out[reduced]
    return out


def exact_augmented_elimination(m: list[list[GI]], n_physical: int,
                                order: list[int]) -> list[GI]:
    N = len(m)
    factors: list[tuple[frozenset[int], EP]] = []
    for i in range(N):
        for j in range(N):
            if m[i][j] != ZERO:
                factors.append((frozenset((i, j)), matrix_edge(i, j, m[i][j])))

    for site in order:
        touched = [(scope, p) for scope, p in factors if site in scope]
        factors = [(scope, p) for scope, p in factors if site not in scope]
        scope: set[int] = set()
        merged: EP = {0: {0: ONE}}
        for sc, p in touched:
            scope.update(sc)
            merged = ep_mul(merged, p)
        kind = "physical" if site < n_physical else "auxiliary"
        message = contract_site(merged, site, kind)
        scope.discard(site)
        factors.append((frozenset(scope), message))

    final: EP = {0: {0: ONE}}
    for scope, p in factors:
        if scope:
            raise ValueError("order did not eliminate all sites")
        final = ep_mul(final, p)
    result = final.get(0, {})
    assert all(c[1] == 0 for c in result.values()), result
    return [result.get(k, ZERO) for k in range(n_physical + 1)]


def chiral_edge(i: int, j: int, value: GI) -> EP:
    # Exterior realization of the chiral determinant block
    # [[X,M],[-M*,Y]]. The minus sign is on the conjugate transposed edge.
    e1 = linear_edge(4 * i, 4 * j + 3, value)
    e2 = linear_edge(4 * j + 2, 4 * i + 1, gneg(gconj(value)))
    return ep_mul(e1, e2)


def exact_chiral_elimination(m: list[list[GI]], n_physical: int,
                              order: list[int]) -> list[GI]:
    """Independent determinant-polynomial/Grassmann implementation."""
    N = len(m)
    factors: list[tuple[frozenset[int], EP]] = []
    for i in range(N):
        A = (1 << (4 * i)) | (1 << (4 * i + 1))
        B = (1 << (4 * i + 2)) | (1 << (4 * i + 3))
        if i < n_physical:
            local: EP = {A: {0: ONE}, B: {1: ONE}, A | B: {0: ONE}}
        else:
            local = {0: {0: ONE}}  # force both auxiliary indices selected
        factors.append((frozenset((i,)), local))
    for i in range(N):
        for j in range(N):
            if m[i][j] != ZERO:
                factors.append((frozenset((i, j)), chiral_edge(i, j, m[i][j])))

    for site in order:
        touched = [(scope, p) for scope, p in factors if site in scope]
        factors = [(scope, p) for scope, p in factors if site not in scope]
        scope: set[int] = set()
        merged: EP = {0: {0: ONE}}
        for sc, p in touched:
            scope.update(sc)
            merged = ep_mul(merged, p)
        local_mask = 15 << (4 * site)
        message: EP = {}
        for mask, p in merged.items():
            if mask & local_mask == local_mask:
                reduced = mask ^ local_mask
                message[reduced] = padd(message.get(reduced, {}), p)
                if not message[reduced]:
                    del message[reduced]
        scope.discard(site)
        factors.append((frozenset(scope), message))

    final: EP = {0: {0: ONE}}
    for scope, p in factors:
        if scope:
            raise ValueError("order did not eliminate all sites")
        final = ep_mul(final, p)
    result = final.get(0, {})
    assert all(c[1] == 0 for c in result.values()), result
    return [result.get(k, ZERO) for k in range(n_physical + 1)]


def det(a: list[list[GI]]) -> GI:
    n = len(a)
    total = ZERO
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = ONE
        for i, j in enumerate(p):
            term = gmul(term, a[i][j])
        total = gadd(total, gneg(term) if inv & 1 else term)
    return total


def minor(a: list[list[GI]], rows: tuple[int, ...], cols: tuple[int, ...]) -> list[list[GI]]:
    return [[a[i][j] for j in cols] for i in rows]


def direct_coefficients(f: list[list[GI]]) -> list[int]:
    n = len(f)
    out = [0] * (n + 1)
    for k in range(n + 1):
        for I in combinations(range(n), k):
            for J in combinations(range(n), k):
                if set(I) & set(J):
                    continue
                d = det(minor(f, I, J))
                out[k] += d[0] * d[0] + d[1] * d[1]
    return out


def elimination_width(a: list[list[GI]], order: list[int]) -> int:
    """Exact induced width of an order on an undirected site-support graph."""
    n = len(a)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i):
            if a[i][j] != ZERO or a[j][i] != ZERO:
                adj[i].add(j)
                adj[j].add(i)
    live = set(range(n))
    width = 0
    for v in order:
        ns = adj[v] & live
        width = max(width, len(ns))
        for x, y in combinations(ns, 2):
            adj[x].add(y)
            adj[y].add(x)
        live.remove(v)
    return width


def make_case(rng: random.Random, n: int, r: int) -> tuple[list[list[GI]], list[list[GI]]]:
    s = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        s[i][i] = (rng.randrange(-1, 2), rng.randrange(-1, 2))
        if i + 1 < n:
            s[i][i + 1] = (rng.randrange(-2, 3), rng.randrange(-2, 3))
            s[i + 1][i] = (rng.randrange(-2, 3), rng.randrange(-2, 3))
    u = [[(rng.randrange(-2, 3), rng.randrange(-1, 2)) for _ in range(r)] for _ in range(n)]
    v = [[(rng.randrange(-2, 3), rng.randrange(-1, 2)) for _ in range(r)] for _ in range(n)]
    uv = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for ell in range(r):
                uv[i][j] = gadd(uv[i][j], gmul(u[i][ell], v[j][ell]))
    f = [[gadd(s[i][j], uv[i][j]) for j in range(n)] for i in range(n)]

    # Schur matrix [[S,U],[-V^T,I]].
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
    return f, m


def main() -> None:
    rng = random.Random(911207)
    cases = [(2, 0), (3, 1), (4, 1), (4, 2), (5, 1), (5, 2)]
    results = []
    for case_id, (n, r) in enumerate(cases):
        f, m = make_case(rng, n, r)
        # Sparse base is a path; eliminate physical sites then auxiliary sites.
        order = list(range(n + r))
        got_g = exact_augmented_elimination(m, n, order)
        got = [c[0] for c in got_g]
        got_chiral_g = exact_chiral_elimination(m, n, order)
        got_chiral = [c[0] for c in got_chiral_g]
        want = direct_coefficients(f)
        assert got == want, (case_id, n, r, got, want)
        assert got_chiral == want, (case_id, n, r, got_chiral, want)
        base_width = elimination_width([row[:n] for row in m[:n]], list(range(n)))
        augmented_width = elimination_width(m, order)
        assert augmented_width <= base_width + r
        results.append({"n": n, "rank_bound": r, "base_order_width": base_width,
                        "augmented_order_width": augmented_width,
                        "coefficients": want, "elimination_order": order})
    print(json.dumps({
        "status": "PASS",
        "seed": 911207,
        "cases": results,
        "scope": "Exact Gaussian-integer checks of Schur augmentation by both same-orientation pairing contraction and chiral-determinant Grassmann elimination, including forced-both auxiliary sites and diagonal identity edges.",
        "not_established": ["general treewidth DP complexity by implementation", "discovery of sparse-plus-low-rank decomposition", "FPRAS or sampler", "novelty"]
    }, indent=2))


if __name__ == "__main__":
    main()
