import numpy as np,json,sys
from pathlib import Path
from mps_sampler import plan,PHI,A,B
from cycle_cuts import schedule
def last_q_sites(n,records):return schedule(n,records)[0]
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'frame_sampler'))
from sampler import bitphase

def evolve(n,records,early):
 d=1<<n;x=np.arange(d);rho=np.zeros((d,d),complex);rho[0,0]=1;last=last_q_sites(n,records)
 for t,(events,_,_,_) in enumerate(records):
  for (u,v),reset,rare,cand in events:
   ph=bitphase(n,[u,v],PHI);rho=ph[:,None]*rho*ph.conj()[None,:]
  for (u,v),reset,rare,cand in events:
   if rare:
    perm=x^((1<<u)|(1<<v));rho=A*A*rho+B*B*rho[np.ix_(perm,perm)]+1j*A*B*(rho[:,perm]-rho[perm,:])
  if early:
   for site in last[t]:
    bits=(x>>site)&1;rho=rho*(bits[:,None]==bits[None,:])
  for (u,v),reset,rare,cand in events:
   if reset:
    mask=(1<<u)|(1<<v);rest=x[(x&mask)==0];shifts=[0,1<<u,1<<v,mask];z=np.zeros_like(rho)
    block=sum(rho[np.ix_(rest+s,rest+s)] for s in shifts)/4
    for s in shifts:z[np.ix_(rest+s,rest+s)]=block
    rho=z
 return np.diag(rho).real
rows=[]
for r,eps in [(.03,.02),(.03,.2),(.3,.2)]:
 for seed in range(100):
  rec,_,_,_=plan(4,[[(0,1),(2,3)],[(0,2),(1,3)]]*10,r,eps,np.random.default_rng(seed))
  a=evolve(4,rec,False);b=evolve(4,rec,True);rows.append(dict(r=r,eps=eps,seed=seed,TV=float(sum(abs(a-b))/2)))
Path(__file__).with_name('cycle_cut_validation.json').write_text(json.dumps(rows,indent=2));print('300 cycle-cut exact-category, all-outcome-summed channels max TV:',max(s['TV'] for s in rows))
