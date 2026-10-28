import json,hashlib,math
from pathlib import Path
# Exact rational score/guard and interval logic checks; no sampled-confidence claim.
from fractions import Fraction as F
checks=0
for n in range(1,11):
 for w in range(1,n+1):
  ints=[(a,b) for a in range(n) for b in range(a,min(n,a+w))]
  for I in ints:
   for J in ints:
    overlap=not(I[1]<J[0] or J[1]<I[0])
    if overlap:
     E=(max(0,J[0]-w+1),min(n-1,J[1]+w-1));assert E[0]<=I[0]<=I[1]<=E[1];assert E[1]-E[0]+1<=3*w-2;checks+=1
    else:assert I in [K for K in ints if K[1]<J[0] or J[1]<K[0]]
# n2,w1 physical gauge-contrast example from normal-cone source.
vL=F(5,8);vG=F(5,16);h=F(1,20)
assert vL-h>vG+h
mu=F(3,8);d=4;assert vL-vG>=3*mu*d/16
# Trace-down gap: local depolarizing logical marginal has gap1; inherited bound3/4.
assert F(1)>=2*mu
# Fixed-width-only false vacuous case n5,w3,I={2},J=[3,5] in 1-based notation.
J=(3,5);I=(2,2);fixed=[(a,a+2) for a in range(1,4)]
assert not [K for K in fixed if K[1]<J[0] or J[1]<K[0]]
assert I[1]<J[0]
# Conservative real source-call horizon for n2,w1 common-bank score radius h=.05.
M=18;L=9;beta=.05;eta=float(4*h/(3*2));N=math.ceil(2*L*L*math.log(2*M/beta)/eta**2)
out={'status':'PASS_EXHAUSTIVE_INTERVAL_LOGIC_AND_EXACT_PHYSICAL_SCORES','overlap_expansion_checks':checks,'logical_score':str(vL),'gauge_score':str(vG),'nonzero_gauge_contrast':'Z/8','score_halfwidth':str(h),'logical_guard_passes':True,'fixed_width_false_vacuity_preserved':True,'conservative_common_bank_calls_for_stated_score_halfwidth':N,'scope':'Exact interval and known-channel score fixtures only. No actual finite-confidence acquisition, generic SDP or generator fitting executed.'};p=Path(__file__);out['source_sha256']=hashlib.sha256(p.with_name('normal_cone_all_interval_localization_20261028.md').read_bytes()).hexdigest();p.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
