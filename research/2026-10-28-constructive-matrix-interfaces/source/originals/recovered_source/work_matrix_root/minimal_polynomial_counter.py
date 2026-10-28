#!/usr/bin/env python3
"""Complete matrix-cubic counts from an acquired minimal polynomial.

For acquired degree h the construction costs (t+1)^(6h+O(1))*poly(a).
This is polynomial for fixed h, not uniformly in h or for arbitrary
Boolean programs. No rank restriction is imposed on the counted inputs.
"""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent')]
from opposite_rank_pencils import (Field,direct_sum,eye,generalized_jordan,
    ManufacturedHomEpi,opposite_moments,rank_restricted_cubic_count)
from matrix_kloosterman import charpoly,factor_polynomial,primary_columns


def minimal_polynomial_types(D,F,maximum_rank=None):
    t=len(D);r=t if maximum_rank is None else maximum_rank
    if type(r) is not int or not 0<=r<=t:raise ValueError('valid rank depth required')
    factors=factor_polynomial(charpoly(D,F),F);primary=[];symbols=[];h=0
    for f,m in factors:
        f=tuple(f);columns=tuple(primary_columns(D,f,m,F));degree=len(f)-1;e=len(columns)
        h+=degree*e;index=len(primary);primary.append((f,columns))
        for power in range(1,min(e,r//degree)+1):
            symbols.append(('regular',index,power,degree*power,degree*power))
    for length in range(1,min(h-1,r)+1):symbols.append(('open',-1,length,length,length+1))
    types=[];multiplicities=[0]*len(symbols);used_columns=[[0]*len(cols) for f,cols in primary]

    def visit(position,u,c):
        if position==len(symbols):
            shapes=[[] for _ in primary];chains=[]
            for (kind,index,power,_,_),number in zip(symbols,multiplicities):
                if kind=='regular':shapes[index].extend([power]*number)
                else:chains.extend([power]*number)
            regular=[];blocks=[]
            for (f,cols),shape in zip(primary,shapes):
                if not shape:continue
                shape=tuple(sorted(shape,reverse=True));v=(len(f)-1)*sum(shape)
                regular.append((f,shape));blocks.append((v,v,eye(v),generalized_jordan(list(f),shape)))
            chains=tuple(sorted(chains,reverse=True))
            for k in chains:
                A=[[int(i==j) for j in range(k)] for i in range(k+1)]
                B=[[int(i==j+1) for j in range(k)] for i in range(k+1)]
                blocks.append((k,k+1,A,B))
            types.append(direct_sum(blocks,(tuple(regular),chains)));return
        kind,index,power,v,w=symbols[position]
        maximum=min((r-u)//v,(t-c)//w)
        if kind=='regular':
            maximum=min(maximum,*(primary[index][1][j]-used_columns[index][j] for j in range(power)))
        for number in range(maximum+1):
            multiplicities[position]=number
            if kind=='regular':
                for j in range(power):used_columns[index][j]+=number
            visit(position+1,u+number*v,c+number*w)
            if kind=='regular':
                for j in range(power):used_columns[index][j]-=number
        multiplicities[position]=0

    visit(0,0,0);types.sort(key=lambda R:(R.u+R.c,R.u,R.c,repr(R.label)))
    return types,dict(minimal_polynomial_degree=h,indecomposable_symbols=len(symbols),
        acquired_primary_columns=[dict(irreducible=list(f),columns=list(cols)) for f,cols in primary],
        maximum_rank=r,maximum_open_chain=min(h-1,r),listed_types=len(types),
        multiplicities_enumerated_directly=True,regular_submodule_caps_acquired=True,
        supplied_primary_decomposition=False)


def full_matrix_cubic_count(D,field_h,beta,phi=(),eta=0,padding=None):
    begun=time.perf_counter();F=Field(field_h);D=[list(row) for row in D];t=len(D)
    if not t or any(len(row)!=t or any(type(x) is not int or not 0<=x<F.q for x in row) for row in D):
        raise ValueError('explicit nonempty square operator over the supplied field required')
    types,acquisition=minimal_polynomial_types(D,F)
    backend=ManufacturedHomEpi(D,field_h,t,types)
    moments=opposite_moments(D,field_h,beta,phi,eta,t,backend)
    result=rank_restricted_cubic_count(moments,padding)
    T=result['padding'];expected_domain=F.q**(t*t+2*t*T)
    if result['restricted_domain_size']!=expected_domain:raise AssertionError('full-rank domain not reconstructed')
    result.pop('rank_cap');result['domain_size']=result.pop('restricted_domain_size')
    result.update(ones=result['satisfying_count'],full_unrestricted_matrix_domain=True,
        source_operator=D,beta=beta,eta=eta,trace_quadratic_anf=sorted(phi),
        field_polynomial=field_h,acquisition=acquisition,moment_result=moments,
        bit_time_bound='(t+1)^(6h+O(1))*poly(a) for acquired minimal-polynomial degree h',
        uniform_polynomial_in_h=False,seconds=time.perf_counter()-begun)
    return result
