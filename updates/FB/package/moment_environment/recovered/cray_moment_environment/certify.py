"""Exact rational certificate for a symmetric flat-bath uncertainty bound.
No floating-point eigenvalues enter the certificate. Roots of diagonal-plus-
rank-one matrices are isolated using rational secular equations, followed by
integer square-root bounds. Python's standard library suffices.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path


def scalar_envelopes():
    x=[F(1)]
    while x[-1]>F(1,10000):
        x.append(x[-1]*F(2,3))
    edges=[F(0)]+list(reversed(x))
    lower={}; upper={}
    for a,b in zip(edges[:-1],edges[1:]):
        w=(b-a)/8
        t=(b**3-a**3)/24
        s=t/w
        lower[s]=lower.get(s,F(0))+w
        aa,bb=a*a,b*b
        wa=(bb*w-t)/(bb-aa)
        wb=(t-aa*w)/(bb-aa)
        for s,q in [(aa,wa),(bb,wb)]:
            if q: upper[s]=upper.get(s,F(0))+q
    return edges,sorted(lower.items()),sorted(upper.items())


def secular_sign(x,atoms,bits=160):
    """Sign of 1 + sum w/(s-x), using certified integer fixed-point sums."""
    scale=1<<bits
    lower=scale
    for s,w in atoms:
        if s==x: raise ValueError('Secular equation evaluated at a pole')
        r=w/(s-x)
        lower+=(r.numerator*scale)//r.denominator
    upper=lower+len(atoms)
    if lower>0: return 1
    if upper<0: return -1
    exact=1+sum((w/(s-x) for s,w in atoms),F(0))
    return (exact>0)-(exact<0)


def root_intervals(atoms,bits=110):
    """Interlacing isolates every eigenvalue of diag(s)+sqrt(w)sqrt(w)^T."""
    nodes=[s for s,w in atoms]
    upper_last=nodes[-1]+sum((w for s,w in atoms),F(0))
    tol=F(1,1<<bits)
    out=[]
    for i,left in enumerate(nodes):
        right=nodes[i+1] if i+1<len(nodes) else upper_last
        while right-left>tol:
            mid=(left+right)/2
            sign=secular_sign(mid,atoms)
            if sign<0: left=mid
            elif sign>0: right=mid
            else:
                left=right=mid
                break
        out.append((left,right))
    return out


def sqrt_interval(x,bits=130):
    if x<0: raise ValueError('Negative radicand')
    scale=1<<bits
    k=isqrt((x.numerator*scale*scale)//x.denominator)
    low=F(k,scale)
    return low,(low if low*low==x else F(k+1,scale))


def free_energy_interval(atoms):
    roots=root_intervals(atoms)
    lo=hi=F(0)
    for s,w in atoms:
        a,b=sqrt_interval(s)
        lo+=a; hi+=b
    for left,right in roots:
        a,_=sqrt_interval(left)
        _,b=sqrt_interval(right)
        lo-=b; hi-=a
    return (lo,hi),roots


def outward_decimal(x,places=14,upper=False):
    scale=10**places
    k=(x.numerator*scale)//x.denominator
    if upper and F(k,scale)<x: k+=1
    sign='-' if k<0 else ''
    mag=abs(k)
    return f'{sign}{mag//scale}.{mag%scale:0{places}d}'


def main():
    edges,low,high=scalar_envelopes()
    el,rl=free_energy_interval(low)
    eh,rh=free_energy_interval(high)
    radius=(el[0]-eh[1],el[1]-eh[0])
    assert radius[0]>0
    out={
        'method':'exact rational secular interlacing and integer square-root enclosure',
        'model':'symmetric flat coupling measure dM(e)=de/16 on [-1,1]',
        'impurity_modes_for_scalar_certificate':1,
        'bin_count':len(edges)-1,
        'moment_types':['pair-total mass','pair-total squared-energy moment'],
        'reference_physical_bath_modes':2*len(low),
        'adversarial_physical_bath_modes':2*len(high)-1,
        'radius_decimal_lower':outward_decimal(radius[0]),
        'radius_decimal_upper':outward_decimal(radius[1],upper=True),
        'radius_fraction_lower':str(radius[0]),'radius_fraction_upper':str(radius[1]),
        'edges':[str(x) for x in edges],
        'lower_gamma_atoms':[[str(s),str(w)] for s,w in low],
        'upper_gamma_atoms':[[str(s),str(w)] for s,w in high],
        'lower_gamma_root_intervals':[[str(a),str(b)] for a,b in rl],
        'upper_gamma_root_intervals':[[str(a),str(b)] for a,b in rh],
        'reference_energy_interval':[str(x) for x in el],
        'adversarial_energy_interval':[str(x) for x in eh]
    }
    Path(__file__).with_name('exact_certificate.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ['edges','lower_gamma_atoms','upper_gamma_atoms','lower_gamma_root_intervals','upper_gamma_root_intervals','reference_energy_interval','adversarial_energy_interval','radius_fraction_lower','radius_fraction_upper']},indent=2))

if __name__=='__main__': main()
