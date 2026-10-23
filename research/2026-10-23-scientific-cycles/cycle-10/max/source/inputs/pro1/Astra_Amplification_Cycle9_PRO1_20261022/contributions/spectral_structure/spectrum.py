"""Exact token construction of 2H; floating eigenvalues are diagnostics."""
from itertools import combinations
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
import json, time, sys

def words(k,n0,n1):
    for iz in combinations(range(k),n0):
        iz=set(iz); others=[a for a in range(k) if a not in iz]
        for ic in combinations(others,n1):
            ic=set(ic)
            yield tuple(0 if a in iz else 1 if a in ic else 2 for a in range(k))

def unmatched(x,start=0):
    pop=[];push=[]
    for a,z in enumerate(x,start):
        if z:push.append(a)
        elif push:push.pop()
        else:pop.append(a)
    return pop,push

def output(x,i,j,first):
    pp,pu=unmatched(x[:i]);mp,mu=unmatched(x[i+1:j],i+1)
    h,d=len(pu),len(mp)
    assert h>=d
    port=list(x);w=port[mu[0]] if mu else port[j]
    for a,b in zip(mu,mu[1:]+[j]):port[a]=port[b]
    port[j]=0
    stack=[x[a] for a in reversed(pu)]+[-1]*(len(x)+2)
    if first:
        stack.insert(d,w);port[i]=stack.pop(0)
    else:
        port[i]=stack.pop(0);stack.insert(d,w)
    for a in reversed(pu):port[a]=stack.pop(0)
    assert -1 not in port
    return tuple(port)

def matrix(k,n0,n1):
    w=list(words(k,n0,n1));lookup={x:i for i,x in enumerate(w)}
    row=[];col=[];data=[]
    for z,x in enumerate(w):
        for i in range(k):
            if x[i]:continue
            _,pu=unmatched(x[:i]);h=len(pu)
            for j in range(i+1,k):
                if not x[j]:continue
                mp,_=unmatched(x[i+1:j]);d=len(mp)
                if h<d:continue
                y=lookup[output(x,i,j,True)];c=1 if h==d else 2
                row.extend([y,z]);col.extend([z,y]);data.extend([c,c])
                if h>d:
                    y=lookup[output(x,i,j,False)]
                    row.extend([y,z]);col.extend([z,y]);data.extend([-2,-2])
    a=coo_matrix((data,(row,col)),shape=(len(w),len(w)),dtype=float).tocsr()
    a.eliminate_zeros()
    return a,w

def extremal(a):
    if not a.nnz:return 0.,0.
    if a.shape[0]<3:
        e=np.linalg.eigvalsh(a.toarray());return e[0]/2,e[-1]/2
    return eigsh(a,k=1,which='SA',return_eigenvectors=False,tol=1e-10)[0]/2,eigsh(a,k=1,which='LA',return_eigenvectors=False,tol=1e-10)[0]/2

def run(kmax):
    rows=[];t=time.perf_counter()
    for k in range(2,kmax+1):
        best=(-1,None);lo=(1,None)
        for n0 in range(k+1):
            for n1 in range((k-n0)//2+1):
                a,w=matrix(k,n0,n1);l,h=extremal(a)
                if h>best[0]:best=(h,(n0,n1,k-n0-n1))
                if l<lo[0]:lo=(l,(n0,n1,k-n0-n1))
                rows.append({'k':k,'counts':[n0,n1,k-n0-n1],'dimension':len(w),'min':l,'max':h})
        print(k,'min',lo,'max',best,'seconds',time.perf_counter()-t,flush=True)
    return {'rows':rows,'wall_seconds':time.perf_counter()-t,'scope':'Exact integer token matrix, numerical eigenvalues only'}

if __name__=='__main__':
    result=run(int(sys.argv[1]) if len(sys.argv)>1 else 8)
    open(__file__.replace('.py','.json'),'w').write(json.dumps(result,indent=2)+'\n')
