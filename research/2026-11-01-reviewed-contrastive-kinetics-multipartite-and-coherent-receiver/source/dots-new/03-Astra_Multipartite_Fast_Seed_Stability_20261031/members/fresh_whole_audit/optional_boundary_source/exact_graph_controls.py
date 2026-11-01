#!/usr/bin/env python3
from itertools import combinations,product
import json

def parts(n,edges):
    E={frozenset(e)for e in edges};missing={i:{j for j in range(n)if i!=j and frozenset((i,j))not in E}for i in range(n)}
    seen=set();groups=[]
    for i in range(n):
        if i in seen:continue
        seen.add(i);todo=[i];g=[]
        while todo:
            v=todo.pop();g.append(v)
            for w in missing[v]:
                if w not in seen:seen.add(w);todo.append(w)
        groups.append(tuple(sorted(g)))
    okay=len(groups)>=2 and all(frozenset((i,j))not in E for g in groups for i,j in combinations(g,2))
    return okay,groups

def run():
    graphs=admitted=capacity_checks=witnesses=large_checks=0;by_n=[]
    for n in range(2,6):
        possible=list(combinations(range(n),2));ng=na=nw=0
        for mask in range(1,1<<len(possible)):
            edges=[e for j,e in enumerate(possible)if mask>>j&1];E={frozenset(e)for e in edges};okay,partition=parts(n,edges)
            witness=next(((u,v,w)for u,v in edges for w in range(n)if w not in (u,v)and frozenset((u,w))not in E and frozenset((v,w))not in E),None)
            assert okay==(witness is None)
            graphs+=1;ng+=1
            if okay:
                admitted+=1;na+=1
                for x in product(range(3),repeat=n):
                    Q=sum(x[i]*x[j]for i,j in edges)
                    if Q:
                        assert Q>=sum(x)-1;capacity_checks+=1
            else:
                witnesses+=1;nw+=1;u,v,w=witness
                for N in [1,10,10**30]:
                    x=[0]*n;x[u]=x[v]=1;x[w]=N
                    assert sum(x[i]*x[j]for i,j in edges)==1 and sum(x)==N+2;large_checks+=1
        by_n.append(dict(n=n,nonempty_graphs=ng,multipartite=na,constant_clock_witnesses=nw))
    assert graphs==1094 and admitted==70 and witnesses==1024
    return dict(status='PASS',nonempty_graphs=graphs,admitted_multipartite_graphs=admitted,
       active_integer_capacity_checks=capacity_checks,explicit_forbidden_witnesses=witnesses,
       exact_large_bulk_witness_checks=large_checks,by_vertices=by_n,
       no_simulation=True,no_stability_inferred_from_graph_rejection=True)
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
