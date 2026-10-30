"""Finite classical regressions only; the quantum theorem is analytic."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
out={}; worst=0.; tested=0
# Shared Poisson kick marks both owners. Each owner resets at rate 1.
# Scalar witness Z=I: alpha=r=D=1; use rho=1/2, b=2,P=1,Delta=1.
for eps in [.001,.01,.05]:
 for theta in [.1,.5,1.]:
  A=np.zeros((4,4))
  for state in range(4):
   # Kick channel sets both mark bits, including its self-loop convention.
   A[3,state]+=eps;A[state,state]-=eps
   for h in range(2):
    if state>>h&1:
     A[state&~(1<<h),state]+=np.exp(theta)
     A[state,state]-=1
  for horizon in [1,2,5,10]:
   mgf=np.ones(4)@expm(horizon*A)[:,0]
   logbound=eps*3*horizon*(np.exp(2*theta)-1)
   assert np.log(mgf)<=logbound+1e-10,(eps,theta,horizon,mgf,logbound)
   worst=max(worst,float(np.log(mgf)-logbound));tested+=1
out['tilted_CTMC_cases']=tested;out['all_marked_emission_mgfs_below_bound']=True
# Random record check: last-ancestor multiplicity and representative intervals.
rng=np.random.default_rng(1729);records=0;checks=0;max_mult=0;repeated=0
for _ in range(1000):
 events=[]
 for e,H in enumerate([(0,1),(1,2)]):
  for t in rng.uniform(0,10,rng.poisson(12)):events.append((float(t),'kick',e,H))
 for h in range(3):
  for t in rng.uniform(0,10,rng.poisson(20)):events.append((float(t),'reset',h,None))
 events.sort();last=[None]*3;anc={};desc={}
 for idx,(t,kind,x,H) in enumerate(events):
  if kind=='kick':
   anc[idx]=(t,H)
   for h in H:last[h]=idx
  elif last[x] is not None:
   a=last[x];desc.setdefault(a,[]).append((x,int(t),t));last[x]=None
 for a,ds in desc.items():
  assert len(ds)<=2 and len({x[0] for x in ds})==len(ds)
  max_mult=max(max_mult,len(ds))
 # One representative per distinct ancestor; all destinations are included.
 reps=[(anc[a][0],*sorted(ds)[0]) for a,ds in desc.items()]
 for i,(tau,h,s,u) in enumerate(reps):
  for tau2,h2,s2,u2 in reps[i+1:]:
   if h==h2:
    repeated+=int(s==s2)
    assert max(tau,tau2)>=min(s,s2) or tau>=s or tau2>=s2,(reps,h)
    checks+=1
 records+=1
out.update(random_records=records,same_owner_interval_checks=checks,repeated_same_owner_cell_checks=repeated,max_descendants_per_kick=max_mult)
# Negative regression: initially marked owner can emit at epsilon=0.
out['initial_mark_counterexample_probability_by_time1']=float(1-np.exp(-1))
out['scope']='Classical finite regression of count envelope and ancestor combinatorics, not a proof of quantum factorization'
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
