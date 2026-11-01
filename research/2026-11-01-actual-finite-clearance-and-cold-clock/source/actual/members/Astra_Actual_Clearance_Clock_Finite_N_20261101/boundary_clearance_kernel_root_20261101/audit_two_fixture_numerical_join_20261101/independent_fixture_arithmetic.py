#!/usr/bin/env python3
"""Arithmetic and failure-ledger checks only until the new admission wrapper is received.

No author code is imported. This file never promotes the pending JSON's status.
"""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib,json

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;SRC=ROOT/'finite_window_consumer'
EXPECTED={
 'compute_pending_windows.py':'2d6df87886ca19ab7f83cf8cd645e0d11d27ebc4fd56932a3741065ac26bbf51',
 'FIXTURE_FAILURE_LEDGER.md':'5ecef7bf9fa54671c64e09106f62587e4d6e0cc55d70d8397b7a11ba6e44c573',
}
hashes={n:hashlib.sha256((SRC/n).read_bytes()).hexdigest() for n in EXPECTED}
assert hashes==EXPECTED
pending=json.loads((SRC/'PENDING_WINDOWS.json').read_text())
assert pending['status']=='PENDING, NOT A CERTIFIED RESULT'
assert [int(row['T']) for row in pending['fixtures']]==[10000,100000]

def sqrt_ceil_binary(x,digits=24):
    """Independent integer bisection certificate, not author's isqrt algorithm."""
    scale=10**digits
    num=x.numerator*scale*scale;den=x.denominator
    lo=0;hi=scale
    while hi*hi*den<num: hi*=2
    while lo<hi:
        mid=(lo+hi)//2
        if mid*mid*den>=num:hi=mid
        else:lo=mid+1
    assert lo*lo*den>=num
    assert lo==0 or (lo-1)**2*den<num
    return F(lo,scale)

def decimal_out(x,digits,upper=False):
    """Signed correct outward decimal; all admitted fixture outputs are positive."""
    scale=10**digits
    n=x.numerator*scale//x.denominator
    if upper and n*x.denominator<x.numerator*scale:n+=1
    sign='-' if n<0 else ''
    n=abs(n)
    return f'{sign}{n//scale}.{n%scale:0{digits}d}'

slo=F('1.106580521912579472');shi=F('1.106580521912579663')
rows=[]
for t,author in zip([10000,100000],pending['fixtures']):
    n=t**5
    r=F(11,20000)+F(4380,19*t)+F(7254,t*t)
    v=F(1449,800*t)+F(1285200,t**3)
    j=F(27,25*t)
    rad=sqrt_ceil_binary(12*v+4*j*j)
    m=2*j+rad
    epsilon=F(1,t)+r+m+F(3000000,t**6)
    lo=slo-epsilon;hi=shi+epsilon+F(5,t)
    assert lo>0 and hi<4
    margin=4-(shi+F(1,t)+r+m+F(1,70*t*t))
    assert margin>0
    computed={
       'scaled_interval':[decimal_out(lo,6),decimal_out(hi,6,True)],
       'physical_interval':[decimal_out(lo*t,6),decimal_out(hi*t,6,True)],
       'residual_upper':decimal_out(r,15,True),'bracket_upper':decimal_out(v,15,True),
       'jump_upper':decimal_out(j,15,True),'martingale_radius_upper':decimal_out(m,15,True),
       'epsilon_upper':decimal_out(epsilon,15,True),
    }
    assert all(author[k]==value for k,value in computed.items())
    # All seven separately named pre-cap exponents.
    pre=[F(n,6200),F(t),F(5*t),F(276),F(t**3-1,20),F(t**3,2500),F(t,80)]
    assert len(pre)==7 and min(pre)>=100
    y=F(n,1920*10**12)-169
    assert y>=50000 and 0<y/n<F(1,1920*10**12)
    assert F(4,3)*64*y/n<1
    entropy_exponent=F(50000**2,520*64**2+1)
    assert entropy_exponent>1000
    assert 160*n*n<2**200
    assert F(n,10**9)-200>1000
    assert min(F(n,64),F(n,96))>=1000
    rows.append({'T':str(t),'N':str(n),**computed,
                 'nonhit_strict_margin_exact':str(margin),
                 'seven_precap_exponents_minimum':str(min(pre)),
                 'entropy_exponent_lower':str(entropy_exponent),
                 'status':'ARITHMETIC_PASS_NOT_YET_SOURCE_BOUND_ADMISSION'})

assert sum((F(6**k,factorial(k)) for k in range(18)),F(0))>400
assert sum((F(4**k,factorial(k)) for k in range(10)),F(0))>50
assert 50**16>6*10**25
assert 7*F(1,2**100)+4*F(1,2**1000)<16*F(1,2**100)
failure=F(1,200)+F(1,10**8)+F(16,2**100)
assert failure<F(1,100)
result={
 'status':'ARITHMETIC_PASS_PENDING_NEW_SOURCE_BOUND_ADMISSION_WRAPPER',
 'source_sha256':hashes,
 'pending_json_sha256':hashlib.sha256((SRC/'PENDING_WINDOWS.json').read_bytes()).hexdigest(),
 'fixtures':rows,'rational_total_failure_upper':str(failure),
 'raw_component_receipts_required':True,
 'new_admission_wrapper_required':True,
 'scalar_source_binding_required':True,
 'cost_scope':'retained-work comparison only; no complete cold speedup follows from measured subtotal',
 'author_general_negative_outward_format_note':'Not signed-correct for negative inputs; irrelevant to the two positive literal fixtures, whose positivity is checked here.',
 'all_arithmetic_assertions_passed':True,
}
(HERE/'ARITHMETIC_RESULTS_PENDING_ADMISSION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
