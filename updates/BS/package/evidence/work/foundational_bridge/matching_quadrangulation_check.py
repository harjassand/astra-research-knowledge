"""Independent finite checks of family-113 label-adapted quadrangulation.
No numerical proof certificates are asserted. Python standard library only.
"""
from itertools import product
from random import Random
from collections import Counter
import json

counts=Counter()

def check(labels, adjacency):
    m=len(labels)
    S=[{labels[(i-1)%m],labels[i]} for i in range(m)]
    def admissible(arc): return bool(S[arc[0]] & S[arc[-1]])
    def good(arc): return len(arc)==2 or bool(S[arc[1]] & S[arc[-2]])
    def exterior(arc):
        direction=1 if (arc[1]-arc[0])%m==1 else -1
        result=[arc[-1]]
        while result[-1]!=arc[0]: result.append((result[-1]+direction)%m)
        return result
    cells=[]
    def recurse(J):
        assert admissible(J) and len(J)%2==0
        s=len(J)-1
        if s==1:return
        E=exterior(J)
        P=min(S[J[0]]&S[J[-1]])
        def edge_labels(J):
            return [next(iter(S[J[i]] & S[J[i+1]])) if False else labels[J[i] if (J[i+1]-J[i])%m==1 else J[i+1]] for i in range(len(J)-1)]
        a=edge_labels(J)
        if good(E):
            if P not in a:P=a[0]
            odd=[i for i in range(s) if i%2 and a[i]==P]
            if odd:p1,p2=odd[0],odd[0]+1
            elif a.index(P)>0:p1,p2=a.index(P)-1,a.index(P)
            elif max(i for i,x in enumerate(a) if x==P)<s-1:
                j=max(i for i,x in enumerate(a) if x==P);p1,p2=j+1,j+2
            else:p1,p2=1,s-1
        else:
            if P in S[E[-2]]:
                J=J[::-1];E=exterior(J);a=edge_labels(J)
            assert P not in S[E[-2]] and a[0]==P
            if a[-1]==P:p1,p2=1,s-1
            else:
                t=1+max(i for i,x in enumerate(a) if x==P)
                p1,p2=(1,t) if t%2==0 else (t,s-1)
        assert 0<p1<p2<s and p1%2==1 and p2%2==0
        arcs=[J[:p1+1],J[p1:p2+1],J[p2:],E]
        assert all(admissible(x) for x in arcs)
        gs=[good(x) for x in arcs];ls=[len(x)>2 for x in arcs]
        assert (gs[0] and gs[2]) or (gs[1] and gs[3])
        if ls[0] and ls[2]:assert gs[1] and gs[3]
        if ls[1] and ls[3]:assert gs[0] and gs[2]
        cells.append(tuple(x[0] for x in arcs))
        for a2 in arcs[:3]:recurse(a2)
    recurse(list(range(m)))
    assert len(cells)==(m-2)//2
    # Check signed cycle identity for arbitrary f by coefficient extraction.
    def norm(M):return tuple(sorted(tuple(sorted(e)) for e in M))
    O=[norm([(i,(i+1)%m) for i in range(e,m,2)]) for e in [0,1]]
    total=Counter()
    for corners in cells:
        # construction may return cells with reversed orientation
        corner_set=set(corners)
        cc=sorted(corner_set)
        arcs=[]
        for k,x in enumerate(cc):
            stop=cc[(k+1)%4];arc=[x]
            while arc[-1]!=stop:arc.append((arc[-1]+1)%m)
            arcs.append(arc)
        Ts=[norm([(a[i],a[i+1]) for i in range(0,len(a)-1,2)]) for a in arcs]
        Cs=[norm([(a[i],a[i+1]) for i in range(1,len(a)-2,2)]+[(a[0],a[-1])]) for a in arcs]
        through=[0 if set(T).issubset(set(O[0])) else 1 for T in Ts]
        terms=Counter()
        for e in [0,1]:
            js=[j for j in range(4) if through[j]==e]
            Y,X=js
            A0=set(O[e]);A1=(A0-set(Ts[Y]))|set(Cs[Y]);A2=(A1-set(Ts[X]))|set(Cs[X])
            # Delta has f(A_P)-f(A_Q)
            terms[norm(A2)]+=1 if e==0 else -1
            # context E = f(A1)-f(A2)-f(A0)+f(H_X)
            HX=(A0-set(Ts[X]))|set(Cs[X]);sgn=1 if e==0 else -1
            for M,sign in [(A1,1),(A2,-1),(A0,-1),(HX,1)]:terms[norm(M)]+=sgn*sign
        total.update(terms)
    target=Counter({O[0]:1,O[1]:-1})
    assert {k:v for k,v in total.items() if v}!={} # nontrivial identity
    assert {k:v for k,v in total.items() if v}==dict(target)
    counts['cases']+=1;counts['cells']+=len(cells)

for edges in [[(0,1),(1,2),(2,3)],[(0,1),(0,2),(0,3)]]:
    adj={i:{i} for i in range(4)}
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    for m in [4,6,8,10]:
        def gen(prefix):
            if len(prefix)==m:
                if prefix[0] in adj[prefix[-1]]:yield prefix
                return
            for v in sorted(adj[prefix[-1]]):yield from gen(prefix+[v])
        for start in range(4):
            for seq in gen([start]):check(seq,adj)
    counts['exhaustive_graphs']+=1
rng=Random(113)
for trial in range(2000):
    k=rng.randrange(2,9);adj={i:{i} for i in range(k)}
    for i in range(1,k):
        p=rng.randrange(i);adj[i].add(p);adj[p].add(i)
    # Closed even walk: a random half followed by its reverse, with random stays.
    walk=[rng.randrange(k)]
    for _ in range(rng.randrange(1,15)):walk.append(rng.choice(sorted(adj[walk[-1]])))
    seq=walk+walk[-2:0:-1]
    if len(seq)>=4:check(seq,adj);counts['random_cases']+=1
print(json.dumps(dict(counts),indent=2))
