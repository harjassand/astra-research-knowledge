#!/usr/bin/env python3
"""Exact finite certificates for replicated-input spectral ranks."""
import itertools
import json
import math
import random
from pathlib import Path

PRIME = 1000000007

def rank_mod(matrix, prime=PRIME):
    a = [[z % prime for z in row] for row in matrix]
    if not a:
        return 0
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], prime - 2, prime)
        a[rank] = [(x * inv) % prime for x in a[rank]]
        for i in range(rank + 1, len(a)):
            factor = a[i][col]
            if factor:
                a[i] = [(x - factor * y) % prime for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a[0]):
            break
    return rank

def choose(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0

def projected_replication(r, q, j, weights=None):
    words = list(itertools.product(range(r), repeat=q))
    index = {a: i for i, a in enumerate(words)}
    coeff = [sum((-1)**i * choose(t, i) * choose(q-t, j-i)
                 for i in range(j+1)) for t in range(q+1)]
    result = []
    for a in words:
        for d in words:
            row = [0] * len(words)
            for mask in range(1 << q):
                b = tuple(d[t] if mask >> t & 1 else a[t] for t in range(q))
                c = tuple(a[t] if mask >> t & 1 else d[t] for t in range(q))
                weight = 1 if weights is None else weights[(b, c)]
                row[index[b]] += coeff[mask.bit_count()] * weight
            result.append(row)
    return result

def main():
    records = []
    weighted_records = []
    for r, q in [(2, q) for q in range(1, 6)] + [(3, q) for q in range(1, 4)]:
        for j in range(q+1):
            rank = rank_mod(projected_replication(r, q, j))
            expected = sum(math.comb(q, s)*(r-1)**s for s in range(j, q+1))
            assert rank == expected, (r, q, j, rank, expected)
            records.append(dict(r=r, Q=q, n=r**q, D=r**(2*q),
                                spectral_level=j, modular_rank=rank,
                                rational_rank_certified=expected))
    rng = random.Random(20261027)
    for r, q in [(2, 2), (2, 3), (3, 2)]:
        words = list(itertools.product(range(r), repeat=q))
        for trial in range(12):
            weights = {(a,d): rng.choice([-3,-2,-1,1,2,3])
                       for a in words for d in words}
            for j in range(q+1):
                rank = rank_mod(projected_replication(r,q,j,weights))
                lower = sum(math.comb(q,s)*(r-1)**s for s in range(j,q+1))
                assert rank >= lower, (r,q,trial,j,rank,lower)
                weighted_records.append(dict(r=r,Q=q,trial=trial,spectral_level=j,
                                             modular_rank=rank,proved_lower_bound=lower))
    out = dict(status="all assertions passed", arithmetic="exact modular integers",
               prime=PRIME, cases=len(records), records=records,
               weighted_cases=len(weighted_records), weighted_records=weighted_records,
               interpretation="Modular lower ranks attain proved rational upper ranks.")
    Path(__file__).with_name("dense_grid_alias_results.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("records","weighted_records")}, indent=2))

if __name__ == "__main__":
    main()
