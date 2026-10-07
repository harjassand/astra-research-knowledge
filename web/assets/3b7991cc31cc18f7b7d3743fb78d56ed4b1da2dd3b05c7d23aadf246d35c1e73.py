"""Exact n=4 check for the pair-restricted determinant-volume support."""

from itertools import combinations
import json


def det2(rows, cols, matrix):
    a, b = rows
    c, d = cols
    return matrix[a][c] * matrix[b][d] - matrix[a][d] * matrix[b][c]


def main():
    n = 4
    # Directed 4-cycle permutation matrix: row i has its 1 in column i+1 mod 4.
    matrix = [[int(j == (i + 1) % n) for j in range(n)] for i in range(n)]
    subsets = list(combinations(range(n), 2))
    weights = {}
    for I in subsets:
        total = 0
        for J in subsets:
            if set(I).isdisjoint(J):
                total += det2(I, J, matrix) ** 2
        if total:
            weights[tuple(I)] = total

    support = set(weights)
    expected = {(0, 2), (1, 3)}
    assert support == expected, (support, weights)
    assert all(weight == 1 for weight in weights.values())

    A, B = sorted(support)
    exchanges = []
    for a in A:
        witnesses = [b for b in B if tuple(sorted((set(A) - {a}) | {b})) in support
                     and tuple(sorted((set(B) - {b}) | {a})) in support]
        exchanges.append({"a": a, "witnesses": witnesses})
    assert all(not item["witnesses"] for item in exchanges)

    print(json.dumps({
        "F": matrix,
        "k": 2,
        "nonzero_pair_weights": {str(I): weight for I, weight in weights.items()},
        "support": [list(I) for I in sorted(support)],
        "basis_exchange_witnesses": exchanges,
        "conclusion": "support is not the set of bases of a matroid",
    }, indent=2))


if __name__ == "__main__":
    main()
