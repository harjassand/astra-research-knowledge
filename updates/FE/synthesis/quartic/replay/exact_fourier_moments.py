#!/usr/bin/env python3
"""Exact nine quartic moments of rational, periodic planar gradients.

Potential: v(x)=sum_j [c_j cos(k_j.x)+s_j sin(k_j.x)], c_j,s_j in Q^2.
Returns E f_i(A0+Dv)-f_i(A0), for
(u^2,v^2,uv,w^2,uw,vw,qu,qv,qw).

Uses pair-frequency convolution and zero-frequency inner products, avoiding a
spatial integration grid. O(M^2) rational arithmetic operations for M waves
(up to fixed constants and dictionary operations); rational bit costs are not
unit cost. No third-party packages are required. This is a moment calculator,
not a quasiconvexity certificate or counterexample generator.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from typing import Iterable, Sequence

Scalar = int | str | Q
Key = tuple[int, int]

@dataclass(frozen=True)
class GQ:
    """Gaussian rational: exact real and imaginary rational parts."""
    real: Q = Q(0)
    imag: Q = Q(0)
    def __add__(self, other: GQ) -> GQ:
        return GQ(self.real+other.real,self.imag+other.imag)
    def __neg__(self) -> GQ:
        return GQ(-self.real,-self.imag)
    def __sub__(self, other: GQ) -> GQ:
        return self+(-other)
    def __mul__(self, other: GQ) -> GQ:
        return GQ(self.real*other.real-self.imag*other.imag,
                  self.real*other.imag+self.imag*other.real)
    def conj(self) -> GQ:
        return GQ(self.real,-self.imag)
    def is_zero(self) -> bool:
        return self.real==0 and self.imag==0

ZERO=GQ()
Poly=dict[Key,GQ]

def rational(x: Scalar) -> Q:
    if isinstance(x,float):
        raise TypeError('Use an integer, Fraction, or decimal/rational string, not a float.')
    return Q(x)

def add_term(p: Poly, k: Key, z: GQ) -> None:
    total=p.get(k,ZERO)+z
    if total.is_zero():p.pop(k,None)
    else:p[k]=total

def add(p: Poly,q: Poly, sign: int=1) -> Poly:
    out=dict(p)
    for k,v in q.items():add_term(out,k,v if sign==1 else -v)
    return out

def product(p: Poly,q: Poly) -> Poly:
    out:Poly={}
    for (i,j),a in p.items():
        for (k,l),b in q.items():add_term(out,(i+k,j+l),a*b)
    return out

def mean_product(p: Poly,q: Poly) -> Q:
    z=ZERO
    for (i,j),a in p.items():z=z+a*q.get((-i,-j),ZERO)
    if z.imag!=0:raise ArithmeticError('Expected a real zero-frequency coefficient.')
    return z.real

@dataclass(frozen=True)
class Wave:
    frequency: Key
    cosine: tuple[Scalar,Scalar]=(0,0)
    sine: tuple[Scalar,Scalar]=(0,0)

def moment_vector(background: Sequence[Sequence[Scalar]], waves: Iterable[Wave]) -> tuple[Q,...]:
    if len(background)!=2 or any(len(row)!=2 for row in background):
        raise ValueError('Background must be a 2 by 2 rational matrix.')
    bg=[rational(x) for row in background for x in row]
    entries: list[Poly]=[{(0,0):GQ(z)} if z else {} for z in bg]
    for wave in waves:
        k=wave.frequency
        if len(k)!=2 or not all(isinstance(x,int) for x in k):
            raise TypeError('Frequencies must be pairs of integers.')
        if k==(0,0):continue  # constant potential has zero gradient
        co=[rational(z) for z in wave.cosine];si=[rational(z) for z in wave.sine]
        if len(co)!=2 or len(si)!=2:raise ValueError('Potential amplitudes need two components.')
        for i in range(2):
            for j in range(2):
                # derivative Fourier coefficients: (s + i*c) outer k / 2.
                z=GQ(si[i]*k[j]/2,co[i]*k[j]/2)
                add_term(entries[2*i+j],k,z)
                add_term(entries[2*i+j],(-k[0],-k[1]),z.conj())
    a,b,c,d=entries
    u=add(product(a,a),product(c,c))
    v=add(product(b,b),product(d,d))
    w=add(product(a,b),product(c,d))
    det=add(product(a,d),product(b,c),-1)
    pairs=[(u,u),(v,v),(u,v),(w,w),(u,w),(v,w),(det,u),(det,v),(det,w)]
    av=[mean_product(p,q) for p,q in pairs]
    aa,bb,cc,dd=bg
    u0=aa*aa+cc*cc;v0=bb*bb+dd*dd;w0=aa*bb+cc*dd;q0=aa*dd-bb*cc
    base=[u0*u0,v0*v0,u0*v0,w0*w0,u0*w0,v0*w0,q0*u0,q0*v0,q0*w0]
    return tuple(x-y for x,y in zip(av,base))

if __name__=='__main__':
    zero=((0,0),(0,0))
    one=moment_vector(zero,[Wave((1,0),sine=(1,0))])
    assert one==(Q(3,8),)+(Q(0),)*8
    two=moment_vector(zero,[Wave((1,0),sine=(1,0)),Wave((0,1),sine=(0,1))])
    assert two==(Q(3,8),Q(3,8),Q(1,4))+(Q(0),)*6
    pstar=(1,1,Q(7,2),Q(1,2),0,0,Q(-29,10),Q(-29,10),0)
    assert sum(a*b for a,b in zip(two,pstar))==Q(13,8)
    # Arbitrarily large integer frequencies need no correspondingly large grid.
    large=moment_vector(zero,[Wave((10**12,0),sine=(Q(1,10**12),0))])
    assert large==one
    print('PASS: single-wave, two-wave, retained-energy, and large-frequency identities.')
    print('Two-wave moment vector:',[str(z) for z in two])
