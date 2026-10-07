"""Costed, checkable low-rank truncation after hard BCS projection.

The certificate is deliberately conservative. Every quantity is rational,
including its squared Lipschitz bound. Acquisition uses one fixed corner;
no SVD, favorable projected-norm oracle, or hidden rank decomposition.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import grassmann_bcs as g
import lowrank_bcs as lr
import band_lowrank_bcs as blr
from fractions import Fraction as Q
from itertools import combinations
import json
import random
import time

def certificate(F,G,k=None,epsilon=Q(1,100)):
    n=len(F)
    if not 0<epsilon<=1: raise ValueError('invalid epsilon')
    if k is not None and not 0<=k<=n//2: raise ValueError('invalid pair count')
    U,V=lr.factor(G)
    cs=lr.counts_factors(U,V)
    q2=sum(cs) if k is None else (cs[k] if k<len(cs) else Q(0))
    delta2=sum(g.abs2(g.add(F[i][j],g.neg(G[i][j])))
               for i in range(n) for j in range(n))
    def l1(A):
        return sum(abs(x[0])+abs(x[1]) for row in A for x in row)
    M=max(Q(1),l1(F),l1(G))
    ks=range(1,n//2+1) if k is None else ([k] if k else [])
    D2=delta2*sum(Q(j*j)*M**(2*(j-1)) for j in ks)
    limit=epsilon*epsilon*q2/64
    return {'accepted':q2>0 and D2<=limit,'rank':len(V),
            'pair_count':k,'epsilon':epsilon,'M':M,'residual_Frobenius_squared':delta2,
            'projected_norm_squared_G':q2,'state_error_squared_bound':D2,
            'acceptance_threshold':limit,'counts_G':cs,
            'relative_count_error_bound':epsilon/2,
            'Born_TV_bound':epsilon/4}

def acquire_and_certify(F,r,k=None,epsilon=Q(1,100)):
    S,U,V=blr.acquire_corner_split(F,r)
    G=lr.matmul(U,V)
    return G,certificate(F,G,k,epsilon)

def law(F,k=None):
    n=len(F)
    ws={}
    ks=range(n//2+1) if k is None else [k]
    for j in ks:
        for I in combinations(range(n),j):
            Is=set(I)
            for J in combinations([i for i in range(n) if i not in Is],j):
                w=g.abs2(g.determinant([[F[i][j] for j in J] for i in I]))
                if w: ws[(I,J)]=w
    z=sum(ws.values())
    return z,{s:w/z for s,w in ws.items()} if z else {}

def tv(p,q):
    return sum(abs(p.get(s,Q(0))-q.get(s,Q(0))) for s in p.keys()|q.keys())/2

def serial(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,list): return [serial(y) for y in x]
    if isinstance(x,dict): return {k:serial(v) for k,v in x.items()}
    return x

def test():
    t0=time.monotonic()
    n=6
    U=[[g.qc(1),g.qc(i+1)] for i in range(n)]
    V=[[g.qc((i+1)**a) for i in range(n)] for a in range(2)]
    G0=lr.matmul(U,V)
    t=Q(1,2**80)
    F=[list(row) for row in G0]
    # T=I+(E01+E10)/4 is positive definite, so F=G0+tT has full rank.
    for i in range(n): F[i][i]=g.add(F[i][i],g.qc(t))
    F[0][1]=g.add(F[0][1],g.qc(t/4))
    F[1][0]=g.add(F[1][0],g.qc(t/4))
    rows=[]
    for k in (2,None):
        G,c=acquire_and_certify(F,2,k,Q(1,100))
        assert c['accepted'] and c['rank']==2
        zF,pF=law(F,k)
        zG,pG=law(G,k)
        assert zG==c['projected_norm_squared_G']
        relative=abs(zF-zG)/zF
        distance=tv(pF,pG)
        assert relative<=c['relative_count_error_bound']
        assert distance<=c['Born_TV_bound']
        # Compare directly to the sharper 2D/sqrt(c_G) inequality, squared.
        assert distance*distance*c['projected_norm_squared_G'] <= 4*c['state_error_squared_bound']
        rows.append({'certificate':serial(c),'exact_relative_error':str(relative),
                     'exact_Born_TV':str(distance)})
    assert len(lr.factor(F)[1])==n
    # Instability even with k <= approximate rank: both matrices are exactly
    # rank one and within epsilon of the same rank-one diagonal matrix.
    discontinuity=[]
    for e in (Q(1,4),Q(1,256)):
        base=[[g.ONE,g.ZERO],[g.ZERO,g.ZERO]]
        A=[list(row) for row in base]
        B=[list(row) for row in base]
        A[0][1]=g.qc(e)
        B[1][0]=g.qc(e)
        za,pa=law(A,1)
        zb,pb=law(B,1)
        assert za==zb==e*e and tv(pa,pb)==1
        assert len(lr.factor(A)[1])==len(lr.factor(B)[1])==1
        # The certificate rejects the zero-norm common approximation.
        assert not certificate(A,base,1)['accepted']
        discontinuity.append({'epsilon':str(e),'rank':1,'pair_count':1,
                              'norm_squared':str(za),'TV':'1',
                              'common_approximation_rejected':True})
    sam=lr.sample(G,k=2,epsilon=Q(1,200),rng=random.Random(6190321))
    out={'status':'PASS','acquired_full_rank_example':{'n':n,'rank_F':n,
         'perturbation':str(t),'target_checks':rows},
         'rank_one_sector_instability':discontinuity,
         'sample_G':{'random_bits':sam['random_bits'],'TV_bound_to_G':sam['TV_bound'],
                     'occupation':sam['occupation']},
         'wall_seconds':time.monotonic()-t0,
         'scope':'Exact finite norm/law checks; perturbation and certificate derivation separate.'}
    Path(__file__).with_name('certified_truncation_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','rank_F':n,'rank_G':2,'targets':2,
                      'instability_cases':2,'sample_bits':sam['random_bits'],
                      'wall_seconds':out['wall_seconds']},indent=2))

if __name__=='__main__': test()
