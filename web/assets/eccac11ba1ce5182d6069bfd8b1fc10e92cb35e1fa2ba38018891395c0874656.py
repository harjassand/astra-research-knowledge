#!/usr/bin/env python3
"""Exact small diagnostics for the rank-one-coupled block coefficient formula."""
from itertools import combinations, permutations
import json
from pathlib import Path


def det(A):
    n = len(A)
    if n == 0:
        return 1
    total = 0
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = -1 if inv % 2 else 1
        for i, j in enumerate(p):
            term *= A[i][j]
        total += term
    return total


def mat(A, I, J):
    return [[A[i][j] for j in J] for i in I]


def local_moments(A, u, v):
    n = len(A)
    out = {"A": [], "B": [], "C": [], "U": [], "V": []}
    for ell in range(n // 2 + 1):
        aa = bb = cc = 0
        for I in combinations(range(n), ell):
            setI = set(I)
            for J in combinations([j for j in range(n) if j not in setI], ell):
                M = mat(A, I, J)
                d = det(M)
                delta = 0
                for p in range(ell):
                    for q in range(ell):
                        minor = [row[:q] + row[q + 1:] for r, row in enumerate(M) if r != p]
                        cofactor = (-1 if (p + q) % 2 else 1) * det(minor)
                        delta += v[J[q]] * cofactor * u[I[p]]
                aa += d * d
                bb += d * delta
                cc += delta * delta
        out["A"].append(aa)
        out["B"].append(bb)
        out["C"].append(cc)

    maxell = (n - 1) // 2
    for ell in range(maxell + 1):
        us = 0
        for I in combinations(range(n), ell + 1):
            setI = set(I)
            for J in combinations([j for j in range(n) if j not in setI], ell):
                M = mat(A, I, J)
                eta = 0
                for p in range(ell + 1):
                    minor = [row[:] for r, row in enumerate(M) if r != p]
                    eta += (-1 if p % 2 else 1) * u[I[p]] * det(minor)
                us += eta * eta
        out["U"].append(us)

        vs = 0
        for I in combinations(range(n), ell):
            setI = set(I)
            for J in combinations([j for j in range(n) if j not in setI], ell + 1):
                M = mat(A, I, J)
                theta = 0
                for q in range(ell + 1):
                    minor = [row[:q] + row[q + 1:] for row in M]
                    theta += (-1 if q % 2 else 1) * v[J[q]] * det(minor)
                vs += theta * theta
        out["V"].append(vs)
    return out


def add(a, b, cap):
    z = [0] * (cap + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j <= cap:
                z[i + j] += x * y
    return z


def sum_poly(a, b, cap):
    z = [0] * (cap + 1)
    for i in range(min(len(a), cap + 1)):
        z[i] += a[i]
    for i in range(min(len(b), cap + 1)):
        z[i] += b[i]
    return z


def product_all(polys, cap, omit=()):
    p = [1]
    for t, x in enumerate(polys):
        if t not in omit:
            p = add(p, x, cap)
    return p


def formula(blocks, u, v, k):
    stats = [local_moments(A, u[o:o+len(A)], v[o:o+len(A)])
             for o, A in offsets(blocks)]
    cap = k
    # Moment recurrences for G0=product d and G1=sum delta_t product_{s!=t} d_s.
    p0, p1, p2 = [1], [0], [0]
    for s in stats:
        a, b, c = s["A"], s["B"], s["C"]
        p0_new = add(p0, a, cap)
        p1_new = sum_poly(add(p1, a, cap), add(p0, b, cap), cap)
        p2_new = sum_poly(sum_poly(add(p2, a, cap), add(p0, c, cap), cap),
                          [2*x for x in add(p1, b, cap)], cap)
        p0, p1, p2 = p0_new, p1_new, p2_new
    balanced = p0[k] + 2*p1[k] + p2[k]

    A_polys = [s["A"] for s in stats]
    mismatch = 0
    for a in range(len(stats)):
        for b in range(len(stats)):
            if a == b or k == 0:
                continue
            prod = [1]
            for t, s in enumerate(stats):
                if t == a:
                    local = s["U"]
                elif t == b:
                    local = s["V"]
                else:
                    local = s["A"]
                prod = add(prod, local, max(0, k-1))
            if k - 1 < len(prod):
                mismatch += prod[k-1]
    return balanced + mismatch, balanced, mismatch


def offsets(blocks):
    cur = 0
    for A in blocks:
        yield cur, A
        cur += len(A)


def block_diag(blocks):
    n = sum(len(A) for A in blocks)
    out = [[0] * n for _ in range(n)]
    off = 0
    for A in blocks:
        b = len(A)
        for i in range(b):
            for j in range(b):
                out[off+i][off+j] = A[i][j]
        off += b
    return out


def brute(F, k):
    n = len(F)
    total = 0
    for I in combinations(range(n), k):
        si = set(I)
        for J in combinations([j for j in range(n) if j not in si], k):
            d = det(mat(F, I, J))
            total += d*d
    return total


def main():
    cases = [
        ([[[0, 1], [2, -1]], [[1, 1], [0, 2]]], [1, -1, 2, 1], [0, 1, -1, 2]),
        ([[[1, 0], [1, 1]], [[0, 1], [1, -1]]], [1, 0, 1, -1], [2, -1, 0, 1]),
        ([[[0, 1], [1, 0]], [[1, 2], [-1, 1]], [[1, 0], [1, 1]]], [1, -1, 0, 1, 2, -1], [0, 1, -1, 1, 0, 2]),
    ]
    out = []
    for blocks, u, v in cases:
        A = block_diag(blocks)
        F = [[A[i][j] + u[i] * v[j] for j in range(len(A))] for i in range(len(A))]
        ks = range(len(F)//2 + 1)
        for k in ks:
            got, bal, mis = formula(blocks, u, v, k)
            want = brute(F, k)
            assert got == want, (len(F), k, got, want, bal, mis)
            out.append({"n": len(F), "k": k, "coefficient": got, "balanced": bal, "one_defect_pair": mis})
    result = {"status": "PASS exact integer fixtures", "cases": out,
              "scope": "Finite formula diagnostics only; universal derivation belongs in rank_one_block.txt; no external validation or priority claim."}
    Path(__file__).with_name("rank_one_block_check.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
