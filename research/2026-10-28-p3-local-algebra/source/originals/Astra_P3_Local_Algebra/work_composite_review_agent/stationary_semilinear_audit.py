#!/usr/bin/env python3
"""Check smooth-quotient promise after noncanonical semilinear acquisition."""
from pathlib import Path
import itertools,json,random,sys,time
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_local_algebra_agent','work_ring_count_agent','work_chain_root'):
    sys.path.insert(0,str(ROOT/folder))
from acquired_chain_counter import *
from stationary_chain_counter import compile_stationary
from field_descent import extract_anf
from smooth_ring_counter import projective_smooth
from top_digit_deflation_audit import brute_sum

def run():
    rng=random.Random(8343729);rows=[]
    H0={(2,0,1):1,(0,3,0):1,(0,0,3):1,(1,1,1):1}
    cubics=[(i,j,3-i-j) for i in range(4) for j in range(4-i)]
    for h,e in [(11,2),(19,2),(11,3)]:
        R=ChainRing(h,e);n=3*R.m;q=1<<R.d;mask=(1<<R.m)-1
        frob=1+rng.randrange(R.d-1)
        timage=rng.randrange(1,q)<<R.d
        for j in range(2,e): timage^=rng.randrange(q)<<(R.d*j)
        def sigma(x):
            out=0
            for j in range(e):
                a=gf_pow((x>>(R.d*j))&R.mask,1<<frob,h)
                out^=R.mul(a,ring_pow(R,timage,j))
            return out
        sigcols=[sigma(1<<j) for j in range(R.m)]
        inverse=Solver(sigcols)
        assert len(span(sigcols))==R.m
        c=solve(R.gram(),sum(R.functional(sigma(1<<j))<<j for j in range(R.m)))
        assert c&R.mask
        H={ex:H0.get(ex,0)^sum(rng.randrange(q)<<(R.d*j) for j in range(1,e)) for ex in cubics}
        H={ex:v for ex,v in H.items() if v}
        M=[[0]*3 for _ in range(3)]
        for i in range(3):
            M[i][i]=(rng.getrandbits(R.m)&~R.mask)^rng.randrange(1,q)
            for j in range(i+1,3): M[i][j]=rng.getrandbits(R.m)
        columns=[[M[i][j] for i in range(3)] for j in range(3)]
        Minv=matrix_inverse(R,M)
        A=[rng.getrandbits(R.m) for _ in range(3)]
        B=[rng.getrandbits(R.m) for _ in range(3)]
        translated=[0]*3
        for i in range(3):
            for j in range(3): translated[i]^=R.mul(Minv[i][j],A[j]^B[j])
            translated[i]=inverse(translated[i])
        Hnew={ex:R.mul(c,inverse(v)) for ex,v in substitute(R,H,columns).items()}
        residue={ex:v&R.mask for ex,v in Hnew.items() if v&R.mask}
        assert projective_smooth(residue,h) and residue[(1,1,1)]
        depth=(e+1)//3;ids=[i*R.m+j for i in range(3) for j in range(R.d*depth)]
        Q={0} if rng.randrange(2) else set()
        for i in ids:
            if rng.randrange(2):Q.add(1<<i)
        for i,j in itertools.combinations(ids,2):
            if rng.randrange(2):Q.add((1<<i)|(1<<j))
        def hidden_x(y):
            sy=[sigma((y>>(i*R.m))&mask) for i in range(3)]
            out=A[:]
            for i in range(3):
                for j in range(3):out[i]^=R.mul(M[i][j],sy[j])
            return out
        def value(y):
            x=hidden_x(y)
            return R.functional(ring_polynomial(R,H,[a^b for a,b in zip(x,B)]))^polynomial_value(Q,sum(v<<(i*R.m) for i,v in enumerate(x)))
        for _ in range(256):
            y=rng.getrandbits(n);x=hidden_x(y)
            left=R.functional(ring_polynomial(R,H,[a^b for a,b in zip(x,B)]))
            ys=[((y>>(i*R.m))&mask)^translated[i] for i in range(3)]
            right=R.functional(ring_polynomial(R,Hnew,ys))
            assert left==right
        raw=extract_anf(value,n)
        expected=(-1)**polynomial_value(Q,sum(v<<(i*R.m) for i,v in enumerate(B)))
        expected*=1<<(R.d*(2*e if e%3==0 else 2*e-1))
        exhaustive=brute_sum(raw,n);assert exhaustive==expected
        started=time.perf_counter();actual=compile_stationary(raw,n)
        assert actual['signed_count']==expected
        row=dict(d=R.d,e=e,n=n,frobenius=frob,uniformizer_image=timage,
            functional_unit=c,semilinear_matrix=M,coordinate_translation=A,
            homogeneous_translation=B,transformed_translation=translated,
            original_H=[dict(exponents=list(ex),coefficient=v) for ex,v in H.items()],
            transformed_H=[dict(exponents=list(ex),coefficient=v) for ex,v in Hnew.items()],
            quotient_Q=sorted(Q),raw_anf=sorted(raw),signed_count=expected,
            functional_identity_checks=256,root_compiler_seconds=time.perf_counter()-started)
        rows.append(row)
        print(json.dumps({k:row[k] for k in ('d','e','n','signed_count','root_compiler_seconds')}),flush=True)
    result=dict(status='all exact assertions passed',cases=rows,total_functional_checks=256*len(rows))
    Path(__file__).with_name('stationary_semilinear_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    result=run();print(json.dumps(dict(status=result['status'],cases=len(result['cases']))))
