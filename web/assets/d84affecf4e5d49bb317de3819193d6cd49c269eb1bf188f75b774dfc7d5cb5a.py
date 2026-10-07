"""Exact hard-BCS counts in O(poly(n,r)*16**r) rational arithmetic.

F=U V is acquired by rational-complex elimination. The counter retains only
4r auxiliary Grassmann generators, and all local 0/u/d prefixes are legal.
The original frozen grassmann_bcs.py supplies independent primitive arithmetic
and direct minor enumeration; its algorithm and initial artifacts are unchanged.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import grassmann_bcs as g
from fractions import Fraction as Q
from itertools import combinations
import random
import json
import time

def factor(F):
    """Return U,V such that F=UV, with r=rank F; exact Q(i) arithmetic."""
    n=len(F)
    A=[list(row) for row in F]
    # RREF augmented with identity records the invertible left row map E.
    E=[[g.ONE if i==j else g.ZERO for j in range(n)] for i in range(n)]
    pivots=[]
    i=0
    for j in range(n):
        p=next((p for p in range(i,n) if A[p][j]!=g.ZERO),None)
        if p is None:
            continue
        if p!=i:
            A[p],A[i]=A[i],A[p]
            E[p],E[i]=E[i],E[p]
        a=A[i][j]
        A[i]=[g.div(x,a) for x in A[i]]
        E[i]=[g.div(x,a) for x in E[i]]
        for p in range(n):
            if p==i or A[p][j]==g.ZERO:
                continue
            a=A[p][j]
            A[p]=[g.add(x,g.neg(g.mul(a,y))) for x,y in zip(A[p],A[i])]
            E[p]=[g.add(x,g.neg(g.mul(a,y))) for x,y in zip(E[p],E[i])]
        pivots.append(j)
        i += 1
        if i==n: break
    r=len(pivots)
    U=[[F[i][j] for j in pivots] for i in range(n)]
    # Pivot columns of RREF are e_a; hence the first r RREF rows give V.
    V=[A[a][:] for a in range(r)]
    for i in range(n):
        for j in range(n):
            z=g.ZERO
            for a in range(r): z=g.add(z,g.mul(U[i][a],V[a][j]))
            assert z==F[i][j]
    return U,V

def local_messages(U,V,allowed=None):
    n=len(U)
    r=len(V)
    if allowed is None: allowed=[{'0','u','d'} for _ in range(n)]
    out=[]
    for i in range(n):
        p={}
        if '0' in allowed[i]: p[(0,0)]=g.ONE
        for a in range(r):
            for b in range(r):
                if 'u' in allowed[i]:
                    # z U_ia conjugate(U_ib) bar-xi2_b xi1_a.
                    # Sorted aux indices are psi1_a,bar2_b, giving a minus.
                    mask=(1<<(2*a+1))|(1<<(2*r+2*b))
                    g.put(p,(mask,1),g.neg(g.mul(U[i][a],g.conj(U[i][b]))))
                if 'd' in allowed[i]:
                    # - V_ai conjugate(V_bi) bar-xi1_a xi2_b.
                    mask=(1<<(2*a))|(1<<(2*r+2*b+1))
                    g.put(p,(mask,0),g.neg(g.mul(V[a][i],g.conj(V[b][i]))))
        out.append(p)
    return out

def counts_factors(U,V,allowed=None,stats=None):
    n=len(U)
    r=len(V)
    if stats is None: stats={}
    stats.update({'rank':r,'products':0,'max_terms':0})
    p={(0,0):g.ONE}
    for q in local_messages(U,V,allowed):
        p=g.product(p,q,stats)
    raw=[g.ZERO for _ in range(min(r,n//2)+1)]
    # Integrating the aux diagonal exponential fills every missing full mode
    # pair. A one-generator mode occupancy can never be completed.
    for (mask,k),c in p.items():
        if any((mask>>(2*a))&3 not in (0,3) for a in range(2*r)):
            continue
        assert k<len(raw)
        raw[k] = g.add(raw[k],c)
    assert all(x[1]==0 for x in raw)
    out=[x[0] for x in raw]
    assert all(x>=0 for x in out)
    return out

def counts(F,allowed=None,stats=None):
    U,V=factor(F)
    return counts_factors(U,V,allowed,stats)

def sample(F,k=None,epsilon=Q(1,1000),rng=None):
    n=len(F)
    U,V=factor(F)
    r=len(V)
    if rng is None: rng=random.SystemRandom()
    if not 0 < epsilon <= 1: raise ValueError('invalid epsilon')
    if k is not None and not 0<=k<=min(r,n//2):
        raise ValueError('pair count out of range')
    allowed=[{'0','u','d'} for _ in range(n)]
    def mass(t):
        p=counts_factors(U,V,t)
        return sum(p) if k is None else p[k]
    z=mass(allowed)
    if z==0: raise ValueError('exact zero sector')
    D=1
    B=0
    while D < 2*max(n,1)/epsilon:
        D*=2
        B+=1
    state=[]
    trace=[]
    for i in range(n):
        ws=[]
        for s in ('0','u','d'):
            allowed[i]={s}
            ws.append(mass(allowed))
        assert sum(ws)==z
        cum=Q(0)
        bounds=[0]
        for a in ws[:-1]:
            cum+=a
            x=D*cum/z
            bounds.append(x.numerator//x.denominator)
        bounds.append(D)
        x=rng.getrandbits(B)
        j=next(j for j in range(3) if bounds[j]<=x<bounds[j+1])
        allowed[i]={('0','u','d')[j]}
        state.append(('0','u','d')[j])
        trace.append({'site':i,'weights':[str(w) for w in ws],
                      'bounds':bounds,'branch':state[-1]})
        z=ws[j]
    assert state.count('u')==state.count('d')
    if k is not None: assert state.count('u')==k
    return {'rank':r,'pair_count':state.count('u'),'occupation':state,
            'random_bits':n*B,'TV_bound':str(Q(2*n,D)),'trace':trace}

def matmul(U,V):
    n=len(U)
    r=len(V)
    F=[]
    for i in range(n):
        row=[]
        for j in range(n):
            z=g.ZERO
            for a in range(r): z=g.add(z,g.mul(U[i][a],V[a][j]))
            row.append(z)
        F.append(row)
    return F

def test():
    rng=random.Random(6190312)
    t0=time.monotonic()
    rows=[]
    ncount=nprefix=0
    for n in range(1,8):
        for r in range(min(3,n)+1):
            U=[[g.qc(Q(rng.randrange(-2,3),rng.randrange(1,4)),
                      Q(rng.randrange(-1,2),rng.randrange(1,4)))
                for a in range(r)] for i in range(n)]
            V=[[g.qc(Q(rng.randrange(-2,3),rng.randrange(1,4)),
                      Q(rng.randrange(-1,2),rng.randrange(1,4)))
                for i in range(n)] for a in range(r)]
            F=matmul(U,V)
            st={}
            p=counts(F,stats=st)
            b=g.brute_counts(F)
            assert p + [Q(0)]*(len(b)-len(p)) == b
            ncount+=1
            # Also check the original nonminimal rank factorization.
            q=counts_factors(U,V)
            assert q + [Q(0)]*(len(b)-len(q)) == b
            ncount+=1
            for rep in range(3):
                allowed=[{s for s in ('0','u','d') if rng.randrange(3)}
                         for _ in range(n)]
                q=counts_factors(U,V,allowed)
                b=g.brute_counts(F,allowed)
                assert q+[Q(0)]*(len(b)-len(q))==b
                nprefix+=1
            rows.append({'n':n,'input_factor_rank':r,'stats':st,
                         'counts':[str(x) for x in p]})
    # Dense connected nonbipartite F, fixed acquired rank 3, n=25.
    n=25
    r=3
    U=[[g.qc(1),g.qc(i+1),g.qc((i+1)**2)] for i in range(n)]
    V=[[g.qc((i+1)**a) for i in range(n)] for a in range(r)]
    F=matmul(U,V)
    st={}
    t1=time.monotonic()
    p=counts(F,stats=st)
    assert st['rank']==3
    c1=sum(g.abs2(F[i][j]) for i in range(n) for j in range(n) if i!=j)
    assert p[0]==1 and p[1]==c1
    # Independently enumerate all 3-by-3 minors for n=9, where rank 3 is
    # maximal but component size and graph treewidth already exceed r.
    small=[row[:9] for row in F[:9]]
    q=counts(small)
    b=g.brute_counts(small)
    assert q+[Q(0)]*(len(b)-len(q))==b
    benchmark={'n':n,'stats':st,'counts':[str(x) for x in p],
               'wall_seconds':time.monotonic()-t1}
    sam=sample(F,k=3,epsilon=Q(1,1000),rng=rng)
    result={'status':'PASS','exact_count_checks':ncount+1,
            'exact_prefix_checks':nprefix,'cases':rows,'dense_benchmark':benchmark,
            'canonical_sample':sam,'wall_seconds':time.monotonic()-t0,
            'scope':'Finite exact tests; proof and uniform bit bound are separate.'}
    out=Path(__file__).with_name('lowrank_checks.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'exact_count_checks':ncount+1,
                      'exact_prefix_checks':nprefix,'dense_benchmark':benchmark,
                      'sample_random_bits':sam['random_bits'],
                      'sample_TV_bound':sam['TV_bound'],
                      'wall_seconds':result['wall_seconds']},indent=2))

if __name__=='__main__': test()
