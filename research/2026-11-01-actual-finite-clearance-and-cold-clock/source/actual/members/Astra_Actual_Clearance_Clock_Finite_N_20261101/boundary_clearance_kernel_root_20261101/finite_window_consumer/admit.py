#!/usr/bin/env python3
"""Source-bound, exact-rational two-fixture clearance receiver.
All mathematical source and receipt files must match the supplied binding.
No trajectory sampling, dynamic source loading, or source-product loops.
"""
from fractions import Fraction as Q
from math import isqrt, factorial
import json
import hashlib
import argparse
from pathlib import Path

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
    if x<0: raise ValueError('This fixture formatter requires nonnegative endpoints.')
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
            'status':'ADMITTED_UNDER_BOUND_SOURCE_THEOREMS',
            'scaled_interval':[outward(lo,6,False),outward(hi,6,True)],
            'physical_interval':[outward(lo*t,6,False),outward(hi*t,6,True)],
            'residual_upper':outward(r,15,True),
            'bracket_upper':outward(v,15,True),
            'jump_upper':outward(j,15,True),
            'martingale_radius_upper':outward(m,15,True),
            'epsilon_upper':outward(eps,15,True),
            'total_failure_upper':'<1/100',
            'output_scope':'First S<=15(N+2)/16 hitting time, model time units; no physical preparation',
            'cold_speedup_claim':False}

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
def receive_sources():
    here=Path(__file__).resolve().parent
    root=here.parent.parent
    manifest_bytes=(here/'ADMISSION_SOURCE_BINDINGS.json').read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest()!='fee8f271579ea33764074c824624c8b1882f8602a9fdeb8aac9ac575f5848f48':
        raise ValueError('The reviewed admission source manifest does not match.')
    manifest=json.loads(manifest_bytes)
    if manifest.get('status')!='ALL_REQUIRED_COMPONENTS_RECEIVED':
        raise ValueError('Mathematical component admission is incomplete.')
    seen=set()
    for row in manifest['files']:
        name=row['path']
        if name in seen or Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('Invalid or duplicate source binding.')
        seen.add(name)
        data=(root/name).read_bytes()
        if hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise ValueError('Source binding mismatch: '+name)
        if 'accepted_status' in row:
            if json.loads(data).get(row.get('accepted_status_key','status'))!=row['accepted_status']:
                raise ValueError('Required mathematical receipt is not accepted: '+name)
    if len(seen)<20:
        raise ValueError('Incomplete source closure.')
    return len(seen)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--T',choices=['10000','100000'])
    args=parser.parse_args()
    try:
        count=receive_sources()
        ts=[int(args.T)] if args.T else [10000,100000]
        result={'status':'ADMITTED_UNDER_BOUND_SOURCE_THEOREMS',
                'source_files_verified':count,
                'confidence_lower':'99%',
                'same_path':'Raw corner to first macro/gate/budget stop or original4T; actual entropy5 continuation',
                'fixtures':[compute(t) for t in ts]}
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(json.dumps({'status':'UNKNOWN','reason':str(exc)},indent=2))
        raise SystemExit(2)
    print(json.dumps(result,indent=2))
