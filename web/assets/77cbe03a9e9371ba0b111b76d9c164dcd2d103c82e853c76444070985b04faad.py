#!/usr/bin/env python3
"""Check whether the July-2026 binary basis-pair obstruction lifts to Q."""
from itertools import combinations

A = [
 [1,0,0,1,0,0,1,0,1],
 [1,1,0,0,1,0,0,1,0],
 [0,1,1,0,0,1,0,0,1],
 [1,0,1,1,0,0,1,0,0],
 [0,1,0,1,1,0,0,1,0],
 [0,0,1,0,1,1,0,0,1],
 [1,0,0,1,0,1,1,0,0],
 [0,1,0,0,1,0,1,1,0],
 [0,0,1,0,0,1,0,1,1],
]
M = [[int(i == j) for j in range(9)] + A[i] for i in range(9)]


def det(a):
    a = [row[:] for row in a]
    n = len(a)
    sign, prev = 1, 1
    for k in range(n-1):
        pivot = next((i for i in range(k,n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k],a[pivot] = a[pivot],a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                a[i][j] = (a[i][j]*p - a[i][k]*a[k][j]) // prev
        for i in range(k+1,n): a[i][k] = 0
        prev = p
    return sign*a[-1][-1]


def det_cols(S):
    return det([[M[i][j] for j in S] for i in range(9)])

all_cols = set(range(18))
bases = set()
for S in combinations(range(18),9):
    if det_cols(S): bases.add(frozenset(S))

complement_pairs = set()
s_values = set()
for B in bases:
    C = frozenset(all_cols - set(B))
    if C in bases:
        pair = tuple(sorted((B,C), key=lambda X: tuple(sorted(X))))
        complement_pairs.add(pair)
        s_values.add(sum((2*i in B) != (2*i+1 in B) for i in range(9)))

print({"Q_bases":len(bases), "Q_complement_basis_pairs":len(complement_pairs),
       "split_counts_s":sorted(s_values),
       "s5_pairs":sum(1 for B,C in complement_pairs if sum((2*i in B) != (2*i+1 in B) for i in range(9))==5)})
