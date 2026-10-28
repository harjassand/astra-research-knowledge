"""Acquire a rational-enclosed 48-node Gaussian quadrature, not an oracle.

Floating leggauss supplies root proposals only. Exact polynomial signs isolate
all roots; rational interval differentiation supplies positive weights.
All trigonometric coefficients are enclosed by rational Taylor remainders.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import math
import time
import numpy as np

HERE=Path(__file__).resolve().parent
Q=48;BITS=48;D=1<<BITS;ORDER=24;STEPS=512


class I:
    def __init__(self,l,u=None):self.l=F(l);self.u=F(l if u is None else u);assert self.l<=self.u
    def __add__(self,b):
        b=b if isinstance(b,I) else I(b);return I(self.l+b.l,self.u+b.u)
    __radd__=__add__
    def __neg__(self):return I(-self.u,-self.l)
    def __sub__(self,b):return self+-as_i(b)
    def __rsub__(self,b):return as_i(b)+-self
    def __mul__(self,b):
        b=as_i(b);v=[x*y for x in [self.l,self.u] for y in [b.l,b.u]];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=as_i(b);assert b.l*b.u>0
        return self*I(1/b.u,1/b.l)
    def __rtruediv__(self,b):return as_i(b)/self
    def dyadic(self):return [self.l.numerator*D//self.l.denominator,-((-self.u.numerator*D)//self.u.denominator)]
    def encode(self):return [str(self.l),str(self.u)]


def as_i(x):return x if isinstance(x,I) else I(x)
def poly(coeff,x):
    y=I(0) if isinstance(x,I) else F(0)
    for c in reversed(coeff):y=y*x+c
    return y
def pi_i():
    def atan(n):
        a=2*48
        s=sum((F((-1)**j,(2*j+1)*n**(2*j+1)) for j in range(48)),F(0))
        e=F(1,97*n**97);return I(s-e,s+e)
    return 16*atan(5)-4*atan(239)
def trig(x,sine=False):
    # Quantize just the argument for a cheap exact rational polynomial.
    mid=(x.l+x.u)/2;q=mid.numerator*(1<<80)//mid.denominator;y=F(q,1<<80)
    argerr=max(abs(y-x.l),abs(y-x.u))
    coeff=[F((-1)**j,math.factorial(2*j+(1 if sine else 0))) for j in range(41)]
    ans=poly(coeff,y*y)*(y if sine else 1)
    degree=83 if sine else 82
    err=argerr+F(4**degree,math.factorial(degree))
    return I(ans-err,ans+err)


def main():
    started=time.perf_counter()
    coeff=[0]*(Q+1)
    for k in range(Q//2+1):coeff[Q-2*k]=(-1)**k*math.comb(Q,k)*math.comb(2*Q-2*k,Q)
    deriv=[(i+1)*coeff[i+1] for i in range(Q)]
    proposals=np.polynomial.legendre.leggauss(Q)[0]
    pi=pi_i();rows=[];proof=[];previous=F(-1);sign_checks=0
    for v in proposals:
        center=F(float(v));lo=center-F(1,1<<40);hi=center+F(1,1<<40)
        fl=poly(coeff,lo);fh=poly(coeff,hi)
        assert lo>previous and fl*fh<0
        for _ in range(80):
            mid=(lo+hi)/2;fm=poly(coeff,mid)
            if fl*fm<0:hi=mid;fh=fm
            else:lo=mid;fl=fm
        sign_checks+=82;previous=hi
        x=I(lo,hi);dp=poly(deriv,x)/(1<<Q)
        assert dp.l*dp.u>0
        weight=1/((1-x*x)*dp*dp) # usual Gauss weight/2, normalized probability
        assert weight.l>0
        k=x*pi/2
        f1=trig(k);g1=trig(k,True);f2=trig(2*k,True);g2=trig(2*k)
        row=[*weight.dyadic(),*f1.dyadic(),*g1.dyadic(),*f2.dyadic(),*g2.dyadic()]
        rows.append(row)
        proof.append({'root':x.encode(),'normalized_weight':weight.encode(),'fixed_intervals':row})
    mass=sum((I(F(r[0],D),F(r[1],D)) for r in rows),I(0))
    assert mass.l<=1<=mass.u
    rx=math.isqrt(3*(1<<(2*BITS-2)))
    assert F(rx,D)**2<=F(3,4)<F(rx+1,D)**2
    text=f'{Q} {STEPS} {ORDER} {BITS} {rx}\n'+'\n'.join(' '.join(map(str,row)) for row in rows)+'\n'
    (HERE/'QUADRATURE.txt').write_text(text)
    out={'nodes':Q,'fixed_fractional_bits':BITS,'Taylor_order':ORDER,'time_steps':STEPS,
         'time_step':'1/1024','interaction_clock':'1/2','source_size':'2^128',
         'source_coupling':'N^-8 = 2^-1024','a1':'1','a2':'1/3',
         'roots_certified_by':'48 disjoint sign-changing intervals of exact degree48 Legendre polynomial; no numerical roots used as premises.',
         'root_sign_evaluations':sign_checks,'root_refinement_bisections':80,
         'pi_interval':pi.encode(),'quadrature_mass_enclosure':mass.encode(),
         'initial_Bloch_rx':{'dyadic_floor':rx,'exact':'sqrt(3)/2','error_upper':'2^-48'},
         'parameters_sha256':hashlib.sha256(text.encode()).hexdigest(),'node_proofs':proof,
         'seconds_after_imports':time.perf_counter()-started,
         'source_model_or_state_sampling':0}
    (HERE/'QUADRATURE_ACQUISITION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['node_proofs','pi_interval']},indent=2))


if __name__=='__main__':main()
