#!/usr/bin/env python3
"""Additional raw-input challenges, independent of receipt mutation tests."""
from fractions import Fraction as F
import json
from verify_adaptive import p,independent_acquire,verify
sp,raw=p.demo_network()
# Neutrality constraints cannot be bypassed by total conservation or WR.
# This separately reversible cubic pair forces v_B=v_C, contradicting positive
# production at the existing pure 2C source.
conflict=raw+[((0,3,0),(0,0,3),F(1)),((0,0,3),(0,3,0),F(1))]
r=p.recognize(sp,conflict);assert r['accepted']
c=p.construct(r,max_bases=None);_,a=independent_acquire(r)
assert not c['accepted'] and c['algebraic_cone_exhausted']
assert a['basis'] is None and c['basis_attempts']==a['attempts']==a['total']
assert c['network_stability']=='UNKNOWN'
# Raw normalization: split one rate into two positive channels and add a null.
u,v,k=raw[0];normalized=[(u,v,F(2,5)),(u,v,F(3,5))]+raw[1:]+[((1,1,1),(1,1,1),F(123))]
r2=p.recognize(sp,normalized);c2=p.construct(r2);verify(r2,c2)
r0=p.recognize(sp,raw);c0=p.construct(r0)
assert c0==c2
# Unsupported scalar boundary is an explicit API assertion, not silently covered.
try:p.recognize(['A'],[((0,),(1,),F(1)),((1,),(0,),F(1))])
except AssertionError:scalar_rejected=True
else:raise AssertionError('scalar input unexpectedly accepted')
print(json.dumps({'conflicting_cubic_pair':c,'independent_exhausted_bases':a['total'],
 'split_rate_and_null_channel_certificate_unchanged':True,'scalar_n1_explicitly_outside_API':scalar_rejected},default=p.encode,indent=2))
