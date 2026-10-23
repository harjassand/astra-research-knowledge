#!/usr/bin/env python3
"""Finite supporting checks for the explicit graph; universal proof is in notes."""
from itertools import product
from pathlib import Path
import json, time, resource

def construct():
    # 0 apex, 1..8 central path, 9+4*(j-1)..12+4*(j-1) attached P4.
    edges=set()
    for j in range(1,9):
        edges.add((0,j))
        if j<8: edges.add((j,j+1))
        hs=list(range(9+4*(j-1),13+4*(j-1)))
        for h in hs: edges.add((j,h))
        for a,b in zip(hs,hs[1:]): edges.add((a,b))
    bags=[{0,j,j+1} for j in range(1,8)]
    bedges=[(i,i+1) for i in range(6)]
    for j in range(1,9):
        hs=list(range(9+4*(j-1),13+4*(j-1)))
        start=len(bags)
        bags += [{j,hs[k],hs[k+1]} for k in range(3)]
        bedges += [(min(j-1,6),start),(start,start+1),(start+1,start+2)]
    return edges,bags,bedges

def verify():
    st=time.perf_counter(); ct=time.process_time()
    edges,bags,bedges=construct()
    assert len(edges)==71 and set().union(*bags)==set(range(41))
    assert max(map(len,bags))==3
    assert len(bedges)==len(bags)-1
    adj=[set() for b in bags]
    for a,b in bedges: adj[a].add(b);adj[b].add(a)
    for u,v in edges: assert any({u,v}<=b for b in bags)
    for v in range(41):
        ids={i for i,b in enumerate(bags) if v in b}; seen=set(); stack=[next(iter(ids))]
        while stack:
            a=stack.pop()
            if a in seen: continue
            seen.add(a);stack += list((adj[a]&ids)-seen)
        assert seen==ids
    count=0
    for cs in product(range(4),repeat=8):
        if any(cs[i]==cs[i+1] for i in range(7)):continue
        redundant=[cs.count(c)>1 for c in cs]
        assert any(redundant[i] and redundant[i+1] for i in range(7))
        count+=1
    assert count==4*3**7
    return {'status':'passed','vertices':41,'edges':len(edges),'bag_count':len(bags),'bag_width':2,'proper_four_color_path_assignments':count,'scope':'Exact finite fixture/decomposition and redundant-pair check, not the all-coloring proof','wall_seconds':time.perf_counter()-st,'cpu_seconds':time.process_time()-ct,'peak_rss_bytes':1024*resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path)
    a=p.parse_args();rec=verify();s=json.dumps(rec,indent=2)+'\n'
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(s,end='')
