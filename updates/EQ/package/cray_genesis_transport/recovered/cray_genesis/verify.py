"""Independent exact-arithmetic verifier for the supplied transport certificates.
Uses only the Python standard library. No optimizer, spectral gap, or simulation.
The variational theorem and orbit-cancellation proof are stated in README.md.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path
import sys
import time

def add_term(poly: dict, shape: frozenset, coefficient: int) -> None:
    poly[shape] = poly.get(shape, 0) + coefficient
    if poly[shape] == 0:
        del poly[shape]

def canonical(shape: frozenset[int]) -> tuple[int, ...]:
    if not shape:
        return ()
    first = min(shape)
    return tuple(sorted(x - first for x in shape))

def swap_gradient_sum(shape: frozenset[int]) -> dict[frozenset[int], int]:
    result = {}
    for shift in {-x for x in shape} | {1-x for x in shape}:
        translated = frozenset(x+shift for x in shape)
        if (0 in translated) == (1 in translated):
            continue
        exchanged = ((translated - {0}) | {1}) if 0 in translated else ((translated - {1}) | {0})
        add_term(result, exchanged, 1)
        add_term(result, translated, -1)
    return result

def verify_lower(data: dict) -> Fraction:
    """Certify q=(eta_0-eta_1)(1-eta_-1 eta_2)*g and evaluate its dual value."""
    density = Fraction(data['density'])
    P, B = density.numerator, density.denominator
    scale = int(data['scale'])
    outer = tuple(data['dual']['outer'])
    index = {x:j for j,x in enumerate(outer)}
    if 0 in index or 1 in index or -1 not in index or 2 not in index:
        raise ValueError('Invalid bond environment.')
    terms = [(frozenset(item['shape']), int(item['numerator'])) for item in data['dual']['terms']]
    # Reconstruct q in raw, squarefree occupation monomials and check every orbit.
    qpoly = {}
    for shape, coefficient in terms:
        if not shape <= set(outer):
            raise ValueError('Dual monomial outside its declared environment.')
        for site, sign in [(0,1),(1,-1)]:
            add_term(qpoly, shape | {site}, sign*coefficient)
            add_term(qpoly, shape | {site,-1,2}, -sign*coefficient)
    orbit = defaultdict(int)
    for shape, coefficient in qpoly.items():
        orbit[canonical(shape)] += coefficient
    if any(orbit.values()):
        raise AssertionError('Dual current does not annihilate translation orbits.')
    # Boolean zeta transform, using unbounded Python integers.
    values = [0]*(1 << len(outer))
    for shape, coefficient in terms:
        values[sum(1 << index[x] for x in shape)] += coefficient
    for bit in range(len(outer)):
        step = 1 << bit
        for start in range(0, len(values), 2*step):
            for offset in range(step):
                values[start+step+offset] += values[start+offset]
    forbidden = (1 << index[-1]) | (1 << index[2])
    numerator = 0
    for state, value in enumerate(values):
        if state & forbidden == forbidden:
            continue # c=0 => current exactly zero.
        occupied = state.bit_count()
        weight = P**occupied*(B-P)**(len(outer)-occupied)
        numerator += weight*(2*value*scale-value*value)
    return Fraction(numerator, B**len(outer)*scale**2)

def verify_upper(data: dict) -> Fraction:
    """Evaluate the Dirichlet trial functional by exact local orthogonality."""
    density=Fraction(data['density']); P,B=density.numerator,density.denominator
    scale=int(data['scale'])
    # Centered monomials h_A=product(eta_i-p), with rational trial coefficients.
    gradient={}
    for item in data['primal']['terms']:
        shape=frozenset(item['shape']); coefficient=int(item['numerator'])
        for a,v in swap_gradient_sum(shape).items():
            add_term(gradient,a,coefficient*v)
    grouped={}
    for shape,coefficient in gradient.items():
        outside=shape-{-1,2}
        if not outside:
            raise AssertionError('Unexpected zero-degree outside factor.')
        mask=int(-1 in shape)+2*int(2 in shape)
        grouped.setdefault(outside,[0,0,0,0])[mask]+=coefficient
    grouped.setdefault(frozenset({0}),[0,0,0,0])
    grouped.setdefault(frozenset({1}),[0,0,0,0])
    degree=max(map(len,grouped))
    numerator=0
    for outside, coefficients in grouped.items():
        s=len(outside)
        current=int(outside==frozenset({0}))-int(outside==frozenset({1}))
        for u,v in [(0,0),(0,1),(1,0)]: # Exactly the allowed rate contexts.
            h1,h2=u*B-P,v*B-P
            factors=[B*B,h1*B,h2*B,h1*h2]
            value=current*scale*B*B+sum(a*b for a,b in zip(coefficients,factors))
            weight=(P*(B-P))**(s-1)*P**(u+v)*(B-P)**(2-u-v)
            numerator+=weight*value*value*B**(2*(degree-s))
    return Fraction(numerator,2*scale**2*B**(2*degree+4))

def outward_decimal(value: Fraction, places: int, upper: bool = False) -> str:
    factor=10**places
    n,d=value.numerator*factor,value.denominator
    scaled=(n+d-1)//d if upper else n//d
    whole,frac=divmod(scaled,factor)
    return f'{whole}.{frac:0{places}d}'

def verify_file(path: Path) -> dict:
    started=time.perf_counter()
    data=json.loads(path.read_text())
    lo=verify_lower(data);hi=verify_upper(data)
    if not lo<=hi:
        raise AssertionError('Inconsistent variational interval.')
    if data.get('lower_fraction') and lo != Fraction(data['lower_fraction']):
        raise AssertionError('Stored lower endpoint mismatch.')
    if data.get('upper_fraction') and hi != Fraction(data['upper_fraction']):
        raise AssertionError('Stored upper endpoint mismatch.')
    return {'density':data['density'],'lower':outward_decimal(lo,12),
            'upper':outward_decimal(hi,12,True),'width':float(hi-lo),
            'lower_fraction':str(lo),'upper_fraction':str(hi),
            'verification_seconds':time.perf_counter()-started}

if __name__=='__main__':
    paths=[Path(p) for p in sys.argv[1:]] or sorted(Path(__file__).parent.glob('certificate_*.json'))
    if not paths:raise SystemExit('No certificates found.')
    for path in paths:
        result=verify_file(path)
        print(f"{path.name}: p={result['density']}  [{result['lower']}, {result['upper']}]  "
              f"width={result['width']:.4g}  verified in {result['verification_seconds']:.3f} s")
