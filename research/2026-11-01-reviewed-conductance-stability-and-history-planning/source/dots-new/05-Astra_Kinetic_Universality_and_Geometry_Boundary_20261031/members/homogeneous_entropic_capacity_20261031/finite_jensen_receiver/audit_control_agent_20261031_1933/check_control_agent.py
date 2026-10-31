from fractions import Fraction as F
from pathlib import Path
import receive_jensen as j
import json,copy,random
count=0;groups={}
def ok(v,g):
 global count
 assert v,g
 count+=1;groups[g]=groups.get(g,0)+1
def no(fn,g):
 try:fn()
 except j.Unknown:ok(True,g);return
 raise AssertionError('accepted '+g)
# Exact rational m=4 integrand: independent Darboux endpoints, not fourth-root reuse.
for k in [F(1,13),F(1),F(21,4)]:
 for N in [1,3,11]:
  a=1+k;f=lambda y:a*a/(2*a-(1+k*(1-y*y)**2))
  h=F(1,2*N);exactlo=h*sum(f(i*h) for i in range(1,N+1));exacthi=h*sum(f(i*h) for i in range(N))
  ii=j.PlusIntegrator(4,k,40,1000,10000);lo,hi=ii.integrate(F(0),F(1,2),N,1)
  ok(lo<=exactlo<=exacthi<=hi,'exact_darboux')
  ok(exactlo-lo<=F(1,2**41) and hi-exacthi<=F(1,2**41),'root_rounding')
# Exact identity and monotonicity, several alpha values including noninteger.
for m in [2,3,5,12]:
 for k in [F(1,100),F(7,3)]:
  ii=j.PlusIntegrator(m,k,50,1000,100000);prior=None
  for y in [F(x,22) for x in range(12)]:
   a=1+k;v=1+k*(1-y*y)**2;r=a*a/(2*a-v);lo,hi=ii.point(y)[1]
   ok(r>=v and (F(lo,2**50)**4<=r**m<=F(hi,2**50)**4),'powered_enclosure')
   if prior is not None:ok(hi<=prior,'monotone')
   prior=hi
raw=j.base.fixture(3);kw={'quad_relative':F(1,5)};c=j.certify(raw,**kw)
# Global evaluation budget boundary, includes full inherited failed-refinement history.
total=c['total_scalar_evaluations'];ok(total==c['point_evaluations']+c['N']+1,'budget')
no(lambda:j.certify(raw,max_points=total-1,**kw),'budget');cc=j.certify(raw,max_points=total,**kw);ok(cc['total_scalar_evaluations']==total,'budget')
ratio=F(c['full_ratio_exact']);exact=j.certify(raw,full_ratio=ratio,**kw);ok(j.verify(raw,exact,full_ratio=ratio,**kw)['status']=='PASS','width')
no(lambda:j.certify(raw,full_ratio=(ratio+1)/2,**kw),'width');no(lambda:j.verify(raw,exact,**kw),'width');no(lambda:j.verify(raw,c,full_ratio=F(2),**kw),'width')
for key in ['mass','resistance','free_rate','jensen_resistance','structural_ratio','full_rate']:
 for side in ['lower','upper']:
  d=copy.deepcopy(c);d[key][side]=str(F(d[key][side])+1);no(lambda d=d:j.verify(raw,d,**kw),'endpoint_binding')
for key in ['schema','structural_method','scalar_source_sha256','full_ratio_exact','b','observable','basins','T','tail_upper']:
 d=copy.deepcopy(c);d[key]='invalid';no(lambda d=d:j.verify(raw,d,**kw),'task_binding')
def leaves(x,p=()):
 if type(x)is int:yield p,x
 elif type(x)is dict:
  for k,v in x.items():
   if k!='seconds':yield from leaves(v,p+(k,))
 elif type(x)is list:
  for k,v in enumerate(x):yield from leaves(v,p+(k,))
for path,val in leaves({k:c[k] for k in ['acquisition','task','N','precision_bits']}):
 for a in [float(val),bool(val)]:
  d=copy.deepcopy(c);o=d
  for key in path[:-1]:o=o[key]
  o[path[-1]]=a;no(lambda d=d:j.verify(raw,d,**kw),'typed_binding')
for val in [True,1,1.0,F(1),F(0),F(-1),float('nan'),float('inf')]:no(lambda val=val:j.certify(raw,full_ratio=val),'requested_type')
for val in [None,[],True]:no(lambda val=val:j.verify(raw,val,**kw),'record')
# Invalid slab and new-point budget checks happen before powers.
ii=j.PlusIntegrator(3,F(1),20,0,10000);no(lambda:ii.point(F(0)),'helper_budget');ok(ii.power_calls==0,'helper_budget')
ii=j.PlusIntegrator(3,F(1),20,20,10000)
for y in [F(-1,100),F(51,100)]:no(lambda y=y:ii.point(y),'slab')
ok(ii.power_calls==0,'slab')
# Graph and beta affect acquisition/task, but the exact structural ratio is unchanged.
cc=j.certify(j.base.fixture(3,graph='complete',coupling=F(10**20),dmin=F(1,19),axis=2),beta=F(3),**kw)
ok(cc['structural_ratio']==c['structural_ratio'],'model_scope')
for side in ['lower','upper']:ok(F(cc['full_rate'][side])*3==F(c['full_rate'][side]),'model_scope')
no(lambda:j.verify(j.base.fixture(3,coupling=F(21)),c,**kw),'model_scope')
print(json.dumps({'status':'PASS','independent_checks':count,'groups':groups},indent=2))
