#!/usr/bin/env python3
"""Four-action exact decoder for P_n^2; X=Z/sqrt(2), integer period-six Z.

decode_scaled(W) expects W=sqrt(2)*Y. Thus input noise E0 in W has actual
normalized action noise squared ||E0||F^2/2. No floating approximation of
sqrt(2) is used in the exact tests. Standard library only.
"""
from fractions import Fraction as F
from functools import lru_cache


def sign(i):
    return 1 if (i // 3) % 2 == 0 else -1


def seed_integer(n):
    return [tuple(int(i % 3 == c) for c in range(3)) + (sign(i),)
            for i in range(n)]


def neighborhood(n, i):
    return range(max(0, i - 2), min(n, i + 3))


def edges(n):
    return [(i, j) for i in range(n) for j in range(i + 1, min(n, i + 3))]


def transpose(A):
    return list(map(list, zip(*A)))


def mul(A, B):
    Bt = transpose(B)
    return [[sum(x*y for x, y in zip(row, col)) for col in Bt] for row in A]


def inv(A):
    n = len(A)
    W = [[F(x) for x in A[i]] + [F(i == j) for j in range(n)] for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j, n) if W[i][j])
        W[j], W[p] = W[p], W[j]
        v = W[j][j]
        W[j] = [x/v for x in W[j]]
        for i in range(n):
            if i != j:
                v = W[i][j]
                W[i] = [a-v*b for a, b in zip(W[i], W[j])]
    return [r[n:] for r in W]


@lru_cache(None)
def local_map(rows):
    M = [list(row) for row in rows]
    Mt = transpose(M)
    if len(M) <= 4:
        return mul(Mt, inv(mul(M, Mt)))
    return mul(inv(mul(Mt, M)), Mt)


def kernel(i, j):
    b = -sign(i-2)*sign(i-1)
    return {i-2:F(1, 2), i-1:F(b, 2), i:F(0),
            i+1:F(-1, 2), i+2:F(-b, 2)}.get(j, F(0))


def scalar_rows(n):
    high = set(range(2, n-2))
    rows = []
    for i, j in edges(n):
        row = {}
        if i in high and kernel(i, j):
            row[i-2] = kernel(i, j)
        if j in high and kernel(j, i):
            row[j-2] = -kernel(j, i)
        if row:
            rows.append((i, j, row))
    return rows


def band_ldl(A, rhs):
    """Exact symmetric bandwidth-two solve; A stores upper triangle."""
    n = len(rhs)
    L, d = {}, []
    for i in range(n):
        for j in range(max(0, i-2), i):
            val = A.get((j, i), F(0))
            for k in range(max(0, i-2, j-2), j):
                val -= L.get((i, k), F(0))*d[k]*L.get((j, k), F(0))
            L[i, j] = val/d[j]
        di = A.get((i, i), F(0))
        for k in range(max(0, i-2), i):
            di -= L[i, k]**2*d[k]
        assert di >= F(7, 16)
        d.append(di)
    y = []
    for i in range(n):
        y.append(rhs[i] - sum(L[i, k]*y[k] for k in range(max(0, i-2), i)))
    z = [y[i]/d[i] for i in range(n)]
    ans = [F(0)]*n
    for i in reversed(range(n)):
        ans[i] = z[i] - sum(L[j, i]*ans[j] for j in range(i+1, min(n, i+3)))
    return ans, min(d) if d else None


def decode_scaled(W):
    """Return upper-triangle supported coefficients, with exact scalars."""
    n = len(W)
    if any(len(row) != 4 for row in W):
        raise ValueError('Expected four action columns')
    Z = seed_integer(n)
    R = []
    for i in range(n):
        ns = list(neighborhood(n, i))
        C = local_map(tuple(Z[j] for j in ns))
        R.append({j:sum(W[i][c]*C[c][k] for c in range(4))
                  for k, j in enumerate(ns)})
    m = max(0, n-4)
    A, rhs = {}, [F(0)]*m
    for i, j, row in scalar_rows(n):
        b = R[j][i] - R[i][j]
        for p, a in row.items():
            rhs[p] += a*b
            for q, c in row.items():
                if p <= q:
                    A[p, q] = A.get((p, q), F(0)) + a*c
    t, pivot_min = band_ldl(A, rhs)
    for i in range(2, n-2):
        for j in neighborhood(n, i):
            R[i][j] += t[i-2]*kernel(i, j)
    result = {(i, i):R[i][i] for i in range(n)}
    result.update({(i, j):(R[i][j]+R[j][i])/2 for i, j in edges(n)})
    return result, {'scalar_unknowns':m, 'minimum_ldl_pivot':str(pivot_min)}


def action_scaled(n, D):
    Z = seed_integer(n)
    W = [[F(0)]*4 for _ in range(n)]
    for (i, j), a in D.items():
        for c in range(4):
            W[i][c] += a*Z[j][c]
            if i != j:
                W[j][c] += a*Z[i][c]
    return W


def norm_squared(D):
    return sum((1 if i == j else 2)*a*a for (i, j), a in D.items())
