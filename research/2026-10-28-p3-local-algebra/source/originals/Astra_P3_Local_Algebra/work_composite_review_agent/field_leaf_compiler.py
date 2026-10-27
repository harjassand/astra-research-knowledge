#!/usr/bin/env python3
"""Manufacture an exact fixed-degree Artin-Schreier point-counting leaf.

This module compiles and certifies the leaf. It does not implement the
Lauder-Wan point-counting algorithm and does not label brute force polynomial.
"""
from pathlib import Path
import itertools,json,random,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_field_root'))
from field_descent import extract_anf,solve,span,gf_mul,gf_pow,bits
from field_kloosterman import gf_trace


def ordinary_value(P,x,h):
    result=0
    for exponents,coefficient in P.items():
        term=coefficient
        for xi,power in zip(x,exponents):
            if power:term=gf_mul(term,gf_pow(xi,power,h),h)
        result^=term
    return result


def fit_trace_cubic(poly,h):
    d=h.bit_length()-1;n=3*d;mask=(1<<d)-1;poly=set(poly)
    if any(m<0 or m>>n or m.bit_count()>3 for m in poly):
        raise ValueError('invalid cubic Boolean field phase')
    monomials=[sum(1<<i for i in S) for k in range(4)
               for S in itertools.combinations(range(n),k)]
    positions={m:i for i,m in enumerate(monomials)}
    def vector(p):return sum(1<<positions[m] for m in p)
    exponents=[(i,j,total-i-j) for total in range(4) for i in range(total+1)
               for j in range(total-i+1)]
    columns=[];models=[];labels=[]
    for ex in exponents:
        for bit in range(d):
            P={ex:1<<bit}
            model=extract_anf(lambda x:gf_trace(ordinary_value(P,[(x>>(d*i))&mask for i in range(3)],h),h),n)
            models.append(model);columns.append(vector(model));labels.append((ex,bit))
    solution=solve(columns,vector(poly))
    if solution is None:raise ValueError('field phase is outside traces of ordinary degree-at-most-three polynomials')
    P={};reconstructed=set()
    for i in bits(solution):
        ex,bit=labels[i];P[ex]=P.get(ex,0)^(1<<bit)
        reconstructed.symmetric_difference_update(models[i])
    assert reconstructed==poly
    P={ex:c for ex,c in P.items() if c}
    equation=[dict(exponents=list(ex)+[0],coefficient=c) for ex,c in sorted(P.items())]
    equation.extend([dict(exponents=[0,0,0,1],coefficient=1),dict(exponents=[0,0,0,2],coefficient=1)])
    certificate=dict(field_modulus=h,field_degree=d,original_binary_variables=n,
        exact_trace_identity=True,ordinary_degree_bound=3,fit_columns=len(columns),
        fit_rank=len(span(columns)),fit_constraints=len(monomials),
        point_count_variables=4,point_count_degree=3,
        artin_schreier_equation=equation,
        signed_count_identity='N(W^2+W+P=0 over Fq) - q^3',
        point_count_backend_implemented=False)
    return P,certificate


def run_checks():
    rng=random.Random(546193);cases=[]
    exponents=[(i,j,total-i-j) for total in range(4) for i in range(total+1)
               for j in range(total-i+1)]
    for h in (3,7,11,19):
        d=h.bit_length()-1;q=1<<d
        for trial in range(3):
            planted={ex:rng.randrange(q) for ex in exponents}
            planted={ex:c for ex,c in planted.items() if c}
            raw=extract_anf(lambda x:gf_trace(ordinary_value(planted,[(x>>(d*i))&(q-1) for i in range(3)],h),h),3*d)
            fitted,cert=fit_trace_cubic(raw,h)
            # Independent direct count of W^2+W=P, without using its trace criterion.
            fibers=[0]*q
            for w in range(q):fibers[gf_mul(w,w,h)^w]+=1
            points=0;signed=0
            for x in itertools.product(range(q),repeat=3):
                a=ordinary_value(fitted,x,h);points+=fibers[a]
                source=ordinary_value(planted,x,h)
                signed+=1-2*gf_trace(source,h)
            assert points-q**3==signed
            cases.append(dict(h=h,d=d,trial=trial,raw_anf=sorted(raw),
                fitted_polynomial=[dict(exponents=list(ex),coefficient=c) for ex,c in fitted.items()],
                point_count=points,signed_count=signed,certificate=cert))
    h=19;d=4;q=16
    bad=extract_anf(lambda x:gf_trace(gf_mul(x&(q-1),gf_mul((x>>d)&(q-1),(x>>(2*d))&(q-1),h),h),h),3*d)
    bad.symmetric_difference_update({(1<<0)|(1<<d)})
    try:fit_trace_cubic(bad,h)
    except ValueError as exc:rejection=str(exc)
    else:raise AssertionError('rank-one cross quadratic should exceed the ordinary degree-three trace space')
    result=dict(status='all exact assertions passed',cases=cases,
        rejected_quadratic_leaf=dict(d=d,h=h,raw_anf=sorted(bad),rejection=rejection),
        scope='exact fixed-degree leaf compilation and point-count identity; no generic point-count backend execution')
    Path(__file__).with_name('field_leaf_compiler_results.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    result=run_checks();print(json.dumps(dict(status=result['status'],cases=len(result['cases']),rejections=1)))
