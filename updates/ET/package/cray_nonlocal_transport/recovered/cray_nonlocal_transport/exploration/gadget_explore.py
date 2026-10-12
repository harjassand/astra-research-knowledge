from collections import deque
from itertools import product
from fractions import Fraction

def graph(w,h):
    sites=[(x,y) for y in range(h) for x in range(w)]
    ix={z:i for i,z in enumerate(sites)}
    edges=[(ix[(x,y)],ix[(x+dx,y+dy)]) for x,y in sites for dx,dy in [(1,0),(0,1)] if (x+dx,y+dy) in ix]
    nb={i:[ix[(x+dx,y+dy)] for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if (x+dx,y+dy) in ix] for i,(x,y) in enumerate(sites)}
    def nexts(s):
        for a,b in edges:
            if ((s>>a)^(s>>b))&1 and any(not (s>>v)&1 for v in nb[a] if v!=b) and any(not(s>>v)&1 for v in nb[b] if v!=a):
                yield s^(1<<a)^(1<<b),(a,b)
    comp={}; cs=[]
    for s in range(1<<len(sites)):
        if s in comp:continue
        k=len(cs);q=[s];comp[s]=k
        for t in q:
            for u,_ in nexts(t):
                if u not in comp: comp[u]=k;q.append(u)
        cs.append(q)
    return sites,ix,nexts,comp,cs

if __name__=='__main__':
 for w,h,pa,pb in [(4,2,(0,0),(2,0)),(5,3,(1,1),(3,1)),(6,3,(1,1),(4,1))]:
    sites,ix,nxt,comp,cs=graph(w,h)
    env=[i for i in range(w*h) if i not in [ix[pa],ix[pb]]]
    failcounts={};succcounts={}
    for v in range(1<<len(env)):
        s=sum(((v>>j)&1)<<i for j,i in enumerate(env))|(1<<ix[pa])
        t=s^(1<<ix[pa])^(1<<ix[pb])
        counts=succcounts if comp[s]==comp[t] else failcounts
        n=v.bit_count();counts[n]=counts.get(n,0)+1
    print(w,h,'components',len(cs),'success',succcounts,'fail',failcounts,flush=True)
    if w==4:
        # per-block lower-left port; env offsets (1,0),(0,1),(1,1)
        left=[ix[(1,0)],ix[(0,1)],ix[(1,1)]]
        right=[ix[(3,0)],ix[(2,1)],ix[(3,1)]]
        feasible=[]
        # symmetric rule horizontally and vertically: exchange first two bits
        for mask in range(1,256):
            allowed=[v for v in range(8) if (mask>>v)&1]
            if any((v&1)<<1 | (v&2)>>1 | (v&4) not in allowed for v in []):pass
            symmetric=all((((v&1)<<1)|((v&2)>>1)|(v&4)) in allowed for v in allowed)
            if not symmetric:continue
            ok=True
            for a,b in product(allowed,repeat=2):
                s=(1<<ix[(0,0)])+sum(((a>>i)&1)<<left[i] for i in range(3))+sum(((b>>i)&1)<<right[i] for i in range(3))
                t=s^1^(1<<ix[(2,0)])
                if comp[s]!=comp[t]:ok=False;break
            if ok:feasible.append(allowed)
        maximal=[a for a in feasible if not any(set(a)<set(b) for b in feasible)]
        print('maximal symmetric gates',maximal,flush=True)
