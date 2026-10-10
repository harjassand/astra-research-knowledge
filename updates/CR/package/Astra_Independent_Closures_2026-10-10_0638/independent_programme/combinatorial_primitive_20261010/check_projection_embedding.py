"""Verify the exact linear-hypergraph projection representation."""
from itertools import combinations
from random import Random
from check_folds import sunflower
import json


def representation(n, edges, colors):
    edges={frozenset(e) for e in edges}
    pair_edge={}
    for e in edges:
        assert len(e)==3
        assert len({colors[v] for v in e})==2
        for p in combinations(sorted(e),2):
            assert p not in pair_edge
            pair_edge[p]=e
    blocks=[pair_edge.get(p,frozenset(p)) for p in combinations(range(n),2)]
    # The final identity coordinate makes the projection injective.
    projected=[tuple(0 if v in B else v+1 for B in blocks)+(v+1,) for v in range(n)]
    full=[(colors[v],)+projected[v] for v in range(n)]
    assert len(set(projected))==n
    for t in combinations(range(n),3):
        assert sunflower([projected[v] for v in t])==(frozenset(t) in edges)
        assert not sunflower([full[v] for v in t])
    return {'vertices':n,'edges':len(edges),'rank':len(full[0]),'all_triples_checked':True}


def main():
    fano=[tuple(x-1 for x in e) for e in combinations(range(1,8),3) if e[0]^e[1]^e[2]==0]
    records=[representation(7,fano,[(v+1).bit_length()-1 for v in range(7)])]
    rng=Random(104729)
    n=18
    colors=[v//6 for v in range(n)]
    candidates=[e for e in combinations(range(n),3) if len({colors[v] for v in e})==2]
    rng.shuffle(candidates)
    edges=[]; used=set()
    for e in candidates:
        pairs=set(combinations(e,2))
        if not pairs&used:
            edges.append(e); used|=pairs
    records.append(representation(n,edges,colors))
    print(json.dumps(records,indent=2))

if __name__=='__main__': main()
