#!/usr/bin/env python3
"""Exact small checks for the zero-Hessian-rank permanent audit.

This is finite arithmetic evidence, not a proof of the uniform formulas in
RESULT.txt. All ranks below are computed over Q by exact Gaussian elimination.
"""
from fractions import Fraction as Q
import json


def permanent(a):
    n = len(a)
    if n == 0:
        return Q(1)
    dp = [Q(0)] * (1 << n)
    dp[0] = Q(1)
    for mask in range(1 << n):
        i = mask.bit_count()
        if i == n or not dp[mask]:
            continue
        for j in range(n):
            if not (mask >> j) & 1:
                dp[mask | (1 << j)] += dp[mask] * a[i][j]
    return dp[-1]


def exact_rank(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        z = a[rank][col]
        a[rank] = [x / z for x in a[rank]]
        for i in range(rows):
            if i != rank and a[i][col]:
                z = a[i][col]
                a[i] = [x - z * y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def permanent_hessian_at(a):
    n = len(a)
    h = [[Q(0) for _ in range(n * n)] for _ in range(n * n)]
    for i in range(n):
        for j in range(n):
            u = i * n + j
            for k in range(n):
                for ell in range(n):
                    v = k * n + ell
                    if i == k or j == ell:
                        continue
                    rows = [x for x in range(n) if x not in (i, k)]
                    cols = [x for x in range(n) if x not in (j, ell)]
                    minor = [[a[x][y] for y in cols] for x in rows]
                    h[u][v] = permanent(minor)
    return h


def det_hessian_at_identity_rank(r):
    # D^2 det(I)[E_ij,E_kl] = tr(E_ij)tr(E_kl)-tr(E_ij E_kl).
    h = [[0] * (r * r) for _ in range(r * r)]
    for i in range(r):
        for j in range(r):
            u = i * r + j
            for k in range(r):
                for ell in range(r):
                    v = k * r + ell
                    h[u][v] = int(i == j and k == ell) - int(j == k and i == ell)
    return exact_rank(h)


def det_zero_hessian_rank_r_minus_1(r):
    # Hessian of the quadratic Taylor term z_rr*sum_{i<r}z_ii-
    # sum_{i<r}z_ir*z_ri at diag(I_{r-1},0).
    h = [[0] * (r * r) for _ in range(r * r)]
    last = (r - 1) * r + (r - 1)
    for i in range(r - 1):
        diagonal = i * r + i
        h[last][diagonal] = h[diagonal][last] = 1
        upper = i * r + (r - 1)
        lower = (r - 1) * r + i
        h[upper][lower] = h[lower][upper] = -1
    return exact_rank(h)


def det_zero_hessian_rank_r_minus_2(r):
    # The quadratic Taylor term is the determinant on the bottom 2x2 block.
    h = [[0] * (r * r) for _ in range(r * r)]
    i, j = r - 2, r - 1
    a, b, c, d = i * r + i, i * r + j, j * r + i, j * r + j
    h[a][d] = h[d][a] = 1
    h[b][c] = h[c][b] = -1
    return exact_rank(h)


def main():
    permanent_cases = []
    for n in range(2, 9):
        a = [[Q(1) for _ in range(n)] for _ in range(n)]
        a[0][n - 1] = -(n - 1)
        h = permanent_hessian_at(a)
        permanent_cases.append({
            "order": n,
            "witness_permanent": str(permanent(a)),
            "hessian_rank_over_Q": exact_rank(h),
            "variable_count": n * n,
            "full_rank": exact_rank(h) == n * n,
        })

    determinant_cases = []
    for r in range(2, 9):
        rank_at_corank_one = det_zero_hessian_rank_r_minus_1(r)
        rank_at_corank_two = det_zero_hessian_rank_r_minus_2(r)
        rank_at_identity = det_hessian_at_identity_rank(r)
        determinant_cases.append({
            "size": r,
            "rank_at_zero_corank_1": rank_at_corank_one,
            "bound_2r": 2 * r,
            "rank_at_zero_corank_2": rank_at_corank_two,
            "rank_at_nonzero_identity": rank_at_identity,
            "variable_count": r * r,
            "checks_pass": rank_at_corank_one == 2 * r
                and rank_at_corank_two == 4
                and rank_at_identity == r * r,
        })

    result = {
        "status": "PASS" if all(c["full_rank"] for c in permanent_cases)
            and all(c["checks_pass"] for c in determinant_cases) else "FAIL",
        "arithmetic": "exact Fraction Gaussian elimination over Q",
        "permanent_witness": "first row (1,...,1,-(m-1)); all remaining rows all ones",
        "permanent_cases": permanent_cases,
        "determinant_cases": determinant_cases,
        "scope": "Finite exact checks only; the uniform Hessian identities are proved in RESULT.txt.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
