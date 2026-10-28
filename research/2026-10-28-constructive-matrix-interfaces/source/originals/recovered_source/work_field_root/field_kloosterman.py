#!/usr/bin/env python3
"""Exact Kloosterman sums using established finite Dwork trace machinery.
The counter does not enumerate field elements. Validation has a separate
exhaustive small-field oracle. NumPy speeds modular ring matrix products.
"""
from fractions import Fraction
from functools import lru_cache
import json, math, time
from pathlib import Path
import numpy as np


def gf_mul(a,b,h):
    d=h.bit_length()-1; out=0
    while b:
        if b&1: out^=a
        b>>=1; a<<=1
        if a>>d: a^=h
    return out


def gf_pow(a,e,h):
    out=1
    while e:
        if e&1: out=gf_mul(out,a,h)
        a=gf_mul(a,a,h); e>>=1
    return out


def gf_trace(a,h):
    out=0
    for _ in range(h.bit_length()-1):
        out^=a; a=gf_mul(a,a,h)
    if out not in (0,1): raise ValueError('not a field presentation')
    return out


def binary_remainder(a,b):
    while a and a.bit_length()>=b.bit_length(): a^=b<<(a.bit_length()-b.bit_length())
    return a


def binary_gcd(a,b):
    while b: a,b=b,binary_remainder(a,b)
    return a


@lru_cache(maxsize=None)
def irreducible_binary(h):
    """Rabin irreducibility test, polynomial time in the extension degree."""
    if not isinstance(h,int) or h<2: return False
    d=h.bit_length()-1; x=binary_remainder(2,h); y=x
    for i in range(1,d+1):
        y=gf_mul(y,y,h)
        if i<=d//2 and binary_gcd(y^x,h)!=1: return False
    return y==x


class Unramified:
    def __init__(self,h,N):
        self.h=h; self.d=h.bit_length()-1; self.N=N
        self.mask=(1<<N)-1
        self.lower=[i for i in range(self.d) if h>>i&1]
        self.one=(1,)+(0,)*(self.d-1)
        self.dtype=np.int64 if N<=62 else object

    def mul(self,a,b):
        c=[0]*(2*self.d-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): c[i+j]+=x*y
        for k in range(2*self.d-2,self.d-1,-1):
            for j in self.lower: c[k-self.d+j]-=c[k]
        return tuple(x&self.mask for x in c[:self.d])

    def teich(self,residue):
        a=tuple(residue>>i&1 for i in range(self.d))
        for _ in range(self.d*((self.N+self.d-1)//self.d)): a=self.mul(a,a)
        check=a
        for _ in range(self.d): check=self.mul(check,check)
        assert check==a
        assert sum((x&1)<<i for i,x in enumerate(a))==residue
        return a

    def matrix_mul(self,A,B):
        size=A.shape[1]
        out=np.zeros((2*self.d-1,size,size),dtype=self.dtype)
        an=[i for i in range(self.d) if np.any(A[i])]
        bn=[i for i in range(self.d) if np.any(B[i])]
        for i in an:
            for j in bn:
                out[i+j]+=A[i]@B[j]; out[i+j]&=self.mask
        for k in range(2*self.d-2,self.d-1,-1):
            for j in self.lower:
                out[k-self.d+j]-=out[k]; out[k-self.d+j]&=self.mask
        return out[:self.d]


def theta_coefficients(N):
    """Formal coefficient expansion; substituting exp(0) at 1 is invalid."""
    r=[Fraction(1)]
    for j in range(1,4*N): r.append((-2*r[-1]+(4*r[-2] if j>=2 else 0))/j)
    mod=1<<N; out=[]
    for j,x in enumerate(r):
        assert x.denominator&1
        if x.numerator:
            v=(abs(x.numerator)&-abs(x.numerator)).bit_length()-1
            assert 4*v>=j
        out.append((x.numerator*pow(x.denominator,-1,mod))%mod)
    assert sum(out)%mod==mod-1
    return out


def local_matrix(ring,A,theta):
    length=len(theta); B=4*ring.N-1
    exponents=np.arange(-B,B+1)
    coefficients=np.zeros((ring.d,2*length-1),dtype=ring.dtype)
    powers=[ring.one]
    for _ in range(1,length): powers.append(ring.mul(powers[-1],A))
    for v,tv in enumerate(theta):
        if not tv: continue
        for u,tu in enumerate(theta):
            scalar=(tv*tu)&ring.mask
            if not scalar: continue
            slot=u-v+length-1
            for j,c in enumerate(powers[v]):
                coefficients[j,slot]=(int(coefficients[j,slot])+scalar*c)&ring.mask
    idx=2*exponents[:,None]-exponents[None,:]+length-1
    valid=(idx>=0)&(idx<2*length-1)
    return coefficients[:,np.clip(idx,0,2*length-2)]*valid[None,:,:]


def kloosterman_dwork(a,h,*,use_hasse=False):
    if not irreducible_binary(h): raise ValueError('modulus must be irreducible over F2')
    d=h.bit_length()-1; q=1<<d
    if not isinstance(a,int) or not 0<=a<q: raise ValueError('field element out of range')
    if a==0: return -1,dict(extension_degree=d,shortcut='zero coefficient')
    N=d//2+3 if use_hasse else d+2
    ring=Unramified(h,N); A=ring.teich(a); theta=theta_coefficients(N)
    product=None; start=time.perf_counter()
    for i in range(d):
        matrix=local_matrix(ring,A,theta)
        product=matrix if product is None else ring.matrix_mul(matrix,product)
        A=ring.mul(A,A)
    residues=[((q-1)*int(np.trace(product[j])))&ring.mask for j in range(d)]
    assert not any(residues[1:]),(a,h,residues)
    answer=residues[0]
    if answer>=1<<(N-1): answer-=1<<N
    bound=math.isqrt(4*q) if use_hasse else q-1
    assert abs(answer)<=bound
    return answer,dict(extension_degree=d,precision_bits=N,
        trace_matrix_dimension=8*N-1,field_enumerations=0,
        frobenius_factors=d,integer_residue=residues[0],
        seconds=time.perf_counter()-start,
        reconstruction_bound='Hasse' if use_hasse else 'elementary')


def kloosterman_brute(a,h):
    q=1<<(h.bit_length()-1)
    return sum((-1)**gf_trace(x^gf_mul(a,gf_pow(x,q-2,h),h),h) for x in range(1,q))


def validation():
    moduli=[0b11,0b111,0b1011,0b10011,0b100101,0b1000011]
    cases=[]
    for h in moduli:
        d=h.bit_length()-1
        samples=list(range(1,1<<d)) if d<=3 else [1,2,(1<<d)-1]
        for a in samples:
            count,data=kloosterman_dwork(a,h)
            oracle=kloosterman_brute(a,h)
            assert count==oracle,(h,a,count,oracle)
            data.update(modulus=h,coefficient=a,count=count,brute_oracle=oracle)
            cases.append(data)
    return dict(status='all exact assertions passed',cases=cases,
        counter_backend='finite Dwork trace, not field enumeration',
        theoretical_claim='specialization of established Dwork machinery')


if __name__=='__main__':
    data=validation(); path=Path(__file__).with_name('field_kloosterman_results.json')
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status=data['status'],cases=len(data['cases']),
        largest_extension=max(x['extension_degree'] for x in data['cases']),results=str(path))))
