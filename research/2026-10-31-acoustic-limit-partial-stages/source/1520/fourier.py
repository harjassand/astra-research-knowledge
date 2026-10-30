"""Actual finite Fourier gradients with exact Gaussian rational coefficients."""
from dataclasses import dataclass
from fractions import Fraction as R
from kernel import data
from receive import r,b
m=r.m
@dataclass(frozen=True)
class Gaussian:
    real:R=R(0)
    imag:R=R(0)
    @staticmethod
    def lift(x):return x if isinstance(x,Gaussian) else Gaussian(R(x))
    def __add__(self,other):
        z=self.lift(other);return Gaussian(self.real+z.real,self.imag+z.imag)
    __radd__=__add__
    def __neg__(self):return Gaussian(-self.real,-self.imag)
    def __sub__(self,other):return self+-self.lift(other)
    def __rsub__(self,other):return self.lift(other)+-self
    def __mul__(self,other):
        z=self.lift(other);return Gaussian(self.real*z.real-self.imag*z.imag,self.real*z.imag+self.imag*z.real)
    __rmul__=__mul__
    def __bool__(self):return bool(self.real or self.imag)

def gradient(modes):
    G=[{} for _ in range(4)]
    for mode in modes:
        k=tuple(mode['frequency']);ss=list(map(R,mode.get('sine',[0,0])));cc=list(map(R,mode.get('cosine',[0,0])))
        assert len(k)==2 and all(isinstance(x,int) for x in k) and k!=(0,0) and len(ss)==len(cc)==2
        for i in range(2):
            for j in range(2):
                for sign in (-1,1):
                    ff=tuple(sign*v for v in k);z=Gaussian(ss[i]*k[j]/2,sign*cc[i]*k[j]/2);G[2*i+j]=m.add(G[2*i+j],{ff:z})
    return G

def average(poly,G):
    z=Gaussian.lift(m.average(poly,G));assert not z.imag;return z.real

def moments(modes):
    d=data();G=gradient(modes)
    S=[[average(b.mul(b.var(4,i),b.var(4,j)),G) for j in range(4)] for i in range(4)]
    ell=[average(P,G) for P in d['polys']];f=average(d['F'],G);T4=average(b.mul(d['T'],d['T']),G)
    return {'gradient':G,'covariance':S,'cubic_target':ell,'quartic_moment':f,'radial_fourth_moment':T4}
