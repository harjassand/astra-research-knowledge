#!/usr/bin/env python3
"""Exact bounded checks for the phase-two microscopic-kernel attack."""
from fractions import Fraction
from itertools import combinations, product
from math import isqrt
from pathlib import Path
from random import Random
from time import perf_counter
import json

from fixed_rank_micro_sampler import QI, TaggedSampler, det, sub


def rank(matrix):
    a = [[x if isinstance(x, QI) else QI(x) for x in row] for row in matrix]
    m, n = len(a), len(a[0])
    row = 0
    for col in range(n):
        pivot = next((i for i in range(row, m) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        p = a[row][col]
        for j in range(col, n):
            a[row][j] = a[row][j] / p
        for i in range(row + 1, m):
            factor = a[i][col]
            for j in range(col, n):
                a[i][j] = a[i][j] - factor * a[row][j]
        row += 1
        if row == m:
            break
    return row


def cycle_counter(q):
    n = 2 * q
    F = [[int(j == (i + 1) % n) for j in range(n)] for i in range(n)]
    support = []
    for I in combinations(range(n), q):
        J = tuple(i for i in range(n) if i not in I)
        w = det(sub(F, I, J)).norm2()
        if w:
            support.append((I, w))
    assert len(support) == 2 and all(w == 1 for _, w in support)
    assert len(set(support[0][0]) ^ set(support[1][0])) == 2 * q
    pairs = list(product(range(2), repeat=2))
    P = [[Fraction(0) for _ in pairs] for _ in pairs]
    for s, (a, b) in enumerate(pairs):
        for t, (c, d) in enumerate(pairs):
            old_union = [int(i in support[a][0]) + int(i in support[b][0]) for i in range(n)]
            new_union = [int(i in support[c][0]) + int(i in support[d][0]) for i in range(n)]
            # Every nonholding single-replica move would replace q>2 pairs.
            allowed = old_union == new_union
            if allowed:
                P[s][t] += Fraction(1, 4)
            else:
                P[s][s] += Fraction(1, 4)
    f = [0, 1]
    values = [f[a] + f[b] for a, b in pairs]
    energy = sum(Fraction(1, 8) * P[s][t] * (values[s] - values[t]) ** 2
                 for s in range(4) for t in range(4))
    assert energy == 0
    assert all(sum(row) == 1 for row in P)
    assert all(P[s][t] == P[t][s] for s in range(4) for t in range(4))
    return {"q": q, "n": n, "full_basis_support": [list(I) for I, _ in support],
            "single_replica_variance": "1/4", "additive_two_replica_energy": "0",
            "kernel_matrix": [[str(x) for x in row] for row in P]}


def embedded_sampler():
    # Two ambient singleton blocks, one pair per block; rank-one off-block V.
    n, m = 2, 2
    V = [[1, 1, 0, 2], [0, 1, 1, 2]]
    local = [[1, 0, 0, 0], [0, 0, 1, 0]]
    X = [1, 1]
    Y = [0, 1, 0, 2]
    assert all(V[i][j] == local[i][j] + X[i] * Y[j] for i in range(n) for j in range(2*m))
    size = n + 2*m
    K = [[0 for _ in range(size)] for _ in range(size)]
    for ell in range(m):
        s, t = n + 2*ell, n + 2*ell + 1
        for i in range(n):
            K[s][i] = V[i][2*ell]
            K[t][i] = V[i][2*ell+1]
        K[s][t] = 1
    Xt = [X[i] if i < n else 0 for i in range(size)]
    Yt = [0 if i < n else Y[i-n] for i in range(size)]
    H = [[Yt[i]*Xt[j] for j in range(size)] for i in range(size)]
    G = [[K[i][j]-H[i][j] for j in range(size)] for i in range(size)]
    assert rank(H) == 1
    order = [0, 2, 3, 1, 4, 5]
    parts = [order[:3], order[3:]]
    assert all(G[i][j] == 0 for a, B in enumerate(parts) for b, C in enumerate(parts)
               if a != b for i in B for j in C)
    blocks = [sub(G, B, B) for B in parts]
    activities_old = [1, 1, 1, Fraction(3, 2), 1, Fraction(3, 2)]
    # Set the t0 activity to 1 and t1 to 3/2; s lines all have activity one.
    activities_old[3] = Fraction(1)
    sampler = TaggedSampler(blocks, [[Yt[i]] for i in order], [[Xt[i]] for i in order],
                            3, [activities_old[i] for i in order])
    assert sampler.completion_mass() == sampler.direct_mass() == 7
    mapped_support = {}
    for I in combinations(range(size), 3):
        J = tuple(i for i in range(size) if i not in I)
        w = det(sub(sampler.F, I, J)).norm2()
        for i in I:
            w *= sampler.activities[i]
        if w:
            original_indices = [order[i] for i in I]
            assert 2 in original_indices and 4 in original_indices
            A = tuple(ell for ell in range(m) if n+2*ell+1 in original_indices)
            mapped_support[A] = mapped_support.get(A, Fraction(0)) + w
    assert mapped_support == {(0,): Fraction(1), (1,): Fraction(6)}
    rng = Random(112)
    for _ in range(32):
        I, J = sampler.sample(rng)
        original_indices = [order[i] for i in I]
        A = tuple(ell for ell in range(m) if n+2*ell+1 in original_indices)
        assert A in mapped_support
    return {"ambient_rows": n, "old_pairs": m, "canonical_dimension": size,
            "block_sizes": [3, 3], "rank_update": 1,
            "canonical_full_basis_partition": "7", "old_basis_weights": {str(k): str(v) for k,v in mapped_support.items()},
            "mapped_exact_draws": 32}


def weak_balance_check():
    rows = []
    product_ratio = Fraction(1)
    for r in range(2, 20, 2):
        d = r-1
        b = 0
        while 2**(2*b) < 16*d:
            b += 1
        a = isqrt(isqrt((4*2**(4*b))//d))
        tau = Fraction(a, 2**b)
        ratio = Fraction(1, d) / tau**4
        assert Fraction(1, 4) <= ratio <= Fraction(64, 81)
        product_ratio *= ratio
        rows.append({"residual_size":r, "rational_tau":str(tau), "g_over_q":str(ratio)})
    assert product_ratio <= Fraction(64,81)**9
    return {"rows": rows, "recursive_ratio_product": str(product_ratio)}


def main():
    start = perf_counter()
    J = [[1]*4 for _ in range(4)]
    natural_residual = [[int(i != j) for j in range(4)] for i in range(4)]
    assert rank(J) == 1 and rank(natural_residual) == 4
    result = {"status":"PASS exact bounded microscopic scope checks",
              "cycle_union_swap_counters":[cycle_counter(q) for q in [3,4]],
              "rank_preserving_canonical_sampler":embedded_sampler(),
              "decomposition_acquisition_counter":{"n":4,"promised_update_rank":1,"natural_residual_rank":4},
              "weak_balance_counter":weak_balance_check(),
              "elapsed_seconds":perf_counter()-start,
              "scope":"Finite fixture validation only. Universal kernel energy and rank-scope statements are proved in MICROSCOPIC_PAIR_KERNEL.txt."}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
