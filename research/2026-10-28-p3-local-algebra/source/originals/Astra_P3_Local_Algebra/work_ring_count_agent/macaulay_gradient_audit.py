#!/usr/bin/env python3
"""Independent algebraic audit of raw affine-center acquisition."""
from smooth_ring_counter import *
from itertools import combinations
from pathlib import Path
import random,json


def exponents(degree): return [(i,j,degree-i-j) for i in range(degree+1) for j in range(degree+1-i)]

def field_eliminate(matrix,h,width=None):
    a=[list(r) for r in matrix]; width=len(a[0]) if width is None and a else (width or 0)
    row=0; pivots=[]; q=1<<(h.bit_length()-1)
    for j in range(width):
        pivot=next((i for i in range(row,len(a)) if a[i][j]),None)
        if pivot is None: continue
        a[row],a[pivot]=a[pivot],a[row]
        inv=gf_pow(a[row][j],q-2,h); a[row]=[gf_mul(x,inv,h) for x in a[row]]
        for i in range(len(a)):
            if i!=row and a[i][j]:
                c=a[i][j]; a[i]=[x^gf_mul(c,y,h) for x,y in zip(a[i],a[row])]
        pivots.append(j); row+=1
    return a,pivots

def gradient(H):
    out=[]
    for i in range(3):
        p={}
        for ex,c in H.items():
            if ex[i]&1:
                e=list(ex); e[i]-=1; p[tuple(e)]=c
        out.append(p)
    return out

def macaulay_rank(H,h):
    mons=exponents(4); lookup={e:i for i,e in enumerate(mons)}; rows=[]
    for g in gradient(H):
        for shift in exponents(2):
            row=[0]*15
            for e,c in g.items(): row[lookup[tuple(x+y for x,y in zip(e,shift))]]^=c
            rows.append(row)
    _,piv=field_eliminate(rows,h)
    return len(piv)

def fvalue(p,vals,h):
    ans=0
    for e,c in p.items():
        v=c
        for x,k in zip(vals,e): v=gf_mul(v,gf_pow(x,k,h),h)
        ans^=v
    return ans

def qfeatures(v,h):
    return [1]+list(v)+[gf_mul(x,x,h) for x in v]+[gf_mul(v[i],v[j],h) for i,j in combinations(range(3),2)]

def fit_gradient(H,center,h):
    d=h.bit_length()-1; mask=(1<<d)-1; points=[0]+[1<<i for i in range(3*d)]
    points+=[(1<<i)|(1<<j) for i,j in combinations(range(3*d),2)]
    values=[tuple((p>>(i*d))&mask for i in range(3)) for p in points]
    basis=[qfeatures(v,h) for v in values]; all_coeff=[]
    for g in gradient(H):
        rhs=[fvalue(g,[x^a for x,a in zip(v,center)],h) for v in values]
        matrix=[f+[y] for f,y in zip(basis,rhs)]; reduced,piv=field_eliminate(matrix,h,10)
        assert len(piv)==10
        assert not any(not any(row[:10]) and row[10] for row in reduced)
        coeff=[0]*10
        for row,j in zip(reduced,piv): coeff[j]=row[10]
        all_coeff.append(coeff)
    mu=H[(1,1,1)]; inv=gf_pow(mu,(1<<d)-2,h); got=[None]*3
    for i in range(3): assert all_coeff[i][1+i]==0
    for i,j in combinations(range(3),2):
        assert all_coeff[i][1+j]==all_coeff[j][1+i]
        got[3-i-j]=gf_mul(inv,all_coeff[i][1+j],h)
    assert got==center
    reconstructed={(1,1,1):mu}
    for i in range(3):
        for j in range(3):
            e=[0]*3; e[i]+=1; e[j]+=2
            if all_coeff[i][4+j]: reconstructed[tuple(e)]=all_coeff[i][4+j]
    assert reconstructed=={e:c for e,c in H.items() if c}
    return all_coeff

def main():
    rng=random.Random(202610272245); checks=0; distribution={}; failures=[]
    others=[m for m in CUBICS if m!=(1,1,1)]
    for bits in range(1<<len(others)):
        H={(1,1,1):1}; H.update({m:1 for j,m in enumerate(others) if bits>>j&1})
        rank=macaulay_rank(H,3); smooth=projective_smooth(H,3)
        assert (rank==15)==smooth
        distribution[str(rank)]=distribution.get(str(rank),0)+1; checks+=1
    fields=[]; centers=0
    for h in (7,11,19):
        q=1<<(h.bit_length()-1); good=0
        for _ in range(80):
            H={m:rng.randrange(q) for m in CUBICS}; H[(1,1,1)]=rng.randrange(1,q)
            H={m:c for m,c in H.items() if c}
            rank=macaulay_rank(H,h); smooth=projective_smooth(H,h)
            assert (rank==15)==smooth
            checks+=1
            if smooth:
                center=[rng.randrange(q) for _ in range(3)]
                coeff=fit_gradient(H,center,h); centers+=1; good+=1
        fields.append(dict(h=h,random_cubics=80,centers_acquired=good))
    # The d=1 ambiguity is an actual rank defect in the proposed fit space.
    q2matrix=[qfeatures(tuple((u>>i)&1 for i in range(3)),3) for u in range(8)]
    _,q2piv=field_eliminate(q2matrix,3)
    assert len(q2piv)==7
    out=dict(macaulay_vs_buchberger=checks,binary_rank_distribution=distribution,
             random_fields=fields,gradient_centers=centers,
             residue_degree_one_fit_rank=len(q2piv),residue_degree_one_required_columns=10)
    Path(__file__).with_name('macaulay_gradient_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out)
if __name__=='__main__': main()
