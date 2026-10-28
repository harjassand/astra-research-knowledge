#!/usr/bin/env python3
"""Independent exact validation of the acquired invariant quadratic branch."""
from pathlib import Path
import json,random,time
from invariant_quadratic_matrix import (Field,invariant_quadratic_gap,
    compile_raw_invariant_quadratic,quadratic_anf,polynomial_value)
from raw_matrix_checks import native_anf
from field_descent import extract_anf,linear_apply,random_invertible

def matrix(packed,t,a):
    mask=(1<<a)-1
    return [[(packed>>(a*(i*t+j)))&mask for j in range(t)] for i in range(t)]

def xor(values):
    out=0
    for v in values:out^=v
    return out

def multiply(A,B,F):
    t=len(A)
    return [[xor(F.mul(A[i][k],B[k][j]) for k in range(t)) for j in range(t)] for i in range(t)]

def source_value(X,F,beta,qpoly):
    t=len(X);trace=xor(X[i][i] for i in range(t));second=0
    for i in range(t):
        for j in range(i+1,t):second^=F.mul(X[i][i],X[j][j])^F.mul(X[i][j],X[j][i])
    return polynomial_value(qpoly,trace)^F.trace(F.mul(beta,second))

def rank(X,F):
    X=[row[:] for row in X];n=len(X);r=0
    for j in range(n):
        p=next((i for i in range(r,n) if X[i][j]),None)
        if p is None:continue
        X[r],X[p]=X[p],X[r];inv=F.pow(X[r][j],F.q-2)
        X[r]=[F.mul(inv,v) for v in X[r]]
        for i in range(r+1,n):
            factor=X[i][j]
            if factor:X[i]=[u^F.mul(factor,v) for u,v in zip(X[i],X[r])]
        r+=1
    return r

def independent_rank_oracle(t,h,beta,qpoly,D=None):
    """Explicit X enumeration and exact Y/Z sum; exponential validation."""
    F=Field(h);total=0;d=F.a*t*t
    for packed in range(1<<d):
        X=matrix(packed,t,F.a);r=rank(X,F);U=multiply(D,X,F) if D is not None else X
        total+=(1-2*source_value(U,F,beta,qpoly))*(1<<(F.a*t*(t-r)))
    return total<<d

def run():
    begun=time.perf_counter();backend=[];rawcases=[]
    for t,h,beta,qpoly in [(2,3,1,set()),(2,3,1,{0,1}),
        (3,3,1,set()),(3,3,1,{1}), (4,3,1,{0,1}),
        (2,7,2,{3}),(2,11,3,{1,6}),(3,7,2,{1,2})]:
        expected=independent_rank_oracle(t,h,beta,qpoly)
        actual,meta=invariant_quadratic_gap(t,h,beta,qpoly)
        assert actual==expected,(t,h,beta,qpoly,actual,expected)
        backend.append(dict(matrix_size=t,field_modulus=h,beta=beta,
            trace_quadratic_anf=sorted(qpoly),gap=actual,independent_X_count=1<<(Field(h).a*t*t)))
        print('backend',t,h,actual,flush=True)
    for t,h,beta,qpoly,seed in [(2,3,1,{0,1},9340),(2,7,2,{3},9341),
        (3,3,1,set(),9342),(4,3,1,{0,1},9343),(3,7,2,{0,3},9344)]:
        F=Field(h);d=F.a*t*t;Z=[[0]*t for _ in range(t)]
        D=[[int(i==j) for j in range(t)] for i in range(t)];D[0][1]=1
        base,n=native_anf(t,h,Z,Z,Z)
        qnative=quadratic_anf(lambda x:source_value(multiply(D,matrix(x,t,F.a),F),F,beta,qpoly),d)
        base^=qnative
        rng=random.Random(seed);P=random_invertible(n,rng);offset=rng.randrange(1<<n)
        raw=extract_anf(lambda x:polynomial_value(base,linear_apply(P,x)^offset),n)
        answer=compile_raw_invariant_quadratic(raw,n)
        expected=independent_rank_oracle(t,h,beta,qpoly,D)
        assert answer['gap']==expected,(t,h,answer,expected)
        rawcases.append(dict(matrix_size=t,field_modulus=h,beta=beta,trace_quadratic_anf=sorted(qpoly),
            seed=seed,distinguished_unit=D,raw_anf=sorted(raw),affine_columns=P,
            affine_offset=offset,production_result=answer,
            independent_gap=expected,independent_X_count=1<<d))
        print('raw',n,answer['ones'],answer['stats']['polar_rank'],
              answer['stats']['unit_acquisition_route'],answer['stats']['seconds'],flush=True)
    t=3;F=Field(3);Z=[[0]*t for _ in range(t)]
    native,n=native_anf(t,3,Z,Z,Z)
    native^=quadratic_anf(lambda x:source_value(matrix(x,t,1),F,1,set()),t*t)
    native.symmetric_difference_update({(1<<0)|(1<<1)})
    try:compile_raw_invariant_quadratic(native,n)
    except ValueError as error:rejection=str(error)
    else:raise AssertionError('deliberately unstructured quadratic source accepted')
    large=[]
    for t,h,beta,qpoly in [(17,0x211,1,{1,6,24}), (33,3,1,{1})]:
        start=time.perf_counter();gap,meta=invariant_quadratic_gap(t,h,beta,qpoly)
        n=3*Field(h).a*t*t
        large.append(dict(matrix_size=t,field_modulus=h,original_bits=n,
            gap_hex=hex(gap),ones_hex=hex(((1<<n)-gap)//2),seconds=time.perf_counter()-start,
            matrix_coordinates_supplied=True,raw_acquisition_executed=False,backend=meta))
        print('large invariant',t,n,large[-1]['seconds'],flush=True)
    result=dict(status='all exact comparisons passed',backend_cases=backend,
        raw_acquisitions=rawcases,controlled_rejection=rejection,
        large_intrinsic_counts=large,practical_speed_comparison_claim=False,
        seconds=time.perf_counter()-begun)
    Path(__file__).with_name('invariant_quadratic_results.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':run()
