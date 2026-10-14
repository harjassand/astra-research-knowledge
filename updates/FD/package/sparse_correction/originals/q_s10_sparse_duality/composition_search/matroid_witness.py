"""Explicit paired-affine-literal GF(2) counterexample, exact subspace counts.
One CPU, streamed subspaces; no expanded 2^94 truth table or ANF materialized.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as Q
from math import comb
import importlib.util,json,random,time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('scaling',HERE.parent/'tensor_scaling.py')
scaling=importlib.util.module_from_spec(spec);spec.loader.exec_module(scaling)


def subspaces(r):
    """Yield (dimension, bit mask of member vectors), each F2^r subspace once.
    Bases are reduced with distinct highest-bit pivots. Only lower nonpivot
    entries are free. This is the unique reduced echelon representation.
    """
    yield 0,1
    for d in range(1,r+1):
        for pivots in combinations(range(r),d):
            pset=set(pivots)
            free=[(i,j) for i,p in enumerate(pivots) for j in range(p) if j not in pset]
            base=[1<<p for p in pivots]
            for choice in range(1<<len(free)):
                basis=base[:]
                active=choice
                while active:
                    bit=active&-active;index=bit.bit_length()-1
                    i,j=free[index];basis[i]|=1<<j
                    active^=bit
                vectors=[0]
                for v in basis:vectors += [x^v for x in vectors]
                mask=0
                for x in vectors:mask|=1<<x
                assert mask.bit_count()==1<<d
                yield d,mask


def rank(cols):
    pivots={}
    for col in cols:
        x=col
        while x:
            p=x.bit_length()-1
            if p in pivots:x^=pivots[p]
            else:pivots[p]=x;break
    return len(pivots)


def gaussian(r,s):
    top=bottom=1
    for i in range(s):top*=2**r-2**i;bottom*=2**s-2**i
    return top//bottom


def exact_counts(r,columns):
    assert len(set(columns))==len(columns)
    assert all(0<x<1<<r for x in columns)
    assert rank(columns)==r
    D=len(columns)
    colmask=sum(1<<x for x in columns)
    B=P=0;dims=[0]*(r+1);counts_by_dim=[{} for _ in range(r+1)]
    for d,U in subspaces(r):
        dims[d]+=1
        n=(U&colmask).bit_count()
        counts_by_dim[d][n]=counts_by_dim[d].get(n,0)+1
        c=r-d;mu=(-1)**c*2**(c*(c-1)//2)
        P+=mu*2**n
        if n>=r:B+=mu*comb(n,r)
    assert dims==[gaussian(r,d) for d in range(r+1)]
    assert 0<B<=comb(D,r)
    assert B<=P<=2**D
    return dict(rank=r,D=D,columns=columns,bases=B,spanning_subsets=P,
        subspaces=sum(dims),subspaces_by_dimension=dims,
        subspace_column_count_histograms=counts_by_dim)


def small_truth_audit():
    r=2;cols=[1,2,3];D=len(cols);n=2*D
    coeff=[0]*(1<<n)
    rows=[]
    for v in range(1<<r):
        mask=sum(1<<(2*j+((a&v).bit_count()%2)) for j,a in enumerate(cols))
        rows.append(mask)
        s=mask
        while True:
            coeff[s]^=1
            if s==0:break
            s=(s-1)&mask
    vals=coeff[:]
    for i in range(n):
        for x in range(1<<n):
            if x>>i&1:vals[x]^=vals[x^(1<<i)]
    flip=sum(1<<(2*j) for j in range(D))
    T=[x for x,c in enumerate(coeff) if c]
    N=[x for x,c in enumerate(vals) if c]
    def swap(x):
        out=0
        for j in range(D):out|=((x>>(2*j)&1)<<(2*j+1))|((x>>(2*j+1)&1)<<(2*j))
        return out
    assert {swap(x) for x in T}==set(N)
    mins=[x for x in T if not any(z!=x and z&x==z for z in T)]
    counts=exact_counts(r,cols)
    assert len(T)==len(N)==(1<<r)*counts['spanning_subsets']==16
    assert len(mins)==(1<<r)*counts['bases']==12
    assert all(x.bit_count()==r for x in mins)
    assert sorted(rows)==[21,26,38,41]
    return dict(rank=r,columns=cols,outer_variables=n,Q_monomial_masks=rows,
        exact_truth_points=1<<n,m=len(T),k=len(N),minimum_terms=len(mins),
        minimum_degree=r,bases=counts['bases'],spanning_subsets=counts['spanning_subsets'])


def main():
    started=time.monotonic()
    rng=random.Random(20261013)
    columns=sorted(rng.sample(range(1,256),47))
    result=exact_counts(8,columns)
    r=result['rank'];D=result['D'];B=result['bases'];P=result['spanning_subsets']
    m=(1<<r)*P;n=2*D;W=B*(1<<n)
    proposals=Q(W,m)
    alpha=scaling.ratio_bounds(scaling.log_bounds(proposals),scaling.log_bounds(m))
    q=Q(m,1<<n)
    result.update(status='EXPLICIT_FINITE_GF2_COUNTEREXAMPLE_EXACT_SUBSPACE_COUNTS',
        coefficient_group='Z/2; every ANF coefficient listed by the unique-solution rule is 1',
        n=n,m=m,k=m,W=W,S=B,q=str(q),proposals=str(proposals),
        ratio_W_over_mk=str(Q(W,m*m)),
        alpha_interval=[scaling.decimal_endpoint(alpha[0]),scaling.decimal_endpoint(alpha[1],True)],
        actual_alpha_lower_float=float(alpha[0]),
        identity='m=k=2^r*P_A(1), W=B_A*2^(2D)',
        small_truth_audit=small_truth_audit(),
        expanded_truth_or_ANF_materialized=False,
        elapsed_seconds=time.monotonic()-started)
    assert m*m<W
    assert alpha[0]>Q(1189,1000)
    (HERE/'matroid_witness_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='subspace_column_count_histograms'},indent=2))

if __name__=='__main__':main()
