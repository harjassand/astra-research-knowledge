#!/usr/bin/env python3
"""Exact target-alignment and negative control, separate from purity tests."""
from fractions import Fraction as F
from pathlib import Path
import datetime,hashlib,json,time


def chart_vector(t,s):
    r=t[0]**2+t[1]**2
    return [2*t[0]/(1+r),2*t[1]/(1+r),s*(1-r)/(1+r)]


def standard_density(b):
    # Complex off-diagonals represented by (real, imaginary) pairs.
    return [[((1+b[2])/2,F(0)),(b[0]/2,-b[1]/2)],
            [(b[0]/2,b[1]/2),((1-b[2])/2,F(0))]]


begin=time.monotonic(); comparisons=0; cases=0
for p,amplitude in [(F(0),F(0)),(F(1),F(0)),
                    (F(1,5),F(2,5)),(F(4,5),F(2,5))]:
    for cosine,sine in [(F(1),F(0)),(F(0),F(1)),
                       (-F(1),F(0)),(F(0),-F(1))]:
        b=[2*amplitude*cosine,2*amplitude*sine,1-2*p]
        s=1 if b[2]>=0 else -1
        t=[b[0]/(1+abs(b[2])),b[1]/(1+abs(b[2]))]
        assert chart_vector(t,s)==b
        target=[[(1-p,F(0)),(amplitude*cosine,-amplitude*sine)],
                [(amplitude*cosine,amplitude*sine),(p,F(0))]]
        assert standard_density(chart_vector(t,s))==target
        assert target[0][0][0]==1-p and target[1][1][0]==p
        comparisons+=7; cases+=1
wrong_at_p0=standard_density([F(0),F(0),-F(1)])
assert wrong_at_p0[0][0][0]==0 and wrong_at_p0[1][1][0]==1
assert wrong_at_p0!=standard_density([F(0),F(0),F(1)])
comparisons+=3
result={'status':'PASS','exact_target_cases':cases,'counted_exact_comparisons':comparisons,
        'target_probabilities':['0','1','1/5','4/5'],
        'wrong_sign_control':'FAILS target alignment at p0 as intended',
        'elapsed_seconds':time.monotonic()-begin,
        'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'corrected standard Bloch-target interface only, no hardware'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
