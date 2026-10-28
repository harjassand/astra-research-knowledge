#!/usr/bin/env python3
"""Polynomial exact cubic matrix sum when BA=CB=AC=0.

All three sources may have growing rank and be nonzero. Count kernel/image
intersections by Gaussian coefficients, no subspace enumeration. Root proof.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from matrix_kloosterman import gaussian_table,matrix_ramanujan,Field,rref,mmul

def annihilating_cubic_from_ranks(n,a,ra,rb,rc):
    if a<1 or min(ra,rb,rc)<0 or max(ra+rb,rb+rc,rc+ra)>n:
        raise ValueError('impossible cyclic-annihilation rank data')
    q=1<<a;G=gaussian_table(n,q);total=0;strata=0
    def choose(x,y):return G[x][y] if 0<=y<=x<=n else 0
    for k in range(n-rb+1):
        r=n-k
        if r<rc:continue
        for u in range(min(ra,r-rc)+1):
            j=r-rc-u
            if not 0<=j<=n-rc-ra:continue
            images=choose(ra,u)*choose(n-rc-ra,j)*q**(u*(n-ra-r+u))
            for v in range(max(0,k-(n-rb-u)),min(k,u)+1):
                kernels=choose(u,v)*choose(n-rb-u,k-v)*q**((u-v)*(k-v))
                total+=images*kernels*q**(n*k)*matrix_ramanujan(r,u-v,q)
                strata+=1
    return q**(n*n)*total,dict(route='cyclic adjacent products zero',matrix_rank=n,
        field_degree=a,rank_A=ra,rank_B=rb,rank_C=rc,dimension_strata=strata,
        enumerated_subspaces=0)

def annihilating_cubic(A,B,C,h=3):
    F=Field(h)
    if any(x for M in (mmul(B,A,F),mmul(C,B,F),mmul(A,C,F)) for row in M for x in row):
        raise ValueError('requires BA=CB=AC=0')
    return annihilating_cubic_from_ranks(len(A),F.a,
        len(rref(A,F)[1]),len(rref(B,F)[1]),len(rref(C,F)[1]))

def checks():
    from matrix_kloosterman import all_matrices,mtrace,trace_product
    from singular_pair_probe import walsh
    F=Field(3);n=2;mats=list(all_matrices(n,F));N=3*n*n
    def enc(M):return sum(x<<(n*i+j) for i,row in enumerate(M) for j,x in enumerate(row))
    def enc_transpose(M):return sum(M[j][i]<<(n*i+j) for i in range(n) for j in range(n))
    phase=[0]*(1<<N)
    for X in mats:
        for Y in mats:
            XY=mmul(X,Y,F)
            for Z in mats:
                phase[enc(X)|(enc(Y)<<4)|(enc(Z)<<8)]=(-1)**trace_product(XY,Z,F)
    walsh(phase);checked=0;all_nonzero=0
    for A in mats:
        for B in mats:
            for C in mats:
                if any(x for M in (mmul(B,A,F),mmul(C,B,F),mmul(A,C,F)) for row in M for x in row):continue
                value,_=annihilating_cubic(A,B,C)
                expected=phase[enc_transpose(A)|(enc_transpose(B)<<4)|(enc_transpose(C)<<8)]
                assert value==expected,(A,B,C,value,expected)
                checked+=1;all_nonzero+=bool(enc(A) and enc(B) and enc(C))
    large=[]
    for n,a,ra,rb,rc in [(4,1,2,2,2),(64,1,32,32,32),(32,8,16,16,16)]:
        value,meta=annihilating_cubic_from_ranks(n,a,ra,rb,rc)
        large.append(dict(**meta,original_bits=3*a*n*n,gap_hex=hex(value),
                          ones_hex=hex(((1<<(3*a*n*n))-value)//2)))
    result=dict(exhaustive_source_triples=checked,all_nonzero_source_triples=all_nonzero,
                full_original_truth_inputs=1<<N,large=large)
    Path(__file__).with_name('annihilating_sources_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='large'},indent=2))

if __name__=='__main__':checks()
