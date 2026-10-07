#!/usr/bin/env python3
"""Independent small-instance audit of the c03_s03 cut-rank claim.

Uses only integer arithmetic and brute-force minors; deliberately does not
import the peer's MPS implementation.  Scope: Schmidt-rank identity on small
instances and the staircase-family coefficient formula, not asymptotics.
"""
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def det(a):
    a = [[Fraction(x) for x in row] for row in a]
    n = len(a)
    if n == 0:
        return Fraction(1)
    ans = Fraction(1)
    for j in range(n):
        p = next((i for i in range(j, n) if a[i][j]), None)
        if p is None:
            return Fraction(0)
        if p != j:
            a[p], a[j] = a[j], a[p]
            ans = -ans
        pivot = a[j][j]
        ans *= pivot
        for i in range(j + 1, n):
            if a[i][j]:
                q = a[i][j] / pivot
                for h in range(j + 1, n):
                    a[i][h] -= q * a[j][h]
                a[i][j] = 0
    return ans


def rank(a):
    a = [[Fraction(x) for x in row] for row in a]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for j in range(n):
        p = next((i for i in range(r, m) if a[i][j]), None)
        if p is None:
            continue
        a[p], a[r] = a[r], a[p]
        pivot = a[r][j]
        for i in range(r + 1, m):
            if a[i][j]:
                q = a[i][j] / pivot
                for h in range(j, n):
                    a[i][h] -= q * a[r][h]
        r += 1
        if r == m:
            break
    return r


def minor(a, rows, cols):
    return det([[a[i][j] for j in cols] for i in rows])


def physical_vector(a):
    """Site-interleaved coefficient vector for exp(sum F_ij u_i d_j)."""
    n = len(a)
    v = {}
    for k in range(n + 1):
        for I in combinations(range(n), k):
            for J in combinations(range(n), k):
                # In up-then-down order the pair amplitude is (-1)^(k(k-1)/2) det F[I,J].
                amp = (-1) ** (k * (k - 1) // 2) * minor(a, I, J)
                # Convert u_0...u_{n-1} d_0...d_{n-1} to
                # u_0 d_0 u_1 d_1 ...; each d_i crosses later u_j.
                crossings = sum(1 for i in J for j in I if i < j)
                amp *= (-1) ** crossings
                state = [0] * n
                for i in I:
                    state[i] |= 1
                for j in J:
                    state[j] |= 2
                v[tuple(state)] = amp
    return v


def matrix_rank(matrix):
    return rank(matrix)


def predicted_cut_rank(a, p):
    n = len(a)
    left = list(range(p))
    right = list(range(p, n))
    lr = [[a[i][j] for j in right] for i in left]
    rl = [[a[i][j] for j in left] for i in right]
    return 2 ** (rank(lr) + rank(rl))


def actual_cut_rank(a, p):
    n = len(a)
    coeff = physical_vector(a)
    row_states = list(product(range(4), repeat=p))
    col_states = list(product(range(4), repeat=n - p))
    rows = []
    for x in row_states:
        rows.append([coeff.get(x + y, 0) for y in col_states])
    return matrix_rank(rows)


def check_cut_rank_family():
    matrices = [
        [[0, 1, 2, 0], [3, 0, 1, 1], [0, 2, 0, 1], [2, 1, 3, 0]],
        [[0, 1, 0, 0], [0, 0, 2, 0], [3, 0, 0, 1], [0, 2, 0, 0]],
        [[0, 2, 4, 6], [0, 0, 3, 9], [0, 0, 0, 5], [0, 0, 0, 0]],
        [[0, 1, 2], [3, 0, 5], [7, 11, 0]],
    ]
    checked = []
    for a in matrices:
        n = len(a)
        cuts = []
        for p in range(n + 1):
            observed = actual_cut_rank(a, p)
            predicted = predicted_cut_rank(a, p)
            assert observed == predicted, (a, p, observed, predicted)
            cuts.append({"p": p, "rank": observed, "predicted": predicted})
        checked.append({"n": n, "cuts": cuts})
    return checked


def staircase_norm(n, k):
    # F_ij=1 for i<j, 2 for i>j, 0 on diagonal. Enumerate disjoint I,J.
    f = [[0 if i == j else (1 if i < j else 2) for j in range(n)] for i in range(n)]
    total = 0
    for I in combinations(range(n), k):
        setI = set(I)
        for J in combinations((j for j in range(n) if j not in setI), k):
            d = minor(f, I, J)
            total += d * d
    return total


def check_staircase():
    out = []
    for n in range(2, 9):
        for k in range(1, n // 2 + 1):
            got = staircase_norm(n, k)
            # C_k = binom(n,2k) (1^2+2^2) |1-2|^(2k-2).
            import math
            want = math.comb(n, 2 * k) * 5
            assert got == want, (n, k, got, want)
            out.append({"n": n, "k": k, "count": str(got), "formula": str(want)})
    return out


def main():
    report = {
        "purpose": "independent exact finite audit; no peer implementation imported",
        "cut_rank_checks": check_cut_rank_family(),
        "staircase_checks": check_staircase(),
        "scope": [
            "confirms the cut-rank/Schmidt-rank identity on four rational matrices of sizes 3 and 4",
            "confirms the peer's staircase coefficient formula by direct complementary-minor enumeration through n=8",
            "does not validate the general algorithm bit-complexity theorem or external novelty",
        ],
    }
    path = Path(__file__).with_name("cutrank_independent_audit.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
