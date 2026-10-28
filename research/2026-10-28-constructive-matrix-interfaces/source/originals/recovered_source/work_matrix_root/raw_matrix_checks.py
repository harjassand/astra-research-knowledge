#!/usr/bin/env python3
"""Independent planted-coordinate checks; compiler receives raw ANF only."""
import json, random
from pathlib import Path
from raw_matrix_trace import compile_raw_matrix_trace
from field_descent import extract_anf,polynomial_value,linear_apply,random_invertible
from matrix_kloosterman import Field,eye,matrix_trace_cubic_count,cubic_zero_source_sum

def native_anf(t,h,A,B,C,constant=0):
    F=Field(h); a=F.a; d=a*t*t; poly={0} if constant else set()
    for i in range(t):
        for j in range(t):
            for k in range(t):
                for u in range(a):
                    for v in range(a):
                        for w in range(a):
                            if F.trace(F.mul(F.mul(1<<u,1<<v),1<<w)):
                                poly.add((1<<(a*(i*t+j)+u))|
                                         (1<<(d+a*(j*t+k)+v))|
                                         (1<<(2*d+a*(k*t+i)+w)))
    for block,M in enumerate([A,B,C]):
        for i in range(t):
            for j in range(t):
                for u in range(a):
                    if F.trace(F.mul(M[j][i],1<<u)):
                        poly.add(1<<(d*block+a*(i*t+j)+u))
    return poly,3*d

def fixture(t,h,seed,source_case='units',constant=0):
    F=Field(h); rng=random.Random(seed); A=eye(t); C=eye(t)
    B=[[rng.randrange(F.q) for _ in range(t)] for _ in range(t)]
    if source_case=='zero':
        A=[[rng.randrange(F.q) for _ in range(t)] for _ in range(t)]
        C=[[0]*t for _ in range(t)]
    if source_case=='pure': A=B=C=[[0]*t for _ in range(t)]
    native,n=native_anf(t,h,A,B,C,constant)
    change=random_invertible(n,rng); offset=rng.randrange(1<<n)
    raw=extract_anf(lambda x:polynomial_value(native,linear_apply(change,x)^offset),n)
    if source_case in ('zero','pure'):
        expected,_=cubic_zero_source_sum(A,B,h); expected*=(-1)**constant
    else: expected=matrix_trace_cubic_count(A,B,C,h,constant)[1]['signed_sum']
    return raw,n,expected,dict(t=t,h=h,seed=seed,source_case=source_case,
                              native_monomials=len(native),raw_monomials=len(raw))

def run():
    cases=[]; full_inputs=0
    for t,h,seed,kind,c in [(2,3,11,'units',0),(2,3,12,'units',1),
            (2,3,13,'zero',0),(2,3,14,'pure',1),(2,7,15,'units',0),
            (3,3,16,'units',1),(2,11,17,'zero',1),(4,3,18,'units',0)]:
        raw,n,expected,meta=fixture(t,h,seed,kind,c)
        result=compile_raw_matrix_trace(raw,n)
        assert result['gap']==expected,(meta,result['gap'],expected)
        if n<=12:
            oracle=sum(1-2*polynomial_value(raw,x) for x in range(1<<n))
            assert oracle==expected; full_inputs+=1<<n
        cases.append(dict(**meta,**result))
        print('passed',t,h,kind,n,len(raw),result['gap'],result['stats']['seconds'],flush=True)
    native,n=native_anf(2,3,eye(2),eye(2),eye(2))
    bad=set(native); bad.add(3)
    try: compile_raw_matrix_trace(bad,n)
    except ValueError as e: rejection=str(e)
    else: raise AssertionError('unsupported same-tensor quadratic accepted')
    report=dict(cases=cases,exhaustive_original_inputs=full_inputs,controlled_rejection=rejection)
    Path(__file__).with_name('raw_matrix_results.json').write_text(json.dumps(report,indent=2))
    return report

if __name__=='__main__': run()
