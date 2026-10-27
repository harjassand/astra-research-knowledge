#!/usr/bin/env python3
from smooth_ring_counter import *
from itertools import combinations
import random,json,time
from pathlib import Path

def binary_smooth_with_xyz():
    others=[m for m in CUBICS if m!=(1,1,1)]
    for bits in range(1<<len(others)):
        H={(1,1,1):1}; H.update({m:1 for j,m in enumerate(others) if bits>>j&1})
        if projective_smooth(H,3): return H
    raise AssertionError('no smooth binary cubic')

def raw_from(R,H,Q):
    n=3*R.d*R.e; width=R.d*R.e
    def value(x):
        vals=[R.packed((x>>(i*width))&((1<<width)-1)) for i in range(3)]
        return R.bit(ring_polynomial_value(R,H,vals))^polynomial_value(Q,x)
    return extract_anf(value,n)

def serial(H): return [[list(e),list(c)] for e,c in sorted(H.items())]

def main():
    rng=random.Random(202610272156); source=binary_smooth_with_xyz(); print('smooth binary residue',source,flush=True)
    smooth_tests=0
    for h in (3,7,11,19):
        q=1<<(h.bit_length()-1)
        for a in range(q):
            H={(2,1,0):1,(1,2,0):1,(0,0,3):1}
            if a: H[(1,1,1)]=a
            assert projective_smooth(H,h)==(gf_pow(a,3,h)!=1),(h,a)
            smooth_tests+=1
    rows=[]
    for h,e in [(3,2),(3,3),(3,5),(7,2),(11,2)]:
        R=ChainRing(h,e); n=3*R.d*e; depth=(e+1)//3
        H={m:tuple([source.get(m,0)]+[rng.randrange(R.q) for _ in range(e-1)]) for m in CUBICS}
        H={m:c for m,c in H.items() if any(c)}
        low=quotient_bitmask(R,depth); ids=[i for i in range(n) if low>>i&1]
        Q={0} if rng.randrange(2) else set()
        for i in ids:
            if rng.randrange(2): Q.add(1<<i)
        for i,j in combinations(ids,2):
            if rng.randrange(2): Q.add((1<<i)|(1<<j))
        B=[sum(1<<j for j in range(n) if i!=j and ((1<<i)|(1<<j)) in Q) for i in range(n)]
        from field_descent import span
        rank=len(span(B)); poly=raw_from(R,H,Q); start=time.perf_counter()
        fit=acquire_quotient_quadratic(poly,R); elapsed=time.perf_counter()-start
        expected=(-1 if 0 in Q else 1)*smooth_homogeneous_sum(R,H)
        assert fit['signed_count']==expected
        assert {m:c[0] for m,c in fit['H'].items() if c[0]}==source
        brute=sum(1-2*polynomial_value(poly,x) for x in range(1<<n))
        assert brute==expected
        rows.append(dict(h=h,e=e,n=n,depth=depth,noise_rank=rank,raw_terms=len(poly),
                         input_anf=sorted(poly),planted_H=serial(H),planted_Q=sorted(Q),
                         acquired_H=serial(fit['H']),acquired_Q=sorted(fit['Q']),
                         signed_count=brute,zero_count=fit['zero_count'],seconds=elapsed,
                         fit_rows=fit['linear_fit_rows'],fit_columns=fit['linear_fit_columns']))
        print('fit',h,e,n,rank,brute,elapsed,flush=True)
    hesse=[]
    for h in (11,37):
        d=h.bit_length()-1; q=1<<d
        for a in range(2,min(q,7)):
            H0={(2,1,0):1,(1,2,0):1,(0,0,3):1,(1,1,1):a}
            if gf_pow(a,3,h)==1: continue
            fast=field_hesse_sum(H0,h); brute=0; points=0
            for x,y,z in product(range(q),repeat=3):
                value=0
                for ex,c in H0.items():
                    v=c
                    for xx,ee in zip((x,y,z),ex): v=gf_mul(v,gf_pow(xx,ee,h),h)
                    value^=v
                brute+=1-2*gf_trace(value,h)
                if (x,y,z)!=(0,0,0) and value==0: points+=1
            points//=q-1
            assert fast==brute==q*(points-q-1)
            hesse.append(dict(h=h,a=a,Z=fast,projective_points=points))
    failures=[]
    for e in (2,3,5):
        R=ChainRing(3,e); H={m:(c,)+(0,)*(e-1) for m,c in source.items()}; n=3*e
        raw=raw_from(R,H,set()); base=smooth_homogeneous_sum(R,H); dep=(e+1)//3
        for j in range(dep,e):
            changed=set(raw); changed.symmetric_difference_update({1<<j})
            Z=sum(1-2*polynomial_value(changed,x) for x in range(1<<n))
            if Z!=base:
                rejected=False
                try: acquire_quotient_quadratic(changed,R)
                except ValueError: rejected=True
                assert rejected
                failures.append(dict(e=e,allowed_quotient_depth=dep,linear_digit=j,base=base,shifted=Z,rejected=True)); break
        else: raise AssertionError('expected incompatible-shift counterexample')
    out=dict(smoothness_family_checks=smooth_tests,raw_acquisition_cases=rows,
             field_formula_cases=hesse,incompatible_linear_shifts=failures)
    Path(__file__).with_name('smooth_ring_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('saved smooth results',len(rows),len(hesse),len(failures))
if __name__=='__main__': main()
