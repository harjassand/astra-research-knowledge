#!/usr/bin/env python3
"""Exact enclosure for source-derived LWW qubit strong-regularity failure."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

# Independent rational enclosures; arithmetic endpoints remain exact Fractions.
# The radicals are bounded first, then monotonicity bounds the scalar functions.
N=10**40
def sqrt_bounds(x):
    x=F(x); k=isqrt(x.numerator*N*N//x.denominator)
    lo=F(k,N); hi=F(k+1,N)
    assert lo*lo<=x<=hi*hi
    return lo,hi
def series_bounds(x,n=700):
    # x is an exact nonnegative rational less than 1.
    assert 0<=x<1
    z=x*x; y=F(1); s=F(0)
    for k in range(n):
        s+=y/(2*k+1); y*=z
    return s, s+y/((2*n+1)*(1-z))
def coarse(x,den=10**30,upper=False):
    a=x.numerator*den; b=x.denominator
    return F(-((-a)//b) if upper else a//b,den)

# Bound atanh(r)/r monotonically using r=sqrt(89)/10.
# Rounding radicals outward to 12 decimals keeps rational series inexpensive.
rlo,rhi=sqrt_bounds(F(89,100))
rlo=coarse(rlo,10**12);rhi=coarse(rhi,10**12,True)
fl=series_bounds(rlo)[0];fu=series_bounds(rhi)[1]
ll,lu=series_bounds(F(1,3));ll*=F(2,3);lu*=F(2,3)
Jlo=ll/2+F(7,100)*fl; Jhi=lu/2+F(7,100)*fu
alo,ahi=sqrt_bounds(11)
# E=(10-sqrt11)/(4(10+sqrt11)) is decreasing in sqrt11.
Elo=(10-ahi)/(4*(10+ahi));Ehi=(10-alo)/(4*(10+alo))
gaplo=Jlo-4*Ehi;gaphi=Jhi-4*Elo
assert gaphi < -F(24,1000)

out={'source':'Liu-Wan-Wu arXiv:2609.13726v1, section5 generator, with independently chosen rational input state.',
     'status':'Root exact rational certificate for an internally reconstructed consequence; source does not itself state this endpoint failure.',
     'sigma':[['1/5','0'],['0','4/5']], 'rho':[['1/4','-2/5'],['-2/5','3/4']],
     'V':[[0,1],[2,0]],
     'E_exact':'(10-sqrt(11))/(4*(10+sqrt(11)))',
     'J_exact':'log(2)/2 + 7/(20*sqrt(89))*log((10+sqrt(89))/(10-sqrt(89)))',
     'J_bounds':[str(coarse(Jlo)),str(coarse(Jhi,upper=True))],
     'E_bounds':[str(coarse(Elo)),str(coarse(Ehi,upper=True))],
     'J_minus_4E_bounds':[str(coarse(gaplo)),str(coarse(gaphi,upper=True))],
     'verified_gap_less_than':'-3/125',
     'arithmetic':'Exact Python integer/Fraction; monotone 700-term positive atanh series and rigorous geometric remainder; integer square-root bounds.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
