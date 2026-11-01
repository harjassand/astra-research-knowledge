#!/usr/bin/env python3
"""Exhaustive small graph controls; ordinary proof is in the companion note."""
from itertools import combinations, permutations, product
from functools import lru_cache
import json

def check(n,mask):
    pairs=list(combinations(range(n),2));edges={e for i,e in enumerate(pairs) if mask>>i&1}
    adj=[set() for _ in range(n)]
    for i,j in edges:adj[i].add(j);adj[j].add(i)
    def edge(i,j):return j in adj[i]
    unseen=set(range(n));biclique=True
    while unseen:
        root=min(unseen);col={root:0};todo=[root]
        while todo:
            i=todo.pop()
            for j in adj[i]:
                if j in col:
                    if col[i]==col[j]:biclique=False
                else:col[j]=1-col[i];todo.append(j)
        unseen-=set(col)
        for i,j in combinations(col,2):
            if edge(i,j)!=(col[i]!=col[j]):biclique=False
    witness=None
    for tri in combinations(range(n),3):
        if all(edge(i,j) for i,j in combinations(tri,2)):
            x=[0]*n;x[tri[0]]=x[tri[1]]=1;x[tri[2]]=2
            witness=(tuple(x),tri[:2],'triangle');break
    if witness is None:
        for p in permutations(range(n),4):
            if all(edge(p[i],p[i+1]) for i in range(3)) and all(not edge(p[i],p[j]) for i,j in [(0,2),(0,3),(1,3)]):
                x=[0]*n
                for i in p:x[i]=1
                witness=(tuple(x),p[1:3],'induced_P4');break
    assert biclique==(witness is None)
    @lru_cache(None)
    def nu(x):
        i=next((i for i,a in enumerate(x) if a),None)
        if i is None:return 0
        y=list(x);y[i]-=1;best=nu(tuple(y))
        for j in adj[i]:
            if y[j]:
                y[j]-=1;best=max(best,1+nu(tuple(y)));y[j]+=1
        return best
    checked=0
    if witness:
        x,(i,j),kind=witness;y=list(x);y[i]-=1;y[j]-=1
        assert edge(i,j) and nu(x)==2 and nu(tuple(y))==0
    else:
        for x in product(range(3),repeat=n):
            for i,j in edges:
                if x[i] and x[j]:
                    y=list(x);y[i]-=1;y[j]-=1
                    assert nu(x)-nu(tuple(y))==1;checked+=1
    return biclique,checked,(witness[2] if witness else None)

def main():
    out=[]
    for n in range(2,6):
        stats={'vertices':n,'graphs':0,'biclique_unions':0,'exact_removals_checked':0,'triangle_witnesses':0,'induced_P4_witnesses':0}
        for mask in range(1<<(n*(n-1)//2)):
            good,count,witness=check(n,mask);stats['graphs']+=1
            stats['biclique_unions']+=int(good);stats['exact_removals_checked']+=count
            if witness:stats[witness+'_witnesses']+=1
        out.append(stats)
    return {'status':'all exact graph controls passed','scope':'matching property only, not network stability','counts':out}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
