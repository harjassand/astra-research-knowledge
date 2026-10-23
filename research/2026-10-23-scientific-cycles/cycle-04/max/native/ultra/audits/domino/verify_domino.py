#!/usr/bin/env python3
"""Stdlib-only verification of the saved rational rook decomposition.

No LP solver or numpy required; the candidate is NOT a counterexample.
"""
import itertools, json, time
from pathlib import Path
from fractions import Fraction as F
from check_domino import projector, overlap, partitions

cpu=time.process_time()
data=json.loads(Path(__file__).with_name('RESULT.json').read_text())
states=[]
for s in (1,-1): states.append((projector(0),projector(0,1,s)))
for s in (1,-1): states.append((projector(2),projector(1,2,s)))
for s in (1,-1): states.append((projector(0,1,s),projector(2)))
for s in (1,-1): states.append((projector(1,2,s),projector(0)))
states.append((projector(1),projector(1)))
G=[[(overlap(a,c)+overlap(b,d))/3 for c,d in states] for a,b in states]
assert G==[[F(x) for x in row] for row in data['gram']]
assert all(overlap(a,c)*overlap(b,d)==int(j==k)
           for j,(a,b) in enumerate(states) for k,(c,d) in enumerate(states))
graphs=set()
for rows in partitions(tuple(range(9))):
    for row1 in itertools.permutations(rows[1]):
        for row2 in itertools.permutations(rows[2]):
            grid=(rows[0],row1,row2);edges=set()
            for row in grid:
                edges.update(tuple(sorted(p)) for p in itertools.combinations(row,2))
            for col in zip(*grid):
                edges.update(tuple(sorted(p)) for p in itertools.combinations(col,2))
            graphs.add(tuple(sorted(edges)))
assert len(graphs)==5040
M=[[F(0) for _ in range(9)] for _ in range(9)]
weight=F(0)
for d in data['decomposition']:
    w=F(d['weight']);assert w>=0;weight+=w
    graph=tuple(tuple(p) for p in d['rook_edges']);assert graph in graphs
    for i in range(9): M[i][i]+=w*F(2,3)
    for i,j in graph: M[i][j]+=w/3;M[j][i]+=w/3
assert weight==1 and M==G
print(json.dumps({'status':'PASS_EXACT_MEMBERSHIP_NOT_COUNTEREXAMPLE',
                  'rook_graphs':len(graphs),'rational_mixture_terms':len(data['decomposition']),
                  'cpu_seconds':time.process_time()-cpu}))
