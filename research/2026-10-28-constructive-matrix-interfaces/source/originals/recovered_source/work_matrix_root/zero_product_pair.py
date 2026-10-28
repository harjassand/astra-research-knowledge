#!/usr/bin/env python3
"""Exact K(A,B) when AB=0 or BA=0, by polynomial dimension strata.
No rank bound, subspace enumeration, or supplied decomposition. Root derivation.
"""
from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from matrix_kloosterman import gaussian_table,matrix_ramanujan,Field,rref,mmul

def zero_product_pair_from_ranks(n,a,rank_A,rank_B,rank_AB,rank_BA):
    if a<1 or not 0<=rank_A<=n or not 0<=rank_B<=n: raise ValueError('invalid input ranks')
    if rank_BA:
        if rank_AB: raise ValueError('requires one vanishing ordered product')
        rank_A,rank_B=rank_B,rank_A;rank_AB,rank_BA=rank_BA,rank_AB
    if rank_A+rank_B>n or not 0<=rank_AB<=min(rank_A,rank_B):
        raise ValueError('impossible ranks for a zero ordered product')
    q=1<<a;b=rank_B;h=n-rank_A;w=b-rank_AB
    if not 0<=w<=min(b,h):raise ValueError('impossible intersection data')
    G=gaussian_table(n,q)
    def choose(u,v):return G[u][v] if 0<=v<=u<=n else 0
    total=0;strata=0
    for k in range(h+1):
        r=n-k
        if r<b:continue
        for s in range(max(0,k-h+w),min(k,w)+1):
            kernels=choose(w,s)*choose(h-w,k-s)*q**((w-s)*(k-s))
            for j in range(s,min(k,r)+1):
                z=r-b-j+s
                if z<0:continue
                images=choose(k-s,j-s)*choose(n-b-k+s,z)*q**((k-j)*z)
                if images:
                    total+=kernels*images*q**(n*k)*matrix_ramanujan(r,r-j,q);strata+=1
    return total,dict(route='one ordered product zero',matrix_rank=n,field_degree=a,
        rank_A=rank_A,rank_B=rank_B,rank_AB=rank_AB,rank_BA=rank_BA,
        image_B_intersect_kernel_A=w,dimension_strata=strata,enumerated_subspaces=0)

def zero_product_pair(A,B,h=3):
    F=Field(h)
    return zero_product_pair_from_ranks(len(A),F.a,len(rref(A,F)[1]),len(rref(B,F)[1]),
        len(rref(mmul(A,B,F),F)[1]),len(rref(mmul(B,A,F),F)[1]))

def checks():
    import numpy as np
    from matrix_kloosterman import all_matrices,minverse,trace_product
    start=time.perf_counter();rows=[]
    archive=np.load(ROOT/'work_norm_frontier_agent'/'pair_spectrum_n3.npz')
    print('archive keys',list(archive.keys()),flush=True)
    spectrum=archive['spectrum'] if 'spectrum' in archive else archive[list(archive.keys())[0]]
    n=3;F=Field(3);mats=list(all_matrices(n,F));checked=0
    def encode(M):return sum(x<<(i*n+j) for i,row in enumerate(M) for j,x in enumerate(row))
    ranks={encode(M):len(rref(M,F)[1]) for M in mats}
    for A in mats:
        aa=encode(A)
        for B in mats:
            bb=encode(B);ab=encode(mmul(A,B,F));ba=encode(mmul(B,A,F))
            if ab and ba:continue
            val,_=zero_product_pair_from_ranks(n,1,ranks[aa],ranks[bb],ranks[ab],ranks[ba])
            exp=int(spectrum[aa|(bb<<9)])
            assert val==exp,(A,B,val,exp);checked+=1
    rows.append(dict(n=3,a=1,all_admitted_source_pairs=checked))
    F=Field(7);n=2;gl=[]
    for X in all_matrices(n,F):
        Y=minverse(X,F)
        if Y is not None:gl.append((X,Y))
    A=[[1,0],[0,0]];checked=0
    for B in all_matrices(n,F):
        if any(x for row in mmul(A,B,F) for x in row) and any(x for row in mmul(B,A,F) for x in row):continue
        exp=sum((-1)**F.trace(trace_product(A,X,F)^trace_product(B,Y,F)) for X,Y in gl)
        val,_=zero_product_pair(A,B,7)
        assert val==exp,(B,val,exp);checked+=1
    rows.append(dict(n=2,a=2,admitted_B_for_projection=checked,GL_oracle_matrices=len(gl)))
    large=[]
    for n,a,ra,rb,rab in [(64,1,32,32,0),(32,8,16,16,0),(64,4,16,32,16)]:
        val,meta=zero_product_pair_from_ranks(n,a,ra,rb,rab,0)
        large.append(dict(**meta,value_hex=hex(val),answer_bits=abs(val).bit_length()))
    result=dict(checks=rows,large=large,seconds=time.perf_counter()-start)
    Path(__file__).with_name('zero_product_pair_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(checks=rows,seconds=result['seconds']),indent=2))

if __name__=='__main__':checks()
