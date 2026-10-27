#!/usr/bin/env python3
"""Independent exact audit of a Frobenius-band trace-quadratic interface."""
from itertools import product
from pathlib import Path
import json
import random
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_field_root'))
from field_rank_decoder import decode_gabidulin


class Field:
    def __init__(self,d,h):
        self.d,self.h,self.q=d,h,1<<d
    def mul(self,a,b):
        out=0
        while b:
            if b&1: out^=a
            b>>=1; a<<=1
            if a&self.q: a^=self.h
        return out
    def power(self,a,e):
        out=1
        while e:
            if e&1: out=self.mul(out,a)
            a=self.mul(a,a); e>>=1
        return out
    def frob(self,a,j):
        for _ in range(j%self.d): a=self.mul(a,a)
        return a
    def trace(self,a):
        out=0
        for _ in range(self.d):
            out^=a; a=self.mul(a,a)
        assert out in (0,1)
        return out


def polynomial_gcd(a,b):
    while b:
        while a and a.bit_length()>=b.bit_length():
            a^=b<<(a.bit_length()-b.bit_length())
        a,b=b,a
    return a


def make_field(d):
    for h in range((1<<d)|1,1<<(d+1),2):
        field=Field(d,h)
        x=2
        good=True
        for i in range(1,d+1):
            x=field.mul(x,x)
            if i<=d//2 and polynomial_gcd(x^2,h)!=1:
                good=False; break
        if good and x==2:
            return field
    raise AssertionError('no irreducible polynomial')


def rank(vectors):
    piv={}
    for x in vectors:
        while x:
            k=x.bit_length()-1
            if k in piv: x^=piv[k]
            else:
                piv[k]=x; break
    return len(piv)


def linear_apply(columns,x):
    out=0
    while x:
        t=x&-x; out^=columns[t.bit_length()-1]; x^=t
    return out


def solve(columns,x):
    piv={}
    for i,col in enumerate(columns):
        y=col; c=1<<i
        while y:
            k=y.bit_length()-1
            if k in piv:
                a,b=piv[k]; y^=a; c^=b
            else:
                piv[k]=(y,c); break
    c=0
    while x:
        k=x.bit_length()-1
        if k not in piv: return None
        a,b=piv[k]; x^=a; c^=b
    return c


def band_value(field,coefficients,s,x):
    out=0
    for j,c in zip(range(-s,s+1),coefficients):
        out^=field.mul(c,field.frob(x,j))
    return out


def folded_cross(field,coefficients,s,x,y):
    out=0
    for j,c in zip(range(-s,s+1),coefficients):
        if j<0:
            out^=field.mul(field.frob(c,-j),field.mul(field.frob(x,-j),y))
        else:
            out^=field.mul(c,field.mul(x,field.frob(y,j)))
    return field.trace(out)


def diagonal_coefficients(field,positive,s):
    coefficients=[0]*(2*s+1)
    for j,c in enumerate(positive,1):
        coefficients[s+j]=c
        coefficients[s-j]=field.frob(c,-j)
    return coefficients


def diagonal_trace(field,positive,x):
    return field.trace(sum_xor(field.mul(c,field.mul(x,field.frob(x,j)))
                               for j,c in enumerate(positive,1)))


def sum_xor(xs):
    out=0
    for x in xs: out^=x
    return out


def matrix_for_map(field,images):
    return [sum(field.trace(field.mul(1<<i,images[j]))<<j
                for j in range(field.d)) for i in range(field.d)]


def canonical_quadratic(B,x):
    return sum((x>>i&1)*((B[i]&x&((1<<i)-1)).bit_count()&1)
               for i in range(len(B)))&1


def exhaustive_small_band(d):
    field=make_field(d); q=field.q; s=1
    mul=[[field.mul(x,y) for y in range(q)] for x in range(q)]
    trace=[field.trace(x) for x in range(q)]
    pairing=[[trace[mul[x][y]] for y in range(q)] for x in range(q)]
    fplus=[field.frob(x,1) for x in range(q)]
    fminus=[field.frob(x,-1) for x in range(q)]
    minimum=d+1; alternating_count=self_adjoint_count=0
    cross_checks=shift_checks=diagonal_checks=0
    unary_correction_cases=0
    for cm,c0,cp in product(range(q),repeat=3):
        coeff=[cm,c0,cp]
        values=[mul[cm][fminus[x]]^mul[c0][x]^mul[cp][fplus[x]] for x in range(q)]
        columns=[values[1<<i] for i in range(d)]
        rr=rank(columns)
        if any(coeff):
            minimum=min(minimum,rr); assert rr>=d-2
        B=matrix_for_map(field,columns)
        isself=all((B[i]>>j&1)==(B[j]>>i&1) for i in range(d) for j in range(d))
        isalt=isself and all(not (B[i]>>i&1) for i in range(d))
        assert isself==(cm==field.frob(cp,-1))
        assert isalt==(cm==field.frob(cp,-1) and c0==0)
        self_adjoint_count+=isself
        alternating_count+=isalt
        cm2=mul[cm][cm]
        for x in range(q):
            shifted=mul[cm][x]^mul[c0][fplus[x]]^mul[cp][fplus[fplus[x]]]
            assert values[fplus[x]]==shifted
            shift_checks+=1
            for y in range(q):
                folded=trace[mul[c0][mul[x][y]]^mul[cp][mul[x][fplus[y]]]^mul[cm2][mul[fplus[x]][y]]]
                assert folded==pairing[x][values[y]]
                cross_checks+=1
        if isalt:
            Q=[trace[mul[cp][mul[x][fplus[x]]]] for x in range(q)]
            correction=sum(Q[1<<i]<<i for i in range(d))
            unary_correction_cases+=bool(correction)
            for x in range(q):
                assert canonical_quadratic(B,x)==Q[x]^((correction&x).bit_count()&1)
                for y in range(q):
                    assert Q[x^y]^Q[x]^Q[y]==pairing[x][values[y]]
                    diagonal_checks+=1
    return dict(d=d,s=s,modulus=field.h,all_band_maps=q**3,
                minimum_nonzero_code_rank=minimum,expected_minimum=d-2,
                self_adjoint_maps=self_adjoint_count,alternating_maps=alternating_count,
                unary_correction_cases=unary_correction_cases,cross_checks=cross_checks,
                precomposition_checks=shift_checks,diagonal_polar_checks=diagonal_checks)


