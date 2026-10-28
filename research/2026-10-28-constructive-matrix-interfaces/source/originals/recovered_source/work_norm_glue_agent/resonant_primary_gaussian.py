#!/usr/bin/env python3
"""Closed residual Gaussian for translation-resonant irreducible primary types.

The trace refinement may be an arbitrary Boolean ANF: it is evaluated at
one manufactured field element. No matrix or field point is enumerated.
This does not by itself evaluate the full arbitrary-shape cubic count.
"""
from pathlib import Path
from fractions import Fraction
from math import comb
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_norm_glue_agent','work_norm_frontier_agent')]
from nonresonant_primary_gaussian import shifted_polynomial, value
from matrix_kloosterman import Field, factor_polynomial


class ResonantPrimaryGaussian:
    def __init__(self,field_h,irreducible,beta,eta=0):
        self.F=F=Field(field_h);self.f=f=tuple(irreducible);self.d=d=len(f)-1
        if d<1 or f[-1]!=1 or any(type(x) is not int or not 0<=x<F.q for x in f):
            raise ValueError('monic polynomial over the supplied field required')
        if not 0<beta<F.q or not 0<=eta<F.q:
            raise ValueError('valid nonzero beta and eta required')
        if factor_polynomial(list(f),F)!=[(list(f),1)]:
            raise ValueError('irreducible polynomial required')
        if shifted_polynomial(f,beta,F)!=list(f):
            raise ValueError('the primary is not beta-resonant')
        if d%2:raise AssertionError('translation-resonant irreducible has odd degree')
        self.beta=beta;self.eta=eta;self.Q=F.q**d
        self.ratio=F.mul(eta,F.inv(beta))
        self.top=[f[d-j] if j<=d else 0 for j in range(4)]
        self.metadata=dict(field_modulus=field_h,irreducible=list(f),
            residue_degree=d,beta=beta,eta=eta,
            unperturbed_Gaussian_sign=1,enumerated_field_elements=0,
            enumerated_matrices=0,uniform_polynomial_time=True)

    def characteristic_top(self,m):
        """Top three elementary coefficients of f^m; period four."""
        if type(m) is not int or m<0:raise ValueError('nonnegative multiplicity required')
        result=[1,0,0,0]
        for _ in range(m%4):
            product=[0]*4
            for i in range(4):
                for j in range(4-i):
                    product[i+j]^=self.F.mul(result[i],self.top[j])
            result=product
        return result

    def trace_support(self,m):
        tau=self.characteristic_top(m)[1]
        return self.F.mul(self.ratio,tau)

    def periodic_sign(self,m,phi=()):
        phi=set(phi);F=self.F
        if any(type(x) is not int or x<0 or x.bit_length()>F.a for x in phi):
            raise ValueError('explicit Boolean ANF on field coordinates required')
        _,tau,e2,e3=self.characteristic_top(m)
        coefficient=F.mul(self.beta^tau,e2)^e3
        phase=F.trace(F.mul(F.mul(self.ratio,self.ratio),coefficient))
        phase^=value(phi,F.mul(self.ratio,tau))
        return 1-2*phase

    def gaussian(self,shape,phi=()):
        shape=tuple(shape)
        if any(type(x) is not int or x<=0 for x in shape) or tuple(sorted(shape,reverse=True))!=shape:
            raise ValueError('explicit nonincreasing positive primary block lengths required')
        m=sum(shape);nstat=sum(i*x for i,x in enumerate(shape));b=self.d*m
        z=self.d*(m+2*nstat)
        return self.periodic_sign(m,phi)*self.F.q**((b*b+z)//2)

    def normalized(self,shape,phi=()):
        shape=tuple(shape);m=sum(shape);nstat=sum(i*x for i,x in enumerate(shape))
        # Validate all supplied data through the full formula.
        actual=self.gaussian(shape,phi);b=self.d*m
        result=self.periodic_sign(m,phi)*self.Q**(m+nstat)
        assert result*self.F.q**(b*(b-1)//2)==actual
        return result

    def quotient_power_moment(self,rho):
        """The eta=p=0 quotient functional in primary power-sum coordinates.

        Its exact Hall-dual kernel is sum_lambda P_lambda(Q X;1/Q).
        Independent Gaussian power moments avoid quotient partition lists.
        """
        rho=tuple(rho);result=Fraction(1)
        for r in set(rho):
            if type(r) is not int or r<1:raise ValueError('positive power-sum indices required')
            mean=self.Q**r if r%2 else self.Q**(r//2)
            variance=r*(self.Q**(2*r)-self.Q**r)
            count=rho.count(r);previous=1;current=mean
            if not count:continue
            for j in range(2,count+1):
                previous,current=current,mean*current+(j-1)*variance*previous
            result*=current
        return result
