#!/usr/bin/env python3
"""Exact balance projections in translation-invariant one-hop Pauli sectors.
Only the diagonal-interaction block is tested; not the complete XXZ resolvent.
For prime ring size all nonconstant diagonal translation orbits have size n.
"""
import itertools
import sympy as s

def canon(A,n):
    return min(tuple(sorted((a+i)%n for a in A)) for i in range(n))

def sector(n,k):
    es=list(itertools.combinations(range(2,n),k-1))
    vs=sorted({canon(A,n) for A in itertools.combinations(range(n),k)})
    vi={v:i for i,v in enumerate(vs)}
    B=s.zeros(len(vs),len(es))
    for j,S in enumerate(es):
        B[vi[canon((*S,1),n)],j]+=1
        B[vi[canon((*S,0),n)],j]-=1
    L=B*B.T
    # Delete one gauge row. Since the quotient is connected this is invertible,
    # except k=1, for which the divergence matrix is zero.
    return es,B,L

def project(B,L,x):
    b=B*x
    if len(b)==1:return x
    u=s.zeros(len(b),1)
    u[:-1,0]=L[:-1,:-1].inv()*b[:-1,0]
    ans=x-B.T*u
    assert B*ans==s.zeros(B.rows,1)
    return ans

def run(n,maxk):
    es,B,L=sector(n,1)
    f=s.ones(1,1)
    for k in range(3,maxk+1,2):
        newes,BB,LL=sector(n,k)
        idx={v:i for i,v in enumerate(newes)}
        raw=s.zeros(len(newes),1)
        for S,c in zip(es,f):
            if 2 not in S and n-1 not in S:
                raw[idx[tuple(sorted((*S,2,n-1)))]]+=c
        f=project(BB,LL,raw)
        norm=s.factor((f.T*f)[0])
        print('n=',n,'k=',k,'vertices=',BB.rows,'edges=',BB.cols,
              'raw_norm2=',s.factor((raw.T*raw)[0]),'balanced_norm2=',norm,
              'nonzero=',sum(c!=0 for c in f),flush=True)
        if n<=7: print('coefficients:',list(zip(newes,f)),flush=True)
        assert norm>0
        es,B,L=newes,BB,LL

if __name__=='__main__':
    run(7,5)
    run(11,7)
