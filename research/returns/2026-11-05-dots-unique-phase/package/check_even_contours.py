"""Exhaustive finite checks of the connected-even-component contour encoding."""
from collections import defaultdict, deque
from itertools import product
from pathlib import Path
import json


def dual_edge(u,v):
    (x,y),(a,b)=sorted((u,v))
    if a==x+1 and b==y:
        ends=((2*x+1,2*y-1),(2*x+1,2*y+1))
    else:
        assert a==x and b==y+1
        ends=((2*x-1,2*y+1),(2*x+1,2*y+1))
    return tuple(sorted(ends))


def walls(spins,L):
    out=set()
    for x in range(-1,L):
        for y in range(L):
            u,v=(x,y),(x+1,y)
            if spins.get(u,1)!=spins.get(v,1):out.add(dual_edge(u,v))
    for x in range(L):
        for y in range(-1,L):
            u,v=(x,y),(x,y+1)
            if spins.get(u,1)!=spins.get(v,1):out.add(dual_edge(u,v))
    return out


def components(edges):
    incident=defaultdict(set)
    for edge in edges:
        for vertex in edge:incident[vertex].add(edge)
    assert all(len(es) in (2,4) for es in incident.values())
    unseen=set(edges);out=[]
    while unseen:
        todo=[next(iter(unseen))];component=set()
        while todo:
            edge=todo.pop()
            if edge in component:continue
            component.add(edge);unseen.discard(edge)
            for vertex in edge:todo.extend(incident[vertex]-component)
        out.append(component)
    return out,any(len(es)==4 for es in incident.values())


def reconstruct(edges,L):
    domain=set(product(range(-1,L+1),repeat=2))
    spins={(-1,-1):1};todo=deque([(-1,-1)])
    while todo:
        u=todo.popleft()
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            v=(u[0]+dx,u[1]+dy)
            if v not in domain:continue
            sign=spins[u]*(-1 if dual_edge(u,v) in edges else 1)
            if v in spins:assert spins[v]==sign
            else:spins[v]=sign;todo.append(v)
    assert all(s==1 for (x,y),s in spins.items() if x in (-1,L) or y in (-1,L))
    interior={p:s for p,s in spins.items() if 0<=p[0]<L and 0<=p[1]<L}
    assert walls(interior,L)==edges
    return interior


def hull(edges,L):
    domain=set(product(range(-1,L+1),repeat=2))
    outside={(-1,-1)};todo=deque([(-1,-1)])
    while todo:
        u=todo.popleft()
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            v=(u[0]+dx,u[1]+dy)
            if v in domain and v not in outside and dual_edge(u,v) not in edges:
                outside.add(v);todo.append(v)
    return domain-outside


def main():
    results=[]
    for L in (2,3):
        sites=list(product(range(L),repeat=2))
        degree_four=0;deleted=0;nested=0
        for bits in range(1<<len(sites)):
            spins={p:(1 if bits>>i&1 else -1) for i,p in enumerate(sites)}
            edges=walls(spins,L);cs,degree4=components(edges)
            degree_four+=degree4
            assert reconstruct(edges,L)==spins
            hulls=[hull(c,L) for c in cs]
            cover=set().union(*hulls) if hulls else set()
            assert {p for p,s in spins.items() if s==-1}<=cover
            nested+=any(a < b for a in hulls for b in hulls)
            for c,S in zip(cs,hulls):
                n=len(c);assert n>=4
                assert len(S)<=(n+1)**2
                if S:
                    assert max(max(p[d] for p in S)-min(p[d] for p in S) for d in (0,1))<=n
                reconstruct(edges-c,L)
                deleted+=1
        results.append({'side':L,'spin_configurations':1<<len(sites),
                        'degree_four_configurations':degree_four,
                        'configurations_with_nested_hulls':nested,
                        'whole_component_deletions_verified':deleted})
    assert sum(r['degree_four_configurations'] for r in results)>0
    assert sum(r['configurations_with_nested_hulls'] for r in results)>0
    result={'status':'all exact even-contour checks passed','boxes':results,
            'scope':'Exhaustive small-box encoding, coverage, deletion and geometry checks; not a proof of the infinite-volume theorem.'}
    (Path(__file__).resolve().parent/'even_contour_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