def exhaustive_diagonal_band(d,s):
    field=make_field(d); q=field.q
    pairing=[[field.trace(field.mul(x,y)) for y in range(q)] for x in range(q)]
    Qs=[]; Ls=[]
    for j in range(1,s+1):
        Qs.append([[field.trace(field.mul(c,field.mul(x,field.frob(x,j))))
                    for x in range(q)] for c in range(q)])
        Ls.append([[field.mul(c,field.frob(x,j))^field.mul(field.frob(c,-j),field.frob(x,-j))
                    for x in range(q)] for c in range(q)])
    checks=representatives=unary=0
    for positive in product(range(q),repeat=s):
        Q=[sum_xor(Qs[j][c][x] for j,c in enumerate(positive)) for x in range(q)]
        L=[sum_xor(Ls[j][c][x] for j,c in enumerate(positive)) for x in range(q)]
        B=matrix_for_map(field,[L[1<<i] for i in range(d)])
        assert all(not (B[i]>>i&1) for i in range(d))
        correction=sum(Q[1<<i]<<i for i in range(d))
        unary+=bool(correction)
        for x in range(q):
            assert canonical_quadratic(B,x)==Q[x]^((correction&x).bit_count()&1)
            for y in range(q):
                assert Q[x^y]^Q[x]^Q[y]==pairing[x][L[y]]
                checks+=1
        representatives+=1
    return dict(d=d,s=s,modulus=field.h,all_positive_coefficients=representatives,
                diagonal_polar_checks=checks,unary_correction_cases=unary)


def boundary_cases():
    out=[]
    for d in [2,4,6]:
        field=make_field(d); s=d//2
        constants=[c for c in range(1,field.q) if field.frob(c,s)==c]
        checks=0
        for c in constants:
            assert all(field.trace(field.mul(c,field.mul(x,field.frob(x,s))))==0
                       for x in range(field.q))
            L=[field.mul(c,field.frob(1<<j,s)) for j in range(d)]
            B=matrix_for_map(field,L)
            assert any(B) and all(not (B[i]>>i&1) for i in range(d))
            a=next(a for a in range(field.q) if a^field.frob(a,s)==c)
            Q=[field.trace(field.mul(a,field.mul(x,field.frob(x,s)))) for x in range(field.q)]
            for x in range(field.q):
                for y in range(field.q):
                    assert Q[x^y]^Q[x]^Q[y]==field.trace(field.mul(x,field.mul(c,field.frob(y,s))))
                    checks+=1
        out.append(dict(d=d,s=s,half_period_coefficients=len(constants),
                        naive_trace_representative_identically_zero=True,
                        nonzero_polar_block=True,corrected_polar_checks=checks))
    return out


def decoder_checks():
    rng=random.Random(2057); records=[]
    for d,s,e in [(3,1,0),(4,1,0),(5,1,1),(5,2,0),(7,2,1),
                  (9,2,2),(11,3,2),(13,4,2)]:
        field=make_field(d); k=2*s+1
        for trial in range(8):
            coeff=[rng.randrange(field.q) for _ in range(k)]
            u=[]; v=[]
            while len(u)<e:
                a=rng.randrange(1,field.q)
                if rank(u+[a])>len(u): u.append(a)
            while len(v)<e:
                a=rng.randrange(1,field.q)
                if rank(v+[a])>len(v): v.append(a)
            errors=[sum_xor(a for a,m in zip(u,v) if (m>>j)&1) for j in range(d)]
            assert rank(errors)==e
            received=[]
            for j in range(d):
                x=1<<j
                original=band_value(field,coeff,s,field.frob(x,s))
                received.append(original^errors[j])
            got,cert=decode_gabidulin(received,field.h,k=k)
            assert got==coeff and cert['error_rank']==e
            for _ in range(32):
                x=rng.randrange(field.q)
                decoded=sum_xor(field.mul(c,field.frob(field.frob(x,-s),j))
                                for j,c in enumerate(got))
                assert decoded==band_value(field,coeff,s,x)
            records.append(dict(d=d,s=s,error_rank=e,trial=trial,
                                minimum_distance=d-2*s,radius=(d-k)//2))
    return records


def main():
    small=[exhaustive_small_band(d) for d in [3,4]]
    diagonal=[exhaustive_diagonal_band(5,2),exhaustive_diagonal_band(6,2)]
    boundary=boundary_cases()
    decoder=decoder_checks()
    result=dict(status='all exact assertions passed',
                exhaustive_small_bands=small,exhaustive_diagonal_bands=diagonal,
                half_period_boundary=boundary,decoding_cases=decoder,
                total_decoding_cases=len(decoder),
                raw_representative_requires_linear_correction=True,
                asymptotic_point_counter_executed=False)
    Path(__file__).with_name('frobenius_band_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='decoding_cases'},indent=2))


if __name__=='__main__':
    main()
