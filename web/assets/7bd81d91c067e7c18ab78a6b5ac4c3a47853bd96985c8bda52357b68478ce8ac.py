#!/usr/bin/env python3
"""Exact rational lift audit of a recent binary basis-pair obstruction."""
from itertools import combinations
from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location("plucker", "work/cycle6/c01_l03/plucker_replica_sos.py")
plucker = module_from_spec(spec)
spec.loader.exec_module(plucker)
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
all_cols = set(range(18))
bases = set()
for S in combinations(range(18), 9):
    if plucker.ordered_minor(M, S):
        bases.add(frozenset(S))

def canonical_pair(B, C):
    return tuple(sorted((frozenset(B), frozenset(C)), key=lambda s: tuple(sorted(s))))

def split_count(B):
    return sum((2*i in B) != (2*i+1 in B) for i in range(9))

nodes = {canonical_pair(B, all_cols - B) for B in bases
         if frozenset(all_cols - B) in bases}
s_values = {split_count(B) for B, _ in nodes}
s5 = sum(split_count(B) == 5 for B, _ in nodes)
seen = set()
component_s = []
edge_count = 0
for root in nodes:
    if root in seen:
        continue
    seen.add(root)
    stack = [root]
    values = set()
    while stack:
        B, C = stack.pop()
        values.add(split_count(B))
        for x in B:
            for y in C:
                B2 = frozenset((set(B) - {x}) | {y})
                C2 = frozenset((set(C) - {y}) | {x})
                if B2 in bases and C2 in bases:
                    edge_count += 1
                    nxt = canonical_pair(B2, C2)
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
    component_s.append(sorted(values))
print({"q_bases": len(bases), "complement_basis_pairs": len(nodes),
       "split_counts": sorted(s_values), "s5_pairs": s5,
       "symmetric_exchange_components": len(component_s),
       "component_split_counts": sorted(component_s),
       "directed_valid_exchanges_scanned": edge_count})
