"""Same-author exact checks. Not an independent review and not a tail proof."""
import multiface as M
from fractions import Fraction as F
from itertools import product
from random import Random
import json,time,hashlib
from pathlib import Path
rng=Random(87023);root=Path(__file__).resolve().parent
counts=dict(fixtures=0,selected_sources=0,profile_bounds=0,local_source_inequality=0,subset_elimination=0,global_sum=0,inactive_join=0,last_death=0,raw_rejections=0,budget_refusals=0)
fixtures=[M.fixture(2,((0,1),)),M.fixture(3,((0,1),(1,2))),M.fixture(4,((0,1),(0,2),(1,2))),M.fixture()]
for fi,raw in enumerate(fixtures):
 p=M.construct(raw);r=p['raw'];n=r['n'];counts['fixtures']+=1
 print('fixture',fi,'faces',len(p['faces']),'M',p['M'],flush=True)
 for j in range(120):
  z=M.profile(p,j);dd=M.diff(p,j)
  assert 0<z<=F(1,j+1)
  assert F(1,8*(j+p['s0']+1)**2)<=dd<=F(1,(j+1)**2)
  counts['profile_bounds']+=1
 groups={}
 for u,v,k in r['internal']:groups.setdefault(u,[]).append((v,k))
 for face in p['faces']:
  for u,out in groups.items():
   bulkcap=u[r['A']]==1 and any(u[i] for i in face['I'])
   onebulk=sum(u[i] for i in face['I'])==1 and u[r['A']]==0
   farhub=u[r['A']]==0 and sum(u[i] for i in face['Far'])==2
   if not(bulkcap or onebulk or farhub):continue
   gap=-sum((k*(p['q']**(-sum(w*(vv-uu) for w,uu,vv in zip(face['resource_weights'],u,v)))-1) for v,k in out),F(0))
   assert gap>0
   assert gap/(p['q']-1)>=(p['g'] if bulkcap else p['h'])
   counts['selected_sources']+=1
 states=list(product(range(3),repeat=r['m'])) if r['m']<=4 else [tuple(rng.randrange(5) for _ in range(r['m'])) for _ in range(100)]
 # Deliberate independent-support and pure-bulk boundary states.
 for face in p['faces']:
  for av in [0,1,2]:
   x=[0]*r['m'];x[r['A']]=av
   for j,i in enumerate(sorted(face['I'])):x[i]=10+j*3
   states.append(tuple(x))
 byI={f['I']:f for f in p['faces']}
 for x in states:
  A=x[r['A']];N=sum(x);Q=sum(x[u]*x[v] for u,v in r['edges']);stats={f['I']:M.face_stats(p,f,x) for f in p['faces']}
  for f in p['faces']:
   st=stats[f['I']];fn=lambda y,f=f:M.profile(p,sum(w*z for w,z in zip(f['resource_weights'],y)))
   actual=M.generator(p,x,fn,t=F(2))
   local=r['lam']*st['Z']-st['r']+p['CA']*A*(st['U']+1)*st['D']+p['CH']*st['Qbad']*st['D']
   assert actual<=local
   counts['local_source_inequality']+=1
   large=frozenset(i for i in f['I'] if x[i]>=p['T']*(st['U']+1))
   if large:
    bound=r['lam']*st['Z']-F(3,4)*st['r']
    if large!=f['I']:
     sj=stats[large];bound+=p['CH']*p['R']*sj['Qfar']*sj['D']
     assert st['D']<=p['R']*sj['D']
   else:bound=r['lam']*st['Z']-F(3,4)*st['r']+p['CA']*(p['B']+1)*A/F(N+1)+p['CH']*(p['B']+1)**2*Q/F((N+1)**2)
   assert actual<=bound
   counts['subset_elimination']+=1
  Psi=sum(f['weight']*stats[f['I']]['Z'] for f in p['faces']);S=sum(f['weight']*stats[f['I']]['r'] for f in p['faces'])
  actual=M.generator(p,x,lambda y:M.psi(p,y),t=F(2));bound=r['lam']*Psi-S/2+p['RA']*A/F(N+1)+p['RQ']*Q/F((N+1)**2)
  assert actual<=bound
  counts['global_sum']+=1
  if A==0 and Q==0:
   assert M.generator(p,x,lambda y:M.value(p,y))<=-r['lam'];counts['inactive_join']+=1
  if A==1 and Q==0 and N>=2:
   assert S>=p['g']*(N-1)*M.diff(p,p['aw']);counts['last_death']+=1
 # Symbolic constructor tail inequalities, including conservative dA.
 assert p['Nstar']>=4*p['RA']/p['D'] and p['Nstar']>=p['RQ']/(p['e']*r['b'])
 assert p['Nstar']>=1+4*r['mu']*p['H']/(p['g']*p['da_lower'])
 assert p['eps']*p['Cbirth']<=p['sstar']/16
 assert M.diff(p,p['aw'])>=p['da_lower']
 try:M.profile(p,p['M']+10,max_power=1)
 except M.BudgetRefusal:counts['budget_refusals']+=1
 else:raise AssertionError('power refusal')
 try:M.construct(raw,max_masks=1)
 except M.BudgetRefusal:counts['budget_refusals']+=1
 else:raise AssertionError('mask refusal')
 for bad in [raw[:-1],raw+[(raw[0][0],raw[0][1],F(-1))]]:
  try:M.recognize(bad)
  except M.Unsupported:counts['raw_rejections']+=1
  else:raise AssertionError('raw rejection')
result=dict(status='PASS_SAME_AUTHOR_COMPONENT_AND_FINITE_STATE_CHECKS_NOT_INDEPENDENT_WHOLE_REVIEW',counts=counts,bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['THEOREM_PENDING.md','multiface.py','check_author.py']})
(root/'author_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
