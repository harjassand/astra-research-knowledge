from itertools import combinations,product
from fractions import Fraction as F
import json

def cover_sets(m,edges):
    out=[]
    for mask in range(1<<m):
        C=frozenset(i for i in range(m)if mask>>i&1)
        if all(u in C or v in C for u,v in edges)and all(any((u==w and v not in C)or(v==w and u not in C)for u,v in edges)for w in C):out.append(C)
    return out

def forbidden(m,edges):
    es=set(edges)
    for k,pat in [(4,[0,2,2,2]),(5,[0,1,1,2,2])]:
        for sub in combinations(range(m),k):
            deg=[sum(tuple(sorted((u,v)))in es for v in sub if v!=u)for u in sub]
            if sorted(deg)==pat:return True
    return False

counts=dict(graphs=0,accepted=0,forbidden=0,capacity_states=0,heavy_absorptions=0,global_Q_bounds=0,sharp_forbidden_states=0)
by_size={}
for m in range(2,6):
    poss=list(combinations(range(m),2));local=0
    for mask in range(1,1<<len(poss)):
        edges=tuple(e for j,e in enumerate(poss)if mask>>j&1);es=set(edges);cs=cover_sets(m,edges)
        domination=all(all(any(tuple(sorted((w,z)))in es for z in (u,v))for w in range(m)if w not in C)for C in cs for u,v in edges if u in C and v in C)
        assert domination== (not forbidden(m,edges));counts['graphs']+=1;counts['accepted'if domination else'forbidden']+=1;local+=domination
        # Global packing bound for every graph; detailed heavy lemma for admitted graphs.
        for x in product(range(3),repeat=m):
            tau=min(sum(x[v]for v in C)for C in cs);Q=sum(x[u]*x[v]for u,v in edges)
            assert 4*len(edges)*Q>=tau*tau;counts['global_Q_bounds']+=1
            if not domination:continue
            counts['capacity_states']+=1
            opt=[C for C in cs if sum(x[v]for v in C)==tau]
            bad=[(u,v)for u,v in edges if any(u in C and v in C for C in opt)]
            qb=sum(x[u]*x[v]for u,v in bad);qg=Q-qb
            for A in (0,1,3):
                r=A+tau;heavy=[v for v in range(m)if x[v]>r];hb=sum(x[v]for v in heavy)
                if hb:assert qb*hb<=len(edges)*r*qg;counts['heavy_absorptions']+=1
        if not domination:
            found=None
            for size,pat in [(4,[0,2,2,2]),(5,[0,1,1,2,2])]:
                for sub in combinations(range(m),size):
                    deg=[sum(tuple(sorted((u,v)))in es for v in sub if v!=u)for u in sub]
                    if sorted(deg)==pat:found=(sub,deg,size);break
                if found:break
            assert found
            sub,deg,size=found;w=sub[deg.index(0)]
            for bulk in (7,10**6):
                x=[0]*m
                for v in sub:x[v]=1
                x[w]=bulk;tau=min(sum(x[v]for v in C)for C in cs)
                opt=[C for C in cs if sum(x[v]for v in C)==tau]
                qb=sum(x[u]*x[v]for u,v in edges if any(u in C and v in C for C in opt))
                qg=sum(x[u]*x[v]for u,v in edges)-qb
                assert (tau,qb,qg)==((2,3,0)if size==4 else(2,1,2))
                counts['sharp_forbidden_states']+=1
        # The forbidden patterns themselves remain stable unit-rate product-form controls.
    by_size[str(m)]=local
print(json.dumps(dict(status='PASS',scope='Finite exact corroboration; graph and count lemmas have ordinary proofs',counts=counts,accepted_by_size=by_size,no_simulation=True),indent=2))
