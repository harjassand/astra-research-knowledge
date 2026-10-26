"""Independent Fraction-arithmetic stress of the stage1 tree theorem.

No stage1 imports/writes. Enumerated cases were frozen in STRESS_SPEC.md.
This checks the finite fixtures exactly; the all-real-domain proof is separate.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import time

OUT=Path(__file__).resolve().parent


def solve(a,b):
    n=len(b); z=[list(row)+[v] for row,v in zip(a,b)]
    for j in range(n):
        p=next(i for i in range(j,n) if z[i][j])
        z[j],z[p]=z[p],z[j]
        scale=z[j][j]
        z[j]=[v/scale for v in z[j]]
        for i in range(n):
            if i!=j and z[i][j]:
                scale=z[i][j]
                z[i]=[v-scale*w for v,w in zip(z[i],z[j])]
    return [row[-1] for row in z]


def laplacian(n,edges):
    a=[[F(0) for _ in range(n)] for _ in range(n)]
    for i,j,g in edges:
        if i<n:a[i][i]+=g
        if j<n:a[j][j]+=g
        if i<n and j<n:
            a[i][j]-=g;a[j][i]-=g
    return a


def moments(c,edges):
    a=laplacian(len(c),edges)
    h=solve(a,c)
    h2=solve(a,[2*x*y for x,y in zip(c,h)])
    return h[0],h2[0]-h[0]**2


def prufer_tree(seq,nv):
    deg=[1]*nv
    for v in seq:deg[v]+=1
    edges=[]
    for v in seq:
        leaf=next(i for i in range(nv) if deg[i]==1)
        edges.append((leaf,v));deg[leaf]-=1;deg[v]-=1
    left=[i for i in range(nv) if deg[i]==1]
    edges.append(tuple(left))
    return edges


def collapse(c,edges):
    n=len(c);adj=[[] for _ in range(n+1)]
    for i,j,g in edges:
        adj[i].append((j,1/g));adj[j].append((i,1/g))
    parent={n:None};pres={};stack=[n]
    while stack:
        i=stack.pop()
        for j,r in adj[i]:
            if j not in parent:
                parent[j]=i;pres[j]=r;stack.append(j)
    path=[];i=0
    while i!=n:path.append(i);i=parent[i]
    k_of={i:k for k,i in enumerate(path)}
    groups=[[] for _ in path]
    for i in range(n):
        j=i
        while j not in k_of and j!=n:j=parent[j]
        if j!=n:groups[k_of[j]].append(i)
    d=[sum((c[i] for i in group),F(0)) for group in groups]
    rr=[pres[i] for i in path]
    tails=[sum(rr[k:],F(0)) for k in range(len(rr))]
    rootpaths=[]
    for i in range(n):
        ss=set();j=i
        while j!=n:ss.add(j);j=parent[j]
        rootpaths.append(ss)
    extra=F(0)
    for k,group in enumerate(groups):
        for i in group:
            for j in group:
                gij=sum((pres[v] for v in rootpaths[i]&rootpaths[j]),F(0))
                hij=gij-tails[k]
                assert hij>=0
                extra+=2*tails[k]*c[i]*c[j]*hij
    collapsed_edges=[(i,i+1,1/r) for i,r in enumerate(rr)]
    return d,collapsed_edges,extra


def fixed_capacity_min_variance(c,mean):
    ss=[];tot=F(0)
    for x in c:tot+=x;ss.append(tot)
    z=1+sum(((b-a)/(b+a) for a,b in zip(ss[:-1],ss[1:])),F(0))
    return mean**2/z


def exact_attainer(n,q):
    cs=F(2,3)
    ss=[cs*q**k for k in range(n)]
    c=[ss[0]]+[b-a for a,b in zip(ss[:-1],ss[1:])]
    w=[F(q-1,q+1)]*n
    w[0]=w[-1]=F(q,q+1)
    z=sum(w,F(0));a=[v/z for v in w]
    r=[aa/s for aa,s in zip(a,ss)]
    edges=[(i,i+1,1/v) for i,v in enumerate(r)]
    mean,var=moments(c,edges)
    assert mean==1 and var==1/z
    assert all(v>0 for v in c+r)
    assert sum(c,F(0))/c[0]==q**(n-1)
    # The conventional GLS estimator uses precisely this covariance kernel.
    kernel=[[min(x,y)/max(x,y) for y in ss] for x in ss]
    raw=solve(kernel,[F(1)]*n)
    gls=[v/sum(raw,F(0)) for v in raw]
    assert gls==a
    return dict(n=n,q=q,capacity_ratio=q**(n-1),variance=str(var),
                source_capacity=str(cs),capacities=list(map(str,c)),
                resistances=list(map(str,r)),gls_weights=list(map(str,gls)))


if __name__=='__main__':
    start=time.perf_counter();rng=random.Random(17102602)
    counts=[];minimum_branch=F(0);max_branch=F(0)
    positive_branch=0;unreachable_cases=0
    for n in [2,3,4,5]:
        count=0
        for seq in product(range(n+1),repeat=n-1):
            topo=prufer_tree(seq,n+1)
            c=[F(rng.randint(1,7),rng.randint(1,5)) for _ in range(n)]
            edges=[(i,j,F(rng.randint(1,7),rng.randint(1,5))) for i,j in topo]
            mean,var=moments(c,edges)
            d,ee,extra=collapse(c,edges)
            cm,cv=moments(d,ee)
            assert mean==cm
            assert var-cv==extra and extra>=0
            assert cv>=fixed_capacity_min_variance(d,cm)
            if extra>0:positive_branch+=1
            if sum(d,F(0))<sum(c,F(0)):unreachable_cases+=1
            max_branch=max(max_branch,extra)
            count+=1
        counts.append(dict(storage_nodes=n,tree_topologies=count))
    attain=[exact_attainer(n,q) for n in range(2,13) for q in [2,3]]
    result=dict(seed=17102602,enumerated_topologies=counts,
                total_topologies=sum(x['tree_topologies'] for x in counts),
                all_exact_assertions_passed=True,
                positive_branch_variance_cases=positive_branch,
                irrelevant_bath_branch_cases=unreachable_cases,
                maximum_exact_branch_variance_penalty=str(max_branch),
                exact_attaining_designs=attain,
                wall_seconds=time.perf_counter()-start,
                scope='All labelled topologies through five storage nodes, one rational fixture each; 22 exact equality designs. Not exhaustive real parameters.')
    (OUT/'exact_stress_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='exact_attaining_designs'},indent=2))
