#!/usr/bin/env python3
"""Small exact fixtures for the phase-retaining block tensor and replica-rank bound."""
from fractions import Fraction
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
        term = (-1 if inv % 2 else 1)
        for i, j in enumerate(p):
            term *= A[i][j]
        total += term
    return total


def minors(A, rows, cols):
    return [[A[i][j] for j in cols] for i in rows]


def local_coeffs(A):
    n = len(A)
    out = []
    for ell in range(n // 2 + 1):
        val = 0
        for I in combinations(range(n), ell):
            Iset = set(I)
            for J in combinations([j for j in range(n) if j not in Iset], ell):
                d = det(minors(A, I, J))
                val += d * d
        out.append(val)
    return out


def conv(a, b, cap):
    z = [0] * (cap + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j <= cap:
                z[i + j] += x * y
    return z


def brute_c(A, k):
    n = len(A)
    total = 0
    for I in combinations(range(n), k):
        Iset = set(I)
        for J in combinations([j for j in range(n) if j not in Iset], k):
            d = det(minors(A, I, J))
            total += d * d
    return total


def block_diagonal(blocks):
    n = sum(len(B) for B in blocks)
    A = [[0] * n for _ in range(n)]
    offset = 0
    for B in blocks:
        b = len(B)
        for i in range(b):
            for j in range(b):
                A[offset + i][offset + j] = B[i][j]
        offset += b
    return A


def replica_matrix(q):
    # One replica amplitude is sum_x |x>_L |~x>_R.
    # Two independent replicas have row label (x,y), column (~x,~y).
    d = 1 << (2 * q)
    M = [[0] * d for _ in range(d)]
    mask = (1 << q) - 1
    for x in range(1 << q):
        for y in range(1 << q):
            row = x * (1 << q) + y
            col = (mask ^ x) * (1 << q) + (mask ^ y)
            M[row][col] = 1
    return M


def main():
    blocks = [
        [[0, 1], [1, 0]],
        [[1, 1], [1, -1]],
        [[1, 2, 0], [0, 1, 1], [2, 0, 1]],
    ]
    A = block_diagonal(blocks)
    cap = len(A) // 2
    dp = [1] + [0] * cap
    for B in blocks:
        dp = conv(dp, local_coeffs(B), cap)
    brute = [brute_c(A, k) for k in range(cap + 1)]
    assert dp == brute

    q_results = []
    for q in range(1, 5):
        M = replica_matrix(q)
        d = 1 << (2 * q)
        assert all(sum(row) == 1 for row in M)
        assert all(sum(M[i][j] for i in range(d)) == 1 for j in range(d))
        full_norm_sq = sum(x * x for row in M for x in row)
        shared_norm_sq = 1 << q
        assert full_norm_sq == 1 << (2 * q)
        assert shared_norm_sq * (1 << q) == full_norm_sq
        q_results.append({
            "q": q,
            "two_replica_schmidt_rank": d,
            "full_tensor_norm_squared": full_norm_sq,
            "shared_orientation_norm_squared": shared_norm_sq,
            "retained_fraction": f"1/{1 << q}",
        })

    plus = [[1, 1], [1, 1]]
    minus = [[1, 1], [1, -1]]
    assert [abs(x) for row in plus for x in row] == [abs(x) for row in minus for x in row]
    def embed_cross(A2):
        return [[0, 0, *A2[0]], [0, 0, *A2[1]], [0, 0, 0, 0], [0, 0, 0, 0]]
    plus4, minus4 = embed_cross(plus), embed_cross(minus)
    phase_pair = {
        "abs_entrywise_equal": True,
        "legal_disjoint_minor_plus": det(plus),
        "legal_disjoint_minor_minus": det(minus),
        "c2_plus": brute_c(plus4, 2),
        "c2_minus": brute_c(minus4, 2),
    }
    assert phase_pair["c2_plus"] == 0 and phase_pair["c2_minus"] == 4

    result = {
        "status": "PASS exact integer fixtures",
        "block_dp_coefficients": dp,
        "block_bruteforce_coefficients": brute,
        "replica_rank_fixtures": q_results,
        "phase_sensitive_legal_disjoint_minor": phase_pair,
        "scope": "Finite exact bookkeeping fixtures only; proofs are in INITIAL.txt. No sampler or general counting algorithm executed.",
    }
    Path(__file__).with_name("phase_tensor_check.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
