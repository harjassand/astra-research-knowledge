"""Sparse-support plus low-rank exact hard-BCS contraction.

S is explicit, F-S is exactly factored by lowrank_bcs.factor. All auxiliary
Grassmann variables survive until the end. The executable uses a width-
checked greedy order for S, retaining full complex interference.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import grassmann_bcs as g
import lowrank_bcs as lr
from fractions import Fraction as Q
import random
import json
import time

def counts(F,S,allowed=None,order=None,stats=None):
    n=len(F)
    if allowed is None: allowed=[{'0','u','d'} for _ in range(n)]
    if order is None: order=g.min_degree_order(S)
    w=g.width(S,order)
    R=[[g.add(F[i][j],g.neg(S[i][j])) for j in range(n)] for i in range(n)]
    U,V=lr.factor(R)
    r=len(V)
    if stats is None: stats={}
    stats.update({'support_width':w,'residual_rank':r,'products':0,'max_terms':0})
    factors=[]
    for i in range(n):
        A=3<<(4*i)
        B=12<<(4*i)
        p={}
        if '0' in allowed[i]: p[(A|B,0)]=g.ONE
        if 'u' in allowed[i]: p[(B,1)]=g.ONE
        if 'd' in allowed[i]: p[(A,0)]=g.ONE
        factors.append(({i},p))
    for i in range(n):
        for j in range(n):
            if S[i][j]==g.ZERO: continue
            e=g.product(g.linear_edge(4*i,4*j+3,S[i][j]),
                        g.linear_edge(4*j+2,4*i+1,g.neg(g.conj(S[i][j]))),stats)
            factors.append(({i,j},e))
    for i in range(n):
        for a in range(r):
            # Aux modes xi1_a and xi2_a occupy 4r generators after phys.
            b1=4*n+2*a
            p1=b1+1
            b2=4*n+2*r+2*a
            p2=b2+1
            terms=((4*i,p1,U[i][a]),
                   (4*i+2,p2,g.neg(g.conj(V[a][i]))),
                   (b1,4*i+3,g.neg(V[a][i])),
                   (b2,4*i+1,g.neg(g.conj(U[i][a]))))
            for x,y,c in terms:
                if c!=g.ZERO: factors.append(({i},g.linear_edge(x,y,c)))
    for i in order:
        bucket=[]
        rem=[]
        for sc,p in factors: (bucket if i in sc else rem).append((sc,p))
        bucket.sort(key=lambda f:len(f[1]))
        p={(0,0):g.ONE}
        sc=set()
        for s,q in bucket:
            sc |= s
            p=g.product(p,q,stats)
        m=15<<(4*i)
        q={}
        for (a,k),c in p.items():
            if a&m==m: g.put(q,(a^m,k),c)
        sc.discard(i)
        factors=rem+[(sc,q)]
    p={(0,0):g.ONE}
    for sc,q in factors:
        assert not sc
        p=g.product(p,q,stats)
    raw=[g.ZERO for _ in range(n//2+1)]
    for (m,k),c in p.items():
        assert not m & ((1<<(4*n))-1)
        a=m>>(4*n)
        if any((a>>(2*j))&3 not in (0,3) for j in range(2*r)): continue
        assert k<len(raw)
        raw[k]=g.add(raw[k],c)
    assert all(c[1]==0 and c[0]>=0 for c in raw)
    return [c[0] for c in raw]

def band_split(F,b):
    n=len(F)
    return [[F[i][j] if abs(i-j)<=b else g.ZERO for j in range(n)]
            for i in range(n)]

def inverse(B):
    r=len(B)
    A=[list(row)+[g.ONE if i==j else g.ZERO for j in range(r)]
       for i,row in enumerate(B)]
    for j in range(r):
        p=next((i for i in range(j,r) if A[i][j]!=g.ZERO),None)
        if p is None: raise ValueError('fixed corner minor is singular')
        A[j],A[p]=A[p],A[j]
        a=A[j][j]
        A[j]=[g.div(x,a) for x in A[j]]
        for i in range(r):
            if i==j: continue
            a=A[i][j]
            A[i]=[g.add(x,g.neg(g.mul(a,y))) for x,y in zip(A[i],A[j])]
    return [row[r:] for row in A]

def acquire_corner_split(F,r):
    """F-only split from its first r rows and last r columns.

    This is a computable admission rule, not a general algorithm to discover
    arbitrary sparse-plus-low-rank decompositions. Its support width is checked.
    """
    n=len(F)
    if not 1<=r<=n: raise ValueError('invalid corner rank')
    K=list(range(n-r,n))
    B=[[F[i][j] for j in K] for i in range(r)]
    Bi=inverse(B)
    U=[[F[i][j] for j in K] for i in range(n)]
    V=[]
    for a in range(r):
        row=[]
        for j in range(n):
            z=g.ZERO
            for b in range(r): z=g.add(z,g.mul(Bi[a][b],F[b][j]))
            row.append(z)
        V.append(row)
    R=lr.matmul(U,V)
    S=[[g.add(F[i][j],g.neg(R[i][j])) for j in range(n)] for i in range(n)]
    return S,U,V

def test():
    rng=random.Random(6190320)
    t0=time.monotonic()
    checks=prefix=0
    rows=[]
    for n in range(1,7):
        r=1 if n<4 else 2
        U=[[g.qc(rng.randrange(-1,2),Q(rng.randrange(-1,2),2))
            for a in range(r)] for i in range(n)]
        V=[[g.qc(rng.randrange(-1,2),Q(rng.randrange(-1,2),3))
            for i in range(n)] for a in range(r)]
        R=lr.matmul(U,V)
        S=[[g.ZERO for j in range(n)] for i in range(n)]
        for i in range(n):
            S[i][i]=g.qc(rng.randrange(-1,2))
            if i+1<n:
                S[i][i+1]=g.qc(Q(1,2),Q(1,3))
                S[i+1][i]=g.qc(-1,Q(1,4))
        F=[[g.add(S[i][j],R[i][j]) for j in range(n)] for i in range(n)]
        st={}
        p=counts(F,S,stats=st)
        assert p==g.brute_counts(F)
        checks+=1
        for rep in range(3):
            a=[{s for s in ('0','u','d') if rng.randrange(3)} for i in range(n)]
            assert counts(F,S,a)==g.brute_counts(F,a)
            prefix+=1
        rows.append({'n':n,'stats':st,'counts':[str(x) for x in p]})
    n=21
    S=[[g.ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n-1):
        S[i][i+1]=g.qc(1)
        S[i+1][i]=g.qc(-1)
    # Dense rank-one perturbation of a large-rank width-one matrix.
    F=[[g.add(S[i][j],g.qc(1)) for j in range(n)] for i in range(n)]
    st={}
    t1=time.monotonic()
    p=counts(F,S,stats=st)
    assert st['support_width']==1 and st['residual_rank']==1
    assert p[0]==1 and p[1]==sum(g.abs2(F[i][j]) for i in range(n)
                               for j in range(n) if i!=j)
    small=[row[:7] for row in F[:7]]
    ssmall=[row[:7] for row in S[:7]]
    assert counts(small,ssmall)==g.brute_counts(small)
    checks+=1
    benchmark={'n':n,'full_rank':len(lr.factor(F)[1]),'stats':st,
               'counts':[str(x) for x in p],'wall_seconds':time.monotonic()-t1}
    Sc,Uc,Vc=acquire_corner_split(F,1)
    stc={}
    pc=counts(F,Sc,stats=stc)
    assert pc==p
    acquired={'rule':'first one row and last one column, exact nonsingular corner',
              'stats':stc,'counts':[str(x) for x in pc]}
    out={'status':'PASS','exact_count_checks':checks,'exact_prefix_checks':prefix,
         'cases':rows,'dense_benchmark':benchmark,'acquired_corner':acquired,
         'wall_seconds':time.monotonic()-t0}
    Path(__file__).with_name('band_lowrank_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))

if __name__=='__main__': test()
