#!/usr/bin/env python3
"""Exact rational arithmetic prototype. NOT ADMITTED before dependency receipt.
No trajectory sampling, dynamic source loading, exponentials, or E-term loops.
"""
from fractions import Fraction as Q
from math import isqrt, factorial
import json

SLO=Q('1.106580521912579472')
SHI=Q('1.106580521912579663')

def sqrt_up(x, digits=24):
    scale=10**digits
    n=isqrt(x.numerator*scale*scale//x.denominator)
    if Q(n*n,scale*scale)<x:n+=1
    y=Q(n,scale)
    assert y*y>=x
    assert n==0 or Q((n-1)**2,scale**2)<x
    return y

def outward(x,digits,upper):
    scale=10**digits
    n=x.numerator*scale//x.denominator
    if upper and Q(n,scale)<x:n+=1
    return f'{n//scale}.{n%scale:0{digits}d}'

def compute(t):
    if t not in (10000,100000):
        raise ValueError('Only two source-bound fixture populations are proposed.')
    r=Q(11,20000)+Q(4380,19*t)+Q(7254,t*t)
    v=Q(1449,800*t)+Q(1285200,t**3)
    j=Q(27,25*t)
    m=2*j+sqrt_up(12*v+4*j*j)
    eps=Q(1,t)+r+m+Q(3000000,t**6)
    assert SHI+Q(1,t)+r+m+Q(1,70*t*t)<4
    lo=SLO-eps; hi=SHI+eps+Q(5,t)
    return {'N':str(t**5),'T':str(t),
            'status':'AUTHOR_PENDING_COMPONENT_RECEIPTS',
            'scaled_interval':[outward(lo,6,False),outward(hi,6,True)],
            'physical_interval':[outward(lo*t,6,False),outward(hi*t,6,True)],
            'residual_upper':outward(r,15,True),
            'bracket_upper':outward(v,15,True),
            'jump_upper':outward(j,15,True),
            'martingale_radius_upper':outward(m,15,True),
            'epsilon_upper':outward(eps,15,True),
            'proposed_total_failure':'<1/100 ONLY AFTER SOURCE-BOUND ADMISSION'}

assert sum(Q(6**k,factorial(k)) for k in range(18))>400
assert sum(Q(4**k,factorial(k)) for k in range(10))>50
assert 50**16>6*10**25
assert 160*10**50<2**200
assert Q(50000**2,520*64**2+1)>1000
assert Q(1,200)+Q(1,10**8)+Q(16,2**100)<Q(1,100)
for _t in (10000,100000):
    _n=_t**5; _y=Q(_n,1920*10**12)-169
    assert _y>=50000 and _y/_n<Q(1,1920*10**12)
    assert min(Q(_n,6200),_t,5*_t,276,Q(_t**3-1,20),Q(_t**3,2500),Q(_t,80))>=100
if __name__=='__main__':
    print(json.dumps({'status':'PENDING, NOT A CERTIFIED RESULT',
                      'fixtures':[compute(t) for t in (10000,100000)]},indent=2))
