#!/usr/bin/env python3
"""Exact minimal-rank fixture showing complete cancellation in the tag expansion."""
from itertools import combinations, permutations
import json
from pathlib import Path


def det(A):
    n = len(A)
    if n == 0:
        return 1
    total = 0
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = -1 if inversions % 2 else 1
        for i, j in enumerate(p):
            term *= A[i][j]
        total += term
    return total


def sub(A, I, J):
    return [[A[i][j] for j in J] for i in I]


def main():
    # Two 2x2 diagonal blocks in G; H=XY^T has rank exactly 2 and only
    # off-block entries. On the sole potentially nonzero legal 2-minor,
    # the p=0 term is +1 and the p=2 term is -1.
    G = [[0] * 4 for _ in range(4)]
    G[0][1] = G[2][3] = 1
    X = [[1, 0], [0, 0], [0, 1], [0, 0]]
    Y = [[0, 0], [0, 1], [0, 0], [1, 0]]
    H = [[sum(X[i][s] * Y[j][s] for s in range(2)) for j in range(4)] for i in range(4)]
    F = [[G[i][j] + H[i][j] for j in range(4)] for i in range(4)]

    I, J = (0, 2), (1, 3)
    terms = []
    for p in range(3):
        for Apos in combinations(range(2), p):
            R = [I[a] for a in Apos]
            Irest = [I[a] for a in range(2) if a not in Apos]
            for Bpos in combinations(range(2), p):
                C = [J[b] for b in Bpos]
                Jrest = [J[b] for b in range(2) if b not in Bpos]
                sign = -1 if (sum(Apos) + sum(Bpos)) % 2 else 1
                for S in combinations(range(2), p):
                    dx = det([[X[i][s] for s in S] for i in R])
                    dy = det([[Y[j][s] for s in S] for j in C])
                    residual = det(sub(G, Irest, Jrest))
                    amplitude = sign * dx * dy * residual
                    terms.append({"p": p, "A_positions": list(Apos), "B_positions": list(Bpos),
                                  "S_zero_based": list(S), "tag_amplitude": amplitude,
                                  "squared_magnitude": amplitude ** 2})
    coherent = sum(t["tag_amplitude"] for t in terms)
    diagonal_positive = sum(t["squared_magnitude"] for t in terms)
    actual_minor = det(sub(F, I, J))
    assert actual_minor == coherent == 0
    assert diagonal_positive == 2
    c2 = 0
    for rows in combinations(range(4), 2):
        for cols in combinations([j for j in range(4) if j not in rows], 2):
            c2 += det(sub(F, rows, cols)) ** 2
    assert c2 == 0
    result = {
        "status": "PASS exact integer cancellation fixture",
        "n": 4,
        "rank_update_rank": 2,
        "block_partition": [[0, 1], [2, 3]],
        "G": G,
        "H": H,
        "F": F,
        "legal_pair": {"I_zero_based": list(I), "J_zero_based": list(J)},
        "tag_terms": terms,
        "coherent_minor": coherent,
        "direct_minor": actual_minor,
        "diagonal_only_tag_mass_for_this_pair": diagonal_positive,
        "c2": c2,
        "scope": "Minimal rank-two off-block update; rules out only diagonal-tag dephasing as a multiplicative proxy, not every nonnegative tensor representation."
    }
    Path(__file__).with_name("tag_dephasing_check.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
