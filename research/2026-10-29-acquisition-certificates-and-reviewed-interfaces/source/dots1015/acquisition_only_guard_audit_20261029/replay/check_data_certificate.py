"""Exact arithmetic tests; synthetic counters do not demonstrate physical yield."""
from exact_data_certificate import *
from copy import deepcopy
import json,random
from pathlib import Path
rng=random.Random(29026)
for i in range(1000):
 v=F(rng.randrange(10**12),rng.randrange(1,10**9)); b=rng.randrange(0,65); u=root_upper(v,b)
 assert u*u>=v and (u==0 or (u-F(1,2**b))**2<v)
def record(h):
 J=16*h*2**h;T=3*J
 return dict(horizon=T,service_target=J,correction_radius=J//256,services_completed=J,probe_count=0,active_calls=J,probe_probability='1/3',perturbation_amplitude=str(720*isqrt(T)),midpoint_bank_size=2**(2*T.bit_length()+8),raw_transfer_factor=8,failure_budget_exponents=[20]*3,verified_code=True,resource_abort=False,edges=[dict(quaternion=[1,0,0,0],coefficients=[],reported_gap_sum=0,squared_feedback_sum=0) for _ in range(3)])
r=record(160);out=certify(r);assert out['accept']
for key,value in [('verified_code',False),('resource_abort',True)]:
 z=deepcopy(r);z[key]=value;assert not certify(z)['accept']
z=deepcopy(r);z['services_completed']-=1;z['active_calls']-=1;assert not certify(z)['accept']
z=deepcopy(r);z['edges'][0]['reported_gap_sum']=1;assert F(certify(z)['virtual_bad_count_upper'])>=F(out['virtual_bad_count_upper'])
invalid=[]
for name,edit in [('alpha',lambda z:z.update(raw_transfer_factor=7)),('quaternion',lambda z:z['edges'][0].update(quaternion=[1,1,0,0])),('negativegap',lambda z:z['edges'][0].update(reported_gap_sum=-1)),('feedback',lambda z:z['edges'][0].update(coefficients=[([4,0,0,0],1)])),('oddspins',lambda z:z['edges'].pop()),('counts',lambda z:z.update(active_calls=0))]:
 z=deepcopy(r);edit(z)
 try:certify(z)
 except ValueError:invalid.append(name)
 else:raise AssertionError(name)
# Nontrivial exact monomial calculation.
ed=[dict(quaternion=['3/5','4/5',0,0],coefficients=[([2,2,0,0],'7/3')])]
assert empirical_score(ed,2,F(1,3))==F(9,2)+F(7,6)*F(144,625)
result=dict(root_checks=1000,invalid_contracts_rejected=invalid,synthetic_h160=out,scope='Synthetic arithmetic only; no acquired data, outer code deployment, physical acceptance or positive yield demonstrated.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
