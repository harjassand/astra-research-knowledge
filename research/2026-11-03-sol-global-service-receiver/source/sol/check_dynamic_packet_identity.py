#!/usr/bin/env python3
"""Exact checks of dynamic source-switch accounting and its crossover."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import sympy as sp
from check_monotone_anchor_receiver import block,ff

P=Path(__file__).resolve().parent
RATES=(Q(1),)*4

def packets(x):return (min(x[1:3])//2,min(x[4:6])//2)
def energy(x):return x[0]**2+x[3]**2

@lru_cache(None)
def profile(a,d):
    if max(a,d)<3:return (Q(0),Q(0))
    if a==0:return (Q(6*d-9),)*2
    if d==0:return (Q(6*a-9),)*2
    t=Q((a-1)*(a-2));u=Q((d-1)*(d-2));f=Q(2*d);b=Q(a)
    det=t*u+t*b+f*u;c1=6*a-9;c2=6*d-9
    return ((t*(u+b)*c1+f*u*c2)/det,(b*t*c1+u*(t+f)*c2)/det)

def K(x):
    v=profile(x[0],x[3]);js=packets(x)
    return energy(x)-sum(j*w for j,w in zip(js,v))

def main():
    count=0
    anchors=((1,10),(2,10),(3,10),(10,1),(10,2),(10,3),(10,10),(3,3),(100,10000))
    for a,d in anchors:
        for b,c,e,f in product((0,1,2,3,100),repeat=4):
            x=(a,b,c,d,e,f);js=packets(x);v=profile(a,d);direct=Q(0);switch=Q(0)
            for port,off in enumerate((0,3)):
                for rate,zloc in block(x[off:off+3],RATES):
                    z=list(x);z[off:off+3]=zloc;z=tuple(z)
                    jnew=packets(z);vnew=profile(z[0],z[3])
                    if zloc[0]<x[off]:
                        direct+=rate*(K(z)-K(x))
                        switch-=rate*sum(j*(vn-vo) for j,vn,vo in zip(jnew,vnew,v))
                    else:
                        deltaJ=jnew[port]-js[port];assert deltaJ in (0,1)
                        rhs=energy(z)-energy(x)-deltaJ*v[port]-sum(j*(vn-vo) for j,vn,vo in zip(jnew,vnew,v))
                        assert K(z)-K(x)==rhs
            fw=2*a*d*ff((b,c),(2,2));bw=a*d*ff((e,f),(2,2))
            for rate,sgn in ((fw,1),(bw,-1)):
                if rate:
                    z=(a,b-2*sgn,c-2*sgn,d,e+2*sgn,f+2*sgn)
                    assert K(z)-K(x)==sgn*(v[0]-v[1])
                    direct+=rate*(K(z)-K(x))
            assert direct==switch,(x,direct,switch)
            count+=1
    a,d=sp.symbols('a d',positive=True)
    t=(a-1)*(a-2);u=(d-1)*(d-2);fw=2*d;bw=a
    v1=(t*(u+bw)*(6*a-9)+fw*u*(6*d-9))/(t*u+t*bw+fw*u)
    diff=sp.factor(v1.subs(a,a+1).subs(d,a*a)-v1.subs(d,a*a))
    # Rational leading coefficients avoid numerical extrapolation.
    num,den=sp.fraction(sp.cancel(diff/a));num=sp.Poly(num,a);den=sp.Poly(den,a)
    assert num.degree()==den.degree()
    exact_limit=num.LC()/den.LC();assert exact_limit==-sp.Rational(8,3)
    samples=[]
    for n in (10,100,1000,1000000):
        dv=profile(n+1,n*n)[0]-profile(n,n*n)[0]
        samples.append({'a':n,'d':n*n,'finite_difference_over_a':float(dv/n)})
    out={'scope':'Exact actual-generator identity checks; not a return theorem.',
         'physical_state_checks':count,'symbolic_fixed_d_difference_limit':str(exact_limit),
         'finite_difference_over_a_samples':samples}
    (P/'results/dynamic_packet_identity.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
