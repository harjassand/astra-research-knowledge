#!/usr/bin/env python3
"""A 96-input raw fixture, with an independent elliptic recurrence count.
No 2^96 truth table or 2^32 field enumeration is used.
"""
import json, random, sys
from pathlib import Path
from field_descent import *

h=0x10000008d; d=32; n=3*d; q=1<<d
# Rabin irreducibility check for this explicit test-input presentation.
def pgcd(a,b):
    while b:
        r=a
        while r and r.bit_length()>=b.bit_length(): r^=b<<(r.bit_length()-b.bit_length())
        a,b=b,r
    return a
assert gf_pow(2,1<<d,h)==2 and pgcd(gf_pow(2,1<<(d//2),h)^2,h)==1
rng=random.Random(32001)
u,v,w=[rng.randrange(q) for _ in range(3)]
planted={(1,1,1):1,(1,1,0):w,(1,0,1):v,(0,1,1):u,
 (1,0,0):1^gf_mul(v,w,h),(0,1,0):1^gf_mul(u,w,h),(0,0,1):1^gf_mul(u,v,h),
 (0,0,0):gf_mul(gf_mul(u,v,h),w,h)^u^v^w}
columns=random_invertible(n,rng); offset=rng.randrange(1<<n)
def evaluator(x):
    y=linear_apply(columns,x)^offset
    fields=[(y>>(d*i))&(q-1) for i in range(3)]
    return gf_trace(field_polynomial_value(planted,fields,h),h)
print(json.dumps({'stage':'construct_raw_anf','original_variables':n}),flush=True)
raw=extract_anf(evaluator,n)
print(json.dumps({'stage':'acquire_and_count','raw_anf_terms':len(raw)}),flush=True)
result=compile_raw(raw,n)
k0,k1=-2,1
for j in range(2,d+1): k0,k1=k1,-k1-2*k0
reference=q*k1
assert result['signed_count']==reference
fpoly={tuple(x['exponents']):x['coefficient'] for x in result['field_polynomial']}
for _ in range(256):
    y=rng.randrange(1<<n); x=linear_apply(result['coordinate_columns'],y)
    fields=[(y>>(d*i))&(q-1) for i in range(3)]
    assert polynomial_value(raw,x)==evaluator(x)
    assert polynomial_value(raw,x)==gf_trace(field_polynomial_value(fpoly,fields,result['field_modulus']),result['field_modulus'])
result.update(independent_reference='K_d(1)=-K_(d-1)(1)-2K_(d-2)(1), K_0=-2,K_1=1',
 independent_reference_count=reference,reference_kloosterman=k1,
 random_original_and_acquired_checks=256,planted_modulus=h,
 planted_polynomial=[{'exponents':list(e),'coefficient':c} for e,c in sorted(planted.items())],
 planted_affine_columns=columns,planted_affine_offset=offset,whole_field_enumerations=0,
 whole_boolean_cube_enumerations=0,practical_speed_claim=False)
Path(__file__).with_name('field_descent_96_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['original_variables','raw_cubic_terms','centroid_dimension','signed_count','zero_count','seconds','reference_kloosterman']}),flush=True)
