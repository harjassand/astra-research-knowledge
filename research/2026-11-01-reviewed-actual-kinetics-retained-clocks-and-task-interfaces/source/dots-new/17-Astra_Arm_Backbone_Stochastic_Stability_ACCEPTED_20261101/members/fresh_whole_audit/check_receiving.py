from fractions import Fraction as F
from itertools import product
from copy import deepcopy
from pathlib import Path
import sys,os,json
import independent_backbone as I
sys.path.insert(0,os.environ.get('BACKBONE_SOURCE_DIR','producer-workspace/stochastic_arm_backbone_recovery_20261101'));import arm_backbone as A
counts={};hit=lambda k,n=1:counts.__setitem__(k,counts.get(k,0)+n)
raw=A.fixture();r=I.parse(raw);c=I.construct(raw,2);wire=json.loads(I.canonical(c));assert I.receive(raw,2,wire);hit('wire_receipt')
for path in(('mass_head','K'),('mass_head','Q'),('mass_head','L0'),('mass_head','Jcoef'),('mass_head','nu'),('plan','core','rho0'),('plan','core','Qhead'),('work','compensation_steps')):
 bad=deepcopy(wire);d=bad
 for key in path[:-1]:d=d[key]
 old=d[path[-1]];d[path[-1]]=str(F(old)+1)if isinstance(old,str)else old+1;assert not I.receive(raw,2,bad);hit('semantic_mutations')
for p in(0,1,10,1000,10000):
 for a in(0,1,2):
  x=[0]*r['n'];x[r['a']]=a
  for f in r['free']:x[f]=10**p
  assert I.scaled(r,c,x)==A.scaled_value(A.recognize(raw),c,x)
  assert I.drift(r,c,x)==A.scaled_drift(A.recognize(raw),c,x);assert not I.outside(c,sum(x));hit('actual_zero_cutoff_scaled_receiving')
for K in(2,3,8):
 s=deepcopy(c);s['plan']['mass']['K']=K;s['mass_head']=I.head(s['plan'],r);s['mass_head']['Jcoef']=1;h=s['mass_head']
 for a in(0,1,2):
  for rare in(0,1,2):
   for offset in(1,2,30):
    x=[rare]*r['n'];x[r['a']]=a
    for f in r['free']:x[f]=0
    U=sum(x);x[r['free'][0]]=((U+1)<<(h['L0']+offset))-1
    assert I.scaled(r,s,x)==A.scaled_value(A.recognize(raw),s,x);hit('synthetic_positive_cutoff_receiving')
for Q in(2,3,5):
 for K in(0,1,2,3):
  for L0 in(0,3):
   for jc in(1,2):
    s=deepcopy(c);s['mass_head'].update(Q=Q,K=K,L0=L0,Jcoef=jc,outer_head_coefficients=(F(1),F(1,2),F(1,4)))
    U=2*((1<<(L0+jc*Q**K+1))+1);ns=I.ceil(1+U+F(1,2)*U**2+F(1,4)*U**4)
    for N in(0,ns-1,ns,ns+1):assert I.outside(s,N)==A.outside_head(s,N)==(N>=ns);hit('nested_head_comparisons')
for b in range(2,9):
 for e in range(15):
  for cap in(0,1,b**e-1,b**e,b**e+1):assert I.I.pow_leq(b,e,cap)==(A.power_at_most(b,e,cap)is not None)==(b**e<=cap);hit('bounded_power_comparisons')
dag=I.dag(raw,c);assert I.canonical(dag)==I.canonical(A.certificate_expressions(raw,c))
for name in dag['outputs']:
 x=I.evaluate(dag,name,1000);y=A.evaluate_expression(dag,name,1000);assert x['status']==y['status']and x['required_upper_power_bits']==y['required_upper_power_bits'];hit('actual_DAG_expansion_refusals')
