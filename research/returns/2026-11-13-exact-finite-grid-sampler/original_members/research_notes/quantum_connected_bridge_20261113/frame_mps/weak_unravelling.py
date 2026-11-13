"""Exact weak-XX + product-Pauli unravelling of the target nonreset channel."""
import numpy as np,time,json
from pathlib import Path
from mps_sampler import MPOMPS,ResourceLimit,PHI,zz,X,I
from compact import CompactMPS

def factors(r,eps):
 a=eps/(1-r);lam=1-a+a*(119-120j)/169;eta=abs(lam);beta=-np.angle(lam)/2;return beta,(1-eta)/2,lam

def sample(n,layers,r,eps,rng,chi=64,error_budget=1e-4,max_cpu=10,max_wall=30,validate=False):
 start=time.perf_counter();cpu=time.process_time();beta,p,lam=factors(r,eps);U=np.cos(beta)*np.eye(4)-1j*np.sin(beta)*np.kron(X,X)
 G=2*sum(map(len,layers));m=MPOMPS(0,chi=chi,strict=True);m.cpu_deadline=cpu+max_cpu;m.wall_deadline=start+max_wall;c=CompactMPS(m,n,list(range(n)),gate_budget=error_budget/max(1,G))
 v=np.zeros(1<<n,complex) if validate else None
 if validate:v[0]=1
 from sampler import bitphase,project
 born=0.;resets=0;flips=0
 def phase(u,v):
  if c.bits[u] is not None and c.bits[v] is not None:return
  if c.bits[u] is not None:c.one(v,np.diag(np.exp(1j*PHI*(1-2*c.bits[u])*np.array([1,-1]))));return
  if c.bits[v] is not None:c.one(u,np.diag(np.exp(1j*PHI*(1-2*c.bits[v])*np.array([1,-1]))));return
  c.pair(u,v,zz(PHI))
 for lay in layers:
  for u,w in lay:
   if rng.random()<r:
    resets+=1
    for s in (u,w):
     b,prob=c.measure(s,rng)
     if validate:v,pd=project(v,s,b);born=max(born,abs(prob-pd))
     new=int(rng.integers(2))
     if b!=new:
      c.one(s,X)
      if validate:v=v[np.arange(len(v))^(1<<s)]
   else:
    phase(u,w);c.pair(u,w,U)
    if validate:
     v*=bitphase(n,[u,w],PHI);v=np.cos(beta)*v-1j*np.sin(beta)*v[np.arange(len(v))^((1<<u)|(1<<w))]
    if rng.random()<p:
     flips+=1;c.one(u,X);c.one(w,X)
     if validate:v=v[np.arange(len(v))^((1<<u)|(1<<w))]
 stats=dict(beta=beta,pauli_probability=p,max_bond=c.maxchi,max_active=c.max_active,svds=c.svds,pair_calls=c.pair_calls,path_error_sum=float(c.error),resets=resets,flips=flips,born_error=born)
 if validate:stats['conditional_TV']=float(sum(abs(abs(c.vector())**2-abs(v)**2))/2)
 result=0
 for s in range(n):b,_=c.measure(s,rng);result|=b<<s
 stats.update(seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,aborted=False);return result,stats

def safe_sample(*a,**kw):
 t=time.perf_counter();cpu=time.process_time()
 try:return sample(*a,**kw)
 except ResourceLimit as e:
  s=e.args[0];s.update(seconds=time.perf_counter()-t,cpu_seconds=time.process_time()-cpu);return 0,s

def channel_check():
 out=[];theta=np.arctan2(5,12);Q=np.cos(theta)*np.eye(4)-1j*np.sin(theta)*np.kron(X,X)
 for r,eps in[(.03,.02),(.03,.05),(.3,.2)]:
  beta,p,lam=factors(r,eps);U=np.cos(beta)*np.eye(4)-1j*np.sin(beta)*np.kron(X,X);P=np.kron(X,X)
  old=(1-eps/(1-r))*np.eye(16)+eps/(1-r)*np.kron(Q,Q.conj());new=(1-p)*np.kron(U,U.conj())+p*np.kron(P@U,(P@U).conj());out.append(dict(r=r,eps=eps,beta=beta,p=p,max_superoperator_error=float(np.max(abs(old-new)))))
 return out
if __name__=='__main__':
 rows=[]
 for seed in range(20):
  _,s=sample(6,[[(0,1),(2,3),(4,5)],[(1,2),(3,4)],[(0,3),(1,4),(2,5)],[]]*10,.03,.05,np.random.default_rng(seed),validate=True,error_budget=1e-10);rows.append(s)
 out=dict(channels=channel_check(),trajectories=rows);Path(__file__).with_name('weak_validation.json').write_text(json.dumps(out,indent=2));print(out['channels']);print(max(s['conditional_TV'] for s in rows),max(s['born_error'] for s in rows))
