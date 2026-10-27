#!/usr/bin/env python3
"""Independent stress check of the acquisition theorem's ring-isomorphism invariance."""
from pathlib import Path
import json,random,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_chain_root'))
from acquired_chain_counter import *
from field_descent import extract_anf

def run():
    rng=random.Random(668912);cases=[];raw_cases=[]
    for h,e in [(0b1011,2),(0b1011,3),(0b10011,3),(0x83,2)]:
        R=ChainRing(h,e);q=1<<R.d;mask=(1<<R.m)-1
        for trial in range(4):
            frob=1+rng.randrange(R.d-1)
            timage=rng.randrange(1,q)<<R.d
            for j in range(2,e):timage^=rng.randrange(q)<<(R.d*j)
            def sigma(a):
                out=0
                for j in range(e):
                    coefficient=gf_pow((a>>(R.d*j))&R.mask,1<<frob,h)
                    out^=R.mul(coefficient,ring_pow(R,timage,j))
                return out
            sigcols=[sigma(1<<j) for j in range(R.m)]
            assert len(span(sigcols))==R.m
            inverse=Solver(sigcols)
            functional=sum(R.functional(sigma(1<<j))<<j for j in range(R.m))
            multiplier=solve(R.gram(),functional)
            assert multiplier is not None and multiplier&R.mask
            P={(1,1,1):rng.randrange(mask+1)|1}
            for exponent in [(1,1,0),(1,0,1),(0,1,1),(1,0,0),(0,1,0),(0,0,1),(0,0,0)]:
                P[exponent]=rng.randrange(mask+1)
            transformed={exponent:R.mul(multiplier,inverse(c)) for exponent,c in P.items()}
            # An upper triangular ring matrix with unit diagonal is invertible.
            columns=[[1,0,0],[rng.randrange(mask+1),1,0],
                     [rng.randrange(mask+1),rng.randrange(mask+1),1]]
            transformed=substitute(R,transformed,columns)
            balanced,planes,cert=factor_chain_cubic(R,transformed)
            ref=balanced_count(R,P);assert balanced_count(R,balanced)==ref
            for _ in range(128):
                values=[rng.randrange(mask+1) for _ in range(3)]
                moved=[0]*3
                for i in range(3):
                    for j in range(3):moved[i]^=R.mul(columns[j][i],values[j])
                expected=R.functional(ring_polynomial(R,P,[sigma(x) for x in moved]))
                actual=R.functional(ring_polynomial(R,transformed,values))
                assert expected==actual
            case=dict(d=R.d,e=e,frobenius_power=frob,uniformizer_image=timage,
                      functional_multiplier=multiplier,pointwise_checks=128,count=ref)
            cases.append(case)
            if trial==0 and R.d<=4:
                n=3*R.m
                def evaluate(x):
                    return R.functional(ring_polynomial(R,transformed,
                        [(x>>(R.m*i))&mask for i in range(3)]))
                raw=extract_anf(evaluate,n)
                result=compile_chain(raw,n)
                assert result['signed_count']==ref
                raw_cases.append(dict(n=n,raw_terms=len(raw),count=ref,
                    acquired_modulus=result['field_modulus'],chain_length=result['chain_length']))
    out=dict(status='all exact assertions passed',semilinear_cases=cases,
             raw_acquisitions=raw_cases,total_pointwise_checks=128*len(cases),
             claim='field Frobenius and nonlinear uniformizer substitutions preserve certified family')
    Path(__file__).with_name('semilinear_ring_audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':
    result=run();print(json.dumps(dict(status=result['status'],cases=len(result['semilinear_cases']),
        raw_cases=len(result['raw_acquisitions']),checks=result['total_pointwise_checks'])))