for K in(2,3,4):
 s=deepcopy(c);s['mass_head'].update(K=K,Q=2,L0=0,Jcoef=1,outer_head_coefficients=(F(1),F(1,2),F(1,4)),H_coefficients=(F(2),F(3)),nu=F(1,7));d=I.dag(raw,s)
 for name in('Bhead','cutoff_exponent','Ucut','Nstar','H','zeta'):assert I.evaluate(d,name,10000)==A.evaluate_expression(d,name,10000);hit('synthetic_DAG_values')
 for name in('Foster_constant','stationary_bound'):assert I.evaluate(d,name,10000)['status']=='UNKNOWN_POWER_INTERMEDIATE_BUDGET';hit('synthetic_DAG_budget_refusals')
s=deepcopy(c);s.update(status='PENDING_CORE_ONLY_FOSTER',head=3,H=F(5),zeta=F(1,11));d=I.dag(raw,s)
for name in d['outputs']:assert I.evaluate(d,name)==A.evaluate_expression(d,name);hit('core_only_DAG_values')
for bad in({},dict(format='wrong',nodes=[],outputs={}),dict(format='exact-rational-dag-v1',nodes=[['q',True,1]],outputs={'x':0}),dict(format='exact-rational-dag-v1',nodes=[['add',0]],outputs={'x':0}),dict(format='exact-rational-dag-v1',nodes=[['q',1,0]],outputs={'x':0}),dict(format='exact-rational-dag-v1',nodes=[['q',1,1]],outputs={'x':-1})):
 try:I.evaluate(bad,'x')
 except ValueError:hit('bad_DAG_refusals')
 else:raise AssertionError('bad DAG')
rows=[]
for t,af,ar in[(F(7,5),F(1,1000),F(1000)),(F(17,5),F(100),F(1,100))]:
 rr=[]
 for idx,(u,v,k)in enumerate(raw):
  if sum(u)==0:k=F(2,7)
  elif sum(v)==0:k=F(11,3)
  elif u[4]+u[5]==2:k=ar
  elif v[4]+v[5]==2:k=af
  else:k*=F(idx%3+2,idx%2+1)
  rr.append((u,v,k))
 rec=I.parse(rr);cc=I.construct(rr,t,250000);assert I.canonical(cc)==I.canonical(A.construct(rr,t,250000));hit('joint_fractional_receipts')
 co=cc['plan']['core'];K=cc['mass_head']['K']
 for x in product(range(2),repeat=rec['n']):assert I.drift(rec,cc,x)<=co['C0'];hit('fractional_core_states')
 for j in range(K-6,K+5):
  g=I.I.evaluate(I.I.mass_g(cc,j));gp=I.I.evaluate(I.I.mass_g(cc,j+1));assert g-gp>=F(1,(j+1)**2)
  if j<K:assert g>=2*t*(I.I.evaluate(I.I.mass_g(cc,j+2))+cc['plan']['mass']['rho'])
  hit('fractional_actual_head_joins')
 rows.append(dict(t=t,q=cc['mass_head']['q'],Q=cc['mass_head']['Q'],steps=cc['plan']['core_profile_steps'],K=K,receipt_sha256=I.digest(cc)))
for t,scale in((F(1001,1000),F(1000)),(F(3,2),F(7)),(F(2),F(1,1000000))):
 rr=[(u,v,k*(scale if sum(u)==2 and u[r['a']]==0 else 1))for u,v,k in raw];u=I.construct(rr,t,0);assert I.canonical(u)==I.canonical(A.construct(rr,t,0))and u['qualitative']['status']!='UNKNOWN';hit('extreme_budget_retains_qualitative')
Path(__file__).with_name('MAIN_DAG.json').write_text(I.canonical(dag)+'\n')
res=dict(status='PASS_FRESH_INDEPENDENT_RECEIVING',counts=counts,parameters=rows,main_bytes=len(I.canonical(c).encode()),main_sha256=I.digest(c),dag_nodes=len(dag['nodes']),dag_bytes=len(I.canonical(dag).encode()),dag_sha256=I.digest(dag),scope='Fresh source binding and fresh independently authored checks. Actual huge powers not expanded. Matching historical outputs does not assert historical source identity.')
Path(__file__).with_name('RECEIVING_RESULTS.json').write_text(json.dumps(I.P.wire(res),indent=2)+'\n');print(json.dumps(counts),flush=True)
